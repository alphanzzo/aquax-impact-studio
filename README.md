# AquaX Impact Studio

**A Python-based sustainability impact calculator for wastewater treatment operations.**

AquaX Impact Studio was developed as a team hackathon prototype to estimate the potential environmental benefits of wastewater treatment optimizations.

The project compares baseline and optimized operating scenarios to calculate energy savings, avoided Scope 2 electricity emissions, reduced chemical consumption, and water reuse.

**Project status:** Prototype — estimates are illustrative and not audited ESG results.

## My Role — Backend & Calculation Engine Engineer

I was responsible for developing the calculation backend, including:

- **Calculation engine:** Implemented Python functions for energy savings, Scope 2 emissions reductions, chemical mass avoided, and water reuse.
- **Input validation:** Added checks for missing, negative, invalid, or non-finite values and unsupported parameters.
- **Historical baseline calculation:** Implemented an optional 12-month baseline using total historical electricity consumption divided by total treated water volume.
- **Emission-factor configuration:** Centralized calculation factors and included source, unit, and verification metadata.
- **Automated testing:** Developed pytest tests covering calculations, input validation, historical baselines, and integration assumptions.
- **Backend integration:** Provided a structured `calculate_metrics(inputs)` interface and technical handover documentation for the frontend developer.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend calculation logic |
| pytest | Automated validation and testing |
| Streamlit | Frontend framework used in the broader team project |
| GitHub | Version control and collaboration |

## Core Calculations

| Metric | Description | Output unit |
|---|---|---|
| Energy savings | Difference between baseline and optimized electricity use | kWh/day, kWh/year |
| Scope 2 emissions reduction | Electricity savings multiplied by the grid emission factor | tCO₂e/year |
| Chemical mass avoided | Reduction in daily chemical consumption | kg/day, kg/year |
| Water reuse | Daily water reuse projected over operating days | m³/day, m³/year |

Each metric includes calculation and data-quality metadata to improve transparency.

## Example Results

Using illustrative inputs of 1,000 m³/day influent, a baseline electricity intensity of 1.0 kWh/m³, optimized intensity of 0.8 kWh/m³, and 365 operating days:

| Metric | Illustrative result |
|---|---:|
| Annual electricity savings | 73,000 kWh |
| Annual Scope 2 emissions reduction | 29.346 tCO₂e |
| Annual chemical mass avoided | 5,475 kg |
| Annual water reuse | 255,500 m³ |

These are calculated scenario results, not measured reductions from an operating treatment plant.



## Running the Backend

Clone this repository:

```bash
git clone https://github.com/alphanzzo/aquax-impact-studio.git
cd aquax-impact-studio
```

Install pytest:

```bash
python -m pip install pytest
```

Run the sample calculation:

```bash
python demo.py
```

Run the automated tests:

```bash
python -m pytest -v test_engine.py
```

This repository demonstrates the backend module. The complete team application may require additional frontend and reporting files.

## Engineering Considerations

**Input validation**

The backend checks numerical inputs and rejects invalid values to prevent misleading or unusable calculations.

**Historical baselines**

When 12 months of electricity consumption and treated-water volume are supplied, the baseline is calculated using total energy divided by total treated water volume rather than an unweighted average of monthly intensities.

**Transparency**

Outputs include units, formulas, assumptions, data-quality labels, and emission-factor metadata where applicable.

## Limitations

- Calculations are based on user-supplied or illustrative assumptions.
- The configured Singapore electricity grid emission factor is provisional and requires source verification.
- Chemical emission factors are not fully verified.
- Chemical mass reduction should not be interpreted as verified chemical-related emissions reduction.
- The prototype is not a certified ESG reporting system and should not be used as evidence of actual plant savings without appropriate data validation.

## Team Collaboration

This project was developed collaboratively during a hackathon.

**My primary contribution:** Backend calculation engine, input validation, factor configuration, automated testing, and integration documentation.

The broader team project also involved frontend/dashboard development and reporting/export functionality.

## Future Improvements

- Verify emission factors against authoritative sources.
- Integrate representative plant operating datasets.
- Expand automated integration testing.
- Improve reporting and factor traceability.
- Connect the calculation engine to production-ready interfaces.

## Backend Architecture

```text
Operational Inputs
       |
       v
Input Validation
       |
       v
Calculation Engine (engine.py)
       |
       +-- Energy Savings
       +-- Scope 2 Emissions
       +-- Chemical Mass Avoided
       +-- Water Reuse
       +-- Historical Baseline
       |
       v
Structured Results + Metadata
       |
       v
Frontend / Reporting Integration
```

The main backend interface is `calculate_metrics(inputs)`.

The calculation module is designed to remain separate from the user interface, allowing other application components to request calculations without duplicating formulas.

## Repository Files

| File | Purpose |
|---|---|
| `engine.py` | Core calculations, validation, and historical baseline logic |
| `config.py` | Emission factors and verification information |
| `test_engine.py` | Automated tests |
| `demo.py` | Example inputs and backend output |
| `BACKEND_HANDOVER.md` | Integration contract and technical documentation |
| `README.md` | Project overview |
