AquaX Impact Studio
A prototype sustainability calculator for wastewater and water-treatment operations. This repository models a plant-level scenario, compares baseline and optimized operating assumptions, and produces a transparent summary of potential energy, chemical, and emissions impacts.

The project is designed around a simple workflow for Audits :

a user enters operational assumptions in a Streamlit UI,
a calculation engine estimates baseline vs. optimized performance,
the results are surfaced in dashboards and downloadable reporting outputs.
This is a demo and prototype, not a certified ESG or compliance system.

What the app does
The app estimates:

energy saved (kWh/day and kWh/year),
Scope 2 electricity emissions reduction (tCO2e),
avoided chemical mass (kg/day and kg/year),
water reuse volume (m3/day and m3/year),
data-quality and formula metadata for each metric.
Outputs are built around the AquaX concept described in the hackathon brief: a transparent, explanation-first sustainability impact calculator that exposes assumptions instead of hiding them behind opaque scores.


Important constraints:

plant names, client identities, and raw source mappings are intentionally withheld,
the dataset is not for public redistribution,
the results should be treated as illustrative estimates, not verified operational or ESG reporting.
The data retain a number of real-world data-quality problems, including missing values, duplicate readings, outliers, and ambiguously labeled chemical fields. This is intentional and reflects the challenge context rather than a clean production dataset.

Quick start
1. Clone and set up the environment
git clone https://github.com/whansel007/ALW-HacknHire.git
cd ALW-HacknHire
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# or: .\.venv\Scripts\activate  # Windows PowerShell
python -m pip install --upgrade pip
pip install -r requirements.txt

2. Run the Streamlit app in VS code
streamlit run streamlit_app.py

Then open the local URL shown in the terminal, typically:

http://localhost:8501
The app lets you enter project assumptions, calculate a scenario, and export the generated report content as a Word annex or JSON payload.

3. Run the backend demo
python demo.py

4. Run tests
pytest -q test_engine.py
pytest -q test_role2_integration.py
pytest -q test_streamlit_exports.py

Notes on scope and limitations
This prototype is intentionally scoped for a small demonstration workflow and should not be interpreted as audited ESG reporting.

Key limitations:

default emission-factor values are provisional,
chemical impact factors are not fully verified,
the app models illustrative scenarios rather than causal, measured savings,
the results are best used for exploration and communication, not operational control or formal external disclosure.
Documentation
BACKEND_HANDOVER.md — calculation engine overview and contract
docs/PRD.md — product requirements and role breakdown
docs/What we are building.md — design summary and rationale
Suggested next steps
confirm the emission-factor sources against authoritative references,

Project structure
engine.py — core backend calculations, validation, and metric generation
streamlit_app.py — main Streamlit application for scenario entry and results display
config.py — emission factors and configuration constants
exporter.py — DOCX and JSON export logic for reporting outputs
mapper.py — mapping layer that converts calculations into report-ready payloads
demo.py — simple command-line demo of the calculation engine
demo_report.py — example script generating downloadable report artifacts
test_engine.py — backend validation tests
test_role2_integration.py — end-to-end checks between backend and UI assumptions
test_streamlit_exports.py — export-related Streamlit validation tests
data/ — anonymized plant operational datasets and workbook metadata
docs/ — project brief, requirements, and supporting reference material
BACKEND_HANDOVER.md — backend handover and API notes
requirements.txt — Python dependencies for the app
Dataset and confidentiality
The repository contains anonymized plant datasets for two plants, labeled only as Plant A and Plant B.

expand the mapping layer for reporting frameworks,
improve data-cleaning and validation around the anonymized plant data,
harden the export experience for downstream presentations and stakeholder reviews.
