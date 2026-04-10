"""
app.py  -  Student Performance Predictor  (Enhanced Professional UI)
"""

import os, sys, json, warnings
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ─── Page config (must be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS injection (theme-aware) ────────────────────────────────────────────
def inject_css(dark):
    if dark:
        # Dark mode - Deep space theme with vibrant accents
        BG      = "#0a0e27"
        CARD    = "rgba(255,255,255,0.03)"
        CARD_HOVER = "rgba(255,255,255,0.06)"
        BORDER  = "rgba(139,92,246,0.15)"
        TXT     = "#f8fafc"
        SUB     = "#cbd5e1"
        MUT     = "#94a3b8"
        SIDEBAR = "linear-gradient(180deg, #0f1629 0%, #1a1f3a 100%)"
        SIDEBAR_BORDER = "rgba(139,92,246,0.2)"
        INP_BG  = "rgba(255,255,255,0.05)"
        INP_BORDER = "rgba(139,92,246,0.3)"
        HERO_BG = "linear-gradient(135deg, #1e1b4b 0%, #312e81 25%, #4c1d95 50%, #5b21b6 75%, #6d28d9 100%)"
        HERO_OVERLAY = "radial-gradient(circle at 20% 50%, rgba(139,92,246,0.3) 0%, transparent 50%), radial-gradient(circle at 80% 50%, rgba(59,130,246,0.2) 0%, transparent 50%)"
        HERO_BORDER = "rgba(167,139,250,0.4)"
        ACCENT_PRIMARY = "#a78bfa"
        ACCENT_SECONDARY = "#60a5fa"
        GLASS_BG = "rgba(15,23,42,0.7)"
        GLASS_BORDER = "rgba(139,92,246,0.3)"
    else:
        # Light mode - Clean modern theme with soft gradients
        BG      = "linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #f0f4f8 100%)"
        CARD    = "rgba(255,255,255,0.9)"
        CARD_HOVER = "rgba(255,255,255,1)"
        BORDER  = "rgba(139,92,246,0.2)"
        TXT     = "#0f172a"
        SUB     = "#475569"
        MUT     = "#64748b"
        SIDEBAR = "linear-gradient(180deg, #ffffff 0%, #f8fafc 100%)"
        SIDEBAR_BORDER = "rgba(139,92,246,0.15)"
        INP_BG  = "rgba(255,255,255,0.8)"
        INP_BORDER = "rgba(139,92,246,0.25)"
        HERO_BG = "linear-gradient(135deg, #ddd6fe 0%, #c7d2fe 25%, #bfdbfe 50%, #bae6fd 75%, #a5f3fc 100%)"
        HERO_OVERLAY = "radial-gradient(circle at 20% 50%, rgba(139,92,246,0.15) 0%, transparent 50%), radial-gradient(circle at 80% 50%, rgba(59,130,246,0.1) 0%, transparent 50%)"
        HERO_BORDER = "rgba(139,92,246,0.3)"
        ACCENT_PRIMARY = "#7c3aed"
        ACCENT_SECONDARY = "#3b82f6"
        GLASS_BG = "rgba(255,255,255,0.8)"
        GLASS_BORDER = "rgba(139,92,246,0.25)"

    hero_title_grad = "linear-gradient(135deg, #1e1b4b 0%, #4c1d95 50%, #1e3a8a 100%)" if not dark else "linear-gradient(135deg, #ffffff 0%, #e0e7ff 50%, #ddd6fe 100%)"
    hero_sub_color  = "#64748b" if not dark else "#cbd5e1"
    hero_stat_val_g = "linear-gradient(90deg, #6d28d9, #2563eb)" if not dark else "linear-gradient(90deg, #c4b5fd, #93c5fd)"

    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ═══════════════════════════════════════════════════════════════════════════
   GLOBAL STYLES & RESET
   ═══════════════════════════════════════════════════════════════════════════ */
*, *::before, *::after {{ 
    box-sizing: border-box; 
    margin: 0;
    padding: 0;
}}

html, body, .stApp {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background: {BG} !important;
    color: {TXT} !important;
    font-size: 16px;
    line-height: 1.6;
}}

