
from config import EMISSION_FACTORS


# ---------- 1. Input validation ----------

ALLOWED_DATA_QUALITY = {
    "Measured Telemetry",
    "User Input",
    "Illustrative Benchmark",
}


def validate_data_quality(quality):
    if quality not in ALLOWED_DATA_QUALITY:
        raise ValueError(
            f"Invalid data quality: {quality}. "
            f"Allowed values: {sorted(ALLOWED_DATA_QUALITY)}"
        )

    return quality

def require_non_negative(name, value):
    """Reject missing, non-numeric, infinite, NaN, or negative inputs."""
    import math

    if isinstance(value, bool):
        raise ValueError(f"{name} must be a number.")

    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a valid number.")

    if not math.isfinite(number) or number < 0:
        raise ValueError(f"{name} must be finite and non-negative.")

    return number


def validate_operating_days(days):
    days = require_non_negative("operating_days", days)

    if days > 366:
        raise ValueError(
            "operating_days cannot exceed 366."
        )

    return days

def validate_reduction(name, percentage):
    percentage = require_non_negative(name, percentage)

    if percentage > 100:
        raise ValueError(f"{name} must be between 0 and 100.")

    return percentage / 100


# ---------- 2. Standardised output format ----------

def make_metric(
    value,
    unit,
    quality,
    formula,
    assumptions=None,
):
    """Return a consistent, traceable metric for Roles 2 and 3."""
    return {
        "value": round(value, 6),
        "unit": unit,
        "data_quality": quality,
        "formula": formula,
        "assumptions": assumptions or [],
    }


# ---------- 3. Energy savings ----------

def calculate_energy_saved(
    influent_m3_day,
    baseline_kwh_m3,
    optimized_kwh_m3,
    operating_days=365,
    quality="Illustrative Benchmark",
):
    volume = require_non_negative("influent_m3_day", influent_m3_day)
    baseline = require_non_negative("baseline_kwh_m3", baseline_kwh_m3)
    optimized = require_non_negative(
        "optimized_kwh_m3", optimized_kwh_m3
    )
    days = validate_operating_days(operating_days)

    daily_savings = (baseline - optimized) * volume
    annual_savings = daily_savings * days

    return {
        "daily": make_metric(
            daily_savings,
            "kWh/day",
            quality,
            "(baseline intensity - optimized intensity)"
            " * daily influent volume",
        ),
        "annual": make_metric(
            annual_savings,
            "kWh/year",
            quality,
            "daily energy savings * operating days",
        ),
    }


# ---------- 4. Scope 2 electricity emissions ----------





def calculate_scope2_reduction(
    energy_saved_kwh,
    grid_ef=None,
    quality="Illustrative Benchmark",
):
    import math

    # Validate energy savings (negative values are allowed)
    if isinstance(energy_saved_kwh, bool):
        raise ValueError("energy_saved_kwh must be a number.")

    try:
        energy = float(energy_saved_kwh)
    except (TypeError, ValueError):
        raise ValueError(
            "energy_saved_kwh must be a valid number."
        )

    if not math.isfinite(energy):
        raise ValueError(
            "energy_saved_kwh must be finite."
        )

    # Get emission factor information
    factor_info = EMISSION_FACTORS["singapore_grid"]

    if grid_ef is None:
        factor = require_non_negative(
            "grid_ef", factor_info["value"]
        )
        factor_source = factor_info["source"]
        factor_year = factor_info["year"]
        factor_status = factor_info["status"]
    else:
        factor = require_non_negative("grid_ef", grid_ef)
        factor_source = "User Input"
        factor_year = None
        factor_status = "unverified"

    # Calculate Scope 2 reduction
    reduction_tonnes = energy * factor / 1000

    result = make_metric(
        reduction_tonnes,
        "tCO2e",
        quality,
        "energy saved * grid emission factor / 1000",
        ["Location-based electricity factor"],
    )

    # Attach emission factor metadata
    result["emission_factor"] = factor
    result["factor_unit"] = factor_info["unit"]
    result["factor_source"] = factor_source
    result["factor_year"] = factor_year
    result["factor_status"] = factor_status

    return result



# ---------- 5. Chemical mass avoided ----------

def calculate_chemical_avoided(
    baseline_chemical_kg_day,
    reduction_pct,
    operating_days=365,
    quality="Illustrative Benchmark",
):
    baseline = require_non_negative(
        "baseline_chemical_kg_day", baseline_chemical_kg_day
    )
    fraction = validate_reduction(
        "reduction_pct", reduction_pct
    )
    days = validate_operating_days(operating_days)

    daily_avoided = baseline * fraction

    return {
        "daily": make_metric(
            daily_avoided,
            "kg/day",
            quality,
            "baseline chemical mass * reduction fraction",
        ),
        "annual": make_metric(
            daily_avoided * days,
            "kg/year",
            quality,
            "daily chemical mass avoided * operating days",
        ),
    }


# ---------- 6. Water reuse volume ----------

