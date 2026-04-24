import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import mlflow
from prometheus_client import make_asgi_app, Counter, Histogram
import time

app = FastAPI(title="Customer Churn Prediction API")

# Add prometheus asgi middleware to route /metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Prometheus Metrics
REQUEST_COUNT = Counter("api_predictions_total", "Total predictions requested", ["status"])
PREDICTION_PROB_HISTOGRAM = Histogram("model_prediction_probability", "Distribution of prediction probabilities")
LATENCY_HISTOGRAM = Histogram("api_latency_seconds", "Latency of prediction requests")

class CustomerData(BaseModel):
    age: int
    tenure: int
    balance: float
    num_products: int
    has_cr_card: int
    is_active_member: int
    estimated_salary: float

model = None

@app.on_event("startup")
def load_model():
    global model
    mlflow.set_tracking_uri("http://localhost:5000")
    model_name = "CustomerChurnXGB"
    
    print(f"Loading latest model from MLflow Registry: {model_name}...")
    try:
        # Load the latest Production or None stage model
        model = mlflow.sklearn.load_model(f"models:/{model_name}/latest")
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Warning: Could not load model {model_name}. Error: {e}")

@app.post("/predict")
def predict(data: CustomerData):
    start_time = time.time()
    
    if model is None:
        REQUEST_COUNT.labels(status="error").inc()
        raise HTTPException(status_code=503, detail="Model not loaded")
        
    try:
        # Convert to DataFrame
        df = pd.DataFrame([data.dict()])
        
        # Predict probability
        # Note: In a real system, the scaler needs to be applied here as well!
        # For simplicity in this example, assuming model handles or scaler is bundled in pipeline.
        # To make it robust, a scikit-learn Pipeline combining scaler and xgboost should be logged in MLflow.
        
        # We will just predict class for now
        prediction = model.predict(df)[0]
        
        # Assuming model.predict_proba exists for probabilities (xgboost loaded via mlflow might behave differently depending on objective)
        # prediction_prob = model.predict_proba(df)[0][1]
        
        # Record metrics
        # PREDICTION_PROB_HISTOGRAM.observe(prediction_prob)
        REQUEST_COUNT.labels(status="success").inc()
        LATENCY_HISTOGRAM.observe(time.time() - start_time)
        
        return {
            "prediction": int(prediction),
            # "probability": float(prediction_prob)
        }
    except Exception as e:
        REQUEST_COUNT.labels(status="error").inc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}
