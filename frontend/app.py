# frontend/app.py
import streamlit as st
import requests
from PIL import Image
import io
from gtts import gTTS
import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AgroInsight | Smart Farming",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 2. CUSTOM UI/UX CSS INJECTION (REFINED GLASS / DARK THEME) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    :root {
        --bg-0: #0a0f0c;
        --bg-1: #0e1511;
        --green: #4caf50;
        --green-light: #7ee08a;
        --green-mid: #66bb6a;
        --line: rgba(102,187,106,0.18);
        --line-strong: rgba(102,187,106,0.32);
        --text-muted: #9fb3a4;
        --glass: rgba(255,255,255,0.035);
    }

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp {
        background:
            radial-gradient(1100px 520px at 0% 0%, #15281c 0%, rgba(14,21,17,0) 55%),
            radial-gradient(900px 500px at 100% 0%, #122119 0%, rgba(10,15,12,0) 50%),
            linear-gradient(180deg, var(--bg-1) 0%, var(--bg-0) 100%);
    }

    /* Tighter, cleaner page padding */
    .block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1180px; }

    h1, h2, h3 { color: var(--green-light) !important; font-weight: 800 !important; letter-spacing: -0.5px; }
    h2, h3 { color: var(--green-mid) !important; }

    /* ---------- HERO ---------- */
    .hero {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, rgba(46,125,50,0.30), rgba(27,94,32,0.04));
        border: 1px solid var(--line-strong);
        border-radius: 22px;
        padding: 30px 34px;
        margin-bottom: 26px;
        backdrop-filter: blur(8px);
        box-shadow: 0 18px 50px rgba(0,0,0,0.35);
    }
    .hero::after {
        content: "";
        position: absolute; top: -40%; right: -10%;
        width: 360px; height: 360px;
        background: radial-gradient(circle, rgba(126,224,138,0.18), transparent 70%);
        pointer-events: none;
    }
    .hero h1 { margin: 0 0 8px 0; font-size: 2.15rem; font-weight: 900 !important; }
    .hero p { color: #c2d2c6; margin: 0; font-size: 1.05rem; max-width: 760px; line-height: 1.5; }
    .hero .badge-row { margin-top: 16px; display: flex; gap: 10px; flex-wrap: wrap; }
    .chip {
        display: inline-flex; align-items: center; gap: 6px;
        font-size: 0.78rem; font-weight: 600; color: #d7e7da;
        background: rgba(255,255,255,0.06);
        border: 1px solid var(--line);
        padding: 5px 12px; border-radius: 999px;
    }

    /* ---------- BUTTONS ---------- */
    div.stButton > button:first-child, div.stDownloadButton > button:first-child,
    div.stFormSubmitButton > button:first-child {
        background: linear-gradient(135deg, #43a047, #2e7d32);
        color: #ffffff !important;
        border-radius: 12px; border: none;
        padding: 0.64rem 1.15rem; font-weight: 700; letter-spacing: 0.2px;
        box-shadow: 0 6px 18px rgba(46,125,50,0.38);
        transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
    }
    div.stButton > button:first-child:hover, div.stDownloadButton > button:first-child:hover,
    div.stFormSubmitButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 24px rgba(46,125,50,0.55);
        background: linear-gradient(135deg, #4caf50, #1b5e20);
    }
    div.stButton > button:first-child:active { transform: translateY(0); }

    /* ---------- METRICS ---------- */
    div[data-testid="stMetric"] {
        background: linear-gradient(160deg, rgba(22,36,26,0.9), rgba(16,26,19,0.9));
        border: 1px solid var(--line-strong);
        border-radius: 16px; padding: 16px 18px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.30);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    div[data-testid="stMetric"]:hover { transform: translateY(-3px); border-color: var(--green); }
    div[data-testid="stMetricValue"] { color: #e8f5e9 !important; font-weight: 800; }
    div[data-testid="stMetricLabel"] { color: var(--text-muted) !important; font-weight: 600; }

    /* ---------- INPUTS ---------- */
    .stTextInput input, .stNumberInput input,
    .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        border-radius: 12px !important;
        background: var(--glass) !important;
        border: 1px solid var(--line) !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus { border-color: var(--green) !important; }

    /* ---------- TABS ---------- */
    button[data-baseweb="tab"] { font-weight: 600; }
    button[data-baseweb="tab"][aria-selected="true"] { color: var(--green-light) !important; }
    div[data-baseweb="tab-highlight"] { background-color: var(--green) !important; }

    /* ---------- FORM / CARD CONTAINER ---------- */
    div[data-testid="stForm"] {
        background: var(--glass);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 22px 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    }

    /* ---------- PILL ---------- */
    .pill {
        display: inline-block; padding: 5px 16px; border-radius: 999px;
        font-size: 0.85rem; font-weight: 700; letter-spacing: 0.3px; margin-bottom: 6px;
    }
    .pill-ok   { background: rgba(76,175,80,0.18);  color: var(--green-light); border: 1px solid rgba(76,175,80,0.45); }
    .pill-warn { background: rgba(239,83,80,0.16);  color: #ff8a80; border: 1px solid rgba(239,83,80,0.45); }

    /* ---------- SIDEBAR ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1a13, #0a0f0c);
        border-right: 1px solid var(--line);
    }
    section[data-testid="stSidebar"] .stRadio label { font-weight: 500; }
    section[data-testid="stSidebar"] .stRadio [role="radiogroup"] > label {
        padding: 6px 8px; border-radius: 10px; transition: background 0.15s ease;
    }
    section[data-testid="stSidebar"] .stRadio [role="radiogroup"] > label:hover {
        background: rgba(102,187,106,0.10);
    }

    hr { border-top: 1px solid var(--line-strong); opacity: 0.6; }

    /* ---------- EMPTY-STATE HINT ---------- */
    .hint {
        text-align: center; color: #8aa092; padding: 46px 24px;
        border: 1px dashed var(--line-strong); border-radius: 18px;
        background: rgba(255,255,255,0.02);
    }
    .hint .emoji { font-size: 2.6rem; display:block; margin-bottom: 10px; }
    .hint .label { font-size: 0.98rem; }

    /* Hide default Streamlit chrome for a cleaner look */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# --- 3. DYNAMIC TRANSLATION DICTIONARY ---
UI_TEXT = {
    "en": {
        "hero_title": "🌿 AgroInsight — Enterprise Ecosystem",
        "hero_sub": "Empowering sustainable agriculture through deep learning and actionable, real-time data insights.",
        "nav_weather": "🌦️ Live Weather Dashboard", "nav_vision": "🍂 Crop Disease Vision Lab",
        "nav_soil": "🧪 Soil Health Analyzer", "nav_market": "📈 Market Price Forecaster",
        "nav_scheme": "🏛️ Govt Schemes Matcher", "nav_chat": "🤖 AgriBot (Vision Enabled)",
        "btn_weather": "Fetch Conditions", "btn_vision": "⚡ Analyze Leaf Now",
        "btn_soil": "🧪 Generate Fertilizer Prescription", "btn_market": "📊 Run LSTM Forecast",
        "upload": "Upload Image", "search_loc": "🔍 Search Location (e.g., Hyderabad)",
        "weather_head": "🌦️ Real-Time Hyperlocal Weather", "vision_head": "📸 Pathogen Diagnostic Scanner",
        "soil_head": "🧪 Soil Chemical Profiling", "market_head": "📈 Deep Learning Price Forecaster",
        "scheme_head": "🏛️ Government Scheme Matcher", "chat_head": "🤖 AgriBot (Vision Enabled)",
        "listen": "🔊 Listen to Advice:"
    },
    "hi": {
        "hero_title": "🌿 एग्रोइनसाइट — एंटरप्राइज इकोसिस्टम",
        "hero_sub": "डीप लर्निंग और वास्तविक समय के डेटा के माध्यम से टिकाऊ कृषि को सशक्त बनाना।",
        "nav_weather": "🌦️ लाइव मौसम डैशबोर्ड", "nav_vision": "🍂 फसल रोग विजन लैब",
        "nav_soil": "🧪 मृदा स्वास्थ्य विश्लेषक", "nav_market": "📈 बाजार मूल्य पूर्वानुमान",
        "nav_scheme": "🏛️ सरकारी योजनाएं", "nav_chat": "🤖 एग्रीबॉट (विज़न चैट)",
        "btn_weather": "स्थितियां प्राप्त करें", "btn_vision": "⚡ अभी पत्ती का विश्लेषण करें",
        "btn_soil": "🧪 उर्वरक नुस्खा उत्पन्न करें", "btn_market": "📊 बाजार का पूर्वानुमान चलाएं",
        "upload": "छवि अपलोड करें", "search_loc": "🔍 स्थान खोजें (उदा., हैदराबाद)",
        "weather_head": "🌦️ वास्तविक समय स्थानीय मौसम", "vision_head": "📸 रोगज़नक़ नैदानिक स्कैनर",
        "soil_head": "🧪 मृदा रासायनिक प्रोफाइलिंग", "market_head": "📈 डीप लर्निंग मूल्य पूर्वानुमानकर्ता",
        "scheme_head": "🏛️ सरकारी योजना खोजक", "chat_head": "🤖 एग्रीबॉट (विज़न चैट)",
        "listen": "🔊 सलाह सुनें:"
    },
    "te": {
        "hero_title": "🌿 ఆగ్రోఇన్‌సైట్ — ఎంటర్‌ప్రైజ్ ఎకోసిస్టమ్",
        "hero_sub": "డీప్ లెర్నింగ్ మరియు రియల్ టైమ్ డేటా ద్వారా స్థిరమైన వ్యవసాయాన్ని శక్తివంతం చేయడం.",
        "nav_weather": "🌦️ ప్రత్యక్ష వాతావరణ డాష్‌బోర్డ్", "nav_vision": "🍂 పంట వ్యాధి విజన్ ల్యాబ్",
        "nav_soil": "🧪 నేల ఆరోగ్య విశ్లేషకం", "nav_market": "📈 మార్కెట్ ధర అంచనా",
        "nav_scheme": "🏛️ ప్రభుత్వ పథకాలు", "nav_chat": "🤖 అగ్రిబాట్ (విజన్ చాట్)",
        "btn_weather": "వాతావరణాన్ని పొందండి", "btn_vision": "⚡ ఆకును ఇప్పుడే విశ్లేషించండి",
        "btn_soil": "🧪 ఎరువుల ప్రిస్క్రిప్షన్ రూపొందించండి", "btn_market": "📊 మార్కెట్ అంచనాను అమలు చేయండి",
        "upload": "చిత్రాన్ని అప్‌లోడ్ చేయండి", "search_loc": "🔍 స్థానాన్ని శోధించండి (ఉదా., హైదరాబాద్)",
        "weather_head": "🌦️ రియల్ టైమ్ వాతావరణం", "vision_head": "📸 వ్యాధికారక రోగనిర్ధారణ స్కానర్",
        "soil_head": "🧪 నేల రసాయన ప్రొఫైలింగ్", "market_head": "📈 డీప్ లెర్నింగ్ ధర అంచనా",
        "scheme_head": "🏛️ ప్రభుత్వ పథకాల శోధన", "chat_head": "🤖 అగ్రిబాట్ (విజన్ చాట్)",
        "listen": "🔊 సలహా వినండి:"
    },
    "mr": {
        "hero_title": "🌿 ॲग्रोइनसाइट — एंटरप्राइझ इकोसिस्टम",
        "hero_sub": "डीप लर्निंग आणि रिअल-टाइम डेटा अंतर्दृष्टीद्वारे शाश्वत शेतीला सक्षम करणे.",
        "nav_weather": "🌦️ थेट हवामान डॅशबोर्ड", "nav_vision": "🍂 पीक रोग व्हिजन लॅब",
        "nav_soil": "🧪 मृदा आरोग्य विश्लेषक", "nav_market": "📈 बाजार भाव अंदाज",
        "nav_scheme": "🏛️ सरकारी योजना", "nav_chat": "🤖 ॲग्रिबॉट (व्हिजन चॅट)",
        "btn_weather": "स्थिती मिळवा", "btn_vision": "⚡ आता पानाचे विश्लेषण करा",
        "btn_soil": "🧪 खत प्रिस्क्रिप्शन व्युत्पन्न करा", "btn_market": "📊 बाजार अंदाज चालवा",
        "upload": "प्रतिमा अपलोड करा", "search_loc": "🔍 स्थान शोधा (उदा., हैदराबाद)",
        "weather_head": "🌦️ रिअल-टाइम स्थानिक हवामान", "vision_head": "📸 रोगजनक निदान स्कॅनर",
        "soil_head": "🧪 मृदा रासायनिक प्रोफाइलिंग", "market_head": "📈 डीप लर्निंग किंमत अंदाज",
        "scheme_head": "🏛️ सरकारी योजना शोधक", "chat_head": "🤖 ॲग्रिबॉट (व्हिजन चॅट)",
        "listen": "🔊 सल्ला ऐका:"
    },
    "ta": {
        "hero_title": "🌿 அக்ரோஇன்சைட் — எண்டர்பிரைஸ் சிஸ்டம்",
        "hero_sub": "ஆழமான கற்றல் மற்றும் நிகழ்நேர தரவு மூலம் நிலையான விவசாயத்தை மேம்படுத்துதல்.",
        "nav_weather": "🌦️ நேரலை வானிலை டாஷ்போர்டு", "nav_vision": "🍂 பயிர் நோய் பார்வை ஆய்வகம்",
        "nav_soil": "🧪 மண் சுகாதார பகுப்பாய்வி", "nav_market": "📈 சந்தை விலை முன்னறிவிப்பாளர்",
        "nav_scheme": "🏛️ அரசு திட்டங்கள்", "nav_chat": "🤖 அக்ரிபாட் (பார்வை அரட்டை)",
        "btn_weather": "நிலைகளைப் பெறுங்கள்", "btn_vision": "⚡ இப்போது இலையை பகுப்பாய்வு செய்",
        "btn_soil": "🧪 உர மருந்து பரிந்துரை உருவாக்கவும்", "btn_market": "📊 சந்தை முன்னறிவிப்பை இயக்கவும்",
        "upload": "படத்தை பதிவேற்றவும்", "search_loc": "🔍 இருப்பிடத்தைத் தேடுங்கள் (உதாரணம், ஹைதராபாத்)",
        "weather_head": "🌦️ நிகழ்நேர உள்ளூர் வானிலை", "vision_head": "📸 நோய்க்கிருமி கண்டறியும் ஸ்கேனர்",
        "soil_head": "🧪 மண் வேதியியல் விவரக்குறிப்பு", "market_head": "📈 ஆழமான கற்றல் விலை முன்னறிவிப்பாளர்",
        "scheme_head": "🏛️ அரசு திட்டங்கள்", "chat_head": "🤖 அக்ரிபாட் (பார்வை அரட்டை)",
        "listen": "🔊 ஆலோசனையைக் கேளுங்கள்:"
    }
}

# --- 4. HELPER FUNCTIONS ---
def play_audio(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp.getvalue(), format='audio/mp3')
    except Exception:
        pass

def hint(emoji, text):
    st.markdown(
        f"<div class='hint'><span class='emoji'>{emoji}</span>"
        f"<span class='label'>{text}</span></div>",
        unsafe_allow_html=True,
    )

def section_header(title, subtitle):
    st.markdown(
        f"<h2 style='margin-bottom:2px'>{title}</h2>"
        f"<p style='color:var(--text-muted); margin-top:0; margin-bottom:18px'>{subtitle}</p>",
        unsafe_allow_html=True,
    )

def generate_report(disease, conf, rec):
    return f"""# AgroInsight Diagnostic Report
**Date:** {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
**Identified Condition:** {disease} (Confidence: {conf})
### Summary
{rec.get('summary')}
### Biological Control
{rec.get('biological')}
### Chemical Treatment
{rec.get('chemical')}
### Prevention
{rec.get('prevention')}
"""

def handle_api_response(response):
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:
        st.warning("⏳ AI speed limit reached! Google Gemini only allows a few free requests per minute. Please wait 30 seconds and try again.")
        return None
    else:
        st.error(f"Backend Server Error: {response.text}")
        return None

# --- 5. SIDEBAR NAVIGATION & SETTINGS ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2913/2913520.png", width=64)
st.sidebar.markdown("### 🌿 AgroInsight")
st.sidebar.caption("Smart farming, simplified.")
st.sidebar.markdown("---")

# Language Setup
language_map = {"English": "en", "Hindi (हिंदी)": "hi", "Telugu (తెలుగు)": "te", "Marathi (मराठी)": "mr", "Tamil (தமிழ்)": "ta"}
st.sidebar.markdown("#### 🌐 Accessibility / पहुंच")
selected_lang_label = st.sidebar.selectbox("Language / भाषा", list(language_map.keys()))
lang_code = language_map[selected_lang_label]
api_lang_string = selected_lang_label.split(" ")[0]

t = UI_TEXT[lang_code]

st.sidebar.markdown("---")
st.sidebar.markdown("#### 🧭 Ecosystem Modules")
module_selection = st.sidebar.radio(
    "Ecosystem Modules",
    [t["nav_weather"], t["nav_vision"], t["nav_soil"], t["nav_market"], t["nav_scheme"], t["nav_chat"]],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.caption(f"🟢 System online · {datetime.datetime.now():%d %b %Y, %H:%M}")

# --- 6. HERO HEADER ---
st.markdown(f"""
    <div class="hero">
        <h1>{t["hero_title"]}</h1>
        <p>{t["hero_sub"]}</p>
        <div class="badge-row">
            <span class="chip">🛰️ Real-time data</span>
            <span class="chip">🧠 Deep learning</span>
            <span class="chip">🌍 5 languages</span>
            <span class="chip">🔊 Voice advice</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# MODULE 1: WEATHER DASHBOARD
# ==========================================
if module_selection == t["nav_weather"]:
    section_header(t["weather_head"], "Verified hyperlocal conditions for smarter field decisions.")
    col_w1, col_w2 = st.columns([3, 1])
    with col_w1:
        city = st.text_input(t["search_loc"], "Hyderabad")
    with col_w2:
        st.write(""); st.write("")
        fetch_weather = st.button(t["btn_weather"], use_container_width=True)

    if fetch_weather and city:
        with st.spinner("Connecting to weather satellites..."):
            try:
                geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
                geo_data = requests.get(geo_url).json()
                if "results" in geo_data:
                    lat = geo_data["results"][0]["latitude"]
                    lon = geo_data["results"][0]["longitude"]
                    region = geo_data["results"][0].get("admin1", "Region")
                    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relativehumidity_2m,precipitation_probability"
                    weather_data = requests.get(weather_url).json()
                    current = weather_data["current_weather"]
                    humidity = weather_data["hourly"]["relativehumidity_2m"][0]
                    rain_prob = weather_data["hourly"]["precipitation_probability"][0]

                    st.success(f"📍 Location Verified: {city.capitalize()}, {region}  (Lat {lat:.2f}, Lon {lon:.2f})")
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("🌡️ Temp", f"{current['temperature']} °C")
                    m2.metric("💨 Wind", f"{current['windspeed']} km/h")
                    m3.metric("💧 Humidity", f"{humidity} %")
                    m4.metric("🌧️ Rain Prob", f"{rain_prob} %")

                    # Smart, context-aware advice
                    if rain_prob > 60:
                        st.warning("☔ High rain probability — consider delaying spraying or fertilizer application.")
                    elif humidity > 80:
                        st.info("💧 High humidity — watch for fungal disease pressure on susceptible crops.")
                    else:
                        st.success("✅ Conditions look favourable for routine field operations.")
                else:
                    st.error("Location not found.")
            except Exception:
                st.error("Failed to fetch weather data.")
    else:
        hint("🛰️", "Search a location to see live weather metrics.")

# ==========================================
# MODULE 2: CROP DISEASE DETECTION & REPORT EXPORT
# ==========================================
elif module_selection == t["nav_vision"]:
    section_header(t["vision_head"], "Upload a leaf photo to detect disease and get a treatment plan.")
    col_up, col_res = st.columns([1, 2])

    with col_up:
        uploaded_file = st.file_uploader(t["upload"], type=["jpg", "jpeg", "png"])
        run_vision = st.button(t["btn_vision"], use_container_width=True) if uploaded_file else False
        if uploaded_file:
            st.image(Image.open(uploaded_file), caption="Sample", use_container_width=True, clamp=True)

    with col_res:
        if uploaded_file and run_vision:
            with st.spinner("Analyzing..."):
                try:
                    img_byte_arr = io.BytesIO()
                    Image.open(uploaded_file).convert("RGB").save(img_byte_arr, format="JPEG")
                    response = requests.post(
                        f"http://127.0.0.1:8000/predict-disease/?language={api_lang_string}",
                        files={"file": (uploaded_file.name, img_byte_arr.getvalue(), "image/jpeg")}
                    )

                    result = handle_api_response(response)
                    if result:
                        rec = result.get("recommendations", {})
                        r1, r2 = st.columns(2)
                        r1.metric("🦠 Condition", result.get("disease"))
                        r2.metric("🤖 Confidence", result.get("confidence"))

                        st.markdown(f"> **Context:** {rec.get('summary')}")
                        st.markdown(f"**{t['listen']}**")
                        play_audio(f"{rec.get('summary')} {rec.get('biological')} {rec.get('chemical')} {rec.get('prevention')}", lang_code)

                        t1, t2, t3 = st.tabs(["🍃 Biological", "🧪 Chemical", "🛡️ Prevention"])
                        t1.info(rec.get("biological")); t2.warning(rec.get("chemical")); t3.success(rec.get("prevention"))

                        st.markdown("---")
                        st.download_button("📥 Download Official Report", generate_report(result.get("disease"), result.get("confidence"), rec), "AgroInsight_Report.md", "text/markdown")
                except Exception:
                    st.error("Backend Server Error.")
        elif not uploaded_file:
            hint("🍃", "Upload an image to see results.")
        else:
            hint("⚡", "Press the Analyze button.")

# ==========================================
# MODULE 3: SOIL HEALTH ANALYZER
# ==========================================
elif module_selection == t["nav_soil"]:
    section_header(t["soil_head"], "Enter your soil readings for a tailored fertilizer prescription.")
    with st.form("soil_form"):
        target_crop = st.selectbox("Target Cultivation Crop", ["Tomato", "Potato", "Rice", "Wheat", "Maize", "Cotton", "Apple"])
        c1, c2, c3, c4 = st.columns(4)
        n_val = c1.number_input("Nitrogen (N)", value=150.0)
        p_val = c2.number_input("Phosphorus (P)", value=45.0)
        k_val = c3.number_input("Potassium (K)", value=130.0)
        ph_val = c4.number_input("Soil pH", value=6.5)
        submit_soil = st.form_submit_button(t["btn_soil"], use_container_width=True)

    if submit_soil:
        with st.spinner("Processing chemical profile..."):
            try:
                response = requests.post("http://127.0.0.1:8000/analyze-soil/", json={"nitrogen": n_val, "phosphorus": p_val, "potassium": k_val, "ph": ph_val, "target_crop": target_crop})
                result = handle_api_response(response)
                if result:
                    status = result.get('status')
                    pill, icon = ("pill-ok", "✅") if status == "Optimal" else ("pill-warn", "⚠️")
                    st.markdown(f"<span class='pill {pill}'>{icon} Status: {status}</span>", unsafe_allow_html=True)
                    st.markdown(f"**Diagnostic Summary:** {result.get('analysis')}")
                    st.info(f"**Prescription:** {result.get('prescription')}")
            except Exception:
                st.error("Backend unreachable.")
    else:
        hint("🧫", "Fill in the soil values.")

# ==========================================
# MODULE 4: MARKET FORECASTER
# ==========================================
elif module_selection == t["nav_market"]:
    section_header(t["market_head"], "LSTM-driven price trends to time your sales for peak profit.")
    col_m1, col_m2 = st.columns([1, 2])
    with col_m1:
        with st.form("market_form"):
            commodity = st.selectbox("Target Commodity", ["Tomato", "Potato", "Rice", "Wheat", "Maize"])
            region = st.selectbox("Mandi / Region", ["Azadpur Mandi (Delhi)", "Vashi Market (Mumbai)", "Kalyanpur (UP)", "Guntur (AP)"])
            submit_market = st.form_submit_button(t["btn_market"], use_container_width=True)
    with col_m2:
        if submit_market:
            with st.spinner("Processing sequence arrays via recurrent gates..."):
                try:
                    response = requests.post("http://127.0.0.1:8000/predict-price/", json={"commodity": commodity, "market_region": region})
                    result = handle_api_response(response)
                    if result:
                        m1, m2 = st.columns(2)
                        m1.metric("Current Spot Price", result.get("current_price"))
                        m2.metric("Optimal Sell Window", result.get("optimal_sell_window"), delta="Target Peak")
                        st.line_chart(result.get("historical_trend", []) + result.get("forecast_trend", []))
                        st.success(f"💡 Market Strategy: {result.get('market_strategy')}")
                except Exception:
                    st.error("Backend unreachable.")
        else:
            hint("📊", "Run the forecast to see predicted trends.")

# ==========================================
# MODULE 5: GOVT SCHEMES MATCHER
# ==========================================
elif module_selection == t["nav_scheme"]:
    section_header(t["scheme_head"], "Find subsidies and schemes matched to your farm profile.")
    with st.form("scheme_form"):
        col1, col2 = st.columns(2)
        with col1:
            state = st.selectbox("Your State", ["Andhra Pradesh", "Telangana", "Maharashtra", "Uttar Pradesh", "Karnataka"])
            crop = st.text_input("Primary Crop", "Paddy")
        with col2:
            size = st.number_input("Farm Size (Acres)", value=2.5, min_value=0.1)
        submit_scheme = st.form_submit_button("🔍 Find My Schemes", use_container_width=True)

    if submit_scheme:
        with st.spinner("Searching Govt Databases..."):
            try:
                response = requests.post("http://127.0.0.1:8000/match-scheme/", json={"state": state, "crop": crop, "farm_size": size, "language": api_lang_string})
                result = handle_api_response(response)
                if result:
                    st.success("Matches Found!")
                    st.markdown(result["schemes"])
            except Exception:
                st.error("Database offline.")
    else:
        hint("🏛️", "Enter your details to discover eligible schemes.")

# ==========================================
# MODULE 6: MULTI-MODAL VISION CHAT
# ==========================================
elif module_selection == t["nav_chat"]:
    section_header(t["chat_head"], "Ask about pests, weeds, or layouts — attach a photo for vision answers.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    with st.expander("📷 Attach Image to Message"):
        chat_img = st.file_uploader("Upload Image (Optional)", type=["jpg", "png", "jpeg"])
        if chat_img:
            st.image(chat_img, width=150)

    if not st.session_state.chat_history:
        hint("🤖", "Start the conversation below — ask anything about your farm.")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask about the image, or general farming advice..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Processing Vision & Text..."):
                try:
                    data = {"message": prompt, "language": api_lang_string}
                    if chat_img:
                        img_bytes = io.BytesIO()
                        Image.open(chat_img).convert("RGB").save(img_bytes, format="JPEG")
                        files = {"file": ("image.jpg", img_bytes.getvalue(), "image/jpeg")}
                        response = requests.post("http://127.0.0.1:8000/vision-chat/", data=data, files=files)
                    else:
                        response = requests.post("http://127.0.0.1:8000/vision-chat/", data=data)

                    result = handle_api_response(response)
                    if result:
                        reply = result["reply"]
                        st.markdown(reply)
                        st.session_state.chat_history.append({"role": "assistant", "content": reply})
                except Exception:
                    st.error("AgriBot connection failed.")
