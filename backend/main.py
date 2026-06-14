# backend/main.py

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import io
import os
import google.generativeai as genai

app = FastAPI(title="AgroInsight Enterprise API", version="7.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# --- 1. API Configuration ---
# Hardened global system instructions to guarantee multilingual output compliance
genai.configure(api_key="AQ.Ab8RN6KixhBP712ZagN5y2QA2l1PrTBjdm0sQ2VI6CyGATFJzw") 
llm = genai.GenerativeModel(
    'gemini-2.5-flash',
    system_instruction="You are AgriBot, an expert multilingual agronomy assistant. You must always deliver your entire analysis, recommendations, structural sections, and advice strictly in the language requested by the user. Never mix English into the localized response."
)

# --- 2. Schemas ---
# Added language fields to SoilMetrics and MarketQuery to capture frontend settings
class SoilMetrics(BaseModel):
    nitrogen: float
    phosphorus: float
    potassium: float
    ph: float
    target_crop: str
    language: str = "English"

class MarketQuery(BaseModel):
    commodity: str
    market_region: str
    language: str = "English"

class ChatQuery(BaseModel):
    message: str
    language: str

class SchemeQuery(BaseModel):
    state: str
    crop: str
    farm_size: float
    language: str

# --- 3. Deep Learning Models ---
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CNN_PATH = os.path.join(BASE_DIR, "models", "plant_disease_cnn.h5")
model_cnn = None

CLASS_NAMES = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy', 'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy'] 

@app.on_event("startup")
async def load_models():
    global model_cnn
    try: model_cnn = load_model(CNN_PATH)
    except: pass

def process_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return np.expand_dims(img_to_array(img.resize((224, 224))), axis=0)

# --- 4. Core Endpoints ---
@app.post("/predict-disease/")
async def predict_disease(language: str = "English", file: UploadFile = File(...)):
    if model_cnn is None: raise HTTPException(status_code=503, detail="AI Offline")
    try:
        processed_img = process_image(await file.read())
        preds = model_cnn.predict(processed_img)[0]
        idx = np.argmax(preds)
        disease = CLASS_NAMES[idx]
        
        prompt = f"Expert agronomy advice for '{disease}'. CRITICAL: You must write the entire explanation and terms in {language}. Format exactly: [SUMMARY] text [BIOLOGICAL] text [CHEMICAL] text [PREVENTION] text."
        resp = llm.generate_content(prompt).text
        
        def ex(tag):
            try: return resp.split(f"[{tag}]")[1].split("[")[0].strip()
            except: return "N/A"
            
        return {
            "disease": disease.replace("___", " - ").replace("_", " "), 
            "confidence": f"{float(preds[idx])*100:.2f}%", 
            "recommendations": {"summary": ex("SUMMARY"), "biological": ex("BIOLOGICAL"), "chemical": ex("CHEMICAL"), "prevention": ex("PREVENTION")}
        }
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "ResourceExhausted" in error_msg:
            raise HTTPException(status_code=429, detail="API Speed Limit Reached. Please wait 30 seconds.")
        raise HTTPException(status_code=500, detail=error_msg)

@app.post("/analyze-soil/")
async def analyze_soil(metrics: SoilMetrics):
    try:
        # Strict language constraint injected into the prompt context
        prompt = (
            f"Analyze soil data for targeting {metrics.target_crop}: Nitrogen: {metrics.nitrogen}, Phosphorus: {metrics.phosphorus}, Potassium: {metrics.potassium}, pH: {metrics.ph}. "
            f"CRITICAL: You MUST write the complete response entirely in {metrics.language}. "
            f"Format exactly as: [ANALYSIS] text [RECOMMENDATION] text."
        )
        text = llm.generate_content(prompt).text
        return {
            "status": "Optimal" if 5.5 < metrics.ph < 7.5 else "Needs Adjustment", 
            "analysis": text.split("[ANALYSIS]")[1].split("[")[0].strip(), 
            "prescription": text.split("[RECOMMENDATION]")[1].strip()
        }
    except Exception as e: 
        if "429" in str(e): raise HTTPException(status_code=429, detail="API Speed Limit Reached. Please wait 30 seconds.")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict-price/")
async def predict_price(query: MarketQuery):
    try:
        base = {"Tomato": 2200, "Potato": 1600, "Rice": 3100, "Wheat": 2400, "Maize": 1900}.get(query.commodity, 2000)
        np.random.seed(len(query.commodity))
        hist = [int(base + (np.sin(i/3) * 150) + np.random.randint(-50, 50)) for i in range(30)]
        forecast = [int(hist[-1] + (i * 45) + np.random.randint(-30, 30)) for i in range(1, 8)]
        best = int(np.argmax(forecast) + 1)
        
        # Injected explicit language localized rule
        prompt = f"Analyze market price trend configurations for {query.commodity}. Peak profitability occurs on Day {best}. Provide exactly 2 sentences of strategic advice. CRITICAL: You must write the entire advice in {query.language}."
        resp = llm.generate_content(prompt).text
        
        return {"commodity": query.commodity, "current_price": f"₹{hist[-1]}/q", "historical_trend": hist, "forecast_trend": forecast, "optimal_sell_window": f"Day {best}", "market_strategy": resp}
    except Exception as e:
        if "429" in str(e): raise HTTPException(status_code=429, detail="API Speed Limit Reached. Please wait 30 seconds.")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/match-scheme/")
async def match_scheme(query: SchemeQuery):
    try:
        resp = llm.generate_content(f"Find 2 Indian govt agricultural schemes for a farmer in {query.state} growing {query.crop} on {query.farm_size} acres. CRITICAL: You must write the entire descriptive details and names in {query.language}.")
        return {"schemes": resp.text}
    except Exception as e:
        if "429" in str(e): raise HTTPException(status_code=429, detail="API Speed Limit Reached. Please wait 30 seconds.")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vision-chat/")
async def vision_chat(message: str = Form(...), language: str = Form(...), file: Optional[UploadFile] = File(None)):
    try:
        prompt = f"You are AgriBot, an AI agronomy expert. Answer concisely. CRITICAL: You must reply entirely in {language}. Prompt: {message}"
        if file is not None and file.filename != "":
            img_bytes = await file.read()
            img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            resp = llm.generate_content([prompt, img])
        else:
            resp = llm.generate_content(prompt)
        return {"reply": resp.text}
    except Exception as e: 
        print(f"🚨 VISION CHAT CRASHED: {str(e)}")
        if "429" in str(e): raise HTTPException(status_code=429, detail="API Speed Limit Reached. Please wait 30 seconds.")
        raise HTTPException(status_code=500, detail=str(e))