import pandas as pd
import os
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

def check_data_drift():
    data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw_data.csv')
    
    if not os.path.exists(data_path):
        print("Data file not found.")
        return False
        
    df = pd.read_csv(data_path)
    
    # Not enough data to check drift
    if len(df) < 200:
        print("Not enough data to check drift yet.")
        return False
        
    # Split the dataset: older half is reference, newer half is current
    midpoint = len(df) // 2
    reference = df.iloc[:midpoint]
    current = df.iloc[midpoint:]
    
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference, current_data=current)
    
    # Get the drift result
    result = report.as_dict()
    dataset_drift = result['metrics'][0]['result']['dataset_drift']
    
    if dataset_drift:
        print("Data drift detected! Triggering retraining pipeline...")
        # Here we could trigger an Airflow DAG, Github Action, or just run DVC locally
        return True
    else:
        print("No data drift detected.")
        return False

if __name__ == "__main__":
    check_data_drift()
