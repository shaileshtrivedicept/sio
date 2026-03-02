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

    # Read the revised file (single sheet, no leading blanks)
    # Specifying sheet_name='Normalized Score' to be explicit and avoid sheet naming issues
    df = pd.read_excel(file_path, sheet_name='Normalized Score')

    # Drop any columns whose name starts with "Unnamed"
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Convert numeric fields
    df['Question_No'] = pd.to_numeric(df['Question_No'], errors='coerce').astype('Int64')
    df['Weight'] = pd.to_numeric(df['Weight'], errors='coerce').astype(float)
    df['Confidence'] = pd.to_numeric(df['Confidence'], errors='coerce').astype(float)
    df['Final_Score'] = pd.to_numeric(df['Final_Score'], errors='coerce').astype(float)

    # Treat missing Notes safely
    df['Notes'] = df['Notes'].astype(str).replace('nan', '')

    # Drop rows where essential identifiers are missing
    df = df.dropna(subset=['AY', 'Semester', 'Studio_Code', 'Panel_ID'])

    return df
