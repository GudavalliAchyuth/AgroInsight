# 🌿 AgroInsight | Enterprise Agritech Ecosystem

AgroInsight is an enterprise-grade AI ecosystem designed to empower sustainable agriculture through deep learning, predictive analytics, and real-time multilingual data insights. 

## 🚀 Core Architecture
This project utilizes a modern, decoupled architecture:
* **Backend:** FastAPI (Python 3.10) for high-performance, asynchronous API routing.
* **Frontend:** Streamlit for a responsive, data-rich user interface.
* **AI/ML Layer:** TensorFlow/Keras for Computer Vision & Time-Series Forecasting, and Google Gemini 2.5 Flash for multi-modal reasoning.

## 🧠 System Modules
1. **📸 Crop Disease Vision Lab:** CNN trained on 50,000+ images to detect 26 diseases across 14 crop species.
2. **📈 Market Price Forecaster:** LSTM-based forecasting using historical APMC data for optimal sell-window prediction.
3. **🧪 Soil Health Analyzer:** Automated N-P-K and pH evaluation for AI-driven fertilizer prescriptions.
4. **🤖 AgriBot (Vision Enabled):** Multi-modal AI assistant for interactive, multilingual farming advice.
5. **🏛️ Govt Schemes Matcher:** Dynamic regional matching for government agricultural support.

### 🔑 Environment Setup
This project uses the Google Gemini API for intelligent agricultural advice. You will need to provide your own API key to run the backend locally.

1. Navigate to the `backend` directory.
2. Duplicate the `.env.example` file and rename the copy to `.env`.
3. Open the new `.env` file and replace `"your_api_key_here"` with your actual Gemini API key.

## ⚙️ How to Run Locally
1. Clone the repository: `git clone https://github.com/GudavalliAchyuth/AgroInsight.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Start the FastAPI backend: `uvicorn backend.main:app --reload`
4. Launch the Streamlit frontend: `streamlit run frontend/app.py`
