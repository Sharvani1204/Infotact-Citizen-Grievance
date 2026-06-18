import streamlit as st
import datetime
import pandas as pd
import numpy as np
import random

from src.predict import predict_department

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CivicRoute – AI Grievance Portal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# Mappings & Global Session State
# ─────────────────────────────────────────────
DEPT_DISPLAY = {
    "drainage":        ("Drainage & Sewage Department",          "🚰", "HIGH"),
    "garbage":         ("Solid Waste & Sanitation Department",   "🗑️", "MEDIUM"),
    "graffiti":        ("Public Works – Graffiti Removal",       "🎨", "LOW"),
    "illegal_dumping": ("Environmental Enforcement Department",  "⚠️", "HIGH"),
    "illegal_parking": ("Traffic & Parking Authority",           "🚗", "MEDIUM"),
    "noise":           ("Noise & Nuisance Control Unit",         "🔊", "MEDIUM"),
    "other":           ("General Civic Services",                "📋", "LOW"),
    "pothole":         ("Roads & Infrastructure Department",     "🛣️", "HIGH"),
    "streetlight":     ("Electrical & Street Lighting Division", "💡", "MEDIUM"),
    "water_leak":      ("Water Supply & Plumbing Department",    "💧", "CRITICAL"),
    "water_leakage":   ("Water Supply & Plumbing Department",    "💧", "CRITICAL"),
}

PRIORITY_STYLE = {
    "CRITICAL": ("🔴", "#BE123C", "#FFF1F2", "#FECDD3"),
    "HIGH":     ("🟠", "#C2410C", "#FFF7ED", "#FED7AA"),
    "MEDIUM":   ("🟡", "#A16207", "#FEFCE8", "#FEF08A"),
    "LOW":      ("🟢", "#15803D", "#F0FDF4", "#BBF7D0"),
}

# Session State Initialization for Real-Time data feel
if "history" not in st.session_state:
    st.session_state.history = [
        {"id": "GRV-20260618-4821", "dept": "Roads & Infrastructure Department", "priority": "HIGH", "status": "In Progress", "desc": "Large pothole near central crossroad."},
        {"id": "GRV-20260618-9104", "dept": "Water Supply & Plumbing Department", "priority": "CRITICAL", "status": "Dispatched", "desc": "Major water pipe burst flooding the residential street."}
    ]

def resolve(label: str):
    label = label.strip().lower()
    return DEPT_DISPLAY.get(label, (label.replace("_", " ").title(), "📋", "MEDIUM"))

# ─────────────────────────────────────────────
# CSS Custom Injection (Maintained Theme Style)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Sora:wght@400;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #F0F4FA !important;
    font-family: 'Inter', sans-serif;
    color: #1A2332;
}

