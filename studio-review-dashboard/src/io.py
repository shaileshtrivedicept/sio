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

    # Read with pandas: pd.read_excel(file, sheet_name="Normalized Score", header=3)
    # The "Normalized Score" sheet contains the pre-calculated weighted Final_Score
    df = pd.read_excel(file_path, sheet_name="Normalized Score", header=3)

    # Then set columns from the first row of the resulting dataframe
    cols = df.iloc[0].tolist()
    df = df.iloc[1:].copy()
    df.columns = cols

    # Drop any columns whose name is NaN (there are many trailing blank columns in this sheet)
    df = df.loc[:, [c for c in df.columns if pd.notna(c)]]

    # In the "Normalized Score" sheet, some column names are duplicated (e.g., Weight, Confidence)
    # We want to keep the first occurrence of each column name.
    df = df.loc[:, ~df.columns.duplicated()]

    # Special fix: the first column 'AY' is read as '0' in the "Normalized Score" sheet
    if '0' in df.columns:
        df = df.rename(columns={'0': 'AY'})

    # Convert numeric fields: Question_No -> int (or nullable Int64)
    # Weight, Confidence, Final_Score -> float
    df['Question_No'] = pd.to_numeric(df['Question_No'], errors='coerce').astype('Int64')
    df['Weight'] = pd.to_numeric(df['Weight'], errors='coerce').astype(float)
    df['Confidence'] = pd.to_numeric(df['Confidence'], errors='coerce').astype(float)
    df['Final_Score'] = pd.to_numeric(df['Final_Score'], errors='coerce').astype(float)

    # Treat missing Notes safely (keep as string / nullable)
    df['Notes'] = df['Notes'].astype(str).replace('nan', '')

    # Drop rows where essential identifiers are missing (optional but recommended)
    df = df.dropna(subset=['AY', 'Semester', 'Studio_Code', 'Panel_ID'])

    return df
