# ============================================
# main.py - Working Model
# ============================================
# importing libraries

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import numpy as np
import joblib
import os
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

print("=" * 50)
print("LOADING MODELS...")
print("=" * 50)

MODEL_READY = False
scaler = None
pca = None
model = None

# Load models
try:
    scaler = joblib.load(BASE_DIR / "scaler.pkl")
    print("✅ scaler.pkl loaded")
except:
    print("❌ scaler.pkl not found")

try:
    pca = joblib.load(BASE_DIR / "pca_transformer.pkl")
    print("✅ pca_transformer.pkl loaded")
except:
    print("❌ pca_transformer.pkl not found")

try:
    model = joblib.load(BASE_DIR / "best_model_pca.pkl")
    print("✅ best_model_pca.pkl loaded")
except:
    print("❌ best_model_pca.pkl not found")

if scaler and pca and model:
    MODEL_READY = True
    print("✅ All models loaded successfully!")
else:
    print("⚠️ Models not loaded. Prediction will use demo mode.")

print("=" * 50)


# ============================================
# Routes
# ============================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "active_page": "home"})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "active_page": "dashboard"})


@app.get("/predict", response_class=HTMLResponse)
async def predict_page(request: Request):
    return templates.TemplateResponse("predict.html", {
        "request": request,
        "active_page": "predict",
        "prediction": None
    })


@app.post("/predict", response_class=HTMLResponse)
async def predict(
        request: Request,
        Lagging_Current_Reactive_Power_kVarh: float = Form(...),
        Leading_Current_Reactive_Power_kVarh: float = Form(...),
        Lagging_Current_Power_Factor: float = Form(...),
        Leading_Current_Power_Factor: float = Form(...),
        NSM: float = Form(...),
        hour: int = Form(...),
        month: int = Form(...),
        is_weekend: int = Form(...),
        Power_Factor_Ratio: float = Form(...),
        Load_Type: str = Form(...),
        Day_of_week: str = Form(...)
):
    try:
        if not MODEL_READY:
            # Demo prediction if models not loaded
            prediction = 25.5
            return templates.TemplateResponse("predict.html", {
                "request": request,
                "active_page": "predict",
                "prediction": f"{prediction} (Demo)"
            })

        # Create feature dictionary
        feature_dict = {
            'Lagging_Current_Reactive.Power_kVarh': Lagging_Current_Reactive_Power_kVarh,
            'Leading_Current_Reactive.Power_kVarh': Leading_Current_Reactive_Power_kVarh,
            'Lagging_Current_Power_Factor': Lagging_Current_Power_Factor,
            'Leading_Current_Power_Factor': Leading_Current_Power_Factor,
            'NSM': NSM,
            'hour': hour,
            'month': month,
            'is_weekend': is_weekend,
            'Power_Factor_Ratio': Power_Factor_Ratio
        }

        # Load Type encoding
        load_types = ['Load_Type_Light_Load', 'Load_Type_Medium_Load', 'Load_Type_Maximum_Load']
        for lt in load_types:
            feature_dict[lt] = 0

        if Load_Type == 'Light_Load':
            feature_dict['Load_Type_Light_Load'] = 1
        elif Load_Type == 'Medium_Load':
            feature_dict['Load_Type_Medium_Load'] = 1
        else:
            feature_dict['Load_Type_Maximum_Load'] = 1

        # Day of week encoding
        days = ['Day_of_week_Monday', 'Day_of_week_Tuesday', 'Day_of_week_Wednesday',
                'Day_of_week_Thursday', 'Day_of_week_Friday', 'Day_of_week_Saturday',
                'Day_of_week_Sunday']
        for d in days:
            feature_dict[d] = 0
        feature_dict[f'Day_of_week_{Day_of_week}'] = 1

        # Create input array
        feature_names = scaler.feature_names_in_
        input_data = [feature_dict.get(f, 0) for f in feature_names]
        input_array = np.array(input_data).reshape(1, -1)

        # Transform and predict
        input_scaled = scaler.transform(input_array)
        input_pca = pca.transform(input_scaled)
        prediction = model.predict(input_pca)[0]
        prediction = round(prediction, 2)

    except Exception as e:
        prediction = f"Error: {str(e)}"

    return templates.TemplateResponse("predict.html", {
        "request": request,
        "active_page": "predict",
        "prediction": prediction
    })


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": MODEL_READY,
        "scaler": scaler is not None,
        "pca": pca is not None,
        "model": model is not None
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)