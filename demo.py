
from engine import calculate_metrics

example_inputs = {
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

results = calculate_metrics(example_inputs)

for metric_name, result in results.items():
    print(f"\n{metric_name}")

    if result is None:
        print("  No historical data provided")
        continue

    if isinstance(result, dict) and "value" in result:
        print(
            f"  {result['value']} "
            f"{result['unit']} "
            f"[{result['data_quality']}]"
        )

    elif isinstance(result, dict):
        for period, metric in result.items():
            if not isinstance(metric, dict):
                continue

            if "value" not in metric:
                continue

            print(
                f"  {period}: {metric['value']} "
                f"{metric['unit']} "
                f"[{metric['data_quality']}]"
            )
