import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_and_clean_data(file_path):
    """
    Loads and cleans the studio review data from an Excel file.
    """
    if not os.path.exists(file_path):
        return pd.DataFrame()

    # Read with pandas: pd.read_excel(file, sheet_name="Normalized Score (2)", header=3)
    df = pd.read_excel(file_path, sheet_name="Normalized Score (2)", header=3)

    # Then set columns from the first row of the resulting dataframe
    cols = df.iloc[0].tolist()
    df = df.iloc[1:].copy()
    df.columns = cols

    # Drop any columns whose name is NaN (there are 1–2 trailing blank columns)
    df = df.loc[:, [c for c in df.columns if pd.notna(c)]]

    # Convert numeric fields: Question_No -> int (or nullable Int64)
    # Weight, Confidence, Final_Score -> float
    df['Question_No'] = pd.to_numeric(df['Question_No'], errors='coerce').astype('Int64')
    df['Weight'] = pd.to_numeric(df['Weight'], errors='coerce').astype(float)
    df['Confidence'] = pd.to_numeric(df['Confidence'], errors='coerce').astype(float)
    df['Final_Score'] = pd.to_numeric(df['Final_Score'], errors='coerce').astype(float)

    # Calculate weighted Final_Score: Final_Score * Weight * Confidence
    # This ensures the totals match the summary sheets in the Excel file
    df['Final_Score'] = df['Final_Score'] * df['Weight'].fillna(0) * df['Confidence'].fillna(0)

    # Treat missing Notes safely (keep as string / nullable)
    df['Notes'] = df['Notes'].astype(str).replace('nan', '')

    # Drop rows where essential identifiers are missing (optional but recommended)
    df = df.dropna(subset=['AY', 'Semester', 'Studio_Code', 'Panel_ID'])

    return df
