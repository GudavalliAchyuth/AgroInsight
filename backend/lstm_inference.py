# backend/lstm_inference.py

from tensorflow.keras.models import load_model
import numpy as np
import pickle
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "apmc_price_lstm.h5")
SCALER_PATH = os.path.join(BASE_DIR, "models", "price_scaler.pkl")

def predict_next_price(last_30_days_prices):
    """
    Takes a list of 30 integers (prices), processes them, 
    and predicts tomorrow's price.
    """
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        return None
        
    # Load model and scaler
    model = load_model(MODEL_PATH)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
        
    # Convert input list to numpy array and shape it
    input_data = np.array(last_30_days_prices).reshape(-1, 1)
    
    # Scale input
    scaled_input = scaler.transform(input_data)
    
    # Reshape for LSTM: [1 sample, 30 time steps, 1 feature]
    final_input = np.reshape(scaled_input, (1, len(scaled_input), 1))
    
    # Predict
    scaled_prediction = model.predict(final_input)
    
    # Invert scaling back to actual Rupee currency value
    predicted_price = scaler.inverse_transform(scaled_prediction)
    
    return float(predicted_price[0][0])