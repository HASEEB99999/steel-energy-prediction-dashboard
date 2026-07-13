# ⚡ Steel Industry Energy Prediction Dashboard

## 📋 Overview
FastAPI dashboard for predicting energy consumption in steel manufacturing using Machine Learning.

**Model Performance:** RMSE 7.51 kWh | R² 0.862 | PCA (18→7 features, 95% variance)

---

## 🚀 Quick Start

```bash
# 1. Clone
https://github.com/HASEEB99999/steel-energy-prediction-dashboard
cd steel-energy-prediction-dashboard

# 2. Create Virtual Environment
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Run
python main.py

# 5. Open Browser
http://127.0.0.1:8000

📊 Routes
Route	       Description
/Home Page
/dashboard	   EDA Visualizations
/predict	   Prediction Form
/health	API Health Check

🛠️ Tech Stack

Backend:       FastAPI, Uvicorn, Jinja2
ML:            scikit-learn, joblib, pandas, numpy
Visualization: matplotlib, seaborn

├── main.py
├── templates/     # HTML files
├── static/        # Images
├── requirements.txt
└── README.md
Author: Haseeb Saleem