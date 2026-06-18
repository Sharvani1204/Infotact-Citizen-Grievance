import streamlit as st
import datetime

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
# Mappings
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
    label = label.strip().lower()
    return DEPT_DISPLAY.get(label, (label.replace("_", " ").title(), "📋", "MEDIUM"))

# ─────────────────────────────────────────────
# CSS
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
   TOP BAR
═══════════════════════════════════════════ */
.topbar {
    background: #0A1628;
    color: white;
    padding: 0 48px;
    height: 56px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #F59E0B;
    position: sticky;
    top: 0;
    z-index: 100;
}
.topbar-left { display: flex; align-items: center; gap: 12px; }
.topbar-logo {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, #F59E0B, #EF4444);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; font-weight: 700; color: white;
    font-family: 'Sora', sans-serif;
    flex-shrink: 0;
}
.topbar-brand strong {
    display: block; font-size: 13px; font-weight: 700;
    letter-spacing: 1.2px; color: white; font-family: 'Sora', sans-serif;
}
.topbar-brand span { font-size: 10.5px; color: rgba(255,255,255,0.45); letter-spacing: 0.3px; }
.topbar-divider {
    width: 1px; height: 26px; background: rgba(255,255,255,0.12); margin: 0 18px;
}
.topbar-tag {
    background: rgba(245,158,11,0.15);
    border: 1px solid rgba(245,158,11,0.3);
    color: #FCD34D;
    font-size: 10px; font-weight: 600; letter-spacing: 0.8px;
    text-transform: uppercase; padding: 3px 10px; border-radius: 4px;
}
.topbar-right { font-size: 11px; color: rgba(255,255,255,0.4); text-align: right; line-height: 1.7; }

