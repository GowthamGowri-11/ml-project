"""
Script to apply enhanced UI styles to app.py
This updates the CSS injection function with premium styles
"""

import re

# Read the current app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the CSS section
# We'll replace everything between the inject_css function start and the Constants section

new_css_function = '''# ─── CSS injection (theme-aware) ────────────────────────────────────────────
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

*, *::before, *::after {{ box-sizing: border-box; }}
html, body, .stApp {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background: {BG} !important;
    color: {TXT} !important;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 2rem !important; max-width: 1400px !important; }}

/* Hero with animations */
.hero {{
    background: {HERO_BG};
    background-size: 200% 200%;
    animation: gradientShift 15s ease infinite;
    border: 2px solid {HERO_BORDER};
    border-radius: 28px;
    padding: 3.5rem 3rem;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(139,92,246,0.25);
    backdrop-filter: blur(20px);
}}
.hero::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: {HERO_OVERLAY};
    opacity: 0.6;
    animation: pulse 8s ease-in-out infinite;
}}
@keyframes gradientShift {{ 0%, 100% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} }}
@keyframes pulse {{ 0%, 100% {{ opacity: 0.6; }} 50% {{ opacity: 0.8; }} }}

.hero-badge {{
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(139,92,246,0.2); border: 1.5px solid rgba(167,139,250,0.5);
    border-radius: 50px; padding: 6px 18px; font-size: 0.75rem; font-weight: 700;
    color: {ACCENT_PRIMARY}; letter-spacing: 1.5px; text-transform: uppercase;
    margin-bottom: 1.5rem; position: relative; z-index: 2;
    backdrop-filter: blur(10px); box-shadow: 0 4px 15px rgba(139,92,246,0.2);
}}
.hero-title {{
    font-size: 3.5rem; font-weight: 900;
    background: {hero_title_grad};
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1.1; margin: 0 0 1rem 0; position: relative; z-index: 2;
    letter-spacing: -0.02em;
}}
.hero-sub {{ font-size: 1.15rem; color: {hero_sub_color}; font-weight: 400; margin: 0 0 2rem 0; position: relative; z-index: 2; }}
.hero-stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem; position: relative; z-index: 2; }}
.hero-stat {{
    text-align: center; padding: 1.5rem;
    background: {GLASS_BG}; border: 1px solid {GLASS_BORDER};
    border-radius: 16px; backdrop-filter: blur(20px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}
.hero-stat:hover {{ transform: translateY(-5px); box-shadow: 0 15px 40px rgba(139,92,246,0.3); }}
.hero-stat-val {{
    font-size: 2.5rem; font-weight: 900;
    background: {hero_stat_val_g};
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    font-family: 'JetBrains Mono', monospace;
}}
.hero-stat-lbl {{ font-size: 0.75rem; color: {MUT}; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 600; }}

/* Cards with glassmorphism */
.stElementContainer div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: {CARD} !important; border: 1.5px solid {BORDER} !important;
    border-radius: 20px !important; backdrop-filter: blur(20px) !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1) !important;
}}
.stElementContainer div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
    border-color: rgba(139,92,246,0.5) !important;
    box-shadow: 0 12px 48px rgba(139,92,246,0.2) !important;
    transform: translateY(-2px) !important;
    background: {CARD_HOVER} !important;
}}

/* KPI Cards */
.kpi-wrap {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; margin-bottom: 2rem; }}
.kpi {{
    background: {CARD}; border: 1.5px solid {BORDER}; border-radius: 18px;
    padding: 2rem 1.5rem; text-align: center;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(20px); box-shadow: 0 8px 32px rgba(0,0,0,0.08);
}}
.kpi:hover {{ border-color: rgba(139,92,246,0.6); transform: translateY(-8px) scale(1.02); box-shadow: 0 20px 60px rgba(139,92,246,0.25); }}
.kpi-icon {{ font-size: 2.5rem; margin-bottom: 1rem; filter: drop-shadow(0 4px 12px rgba(139,92,246,0.3)); }}
.kpi-val {{
    font-size: 2.8rem; font-weight: 900;
    background: linear-gradient(135deg, {ACCENT_PRIMARY}, {ACCENT_SECONDARY});
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    font-family: 'JetBrains Mono', monospace;
}}
.kpi-lbl {{ font-size: 0.8rem; color: {MUT}; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }}
.kpi3 {{ grid-template-columns: repeat(3, 1fr); }}

/* Prediction Card */
.pred-card {{
    background: linear-gradient(135deg, rgba(139,92,246,0.15) 0%, rgba(59,130,246,0.1) 100%);
    border: 2px solid rgba(167,139,250,0.4); border-radius: 28px;
    padding: 3rem 2.5rem; text-align: center;
    box-shadow: 0 20px 60px rgba(139,92,246,0.2);
    margin: 1.5rem 0; backdrop-filter: blur(30px);
}}
.pred-gpa {{
    font-size: 6rem; font-weight: 900;
    background: linear-gradient(135deg, #a78bfa 0%, #60a5fa 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    font-family: 'JetBrains Mono', monospace;
}}
.pred-label {{ font-size: 0.9rem; color: {MUT}; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; }}
.pred-grade {{ font-size: 1.8rem; font-weight: 700; margin-top: 1rem; }}
.pred-sub {{ font-size: 1rem; color: {SUB}; margin-top: 0.5rem; }}
.grade-badge {{
    display: inline-block; padding: 10px 28px; border-radius: 50px;
    font-size: 1rem; font-weight: 800; margin-top: 1.5rem;
    box-shadow: 0 8px 24px rgba(0,0,0,0.15); transition: all 0.3s;
}}
.grade-badge:hover {{ transform: scale(1.05); }}
.grade-A {{ background: linear-gradient(135deg, #10b981, #34d399); color: white; }}
.grade-B {{ background: linear-gradient(135deg, #3b82f6, #60a5fa); color: white; }}
.grade-C {{ background: linear-gradient(135deg, #f59e0b, #fbbf24); color: white; }}
.grade-D {{ background: linear-gradient(135deg, #f97316, #fb923c); color: white; }}
.grade-F {{ background: linear-gradient(135deg, #ef4444, #f87171); color: white; }}

/* Section Headers */
.sec-head {{
    font-size: 1.4rem; font-weight: 800; color: {TXT};
    margin: 2.5rem 0 1.5rem 0; display: flex; align-items: center; gap: 12px;
    position: relative; padding-left: 20px;
}}
.sec-head::before {{
    content: ''; position: absolute; left: 0; width: 6px; height: 100%;
    background: linear-gradient(180deg, {ACCENT_PRIMARY}, {ACCENT_SECONDARY});
    border-radius: 3px; box-shadow: 0 0 20px rgba(139,92,246,0.5);
}}
.sec-head::after {{
    content: ''; flex: 1; height: 2px;
    background: linear-gradient(90deg, rgba(139,92,246,0.5), transparent);
}}

/* Progress Bars */
.prog-wrap {{ margin: 1rem 0; }}
.prog-label {{ display: flex; justify-content: space-between; font-size: 0.85rem; color: {SUB}; margin-bottom: 8px; font-weight: 600; }}
.prog-track {{ height: 10px; background: {BORDER}; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1) inset; }}
.prog-fill {{
    height: 100%; border-radius: 10px;
    background: linear-gradient(90deg, #7c3aed, #3b82f6);
    transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 0 20px rgba(124,58,237,0.5);
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background: {SIDEBAR} !important;
    border-right: 2px solid {SIDEBAR_BORDER} !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.1) !important;
}}
.sidebar-logo {{ text-align: center; padding: 2rem 0 1rem; font-size: 3.5rem; filter: drop-shadow(0 4px 12px rgba(139,92,246,0.4)); }}
.sidebar-title {{ text-align: center; font-size: 1.2rem; font-weight: 800; color: {TXT}; margin-bottom: 0.3rem; }}
.sidebar-sub {{ text-align: center; font-size: 0.75rem; color: {MUT}; margin-bottom: 2rem; text-transform: uppercase; letter-spacing: 1.5px; }}
.status-pill {{
    display: flex; align-items: center; gap: 10px;
    padding: 12px 18px; border-radius: 50px; font-size: 0.85rem; font-weight: 700;
    margin: 1rem 0; backdrop-filter: blur(10px); transition: all 0.3s;
}}
.status-on {{ background: rgba(34,197,94,0.15); color: #4ade80; border: 1.5px solid rgba(34,197,94,0.4); box-shadow: 0 4px 16px rgba(34,197,94,0.2); }}
.status-off {{ background: rgba(239,68,68,0.15); color: #f87171; border: 1.5px solid rgba(239,68,68,0.4); box-shadow: 0 4px 16px rgba(239,68,68,0.2); }}
.dot {{ width: 10px; height: 10px; border-radius: 50%; }}
.dot-on {{ background: #4ade80; box-shadow: 0 0 12px #4ade80; animation: blink 2s ease-in-out infinite; }}
.dot-off {{ background: #f87171; }}
@keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{ gap: 8px; background: transparent !important; border-bottom: 2px solid {BORDER} !important; }}
.stTabs [data-baseweb="tab"] {{
    background: transparent !important; border: 1.5px solid transparent !important;
    border-radius: 12px 12px 0 0 !important; color: {MUT} !important;
    font-weight: 600 !important; padding: 12px 24px !important;
    transition: all 0.3s !important;
}}
.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, rgba(139,92,246,0.15), rgba(59,130,246,0.1)) !important;
    border-color: rgba(139,92,246,0.4) !important; color: {ACCENT_PRIMARY} !important;
    box-shadow: 0 -4px 16px rgba(139,92,246,0.2) !important;
}}

/* Inputs */
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] > div {{
    background: {INP_BG} !important; border: 1.5px solid {INP_BORDER} !important;
    border-radius: 12px !important; color: {TXT} !important;
    padding: 12px 16px !important; backdrop-filter: blur(10px) !important;
    transition: all 0.3s !important;
}}
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stTextInput"] input:focus {{
    border-color: {ACCENT_PRIMARY} !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.2) !important;
}}

/* Buttons */
.stButton > button {{
    border-radius: 14px !important; font-weight: 700 !important;
    transition: all 0.3s !important; padding: 14px 32px !important;
    text-transform: uppercase !important;
}}
.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, #7c3aed 0%, #3b82f6 100%) !important;
    border: none !important;
    box-shadow: 0 8px 32px rgba(124,58,237,0.4) !important;
    color: white !important;
}}
.stButton > button[kind="primary"]:hover {{
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 12px 48px rgba(124,58,237,0.5) !important;
}}

/* Data Tables */
.stDataFrame {{ border-radius: 16px !important; overflow: hidden !important; border: 1.5px solid {BORDER} !important; box-shadow: 0 8px 32px rgba(0,0,0,0.08) !important; }}

/* Insight Cards */
.insight-card {{
    background: {CARD}; border: 1.5px solid {BORDER}; border-radius: 16px;
    padding: 1.5rem; margin-bottom: 1rem; backdrop-filter: blur(20px); transition: all 0.3s;
}}
.insight-card:hover {{ border-color: rgba(139,92,246,0.4); box-shadow: 0 8px 32px rgba(139,92,246,0.15); }}
.insight-row {{ display: flex; justify-content: space-between; margin: 0.6rem 0; font-size: 0.9rem; }}
.insight-key {{ color: {SUB}; font-weight: 500; }}
.insight-val {{ color: {ACCENT_PRIMARY}; font-weight: 800; font-family: 'JetBrains Mono', monospace; }}

/* Widget Labels */
.stSlider label, .stSelectbox label, .stNumberInput label, .stTextInput label, .stCheckbox label {{
    color: {TXT} !important; font-weight: 600 !important;
}}
div[data-testid="stMarkdownContainer"] p, div[data-testid="stMarkdownContainer"] span {{ color: {TXT} !important; }}

/* Slider */
.stSlider > div > div > div > div {{ background: linear-gradient(90deg, {ACCENT_PRIMARY}, {ACCENT_SECONDARY}) !important; box-shadow: 0 0 12px rgba(139,92,246,0.5) !important; }}

/* Scrollbar */
::-webkit-scrollbar {{ width: 10px; height: 10px; }}
::-webkit-scrollbar-track {{ background: {BORDER}; border-radius: 10px; }}
::-webkit-scrollbar-thumb {{
    background: linear-gradient(180deg, {ACCENT_PRIMARY}, {ACCENT_SECONDARY});
    border-radius: 10px; border: 2px solid {BORDER};
}}
</style>
""", unsafe_allow_html=True)
'''

# Pattern to match the inject_css function
pattern = r'# ─── CSS injection.*?(?=# ─── Constants)'

# Replace
new_content = re.sub(pattern, new_css_function, content, flags=re.DOTALL)

# Write back
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ Enhanced UI styles applied successfully!")
print("🎨 Features added:")
print("   - Glassmorphism effects")
print("   - Animated gradients")
print("   - Premium card designs")
print("   - Enhanced typography")
print("   - Smooth transitions")
print("   - Custom scrollbars")
print("\n🔄 Restart the Streamlit app to see changes")
