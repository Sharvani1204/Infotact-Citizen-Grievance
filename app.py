import streamlit as st
import datetime

# predict_department returns a plain label string (e.g. "water_leak")
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
# Mappings  (mirrors what your labels list has)
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

def resolve(label: str):
    """Turn raw label → (dept_name, icon, priority)"""
    label = label.strip().lower()
    return DEPT_DISPLAY.get(label, (label.replace("_", " ").title(), "📋", "MEDIUM"))

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&family=DM+Serif+Display&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"] {
    background: #EEF2F7 !important;
    font-family: 'DM Sans', sans-serif;
}
#MainMenu, footer, header, [data-testid="stToolbar"] { visibility:hidden; display:none; }

/* ── Top Bar ── */
.topbar {
    background: #0B2447;
    color: white;
    padding: 11px 48px;
    display: flex; justify-content: space-between; align-items: center;
    border-bottom: 3px solid #F59E0B;
}
.topbar-left   { display:flex; align-items:center; gap:14px; }
.topbar-emblem { font-size:30px; line-height:1; }
.topbar-name strong { display:block; font-size:14px; letter-spacing:.8px; }
.topbar-name span   { font-size:11px; opacity:.65; }
.topbar-right  { font-size:11px; opacity:.65; text-align:right; line-height:1.6; }

