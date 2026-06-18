import streamlit as st
import datetime
from src.predict import predict_department

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="CivicRoute - Citizen Grievance Portal",
    page_icon="🏛️",
    layout="wide"
)

# =========================================================
# DEPARTMENT INFO
# predict_department() returns a plain string label like "water_leak".
# This dictionary turns that into a nice department name + icon + priority.
# =========================================================
DEPARTMENT_INFO = {
    "drainage":        {"name": "Drainage & Sewage Department",        "icon": "🚰", "priority": "HIGH"},
    "garbage":         {"name": "Solid Waste & Sanitation Department", "icon": "🗑️", "priority": "MEDIUM"},
    "graffiti":        {"name": "Public Works - Graffiti Removal",     "icon": "🎨", "priority": "LOW"},
    "illegal_dumping": {"name": "Environmental Enforcement Department","icon": "⚠️", "priority": "HIGH"},
    "illegal_parking": {"name": "Traffic & Parking Authority",         "icon": "🚗", "priority": "MEDIUM"},
    "noise":           {"name": "Noise & Nuisance Control Unit",       "icon": "🔊", "priority": "MEDIUM"},
    "other":           {"name": "General Civic Services",             "icon": "📋", "priority": "LOW"},
    "pothole":         {"name": "Roads & Infrastructure Department",  "icon": "🛣️", "priority": "HIGH"},
    "streetlight":     {"name": "Electrical & Street Lighting Division","icon": "💡", "priority": "MEDIUM"},
    "water_leak":      {"name": "Water Supply & Plumbing Department", "icon": "💧", "priority": "CRITICAL"},
    "water_leakage":   {"name": "Water Supply & Plumbing Department", "icon": "💧", "priority": "CRITICAL"},
}

PRIORITY_COLOR = {
    "CRITICAL": "#DC2626",
    "HIGH":     "#EA580C",
    "MEDIUM":   "#CA8A04",
    "LOW":      "#16A34A",
}


def get_department_info(label):
    """Safely look up department info, with a fallback for unknown labels."""
    label = label.strip().lower()
    if label in DEPARTMENT_INFO:
        return DEPARTMENT_INFO[label]
    return {"name": label.replace("_", " ").title(), "icon": "📋", "priority": "MEDIUM"}


# =========================================================
# STYLING
# =========================================================
st.markdown("""
<style>
.main-title {
    text-align: center;
    color: #0B2447;
    font-size: 38px;
    font-weight: 700;
    margin-bottom: 0px;
}
.sub-title {
    text-align: center;
    color: #475569;
    font-size: 16px;
    margin-bottom: 25px;
}
.metric-card {
    background: white;
    padding: 18px;
    border-radius: 10px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
    text-align: center;
}
.result-box {
    padding: 22px;
    border-radius: 12px;
    background: #F8FAFC;
    border-left: 8px solid #0B2447;
}
.result-dept {
    font-size: 24px;
    font-weight: 700;
    color: #0B2447;
    margin-bottom: 10px;
}
.result-tag {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    color: white;
    margin-right: 8px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown('<div class="main-title">🏛️ AI Citizen Grievance Routing System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Deep Learning Based Complaint Classification for Smart Municipal Governance</div>', unsafe_allow_html=True)

# =========================================================
# DASHBOARD CARDS
# =========================================================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h4>Model</h4>
        <p>Bi-LSTM</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h4>Tokenizer</h4>
        <p>Keras NLP</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h4>Deployment</h4>
        <p>Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =========================================================
# COMPLAINT INPUT
# =========================================================
st.subheader("📝 Submit Citizen Complaint")

complaint = st.text_area(
    "Enter Complaint Description",
    height=180,
    placeholder="Example: Street light not working near bus stand for the past 2 weeks..."
)

# =========================================================
# PREDICTION
# =========================================================
if st.button("🔍 Route Complaint", use_container_width=True):

    if complaint.strip() == "":
        st.warning("Please enter a complaint description.")
    else:
        with st.spinner("Analyzing complaint using LSTM model..."):
            raw_label = predict_department(complaint)   # plain string, e.g. "water_leak"
            info = get_department_info(raw_label)

        color = PRIORITY_COLOR.get(info["priority"], "#0B2447")

        st.markdown(f"""
        <div class="result-box">
            <div class="result-dept">{info['icon']} {info['name']}</div>
            <span class="result-tag" style="background:{color};">Priority: {info['priority']}</span>
            <span class="result-tag" style="background:#0B2447;">Category: {raw_label.replace('_',' ').title()}</span>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.caption("AI-Powered Municipal Complaint Routing System | Built using TensorFlow, Keras, LSTM and Streamlit")
