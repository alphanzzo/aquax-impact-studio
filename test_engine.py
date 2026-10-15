




import pytest

from engine import (
    calculate_metrics,
    calculate_scope2_reduction,
    calculate_historical_baseline,
)



@pytest.fixture
def example_inputs():
    return {
        "influent_m3_day": 1000,
        "baseline_kwh_m3": 1.0,
        "optimized_kwh_m3": 0.8,
        "operating_days": 365,
        "grid_ef": 0.402,
        "baseline_chemical_kg_day": 100,
        "chemical_reduction_pct": 15,
        "reuse_m3_day": 700,
        "quality": "Illustrative Benchmark",
    }


def test_energy_saved(example_inputs):
    results = calculate_metrics(example_inputs)
    energy = results["energy_saved"]

    assert energy["daily"]["value"] == pytest.approx(200.0)
    assert energy["annual"]["value"] == pytest.approx(73000.0)


def test_scope2_reduction(example_inputs):
    results = calculate_metrics(example_inputs)
    ghg = results["scope2_reduction"]

    assert ghg["value"] == pytest.approx(29.346)
    assert ghg["unit"] == "tCO2e"


def test_chemical_avoided(example_inputs):
    results = calculate_metrics(example_inputs)
    chemical = results["chemical_avoided"]

    assert chemical["daily"]["value"] == pytest.approx(15.0)
    assert chemical["annual"]["value"] == pytest.approx(5475.0)


def test_water_reuse(example_inputs):
    results = calculate_metrics(example_inputs)
    water = results["water_reuse"]

    assert water["daily"]["value"] == pytest.approx(700.0)
    assert water["annual"]["value"] == pytest.approx(255500.0)

    



@pytest.mark.parametrize("bad_value", [
    -1,
    float("nan"),
    float("inf"),
    -float("inf"),
    "hello",
    None,
])
def test_invalid_influent_flow_is_rejected(example_inputs, bad_value):
    example_inputs["influent_m3_day"] = bad_value

    with pytest.raises((ValueError, TypeError)):
        calculate_metrics(example_inputs)


def test_reduction_above_100_is_rejected(example_inputs):
    example_inputs["chemical_reduction_pct"] = 150

    with pytest.raises((ValueError, TypeError)):
        calculate_metrics(example_inputs)






def test_historical_baseline_uses_total_volume():
    electricity = [1000] + [9000] + [0] * 10
    water = [1000] + [3000] + [0] * 10

    result = calculate_historical_baseline(
        electricity,
        water,
        quality="Illustrative Benchmark",
    )

    assert result["value"] == pytest.approx(2.5)
    assert result["unit"] == "kWh/m3"


def test_historical_baseline_requires_12_months():
    with pytest.raises(ValueError):
        calculate_historical_baseline(
            [1000, 9000],
            [1000, 3000],
        )


def test_historical_baseline_rejects_zero_total_water():
    with pytest.raises(ValueError):
        calculate_historical_baseline(
            [1000] * 12,
            [0] * 12,
        )

        

def test_scope2_includes_emission_factor_metadata():
    ghg = calculate_scope2_reduction(
        energy_saved_kwh=73000
    )

    assert ghg["emission_factor"] == pytest.approx(0.402)
    assert ghg["factor_unit"] == "kgCO2e/kWh"
    assert ghg["factor_source"] == (
        "EMA — exact publication to be confirmed"
    )
    assert ghg["factor_year"] == 2024
    assert ghg["factor_status"] == "provisional"


    


def test_custom_grid_factor_metadata():
    ghg = calculate_scope2_reduction(
        energy_saved_kwh=1000,
        grid_ef=0.500
    )

    assert ghg["value"] == pytest.approx(0.5)
    assert ghg["factor_source"] == "User Input"
    assert ghg["factor_year"] is None
    assert ghg["factor_status"] == "unverified"

def test_historical_baseline_integration(example_inputs):
    inputs = example_inputs.copy()

    # 12 months of historical records
    inputs["monthly_electricity_kwh"] = [2000] * 12
    inputs["monthly_treated_m3"] = [2000] * 12

    results = calculate_metrics(inputs)

    # Historical baseline = 24000 / 24000 = 1.0 kWh/m3
    assert results["historical_baseline"]["value"] == pytest.approx(1.0)

    # Energy saved = (1.0 - 0.8) * 1000 = 200 kWh/day
    assert results["energy_saved"]["daily"]["value"] == pytest.approx(200)

def test_historical_baseline_overrides_manual(example_inputs):
    inputs = example_inputs.copy()

    # Manually entered baseline
    inputs["baseline_kwh_m3"] = 1.0

    # Historical baseline = 36000 / 24000 = 1.5 kWh/m3
    inputs["monthly_electricity_kwh"] = [3000] * 12
    inputs["monthly_treated_m3"] = [2000] * 12

    results = calculate_metrics(inputs)

    # Verify the historical baseline
    assert results["historical_baseline"]["value"] == pytest.approx(1.5)

    # Verify energy savings use 1.5, NOT 1.0
    assert results["energy_saved"]["daily"]["value"] == pytest.approx(700)

    # Verify annual energy savings
    assert results["energy_saved"]["annual"]["value"] == pytest.approx(255500)

def test_missing_historical_water_is_rejected(example_inputs):
    inputs = example_inputs.copy()

    inputs["monthly_electricity_kwh"] = [3000] * 12

    with pytest.raises(ValueError):
        calculate_metrics(inputs)


