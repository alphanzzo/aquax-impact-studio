# AquaX Impact Studio — Backend Handover

**Owner:** Role 1 — Backend & Calculation Engine  
**Integration:** Role 2 — Streamlit Frontend

## 1. Backend overview

The AquaX calculation engine processes wastewater treatment plant inputs and estimates energy savings, Scope 2 electricity emissions reductions, chemical mass avoided, and water reuse volumes.

The main entry point is `calculate_metrics(inputs)` in `engine.py`.

## 2. How to call the backend

```python
from engine import calculate_metrics

inputs = {
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

results = calculate_metrics(inputs)
```

## 3. Input requirements

| Input | Unit | Required |
|---|---|---|
| `influent_m3_day` | m³/day | Yes |
| `baseline_kwh_m3` | kWh/m³ | Unless historical records are provided |
| `optimized_kwh_m3` | kWh/m³ | Yes |
| `baseline_chemical_kg_day` | kg/day | Yes |
| `chemical_reduction_pct` | % | Yes |
| `reuse_m3_day` | m³/day | Yes |
| `operating_days` | days/year | No; default 365 |
| `grid_ef` | kgCO₂e/kWh | No; configured default |
| `quality` | Label | No; default Illustrative Benchmark |

Optional historical inputs:

- `monthly_electricity_kwh`: exactly 12 monthly electricity readings.
- `monthly_treated_m3`: exactly 12 monthly treated-water volumes.
- `historical_data_quality`: provenance label, default User Input.

Both historical arrays must be supplied together. When present, their volume-weighted baseline overrides the manually entered baseline.

## 4. Output structure

The function returns a Python dictionary with these keys:

- `historical_baseline`: baseline metric dictionary, or `None`.
- `energy_saved`: daily and annual metrics, plus baseline source and quality metadata.
- `scope2_reduction`: annual reduction in tCO₂e, with grid emission factor metadata.
- `chemical_avoided`: daily and annual avoided chemical mass.
- `water_reuse`: daily and annual reuse volumes.

For example, Role 2 can access:

```python
annual_energy = results["energy_saved"]["annual"]["value"]
annual_ghg = results["scope2_reduction"]["value"]
annual_chemical = results["chemical_avoided"]["annual"]["value"]
annual_reuse = results["water_reuse"]["annual"]["value"]
```

Each metric dictionary includes `value`, `unit`, `data_quality`, `formula`, and `assumptions`.

## 5. Validation and error handling

The backend rejects invalid numeric values, percentages above 100, operating days above 366, incomplete historical data, missing required inputs, and unsupported data-quality labels.

The Streamlit frontend should catch `ValueError` and `TypeError` and display the error message to users.

## 6. Data-quality and reporting limitations

Supported labels:

- Measured Telemetry
- User Input
- Illustrative Benchmark

Labels describe the claimed origin of data; the backend does not independently verify plant records.

The configured Singapore grid emission factor is provisional and must be confirmed against an appropriate official publication before external reporting.

Chemical mass avoided is not the same as chemical-related greenhouse gas emissions avoided. Chemical emission factors remain unverified, so chemical emissions reductions are not currently calculated.

All demonstration results are illustrative estimates, not verified ESG claims.

## 7. Testing

Run:

```powershell
python -m pytest -v test_engine.py
```

Latest verified test result: **28 passed**.

Run the sample demonstration:

```powershell
python demo.py
```

## 8. Integration responsibilities

**Role 1:** Maintain calculations, validation, emission factor configuration, metadata, and backend tests.

**Role 2:** Build Streamlit inputs, call `calculate_metrics()`, display results and metadata, and handle validation errors.

**Role 3 / Reporting:** Use the output metrics, formulas, assumptions, and provenance for report generation, subject to source verification.