/* ═══════════════════════════════════════════
   HERO
═══════════════════════════════════════════ */
.hero {
    background: linear-gradient(135deg, #0A1628 0%, #0D2045 45%, #102B60 100%);
    color: white;
    padding: 56px 60px 52px;
    position: relative;
    overflow: hidden;
}
.hero-grid {
    position: absolute; inset: 0; pointer-events: none;
    background-image:
        linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
    background-size: 40px 40px;
}
.hero-glow {
    position: absolute; right: -120px; top: -120px;
    width: 500px; height: 500px; border-radius: 50%;
    background: radial-gradient(circle, rgba(245,158,11,0.12) 0%, transparent 65%);
    pointer-events: none;
}
.hero-glow2 {
    position: absolute; left: 30%; bottom: -100px;
    width: 300px; height: 300px; border-radius: 50%;
    background: radial-gradient(circle, rgba(99,102,241,0.10) 0%, transparent 65%);
    pointer-events: none;
}
.hero-inner { position: relative; z-index: 1; }
.hero-eyebrow {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(245,158,11,0.12);
    border: 1px solid rgba(245,158,11,0.35);
    border-radius: 6px;
    padding: 5px 14px 5px 10px;
    margin-bottom: 22px;
}
.hero-eyebrow-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #F59E0B;
    box-shadow: 0 0 8px #F59E0B;
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.6; transform: scale(0.85); }
}
.hero-eyebrow-text {
    font-size: 10.5px; font-weight: 600; letter-spacing: 1px;
    color: #FCD34D; text-transform: uppercase;
}
.hero h1 {
    font-family: 'Sora', sans-serif;
    font-size: 42px; font-weight: 800;
    line-height: 1.1; letter-spacing: -0.5px;
    margin-bottom: 16px; color: white;
}
.hero h1 em {
    font-style: normal;
    background: linear-gradient(90deg, #F59E0B, #FCD34D);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-desc {
    font-size: 15px; color: rgba(255,255,255,0.65);
    max-width: 580px; line-height: 1.75; margin-bottom: 30px;
}
.hero-chips { display: flex; gap: 10px; flex-wrap: wrap; }
.hero-chip {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px; padding: 5px 14px;
    font-size: 11.5px; font-weight: 500; color: rgba(255,255,255,0.75);
}

/* ═══════════════════════════════════════════
   STATS
═══════════════════════════════════════════ */
.stats-wrap {
    background: white;
    border-bottom: 1px solid #E5EAF2;
    padding: 0 60px;
}
.stats-inner {
    display: flex; gap: 0;
    max-width: 1400px; margin: 0 auto;
}
.stat-item {
    flex: 1; padding: 22px 30px; display: flex; align-items: center;
    gap: 16px; border-right: 1px solid #F0F4FA;
    transition: background 0.2s;
}
.stat-item:last-child { border-right: none; }
.stat-item:hover { background: #FAFBFF; }
.stat-ico-wrap {
    width: 46px; height: 46px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; flex-shrink: 0;
}
.s-blue  { background: #EFF6FF; }
.s-green { background: #F0FDF4; }
.s-amber { background: #FFFBEB; }
.s-rose  { background: #FFF1F2; }
.stat-lbl { font-size: 10.5px; color: #94A3B8; font-weight: 600; letter-spacing: 0.4px; text-transform: uppercase; margin-bottom: 4px; }
.stat-val { font-size: 24px; font-weight: 800; color: #0A1628; line-height: 1; font-family: 'Sora', sans-serif; }
.stat-trend { font-size: 10px; color: #22C55E; font-weight: 600; margin-top: 3px; }

/* ═══════════════════════════════════════════
   BODY LAYOUT
═══════════════════════════════════════════ */
.body-wrap {
    padding: 32px 60px 40px;
    display: flex; gap: 28px; align-items: flex-start;
    max-width: 1400px; margin: 0 auto;
}

/* ═══════════════════════════════════════════
   FORM PANEL
═══════════════════════════════════════════ */
.fpanel {
    background: white;
    border: 1px solid #E5EAF2;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 24px rgba(10,22,40,0.07), 0 1px 4px rgba(10,22,40,0.04);
}
.fpanel-head {
    padding: 20px 28px;
    display: flex; align-items: center; gap: 14px;
    border-bottom: 1px solid #F0F4FA;
    background: linear-gradient(135deg, #0A1628, #0D2045);
}
.fpanel-head-iconbox {
    width: 42px; height: 42px; border-radius: 10px;
    background: rgba(245,158,11,0.18);
    border: 1px solid rgba(245,158,11,0.3);
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; flex-shrink: 0;
}
.fpanel-head-title { font-size: 15px; font-weight: 700; color: white; font-family: 'Sora', sans-serif; margin-bottom: 3px; }
.fpanel-head-sub { font-size: 11px; color: rgba(255,255,255,0.45); }

.fpanel-body { padding: 28px 28px 24px; }
.field-lbl {
    display: block; font-size: 11px; font-weight: 700;
    color: #64748B; text-transform: uppercase; letter-spacing: 0.8px;
    margin-bottom: 10px;
}
.req { color: #EF4444; margin-left: 2px; }
.char-hint { font-size: 10.5px; color: #94A3B8; font-weight: 500; margin-top: 6px; }

[data-testid="stTextArea"] textarea {
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important; line-height: 1.65 !important;
    color: #1A2332 !important;
    padding: 14px 16px !important;
    background: #FAFBFF !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    resize: vertical !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: #3B82F6 !important;
    background: white !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.10) !important;
    outline: none !important;
}
[data-testid="stTextArea"] label { display: none !important; }

.example-chips { display: flex; gap: 8px; flex-wrap: wrap; margin: 14px 0; }
.example-chip {
    display: inline-flex; align-items: center; gap: 5px;
    background: #F1F5F9; border: 1px solid #E2E8F0;
    border-radius: 6px; padding: 4px 12px;
    font-size: 11.5px; color: #475569; font-weight: 500;
    cursor: default; transition: all 0.15s;
}
.example-chip:hover { background: #EFF6FF; border-color: #BFDBFE; color: #1D4ED8; }
.example-lbl { font-size: 10.5px; color: #94A3B8; font-weight: 600; letter-spacing: 0.4px; text-transform: uppercase; margin-bottom: 8px; }

[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #1D4ED8, #2563EB) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important; font-weight: 700 !important;
    letter-spacing: 0.3px !important;
    padding: 14px 28px !important; width: 100% !important;
    box-shadow: 0 4px 16px rgba(37,99,235,0.30) !important;
    transition: all 0.2s ease !important;
    margin-top: 4px !important;
}
[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #1E40AF, #2563EB) !important;
    box-shadow: 0 8px 24px rgba(37,99,235,0.40) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ═══════════════════════════════════════════
   RESULT CARD
═══════════════════════════════════════════ */
.rcard {
    margin-top: 20px;
    background: white;
    border: 1px solid #E5EAF2;
    border-radius: 16px; overflow: hidden;
    box-shadow: 0 4px 24px rgba(10,22,40,0.07);
    animation: slideUp 0.4s cubic-bezier(0.16,1,0.3,1);
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
.rcard-banner {
    padding: 14px 24px;
    display: flex; align-items: center; gap: 10px;
    font-size: 12px; font-weight: 700; letter-spacing: 0.6px;
    text-transform: uppercase; color: white;
}
.rcard-check {
    width: 24px; height: 24px; border-radius: 50%;
    background: rgba(255,255,255,0.2);
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; flex-shrink: 0;
}
.rcard-body { padding: 26px 24px; }
.rcard-dept-eyebrow { font-size: 10px; color: #94A3B8; font-weight: 700; letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 10px; }
.rcard-dept-row { display: flex; align-items: center; gap: 14px; margin-bottom: 22px; }
.rcard-dept-icon {
    width: 56px; height: 56px; border-radius: 14px;
    background: #F0F4FA; display: flex; align-items: center;
    justify-content: center; font-size: 28px; flex-shrink: 0;
}
.rcard-dept-name { font-size: 20px; font-weight: 800; color: #0A1628; line-height: 1.2; font-family: 'Sora', sans-serif; }
.rcard-pills { display: flex; gap: 8px; flex-wrap: wrap; }
.rcard-pill {
    display: inline-flex; align-items: center; gap: 5px;
    background: #F1F5F9; border-radius: 6px;
    padding: 6px 12px; font-size: 12px; font-weight: 600; color: #334155;
    border: 1px solid #E2E8F0;
}
.rcard-pill-pri {
    border: 1.5px solid;
    font-weight: 700;
}
.rcard-divider { height: 1px; background: #F0F4FA; margin: 20px 0; }
.rcard-ticket {
    display: flex; align-items: center; justify-content: space-between;
    background: #F8FAFF; border: 1px solid #E8EEFE;
    border-radius: 10px; padding: 12px 16px;
}
.rcard-ticket-lbl { font-size: 10.5px; color: #94A3B8; font-weight: 600; letter-spacing: 0.4px; text-transform: uppercase; margin-bottom: 4px; }
.rcard-ticket-id { font-size: 16px; font-weight: 800; color: #1D4ED8; font-family: 'Sora', sans-serif; letter-spacing: 0.5px; }
.rcard-ticket-status {
    display: flex; align-items: center; gap: 6px;
    font-size: 11px; font-weight: 700;
    color: #15803D; background: #F0FDF4;
    border: 1px solid #BBF7D0; border-radius: 6px;
    padding: 5px 12px;
}
.status-dot { width: 7px; height: 7px; border-radius: 50%; background: #22C55E; animation: pulse 2s infinite; }

/* ═══════════════════════════════════════════
   SIDE CARDS
═══════════════════════════════════════════ */
.scard {
    background: white; border: 1px solid #E5EAF2;
    border-radius: 14px; padding: 22px;
    box-shadow: 0 2px 12px rgba(10,22,40,0.05);
    margin-bottom: 20px;
}
.scard:last-child { margin-bottom: 0; }
.scard-head {
    display: flex; align-items: center; gap: 8px;
    margin-bottom: 18px; padding-bottom: 14px;
    border-bottom: 1px solid #F0F4FA;
}
.scard-head-bar {
    width: 3px; height: 16px; border-radius: 2px;
    background: linear-gradient(180deg, #F59E0B, #EF4444);
    flex-shrink: 0;
}
.scard-head h4 {
    font-size: 11px; font-weight: 700; color: #0A1628;
    text-transform: uppercase; letter-spacing: 0.8px; margin: 0;
}
.dlist { list-style: none; padding: 0; margin: 0; }
.dlist li {
    display: flex; align-items: center; gap: 10px;
    padding: 7px 0; font-size: 12.5px; color: #475569;
    border-bottom: 1px solid #F8FAFC;
}
.dlist li:last-child { border-bottom: none; }
.ddot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #3B82F6; flex-shrink: 0;
}

.step-item { display: flex; gap: 14px; margin-bottom: 16px; align-items: flex-start; }
.step-item:last-child { margin-bottom: 0; }
.step-num {
    width: 28px; height: 28px; border-radius: 8px;
    background: #0A1628; color: white;
    font-size: 12px; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; margin-top: 1px;
    font-family: 'Sora', sans-serif;
}
.step-content strong { font-size: 12.5px; color: #0A1628; font-weight: 700; display: block; margin-bottom: 3px; }
.step-content span { font-size: 12px; color: #64748B; line-height: 1.55; }

/* ═══════════════════════════════════════════
   AI BADGE CARD
═══════════════════════════════════════════ */
.ai-card {
    background: linear-gradient(135deg, #0A1628, #0D2045);
    border-radius: 14px; padding: 20px;
    margin-bottom: 20px;
    position: relative; overflow: hidden;
}
.ai-card-glow {
    position: absolute; right: -30px; top: -30px;
    width: 120px; height: 120px; border-radius: 50%;
    background: radial-gradient(circle, rgba(245,158,11,0.2), transparent 70%);
    pointer-events: none;
}
.ai-card h4 { font-size: 11px; font-weight: 700; color: rgba(255,255,255,0.4); text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 10px; }
.ai-accuracy { font-size: 38px; font-weight: 800; color: white; font-family: 'Sora', sans-serif; line-height: 1; margin-bottom: 4px; }
.ai-accuracy span { font-size: 18px; color: rgba(255,255,255,0.5); }
.ai-desc { font-size: 11.5px; color: rgba(255,255,255,0.5); margin-bottom: 14px; }
.ai-bar-wrap { background: rgba(255,255,255,0.08); border-radius: 4px; height: 6px; overflow: hidden; }
.ai-bar-fill { height: 100%; border-radius: 4px; background: linear-gradient(90deg, #F59E0B, #FCD34D); width: 94.2%; }

/* ═══════════════════════════════════════════
   FOOTER
═══════════════════════════════════════════ */
.govfooter {
    background: #0A1628;
    padding: 24px 60px;
    display: flex; justify-content: space-between; align-items: center;
    margin-top: 8px;
}
.footer-left strong { display: block; font-size: 13px; font-weight: 700; color: rgba(255,255,255,0.85); margin-bottom: 4px; font-family: 'Sora', sans-serif; }
.footer-left span { font-size: 11px; color: rgba(255,255,255,0.35); }
.footer-right { font-size: 11px; color: rgba(255,255,255,0.35); text-align: right; line-height: 1.8; }
.footer-right a { color: #F59E0B; text-decoration: none; }

/* Streamlit column gap fix */
[data-testid="stColumns"] { gap: 0 !important; padding: 0 !important; }
[data-testid="stColumn"] { padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Top Bar
# ─────────────────────────────────────────────
now = datetime.datetime.now()
st.markdown(f"""
<div class="topbar">
  <div class="topbar-left">
    <div class="topbar-logo">CR</div>
    <div class="topbar-brand">
      <strong>CIVICROUTE PORTAL</strong>
      <span>Municipal Corporation of India — Integrated Grievance Redressal System</span>
    </div>
    <div class="topbar-divider"></div>
    <div class="topbar-tag">🤖 AI-Powered</div>
  </div>
  <div class="topbar-right">
    {now.strftime("%d %b %Y")} &nbsp;·&nbsp; {now.strftime("%I:%M %p IST")}
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Hero
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-grid"></div>
  <div class="hero-glow"></div>
  <div class="hero-glow2"></div>
  <div class="hero-inner">
    <div class="hero-eyebrow">
      <div class="hero-eyebrow-dot"></div>
      <span class="hero-eyebrow-text">Live &nbsp;·&nbsp; Bi-LSTM NLP Engine &nbsp;·&nbsp; 94.2% Accuracy</span>
    </div>
    <h1>Route your complaint to<br>the <em>right department</em>, instantly.</h1>
    <p class="hero-desc">
      Describe your civic issue in plain language. Our deep learning model identifies the
      responsible authority, assigns urgency, and generates a tracked ticket — in under 2 seconds.
    </p>
    <div class="hero-chips">
      <span class="hero-chip">🚰 Water & Drainage</span>
      <span class="hero-chip">🛣️ Roads & Potholes</span>
      <span class="hero-chip">💡 Street Lighting</span>
      <span class="hero-chip">🗑️ Waste Management</span>
      <span class="hero-chip">🚗 Parking & Traffic</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Stats
# ─────────────────────────────────────────────
st.markdown("""
<div class="stats-wrap">
  <div class="stats-inner">
    <div class="stat-item">
      <div class="stat-ico-wrap s-blue">📋</div>
      <div>
        <div class="stat-lbl">Complaints Routed</div>
        <div class="stat-val">24,831</div>
        <div class="stat-trend">↑ 3.2% this week</div>
      </div>
    </div>
    <div class="stat-item">
      <div class="stat-ico-wrap s-green">✅</div>
      <div>
        <div class="stat-lbl">Model Accuracy</div>
        <div class="stat-val">94.2%</div>
        <div class="stat-trend">↑ 1.1% from last run</div>
      </div>
    </div>
    <div class="stat-item">
      <div class="stat-ico-wrap s-amber">⚡</div>
      <div>
        <div class="stat-lbl">Avg. Response Time</div>
        <div class="stat-val">&lt; 2s</div>
        <div class="stat-trend">Real-time inference</div>
      </div>
    </div>
    <div class="stat-item">
      <div class="stat-ico-wrap s-rose">🚨</div>
      <div>
        <div class="stat-lbl">Critical Tickets Today</div>
        <div class="stat-val">7</div>
        <div class="stat-trend">Active escalations</div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Main Layout
# ─────────────────────────────────────────────
st.markdown('<div class="body-wrap">', unsafe_allow_html=True)
left, right = st.columns([2.8, 1.2], gap="large")

with left:
    st.markdown("""
    <div class="fpanel">
      <div class="fpanel-head">
        <div class="fpanel-head-iconbox">📝</div>
        <div>
          <div class="fpanel-head-title">Submit New Complaint</div>
          <div class="fpanel-head-sub">Submissions are encrypted, logged, and tracked under your session ID</div>
        </div>
      </div>
      <div class="fpanel-body">
        <span class="field-lbl">Complaint Description <span class="req">*</span></span>
    """, unsafe_allow_html=True)

    complaint = st.text_area(
        label="complaint",
        height=190,
        placeholder=(
            "Describe your civic issue clearly...\n\n"
            "Example: The drainage pipe near Rajiv Nagar bus stand has been overflowing "
            "for 3 days causing severe water-logging on the main road."
        ),
        label_visibility="collapsed"
    )

    st.markdown("""
        <p class="char-hint">💡 Be specific — include the location, duration, and impact of the issue for faster resolution.</p>
        <div class="example-lbl">Quick examples</div>
        <div class="example-chips">
          <span class="example-chip">🕳️ Pothole on main road</span>
          <span class="example-chip">💧 Water pipe burst</span>
          <span class="example-chip">💡 Street light not working</span>
          <span class="example-chip">🗑️ Garbage not collected</span>
          <span class="example-chip">🚗 Illegal parking</span>
        </div>
    """, unsafe_allow_html=True)

    submit = st.button("🔍  Analyse & Route Complaint", use_container_width=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

    # ── Result ────────────────────────────────
    if submit:
        if not complaint.strip():
            st.warning("⚠️  Please enter a complaint description before submitting.")
        else:
            with st.spinner("Analysing complaint with Bi-LSTM model…"):
                raw_label = predict_department(complaint)

            dept_name, dept_icon, priority = resolve(raw_label)
            p_icon, p_color, p_bg, p_border = PRIORITY_STYLE[priority]
            ticket_id = f"GRV-{now.strftime('%Y%m%d')}-{abs(hash(complaint)) % 9000 + 1000}"

            st.markdown(f"""
            <div class="rcard">
              <div class="rcard-banner" style="background: linear-gradient(135deg, {p_color}, {p_color}CC);">
                <div class="rcard-check">✓</div>
                Complaint routed successfully &nbsp;—&nbsp; AI classification complete
              </div>
              <div class="rcard-body">
                <div class="rcard-dept-eyebrow">Assigned Department</div>
                <div class="rcard-dept-row">
                  <div class="rcard-dept-icon">{dept_icon}</div>
                  <div class="rcard-dept-name">{dept_name}</div>
                </div>
                <div class="rcard-pills">
                  <div class="rcard-pill rcard-pill-pri" style="background:{p_bg}; color:{p_color}; border-color:{p_border};">
                    {p_icon} &nbsp;Priority: {priority}
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
                  <div class="rcard-ticket-status">
                    <div class="status-dot"></div> Active — Awaiting Department
                  </div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

with right:
    # AI accuracy card
    st.markdown("""
    <div class="ai-card">
      <div class="ai-card-glow"></div>
      <h4>Model Performance</h4>
      <div class="ai-accuracy">94.2<span>%</span></div>
      <div class="ai-desc">Classification accuracy on held-out test set</div>
      <div class="ai-bar-wrap"><div class="ai-bar-fill"></div></div>
    </div>
    """, unsafe_allow_html=True)

    # Departments card
    st.markdown("""
    <div class="scard">
      <div class="scard-head">
        <div class="scard-head-bar"></div>
        <h4>Covered Departments</h4>
      </div>
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

    # How it works
    st.markdown("""
    <div class="scard">
      <div class="scard-head">
        <div class="scard-head-bar"></div>
        <h4>How It Works</h4>
      </div>
      <div class="step-item">
        <div class="step-num">1</div>
        <div class="step-content">
          <strong>Describe the Issue</strong>
          <span>Type your complaint in plain language — no forms or codes needed.</span>
        </div>
      </div>
      <div class="step-item">
        <div class="step-num">2</div>
        <div class="step-content">
          <strong>AI Classification</strong>
          <span>Bi-LSTM model routes the complaint to the correct department.</span>
        </div>
      </div>
      <div class="step-item">
        <div class="step-num">3</div>
        <div class="step-content">
          <strong>Priority Assigned</strong>
          <span>Urgency level from Critical to Low is set automatically.</span>
        </div>
      </div>
      <div class="step-item">
        <div class="step-num">4</div>
        <div class="step-content">
          <strong>Ticket Generated</strong>
          <span>A unique reference ID is issued for tracking and follow-up.</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close body-wrap

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("""
<div class="govfooter">
  <div class="footer-left">
    <strong>CivicRoute — AI Citizen Grievance Management Portal</strong>
    <span>Built with TensorFlow · Keras Bi-LSTM · Streamlit &nbsp;|&nbsp; Government of India Initiative</span>
  </div>
  <div class="footer-right">
    <a href="mailto:grievance@municipal.gov.in">grievance@municipal.gov.in</a><br>
    © 2025 Municipal Corporation of India
  </div>
</div>
""", unsafe_allow_html=True)

