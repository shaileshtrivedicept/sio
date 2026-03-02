# Studio Review Dashboard

Interactive Streamlit dashboard for analyzing and visualizing studio review performance data.

## Features
- **Key Performance Indicators (KPIs)**: Tracking total studios, panels, response counts, average scores, and panel spread.
- **Studio Trajectory**: Visualizing performance over semesters with chronological sorting and total score overlays.
- **Construct Contribution Heatmap**: Analyzing the distribution of score contributions across various constructs.
- **Final Score Distribution**: Box plots of scores categorized by Construct ID, with optional Panel ID faceting.
- **Performance Rankings**: Top and Bottom 10 studios for selected semesters.
- **Data Export**: Downloadable CSV files for filtered raw data and calculated metrics.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- `pip`

### Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally
Run the Streamlit application from the `studio-review-dashboard` directory:
```bash
cd studio-review-dashboard
streamlit run app.py
```

## Data Management
The dashboard reads data from: `data/BoR_Rating_Data.xlsx`.

To update the data:
1. Replace the file in the `data/` directory.
2. Ensure the sheet name is 'Normalized Score' or update the loading logic in `src/io.py`.
3. Column names should remain consistent (AY, Semester, Studio_Code, Panel_ID, Final_Score, etc.).

## Project Structure
- `app.py`: Main Streamlit application entry point.
- `data/`: Directory for the Excel data source.
- `src/io.py`: Data ingestion and cleaning logic.
- `src/metrics.py`: Business logic for aggregating scores and computing shares.
- `requirements.txt`: Python package dependencies.
