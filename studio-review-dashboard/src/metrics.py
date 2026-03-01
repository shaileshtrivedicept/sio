import pandas as pd

def calculate_metrics(df):
    """
    Computes aggregated metrics from the cleaned dataframe.
    """
    if df.empty:
        return None, None, None, None

    # A) Panel scores table: panel_scores = sum(Final_Score) grouped by [AY, Semester, Studio_Code, Panel_ID]
    panel_scores = df.groupby(['AY', 'Semester', 'Studio_Code', 'Panel_ID'])['Final_Score'].sum().reset_index()

    # B) Studio-semester totals: studio_sem_total = sum(Final_Score) grouped by [AY, Semester, Studio_Code]
    studio_sem_total = df.groupby(['AY', 'Semester', 'Studio_Code'])['Final_Score'].sum().reset_index()
    studio_sem_total.rename(columns={'Final_Score': 'Studio_Total_Score'}, inplace=True)

    # C) Construct contribution: construct_scores = sum(Final_Score) grouped by [AY, Semester, Studio_Code, Construct_ID]
    construct_scores = df.groupby(['AY', 'Semester', 'Studio_Code', 'Construct_ID'])['Final_Score'].sum().reset_index()
    construct_scores.rename(columns={'Final_Score': 'Construct_Score'}, inplace=True)

    # construct_share = construct_scores / studio_sem_total (merge then divide)
    construct_share = pd.merge(construct_scores, studio_sem_total, on=['AY', 'Semester', 'Studio_Code'], how='left')
    construct_share['Construct_Share'] = construct_share['Construct_Score'] / construct_share['Studio_Total_Score']

    # SPREAD column at Studio_Code+Semester level for panel_scores
    spread_df = panel_scores.groupby(['AY', 'Semester', 'Studio_Code'])['Final_Score'].agg(['max', 'min']).reset_index()
    spread_df['SPREAD'] = spread_df['max'] - spread_df['min']

    panel_scores = pd.merge(panel_scores, spread_df[['AY', 'Semester', 'Studio_Code', 'SPREAD']], on=['AY', 'Semester', 'Studio_Code'], how='left')

    return panel_scores, studio_sem_total, construct_scores, construct_share