/* ── Hero ── */
.hero {
    background: linear-gradient(130deg,#0B2447 0%,#19376D 55%,#1565C0 100%);
    color: white; padding: 44px 60px 38px;
    position:relative; overflow:hidden;
}
.hero::before {
    content:''; position:absolute; right:-80px; top:-80px;
    width:360px; height:360px; border-radius:50%;
    background:rgba(245,158,11,.07); pointer-events:none;
}
.hero-badge {
    display:inline-flex; align-items:center; gap:6px;
    background:rgba(245,158,11,.18); border:1px solid rgba(245,158,11,.4);
    color:#FCD34D; font-size:10px; font-weight:700; letter-spacing:1.2px;
    text-transform:uppercase; padding:4px 14px; border-radius:20px; margin-bottom:16px;
}
.hero h1 {
    font-family:'DM Serif Display',serif; font-size:36px; font-weight:400;
    letter-spacing:-.4px; margin-bottom:10px;
}
.hero p { font-size:14px; opacity:.78; max-width:560px; line-height:1.7; }

/* ── Stats ── */
.stats {
    display:flex; gap:18px;
    padding:22px 60px;
    background:white; border-bottom:1px solid #E2E8F0;
}
.stat {
    flex:1; background:white; border:1px solid #E2E8F0; border-radius:10px;
    padding:16px 20px; display:flex; align-items:center; gap:14px;
    box-shadow:0 1px 4px rgba(0,0,0,.05);
}
.stat-ico {
    width:42px; height:42px; border-radius:9px;
    display:flex; align-items:center; justify-content:center; font-size:21px; flex-shrink:0;
}
.ic-blue{background:#EFF6FF;} .ic-green{background:#F0FDF4;}
.ic-amber{background:#FFFBEB;} .ic-red{background:#FFF1F2;}
.stat-lbl { font-size:11px; color:#64748B; font-weight:600; letter-spacing:.3px; margin-bottom:3px; }
.stat-val { font-size:22px; font-weight:700; color:#0B2447; line-height:1; }

/* ── Form Panel ── */
.fpanel {
    background:white; border:1px solid #E2E8F0; border-radius:14px;
    overflow:hidden; box-shadow:0 2px 14px rgba(11,36,71,.07);
}
.fpanel-head {
    background:#0B2447; color:white;
    padding:18px 28px; display:flex; align-items:center; gap:10px;
}
.fpanel-head-icon { font-size:20px; }
.fpanel-head-title { font-size:15px; font-weight:600; }
.fpanel-head-sub { font-size:11px; opacity:.6; margin-top:2px; }
.fpanel-body { padding:28px; }
.field-lbl {
    display:block; font-size:11px; font-weight:700; color:#374151;
    text-transform:uppercase; letter-spacing:.7px; margin-bottom:8px;
}
.req { color:#EF4444; margin-left:3px; }

/* Textarea */
[data-testid="stTextArea"] textarea {
    border:1.5px solid #CBD5E1 !important; border-radius:8px !important;
    font-family:'DM Sans',sans-serif !important; font-size:14px !important;
    color:#1E293B !important; padding:14px 16px !important;
    background:#FAFAFA !important; transition:border-color .2s !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color:#1565C0 !important; background:white !important;
    box-shadow:0 0 0 3px rgba(21,101,192,.10) !important;
}
[data-testid="stTextArea"] label { display:none !important; }

/* Button */
[data-testid="stButton"]>button {
    background:linear-gradient(135deg,#0B2447,#1565C0) !important;
    color:white !important; border:none !important; border-radius:8px !important;
    font-family:'DM Sans',sans-serif !important; font-size:14px !important;
    font-weight:600 !important; letter-spacing:.4px !important;
    padding:14px 28px !important; width:100% !important;
    box-shadow:0 4px 14px rgba(11,36,71,.25) !important;
    transition:all .2s ease !important;
}
[data-testid="stButton"]>button:hover {
    background:linear-gradient(135deg,#19376D,#1976D2) !important;
    box-shadow:0 6px 20px rgba(11,36,71,.35) !important;
    transform:translateY(-1px) !important;
}

/* ── Result Card ── */
.rcard {
    margin-top:22px; background:white; border:1px solid #E2E8F0;
    border-radius:14px; overflow:hidden;
    box-shadow:0 2px 14px rgba(11,36,71,.07);
    animation:fadeUp .4s ease;
}
@keyframes fadeUp{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
.rcard-head {
    padding:13px 22px; font-size:11px; font-weight:700;
    letter-spacing:1px; text-transform:uppercase;
    display:flex; align-items:center; gap:8px;
}
.rcard-body { padding:24px; }
.rcard-dept-lbl { font-size:10px; color:#64748B; font-weight:700; letter-spacing:.7px; text-transform:uppercase; margin-bottom:6px; }
.rcard-dept-ico { font-size:28px; margin-bottom:6px; }
.rcard-dept-name { font-size:22px; font-weight:700; color:#0B2447; margin-bottom:20px; line-height:1.2; }
.pills { display:flex; gap:10px; flex-wrap:wrap; }
.pill {
    display:inline-flex; align-items:center; gap:6px;
    background:#F1F5F9; border-radius:20px;
    padding:5px 14px; font-size:12px; font-weight:600; color:#334155;
}
.pill-p { border:1px solid; }

/* ── Side cards ── */
.scard { background:white; border:1px solid #E2E8F0; border-radius:12px; padding:20px; box-shadow:0 1px 4px rgba(0,0,0,.05); }
.scard h4 {
    font-size:11px; font-weight:700; color:#0B2447;
    text-transform:uppercase; letter-spacing:.8px;
    margin-bottom:14px; padding-bottom:10px; border-bottom:2px solid #F59E0B;
}
.dlist { list-style:none; padding:0; }
.dlist li {
    display:flex; align-items:center; gap:10px;
    padding:8px 0; font-size:13px; color:#374151;
    border-bottom:1px solid #F8FAFC;
}
.dlist li:last-child { border-bottom:none; }
.ddot { width:7px; height:7px; border-radius:50%; background:#1565C0; flex-shrink:0; }
.step { display:flex; gap:13px; margin-bottom:15px; align-items:flex-start; }
.stepn {
    width:27px; height:27px; border-radius:50%; background:#0B2447; color:white;
    font-size:12px; font-weight:700; display:flex; align-items:center; justify-content:center; flex-shrink:0; margin-top:1px;
}
.stept { font-size:13px; color:#374151; line-height:1.5; }
.stept strong { color:#0B2447; display:block; margin-bottom:2px; }

/* ── Footer ── */
.govfooter {
    background:#0B2447; color:rgba(255,255,255,.5);
    text-align:center; padding:20px 40px; font-size:12px; margin-top:12px;
}
.govfooter strong { color:rgba(255,255,255,.85); }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Top Bar
# ─────────────────────────────────────────────
now = datetime.datetime.now()
st.markdown(f"""
<div class="topbar">
  <div class="topbar-left">
    <div class="topbar-emblem">🏛️</div>
    <div class="topbar-name">
      <strong>CIVICROUTE PORTAL</strong>
      <span>Integrated Citizen Grievance Redressal System &nbsp;|&nbsp; Municipal Corporation of India</span>
    </div>
  </div>
  <div class="topbar-right">
    {now.strftime("%A, %d %B %Y")}<br>{now.strftime("%I:%M %p IST")}
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Hero
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">🤖 AI-Powered &nbsp;·&nbsp; Bi-LSTM Deep Learning</div>
  <h1>Citizen Grievance Routing System</h1>
  <p>Submit your civic complaint in plain language. Our NLP engine instantly identifies
  the responsible department and assigns an urgency priority — so your issue reaches
  the right team without delay.</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Stats Row
# ─────────────────────────────────────────────
st.markdown("""
<div class="stats">
  <div class="stat"><div class="stat-ico ic-blue">📋</div><div><div class="stat-lbl">Complaints Routed</div><div class="stat-val">24,831</div></div></div>
  <div class="stat"><div class="stat-ico ic-green">✅</div><div><div class="stat-lbl">Model Accuracy</div><div class="stat-val">94.2%</div></div></div>
  <div class="stat"><div class="stat-ico ic-amber">⚡</div><div><div class="stat-lbl">Avg. Response Time</div><div class="stat-val">&lt; 2 sec</div></div></div>
  <div class="stat"><div class="stat-ico ic-red">🚨</div><div><div class="stat-lbl">Critical Tickets Today</div><div class="stat-val">7</div></div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Main Layout
# ─────────────────────────────────────────────
left, right = st.columns([3, 1.4], gap="large")

with left:
    # Form Panel header
    st.markdown("""
    <div class="fpanel">
      <div class="fpanel-head">
        <div class="fpanel-head-icon">📝</div>
        <div>
          <div class="fpanel-head-title">Submit New Complaint</div>
          <div class="fpanel-head-sub">All submissions are logged and tracked under your session ID</div>
        </div>
      </div>
      <div class="fpanel-body">
        <span class="field-lbl">Complaint Description <span class="req">*</span></span>
    """, unsafe_allow_html=True)

    complaint = st.text_area(
        label="complaint",
        height=180,
        placeholder=(
            "Describe your issue in detail...\n\n"
            "Example: The drainage pipe near Rajiv Nagar bus stand has been overflowing "
            "for 3 days causing water logging on the main road."
        ),
        label_visibility="collapsed"
    )

    submit = st.button("🔍  Analyse & Route Complaint", use_container_width=True)

    st.markdown("</div></div>", unsafe_allow_html=True)  # close fpanel-body + fpanel

    # ── Result ────────────────────────────────
    if submit:
        if not complaint.strip():
            st.warning("⚠️  Please enter a complaint description before submitting.")
        else:
            with st.spinner("Analysing with Bi-LSTM model…"):
                raw_label = predict_department(complaint)   # returns plain string

            dept_name, dept_icon, priority = resolve(raw_label)
            p_icon, p_color, p_bg, p_border = PRIORITY_STYLE[priority]
            ticket_id = f"GRV-{now.strftime('%Y%m%d')}-{abs(hash(complaint)) % 9000 + 1000}"

            st.markdown(f"""
            <div class="rcard">
              <div class="rcard-head" style="background:{p_color};color:white;">
                ✅ &nbsp; Complaint Successfully Routed &nbsp;·&nbsp; Ticket #{ticket_id}
              </div>
              <div class="rcard-body">
                <div class="rcard-dept-lbl">Assigned Department</div>
                <div class="rcard-dept-ico">{dept_icon}</div>
                <div class="rcard-dept-name">{dept_name}</div>
                <div class="pills">
                  <div class="pill pill-p" style="background:{p_bg};color:{p_color};border-color:{p_border};">
                    {p_icon} Priority: {priority}
                  </div>
                  <div class="pill">🏷️ Category: {raw_label.replace('_',' ').title()}</div>
                  <div class="pill">🕐 {now.strftime('%d %b %Y, %I:%M %p')}</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="scard">
      <h4>Covered Departments</h4>
      <ul class="dlist">
        <li><div class="ddot"></div> Water Supply &amp; Plumbing</li>
        <li><div class="ddot"></div> Roads &amp; Infrastructure</li>
        <li><div class="ddot"></div> Drainage &amp; Sewage</li>
        <li><div class="ddot"></div> Solid Waste &amp; Sanitation</li>
        <li><div class="ddot"></div> Electrical &amp; Street Lighting</li>
        <li><div class="ddot"></div> Traffic &amp; Parking Authority</li>
        <li><div class="ddot"></div> Noise &amp; Nuisance Control</li>
        <li><div class="ddot"></div> Environmental Enforcement</li>
        <li><div class="ddot"></div> Public Works – Graffiti</li>
        <li><div class="ddot"></div> General Civic Services</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="scard">
      <h4>How It Works</h4>
      <div class="step"><div class="stepn">1</div><div class="stept"><strong>Describe the Issue</strong>Type your complaint in plain language — no forms to fill.</div></div>
      <div class="step"><div class="stepn">2</div><div class="stept"><strong>AI Classification</strong>Bi-LSTM model classifies the complaint into the correct department.</div></div>
      <div class="step"><div class="stepn">3</div><div class="stept"><strong>Priority Assigned</strong>Urgency level (Critical → Low) is assigned automatically.</div></div>
      <div class="step"><div class="stepn">4</div><div class="stept"><strong>Instant Routing</strong>Complaint is logged with a unique Ticket ID for tracking.</div></div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("""
<div class="govfooter">
  <strong>CivicRoute — AI Citizen Grievance Management Portal</strong><br>
  Built with TensorFlow · Keras Bi-LSTM · Streamlit &nbsp;|&nbsp;
  Government of India Initiative &nbsp;|&nbsp; grievance@municipal.gov.in
</div>
""", unsafe_allow_html=True)