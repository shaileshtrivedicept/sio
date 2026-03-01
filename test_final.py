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

    if df.empty:
        print("Dataframe is empty!")
        return False

    # 2. Test metrics calculation
    print("Testing calculate_metrics...")
    panel_scores, studio_sem_total, construct_scores, construct_share = calculate_metrics(df)

    if panel_scores is None:
        print("Metrics calculation failed!")
        return False

    print("All backend tests passed successfully!")
    return True

if __name__ == "__main__":
    if test_backend():
        exit(0)
    else:
        exit(1)
