import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from src.io import load_and_clean_data
from src.metrics import calculate_metrics

# Set page config
st.set_page_config(page_title="Studio Review Dashboard", layout="wide")

# Constants
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "normalized_score_calculation_sample_V3.xlsx")

# Title
st.title("Studio Review Dashboard")

# Load data
df = load_and_clean_data(DATA_PATH)

if df.empty:
    st.error(f"Failed to load data from {DATA_PATH}. Please ensure the file exists and is in the correct format.")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")

ay_list = sorted([x for x in df['AY'].unique() if pd.notna(x)])
semester_list = sorted([x for x in df['Semester'].unique() if pd.notna(x)])
level_list = sorted([x for x in df['Level'].unique() if pd.notna(x)])
studio_code_list = sorted([x for x in df['Studio_Code'].unique() if pd.notna(x)])
studio_focus_area_list = sorted([str(x) for x in df['Studio_Focus_Area'].unique() if pd.notna(x)])
panel_id_list = sorted([x for x in df['Panel_ID'].unique() if pd.notna(x)])
construct_id_list = sorted([x for x in df['Construct_ID'].unique() if pd.notna(x)])

sel_ay = st.sidebar.multiselect("Academic Year (AY)", ay_list, default=ay_list)
sel_semester = st.sidebar.multiselect("Semester", semester_list, default=semester_list)
sel_level = st.sidebar.multiselect("Level", level_list, default=level_list)
sel_studio_code = st.sidebar.multiselect("Studio Code", studio_code_list, default=studio_code_list)
sel_studio_focus_area = st.sidebar.multiselect("Studio Focus Area", studio_focus_area_list, default=studio_focus_area_list)
sel_panel_id = st.sidebar.multiselect("Panel ID", panel_id_list, default=panel_id_list)
sel_construct_id = st.sidebar.multiselect("Construct ID", construct_id_list, default=construct_id_list)

# Apply filters
filtered_df = df[
    (df['AY'].isin(sel_ay)) &
    (df['Semester'].isin(sel_semester)) &
    (df['Level'].isin(sel_level)) &
    (df['Studio_Code'].isin(sel_studio_code)) &
    (df['Studio_Focus_Area'].isin(sel_studio_focus_area)) &
    (df['Panel_ID'].isin(sel_panel_id)) &
    (df['Construct_ID'].isin(sel_construct_id))
]

if filtered_df.empty:
    st.warning("Filters empty out the dataset. Please adjust your selection.")
    st.stop()

# Compute metrics for filtered data
panel_scores, studio_sem_total, construct_scores, construct_share = calculate_metrics(filtered_df)

