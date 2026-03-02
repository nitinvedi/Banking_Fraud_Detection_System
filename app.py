import streamlit as st
import pandas as pd
import joblib
import requests
from geopy.distance import geodesic
from datetime import datetime

st.set_page_config(
    page_title="FraudShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

/* ── Result cards ── */
.fraud-card {
    border-left: 5px solid #ef4444;
    background: #fff5f5;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
}
.safe-card {
    border-left: 5px solid #10b981;
    background: #f0fdf4;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
}

/* ── Confidence bar ── */
.conf-bar-wrap {
    background: #e5e7eb;
    border-radius: 100px;
    height: 8px;
    margin: 0.5rem 0 0.3rem;
    overflow: hidden;
}
.conf-bar-fill-fraud {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #ef4444, #f97316);
}
.conf-bar-fill-safe {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #10b981, #06b6d4);
}

/* ── Badges ── */
.badge-fraud {
    display: inline-block;
    background: #fee2e2; color: #b91c1c !important;
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 1px; text-transform: uppercase;
    padding: 3px 10px; border-radius: 20px; margin-bottom: 0.5rem;
}
.badge-safe {
    display: inline-block;
    background: #d1fae5; color: #065f46 !important;
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 1px; text-transform: uppercase;
    padding: 3px 10px; border-radius: 20px; margin-bottom: 0.5rem;
}

/* ── Team cards ── */
.team-wrap {
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 1.5rem 1rem;
    text-align: center;
    transition: box-shadow 0.2s;
}
.team-wrap:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.1); }
.avatar-circle {
    width: 56px; height: 56px; border-radius: 50%;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem; font-weight: 700; color: #fff !important;
    margin: 0 auto 0.7rem;
}
.team-name { font-weight: 600; font-size: 0.95rem; }
.team-id   { font-size: 0.78rem; color: #6b7280 !important; }

/* ── Sidebar history ── */
.hist-card {
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 0.65rem 0.9rem;
    margin-bottom: 0.5rem;
}
.hist-fraud { border-left: 3px solid #ef4444 !important; }
.hist-safe  { border-left: 3px solid #10b981 !important; }

/* ── Misc ── */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.65rem 1.5rem !important;
}

/* ── FORM CARD ── */
.form-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 1.8rem 2rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-bottom: 1.2rem;
}
.form-section-title {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #6366f1 !important;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.form-divider {
    border: none;
    border-top: 1px solid #f3f4f6;
    margin: 1.4rem 0;
}
.required-star { color: #ef4444 !important; font-size: 0.75rem; vertical-align: super; }
.field-hint { font-size: 0.78rem; color: #9ca3af !important; margin-top: -0.4rem; margin-bottom: 0.5rem; }

/* ── Input override ── */
.stTextInput input, .stNumberInput input {
    border-radius: 8px !important;
    border: 1.5px solid #e5e7eb !important;
    font-size: 0.92rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
}
[data-testid="stSelectbox"] > div > div {
    border-radius: 8px !important;
    border: 1.5px solid #e5e7eb !important;
}

/* ── Submit button ── */
[data-testid="stForm"] .stButton > button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    width: 100% !important;
    margin-top: 0.5rem !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.35) !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
[data-testid="stForm"] .stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.45) !important;
}
[data-testid="stForm"] .stButton > button:active {
    transform: translateY(0) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ──
if 'transaction_history' not in st.session_state:
    st.session_state.transaction_history = []

# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div style="padding: 0.5rem 0 1rem;">
        <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.3rem;">
            <span style="font-size:1.4rem;">🛡️</span>
            <span style="font-size:1.1rem; font-weight:700; color:#1e293b;">FraudShield</span>
        </div>
        <div style="width:100%; height:1px; background:#e5e7eb; margin:0.8rem 0;"></div>
        <p style="font-size:0.75rem; color:#6b7280; letter-spacing:0.8px; text-transform:uppercase; margin:0;">Transaction History</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.transaction_history:
        for t in st.session_state.transaction_history:
            fraud_cls = "hist-fraud" if t["is_fraud"] else "hist-safe"
            icon = "⚠️" if t["is_fraud"] else "✅"
            label = "FRAUD" if t["is_fraud"] else "SAFE"
            color = "#fca5a5" if t["is_fraud"] else "#6ee7b7"
            st.markdown(f"""
            <div class="hist-card {fraud_cls}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:600; font-size:0.88rem;">{icon} {t['merchant']}</span>
                    <span style="color:{color} !important; font-size:0.72rem; font-weight:700; letter-spacing:0.8px;">{label}</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-top:0.3rem;">
                    <span style="font-size:0.78rem; color:#94a3b8 !important;">{t['amount']} · {t['category']}</span>
                    <span style="font-size:0.72rem; color:#94a3b8 !important;">{t['confidence']}</span>
                </div>
                <div style="font-size:0.7rem; color:#475569 !important; margin-top:0.25rem;">{t['timestamp']}</div>
            </div>
            """, unsafe_allow_html=True)
        if st.button("🗑️ Clear History"):
            st.session_state.transaction_history = []
            st.rerun()
    else:
        st.markdown("""
        <div style="text-align:center; padding:2rem 1rem; color:#475569 !important;">
            <div style="font-size:2rem; margin-bottom:0.5rem;">📋</div>
            <p style="font-size:0.85rem; color:#475569 !important;">No history yet.<br>Analyze a transaction to start.</p>
        </div>
        """, unsafe_allow_html=True)

# ── Load models ──
@st.cache_resource
def load_models():
    model = joblib.load("fraud_detection_model.jb")
    encoder = joblib.load("label_encoder.jb")
    return model, encoder

model, encoder = load_models()

def haversine(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).km

def get_location_name(lat, lon):
    try:
        response = requests.get(
            f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1",
            headers={"User-Agent": "FraudDetectionApp/1.0"}
        )
        if response.status_code == 200:
            data = response.json()
            address = data.get('address', {})
            return {
                'city': address.get('city', address.get('town', '')),
                'country': address.get('country', ''),
                'full_address': data.get('display_name', '')
            }
    except Exception as e:
        st.warning(f"Could not fetch location details: {str(e)}")
    return None

def detect_location_by_ip():
    try:
        response = requests.get("http://ip-api.com/json/")
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return data.get("lat"), data.get("lon")
    except Exception as e:
        st.error(f"Error detecting location: {str(e)}")
    return None, None

# ── HEADER ──
st.title("🛡️ Fraud Detection System")
st.caption("Detect fraudulent transactions in real-time using a LightGBM machine learning model.")
st.divider()

# ── Auto-detect location ──
st.markdown("""
<div style="
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #f0f4ff;
    border: 1px solid #c7d2fe;
    border-radius: 12px;
    padding: 0.9rem 1.3rem;
    margin-bottom: 1.2rem;
    gap: 1rem;
">
    <div style="display:flex; align-items:center; gap:0.8rem;">
        <span style="font-size:1.5rem;">📍</span>
        <div>
            <div style="font-weight:600; font-size:0.92rem; color:#3730a3;">Auto-detect my location</div>
            <div style="font-size:0.78rem; color:#6366f1; margin-top:1px;">Uses your IP address to fill in latitude &amp; longitude automatically</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

col_detect, col_status = st.columns([1, 3])
with col_detect:
    detect_clicked = st.button("📡 Detect Location", use_container_width=True)
with col_status:
    if detect_clicked:
        with st.spinner("Detecting location via IP…"):
            lat_ip, lon_ip = detect_location_by_ip()
        if lat_ip is not None and lon_ip is not None:
            st.session_state['user_lat'] = lat_ip
            st.session_state['user_lon'] = lon_ip
            loc_details = get_location_name(lat_ip, lon_ip)
            if loc_details:
                city    = loc_details.get('city', 'Unknown')
                country = loc_details.get('country', 'Unknown')
                st.success(f"📍 **{city}, {country}** — coordinates saved to location fields below.")
            else:
                st.info("✅ Location detected. Coordinates saved.")
        else:
            st.error("❌ Could not detect location via IP. Fill in coordinates manually.")


# ── FORM ──
st.markdown('<div class="form-card">', unsafe_allow_html=True)

with st.form("transaction_form"):

    # ── Row 1: Merchant info ──
    st.markdown('<div class="form-section-title">🏪 Merchant &amp; Transaction</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        merchant = st.text_input("Merchant Name ", placeholder="Amazon, Walmart, Starbucks…")
        st.markdown('<p class="field-hint">Required ✱</p>', unsafe_allow_html=True)
    with col2:
        category = st.text_input("Category ", placeholder="Electronics, Grocery, Travel…")
        st.markdown('<p class="field-hint">Required ✱</p>', unsafe_allow_html=True)
    with col3:
        amt = st.number_input("Amount (USD)", min_value=0.0, format="%.2f", value=50.0)

    st.markdown('<hr class="form-divider">', unsafe_allow_html=True)

    # ── Row 2: Card & Identity ──
    st.markdown('<div class="form-section-title">� Payment &amp; Identity</div>', unsafe_allow_html=True)
    col4, col5 = st.columns([2, 1])
    with col4:
        cc_num = st.text_input("Credit Card Number ", placeholder="1234 5678 9012 3456", help="Hashed locally — never stored or transmitted")
        st.markdown('<p class="field-hint">Required ✱ &nbsp;·&nbsp; 🔒 Hashed client-side, never stored</p>', unsafe_allow_html=True)
    with col5:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    st.markdown('<hr class="form-divider">', unsafe_allow_html=True)

    # ── Row 3: Time ──
    st.markdown('<div class="form-section-title">� Transaction Time</div>', unsafe_allow_html=True)
    tc1, tc2, tc3 = st.columns(3)
    with tc1:
        hour  = st.slider("Hour of Day", 0, 23, 12, help="0 = midnight, 23 = 11 PM")
    with tc2:
        day   = st.slider("Day of Month", 1, 31, 15)
    with tc3:
        month = st.slider("Month", 1, 12, 6)

    st.markdown('<hr class="form-divider">', unsafe_allow_html=True)

    # ── Row 4: Location ──
    st.markdown('<div class="form-section-title">� Location Coordinates</div>', unsafe_allow_html=True)
    lc1, lc2, lc3, lc4 = st.columns(4)
    with lc1:
        lat = st.number_input("Your Latitude",  format="%.6f", value=st.session_state.get('user_lat', 40.7128), key="lat_input")
    with lc2:
        lon = st.number_input("Your Longitude", format="%.6f", value=st.session_state.get('user_lon', -74.0060), key="lon_input")
    with lc3:
        merch_lat = st.number_input("Merchant Latitude",  format="%.6f", value=40.7306)
    with lc4:
        merch_lon = st.number_input("Merchant Longitude", format="%.6f", value=-73.9352)

    st.markdown('<br>', unsafe_allow_html=True)
    submitted = st.form_submit_button("🔍  Analyze Transaction", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

distance = haversine(lat, lon, merch_lat, merch_lon)

if submitted:
    if merchant and category and cc_num:
        with st.spinner("Running fraud analysis…"):
            input_data = pd.DataFrame(
                [[merchant, category, amt, distance, hour, day, month, gender, cc_num]],
                columns=['merchant','category','amt','distance','hour','day','month','gender','cc_num']
            )
            for col in ['merchant', 'category', 'gender']:
                try:
                    input_data[col] = encoder[col].transform(input_data[col])
                except ValueError:
                    input_data[col] = -1

            input_data['cc_num'] = input_data['cc_num'].apply(lambda x: hash(x) % (10 ** 2))
            prediction  = model.predict(input_data)[0]
            confidence  = model.predict_proba(input_data)[0][1] * 100

            # Save to history
            st.session_state.transaction_history.insert(0, {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "merchant": merchant, "amount": f"${amt:.2f}",
                "category": category, "is_fraud": bool(prediction),
                "confidence": f"{confidence:.1f}%", "distance": f"{distance:.2f} km"
            })
            if len(st.session_state.transaction_history) > 10:
                st.session_state.transaction_history = st.session_state.transaction_history[:10]

            # ── Result display ──
            st.markdown('<div class="section-header"><div class="icon-wrap">📊</div><h3>Analysis Result</h3></div>', unsafe_allow_html=True)

            if prediction == 1:
                bar_pct = f"{confidence:.1f}"
                st.markdown(f"""
                <div class="fraud-card">
                    <span class="badge-fraud">⚠️ Fraud Detected</span>
                    <h2 style="color:#fca5a5 !important; margin:0.2rem 0 0.5rem; font-size:1.5rem;">Suspicious Transaction</h2>
                    <p style="color:#fbd5d5 !important; margin:0 0 1rem;">Our model identified patterns consistent with fraudulent activity.</p>
                    <div style="margin-bottom:0.2rem; display:flex; justify-content:space-between;">
                        <span style="font-size:0.82rem; color:#94a3b8 !important;">Fraud Probability</span>
                        <span style="font-size:0.82rem; color:#fca5a5 !important; font-weight:700;">{bar_pct}%</span>
                    </div>
                    <div class="conf-bar-wrap"><div class="conf-bar-fill-fraud" style="width:{bar_pct}%;"></div></div>
                    <p style="color:#f87171 !important; font-size:0.85rem; margin-top:0.8rem;">
                        🔔 <strong>Recommendation:</strong> Contact your bank immediately and freeze the card.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                safe_conf = f"{100 - confidence:.1f}"
                st.markdown(f"""
                <div class="safe-card">
                    <span class="badge-safe">✅ Legitimate</span>
                    <h2 style="color:#6ee7b7 !important; margin:0.2rem 0 0.5rem; font-size:1.5rem;">Transaction Looks Safe</h2>
                    <p style="color:#d1fae5 !important; margin:0 0 1rem;">No suspicious patterns detected in this transaction.</p>
                    <div style="margin-bottom:0.2rem; display:flex; justify-content:space-between;">
                        <span style="font-size:0.82rem; color:#94a3b8 !important;">Safety Score</span>
                        <span style="font-size:0.82rem; color:#6ee7b7 !important; font-weight:700;">{safe_conf}%</span>
                    </div>
                    <div class="conf-bar-wrap"><div class="conf-bar-fill-safe" style="width:{safe_conf}%;"></div></div>
                    <p style="color:#34d399 !important; font-size:0.85rem; margin-top:0.8rem;">
                        ✔️ <strong>All clear.</strong> Transaction appears within normal parameters.
                    </p>
                </div>
                """, unsafe_allow_html=True)

            # ── Location details ──
            st.subheader("📍 Location Analysis")
            mc1, mc2 = st.columns(2)
            with mc1:
                st.metric("Distance Between Locations", f"{distance:.2f} km")
                st.write(f"**Your coords:** {lat:.6f}, {lon:.6f}")
                st.write(f"**Merchant coords:** {merch_lat:.6f}, {merch_lon:.6f}")
            with mc2:
                df_loc = pd.DataFrame({'lat': [lat, merch_lat], 'lon': [lon, merch_lon]})
                st.map(df_loc, zoom=10)

    else:
        st.error("⚠️ Please fill in Merchant Name, Category, and Credit Card Number.")

# ── TEAM SECTION ──
st.divider()
st.subheader("👥 Our Team")

team = [
    {"name": "Nitin Chaturvedi", "id": "12306849", "initials": "NC"},
    {"name": "Aditi Verma",      "id": "12307076", "initials": "AV"},
    {"name": "Mansi Singh",      "id": "12306194", "initials": "MS"},
]
t1, t2, t3 = st.columns(3)
for col, member in zip([t1, t2, t3], team):
    with col:
        st.markdown(f"""
        <div class="team-wrap">
            <div class="avatar-circle">{member['initials']}</div>
            <div class="team-name">{member['name']}</div>
            <div class="team-id">{member['id']}</div>
        </div>
        """, unsafe_allow_html=True)

# ── FOOTER ──
st.markdown("""
<div style="text-align:center; padding: 3rem 0 1rem; margin-top:1rem;">
    <p style="color:#1e293b !important; font-size:0.82rem; letter-spacing:0.5px;">
        FraudShield AI · v2.0 · Powered by LightGBM
    </p>
</div>
""", unsafe_allow_html=True)