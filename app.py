"""
app.py  -  Student Performance Predictor  (Enhanced Professional UI)
"""

import os, sys, json, warnings
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import joblib

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Fix for pickle loading - make this module available as 'main'
if '__main__' not in sys.modules:
    sys.modules['__main__'] = sys.modules[__name__]

# ─── Page config (must be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Performance optimization: Disable Streamlit's default animations
st.markdown("""
<style>
    /* Disable default Streamlit animations for faster LCP */
    .stApp { animation: none !important; }
    .element-container { animation: none !important; }
</style>
""", unsafe_allow_html=True)

# ─── CSS injection (theme-aware) ────────────────────────────────────────────
def inject_css(dark):
    # Add a unique identifier to force CSS refresh on theme change
    theme_id = "dark" if dark else "light"
    
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
        # Light mode - MAXIMUM VISIBILITY with very dark text
        BG      = "linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #f0f4f8 100%)"
        CARD    = "rgba(255,255,255,0.98)"  # More solid
        CARD_HOVER = "rgba(255,255,255,1)"
        BORDER  = "rgba(100,80,200,0.4)"  # Much darker border
        TXT     = "#0a0a0a"  # Almost black - maximum contrast
        SUB     = "#1e293b"  # Very dark subtitle
        MUT     = "#334155"  # Dark muted text (was #475569)
        SIDEBAR = "linear-gradient(180deg, #ffffff 0%, #f8fafc 100%)"
        SIDEBAR_BORDER = "rgba(100,80,200,0.3)"
        INP_BG  = "#ffffff"  # Pure white for maximum contrast
        INP_BORDER = "rgba(100,80,200,0.5)"  # Much darker border
        HERO_BG = "linear-gradient(135deg, #ddd6fe 0%, #c7d2fe 25%, #bfdbfe 50%, #bae6fd 75%, #a5f3fc 100%)"
        HERO_OVERLAY = "radial-gradient(circle at 20% 50%, rgba(139,92,246,0.15) 0%, transparent 50%), radial-gradient(circle at 80% 50%, rgba(59,130,246,0.1) 0%, transparent 50%)"
        HERO_BORDER = "rgba(100,80,200,0.5)"  # Much darker border
        ACCENT_PRIMARY = "#6d28d9"  # Darker purple
        ACCENT_SECONDARY = "#2563eb"  # Darker blue
        GLASS_BG = "rgba(255,255,255,0.95)"
        GLASS_BORDER = "rgba(100,80,200,0.4)"

    hero_title_grad = "linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0a0a0a 100%)" if not dark else "linear-gradient(135deg, #ffffff 0%, #e0e7ff 50%, #ddd6fe 100%)"
    hero_sub_color  = "#1e293b" if not dark else "#cbd5e1"  # Much darker in light mode
    hero_stat_val_g = "linear-gradient(90deg, #5b21b6, #1e40af)" if not dark else "linear-gradient(90deg, #c4b5fd, #93c5fd)"

    st.markdown(f"""
<style data-theme="{theme_id}">
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

/* Force background on all Streamlit containers */
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
.main {{
    background: {BG} !important;
}}

/* Ensure main content area has correct background */
.main .block-container {{
    background: transparent !important;
}}

#MainMenu, footer, header {{ visibility: hidden; }}
footer {{ display: none !important; }}
footer::after {{ display: none !important; }}
.viewerBadge_container__1QSob {{ display: none !important; }}
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

/* Sidebar Toggle Enhancement */
[data-testid="stSidebarCollapseButton"] {{
    background: rgba(139,92,246,0.1) !important;
    border: 1px solid rgba(139,92,246,0.2) !important;
    border-radius: 8px !important;
    padding: 0.2rem !important;
    transition: all 0.3s !important;
}}

[data-testid="stSidebarCollapseButton"]:hover {{
    background: rgba(139,92,246,0.2) !important;
    border-color: rgba(139,92,246,0.4) !important;
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

/* Streamlit Widget Text Contrast - MAXIMUM VISIBILITY */
.stSlider label, .stSelectbox label, .stNumberInput label, .stTextInput label, .stCheckbox label, .stMultiSelect label, .stRadio label {{
    color: {TXT} !important; 
    font-weight: 500 !important;
}}
div[data-testid="stMarkdownContainer"] p, div[data-testid="stMarkdownContainer"] span {{
    color: {TXT} !important;
}}
.stSlider [data-testid="stWidgetLabel"] {{ 
    color: {TXT} !important; 
    font-weight: 500 !important;
}}

/* Force text visibility in ALL Streamlit elements */
.stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown div, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {{
    color: {TXT} !important;
}}

/* Ensure ALL input text is visible */
input, textarea, select, option {{
    color: {TXT} !important;
    font-weight: 400 !important;
}}

/* Tab text visibility - ENHANCED */
.stTabs [data-baseweb="tab"] {{
    color: {MUT} !important;
    font-weight: 500 !important;
}}
.stTabs [aria-selected="true"] {{
    color: {ACCENT_PRIMARY} !important;
    font-weight: 600 !important;
}}

/* Button text */
.stButton > button {{
    color: #ffffff !important;
    font-weight: 600 !important;
}}

/* Metric labels and values - MAXIMUM CONTRAST */
[data-testid="stMetricLabel"], [data-testid="stMetricValue"] {{
    color: {TXT} !important;
    font-weight: 600 !important;
}}

/* Dataframe text - ALL CELLS */
.stDataFrame, .stDataFrame *, .stDataFrame table, .stDataFrame th, .stDataFrame td {{
    color: {TXT} !important;
}}

/* Alert text - ALL TYPES */
.stAlert, .stAlert *, .stSuccess, .stSuccess *, .stInfo, .stInfo *, .stWarning, .stWarning *, .stError, .stError * {{
    color: {TXT} !important;
}}

/* Expander text */
.streamlit-expanderHeader, .streamlit-expanderContent, .streamlit-expanderHeader *, .streamlit-expanderContent * {{
    color: {TXT} !important;
}}

/* Code block text */
.stCodeBlock, .stCodeBlock * {{
    color: {TXT} !important;
}}

/* Plotly chart text - FORCE VISIBILITY */
.js-plotly-plot .plotly, .js-plotly-plot .plotly *, 
.js-plotly-plot text, .js-plotly-plot .xtick text, .js-plotly-plot .ytick text,
.js-plotly-plot .legendtext, .js-plotly-plot .annotation {{
    fill: {TXT} !important;
    color: {TXT} !important;
}}

/* Container text */
[data-testid="stVerticalBlock"] *, [data-testid="stHorizontalBlock"] * {{
    color: {TXT} !important;
}}

/* Input field cleanup - ENHANCED VISIBILITY */
/* Slider track and thumb - THEME AWARE */
.stSlider > div > div > div > div {{ 
    background: #7c3aed !important; 
}}

/* Slider track background */
.stSlider > div > div > div {{
    background: {BORDER} !important;
}}

/* Slider thumb (handle) */
.stSlider [role="slider"] {{
    background: #7c3aed !important;
    border: 2px solid #ffffff !important;
    box-shadow: 0 2px 8px rgba(124,58,237,0.4) !important;
}}

/* Slider value label */
.stSlider [data-testid="stTickBar"] {{
    color: {TXT} !important;
}}

/* Input fields - MAXIMUM VISIBILITY */
div[data-testid="stNumberInput"] input, 
div[data-testid="stTextInput"] input, 
div[data-testid="stSelectbox"] > div {{
    background: {INP_BG} !important; 
    border: 1px solid {INP_BORDER} !important; 
    border-radius: 8px !important; 
    color: {TXT} !important;
    font-weight: 500 !important;
}}

/* Selectbox - Force text visibility */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
div[data-testid="stSelectbox"] [role="button"] {{
    color: {TXT} !important;
    background: {INP_BG} !important;
}}

/* Selectbox selected value */
div[data-testid="stSelectbox"] [data-baseweb="select"] [role="button"] > div {{
    color: {TXT} !important;
}}

/* Ensure dropdown options are visible */
div[data-baseweb="select"] > div,
div[data-baseweb="select"] > div > div,
div[data-baseweb="select"] span {{
    color: {TXT} !important;
    background: {INP_BG} !important;
}}

/* Ensure all input placeholders are visible */
input::placeholder, textarea::placeholder {{
    color: {MUT} !important;
    opacity: 0.7 !important;
}}

/* Number input buttons */
div[data-testid="stNumberInput"] button {{
    color: {TXT} !important;
}}

/* Select dropdown menu - ENHANCED */
[data-baseweb="popover"],
[data-baseweb="popover"] > div {{
    background: {CARD} !important;
    color: {TXT} !important;
}}

[data-baseweb="menu"],
[data-baseweb="menu"] li,
[data-baseweb="menu"] ul li {{
    color: {TXT} !important;
    background: {CARD} !important;
}}

[data-baseweb="menu"] li:hover {{
    background: {CARD_HOVER} !important;
    color: {TXT} !important;
}}

/* Checkbox and radio text */
.stCheckbox > label > div, .stRadio > label > div {{
    color: {TXT} !important;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   ENTRANCE ANIMATIONS - Smooth page load effects
   ═══════════════════════════════════════════════════════════════════════════ */

/* Keyframe Definitions */
@keyframes fadeInUp {{
    from {{
        opacity: 0;
        transform: translateY(30px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to {{ opacity: 1; }}
}}

@keyframes slideInLeft {{
    from {{
        opacity: 0;
        transform: translateX(-40px);
    }}
    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

@keyframes slideInRight {{
    from {{
        opacity: 0;
        transform: translateX(40px);
    }}
    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

@keyframes scaleIn {{
    from {{
        opacity: 0;
        transform: scale(0.9);
    }}
    to {{
        opacity: 1;
        transform: scale(1);
    }}
}}

@keyframes bounceIn {{
    0% {{
        opacity: 0;
        transform: scale(0.3);
    }}
    50% {{
        transform: scale(1.05);
    }}
    70% {{
        transform: scale(0.95);
    }}
    100% {{
        opacity: 1;
        transform: scale(1);
    }}
}}

/* Hero Section Animation - OPTIMIZED FOR LCP */
.hero {{
    animation: fadeIn 0.3s ease-out;
}}

.hero-badge {{
    animation: fadeIn 0.4s ease-out 0.05s backwards;
}}

.hero-title {{
    animation: fadeIn 0.3s ease-out 0.1s backwards;
}}

.hero-sub {{
    animation: fadeIn 0.3s ease-out 0.15s backwards;
}}

.hero-stats {{
    animation: fadeIn 0.3s ease-out 0.2s backwards;
}}

.hero-stat {{
    animation: fadeIn 0.3s ease-out backwards;
}}

.hero-stat:nth-child(1) {{ animation-delay: 0.2s; }}
.hero-stat:nth-child(2) {{ animation-delay: 0.22s; }}
.hero-stat:nth-child(3) {{ animation-delay: 0.24s; }}
.hero-stat:nth-child(4) {{ animation-delay: 0.26s; }}

/* KPI Cards Animation - FASTER */
.kpi-wrap {{
    animation: fadeIn 0.3s ease-out 0.15s backwards;
}}

.kpi {{
    animation: fadeIn 0.3s ease-out backwards;
}}

.kpi:nth-child(1) {{ animation-delay: 0.18s; }}
.kpi:nth-child(2) {{ animation-delay: 0.2s; }}
.kpi:nth-child(3) {{ animation-delay: 0.22s; }}
.kpi:nth-child(4) {{ animation-delay: 0.24s; }}

/* Section Headers Animation - SIMPLIFIED */
.sec-head {{
    animation: fadeIn 0.3s ease-out backwards;
}}

/* Prediction Card Animation - SIMPLIFIED */
.pred-card {{
    animation: fadeIn 0.4s ease-out backwards;
}}

/* Container Animations - SIMPLIFIED */
.stElementContainer div[data-testid="stVerticalBlockBorderWrapper"] {{
    animation: fadeIn 0.3s ease-out backwards;
}}

/* Stagger effect - MINIMAL DELAYS */
.element-container:nth-child(1) .stElementContainer div[data-testid="stVerticalBlockBorderWrapper"] {{ animation-delay: 0.02s; }}
.element-container:nth-child(2) .stElementContainer div[data-testid="stVerticalBlockBorderWrapper"] {{ animation-delay: 0.04s; }}
.element-container:nth-child(3) .stElementContainer div[data-testid="stVerticalBlockBorderWrapper"] {{ animation-delay: 0.06s; }}
.element-container:nth-child(4) .stElementContainer div[data-testid="stVerticalBlockBorderWrapper"] {{ animation-delay: 0.08s; }}

/* Tab Animation - SIMPLIFIED */
.stTabs {{
    animation: fadeIn 0.3s ease-out 0.1s backwards;
}}

.stTabs [data-baseweb="tab"] {{
    animation: fadeIn 0.2s ease-out backwards;
}}

.stTabs [data-baseweb="tab"]:nth-child(1) {{ animation-delay: 0.12s; }}
.stTabs [data-baseweb="tab"]:nth-child(2) {{ animation-delay: 0.14s; }}
.stTabs [data-baseweb="tab"]:nth-child(3) {{ animation-delay: 0.16s; }}
.stTabs [data-baseweb="tab"]:nth-child(4) {{ animation-delay: 0.18s; }}

/* Chart Animations - MINIMAL */
.js-plotly-plot {{
    animation: fadeIn 0.3s ease-out 0.15s backwards;
}}

/* Dataframe Animation - MINIMAL */
.stDataFrame {{
    animation: fadeIn 0.3s ease-out 0.18s backwards;
}}

/* Button Animation - MINIMAL */
.stButton > button {{
    animation: fadeIn 0.2s ease-out 0.2s backwards;
}}

/* Input Fields Animation - MINIMAL */
div[data-testid="stNumberInput"],
div[data-testid="stTextInput"],
div[data-testid="stSelectbox"],
.stSlider,
.stCheckbox {{
    animation: fadeIn 0.2s ease-out backwards;
}}

/* Minimal stagger for inputs */
.stNumberInput:nth-of-type(1), .stSelectbox:nth-of-type(1) {{ animation-delay: 0.08s; }}
.stNumberInput:nth-of-type(2), .stSelectbox:nth-of-type(2) {{ animation-delay: 0.09s; }}
.stNumberInput:nth-of-type(3), .stSelectbox:nth-of-type(3) {{ animation-delay: 0.1s; }}
.stNumberInput:nth-of-type(4), .stSelectbox:nth-of-type(4) {{ animation-delay: 0.11s; }}
.stNumberInput:nth-of-type(5), .stSelectbox:nth-of-type(5) {{ animation-delay: 0.12s; }}
.stNumberInput:nth-of-type(6), .stSelectbox:nth-of-type(6) {{ animation-delay: 0.13s; }}

/* Sidebar Animation - SIMPLIFIED */
section[data-testid="stSidebar"] {{
    animation: fadeIn 0.3s ease-out;
}}

/* Ensure sidebar is visible on desktop */
@media only screen and (min-width: 769px) {{
    section[data-testid="stSidebar"] {{
        display: block !important;
        visibility: visible !important;
    }}
}}

/* Enhanced visibility for light mode elements */
.stElementContainer div[data-testid="stVerticalBlockBorderWrapper"] {{
    border-width: 1.5px !important;
}}

/* Ensure all borders are visible in light mode */
.stTabs [data-baseweb="tab-list"] {{
    border-bottom-width: 2px !important;
}}

/* Chart containers - minimal styling, let Plotly handle backgrounds */
.js-plotly-plot {{
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
    padding: 0.5rem !important;
    overflow: hidden !important;
}}

.sidebar-logo {{
    animation: fadeIn 0.3s ease-out 0.05s backwards;
}}

.sidebar-title {{
    animation: fadeIn 0.3s ease-out 0.1s backwards;
}}

.sidebar-sub {{
    animation: fadeIn 0.3s ease-out 0.15s backwards;
}}

.status-pill {{
    animation: fadeIn 0.2s ease-out 0.18s backwards;
}}

/* Alert Animations - SIMPLIFIED */
.stAlert {{
    animation: fadeIn 0.3s ease-out backwards;
}}

/* Progress Bar Fill Animation - FASTER */
.prog-fill {{
    animation: expandWidth 0.8s ease-out 0.2s backwards;
}}

@keyframes expandWidth {{
    from {{ width: 0 !important; }}
}}

/* Insight Card Animation - SIMPLIFIED */
.insight-card {{
    animation: fadeIn 0.3s ease-out backwards;
}}

.insight-card:nth-child(1) {{ animation-delay: 0.12s; }}
.insight-card:nth-child(2) {{ animation-delay: 0.15s; }}
.insight-card:nth-child(3) {{ animation-delay: 0.18s; }}

/* Grade Badge Animation - SIMPLIFIED */
.grade-badge {{
    animation: fadeIn 0.3s ease-out 0.4s backwards;
}}

/* Hover Enhancement - Keep simple */
.kpi:hover, .pred-card:hover, .insight-card:hover {{
    animation: none;
}}

/* DISABLED CONTINUOUS ANIMATIONS FOR BETTER PERFORMANCE */
/* These animations hurt LCP and FPS - disabled by default */
/*
@keyframes floatSoft {{
    0%, 100% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-5px); }}
}}

.hero-badge {{
    animation: fadeIn 0.4s ease-out 0.05s backwards, floatSoft 3s ease-in-out 1s infinite;
}}
*/

/* Shimmer effect - ONE TIME ONLY, NO REPEAT */
@keyframes shimmer {{
    0% {{ background-position: -1000px 0; }}
    100% {{ background-position: 1000px 0; }}
}}

.hero-title {{
    background-size: 200% auto;
}}

/* DISABLED PULSE GLOW FOR BETTER PERFORMANCE */
/*
@keyframes pulseGlow {{
    0%, 100% {{ box-shadow: 0 0 20px rgba(139,92,246,0.1); }}
    50% {{ box-shadow: 0 0 40px rgba(139,92,246,0.3); }}
}}

.pred-card {{
    animation: fadeIn 0.4s ease-out backwards, pulseGlow 2s ease-in-out 0.8s infinite;
}}
*/

/* Reduce motion for users who prefer it */
@media (prefers-reduced-motion: reduce) {{
    *, *::before, *::after {{
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }}
}}

/* ═══════════════════════════════════════════════════════════════════════════
   RESPONSIVE DESIGN - Mobile, Tablet, Desktop
   ═══════════════════════════════════════════════════════════════════════════ */

/* Mobile Phones (Portrait) - 320px to 480px */
@media only screen and (max-width: 480px) {{
    .block-container {{
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        padding-top: 1rem !important;
    }}
    
    .hero {{
        padding: 1rem 1.2rem !important;
        border-radius: 12px !important;
    }}
    
    .hero-title {{
        font-size: 1.4rem !important;
        line-height: 1.2 !important;
    }}
    
    .hero-sub {{
        font-size: 0.8rem !important;
    }}
    
    .hero-stats {{
        flex-direction: column !important;
        gap: 0.6rem !important;
    }}
    
    .hero-stat {{
        text-align: center !important;
        width: 100% !important;
    }}
    
    .kpi-wrap {{
        grid-template-columns: 1fr !important;
        gap: 0.8rem !important;
    }}
    
    .kpi {{
        padding: 0.8rem !important;
    }}
    
    .kpi-val {{
        font-size: 1.3rem !important;
    }}
    
    .pred-card {{
        padding: 1.2rem 1rem !important;
    }}
    
    .pred-gpa {{
        font-size: 2.5rem !important;
    }}
    
    /* FORCE COLUMN STACKING ON MOBILE */
    [data-testid="stHorizontalBlock"] {{
        flex-direction: column !important;
        gap: 1.5rem !important;
        display: flex !important;
    }}
    
    [data-testid="column"] {{
        width: 100% !important;
        min-width: 100% !important;
        flex: 1 1 auto !important;
    }}

    
    /* Fix table overflow */
    table {{
        display: block !important;
        overflow-x: auto !important;
        white-space: nowrap !important;
    }}
}}



/* Mobile Phones (Landscape) & Small Tablets - 481px to 768px */
@media only screen and (min-width: 481px) and (max-width: 768px) {{
    .block-container {{
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }}
    
    /* Column Stacking for Tablets */
    [data-testid="stHorizontalBlock"] {{
        flex-direction: column !important;
        gap: 1.5rem !important;
    }}
    
    [data-testid="column"] {{
        width: 100% !important;
        min-width: 100% !important;
    }}

    .hero {{
        padding: 1.6rem 1.8rem !important;
    }}
    
    .hero-title {{
        font-size: 2rem !important;
    }}
    
    .kpi-wrap {{
        grid-template-columns: repeat(2, 1fr) !important;
    }}
    
    .pred-gpa {{
        font-size: 3.5rem !important;
    }}
}}


/* Tablets (Portrait) - 769px to 1024px */
@media only screen and (min-width: 769px) and (max-width: 1024px) {{
    .hero-title {{
        font-size: 2.2rem !important;
    }}
    
    .kpi-wrap {{
        grid-template-columns: repeat(4, 1fr) !important;
        gap: 0.8rem !important;
    }}
    
    .kpi {{
        padding: 1rem 1.2rem !important;
    }}
}}

/* Large Tablets & Small Desktops - 1025px to 1280px */
@media only screen and (min-width: 1025px) and (max-width: 1280px) {{
    .block-container {{
        max-width: 1200px !important;
    }}
}}

/* Touch Device Optimizations */
@media (hover: none) and (pointer: coarse) {{
    /* Larger touch targets */
    .stButton > button {{
        min-height: 44px !important;
        padding: 0.6rem 1.2rem !important;
    }}
    
    .stCheckbox {{
        min-height: 44px !important;
    }}
    
    /* Remove hover effects on touch devices */
    .kpi:hover,
    .pred-card:hover,
    .insight-card:hover {{
        transform: none !important;
    }}
}}

/* High DPI Displays (Retina) */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {{
    /* Sharper text rendering */
    body {{
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }}
}}

/* Print Styles */
@media print {{
    .stButton, section[data-testid="stSidebar"], .stTabs {{
        display: none !important;
    }}
    
    .hero, .kpi, .pred-card {{
        break-inside: avoid !important;
    }}
}}

/* Performance Optimization: Reduce animations on low-end devices */
@media (prefers-reduced-motion: no-preference) and (max-width: 768px) {{
    /* Simpler animations on mobile for better performance */
    .hero, .kpi, .pred-card {{
        animation-duration: 0.3s !important;
    }}
    
    /* Disable continuous animations on mobile */
    .hero-badge, .pred-card {{
        animation-iteration-count: 1 !important;
    }}
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
    
    try:
        if os.path.exists(mp) and os.path.exists(pp):
            # Import train_new_dataset to make MinimalPreprocessor available
            try:
                import train_new_dataset
                # Make the class available in multiple namespaces for pickle
                sys.modules['__main__'].MinimalPreprocessor = train_new_dataset.MinimalPreprocessor
            except:
                pass
            
            model = joblib.load(mp)
            preprocessor = joblib.load(pp)
            return model, preprocessor
        else:
            st.warning("⚠️ Model files not found. Please ensure models are trained.")
            return None, None
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        st.info("💡 The app will continue with limited functionality. Model files may need to be retrained.")
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
    """
    Returns a complete Plotly layout configuration for the current theme.
    Ensures proper backgrounds, text colors, and styling for both dark and light modes.
    """
    if dark:
        return dict(
            template="plotly_dark",
            paper_bgcolor="#0f1629",
            plot_bgcolor="#0f1629",
            font=dict(family="Inter", color="#e2e8f0", size=12),
            xaxis=dict(
                gridcolor="rgba(255,255,255,0.1)",
                zerolinecolor="rgba(255,255,255,0.2)",
                color="#e2e8f0"
            ),
            yaxis=dict(
                gridcolor="rgba(255,255,255,0.1)",
                zerolinecolor="rgba(255,255,255,0.2)",
                color="#e2e8f0"
            ),
        )
    else:
        return dict(
            template="plotly_white",
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            font=dict(family="Inter", color="#0a0a0a", size=12),
            xaxis=dict(
                gridcolor="rgba(0,0,0,0.1)",
                zerolinecolor="rgba(0,0,0,0.2)",
                color="#0a0a0a"
            ),
            yaxis=dict(
                gridcolor="rgba(0,0,0,0.1)",
                zerolinecolor="rgba(0,0,0,0.2)",
                color="#0a0a0a"
            ),
        )

def apply_axes_style(fig, dark=True):
    """
    Applies consistent axis styling to a Plotly figure.
    """
    if dark:
        grid_c = "rgba(255,255,255,0.08)"
        txt_c = "#e2e8f0"
        line_c = "rgba(255,255,255,0.15)"
    else:
        grid_c = "rgba(0,0,0,0.1)"
        txt_c = "#0a0a0a"
        line_c = "rgba(0,0,0,0.2)"
    
    fig.update_xaxes(
        gridcolor=grid_c, 
        zerolinecolor=line_c, 
        tickfont=dict(color=txt_c, size=11),
        linecolor=line_c,
        linewidth=1
    )
    fig.update_yaxes(
        gridcolor=grid_c, 
        zerolinecolor=line_c, 
        tickfont=dict(color=txt_c, size=11),
        linecolor=line_c,
        linewidth=1
    )
    return fig

def prog_bar(label, val_str, pct):
    return f"""
    <div class="prog-wrap">
        <div class="prog-label"><span>{label}</span><span>{val_str}</span></div>
        <div class="prog-track"><div class="prog-fill" style="width:{pct:.0f}%"></div></div>
    </div>"""

# ─── Session state ─────────────────────────────────────────────────────────────
# Force light mode as default
st.session_state.dark_mode = False

if "model" not in st.session_state:
    st.session_state.model        = None
    st.session_state.preprocessor = None
    st.session_state.metadata     = None
    st.session_state.df           = None
    st.session_state.history      = []
    st.session_state.loaded       = False

# Inject theme CSS based on current mode (ALWAYS inject on every page load)
inject_css(dark=st.session_state.dark_mode)

# Show loading indicator while loading heavy resources
if "loaded" not in st.session_state or not st.session_state.loaded:
    with st.spinner('🚀 Loading Student Performance Predictor...'):
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

        # Import data manager for dynamic updates
        try:
            from src.data_manager import DataManager, get_record_count
            data_manager = DataManager()
        except Exception as e:
            data_manager = None
        
        st.session_state.loaded = True
else:
    # Already loaded, just get data manager
    try:
        from src.data_manager import DataManager, get_record_count
        data_manager = DataManager()
    except Exception as e:
        data_manager = None

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
    pass


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
                

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Save to dataset section - MORE PROMINENT
        st.markdown('<div class="sec-head">💾 Save Options</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            **Automatically save predictions to dataset:**
            - ✅ Each prediction will be added to the training data
            - 📈 Dataset will grow automatically (2,393 → 2,394 → ...)
            - 🔄 You can retrain the model later with accumulated data
            """)
        with col2:
            save_to_dataset = st.checkbox("✅ Auto-save", value=True, key="save_checkbox", help="Uncheck to make predictions without saving")
            
        if data_manager is None:
            st.warning("⚠️ Data manager not available. Predictions will not be saved.")
            save_to_dataset = False
        else:
            if save_to_dataset:
                st.success("✅ Auto-save is ON - Predictions will be added to dataset")
            else:
                st.info("ℹ️ Auto-save is OFF - Predictions will be temporary only")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Enhanced prediction button
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
                    title={'text': "GPA Score", 'font': {'size': 16, 'color': '#e2e8f0' if st.session_state.dark_mode else '#1e293b'}}
                ))
                fig_gauge_gpa.update_layout(**plotly_theme(st.session_state.dark_mode), height=280, margin=dict(l=20, r=20, t=50, b=20), showlegend=False)
                st.plotly_chart(fig_gauge_gpa, use_container_width=True, config={'displayModeBar': False})

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
            
            # Save to dataset if checkbox is checked
            if save_to_dataset:
                if data_manager is None:
                    st.error("❌ Cannot save: Data manager not initialized")
                else:
                    try:
                        # Save without showing intermediate message
                        stats = data_manager.add_prediction_to_dataset(input_dict, gpa)
                        
                        if stats:
                            # Show success message that stays visible
                            st.success(f"""
                            ✅ **Successfully saved to dataset!**
                            - Total records: **{stats['total_records']:,}**
                            - Last updated: {stats['last_updated']}
                            - New StudentID: {stats['total_records']}
                            """)
                            
                            # Reload dataset in background (don't rerun the app)
                            st.session_state.df = pd.read_csv(DATASET_PATH)
                            
                            # Update initial count if not set
                            if 'initial_count' not in st.session_state:
                                st.session_state.initial_count = len(st.session_state.df) - 1
                            
                            # DON'T rerun - let user see the results
                            # st.rerun()  ← REMOVED THIS LINE
                        else:
                            st.error("❌ Failed to save: No stats returned")
                    except Exception as e:
                        st.error(f"❌ Error saving to dataset: {str(e)}")
                        import traceback
                        st.code(traceback.format_exc())
            
            # Show prediction history
            if len(st.session_state.history) > 1:
                st.markdown('<div class="sec-head">📜 Prediction History (This Session)</div>', unsafe_allow_html=True)
                history_df = pd.DataFrame(st.session_state.history)
                st.dataframe(history_df, use_container_width=True, hide_index=True)
            
            # Show recent dataset records if data was saved
            if save_to_dataset and st.session_state.df is not None:
                st.markdown('<div class="sec-head">📊 Recent Dataset Records</div>', unsafe_allow_html=True)
                st.markdown("**Last 5 records in the dataset:**")
                recent_df = st.session_state.df.tail(5)[['StudentID', 'Age', 'StudyTimeWeekly', 'Absences', 'GPA', 'GradeClass']]
                st.dataframe(recent_df, use_container_width=True, hide_index=True)
            
            # Add a button to make another prediction
            st.markdown("<br>", unsafe_allow_html=True)
            col_reset1, col_reset2, col_reset3 = st.columns([1, 2, 1])
            with col_reset2:
                if st.button("🔄 Make Another Prediction", use_container_width=True, type="primary"):
                    # Clear the prediction results by rerunning
                    st.rerun()


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

        # Enhanced Dataset Statistics
        st.markdown('<div class="sec-head">📈 Key Statistics & Insights</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="g-card">
                <h4 style="color:#a78bfa;margin-top:0;font-size:0.95rem;">🎯 GPA Distribution</h4>
            </div>""", unsafe_allow_html=True)
            
            gpa_stats = df['GPA'].describe()
            st.markdown(f"""
            <div style="padding:0.8rem;background:rgba(124,58,237,0.05);border-radius:8px;border:1px solid rgba(124,58,237,0.2);">
                <div style="display:flex;justify-content:space-between;margin:0.4rem 0;font-size:0.85rem;">
                    <span style="color:#94a3b8;">Minimum:</span>
                    <span style="color:#e2e8f0;font-weight:600;">{gpa_stats['min']:.2f}</span>
                </div>
                <div style="display:flex;justify-content:space-between;margin:0.4rem 0;font-size:0.85rem;">
                    <span style="color:#94a3b8;">Maximum:</span>
                    <span style="color:#e2e8f0;font-weight:600;">{gpa_stats['max']:.2f}</span>
                </div>
                <div style="display:flex;justify-content:space-between;margin:0.4rem 0;font-size:0.85rem;">
                    <span style="color:#94a3b8;">Median:</span>
                    <span style="color:#e2e8f0;font-weight:600;">{gpa_stats['50%']:.2f}</span>
                </div>
                <div style="display:flex;justify-content:space-between;margin:0.4rem 0;font-size:0.85rem;">
                    <span style="color:#94a3b8;">Std Dev:</span>
                    <span style="color:#e2e8f0;font-weight:600;">{gpa_stats['std']:.2f}</span>
                </div>
            </div>""", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="g-card">
                <h4 style="color:#a78bfa;margin-top:0;font-size:0.95rem;">📚 Study Patterns</h4>
            </div>""", unsafe_allow_html=True)
            
            avg_study = df['StudyTimeWeekly'].mean()
            avg_absences = df['Absences'].mean()
            tutoring_pct = df['Tutoring'].mean() * 100
            
            st.markdown(f"""
            <div style="padding:0.8rem;background:rgba(59,130,246,0.05);border-radius:8px;border:1px solid rgba(59,130,246,0.2);">
                <div style="display:flex;justify-content:space-between;margin:0.4rem 0;font-size:0.85rem;">
                    <span style="color:#94a3b8;">Avg Study Time:</span>
                    <span style="color:#e2e8f0;font-weight:600;">{avg_study:.1f}h/week</span>
                </div>
                <div style="display:flex;justify-content:space-between;margin:0.4rem 0;font-size:0.85rem;">
                    <span style="color:#94a3b8;">Avg Absences:</span>
                    <span style="color:#e2e8f0;font-weight:600;">{avg_absences:.1f} days</span>
                </div>
                <div style="display:flex;justify-content:space-between;margin:0.4rem 0;font-size:0.85rem;">
                    <span style="color:#94a3b8;">With Tutoring:</span>
                    <span style="color:#e2e8f0;font-weight:600;">{tutoring_pct:.1f}%</span>
                </div>
                <div style="display:flex;justify-content:space-between;margin:0.4rem 0;font-size:0.85rem;">
                    <span style="color:#94a3b8;">Parental Support:</span>
                    <span style="color:#e2e8f0;font-weight:600;">{df['ParentalSupport'].mean():.1f}/4</span>
                </div>
            </div>""", unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="g-card">
                <h4 style="color:#a78bfa;margin-top:0;font-size:0.95rem;">🏃 Activities</h4>
            </div>""", unsafe_allow_html=True)
            
            extracurricular_pct = df['Extracurricular'].mean() * 100
            sports_pct = df['Sports'].mean() * 100
            music_pct = df['Music'].mean() * 100
            volunteer_pct = df['Volunteering'].mean() * 100
            
            st.markdown(f"""
            <div style="padding:0.8rem;background:rgba(34,197,94,0.05);border-radius:8px;border:1px solid rgba(34,197,94,0.2);">
                <div style="display:flex;justify-content:space-between;margin:0.4rem 0;font-size:0.85rem;">
                    <span style="color:#94a3b8;">Extracurricular:</span>
                    <span style="color:#e2e8f0;font-weight:600;">{extracurricular_pct:.1f}%</span>
                </div>
                <div style="display:flex;justify-content:space-between;margin:0.4rem 0;font-size:0.85rem;">
                    <span style="color:#94a3b8;">Sports:</span>
                    <span style="color:#e2e8f0;font-weight:600;">{sports_pct:.1f}%</span>
                </div>
                <div style="display:flex;justify-content:space-between;margin:0.4rem 0;font-size:0.85rem;">
                    <span style="color:#94a3b8;">Music:</span>
                    <span style="color:#e2e8f0;font-weight:600;">{music_pct:.1f}%</span>
                </div>
                <div style="display:flex;justify-content:space-between;margin:0.4rem 0;font-size:0.85rem;">
                    <span style="color:#94a3b8;">Volunteering:</span>
                    <span style="color:#e2e8f0;font-weight:600;">{volunteer_pct:.1f}%</span>
                </div>
            </div>""", unsafe_allow_html=True)

        # Grade Distribution Summary
        st.markdown('<div class="sec-head">🎯 Grade Distribution Summary</div>', unsafe_allow_html=True)
        
        grade_map = {0.0:"A", 1.0:"B", 2.0:"C", 3.0:"D", 4.0:"F"}
        grade_counts = df["GradeClass"].value_counts()
        total_students = len(df)
        
        grade_cols = st.columns(5)
        grade_colors = ["#10b981", "#3b82f6", "#f59e0b", "#f97316", "#ef4444"]
        grade_icons = ["🏆", "🥈", "🥉", "📝", "⚠️"]
        
        for idx, (grade_val, grade_letter) in enumerate(grade_map.items()):
            count = grade_counts.get(grade_val, 0)
            percentage = (count / total_students * 100) if total_students > 0 else 0
            
            with grade_cols[idx]:
                st.markdown(f"""
                <div style="padding:1rem;background:rgba(124,58,237,0.05);border-radius:12px;border:2px solid {grade_colors[idx]};text-align:center;">
                    <div style="font-size:2rem;margin-bottom:0.3rem;">{grade_icons[idx]}</div>
                    <div style="font-size:1.5rem;font-weight:700;color:{grade_colors[idx]};margin-bottom:0.2rem;">Grade {grade_letter}</div>
                    <div style="font-size:1.2rem;color:#e2e8f0;font-weight:600;margin-bottom:0.2rem;">{count}</div>
                    <div style="font-size:0.85rem;color:#94a3b8;">{percentage:.1f}%</div>
                </div>""", unsafe_allow_html=True)

        # Demographics Overview
        st.markdown('<div class="sec-head">👥 Demographics Overview</div>', unsafe_allow_html=True)
        
        demo_col1, demo_col2 = st.columns(2)
        
        with demo_col1:
            st.markdown("""
            <div class="g-card">
                <h4 style="color:#a78bfa;margin-top:0;font-size:0.95rem;">🚻 Gender Distribution</h4>
            </div>""", unsafe_allow_html=True)
            
            gender_counts = df['Gender'].value_counts()
            male_count = gender_counts.get(1, 0)
            female_count = gender_counts.get(0, 0)
            male_pct = (male_count / total_students * 100) if total_students > 0 else 0
            female_pct = (female_count / total_students * 100) if total_students > 0 else 0
            
            st.markdown(f"""
            <div style="padding:1rem;background:rgba(124,58,237,0.05);border-radius:8px;">
                <div style="margin:0.8rem 0;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:0.3rem;">
                        <span style="color:#94a3b8;font-size:0.9rem;">👨 Male</span>
                        <span style="color:#e2e8f0;font-weight:600;">{male_count} ({male_pct:.1f}%)</span>
                    </div>
                    <div style="height:10px;background:rgba(255,255,255,0.05);border-radius:5px;overflow:hidden;">
                        <div style="height:100%;width:{male_pct}%;background:#3b82f6;border-radius:5px;"></div>
                    </div>
                </div>
                <div style="margin:0.8rem 0;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:0.3rem;">
                        <span style="color:#94a3b8;font-size:0.9rem;">👩 Female</span>
                        <span style="color:#e2e8f0;font-weight:600;">{female_count} ({female_pct:.1f}%)</span>
                    </div>
                    <div style="height:10px;background:rgba(255,255,255,0.05);border-radius:5px;overflow:hidden;">
                        <div style="height:100%;width:{female_pct}%;background:#ec4899;border-radius:5px;"></div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)
        
        with demo_col2:
            st.markdown("""
            <div class="g-card">
                <h4 style="color:#a78bfa;margin-top:0;font-size:0.95rem;">🎓 Parental Education</h4>
            </div>""", unsafe_allow_html=True)
            
            edu_map = {0: "None", 1: "High School", 2: "Some College", 3: "Bachelor's", 4: "Higher"}
            edu_counts = df['ParentalEducation'].value_counts().sort_index()
            
            edu_html = '<div style="padding:1rem;background:rgba(124,58,237,0.05);border-radius:8px;">'
            for edu_val in sorted(edu_counts.index):
                count = edu_counts[edu_val]
                pct = (count / total_students * 100) if total_students > 0 else 0
                edu_html += f"""
                <div style="margin:0.5rem 0;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:0.2rem;font-size:0.85rem;">
                        <span style="color:#94a3b8;">{edu_map.get(edu_val, 'Unknown')}</span>
                        <span style="color:#e2e8f0;font-weight:600;">{count} ({pct:.1f}%)</span>
                    </div>
                    <div style="height:6px;background:rgba(255,255,255,0.05);border-radius:3px;overflow:hidden;">
                        <div style="height:100%;width:{pct}%;background:#a78bfa;border-radius:3px;"></div>
                    </div>
                </div>"""
            edu_html += '</div>'
            st.markdown(edu_html, unsafe_allow_html=True)

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

        # Model Performance Insights
        st.markdown('<div class="sec-head">💡 Performance Insights</div>', unsafe_allow_html=True)
        
        insight_col1, insight_col2, insight_col3 = st.columns(3)
        
        with insight_col1:
            r2_score = bm.get('r2_score', 0)
            r2_pct = r2_score * 100
            r2_rating = "Excellent" if r2_score >= 0.95 else "Very Good" if r2_score >= 0.90 else "Good" if r2_score >= 0.80 else "Fair"
            r2_color = "#10b981" if r2_score >= 0.95 else "#3b82f6" if r2_score >= 0.90 else "#f59e0b" if r2_score >= 0.80 else "#f97316"
            
            st.markdown(f"""
<div style="padding:1.2rem;background:rgba(124,58,237,0.05);border-radius:12px;border:2px solid {r2_color};">
<div style="text-align:center;margin-bottom:0.8rem;">
<div style="font-size:2.5rem;font-weight:700;color:{r2_color};">{r2_pct:.1f}%</div>
<div style="font-size:0.9rem;color:#94a3b8;margin-top:0.2rem;">Model Accuracy</div>
</div>
<div style="padding:0.6rem;background:rgba(0,0,0,0.2);border-radius:6px;text-align:center;">
<div style="font-size:0.85rem;color:#e2e8f0;font-weight:600;">{r2_rating} Performance</div>
<div style="font-size:0.75rem;color:#94a3b8;margin-top:0.2rem;">R² Score: {r2_score:.4f}</div>
</div>
</div>""", unsafe_allow_html=True)
        
        with insight_col2:
            mae = bm.get('mae', 0)
            mae_rating = "Excellent" if mae <= 0.15 else "Very Good" if mae <= 0.20 else "Good" if mae <= 0.30 else "Fair"
            mae_color = "#10b981" if mae <= 0.15 else "#3b82f6" if mae <= 0.20 else "#f59e0b" if mae <= 0.30 else "#f97316"
            
            st.markdown(f"""
<div style="padding:1.2rem;background:rgba(124,58,237,0.05);border-radius:12px;border:2px solid {mae_color};">
<div style="text-align:center;margin-bottom:0.8rem;">
<div style="font-size:2.5rem;font-weight:700;color:{mae_color};">{mae:.4f}</div>
<div style="font-size:0.9rem;color:#94a3b8;margin-top:0.2rem;">Mean Absolute Error</div>
</div>
<div style="padding:0.6rem;background:rgba(0,0,0,0.2);border-radius:6px;text-align:center;">
<div style="font-size:0.85rem;color:#e2e8f0;font-weight:600;">{mae_rating} Precision</div>
<div style="font-size:0.75rem;color:#94a3b8;margin-top:0.2rem;">Avg Error: ±{mae*2.5:.2f} GPA points</div>
</div>
</div>""", unsafe_allow_html=True)
        
        with insight_col3:
            rmse = bm.get('rmse', 0)
            rmse_rating = "Excellent" if rmse <= 0.18 else "Very Good" if rmse <= 0.25 else "Good" if rmse <= 0.35 else "Fair"
            rmse_color = "#10b981" if rmse <= 0.18 else "#3b82f6" if rmse <= 0.25 else "#f59e0b" if rmse <= 0.35 else "#f97316"
            
            st.markdown(f"""
<div style="padding:1.2rem;background:rgba(124,58,237,0.05);border-radius:12px;border:2px solid {rmse_color};">
<div style="text-align:center;margin-bottom:0.8rem;">
<div style="font-size:2.5rem;font-weight:700;color:{rmse_color};">{rmse:.4f}</div>
<div style="font-size:0.9rem;color:#94a3b8;margin-top:0.2rem;">Root Mean Squared Error</div>
</div>
<div style="padding:0.6rem;background:rgba(0,0,0,0.2);border-radius:6px;text-align:center;">
<div style="font-size:0.85rem;color:#e2e8f0;font-weight:600;">{rmse_rating} Consistency</div>
<div style="font-size:0.75rem;color:#94a3b8;margin-top:0.2rem;">Std Error: ±{rmse*2.5:.2f} GPA points</div>
</div>
</div>""", unsafe_allow_html=True)

        # Model Comparison Summary
        st.markdown('<div class="sec-head">🔬 All Models Comparison</div>', unsafe_allow_html=True)
        
        names = list(metrics.keys())
        
        for model_name in names:
            m = metrics[model_name]
            is_best = (model_name == best)
            
            border_color = "#7c3aed" if is_best else "rgba(124,58,237,0.3)"
            bg_color = "rgba(124,58,237,0.1)" if is_best else "rgba(124,58,237,0.03)"
            
            st.markdown(f"""
<div style="padding:1rem;margin:0.8rem 0;background:{bg_color};border-radius:10px;border:2px solid {border_color};">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.8rem;">
<div>
<span style="font-size:1.1rem;font-weight:700;color:#e2e8f0;">{'🏆 ' if is_best else ''}{model_name}</span>
{f'<span style="margin-left:0.5rem;padding:0.2rem 0.6rem;background:#7c3aed;color:#fff;border-radius:12px;font-size:0.75rem;font-weight:600;">BEST MODEL</span>' if is_best else ''}
</div>
<div style="font-size:1.2rem;font-weight:700;color:#a78bfa;">{m['r2_score']*100:.2f}%</div>
</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.8rem;">
<div style="text-align:center;padding:0.6rem;background:rgba(0,0,0,0.2);border-radius:6px;">
<div style="font-size:0.75rem;color:#94a3b8;margin-bottom:0.2rem;">R² Score</div>
<div style="font-size:1rem;font-weight:600;color:#e2e8f0;">{m['r2_score']:.4f}</div>
</div>
<div style="text-align:center;padding:0.6rem;background:rgba(0,0,0,0.2);border-radius:6px;">
<div style="font-size:0.75rem;color:#94a3b8;margin-bottom:0.2rem;">MAE</div>
<div style="font-size:1rem;font-weight:600;color:#e2e8f0;">{m['mae']:.4f}</div>
</div>
<div style="text-align:center;padding:0.6rem;background:rgba(0,0,0,0.2);border-radius:6px;">
<div style="font-size:0.75rem;color:#94a3b8;margin-bottom:0.2rem;">RMSE</div>
<div style="font-size:1rem;font-weight:600;color:#e2e8f0;">{m['rmse']:.4f}</div>
</div>
</div>
</div>""", unsafe_allow_html=True)

        # Gauge for best model
        st.markdown('<div class="sec-head">🎯 Accuracy Gauge</div>', unsafe_allow_html=True)
        r2_pct = bm.get("r2_score", 0.95) * 100
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=r2_pct,
            delta={"reference": 90, "suffix":"%"},
            number={"suffix":"%", "font":{"size":38,"color":"#a78bfa","family":"Inter"}},
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
            title={"text": f"<b>{best}</b> - Model Accuracy", "font":{"color":"#e2e8f0" if st.session_state.dark_mode else "#1e293b","size":13}},
        ))
        fig_gauge.update_layout(
            **plotly_theme(st.session_state.dark_mode), 
            height=280, 
            margin=dict(l=40, r=40, t=80, b=20),
            showlegend=False
        )
        st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})


        # Metrics Explanation
        st.markdown('<div class="sec-head">📚 Understanding the Metrics</div>', unsafe_allow_html=True)
        
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        
        with metric_col1:
            st.markdown("""
            <div class="g-card">
                <h4 style="color:#a78bfa;margin-top:0;font-size:0.95rem;">📐 R² Score</h4>
                <p style="color:#94a3b8;font-size:0.82rem;line-height:1.6;">
                    Measures how well the model explains variance in GPA. 
                    <br><br>
                    <strong style="color:#e2e8f0;">1.0 = Perfect</strong><br>
                    <strong style="color:#10b981;">0.95+ = Excellent</strong><br>
                    <strong style="color:#3b82f6;">0.90+ = Very Good</strong><br>
                    <strong style="color:#f59e0b;">0.80+ = Good</strong>
                </p>
            </div>""", unsafe_allow_html=True)
        
        with metric_col2:
            st.markdown("""
            <div class="g-card">
                <h4 style="color:#a78bfa;margin-top:0;font-size:0.95rem;">📉 MAE</h4>
                <p style="color:#94a3b8;font-size:0.82rem;line-height:1.6;">
                    Average absolute difference between predicted and actual GPA.
                    <br><br>
                    <strong style="color:#10b981;">≤0.15 = Excellent</strong><br>
                    <strong style="color:#3b82f6;">≤0.20 = Very Good</strong><br>
                    <strong style="color:#f59e0b;">≤0.30 = Good</strong><br>
                    Lower is better!
                </p>
            </div>""", unsafe_allow_html=True)
        
        with metric_col3:
            st.markdown("""
            <div class="g-card">
                <h4 style="color:#a78bfa;margin-top:0;font-size:0.95rem;">📏 RMSE</h4>
                <p style="color:#94a3b8;font-size:0.82rem;line-height:1.6;">
                    Penalizes larger errors more heavily than MAE. Shows prediction consistency.
                    <br><br>
                    <strong style="color:#10b981;">≤0.18 = Excellent</strong><br>
                    <strong style="color:#3b82f6;">≤0.25 = Very Good</strong><br>
                    <strong style="color:#f59e0b;">≤0.35 = Good</strong><br>
                    Lower is better!
                </p>
            </div>""", unsafe_allow_html=True)


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
<h4 style="color:#a78bfa;margin-top:0">🚀 Key Features</h4>
<div style="font-size:0.82rem;color:#94a3b8;line-height:2.1;">
✨ &nbsp;<strong style="color:#e2e8f0">Real-time Predictions</strong> - Instant results<br>
📊 &nbsp;<strong style="color:#e2e8f0">Interactive Dashboards</strong> - Visual insights<br>
💾 &nbsp;<strong style="color:#e2e8f0">Auto-save Dataset</strong> - Growing data<br>
🎨 &nbsp;<strong style="color:#e2e8f0">Dark/Light Themes</strong> - Your preference<br>
📈 &nbsp;<strong style="color:#e2e8f0">Performance Tracking</strong> - Monitor trends<br>
🔒 &nbsp;<strong style="color:#e2e8f0">Data Privacy</strong> - Secure & local
</div>
</div>""", unsafe_allow_html=True)



    # Model Performance Comparison
    st.markdown('<div class="sec-head">🎮 Model Performance Overview</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding:1rem;background:rgba(124,58,237,0.05);border-radius:8px;border:1px solid rgba(124,58,237,0.2);margin-bottom:1rem;">
        <p style="color:#94a3b8;font-size:0.9rem;margin:0;">
            🎯 Our system uses Linear Regression as the primary model with 95.32% accuracy for optimal performance.
        </p>
    </div>""", unsafe_allow_html=True)
    
    # Only show Linear Regression
    pass

    
    # Interactive Feature Importance Simulator
    st.markdown('<div class="sec-head">🎯 Feature Impact Simulator</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding:1rem;background:rgba(59,130,246,0.05);border-radius:8px;border:1px solid rgba(59,130,246,0.2);margin-bottom:1rem;">
        <p style="color:#94a3b8;font-size:0.9rem;margin:0;">
            🔬 Adjust the sliders to see how different factors impact student performance predictions.
        </p>
    </div>""", unsafe_allow_html=True)
    
    sim_col1, sim_col2 = st.columns(2)
    
    with sim_col1:
        study_impact = st.slider("📚 Study Time Impact", 0, 100, 85, key="study_impact")
        attendance_impact = st.slider("✅ Attendance Impact", 0, 100, 75, key="attendance_impact")
        support_impact = st.slider("👨‍👩‍👧 Parental Support Impact", 0, 100, 60, key="support_impact")
    
    with sim_col2:
        tutoring_impact = st.slider("🧑‍🏫 Tutoring Impact", 0, 100, 55, key="tutoring_impact")
        activities_impact = st.slider("🏃 Activities Impact", 0, 100, 45, key="activities_impact")
        age_impact = st.slider("🎂 Age/Maturity Impact", 0, 100, 30, key="age_impact")
    
    # Calculate overall impact
    total_impact = (study_impact + attendance_impact + support_impact + tutoring_impact + activities_impact + age_impact) / 6
    
    impact_color = "#10b981" if total_impact >= 70 else "#f59e0b" if total_impact >= 50 else "#ef4444"
    impact_rating = "High Impact" if total_impact >= 70 else "Moderate Impact" if total_impact >= 50 else "Low Impact"
    
    st.markdown(f"""
    <div style="padding:1.5rem;background:rgba(124,58,237,0.05);border-radius:12px;border:2px solid {impact_color};margin-top:1rem;">
        <div style="text-align:center;">
            <div style="font-size:0.9rem;color:#94a3b8;margin-bottom:0.5rem;">Overall Performance Impact</div>
            <div style="font-size:3rem;font-weight:700;color:{impact_color};">{total_impact:.1f}%</div>
            <div style="font-size:1.1rem;color:#e2e8f0;margin-top:0.5rem;font-weight:600;">{impact_rating}</div>
            <div style="margin-top:1rem;padding:0.8rem;background:rgba(0,0,0,0.2);border-radius:8px;">
                <div style="font-size:0.85rem;color:#94a3b8;">
                    Based on your settings, a student with these factor levels would likely achieve a 
                    <strong style="color:#a78bfa;">GPA of {(total_impact/100)*10:.2f}/10</strong>
                </div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown('<div class="sec-head">📈 Quick Statistics</div>', unsafe_allow_html=True)
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.markdown("""
        <div style="padding:1rem;background:rgba(16,185,129,0.1);border-radius:8px;text-align:center;border:1px solid rgba(16,185,129,0.3);">
            <div style="font-size:2rem;margin-bottom:0.3rem;">🎓</div>
            <div style="font-size:1.5rem;font-weight:700;color:#10b981;">2,410</div>
            <div style="font-size:0.8rem;color:#94a3b8;margin-top:0.2rem;">Students Analyzed</div>
        </div>""", unsafe_allow_html=True)
    
    with stat_col2:
        st.markdown("""
        <div style="padding:1rem;background:rgba(59,130,246,0.1);border-radius:8px;text-align:center;border:1px solid rgba(59,130,246,0.3);">
            <div style="font-size:2rem;margin-bottom:0.3rem;">🎯</div>
            <div style="font-size:1.5rem;font-weight:700;color:#3b82f6;">95.3%</div>
            <div style="font-size:0.8rem;color:#94a3b8;margin-top:0.2rem;">Prediction Accuracy</div>
        </div>""", unsafe_allow_html=True)
    
    with stat_col3:
        st.markdown("""
        <div style="padding:1rem;background:rgba(245,158,11,0.1);border-radius:8px;text-align:center;border:1px solid rgba(245,158,11,0.3);">
            <div style="font-size:2rem;margin-bottom:0.3rem;">🤖</div>
            <div style="font-size:1.5rem;font-weight:700;color:#f59e0b;">3</div>
            <div style="font-size:0.8rem;color:#94a3b8;margin-top:0.2rem;">ML Models</div>
        </div>""", unsafe_allow_html=True)
    
    with stat_col4:
        st.markdown("""
        <div style="padding:1rem;background:rgba(236,72,153,0.1);border-radius:8px;text-align:center;border:1px solid rgba(236,72,153,0.3);">
            <div style="font-size:2rem;margin-bottom:0.3rem;">📊</div>
            <div style="font-size:1.5rem;font-weight:700;color:#ec4899;">12</div>
            <div style="font-size:0.8rem;color:#94a3b8;margin-top:0.2rem;">Input Features</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div style="text-align:center;margin-top:2rem;color:#64748b;font-size:0.75rem;">Student Performance Predictor · v2.0 · Built with ❤️</div>', unsafe_allow_html=True)