def calculate_water_reuse(
    reuse_m3_day,
    operating_days=365,
    quality="Illustrative Benchmark",
):
    reuse = require_non_negative("reuse_m3_day", reuse_m3_day)
    days = validate_operating_days(operating_days)

    return {
        "daily": make_metric(
            reuse,
            "m3/day",
            quality,
            "measured or assumed reclaimed water delivered for reuse",
        ),
        "annual": make_metric(
            reuse * days,
            "m3/year",
            quality,
            "daily reuse volume * operating days",
        ),
    }


# ---------- 7. One function for the whole application ----------


def calculate_metrics(inputs):

    required_inputs = [
        "influent_m3_day",
        "optimized_kwh_m3",
        "baseline_chemical_kg_day",
        "chemical_reduction_pct",
        "reuse_m3_day",
    ]

    for name in required_inputs:
        if name not in inputs:
            raise ValueError(f"Missing required input: {name}")

    if (
        inputs.get("monthly_electricity_kwh") is None
        and inputs.get("monthly_treated_m3") is None
        and "baseline_kwh_m3" not in inputs
    ):
        raise ValueError(
            "Missing required input: baseline_kwh_m3"
        )

    quality = validate_data_quality(
        inputs.get("quality", "Illustrative Benchmark")
    )

    monthly_electricity = inputs.get("monthly_electricity_kwh")
    monthly_water = inputs.get("monthly_treated_m3")

    if monthly_electricity is not None or monthly_water is not None:

        if monthly_electricity is None or monthly_water is None:
            raise ValueError(
                "Both monthly_electricity_kwh and "
                "monthly_treated_m3 are required."
            )

        baseline = calculate_historical_baseline(
            monthly_electricity_kwh=monthly_electricity,
            monthly_treated_m3=monthly_water,
            quality=validate_data_quality(
                inputs.get("historical_data_quality", "User Input")
            ),
        )

        baseline_kwh_m3 = baseline["value"]

    else:
        baseline = None
        baseline_kwh_m3 = inputs["baseline_kwh_m3"]


    # EXISTING: Calculate energy savings
    energy = calculate_energy_saved(
        influent_m3_day=inputs["influent_m3_day"],
        baseline_kwh_m3=baseline_kwh_m3,
        optimized_kwh_m3=inputs["optimized_kwh_m3"],
        operating_days=inputs.get("operating_days", 365),
         
        quality=quality,

    )
    
    # Track which baseline was used
    if baseline is not None:
        baseline_source = "12-month historical records"
        baseline_quality = baseline["data_quality"]
    else:
        baseline_source = "Manual input"
        baseline_quality = "User Input"

    # Attach baseline information to energy results
    energy["baseline_kwh_m3"] = baseline_kwh_m3
    energy["baseline_source"] = baseline_source
    energy["baseline_quality"] = baseline_quality

    # EXISTING: Calculate Scope 2 emissions reduction
    ghg = calculate_scope2_reduction(
        energy_saved_kwh=energy["annual"]["value"],
        grid_ef=inputs.get("grid_ef"),
        
quality=quality,

    )

    # EXISTING: Calculate chemical savings
    chemical = calculate_chemical_avoided(
        baseline_chemical_kg_day=inputs[
            "baseline_chemical_kg_day"
        ],
        reduction_pct=inputs["chemical_reduction_pct"],
        operating_days=inputs.get("operating_days", 365),
        
quality=quality,

    )

    # EXISTING: Calculate water reuse
    water = calculate_water_reuse(
        reuse_m3_day=inputs["reuse_m3_day"],
        operating_days=inputs.get("operating_days", 365),
        
quality=quality,

    )

    # UPDATED: Include historical baseline in output
    return {
        "historical_baseline": baseline,
        "energy_saved": energy,
        "scope2_reduction": ghg,
        "chemical_avoided": chemical,
        "water_reuse": water,
    }


def calculate_historical_baseline(
    monthly_electricity_kwh,
    monthly_treated_m3,
    quality="Measured Telemetry",
):
    """
    Calculate 12-month baseline energy intensity.

    Baseline intensity = total electricity / total treated water
    """

    if len(monthly_electricity_kwh) != 12:
        raise ValueError(
            "Exactly 12 monthly electricity values are required."
        )

    if len(monthly_treated_m3) != 12:
        raise ValueError(
            "Exactly 12 monthly treated-water values are required."
        )

    electricity = [
        require_non_negative(f"electricity_month_{i + 1}", value)
        for i, value in enumerate(monthly_electricity_kwh)
    ]

    water = [
        require_non_negative(f"water_month_{i + 1}", value)
        for i, value in enumerate(monthly_treated_m3)
    ]

    total_electricity = sum(electricity)
    total_water = sum(water)

    if total_water <= 0:
        raise ValueError(
            "Total treated water over 12 months must be greater than zero."
        )

    baseline_intensity = total_electricity / total_water

    return make_metric(
        baseline_intensity,
        "kWh/m3",
        quality,
        "total electricity over 12 months / total treated water over 12 months",
        ["Exactly 12 monthly values", "Volume-weighted baseline"],
    )
