import os
import pandas as pd
from src.io import load_and_clean_data
from src.metrics import calculate_metrics

def test_backend():
    # File path
    data_path = "data/normalized_score_calculation_sample_V3.xlsx"

    # 1. Test data loading and cleaning
    print(f"Testing load_and_clean_data with {data_path}...")
    df = load_and_clean_data(data_path)

    assert not df.empty, "Dataframe is empty!"
    print(f"Data loaded. Shape: {df.shape}")

    # Verify expected columns
    expected_cols = ['AY', 'Semester', 'Level', 'Studio_Code', 'Studio_Focus_Area', 'Panel_ID', 'Construct_ID', 'Question_No', 'Weight', 'Confidence', 'Final_Score']
    for col in expected_cols:
        assert col in df.columns, f"Missing expected column: {col}"

    # Verify data types
    assert pd.api.types.is_integer_dtype(df['Question_No']) or isinstance(df['Question_No'].dtype, pd.Int64Dtype), f"Question_No is not int: {df['Question_No'].dtype}"
    assert pd.api.types.is_float_dtype(df['Weight']), f"Weight is not float: {df['Weight'].dtype}"
    assert pd.api.types.is_float_dtype(df['Confidence']), f"Confidence is not float: {df['Confidence'].dtype}"
    assert pd.api.types.is_float_dtype(df['Final_Score']), f"Final_Score is not float: {df['Final_Score'].dtype}"

    print("Data cleaning verification passed.")

    # 2. Test metrics calculation
    print("Testing calculate_metrics...")
    panel_scores, studio_sem_total, construct_scores, construct_share = calculate_metrics(df)

    assert panel_scores is not None, "panel_scores is None"
    assert 'SPREAD' in panel_scores.columns, "SPREAD column missing in panel_scores"
    assert studio_sem_total is not None, "studio_sem_total is None"
    assert 'Studio_Total_Score' in studio_sem_total.columns, "Studio_Total_Score column missing"
    assert construct_share is not None, "construct_share is None"
    assert 'Construct_Share' in construct_share.columns, "Construct_Share column missing"

    print("Metrics calculation verification passed.")
    print("All backend tests passed successfully!")

if __name__ == "__main__":
    try:
        test_backend()
    except Exception as e:
        print(f"Backend test failed: {e}")
        exit(1)
