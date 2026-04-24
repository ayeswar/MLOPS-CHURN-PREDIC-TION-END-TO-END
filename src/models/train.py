import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.pipeline import Pipeline
import xgboost as xgb
import mlflow
import mlflow.sklearn

def load_and_preprocess_data(data_path):
    # Load data
    df = pd.read_csv(data_path)
    
    # Feature selection
    # Drop customer_id as it's not a predictive feature
    features = ['age', 'tenure', 'balance', 'num_products', 'has_cr_card', 'is_active_member', 'estimated_salary']
    target = 'churn'
    
    X = df[features]
    y = df[target]
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    return X_train, X_test, y_train, y_test

def main():
    # Set up MLflow
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("Customer_Churn_Prediction")

    data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw_data.csv')
    
    if not os.path.exists(data_path):
        print(f"Data file not found at {data_path}. Ensure the consumer is running and writing data.")
        return

    # Load and preprocess
    X_train, X_test, y_train, y_test = load_and_preprocess_data(data_path)
    
    # Model parameters
    params = {
        'objective': 'binary:logistic',
        'max_depth': 6,
        'learning_rate': 0.1,
        'n_estimators': 100,
        'random_state': 42
    }

    # Start MLflow run
    with mlflow.start_run():
        print("Training XGBoost model...")
        
        # Create a pipeline
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', xgb.XGBClassifier(**params))
        ])
        
        pipeline.fit(X_train, y_train)

        # Make predictions
        y_pred = pipeline.predict(X_test)

        # Calculate metrics
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1': f1_score(y_test, y_pred)
        }
        
        print("Model metrics:", metrics)

        # Log parameters and metrics
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)

        # Infer signature and log model
        signature = mlflow.models.infer_signature(X_train, pipeline.predict(X_train))
        mlflow.sklearn.log_model(
            sk_model=pipeline,
            artifact_path="xgboost-model",
            signature=signature,
            registered_model_name="CustomerChurnXGB"
        )
        print("Model saved to MLflow and registered as 'CustomerChurnXGB'")

if __name__ == "__main__":
    main()