def test_incomplete_historical_records_are_rejected(example_inputs):
    inputs = example_inputs.copy()

    inputs["monthly_electricity_kwh"] = [3000] * 6
    inputs["monthly_treated_m3"] = [2000] * 6

    with pytest.raises(ValueError):
        calculate_metrics(inputs)


def test_negative_energy_savings(example_inputs):
    inputs = example_inputs.copy()

    inputs["monthly_electricity_kwh"] = [1000] * 12
    inputs["monthly_treated_m3"] = [2000] * 12

    results = calculate_metrics(inputs)

    assert results["historical_baseline"]["value"] == pytest.approx(0.5)

    assert results["energy_saved"]["daily"]["value"] == pytest.approx(-300)

    assert results["energy_saved"]["annual"]["value"] == pytest.approx(-109500)

    assert results["scope2_reduction"]["value"] == pytest.approx(-44.019)



def test_historical_baseline_quality(example_inputs):
    inputs = example_inputs.copy()

    # Tell AquaX to label the historical records as measured
    inputs["historical_data_quality"] = "Measured Telemetry"

    inputs["monthly_electricity_kwh"] = [3000] * 12
    inputs["monthly_treated_m3"] = [2000] * 12

    results = calculate_metrics(inputs)

    baseline = results["historical_baseline"]

    assert baseline["value"] == pytest.approx(1.5)
    assert baseline["data_quality"] == "Measured Telemetry"

# Only label genuinely measured historical data as "Measured Telemetry".
# Use "Illustrative Benchmark" for simulated example data.

def test_energy_baseline_source_tracking(example_inputs):
    inputs = example_inputs.copy()
    inputs["historical_data_quality"] = "Measured Telemetry"
    inputs["monthly_electricity_kwh"] = [3000] * 12
    inputs["monthly_treated_m3"] = [2000] * 12

    results = calculate_metrics(inputs)
    energy = results["energy_saved"]

    assert energy["baseline_kwh_m3"] == pytest.approx(1.5)
    assert energy["baseline_source"] == "12-month historical records"
    assert energy["baseline_quality"] == "Measured Telemetry"
#One important detail: your demonstration code at the top of test_engine.py loops through the energy result and assumes every field is a daily or annual metric. These new metadata fields will break that printing loop.

def test_simulated_historical_data_quality(example_inputs):
    inputs = example_inputs.copy()

    inputs["monthly_electricity_kwh"] = [3000] * 12
    inputs["monthly_treated_m3"] = [2000] * 12

    inputs["historical_data_quality"] = "Illustrative Benchmark"

    results = calculate_metrics(inputs)

    assert results["historical_baseline"]["data_quality"] == (
        "Illustrative Benchmark"
    )

    assert results["energy_saved"]["baseline_quality"] == (
        "Illustrative Benchmark"
    )

def test_invalid_historical_data_quality(example_inputs):
    inputs = example_inputs.copy()

    inputs["monthly_electricity_kwh"] = [3000] * 12
    inputs["monthly_treated_m3"] = [2000] * 12
    inputs["historical_data_quality"] = "Random"

    with pytest.raises(ValueError):
        calculate_metrics(inputs)

def test_invalid_main_data_quality(example_inputs):
    inputs = example_inputs.copy()

    inputs["quality"] = "Random"

    with pytest.raises(ValueError):
        calculate_metrics(inputs)

def test_operating_days_above_year_is_rejected(example_inputs):
    inputs = example_inputs.copy()

    inputs["operating_days"] = 500

    with pytest.raises(ValueError):
        calculate_metrics(inputs)

def test_missing_required_input(example_inputs):
    inputs = example_inputs.copy()

    del inputs["influent_m3_day"]

    with pytest.raises(
        ValueError,
        match="Missing required input: influent_m3_day"
    ):
        calculate_metrics(inputs)

def test_streamlit_manual_input_integration(example_inputs):
    # Simulate inputs from Role 2's Streamlit dashboard
    inputs = example_inputs.copy()

    results = calculate_metrics(inputs)

    # Check all dashboard outputs
    assert results["historical_baseline"] is None

    assert results["energy_saved"]["annual"]["value"] == pytest.approx(73000)

    assert results["scope2_reduction"]["value"] == pytest.approx(29.346)

    assert results["chemical_avoided"]["annual"]["value"] == pytest.approx(5475)

    assert results["water_reuse"]["annual"]["value"] == pytest.approx(255500)

    # Check the baseline source
    assert results["energy_saved"]["baseline_source"] == "Manual input"


def test_streamlit_historical_input_integration(example_inputs):
    # Simulate 12 months of historical plant data
    inputs = example_inputs.copy()

    inputs["monthly_electricity_kwh"] = [3000] * 12
    inputs["monthly_treated_m3"] = [2000] * 12
    inputs["historical_data_quality"] = "Illustrative Benchmark"

    results = calculate_metrics(inputs)

    # Historical baseline = 1.5 kWh/m3
    assert results["historical_baseline"]["value"] == pytest.approx(1.5)

    # Daily energy saved = (1.5 - 0.8) * 1000
    assert results["energy_saved"]["daily"]["value"] == pytest.approx(700)

    # Annual energy saved = 700 * 365
    assert results["energy_saved"]["annual"]["value"] == pytest.approx(255500)

    # Scope 2 reduction = 255500 * 0.402 / 1000
    assert results["scope2_reduction"]["value"] == pytest.approx(102.711)

    # Confirm historical baseline was used
    assert results["energy_saved"]["baseline_source"] == (
        "12-month historical records"
    )
