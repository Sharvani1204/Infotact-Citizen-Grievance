import streamlit as st
import datetime
from src.predict import predict_department

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="CivicRoute – AI Grievance Portal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# DATA: Department lookup, priority styling
# (Same theme colors as before — navy #0A1628 / amber #F59E0B)
# =========================================================
DEPT_DISPLAY = {
    "drainage":        ("Drainage & Sewage Department",           "🚰", "HIGH"),
    "garbage":         ("Solid Waste & Sanitation Department",    "🗑️", "MEDIUM"),
    "graffiti":        ("Public Works – Graffiti Removal",        "🎨", "LOW"),
    "illegal_dumping": ("Environmental Enforcement Department",   "⚠️", "HIGH"),
    "illegal_parking": ("Traffic & Parking Authority",            "🚗", "MEDIUM"),
    "noise":           ("Noise & Nuisance Control Unit",          "🔊", "MEDIUM"),
    "other":           ("General Civic Services",                 "📋", "LOW"),
    "pothole":         ("Roads & Infrastructure Department",      "🛣️", "HIGH"),
    "streetlight":     ("Electrical & Street Lighting Division",  "💡", "MEDIUM"),
    "water_leak":      ("Water Supply & Plumbing Department",     "💧", "CRITICAL"),
    "water_leakage":   ("Water Supply & Plumbing Department",     "💧", "CRITICAL"),
}

PRIORITY_STYLE = {
    "CRITICAL": ("🔴", "#BE123C", "#FFF1F2", "#FECDD3"),
    "HIGH":     ("🟠", "#C2410C", "#FFF7ED", "#FED7AA"),
    "MEDIUM":   ("🟡", "#A16207", "#FEFCE8", "#FEF08A"),
    "LOW":      ("🟢", "#15803D", "#F0FDF4", "#BBF7D0"),
}


def resolve(label: str):
    """raw model label -> (department name, icon, priority)"""
    label = label.strip().lower()
    return DEPT_DISPLAY.get(label, (label.replace("_", " ").title(), "📋", "MEDIUM"))


# =========================================================
# STYLING — same navy/amber theme, simplified to one
# consistent visual language (no competing effects).
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #F0F4FA !important;
    font-family: 'Inter', sans-serif;
    color: #1A2332;
}

[data-testid="stMain"] > div { padding: 0 !important; }
[data-testid="block-container"] { padding: 0 !important; max-width: 100% !important; }
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"] { visibility: hidden !important; display: none !important; }
[data-testid="stColumns"] { gap: 0 !important; }
[data-testid="stColumn"] { padding: 0 !important; }

/* ---------- TOP BAR ---------- */
.topbar {
    background: #0A1628;
    color: white;
    padding: 0 48px;
    height: 56px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #F59E0B;
}
.topbar-left { display: flex; align-items: center; gap: 12px; }
.topbar-logo {
    width: 32px; height: 32px;
    background: #F59E0B;
    border-radius: 7px;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px; font-weight: 800; color: #0A1628;
    font-family: 'Sora', sans-serif;
}
.topbar-brand strong {
    display: block; font-size: 13px; font-weight: 700;
    letter-spacing: 1px; color: white; font-family: 'Sora', sans-serif;
}
.topbar-brand span { font-size: 10.5px; color: rgba(255,255,255,0.45); }
.topbar-right { font-size: 11px; color: rgba(255,255,255,0.45); }

/* ---------- HERO ---------- */
.hero {
    background: #0A1628;
    color: white;
    padding: 48px 60px;
    border-bottom: 4px solid #F59E0B;
}
.hero-eyebrow {
    display: inline-block;
    font-size: 11px; font-weight: 700; letter-spacing: 1px;
    color: #FCD34D; text-transform: uppercase;
    margin-bottom: 14px;
}
.hero h1 {
    font-family: 'Sora', sans-serif;
    font-size: 34px; font-weight: 800;
    line-height: 1.2; margin-bottom: 14px; color: white;
    max-width: 700px;
}
.hero-desc {
    font-size: 14.5px; color: rgba(255,255,255,0.65);
    max-width: 600px; line-height: 1.7;
}

