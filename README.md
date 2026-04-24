# 🔄 Customer Churn Prediction — End-to-End MLOps Pipeline

> A **production-grade, fully open-source MLOps system** for predicting customer churn in real time — built with Kafka, XGBoost, MLflow, FastAPI, Prometheus, Grafana, Evidently AI, DVC, and Kubernetes.

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![MLflow](https://img.shields.io/badge/MLflow-Tracking-orange?logo=mlflow)](https://mlflow.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Serving-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Kafka](https://img.shields.io/badge/Kafka-Streaming-black?logo=apachekafka)](https://kafka.apache.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?logo=kubernetes)](https://kubernetes.io/)
[![DVC](https://img.shields.io/badge/DVC-Pipeline-945DD6?logo=dvc)](https://dvc.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Running the Pipeline](#-running-the-pipeline)
- [API Reference](#-api-reference)
- [Monitoring](#-monitoring)
- [Model Retraining](#-model-retraining)
- [Kubernetes Deployment](#-kubernetes-deployment)
- [Contributing](#-contributing)
- [Author](#-author)

---

## 🌟 Overview

This project implements a **complete, end-to-end MLOps pipeline** for Customer Churn Prediction using only free and open-source tools — no paid cloud services required. It simulates a real-world production ML system that:

- **Streams** live customer data via **Apache Kafka**
- **Trains** XGBoost/LightGBM models tracked in **MLflow**
- **Serves** predictions via a **FastAPI** REST API
- **Monitors** model health with **Prometheus** + **Grafana**
- **Detects** data drift using **Evidently AI**
- **Automates** retraining with **DVC pipelines**
- **Orchestrates** everything with **Docker Compose** and **Kubernetes**

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     MLOps Churn System                          │
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────────────┐  │
│  │ Data Gen │───▶│  Kafka   │───▶│  Consumer / Feature Eng  │  │
│  └──────────┘    │ Zookeeper│    └────────────┬─────────────┘  │
│                  └──────────┘                 │                │
│                                               ▼                │
│  ┌──────────┐    ┌──────────┐    ┌────────────────────────┐   │
│  │  MLflow  │◀───│  Train   │◀───│   DVC Pipeline (DVC)   │   │
│  │ Tracking │    │ XGBoost  │    └────────────────────────┘   │
│  └──────────┘    └────┬─────┘                                  │
│                       │                                        │
│                       ▼                                        │
│            ┌──────────────────┐    ┌─────────────────────┐    │
│            │  FastAPI Server  │───▶│ Prometheus + Grafana │    │
│            │  /predict API    │    │    (Monitoring)      │    │
│            └──────────────────┘    └─────────────────────┘    │
│                       │                                        │
│                       ▼                                        │
│            ┌──────────────────┐                               │
│            │   Evidently AI   │                               │
│            │  (Drift Reports) │                               │
│            └──────────────────┘                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| **Data Streaming** | Apache Kafka + Zookeeper | Real-time customer event streaming |
| **ML Training** | XGBoost, LightGBM, Scikit-learn | Model training & evaluation |
| **Experiment Tracking** | MLflow | Model versioning & registry |
| **Model Serving** | FastAPI + Uvicorn | REST API for predictions |
| **Monitoring** | Prometheus + Grafana | Metrics & dashboards |
| **Drift Detection** | Evidently AI | Data & model drift alerts |
| **Pipeline Automation** | DVC | Reproducible ML pipelines |
| **Containerization** | Docker + Docker Compose | Service orchestration |
| **Orchestration** | Kubernetes (k8s) | Production deployment |
| **Data Processing** | Pandas, NumPy | Feature engineering |

---

## 📁 Project Structure

```
Customer_Churn_MLOps/
│
├── 📂 data/
│   └── raw_data.csv              # Raw customer churn dataset
│
├── 📂 src/
│   ├── 📂 stream/
│   │   ├── producer.py           # Kafka producer (simulates live data)
│   │   └── consumer.py           # Kafka consumer (processes events)
│   ├── 📂 models/
│   │   └── train.py              # XGBoost model training + MLflow logging
│   ├── 📂 features/              # Feature engineering modules
│   ├── 📂 serve/
│   │   └── app.py                # FastAPI prediction service
│   └── 📂 monitor/               # Evidently drift detection
│
├── 📂 k8s/
│   └── deployment.yaml           # Kubernetes deployment manifest
│
├── 📂 .github/                   # GitHub Actions CI/CD workflows
│
├── 🐳 Dockerfile                 # App container definition
├── 🐳 docker-compose.yml         # Multi-service orchestration
├── 📋 dvc.yaml                   # DVC pipeline definition
├── 📊 prometheus.yml             # Prometheus scrape config
├── 📦 requirements.txt           # Python dependencies
├── 🔧 generate_data.py           # Synthetic data generator
└── 📤 export_model.py            # Model export utility
```

---

## 🚀 Getting Started

### Prerequisites

Ensure the following are installed on your machine:

- [Python 3.11+](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/) (for Kubernetes)
- [DVC](https://dvc.org/doc/install) (`pip install dvc`)
- [Git](https://git-scm.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/ayeswar/MLOPS-CHURN-PREDIC-TION-END-TO-END.git
cd MLOPS-CHURN-PREDIC-TION-END-TO-END
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate Synthetic Data (optional)

```bash
python generate_data.py
```

---

## ⚙️ Running the Pipeline

### Step 1 — Start All Services with Docker Compose

This launches **Kafka, Zookeeper, MLflow, Prometheus, and Grafana** with one command:

```bash
docker-compose up -d
```

| Service | URL |
|---------|-----|
| MLflow UI | http://localhost:5000 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 (admin/admin) |
| Kafka Broker | localhost:29092 |

### Step 2 — Run the DVC Training Pipeline

```bash
dvc repro
```

This triggers `src/models/train.py` which:
- Loads `data/raw_data.csv`
- Trains an XGBoost model
- Logs metrics and artifacts to MLflow

### Step 3 — Start Kafka Streaming

```bash
# Terminal 1 — Start Producer
python src/stream/producer.py

# Terminal 2 — Start Consumer
python src/stream/consumer.py
```

### Step 4 — Launch the Prediction API

```bash
uvicorn src.serve.app:app --reload --port 8000
```

API docs available at: **http://localhost:8000/docs**

---

## 📡 API Reference

### `POST /predict`

Predict churn probability for a customer.

**Request Body:**
```json
{
  "tenure": 12,
  "monthly_charges": 65.5,
  "total_charges": 786.0,
  "contract": "Month-to-month",
  "payment_method": "Electronic check",
  "internet_service": "Fiber optic"
}
```

**Response:**
```json
{
  "churn_probability": 0.82,
  "prediction": "Churn",
  "confidence": "High"
}
```

### `GET /health`

Returns API health status and model metadata.

### `GET /metrics`

Prometheus-compatible metrics endpoint.

---

## 📊 Monitoring

### Grafana Dashboards

1. Open Grafana at **http://localhost:3000**
2. Login: `admin / admin`
3. Add Prometheus as a data source (`http://prometheus:9090`)
4. Import dashboard or build custom panels for:
   - Prediction request rates
   - Latency percentiles (p50, p95, p99)
   - Error rates
   - Model drift alerts

### Evidently AI — Drift Detection

Run the monitoring report:

```bash
python src/monitor/drift_report.py
```

Generates an HTML report showing:
- Dataset drift metrics
- Feature distribution shifts
- Model performance degradation

---

## 🔁 Model Retraining

The DVC pipeline automates retraining when new data arrives:

```bash
# Pull latest data
dvc pull

# Reproduce pipeline (only reruns changed stages)
dvc repro

# Push updated model artifacts
dvc push
```

DVC tracks:
- `data/raw_data.csv` — Input data
- `src/models/train.py` — Training script
- Auto-versioned model artifacts in `mlruns/`

---

## ☸️ Kubernetes Deployment

Deploy the FastAPI serving container to Kubernetes:

```bash
# Apply deployment manifest
kubectl apply -f k8s/deployment.yaml

# Check pod status
kubectl get pods

# View logs
kubectl logs -l app=churn-predictor
```

The `k8s/deployment.yaml` defines:
- Deployment with replica sets
- Service for external access
- Resource limits and health probes

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 👨‍💻 Author

**Papannagari Ayeswararao**  
📧 [ayeswararao@email.com](mailto:ayeswararao@email.com)  
📞 +91-6302587178  
🔗 [GitHub](https://github.com/ayeswar) | [LinkedIn](https://linkedin.com/in/ayeswararao)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

⭐ **Star this repo if you found it helpful!** ⭐

*Built with ❤️ using 100% open-source tools*

</div>