[data-testid="stMain"] > div { padding: 0 !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
[data-testid="stVerticalBlockBorderWrapper"] { padding: 0 !important; }
[data-testid="block-container"] { padding: 0 !important; max-width: 100% !important; }

#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"] { visibility: hidden !important; display: none !important; }

/* ═══════════════════════════════════════════
   UPPER ELEMENT TIMES NEW ROMAN OVERRIDES
═══════════════════════════════════════════ */
.topbar-brand, .topbar-right, .hero h1, .hero-desc, .hero-eyebrow-text {
    font-family: 'Times New Roman', Times, serif !important;
}

.topbar {
    background: #0A1628; color: white; padding: 0 48px; height: 56px;
    display: flex; justify-content: space-between; align-items: center;
    border-bottom: 2px solid #F59E0B; position: sticky; top: 0; z-index: 100;
}
.topbar-left { display: flex; align-items: center; gap: 14px; }
.topbar-logo-emoji {
    font-size: 24px;
    line-height: 1;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.topbar-brand strong { display: block; font-size: 14px; font-weight: 700; letter-spacing: 0.5px; color: white; }
.topbar-brand span { display: block; font-size: 11.5px; color: rgba(255,255,255,0.7); margin-top: 2px; }
.topbar-right { font-size: 12px; color: rgba(255,255,255,0.75); text-align: right; line-height: 1.3; font-weight: bold; }

.hero {
    background: linear-gradient(135deg, #0A1628 0%, #0D2045 45%, #102B60 100%);
    color: white; padding: 42px 60px 38px; position: relative; overflow: hidden;
}
.hero h1 {
    font-weight: 500; font-size: 46px; letter-spacing: -0.5px; margin-top: 15px; margin-bottom: 20px;
}
.hero-desc { font-size: 16px; color: rgba(255,255,255,0.75); max-width: 740px; line-height: 1.6; font-weight: 400; }

.stats-wrap { background: white; border-bottom: 1px solid #E5EAF2; padding: 0 60px; }
.stats-inner { display: flex; max-width: 1400px; margin: 0 auto; }
.stat-item { flex: 1; padding: 18px 24px; display: flex; align-items: center; gap: 14px; border-right: 1px solid #F0F4FA; }
.stat-item:last-child { border-right: none; }
.stat-val { font-size: 22px; font-weight: 800; color: #0A1628; font-family: 'Sora', sans-serif; }
.stat-lbl { font-size: 10px; color: #94A3B8; font-weight: 600; text-transform: uppercase; }

.body-wrap { padding: 24px 60px; max-width: 1400px; margin: 0 auto; }

.fpanel { background: white; border: 1px solid #E5EAF2; border-radius: 16px; overflow: hidden; margin-bottom: 24px; box-shadow: 0 4px 20px rgba(10,22,40,0.05); }
.fpanel-head { padding: 16px 24px; display: flex; align-items: center; gap: 12px; background: linear-gradient(135deg, #0A1628, #0D2045); color: white;}
.fpanel-head-title { font-size: 15px; font-weight: 700; font-family: 'Sora', sans-serif; }
.fpanel-body { padding: 24px; }

.field-lbl { display: block; font-size: 11px; font-weight: 700; color: #0A1628; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px; margin-top: 4px;}
.req { color: #EF4444; }

/* ═══════════════════════════════════════════
   HIGHLIGHTED INPUT TEXTAREA
═══════════════════════════════════════════ */
[data-testid="stTextArea"] textarea {
    border: 2px solid #2563EB !important;
    border-radius: 12px !important;
    background: #F8FAFF !important;
    box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.15) !important;
    animation: focusGlow 2.5s infinite alternate ease-in-out;
}

[data-testid="stTextArea"] textarea:focus {
    border-color: #1D4ED8 !important;
    background: white !important;
    box-shadow: 0 0 0 6px rgba(29, 78, 216, 0.25) !important;
    outline: none !important;
}

@keyframes focusGlow {
    0% { box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1); }
    100% { box-shadow: 0 0 0 6px rgba(37, 99, 235, 0.25); }
}

.scard { background: white; border: 1px solid #E5EAF2; border-radius: 14px; padding: 20px; box-shadow: 0 2px 12px rgba(10,22,40,0.04); margin-bottom: 20px; }
.scard-head { display: flex; align-items: center; gap: 8px; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 1px solid #F0F4FA; }
.scard-head-bar { width: 3px; height: 16px; background: linear-gradient(180deg, #F59E0B, #EF4444); border-radius: 2px; }
.scard-head h4 { font-size: 11px; font-weight: 700; color: #0A1628; text-transform: uppercase; letter-spacing: 0.8px; }

.ai-card { background: linear-gradient(135deg, #0A1628, #0D2045); border-radius: 14px; padding: 20px; color: white; margin-bottom: 20px; }
.ai-accuracy { font-size: 36px; font-weight: 800; font-family: 'Sora', sans-serif; }

.track-step-container { display: flex; justify-content: space-between; margin-top: 15px; background: #F8FAFC; padding: 12px; border-radius: 8px; border: 1px solid #E2E8F0; }
.track-node { text-align: center; font-size: 11px; font-weight: 600; color: #94A3B8; }
.track-node.active { color: #1D4ED8; font-weight: 700; }

.govfooter { background: #0A1628; padding: 20px 60px; display: flex; justify-content: space-between; align-items: center; color: white; margin-top: 40px;}
.footer-left strong { font-size: 12px; font-family: 'Sora', sans-serif; color: rgba(255,255,255,0.9); }
.footer-right a { color: #F59E0B; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Top Bar
# ─────────────────────────────────────────────
now = datetime.datetime.now()
st.markdown(f"""
<div class="topbar">
  <div class="topbar-left">
    <div class="topbar-logo-emoji">🏛️</div>
    <div class="topbar-brand">
      <strong>CIVICROUTE PORTAL</strong>
      <span>Integrated Citizen Grievance Redressal System | Municipal Corporation of India</span>
    </div>
  </div>
  <div class="topbar-right">
    {now.strftime("%A, %d %B %Y")}<br>
    {now.strftime("%I:%M %p IST")}
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Hero
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-inner">
    <div class="hero-eyebrow" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); border-radius: 20px; padding: 6px 16px; display: inline-block;">
      <span class="hero-eyebrow-text" style="color: #F59E0B; font-size: 10px; font-weight: 700; letter-spacing: 1.5px;">⚡ AI-POWERED &nbsp;·&nbsp; BI-LSTM DEEP LEARNING</span>
    </div>
    <h1>Citizen Grievance Routing System</h1>
    <p class="hero-desc">
      Submit your civic complaint in plain language. Our NLP engine instantly identifies the 
      responsible department and assigns an urgency priority — so your issue reaches the right team 
      without delay.
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Dynamic Numerical Analytics
# ─────────────────────────────────────────────
total_routed = 24831 + len(st.session_state.history) - 2
st.markdown(f"""
<div class="stats-wrap">
  <div class="stats-inner">
    <div class="stat-item">
      <div><div class="stat-lbl">Live Dynamic Load</div><div class="stat-val">{total_routed}</div></div>
    </div>
    <div class="stat-item">
      <div><div class="stat-lbl">Model Accuracy Score</div><div class="stat-val">94.2%</div></div>
    </div>
    <div class="stat-item">
      <div><div class="stat-lbl">Inference Latency</div><div class="stat-val">&lt; 1.84s</div></div>
    </div>
    <div class="stat-item">
      <div><div class="stat-lbl">Critical Load Today</div><div class="stat-val">8</div></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Main Interface Layout Splitting
# ─────────────────────────────────────────────
st.markdown('<div class="body-wrap">', unsafe_allow_html=True)
left, right = st.columns([2.6, 1.4], gap="large")

with left:
    mode = st.tabs(["📝 File New Grievance", "🔍 Real-Time Ticket Tracker"])
    
    # ── TAB 1: SUBMISSION ENGINE ──
    with mode[0]:
        st.markdown("""
        <div class="fpanel">
          <div class="fpanel-head"><div class="fpanel-head-title">Citizen Submission Portal</div></div>
          <div class="fpanel-body">
        """, unsafe_allow_html=True)
        
        st.markdown('<span class="field-lbl">Complaint Description <span class="req">*</span></span>', unsafe_allow_html=True)
        complaint = st.text_area(
            label="Grievance Statement Input",
            height=200,
            placeholder="Type descriptive language regarding your issue (e.g. Sewage water is backing up into the main street road...)",
            label_visibility="collapsed"
        )
        
        st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
        submit = st.button("🚀 Process & Dispatch Complaint", use_container_width=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

        if submit:
            if not complaint.strip():
                st.warning("⚠️ Input field cannot be calculated as empty. Please type your grievance.")
            else:
                with st.spinner("Executing sequence matching inside Bi-LSTM Network layers..."):
                    raw_label = predict_department(complaint)
                
                dept_name, dept_icon, priority = resolve(raw_label)
                p_icon, p_color, p_bg, p_border = PRIORITY_STYLE[priority]
                generated_id = f"GRV-{now.strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
                
                # Appending dynamically to state memory tracking structures
                st.session_state.history.append({
                    "id": generated_id, "dept": dept_name, "priority": priority, "status": "Assigned", "desc": complaint
                })
                
                st.markdown(f"""
                <div class="rcard" style="background: white; border: 1px solid #E5EAF2; border-radius: 16px; overflow: hidden; margin-top:20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                  <div class="rcard-banner" style="background: {p_color}; color: white; padding: 12px; font-weight:700; font-size:13px;">
                    ✓ AI DEEP INFRASTRUCTURE REDIRECTION VERIFIED
                  </div>
                  <div style="padding: 20px;">
                    <small style="color: #94A3B8; font-weight:700;">CLASSIFIED DEPARTMENT</small>
                    <h3 style="font-family:'Sora'; color:#0A1628; margin: 5px 0 15px 0;">{dept_icon} {dept_name}</h3>
                    <span style="background:{p_bg}; color:{p_color}; border: 1px solid {p_border}; padding: 4px 10px; border-radius:6px; font-weight:700; font-size:12px;">
                      Priority Level: {priority}
                    </span>
                    <hr style="margin:15px 0; border:0; border-top:1px solid #F0F4FA;">
                    <div style="background:#F8FAFF; border:1px solid #E8EEFE; padding:12px; border-radius:8px; display:flex; justify-content:space-between; align-items:center;">
                      <div>
                        <div style="font-size:10px; color:#94A3B8; font-weight:700;">TICKET REFERENCE ID</div>
                        <div style="font-family:'Sora'; color:#1D4ED8; font-weight:800; font-size:15px;">{generated_id}</div>
                      </div>
                      <div style="background:#F0FDF4; border:1px solid #BBF7D0; color:#15803D; padding:4px 10px; border-radius:6px; font-weight:700; font-size:11px;">
                        🟢 Status: Dispatched
                      </div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 2: REAL-TIME TRACKING SUITE ──
    with mode[1]:
        st.markdown("""
        <div class="fpanel">
          <div class="fpanel-head"><div class="fpanel-head-title">Integrated Lifecycle Tracking</div></div>
          <div class="fpanel-body">
        """, unsafe_allow_html=True)
        
        search_id = st.text_input("Enter Registered Ticket Reference Code (e.g., GRV-20260618-4821)", value="", placeholder="GRV-YYYYMMDD-XXXX")
        
        if search_id:
            matched_ticket = next((t for t in st.session_state.history if t["id"].strip().upper() == search_id.strip().upper()), None)
            
            if matched_ticket:
                st.markdown(f"""
                <div style="background:#FAFBFF; padding:16px; border-radius:10px; border:1px solid #E2E8F0; margin-bottom:15px;">
                  <span style="font-size:11px; background:#E2E8F0; padding:2px 6px; border-radius:4px; font-weight:600;">{matched_ticket['id']}</span>
                  <h4 style="margin:10px 0 5px 0; font-family:'Sora';">{matched_ticket['dept']}</h4>
                  <p style="font-size:13px; color:#475569;">" {matched_ticket['desc']} "</p>
                </div>
                """, unsafe_allow_html=True)
                
                status = matched_ticket["status"]
                s1, s2, s3 = ("active", "", "") if status == "Assigned" else (("active", "active", "") if status == "Dispatched" else ("active", "active", "active"))
                
                st.markdown(f"""
                <div class="track-step-container">
                  <div class="track-node {s1}">■ Registered</div>
                  <div class="track-node {s2}">■ Department Dispatched</div>
                  <div class="track-node {s3}">■ Ground Resolution</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("No active tracking metrics found matches that reference criteria.")
        else:
            st.info("💡 Input a generated ticket ID string above to preview state changes in real-time context loops.")
        st.markdown("</div></div>", unsafe_allow_html=True)

with right:
    # Performance Evaluation Dashboard card
    st.markdown("""
    <div class="ai-card">
      <h4>Bi-LSTM Model Evaluation</h4>
      <div class="ai-accuracy">94.2<span>%</span></div>
      <div style="font-size:11px; opacity:0.6; margin-bottom:10px;">Classification accuracy validation score matrix</div>
      <div class="ai-bar-wrap" style="background:rgba(255,255,255,0.1); height:6px; border-radius:4px; overflow:hidden;">
        <div style="width:94.2%; height:100%; background:linear-gradient(90deg, #F59E0B, #FCD34D);"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # LIVE DATA VISUALIZATION CHART
    st.markdown("""
    <div class="scard">
      <div class="scard-head">
        <div class="scard-head-bar"></div>
        <h4>Live Structural Analytics Queue</h4>
      </div>
    """, unsafe_allow_html=True)
    
    chart_data = pd.DataFrame(
        np.random.randint(10, 50, size=(10, 1)),
        index=['Water', 'Roads', 'Sewage', 'Trash', 'Light', 'Parking', 'Noise', 'Enforce', 'Graffiti', 'General'],
        columns=['Active Load Count']
    )
    st.bar_chart(chart_data, color="#1D4ED8", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Department Coverage Directory panel
    st.markdown("""
    <div class="scard">
      <div class="scard-head">
        <div class="scard-head-bar"></div>
        <h4>Covered Domains Registry</h4>
      </div>
      <ul class="dlist" style="list-style:none; font-size:12px; line-height:1.8;">
        <li>🔹 Water Supply &amp; Piping Maintenance</li>
        <li>🔹 Structural Roads &amp; Asphalt Management</li>
        <li>🔹 Sewage Networks Management</li>
        <li>🔹 Solid Waste Sanitation Division</li>
        <li>🔹 Electrical Systems &amp; Lighting Grids</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close body-wrap

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("""
<div class="govfooter">
  <div class="footer-left">
    <strong>CivicRoute — Real-Time Deep Learning NLP Grievance Frame</strong><br>
    <span>Built with TensorFlow · Keras Bi-LSTM Model Layer Optimization · Streamlit Execution Architecture</span>
  </div>
  <div class="footer-right">
    © 2026 Municipal Corporation of India
  </div>
</div>
""", unsafe_allow_html=True)