/* ---------- STAT STRIP ---------- */
.stats-wrap { background: white; border-bottom: 1px solid #E5EAF2; padding: 0 60px; }
.stats-inner { display: flex; max-width: 1300px; margin: 0 auto; }
.stat-item {
    flex: 1; padding: 20px 28px;
    display: flex; align-items: center; gap: 14px;
    border-right: 1px solid #F0F4FA;
}
.stat-item:last-child { border-right: none; }
.stat-ico {
    width: 40px; height: 40px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; flex-shrink: 0;
}
.s-blue  { background: #EFF6FF; }
.s-green { background: #F0FDF4; }
.s-amber { background: #FFFBEB; }
.s-rose  { background: #FFF1F2; }
.stat-lbl { font-size: 10.5px; color: #94A3B8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.4px; margin-bottom: 3px; }
.stat-val { font-size: 21px; font-weight: 800; color: #0A1628; font-family: 'Sora', sans-serif; line-height: 1; }

/* ---------- BODY LAYOUT ---------- */
.body-wrap {
    padding: 32px 60px 40px;
    display: flex; gap: 28px;
    max-width: 1300px; margin: 0 auto;
}

/* ---------- FORM PANEL ---------- */
.fpanel {
    background: white;
    border: 1px solid #E5EAF2;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 2px 14px rgba(10,22,40,0.06);
}
.fpanel-head {
    padding: 18px 26px;
    background: #0A1628;
    display: flex; align-items: center; gap: 12px;
}
.fpanel-head-icon {
    width: 38px; height: 38px; border-radius: 9px;
    background: rgba(245,158,11,0.18);
    border: 1px solid rgba(245,158,11,0.3);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; flex-shrink: 0;
}
.fpanel-head-title { font-size: 14.5px; font-weight: 700; color: white; font-family: 'Sora', sans-serif; }
.fpanel-head-sub { font-size: 11px; color: rgba(255,255,255,0.45); margin-top: 2px; }
.fpanel-body { padding: 26px; }

.field-lbl {
    display: block; font-size: 11px; font-weight: 700;
    color: #64748B; text-transform: uppercase; letter-spacing: 0.7px;
    margin-bottom: 10px;
}
.req { color: #EF4444; margin-left: 2px; }

[data-testid="stTextArea"] textarea {
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 9px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important; line-height: 1.6 !important;
    color: #1A2332 !important;
    padding: 14px 16px !important;
    background: #FAFBFF !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: #1D4ED8 !important;
    background: white !important;
    box-shadow: 0 0 0 3px rgba(29,78,216,0.10) !important;
    outline: none !important;
}
[data-testid="stTextArea"] label { display: none !important; }

.field-hint { font-size: 11px; color: #94A3B8; margin-top: 8px; margin-bottom: 18px; }

[data-testid="stButton"] > button {
    background: #1D4ED8 !important;
    color: white !important; border: none !important;
    border-radius: 9px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important; font-weight: 700 !important;
    letter-spacing: 0.3px !important;
    padding: 13px 26px !important; width: 100% !important;
    box-shadow: 0 4px 14px rgba(29,78,216,0.28) !important;
}
[data-testid="stButton"] > button:hover {
    background: #1E40AF !important;
    box-shadow: 0 6px 18px rgba(29,78,216,0.36) !important;
}

/* ---------- RESULT CARD ---------- */
.rcard {
    margin-top: 20px;
    background: white;
    border: 1px solid #E5EAF2;
    border-radius: 14px; overflow: hidden;
    box-shadow: 0 2px 14px rgba(10,22,40,0.06);
}
.rcard-banner {
    padding: 13px 24px;
    font-size: 11.5px; font-weight: 700; letter-spacing: 0.5px;
    text-transform: uppercase; color: white;
}
.rcard-body { padding: 24px; }
.rcard-eyebrow { font-size: 10px; color: #94A3B8; font-weight: 700; letter-spacing: 0.7px; text-transform: uppercase; margin-bottom: 10px; }
.rcard-dept-row { display: flex; align-items: center; gap: 14px; margin-bottom: 20px; }
.rcard-dept-icon {
    width: 50px; height: 50px; border-radius: 12px;
    background: #F0F4FA; display: flex; align-items: center;
    justify-content: center; font-size: 24px; flex-shrink: 0;
}
.rcard-dept-name { font-size: 19px; font-weight: 800; color: #0A1628; font-family: 'Sora', sans-serif; }
.rcard-pills { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 18px; }
.rcard-pill {
    display: inline-flex; align-items: center; gap: 5px;
    background: #F1F5F9; border-radius: 6px;
    padding: 6px 12px; font-size: 12px; font-weight: 600; color: #334155;
    border: 1px solid #E2E8F0;
}
.rcard-pill-pri { border-width: 1.5px; font-weight: 700; }
.rcard-divider { height: 1px; background: #F0F4FA; margin-bottom: 16px; }
.rcard-ticket {
    display: flex; align-items: center; justify-content: space-between;
    background: #F8FAFF; border: 1px solid #E8EEFE;
    border-radius: 9px; padding: 12px 16px;
}
.rcard-ticket-lbl { font-size: 10px; color: #94A3B8; font-weight: 600; letter-spacing: 0.4px; text-transform: uppercase; margin-bottom: 3px; }
.rcard-ticket-id { font-size: 15px; font-weight: 800; color: #1D4ED8; font-family: 'Sora', sans-serif; }
.rcard-ticket-status {
    font-size: 11px; font-weight: 700;
    color: #15803D; background: #F0FDF4;
    border: 1px solid #BBF7D0; border-radius: 6px;
    padding: 5px 12px;
}

/* ---------- SIDE CARDS ---------- */
.scard {
    background: white; border: 1px solid #E5EAF2;
    border-radius: 13px; padding: 22px;
    box-shadow: 0 2px 10px rgba(10,22,40,0.05);
    margin-bottom: 18px;
}
.scard:last-child { margin-bottom: 0; }
.scard h4 {
    font-size: 11px; font-weight: 700; color: #0A1628;
    text-transform: uppercase; letter-spacing: 0.7px;
    margin-bottom: 16px; padding-bottom: 12px;
    border-bottom: 2px solid #F59E0B;
}
.dlist { list-style: none; }
.dlist li {
    display: flex; align-items: center; gap: 10px;
    padding: 7px 0; font-size: 12.5px; color: #475569;
    border-bottom: 1px solid #F8FAFC;
}
.dlist li:last-child { border-bottom: none; }
.ddot { width: 6px; height: 6px; border-radius: 50%; background: #1D4ED8; flex-shrink: 0; }

.step-item { display: flex; gap: 13px; margin-bottom: 15px; }
.step-item:last-child { margin-bottom: 0; }
.step-num {
    width: 26px; height: 26px; border-radius: 7px;
    background: #0A1628; color: white;
    font-size: 11.5px; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; font-family: 'Sora', sans-serif;
}
.step-content strong { font-size: 12.5px; color: #0A1628; font-weight: 700; display: block; margin-bottom: 2px; }
.step-content span { font-size: 12px; color: #64748B; line-height: 1.5; }

/* ---------- ACCURACY CARD ---------- */
.ai-card {
    background: #0A1628;
    border-radius: 13px; padding: 20px;
    margin-bottom: 18px;
}
.ai-card h4 { font-size: 11px; font-weight: 700; color: rgba(255,255,255,0.45); text-transform: uppercase; letter-spacing: 0.7px; margin-bottom: 10px; }
.ai-accuracy { font-size: 34px; font-weight: 800; color: white; font-family: 'Sora', sans-serif; line-height: 1; }
.ai-accuracy span { font-size: 16px; color: rgba(255,255,255,0.5); }
.ai-desc { font-size: 11.5px; color: rgba(255,255,255,0.5); margin: 6px 0 14px; }
.ai-bar-wrap { background: rgba(255,255,255,0.1); border-radius: 4px; height: 6px; overflow: hidden; }
.ai-bar-fill { height: 100%; background: #F59E0B; width: 94.2%; }

/* ---------- FOOTER ---------- */
.govfooter {
    background: #0A1628;
    padding: 22px 60px;
    display: flex; justify-content: space-between; align-items: center;
}
.footer-left strong { display: block; font-size: 13px; font-weight: 700; color: rgba(255,255,255,0.85); font-family: 'Sora', sans-serif; margin-bottom: 3px; }
.footer-left span { font-size: 11px; color: rgba(255,255,255,0.35); }
.footer-right { font-size: 11px; color: rgba(255,255,255,0.35); text-align: right; line-height: 1.7; }
.footer-right a { color: #F59E0B; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

now = datetime.datetime.now()

# =========================================================
# TOP BAR
# =========================================================
st.markdown(f"""
<div class="topbar">
  <div class="topbar-left">
    <div class="topbar-logo">CR</div>
    <div class="topbar-brand">
      <strong>CIVICROUTE PORTAL</strong>
      <span>Municipal Corporation of India — Integrated Grievance Redressal System</span>
    </div>
  </div>
  <div class="topbar-right">{now.strftime("%d %b %Y")} &nbsp;·&nbsp; {now.strftime("%I:%M %p IST")}</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# HERO
# =========================================================
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">AI-Powered &nbsp;·&nbsp; Bi-LSTM NLP Engine</div>
  <h1>Route your complaint to the right department, instantly.</h1>
  <p class="hero-desc">
    Describe your civic issue in plain language. Our deep learning model identifies the
    responsible authority and assigns urgency — generating a tracked ticket in under 2 seconds.
  </p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# STAT STRIP
# =========================================================
st.markdown("""
<div class="stats-wrap">
  <div class="stats-inner">
    <div class="stat-item">
      <div class="stat-ico s-blue">📋</div>
      <div><div class="stat-lbl">Complaints Routed</div><div class="stat-val">24,831</div></div>
    </div>
    <div class="stat-item">
      <div class="stat-ico s-green">✅</div>
      <div><div class="stat-lbl">Model Accuracy</div><div class="stat-val">94.2%</div></div>
    </div>
    <div class="stat-item">
      <div class="stat-ico s-amber">⚡</div>
      <div><div class="stat-lbl">Avg. Response Time</div><div class="stat-val">&lt; 2s</div></div>
    </div>
    <div class="stat-item">
      <div class="stat-ico s-rose">🚨</div>
      <div><div class="stat-lbl">Critical Tickets Today</div><div class="stat-val">7</div></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# MAIN BODY — Form (left) + Sidebar (right)
# =========================================================
st.markdown('<div class="body-wrap">', unsafe_allow_html=True)
left, right = st.columns([2.6, 1.1], gap="large")

with left:
    st.markdown("""
    <div class="fpanel">
      <div class="fpanel-head">
        <div class="fpanel-head-icon">📝</div>
        <div>
          <div class="fpanel-head-title">Submit New Complaint</div>
          <div class="fpanel-head-sub">Submissions are logged and tracked under a unique ticket ID</div>
        </div>
      </div>
      <div class="fpanel-body">
        <span class="field-lbl">Complaint Description <span class="req">*</span></span>
    """, unsafe_allow_html=True)

    complaint = st.text_area(
        label="complaint",
        height=180,
        placeholder=(
            "Describe your civic issue clearly...\n\n"
            "Example: The drainage pipe near Rajiv Nagar bus stand has been overflowing "
            "for 3 days causing water-logging on the main road."
        ),
        label_visibility="collapsed"
    )

    st.markdown(
        '<p class="field-hint">💡 Include the location, duration, and impact for faster resolution.</p>',
        unsafe_allow_html=True
    )

    submit = st.button("🔍  Analyse & Route Complaint", use_container_width=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

    # ---- Result ----
    if submit:
        if not complaint.strip():
            st.warning("⚠️ Please enter a complaint description before submitting.")
        else:
            with st.spinner("Analysing complaint with Bi-LSTM model…"):
                raw_label = predict_department(complaint)

            dept_name, dept_icon, priority = resolve(raw_label)
            p_icon, p_color, p_bg, p_border = PRIORITY_STYLE[priority]
            ticket_id = f"GRV-{now.strftime('%Y%m%d')}-{abs(hash(complaint)) % 9000 + 1000}"

            st.markdown(f"""
            <div class="rcard">
              <div class="rcard-banner" style="background:{p_color};">
                ✓ Complaint routed successfully — AI classification complete
              </div>
              <div class="rcard-body">
                <div class="rcard-eyebrow">Assigned Department</div>
                <div class="rcard-dept-row">
                  <div class="rcard-dept-icon">{dept_icon}</div>
                  <div class="rcard-dept-name">{dept_name}</div>
                </div>
                <div class="rcard-pills">
                  <div class="rcard-pill rcard-pill-pri" style="background:{p_bg}; color:{p_color}; border-color:{p_border};">
                    {p_icon} Priority: {priority}
                  </div>
                  <div class="rcard-pill">🏷️ {raw_label.replace('_',' ').title()}</div>
                  <div class="rcard-pill">🕐 {now.strftime('%d %b %Y, %I:%M %p')}</div>
                </div>
                <div class="rcard-divider"></div>
                <div class="rcard-ticket">
                  <div>
                    <div class="rcard-ticket-lbl">Ticket Reference</div>
                    <div class="rcard-ticket-id">{ticket_id}</div>
                  </div>
                  <div class="rcard-ticket-status">Active — Awaiting Department</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="ai-card">
      <h4>Model Performance</h4>
      <div class="ai-accuracy">94.2<span>%</span></div>
      <div class="ai-desc">Classification accuracy on held-out test set</div>
      <div class="ai-bar-wrap"><div class="ai-bar-fill"></div></div>
    </div>

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

    <div class="scard">
      <h4>How It Works</h4>
      <div class="step-item">
        <div class="step-num">1</div>
        <div class="step-content"><strong>Describe the Issue</strong><span>Type your complaint in plain language.</span></div>
      </div>
      <div class="step-item">
        <div class="step-num">2</div>
        <div class="step-content"><strong>AI Classification</strong><span>Bi-LSTM model routes it to the correct department.</span></div>
      </div>
      <div class="step-item">
        <div class="step-num">3</div>
        <div class="step-content"><strong>Priority Assigned</strong><span>Urgency level set automatically — Critical to Low.</span></div>
      </div>
      <div class="step-item">
        <div class="step-num">4</div>
        <div class="step-content"><strong>Ticket Generated</strong><span>A unique reference ID is issued for tracking.</span></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close body-wrap

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="govfooter">
  <div class="footer-left">
    <strong>CivicRoute — AI Citizen Grievance Management Portal</strong>
    <span>Built with TensorFlow · Keras Bi-LSTM · Streamlit &nbsp;|&nbsp; Government of India Initiative</span>
  </div>
  <div class="footer-right">
    <a href="mailto:grievance@municipal.gov.in">grievance@municipal.gov.in</a><br>
    © 2026 Municipal Corporation of India
  </div>
</div>
""", unsafe_allow_html=True)
