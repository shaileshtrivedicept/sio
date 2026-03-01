# Studio Review Dashboard

A Streamlit dashboard that visualizes studio review performance from Excel-based scoring data.

## Features
- Interactive sidebar filters for AY, Semester, Level, Studio, and Panels.
- KPI metrics for high-level summary.
- Multiple visual analytics:
  - Studio Trajectory over semesters.
  - Construct Contribution Heatmap.
  - Final Score Distribution (Box plots).
  - Top/Bottom performing studios.
- Data export in CSV format.

## Setup and Running Locally

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Dashboard:**
   ```bash
   streamlit run app.py
   ```

## Data Management
- The data source is an Excel file located at `data/normalized score calculation sample V3.xlsx`.
- To replace the data, drop a new `.xlsx` file into the `data/` directory.
- Ensure the sheet name "Normalized Score (2)" remains consistent, or update `src/io.py` to reflect the new sheet name.
- The dashboard expects a specific structure: 3 blank rows, a header row, followed by data rows starting with "AY", "Semester", etc.