#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ 
    padding-top: 2rem !important; 
    padding-bottom: 3rem !important;
    max-width: 1400px !important;
}}
.hero {{
    background: {HERO_BG};
    border: 1px solid {HERO_BORDER};
    border-radius: 20px; padding: 2.4rem 2.8rem; margin-bottom: 2rem;
    position: relative; overflow: hidden;
}}
.hero::before {{
    content: ''; position: absolute; top: -60%; right: -10%;
    width: 420px; height: 420px;
    background: radial-gradient(circle, rgba(139,92,246,0.18) 0%, transparent 70%);
    border-radius: 50%; animation: pulse 6s ease-in-out infinite;
}}
@keyframes pulse {{ 0%,100%{{transform:scale(1);opacity:1;}} 50%{{transform:scale(1.12);opacity:0.7;}} }}
.hero-badge {{
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(139,92,246,0.15); border: 1px solid rgba(139,92,246,0.35);
    border-radius: 30px; padding: 4px 14px; font-size: 0.75rem; font-weight: 600;
    color: #a78bfa; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 1rem;
}}
.hero-title {{
    font-size: 2.6rem; font-weight: 900;
    background: {hero_title_grad};
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1.15; margin: 0 0 0.6rem 0; position: relative; z-index: 1;
}}
.hero-sub {{ font-size: 1.05rem; color: {hero_sub_color}; font-weight: 400; margin: 0; position: relative; z-index: 1; }}
.hero-stats {{ display: flex; gap: 2rem; margin-top: 1.6rem; position: relative; z-index: 1; }}
.hero-stat {{ text-align: left; }}
.hero-stat-val {{ font-size: 1.6rem; font-weight: 800; background: {hero_stat_val_g}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
.hero-stat-lbl {{ font-size: 0.72rem; color: {MUT}; text-transform: uppercase; letter-spacing: 0.8px; }}
.stElementContainer div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 16px !important;
    padding: 0px !important;
    backdrop-filter: blur(12px) !important;
    transition: all 0.3s ease !important;
}}
.stElementContainer div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
    border-color: rgba(139,92,246,0.3) !important;
    box-shadow: 0 0 30px rgba(139,92,246,0.08) !important;
}}
.kpi-wrap {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.4rem; }}
.kpi {{
    background: {CARD}; border: 1px solid {BORDER}; border-radius: 14px;
    padding: 1.2rem 1.4rem; text-align: center; transition: all 0.3s;
}}
.kpi:hover {{ border-color: rgba(139,92,246,0.4); transform: translateY(-2px); box-shadow: 0 8px 24px rgba(139,92,246,0.1); }}
.kpi-val {{ font-size: 1.9rem; font-weight: 800; color: #a78bfa; line-height: 1.1; }}
.kpi-lbl {{ font-size: 0.75rem; color: {MUT}; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.6px; }}
.kpi-icon {{ font-size: 1.4rem; margin-bottom: 0.3rem; }}
.kpi3 {{ grid-template-columns: repeat(3, 1fr); }}
.pred-card {{
    background: linear-gradient(135deg, rgba(139,92,246,0.12) 0%, rgba(59,130,246,0.08) 100%);
    border: 1.5px solid rgba(139,92,246,0.35);
    border-radius: 20px; padding: 2.2rem 2rem; text-align: center;
    box-shadow: 0 0 40px rgba(139,92,246,0.1); margin: 1rem 0;
}}
.pred-gpa {{ font-size: 4.5rem; font-weight: 900; line-height: 1;
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}}
.pred-label {{ font-size: 0.82rem; color: {MUT}; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.4rem; }}
.pred-grade {{ font-size: 1.6rem; font-weight: 700; margin-top: 0.6rem; }}
.pred-sub {{ font-size: 0.9rem; color: {SUB}; margin-top: 0.3rem; }}
.grade-badge {{ display: inline-block; padding: 6px 20px; border-radius: 30px; font-size: 0.85rem; font-weight: 700; margin-top: 0.8rem; }}
.grade-A  {{ background: rgba(34,197,94,0.15);  color: #4ade80; border: 1px solid rgba(34,197,94,0.3);  }}
.grade-B  {{ background: rgba(59,130,246,0.15); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }}
.grade-C  {{ background: rgba(234,179,8,0.15);  color: #facc15; border: 1px solid rgba(234,179,8,0.3);  }}
.grade-D  {{ background: rgba(249,115,22,0.15); color: #fb923c; border: 1px solid rgba(249,115,22,0.3); }}
.grade-F  {{ background: rgba(239,68,68,0.15);  color: #f87171; border: 1px solid rgba(239,68,68,0.3);  }}
.sec-head {{
    font-size: 1.05rem; font-weight: 700; color: {TXT};
    margin: 1.4rem 0 0.8rem 0; display: flex; align-items: center; gap: 8px;
}}
.sec-head::after {{
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(139,92,246,0.4), transparent);
}}
.prog-wrap {{ margin: 0.5rem 0; }}
.prog-label {{ display: flex; justify-content: space-between; font-size: 0.8rem; color: {SUB}; margin-bottom: 4px; }}
.prog-track {{ height: 6px; background: {BORDER}; border-radius: 4px; overflow: hidden; }}
.prog-fill  {{ height: 100%; border-radius: 4px; background: linear-gradient(90deg, #7c3aed, #3b82f6); transition: width 0.8s cubic-bezier(.4,0,.2,1); }}
section[data-testid="stSidebar"] {{
    background: {SIDEBAR} !important;
    border-right: 1px solid {SIDEBAR_BORDER} !important;
}}
.sidebar-logo {{ text-align: center; padding: 1rem 0 0.5rem; font-size: 2.4rem; line-height: 1; }}
.sidebar-title {{ text-align: center; font-size: 1rem; font-weight: 700; color: {TXT}; margin-bottom: 0.2rem; }}
.sidebar-sub {{ text-align: center; font-size: 0.72rem; color: {MUT}; margin-bottom: 1rem; }}
.status-pill {{ display: flex; align-items: center; gap: 8px; padding: 8px 14px; border-radius: 30px; font-size: 0.8rem; font-weight: 600; margin: 0.5rem 0; }}
.status-on  {{ background: rgba(34,197,94,0.1);  color: #4ade80; border: 1px solid rgba(34,197,94,0.25);  }}
.status-off {{ background: rgba(239,68,68,0.1);  color: #f87171; border: 1px solid rgba(239,68,68,0.25);  }}
.dot {{ width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }}
.dot-on  {{ background: #4ade80; box-shadow: 0 0 6px #4ade80; animation: blink 1.5s ease-in-out infinite; }}
.dot-off {{ background: #f87171; }}
@keyframes blink {{ 0%,100%{{opacity:1;}} 50%{{opacity:0.4;}} }}
.stTabs [data-baseweb="tab-list"] {{
    gap: 6px; background: transparent !important;
    border-bottom: 1px solid {BORDER} !important;
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent !important; border: 1px solid transparent !important;
    border-radius: 8px 8px 0 0 !important; color: {MUT} !important;
    font-weight: 500 !important; padding: 8px 18px !important; transition: all 0.2s !important;
}}
.stTabs [aria-selected="true"] {{
    background: rgba(139,92,246,0.12) !important;
    border-color: rgba(139,92,246,0.3) !important; color: #a78bfa !important;
}}
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] > div {{
    background: {INP_BG} !important;
    border: 1px solid {INP_BORDER} !important;
    border-radius: 8px !important; color: {TXT} !important;
}}
.stButton > button {{ border-radius: 10px !important; font-weight: 600 !important; transition: all 0.25s !important; }}
.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, #7c3aed, #3b82f6) !important;
    border: none !important; box-shadow: 0 4px 20px rgba(124,58,237,0.35) !important;
}}
.stButton > button[kind="primary"]:hover {{ transform: translateY(-1px) !important; box-shadow: 0 8px 28px rgba(124,58,237,0.45) !important; }}
.stDataFrame {{ border-radius: 12px; overflow: hidden; }}
.stAlert {{ border-radius: 10px !important; }}
.insight-card {{
    background: {CARD}; border: 1px solid {BORDER}; border-radius: 12px;
    padding: 1rem 1.2rem; margin-bottom: 0.75rem;
}}
.insight-row {{ display:flex; justify-content:space-between; align-items:center; margin:0.35rem 0; font-size:0.82rem; }}
.insight-key {{ color:{SUB}; }}
.insight-val {{ color:#a78bfa; font-weight:700; }}
.stTabs [aria-selected="true"] {{ background: rgba(139,92,246,0.12) !important; border-color: rgba(139,92,246,0.3) !important; color: #a78bfa !important; }}

/* Streamlit Widget Text Contrast */
.stSlider label, .stSelectbox label, .stNumberInput label, .stTextInput label, .stCheckbox label, .stMultiSelect label, .stRadio label {{
    color: {TXT} !important; font-weight: 500 !important;
}}
div[data-testid="stMarkdownContainer"] p, div[data-testid="stMarkdownContainer"] span {{
    color: {TXT} !important;
}}
.stSlider [data-testid="stWidgetLabel"] {{ color: {TXT} !important; }}

/* Input field cleanup */
.stSlider > div > div > div > div {{ background: #7c3aed !important; }}
div[data-testid="stNumberInput"] input, div[data-testid="stTextInput"] input, div[data-testid="stSelectbox"] > div {{
    background: {INP_BG} !important; border: 1px solid {INP_BORDER} !important; border-radius: 8px !important; color: {TXT} !important;
}}
</style>
""", unsafe_allow_html=True)

# ─── Constants ────────────────────────────────────────────────────────────────
MODEL_DIR    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
DATASET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset", "Student_performance_data _.csv")
METADATA_PATH = os.path.join(MODEL_DIR, "model_metadata.json")

FEATURE_COLS = ["Age","Gender","Ethnicity","ParentalEducation","StudyTimeWeekly",
                "Absences","Tutoring","ParentalSupport","Extracurricular","Sports","Music","Volunteering"]

# ─── Helpers ──────────────────────────────────────────────────────────────────
class MinimalPreprocessor:
    """
    Lightweight preprocessor wrapper that stores the scaler and feature names
    in a format compatible with the existing app.py.
    """
    def __init__(self, feature_cols, scaler):
        self.feature_columns     = feature_cols
        self.scaler              = scaler
        self.label_encoders      = {}
        self.categorical_columns = []
        self.numerical_columns   = feature_cols
        self.target_column       = "GPA"
        self.is_fitted           = True

def gpa_to_grade(gpa):
    """Grade thresholds on 0-10 scale."""
    if gpa >= 9.0: return "A",  "Excellent", "grade-A"
    if gpa >= 7.5: return "B",  "Good",      "grade-B"
    if gpa >= 6.0: return "C",  "Average",   "grade-C"
    if gpa >= 4.0: return "D",  "Below Avg", "grade-D"
    return               "F",  "Failing",   "grade-F"

def load_metadata():
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH) as f:
            return json.load(f)
    return None

def load_model_and_preprocessor():
    mp = os.path.join(MODEL_DIR, "best_model.joblib")
    pp = os.path.join(MODEL_DIR, "preprocessor.joblib")
    if os.path.exists(mp) and os.path.exists(pp):
        return joblib.load(mp), joblib.load(pp)
    return None, None

def predict_gpa(model, preprocessor, input_dict):
    """Returns GPA on 0-10 scale (model output 0-4 scaled x2.5)."""
    df = pd.DataFrame([input_dict])
    for col in FEATURE_COLS:
        if col not in df.columns:
            df[col] = 0
    df = df[FEATURE_COLS]
    X = preprocessor.scaler.transform(df)
    pred = float(model.predict(X)[0])
    pred_4scale = max(0.0, min(4.0, pred))
    return round(pred_4scale * 2.5, 2)  # convert 0-4 -> 0-10

def plotly_theme(dark=True):
    txt_c  = "#94a3b8" if dark else "#4a5568"
    return dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color=txt_c),
    )

def apply_axes_style(fig, dark=True):
    grid_c = "rgba(255,255,255,0.06)" if dark else "rgba(0,0,0,0.08)"
    txt_c  = "#94a3b8" if dark else "#475569"
    fig.update_xaxes(gridcolor=grid_c, zerolinecolor=grid_c, tickfont=dict(color=txt_c))
    fig.update_yaxes(gridcolor=grid_c, zerolinecolor=grid_c, tickfont=dict(color=txt_c))
    return fig

def prog_bar(label, val_str, pct):
    return f"""
    <div class="prog-wrap">
        <div class="prog-label"><span>{label}</span><span>{val_str}</span></div>
        <div class="prog-track"><div class="prog-fill" style="width:{pct:.0f}%"></div></div>
    </div>"""

# ─── Session state ─────────────────────────────────────────────────────────────
if "model" not in st.session_state:
    st.session_state.model        = None
    st.session_state.preprocessor = None
    st.session_state.metadata     = None
    st.session_state.df           = None
    st.session_state.history      = []
    st.session_state.dark_mode    = True

# Auto-load model on startup
if st.session_state.model is None:
    m, p = load_model_and_preprocessor()
    if m:
        st.session_state.model        = m
        st.session_state.preprocessor = p
        st.session_state.metadata     = load_metadata()

# Auto-load dataset
if st.session_state.df is None and os.path.exists(DATASET_PATH):
    st.session_state.df = pd.read_csv(DATASET_PATH)


# Inject theme CSS based on current mode
inject_css(dark=st.session_state.dark_mode)

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🎓</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Student Performance</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">AI Prediction Dashboard</div>', unsafe_allow_html=True)

    # ── Dark / Light toggle ──
    col_tog1, col_tog2 = st.columns([1, 2])
    with col_tog1:
        st.markdown('<div style="padding-top:6px;font-size:1.2rem;">' +
            ('🌙' if st.session_state.dark_mode else '☀️') + '</div>', unsafe_allow_html=True)
    with col_tog2:
        toggled = st.toggle(
            "Dark Mode" if st.session_state.dark_mode else "Light Mode",
            value=st.session_state.dark_mode,
            key="theme_toggle"
        )
    if toggled != st.session_state.dark_mode:
        st.session_state.dark_mode = toggled
        st.rerun()

    st.markdown("---")

    # Model status
    if st.session_state.model:
        st.markdown('<div class="status-pill status-on"><div class="dot dot-on"></div>Model Ready</div>', unsafe_allow_html=True)
        meta = st.session_state.metadata
        if meta:
            best = meta.get("best_model","-")
            r2   = meta.get("metrics",{}).get(best,{}).get("r2_score","-")
            st.markdown(f'<div style="font-size:0.75rem;color:#64748b;padding:0 4px;">🏆 {best} &nbsp;|&nbsp; R² {r2}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-pill status-off"><div class="dot dot-off"></div>No Model Loaded</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**📂 Dataset**")
    if st.session_state.df is not None:
        df = st.session_state.df
        st.markdown(f'<div style="font-size:0.8rem;color:#64748b;">✅ {len(df):,} records loaded</div>', unsafe_allow_html=True)
    else:
        uploaded = st.file_uploader("Upload CSV", type=["csv"])
        if uploaded:
            st.session_state.df = pd.read_csv(uploaded)
            st.success(f"Loaded {len(st.session_state.df):,} records")

    st.markdown("---")
    st.markdown("**⚡ Quick Facts**")
    st.markdown("""
<div style="font-size:0.78rem; color:#64748b; line-height:1.9;">
🔢 &nbsp;3 ML Models compared<br>
🧬 &nbsp;12 input features<br>
📈 &nbsp;Predicts GPA (0-10)<br>
🎯 &nbsp;95.32% R² accuracy
</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="text-align:center;font-size:0.7rem;color:#1e293b;">Built with Streamlit · Scikit-learn</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  HERO BANNER
# ══════════════════════════════════════════════════════════════════════════════
df = st.session_state.df
n_records = len(df) if df is not None else 2393
avg_gpa   = round(df["GPA"].mean() * 2.5, 2) if (df is not None and "GPA" in df.columns) else 4.78

st.markdown(f"""
<div class="hero">
  <div class="hero-badge">✦ AI-Powered Analytics</div>
  <h1 class="hero-title">Student Performance Predictor</h1>
  <p class="hero-sub">Predict GPA with machine learning · Explore patterns · Compare models</p>
  <div class="hero-stats">
    <div class="hero-stat"><div class="hero-stat-val">{n_records:,}</div><div class="hero-stat-lbl">Students</div></div>
    <div class="hero-stat"><div class="hero-stat-val">95.32%</div><div class="hero-stat-lbl">R² Accuracy</div></div>
    <div class="hero-stat"><div class="hero-stat-val">{avg_gpa}</div><div class="hero-stat-lbl">Avg GPA</div></div>
    <div class="hero-stat"><div class="hero-stat-val">3</div><div class="hero-stat-lbl">ML Models</div></div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "🔮  Predict GPA",
    "📊  Data Explorer",
    "📈  Model Performance",
    "ℹ️  About",
])


# ─── TAB 1 · PREDICT ──────────────────────────────────────────────────────────
with tab1:
    if st.session_state.model is None:
        st.warning("⚠️ No trained model found. Run `python train_new_dataset.py` first.")
    else:
        # Enhanced input section with better organization
        st.markdown('<div class="sec-head">🧑‍🎓 Student Profile Input</div>', unsafe_allow_html=True)

        # Three column layout for better space utilization
        col1, col2, col3 = st.columns([1, 1, 1], gap="medium")

        with col1:
            with st.container(border=True):
                st.markdown("**👤 Demographics & Background**")
                age    = st.slider("Age", 15, 18, 17, help="Student's current age")
                gender = st.selectbox("Gender", ["Male (1)", "Female (0)"], help="Biological gender")
                gender_val = 1 if "Male" in gender else 0
                ethnicity = st.selectbox("Ethnicity", ["Group 0","Group 1","Group 2","Group 3"], help="Ethnic background group")
                eth_val = int(ethnicity.split()[-1])
                par_edu = st.selectbox("Parental Education", ["None (0)","High School (1)","Some College (2)","Bachelor's (3)","Higher (4)"], help="Highest education level of parents")
                par_edu_val = int(par_edu.split("(")[-1].replace(")",""))

        with col2:
            with st.container(border=True):
                st.markdown("**📚 Academic Performance**")
                study_time = st.slider("Weekly Study Hours", 0.0, 20.0, 10.0, 0.5, help="Hours spent studying per week")
                absences   = st.slider("Absences This Term", 0, 30, 5, help="Number of days absent")
                tutoring   = st.checkbox("Receives Tutoring", value=False, help="Currently receiving tutoring support")
                par_support = st.select_slider("Parental Support", options=[0,1,2,3,4], value=2, help="Level of parental involvement (0=None, 4=Very High)")

        with col3:
            with st.container(border=True):
                st.markdown("**🏃 Activities & Engagement**")
                extracurr = st.checkbox("Extracurricular Activities", value=False, help="Participates in school clubs/activities")
                sports    = st.checkbox("Sports", value=False, help="Participates in sports teams")
                music     = st.checkbox("Music", value=False, help="Participates in music programs")
                volunteer = st.checkbox("Volunteering", value=False, help="Engages in volunteer work")
                
                activities = sum([extracurr, sports, music, volunteer])
                st.markdown(f"""
                <div style="margin-top:1rem;padding:0.8rem;background:rgba(124,58,237,0.1);border-radius:8px;text-align:center;">
                    <div style="font-size:2rem;font-weight:800;color:#a78bfa;">{activities}/4</div>
                    <div style="font-size:0.75rem;color:#94a3b8;">Active Engagements</div>
                </div>
                """, unsafe_allow_html=True)

        # Enhanced visual summary section
        st.markdown('<div class="sec-head">📊 Profile Analysis</div>', unsafe_allow_html=True)
        
        sum_col1, sum_col2 = st.columns([1.2, 1], gap="large")
        
        with sum_col1:
            with st.container(border=True):
                st.markdown("**📈 Performance Indicators**")
                
                # Calculate percentiles if dataset available
                if df is not None:
                    study_percentile = (df["StudyTimeWeekly"] < study_time).mean() * 100
                    absence_percentile = (df["Absences"] > absences).mean() * 100
                    
                    st.markdown(prog_bar("Study Time", f"{study_time}h/wk (Top {100-study_percentile:.0f}%)", (study_time/20)*100), unsafe_allow_html=True)
                    st.markdown(prog_bar("Attendance", f"{max(0,100-absences*3.33):.0f}% (Better than {absence_percentile:.0f}%)", max(0,100-absences*3.33)), unsafe_allow_html=True)
                else:
                    st.markdown(prog_bar("Study Time", f"{study_time}h/wk", (study_time/20)*100), unsafe_allow_html=True)
                    st.markdown(prog_bar("Attendance (est.)", f"{max(0,100-absences*3.33):.0f}%", max(0,100-absences*3.33)), unsafe_allow_html=True)
                
                st.markdown(prog_bar("Parental Support", f"Level {par_support}/4", (par_support/4)*100), unsafe_allow_html=True)
                st.markdown(prog_bar("Activity Engagement", f"{activities}/4 activities", (activities/4)*100), unsafe_allow_html=True)
                
                # Support factors summary
                support_score = (int(tutoring) + (par_support/4) + (activities/4)) / 3 * 100
                st.markdown(prog_bar("Overall Support", f"{support_score:.0f}%", support_score), unsafe_allow_html=True)

        with sum_col2:
            # Dataset comparison insights
            if df is not None and "GPA" in df.columns:
                with st.container(border=True):
                    st.markdown("**🎯 Benchmark Comparison**")
                    avg_st  = df["StudyTimeWeekly"].mean()
                    avg_abs = df["Absences"].mean()
                    avg_g   = df["GPA"].mean() * 2.5
                    pct_tut = df["Tutoring"].mean() * 100
                    pct_ext = df["Extracurricular"].mean() * 100
                    
                    # Comparison metrics
                    study_diff = ((study_time - avg_st) / avg_st * 100) if avg_st > 0 else 0
                    absence_diff = ((absences - avg_abs) / avg_abs * 100) if avg_abs > 0 else 0
                    
                    st.markdown(f"""
<div class="insight-card" style="margin:0;">
  <div class="insight-row"><span class="insight-key">📚 Your Study Time</span><span class="insight-val">{study_time:.1f}h ({study_diff:+.0f}%)</span></div>
  <div class="insight-row"><span class="insight-key">📊 Dataset Average</span><span class="insight-val">{avg_st:.1f}h</span></div>
  <div style="height:1px;background:rgba(255,255,255,0.06);margin:0.5rem 0;"></div>
  <div class="insight-row"><span class="insight-key">🚫 Your Absences</span><span class="insight-val">{absences} ({absence_diff:+.0f}%)</span></div>
  <div class="insight-row"><span class="insight-key">📊 Dataset Average</span><span class="insight-val">{avg_abs:.1f}</span></div>
  <div style="height:1px;background:rgba(255,255,255,0.06);margin:0.5rem 0;"></div>
  <div class="insight-row"><span class="insight-key">🎓 Expected GPA Range</span><span class="insight-val">{avg_g-0.5:.1f} - {avg_g+0.5:.1f}</span></div>
  <div class="insight-row"><span class="insight-key">🧑‍🏫 Tutoring Rate</span><span class="insight-val">{pct_tut:.0f}%</span></div>
  <div class="insight-row"><span class="insight-key">🏃 Activity Rate</span><span class="insight-val">{pct_ext:.0f}%</span></div>
</div>""", unsafe_allow_html=True)
                
                # Mini distribution chart
                with st.container(border=True):
                    st.markdown("**📉 GPA Distribution Context**")
                    fig_mini = go.Figure()
                    
                    # Histogram
                    fig_mini.add_trace(go.Histogram(
                        x=df["GPA"] * 2.5, nbinsx=30,
                        marker_color="#7c3aed", opacity=0.7,
                        marker_line_color="rgba(124,58,237,0.3)", marker_line_width=1,
                        name="Students"
                    ))
                    
                    # Average line
                    fig_mini.add_vline(x=avg_g, line_color="#f59e0b", line_width=2, line_dash="dash",
                        annotation_text=f"Avg: {avg_g:.2f}", annotation_position="top",
                        annotation_font_color="#f59e0b", annotation_font_size=10)
                    
                    fig_mini.update_layout(
                        **plotly_theme(st.session_state.dark_mode), height=200,
                        margin=dict(l=10, r=10, t=10, b=30),
                        showlegend=False,
                    )
                    apply_axes_style(fig_mini, st.session_state.dark_mode)
                    fig_mini.update_xaxes(title="GPA (0-10 scale)", tickfont=dict(size=9))
                    fig_mini.update_yaxes(title="Count", tickfont=dict(size=9))
                    st.plotly_chart(fig_mini, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Enhanced prediction button
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            predict_btn = st.button("🔮  Predict Student Performance", use_container_width=True, type="primary")

        if predict_btn:
            input_dict = {
                "Age": age, "Gender": gender_val, "Ethnicity": eth_val,
                "ParentalEducation": par_edu_val, "StudyTimeWeekly": study_time,
                "Absences": absences, "Tutoring": int(tutoring),
                "ParentalSupport": par_support, "Extracurricular": int(extracurr),
                "Sports": int(sports), "Music": int(music), "Volunteering": int(volunteer),
            }
            with st.spinner("🤖 Analyzing student profile and generating prediction..."):
                gpa = predict_gpa(st.session_state.model, st.session_state.preprocessor, input_dict)

            letter, desc, badge_cls = gpa_to_grade(gpa)
            pct = (gpa / 10.0) * 100
            
            # Calculate percentile rank if dataset available
            percentile_rank = 0
            if df is not None and "GPA" in df.columns:
                percentile_rank = (df["GPA"] * 2.5 < gpa).mean() * 100

            st.markdown('<div class="sec-head">🎯 Prediction Results</div>', unsafe_allow_html=True)
            
            # Enhanced prediction display
            res_col1, res_col2 = st.columns([1, 1.2], gap="large")
            
            with res_col1:
                st.markdown(f"""
                <div class="pred-card">
                    <div class="pred-label">Predicted GPA</div>
                    <div class="pred-gpa">{gpa:.2f}</div>
                    <div class="pred-sub">out of 10.00</div>
                    <div class="pred-grade">
                        <span class="grade-badge {badge_cls}">Grade {letter} - {desc}</span>
                    </div>
                    {"<div style='margin-top:1rem;font-size:0.85rem;color:#94a3b8;'>📊 Better than " + f"{percentile_rank:.1f}% of students</div>" if percentile_rank > 0 else ""}
                </div>""", unsafe_allow_html=True)

            with res_col2:
                # Gauge chart for GPA
                fig_gauge_gpa = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=gpa,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    number={'suffix': "/10", 'font': {'size': 40, 'color': '#a78bfa'}},
                    gauge={
                        'axis': {'range': [0, 10], 'tickwidth': 1, 'tickcolor': "#64748b"},
                        'bar': {'color': "#7c3aed", 'thickness': 0.3},
                        'bgcolor': "rgba(0,0,0,0)",
                        'borderwidth': 2,
                        'bordercolor': "rgba(124,58,237,0.3)",
                        'steps': [
                            {'range': [0, 4], 'color': 'rgba(239,68,68,0.15)'},
                            {'range': [4, 6], 'color': 'rgba(249,115,22,0.15)'},
                            {'range': [6, 7.5], 'color': 'rgba(234,179,8,0.15)'},
                            {'range': [7.5, 9], 'color': 'rgba(59,130,246,0.15)'},
                            {'range': [9, 10], 'color': 'rgba(34,197,94,0.15)'},
                        ],
                        'threshold': {
                            'line': {'color': "#4ade80", 'width': 3},
                            'thickness': 0.75,
                            'value': 7.5
                        }
                    },
                    title={'text': "GPA Score", 'font': {'size': 16, 'color': '#94a3b8'}}
                ))
                fig_gauge_gpa.update_layout(**plotly_theme(st.session_state.dark_mode), height=280, margin=dict(l=20, r=20, t=50, b=20))
                st.plotly_chart(fig_gauge_gpa, use_container_width=True)

            # Enhanced KPI metrics
            meta = st.session_state.metadata or {}
            best = meta.get("best_model","Linear Regression")
            r2   = meta.get("metrics",{}).get(best,{}).get("r2_score", 0.9532)
            confidence = round(r2 * 100, 1)
            
            # Calculate risk factors
            risk_factors = []
            if absences > 10: risk_factors.append("High Absences")
            if study_time < 5: risk_factors.append("Low Study Time")
            if par_support < 2: risk_factors.append("Low Support")
            if activities == 0: risk_factors.append("No Activities")
            
            risk_count = len(risk_factors)
            risk_color = "#4ade80" if risk_count == 0 else "#facc15" if risk_count <= 2 else "#f87171"

            st.markdown(f"""
            <div class="kpi-wrap">
                <div class="kpi"><div class="kpi-icon">🎯</div><div class="kpi-val">{gpa:.2f}</div><div class="kpi-lbl">Predicted GPA</div></div>
                <div class="kpi"><div class="kpi-icon">🏅</div><div class="kpi-val">{letter}</div><div class="kpi-lbl">Letter Grade</div></div>
                <div class="kpi"><div class="kpi-icon">📊</div><div class="kpi-val">{confidence}%</div><div class="kpi-lbl">Model Confidence</div></div>
                <div class="kpi"><div class="kpi-icon">⚠️</div><div class="kpi-val" style="color:{risk_color}">{risk_count}</div><div class="kpi-lbl">Risk Factors</div></div>
            </div>""", unsafe_allow_html=True)

            # Detailed analysis section
            st.markdown('<div class="sec-head">📊 Detailed Performance Analysis</div>', unsafe_allow_html=True)
            
            analysis_col1, analysis_col2 = st.columns(2, gap="large")
            
            with analysis_col1:
                # Enhanced radar chart
                categories = ["Study Time","Attendance","Parental Support","Activities","Tutoring"]
                values = [
                    (study_time/20)*100,
                    max(0, 100-absences*3.33),
                    (par_support/4)*100,
                    (activities/4)*100,
                    100 if tutoring else 0,
                ]
                
                fig_radar = go.Figure()
                
                # Add student profile
                fig_radar.add_trace(go.Scatterpolar(
                    r=values+[values[0]], 
                    theta=categories+[categories[0]],
                    fill='toself',
                    fillcolor='rgba(124,58,237,0.2)',
                    line=dict(color='#a78bfa', width=3),
                    marker=dict(color='#a78bfa', size=8),
                    name='Student Profile'
                ))
                
                # Add average profile if dataset available
                if df is not None:
                    avg_values = [
                        (df["StudyTimeWeekly"].mean()/20)*100,
                        max(0, 100-df["Absences"].mean()*3.33),
                        (df["ParentalSupport"].mean()/4)*100,
                        ((df["Extracurricular"].mean() + df["Sports"].mean() + df["Music"].mean() + df["Volunteering"].mean())/4)*100,
                        df["Tutoring"].mean()*100,
                    ]
                    fig_radar.add_trace(go.Scatterpolar(
                        r=avg_values+[avg_values[0]], 
                        theta=categories+[categories[0]],
                        fill='toself',
                        fillcolor='rgba(249,115,22,0.1)',
                        line=dict(color='#f59e0b', width=2, dash='dash'),
                        marker=dict(color='#f59e0b', size=6),
                        name='Dataset Average'
                    ))
                
                fig_radar.update_layout(
                    **plotly_theme(st.session_state.dark_mode), 
                    title="Performance Profile Comparison",
                    polar=dict(
                        bgcolor="rgba(0,0,0,0)",
                        radialaxis=dict(
                            visible=True, 
                            range=[0,100], 
                            gridcolor="rgba(124,58,237,0.15)",
                            tickfont=dict(size=10, color='#94a3b8')
                        ),
                        angularaxis=dict(
                            gridcolor="rgba(124,58,237,0.15)",
                            tickfont=dict(size=11, color='#e2e8f0')
                        ),
                    ), 
                    height=380,
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.15,
                        xanchor="center",
                        x=0.5,
                        font=dict(size=10, color='#94a3b8')
                    )
                )
                st.plotly_chart(fig_radar, use_container_width=True)
            
            with analysis_col2:
                # Feature contribution analysis
                with st.container(border=True):
                    st.markdown("**🔍 Key Performance Factors**")
                    
                    # Calculate feature impacts (simplified)
                    factors = [
                        ("Study Time", study_time/20*100, "📚"),
                        ("Attendance", max(0, 100-absences*3.33), "✅"),
                        ("Parental Support", par_support/4*100, "👨‍👩‍👧"),
                        ("Activities", activities/4*100, "🏃"),
                        ("Tutoring", 100 if tutoring else 0, "🧑‍🏫"),
                    ]
                    
                    for name, score, icon in factors:
                        color = "#4ade80" if score >= 75 else "#facc15" if score >= 50 else "#f87171"
                        st.markdown(f"""
                        <div style="margin:0.6rem 0;">
                            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                                <span style="font-size:0.85rem;color:#e2e8f0;">{icon} {name}</span>
                                <span style="font-size:0.85rem;font-weight:700;color:{color};">{score:.0f}%</span>
                            </div>
                            <div style="height:8px;background:rgba(255,255,255,0.05);border-radius:4px;overflow:hidden;">
                                <div style="height:100%;width:{score}%;background:{color};border-radius:4px;transition:width 0.8s;"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Risk factors and recommendations
                with st.container(border=True):
                    st.markdown("**⚠️ Risk Assessment**")
                    if risk_factors:
                        for risk in risk_factors:
                            st.markdown(f"<div style='padding:0.4rem 0.6rem;margin:0.3rem 0;background:rgba(239,68,68,0.1);border-left:3px solid #f87171;border-radius:4px;font-size:0.82rem;color:#fca5a5;'>⚠️ {risk}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='padding:0.6rem;background:rgba(34,197,94,0.1);border-left:3px solid #4ade80;border-radius:4px;font-size:0.85rem;color:#86efac;'>✅ No significant risk factors identified</div>", unsafe_allow_html=True)
                
                # Recommendations
                with st.container(border=True):
                    st.markdown("**💡 Recommendations**")
                    recommendations = []
                    if study_time < 10:
                        recommendations.append("📚 Increase weekly study hours to 10-15h")
                    if absences > 5:
                        recommendations.append("✅ Improve attendance (target <5 absences)")
                    if not tutoring and gpa < 7:
                        recommendations.append("🧑‍🏫 Consider tutoring support")
                    if activities < 2:
                        recommendations.append("🏃 Join extracurricular activities")
                    if par_support < 3:
                        recommendations.append("👨‍👩‍👧 Seek more parental involvement")
                    
                    if recommendations:
                        for rec in recommendations:
                            st.markdown(f"<div style='padding:0.4rem 0.6rem;margin:0.3rem 0;background:rgba(59,130,246,0.1);border-left:3px solid #60a5fa;border-radius:4px;font-size:0.82rem;color:#93c5fd;'>{rec}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='padding:0.6rem;background:rgba(34,197,94,0.1);border-left:3px solid #4ade80;border-radius:4px;font-size:0.85rem;color:#86efac;'>🎉 Excellent profile! Keep up the great work!</div>", unsafe_allow_html=True)

            # Save to history
            st.session_state.history.append({
                "GPA": round(gpa,2), "Grade": letter, "Study Time": study_time,
                "Absences": absences, "Parental Support": par_support,
                "Activities": activities, "Risk Factors": risk_count,
                "Percentile": round(percentile_rank, 1) if percentile_rank > 0 else 0
            })
            
            # Show prediction history
            if len(st.session_state.history) > 1:
                st.markdown('<div class="sec-head">📜 Prediction History</div>', unsafe_allow_html=True)
                history_df = pd.DataFrame(st.session_state.history)
                st.dataframe(history_df, use_container_width=True, hide_index=True)


# ─── TAB 2 · DATA EXPLORER ────────────────────────────────────────────────────
with tab2:
    if df is None:
        st.info("📂 No dataset loaded. Please place the CSV in the dataset/ folder.")
    else:
        st.markdown('<div class="sec-head">📊 Dataset Overview</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="kpi-wrap">
            <div class="kpi"><div class="kpi-icon">👥</div><div class="kpi-val">{len(df):,}</div><div class="kpi-lbl">Students</div></div>
            <div class="kpi"><div class="kpi-icon">📋</div><div class="kpi-val">{len(df.columns)}</div><div class="kpi-lbl">Columns</div></div>
            <div class="kpi"><div class="kpi-icon">🎓</div><div class="kpi-val">{df['GPA'].mean():.2f}</div><div class="kpi-lbl">Avg GPA</div></div>
            <div class="kpi"><div class="kpi-icon">⚠️</div><div class="kpi-val">{df.isnull().sum().sum()}</div><div class="kpi-lbl">Missing</div></div>
        </div>""", unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        with c1:
            st.markdown('<div class="sec-head">📈 GPA Distribution</div>', unsafe_allow_html=True)
            fig_hist = px.histogram(df, x="GPA", nbins=40, color_discrete_sequence=["#7c3aed"])
            fig_hist.update_layout(**plotly_theme(st.session_state.dark_mode), height=300, bargap=0.05)
            apply_axes_style(fig_hist, st.session_state.dark_mode)
            fig_hist.update_traces(marker_line_color="rgba(0,0,0,0.3)", marker_line_width=0.5)
            st.plotly_chart(fig_hist, use_container_width=True)

        with c2:
            st.markdown('<div class="sec-head">🎯 Grade Distribution</div>', unsafe_allow_html=True)
            grade_counts = df["GradeClass"].value_counts().reset_index()
            grade_counts.columns = ["GradeClass","Count"]
            grade_map = {0.0:"A",1.0:"B",2.0:"C",3.0:"D",4.0:"F"}
            grade_counts["Label"] = grade_counts["GradeClass"].map(grade_map)
            fig_pie = px.pie(grade_counts, values="Count", names="Label",
                color_discrete_sequence=["#7c3aed","#3b82f6","#06b6d4","#f59e0b","#ef4444"])
            fig_pie.update_layout(**plotly_theme(st.session_state.dark_mode), height=300)
            fig_pie.update_traces(textfont_size=12, hole=0.45)
            st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown('<div class="sec-head">🔥 Study Time vs GPA</div>', unsafe_allow_html=True)
        fig_scatter = px.scatter(df, x="StudyTimeWeekly", y="GPA", color="GPA",
            color_continuous_scale=["#1e1b4b","#7c3aed","#a78bfa","#ddd6fe"],
            opacity=0.7, size_max=6)
        fig_scatter.update_layout(**plotly_theme(st.session_state.dark_mode), height=340,
            xaxis_title="Weekly Study Hours", yaxis_title="GPA",
            coloraxis_showscale=False)
        apply_axes_style(fig_scatter, st.session_state.dark_mode)
        st.plotly_chart(fig_scatter, use_container_width=True)

        st.markdown('<div class="sec-head">🔗 Correlation Matrix</div>', unsafe_allow_html=True)
        num_cols = ["Age","StudyTimeWeekly","Absences","Tutoring","ParentalSupport",
                    "Extracurricular","Sports","Music","Volunteering","GPA"]
        corr = df[num_cols].corr().round(2)
        fig_heat = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r",
            zmin=-1, zmax=1, aspect="auto")
        fig_heat.update_layout(**plotly_theme(st.session_state.dark_mode), height=420)
        apply_axes_style(fig_heat, st.session_state.dark_mode)
        fig_heat.update_traces(textfont_size=9)
        st.plotly_chart(fig_heat, use_container_width=True)

        st.markdown('<div class="sec-head">🗃️ Raw Data Preview</div>', unsafe_allow_html=True)
        st.dataframe(df.head(30), use_container_width=True, height=320)


# ─── TAB 3 · MODEL PERFORMANCE ────────────────────────────────────────────────
with tab3:
    meta = st.session_state.metadata
    if meta is None:
        st.info("🏋️ No model metadata found. Run `python train_new_dataset.py` first.")
    else:
        metrics = meta.get("metrics", {})
        best    = meta.get("best_model","-")

        st.markdown('<div class="sec-head">🏆 Best Model Performance</div>', unsafe_allow_html=True)
        bm = metrics.get(best, {})
        st.markdown(f"""
        <div class="kpi-wrap kpi3">
            <div class="kpi"><div class="kpi-icon">📐</div><div class="kpi-val">{bm.get('r2_score','-')}</div><div class="kpi-lbl">R² Score</div></div>
            <div class="kpi"><div class="kpi-icon">📉</div><div class="kpi-val">{bm.get('mae','-')}</div><div class="kpi-lbl">MAE</div></div>
            <div class="kpi"><div class="kpi-icon">📏</div><div class="kpi-val">{bm.get('rmse','-')}</div><div class="kpi-lbl">RMSE</div></div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f'<div style="text-align:center;margin:-0.5rem 0 1.2rem;font-size:0.85rem;color:#64748b;">🏅 Best model: <strong style="color:#a78bfa">{best}</strong></div>', unsafe_allow_html=True)

        st.markdown('<div class="sec-head">📊 Model Comparison</div>', unsafe_allow_html=True)

        names = list(metrics.keys())
        r2s   = [metrics[n]["r2_score"] for n in names]
        maes  = [metrics[n]["mae"]       for n in names]
        rmses = [metrics[n]["rmse"]      for n in names]

        colors = ["#7c3aed" if n==best else "#334155" for n in names]

        c1, c2 = st.columns(2)
        with c1:
            fig_r2 = go.Figure(go.Bar(x=names, y=r2s, marker_color=colors,
                text=[f"{v:.4f}" for v in r2s], textposition="outside",
                textfont=dict(color="#e2e8f0",size=11)))
            fig_r2.update_layout(**plotly_theme(st.session_state.dark_mode), height=300,
                title="R2 Score (Higher = Better)")
            apply_axes_style(fig_r2, st.session_state.dark_mode)
            fig_r2.update_yaxes(range=[0,1.05])
            st.plotly_chart(fig_r2, use_container_width=True)

        with c2:
            fig_mae = go.Figure(go.Bar(x=names, y=maes, marker_color=colors,
                text=[f"{v:.4f}" for v in maes], textposition="outside",
                textfont=dict(color="#e2e8f0",size=11)))
            fig_mae.update_layout(**plotly_theme(st.session_state.dark_mode), height=300,
                title="MAE (Lower = Better)")
            apply_axes_style(fig_mae, st.session_state.dark_mode)
            st.plotly_chart(fig_mae, use_container_width=True)

        st.markdown('<div class="sec-head">📋 Detailed Metrics Table</div>', unsafe_allow_html=True)
        rows = []
        for n in names:
            m = metrics[n]
            rows.append({"Model": ("🏆 " if n==best else "   ") + n,
                         "R² Score": m["r2_score"], "MAE": m["mae"], "RMSE": m["rmse"],
                         "Accuracy": f"{m['r2_score']*100:.2f}%"})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        # Gauge for best model
        st.markdown('<div class="sec-head">🎯 Accuracy Gauge</div>', unsafe_allow_html=True)
        r2_pct = bm.get("r2_score", 0.95) * 100
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=r2_pct,
            delta={"reference": 90, "suffix":"%"},
            number={"suffix":"%", "font":{"size":42,"color":"#a78bfa","family":"Inter"}},
            gauge={
                "axis":{"range":[0,100], "tickfont":{"color":"#64748b"}, "tickcolor":"#334155"},
                "bar":{"color":"#7c3aed", "thickness":0.25},
                "bgcolor":"rgba(0,0,0,0)",
                "bordercolor":"rgba(0,0,0,0)",
                "steps":[
                    {"range":[0,60],  "color":"rgba(239,68,68,0.1)"},
                    {"range":[60,80], "color":"rgba(234,179,8,0.1)"},
                    {"range":[80,100],"color":"rgba(34,197,94,0.1)"},
                ],
                "threshold":{"line":{"color":"#4ade80","width":3},"value":90},
            },
            title={"text": f"<b>{best}</b> - Model Accuracy", "font":{"color":"#94a3b8","size":14}},
        ))
        fig_gauge.update_layout(**plotly_theme(), height=320)
        st.plotly_chart(fig_gauge, use_container_width=True)


# ─── TAB 4 · ABOUT ────────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="sec-head">ℹ️ About This Project</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
<div class="g-card">
<h4 style="color:#a78bfa;margin-top:0">🧠 How It Works</h4>
<p style="color:#94a3b8;font-size:0.88rem;line-height:1.7;">
The system uses <strong>12 student features</strong> - demographics, study habits, and extracurricular activities - to predict GPA using machine learning.<br><br>
Three regression models compete; the best one (by R² score) is saved and used for all predictions.
</p>
</div>""", unsafe_allow_html=True)

        st.markdown("""
<div class="g-card">
<h4 style="color:#a78bfa;margin-top:0">📊 Input Features</h4>
<table style="width:100%;font-size:0.82rem;color:#94a3b8;border-collapse:collapse;">
<tr style="border-bottom:1px solid rgba(255,255,255,0.06)"><th style="text-align:left;padding:4px 8px;color:#e2e8f0">Feature</th><th style="padding:4px 8px;color:#e2e8f0">Type</th></tr>
<tr><td style="padding:3px 8px">Age</td><td style="padding:3px 8px">Numerical</td></tr>
<tr><td style="padding:3px 8px">Gender</td><td style="padding:3px 8px">Binary</td></tr>
<tr><td style="padding:3px 8px">Ethnicity</td><td style="padding:3px 8px">Categorical</td></tr>
<tr><td style="padding:3px 8px">Parental Education</td><td style="padding:3px 8px">Ordinal</td></tr>
<tr><td style="padding:3px 8px">Study Time Weekly</td><td style="padding:3px 8px">Numerical</td></tr>
<tr><td style="padding:3px 8px">Absences</td><td style="padding:3px 8px">Numerical</td></tr>
<tr><td style="padding:3px 8px">Tutoring / Support</td><td style="padding:3px 8px">Binary</td></tr>
<tr><td style="padding:3px 8px">Sports / Music / Volunteer</td><td style="padding:3px 8px">Binary</td></tr>
</table>
</div>""", unsafe_allow_html=True)

    with c2:
        st.markdown("""
<div class="g-card">
<h4 style="color:#a78bfa;margin-top:0">🤖 ML Models</h4>
<div style="font-size:0.85rem;color:#94a3b8;line-height:2;">
<div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.05);padding:4px 0;">
  <span>📐 Linear Regression</span><span style="color:#4ade80">R² 95.32%</span>
</div>
<div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.05);padding:4px 0;">
  <span>🌲 Decision Tree</span><span style="color:#facc15">R² 87.08%</span>
</div>
<div style="display:flex;justify-content:space-between;padding:4px 0;">
  <span>🌳 Random Forest</span><span style="color:#60a5fa">R² 92.69%</span>
</div>
</div>
</div>""", unsafe_allow_html=True)

        st.markdown("""
<div class="g-card">
<h4 style="color:#a78bfa;margin-top:0">🛠️ Tech Stack</h4>
<div style="font-size:0.82rem;color:#94a3b8;line-height:2.1;">
🐍 &nbsp;<strong style="color:#e2e8f0">Python 3.10+</strong> - Core language<br>
🎈 &nbsp;<strong style="color:#e2e8f0">Streamlit</strong> - UI framework<br>
🤖 &nbsp;<strong style="color:#e2e8f0">Scikit-learn</strong> - ML models<br>
📊 &nbsp;<strong style="color:#e2e8f0">Plotly</strong> - Interactive charts<br>
🐼 &nbsp;<strong style="color:#e2e8f0">Pandas / NumPy</strong> - Data processing<br>
💾 &nbsp;<strong style="color:#e2e8f0">Joblib</strong> - Model persistence
</div>
</div>""", unsafe_allow_html=True)

    st.markdown('<div style="text-align:center;margin-top:2rem;color:#1e293b;font-size:0.75rem;">Student Performance Predictor · v2.0 · Built with ❤️</div>', unsafe_allow_html=True)