# KPI row
st.subheader("Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)

num_studios = filtered_df['Studio_Code'].nunique()
num_panels = filtered_df['Panel_ID'].nunique()
num_responses = len(filtered_df)
avg_final_score = filtered_df['Final_Score'].mean()

# Panel Spread calculation: for each Studio_Code+Semester compute max(panel_sum)-min(panel_sum), then show mean spread across filtered studios
# We take the first SPREAD for each Studio_Code+Semester to avoid weighting by number of panels
mean_panel_spread = panel_scores.groupby(['AY', 'Semester', 'Studio_Code'])['SPREAD'].first().mean()

col1.metric("# Studios", num_studios)
col2.metric("# Panels", num_panels)
col3.metric("# Responses", num_responses)
col4.metric("Avg Final Score", f"{avg_final_score:.2f}")
col5.metric("Avg Panel Spread", f"{mean_panel_spread:.2f}")

# Charts Section
st.divider()

# (Chart 1) “Studio Trajectory”
st.subheader("Studio Trajectory")
st_col1, st_col2 = st.columns([1, 4])
with st_col1:
    traj_studio = st.selectbox("Select Studio for Trajectory", sorted(filtered_df['Studio_Code'].unique()))

# Filter data for selected studio
traj_df = filtered_df[filtered_df['Studio_Code'] == traj_studio]
# Get panel scores for selected studio
traj_panel_scores = panel_scores[panel_scores['Studio_Code'] == traj_studio]
# Get studio totals for selected studio
traj_studio_totals = studio_sem_total[studio_sem_total['Studio_Code'] == traj_studio]

# Order semesters chronologically if possible, otherwise by academic order
# Given semesters like M18, S19, M19, S20...
# Monsoon (M) usually starts the academic year, followed by Spring (S) of the next calendar year.
def sort_semesters(sem):
    try:
        season = sem[0]
        year = int(sem[1:])
        # If year is 18 (2018), M18 is Monsoon 2018. S19 is Spring 2019.
        # They belong to the same academic year 2018-19.
        # Let's map them to a continuous timeline.
        # M18 -> 2018.5, S19 -> 2019.0
        if season == 'M':
            return year + 0.5
        elif season == 'S':
            return float(year)
        return float(year)
    except:
        return 0.0

unique_sems = sorted(filtered_df['Semester'].unique(), key=sort_semesters)

fig1 = go.Figure()

# Add lines for each Panel_ID
for panel_id in traj_panel_scores['Panel_ID'].unique():
    p_data = traj_panel_scores[traj_panel_scores['Panel_ID'] == panel_id].sort_values(by='Semester', key=lambda x: x.map(sort_semesters))
    fig1.add_trace(go.Scatter(x=p_data['Semester'], y=p_data['Final_Score'], name=f"Panel {panel_id}", mode='lines+markers'))

# Add thicker line for studio total
traj_studio_totals_sorted = traj_studio_totals.sort_values(by='Semester', key=lambda x: x.map(sort_semesters))
fig1.add_trace(go.Scatter(x=traj_studio_totals_sorted['Semester'], y=traj_studio_totals_sorted['Studio_Total_Score'],
                         name="Total Score", mode='lines+markers', line=dict(width=4, color='black')))

fig1.update_layout(xaxis_title="Semester", yaxis_title="Score", xaxis={'categoryorder': 'array', 'categoryarray': unique_sems})
st.plotly_chart(fig1, use_container_width=True)

# (Chart 2) “Construct Contribution Heatmap”
st.subheader("Construct Contribution Heatmap")
heatmap_data = construct_share.pivot_table(index='Construct_ID', columns='Semester', values='Construct_Share', aggfunc='mean').reindex(columns=unique_sems)
fig2 = px.imshow(heatmap_data, labels=dict(x="Semester", y="Construct ID", color="Contribution Share"),
                aspect="auto", color_continuous_scale="Viridis")
st.plotly_chart(fig2, use_container_width=True)

# (Chart 3) “Final Score Distribution”
st.subheader("Final Score Distribution")
st_col3, st_col4 = st.columns([1, 4])
with st_col3:
    facet_by_panel = st.checkbox("Facet by Panel ID")

if facet_by_panel:
    fig3 = px.box(filtered_df, x="Construct_ID", y="Final_Score", color="Panel_ID", points="all")
else:
    fig3 = px.box(filtered_df, x="Construct_ID", y="Final_Score", points="all")
st.plotly_chart(fig3, use_container_width=True)

# (Chart 4) “Top/Bottom Studios”
st.subheader("Top/Bottom Studios")
st_col5, st_col6 = st.columns([1, 4])
with st_col5:
    selected_sem = st.selectbox("Select Semester for Comparison", unique_sems)
    top_bottom_toggle = st.radio("Show", ["Top 10", "Bottom 10"])

sem_studios = studio_sem_total[studio_sem_total['Semester'] == selected_sem].sort_values(by='Studio_Total_Score', ascending=(top_bottom_toggle == "Bottom 10"))
plot_studios = sem_studios.head(10)

fig4 = px.bar(plot_studios, x='Studio_Code', y='Studio_Total_Score', color='Studio_Total_Score',
             title=f"{top_bottom_toggle} Studios in {selected_sem}")
st.plotly_chart(fig4, use_container_width=True)

# Data tables
st.divider()
st.subheader("Detailed Data")

st.write("### Panel Scores and Spread")
st.dataframe(panel_scores.sort_values(['AY', 'Semester', 'Studio_Code', 'Panel_ID']))

col_d1, col_d2, col_d3 = st.columns(3)
with col_d1:
    st.download_button("Download Filtered Raw Data (CSV)", filtered_df.to_csv(index=False).encode('utf-8'), "filtered_raw_data.csv", "text/csv")
with col_d2:
    st.download_button("Download Panel Scores (CSV)", panel_scores.to_csv(index=False).encode('utf-8'), "panel_scores.csv", "text/csv")
with col_d3:
    st.download_button("Download Construct Share (CSV)", construct_share.to_csv(index=False).encode('utf-8'), "construct_share.csv", "text/csv")
