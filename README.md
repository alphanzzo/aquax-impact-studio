## Application Screenshots & Demonstration

### 1. Interactive Sustainability Dashboard

![AquaX Dashboard](<img width="1432" height="772" alt="Screenshot 2026-10-21 220705" src="https://github.com/user-attachments/assets/61f85de4-7b2e-4537-a65d-b1a7546f1676" />


The AquaX Impact Calculator allows users to enter wastewater treatment plant conditions and explore the potential environmental impact of operational improvements.

The left sidebar contains shared operating assumptions, including daily influent flow, baseline electricity intensity, chemical consumption and operating days.
When you run it on streamlit, change value for eg. Inflow rate (with arrow pointed at left) to see the different metrics change in the middle, one of the metrics that will change is the "Daily energy saved" (arrow pointed at middle)

The main dashboard allows users to adjust optimized energy intensity, chemical reduction percentages and water reuse targets. Results are recalculated to display the estimated environmental impact.

**Example scenario shown:**
- Daily energy savings: **200 kWh/day**
- Annual energy savings: **73,000 kWh/year**
- Estimated annual Scope 2 emissions reduction: **29.346 tCO₂e/year**

All values are illustrative scenario estimates rather than verified operational savings.

### 2. Automatically Generated Sustainability Report



The application can generate a structured sustainability annex in Word format using the calculated scenario results. (See arrow pointed in screenshot below)
<img width="1296" height="732" alt="Screenshot 2026-10-21 220841" src="https://github.com/user-attachments/assets/337f09b0-b035-4318-99fc-63a8cf2fde94" />

See an example of the generated report in the file below:

![Sustainability Annex Preview]([AquaX_Sustainability_Annex (3).docx](https://github.com/user-attachments/files/33773054/AquaX_Sustainability_Annex.3.docx)
)
The report includes:
- Annual energy savings, estimated Scope 2 emissions reductions, chemical mass avoided and water reuse
- Calculation methodologies, assumptions and data-quality information
- Sustainability reporting framework mappings and outstanding disclosure requirements
- Limitations and verification disclaimers


The sample report demonstrates how calculated results can be transformed into documentation for stakeholder review. It is not an officially audited ESG report.

### 3. My Contribution — Backend Engineer

As part of a team hackathon project, I developed the Python backend responsible for calculating the environmental metrics displayed in the dashboard.

My work included input validation, calculation functions, 12-month historical baseline logic, emission-factor metadata, automated pytest tests and integration documentation.
In this GitHub repository it will be test_engine.py , engine.py, demo.py, config.py and BACKEND_HANDOVER.md

The frontend dashboard and reporting/export components were developed collaboratively by other team members.
