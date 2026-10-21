## Application Screenshots & Demonstration

### 1. Interactive Sustainability Dashboard

![AquaX Dashboard](images/aquax-dashboard.png)

The AquaX Impact Calculator allows users to enter wastewater treatment plant conditions and explore the potential environmental impact of operational improvements.

The left sidebar contains shared operating assumptions, including daily influent flow, baseline electricity intensity, chemical consumption and operating days.

The main dashboard allows users to adjust optimized energy intensity, chemical reduction percentages and water reuse targets. Results are recalculated to display the estimated environmental impact.

**Example scenario shown:**
- Daily energy savings: **200 kWh/day**
- Annual energy savings: **73,000 kWh/year**
- Estimated annual Scope 2 emissions reduction: **29.346 tCO₂e/year**

All values are illustrative scenario estimates rather than verified operational savings.

### 2. Automatically Generated Sustainability Report

![Sustainability Annex Preview]([AquaX_Sustainability_Annex (3).docx](https://github.com/user-attachments/files/33773054/AquaX_Sustainability_Annex.3.docx)
)

The application can generate a structured sustainability annex in Word format using the calculated scenario results.

The report includes:
- Annual energy savings, estimated Scope 2 emissions reductions, chemical mass avoided and water reuse
- Calculation methodologies, assumptions and data-quality information
- Sustainability reporting framework mappings and outstanding disclosure requirements
- Limitations and verification disclaimers

**[View the Sample Sustainability Annex](reports/AquaX_Sustainability_Annex.docx)**

The sample report demonstrates how calculated results can be transformed into documentation for stakeholder review. It is not an audited ESG report.

### 3. My Contribution — Backend Engineer

As part of a team hackathon project, I developed the Python backend responsible for calculating the environmental metrics displayed in the dashboard.

My work included input validation, calculation functions, 12-month historical baseline logic, emission-factor metadata, automated pytest tests and integration documentation.

The frontend dashboard and reporting/export components were developed collaboratively by other team members.
