"""
Rakshika-Ai Theme Module - Centralized CSS Styling for Women's Safety Application
A professional, empowering theme reflecting safety, trust, and support.
"""

from turtle import right

import streamlit as st

# ========== COLOR PALETTE ==========
COLORS = {
    # Primary - Safety & Trust (Purple tones)
    "primary": "#6B46C1",          # Deep Purple
    "primary_light": "#8B5CF6",    # Light Purple
    "primary_dark": "#5A36A3",     # Dark Purple
    
    # Secondary - Emergency & Action (Red tones)
    "danger": "#DC2626",           # Bright Red
    "danger_light": "#EF4444",     # Light Red
    "danger_dark": "#B91C1C",      # Dark Red
    
    # Accent - Hope & Empowerment (Rose tones)
    "accent": "#DB2777",           # Deep Rose
    "accent_light": "#EC4899",     # Light Rose
    
    # Success & Support
    "success": "#10B981",          # Teal/Green
    "success_light": "#34D399",    # Light Teal
    
    # Neutral Backgrounds
    "bg_light": "#F9FAFB",         # Almost white
    "bg_medium": "#F3F4F6",        # Light gray
    "bg_dark": "#1F2937",          # Dark gray
    
    # Text
    "text_dark": "#111827",        # Almost black
    "text_light": "#6B7280",       # Gray
    "text_white": "#FFFFFF",       # White
    
    # Borders & Shadows
    "border": "#E5E7EB",           # Light border
    "shadow": "rgba(0, 0, 0, 0.1)",
}

# ========== APPLY GLOBAL THEME ==========
def apply_global_theme():
    """Apply the Rakshika-Ai theme globally to the app"""
    theme_css = f"""
    <style>
    /* ===== ANIMATIONS ===== */
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes slideInLeft {{
        from {{
            opacity: 0;
            transform: translateX(-30px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.8; }}
    }}
    
    @keyframes glow {{
        0%, 100% {{
            box-shadow: 0 0 20px rgba(107, 70, 193, 0.3), 0 4px 12px {COLORS['shadow']};
        }}
        50% {{
            box-shadow: 0 0 40px rgba(107, 70, 193, 0.6), 0 8px 20px {COLORS['shadow']};
        }}
    }}
    
    @keyframes shimmer {{
        0% {{ background-position: -1000px 0; }}
        100% {{ background-position: 1000px 0; }}
    }}
    
    /* ===== GLOBAL STYLING ===== */
    * {{
        margin: 0;
        padding: 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    html, body, [data-testid="stAppViewContainer"] {{
        background: linear-gradient(135deg, {COLORS['bg_light']} 0%, {COLORS['bg_medium']} 50%, #F0E9FF 100%);
        background-attachment: fixed;
        color: {COLORS['text_dark']};
        font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
    }}
    
    /* ===== MAIN CONTAINER ===== */
    .block-container {{
        background: {COLORS['text_white']};
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08), 
                    0 0 0 1px rgba(107, 70, 193, 0.1);
        animation: fadeInUp 0.6s ease-out;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(107, 70, 193, 0.05);
    }}
    /* FIX Plotly hover issues */
.js-plotly-plot *{{
    transition: none !important;
}}

.js-plotly-plot .hoverlayer {{
    pointer-events: none;
}}

.js-plotly-plot .hovertext {{
    overflow: visible !important;
}}
    
    /* ===== HEADERS ===== */
    h1, h2, h3, h4, h5, h6 {{
        color: {COLORS['text_dark']} !important;
        font-weight: 700;
        letter-spacing: -0.8px;
        animation: slideInLeft 0.6s ease-out;
    }}
    
    h1 {{
        font-size: 2.75rem;
        margin-bottom: 1.25rem;
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['accent']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 2px 10px rgba(107, 70, 193, 0.1);
        letter-spacing: -1px;
    }}
    
    h2 {{
        font-size: 2rem;
        margin-top: 1.75rem;
        margin-bottom: 0.875rem;
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_light']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        position: relative;
        padding-bottom: 0.5rem;
    }}
    
    h2::after {{
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 50px;
        height: 4px;
        background: linear-gradient(90deg, {COLORS['primary']}, {COLORS['accent']});
        border-radius: 2px;
    }}
    
    h3 {{
        font-size: 1.5rem;
        margin-bottom: 0.75rem;
        color: {COLORS['primary']} !important;
    }}
    
    /* ===== TEXT & PARAGRAPHS ===== */
    p, span {{
        color: {COLORS['text_dark']};
        line-height: 1.7;
        letter-spacing: 0.3px;
    }}
    
    /* ===== BUTTONS ===== */
    .stButton > button {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_light']} 100%) !important;
        color: {COLORS['text_white']} !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 24px rgba(107, 70, 193, 0.3) !important;
        position: relative;
        overflow: hidden;
    }}
    
    .stButton > button::before {{
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-4px) !important;
        box-shadow: 0 16px 40px rgba(107, 70, 193, 0.45) !important;
        background: linear-gradient(135deg, {COLORS['primary_light']} 0%, {COLORS['primary']} 100%) !important;
    }}
    
    .stButton > button:hover::before {{
        width: 300px !important;
        height: 300px !important;
    }}
    
    .stButton > button:active {{
        transform: translateY(-1px) !important;
    }}
    
    /* ===== DANGER BUTTON ===== */
    .stButton.danger > button {{
        background: linear-gradient(135deg, {COLORS['danger']} 0%, {COLORS['danger_light']} 100%) !important;
        box-shadow: 0 8px 24px rgba(220, 38, 38, 0.35) !important;
    }}
    
    .stButton.danger > button:hover {{
        box-shadow: 0 16px 40px rgba(220, 38, 38, 0.45) !important;
        background: linear-gradient(135deg, {COLORS['danger_light']} 0%, {COLORS['danger']} 100%) !important;
    }}
    
    /* ===== TEXT INPUTS ===== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {{
        background-color: {COLORS['bg_light']} !important;
        border: 2px solid {COLORS['border']} !important;
        border-radius: 10px !important;
        padding: 14px 16px !important;
        color: {COLORS['text_dark']} !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: {COLORS['primary']} !important;
        box-shadow: 0 0 0 4px rgba(107, 70, 193, 0.15), 0 4px 12px rgba(107, 70, 193, 0.2) !important;
        background-color: rgba(139, 92, 246, 0.02) !important;
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: {COLORS['text_light']} !important;
        opacity: 0.7;
    }}
    
    /* ===== LABELS ===== */
    label {{
        color: {COLORS['text_dark']} !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 0.3px;
        text-transform: capitalize;
    }}
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['primary_dark']} 0%, {COLORS['primary']} 50%, {COLORS['primary_light']} 100%) !important;
        box-shadow: 4px 0 20px rgba(107, 70, 193, 0.2) !important;
    }}
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {{
        color: {COLORS['text_white']} !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }}
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {{
        color: rgba(255, 255, 255, 0.95) !important;
        font-weight: 500;
    }}
    
    [data-testid="stSidebar"] button {{
        background: rgba(255, 255, 255, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: {COLORS['text_white']} !important;
        border-radius: 10px !important;
    }}
    
    [data-testid="stSidebar"] button:hover {{
        background: rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 4px 12px rgba(255, 255, 255, 0.2) !important;
    }}
    
    /* ===== CARDS & CONTAINERS ===== */
    .metric-card {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_light']} 100%);
        padding: 28px;
        border-radius: 16px;
        color: {COLORS['text_white']};
        text-align: center;
        box-shadow: 0 12px 32px rgba(107, 70, 193, 0.25);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s ease-out backwards;
    }}
    
    .metric-card::before {{
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%);
        transition: all 0.4s ease;
    }}

    .metric-card.compact {{
        padding: 16px;
        border-radius: 14px;
        box-shadow: 0 10px 22px rgba(107, 70, 193, 0.18);
        min-height: 0;
    }}

    .metric-card.compact .metric-value {{
        font-size: 1.8rem;
    }}

    .metric-card.compact .metric-label {{
        font-size: 0.95rem;
    }}

    .metric-card.compact div[style] {{
        font-size: 1.4rem !important;
        margin-bottom: 8px !important;
    }}

    .dataset-card.compact {{
        padding: 12px;
        border-radius: 16px;
        min-height: auto;
    }}

    .dataset-card.compact .dataset-title {{
        font-size: 1rem;
    }}

    .dataset-card.compact .dataset-desc {{
        font-size: 0.9rem;
    }}

    .safety-card {{
        background: {COLORS['text_white']};
        border: 1px solid rgba(107, 70, 193, 0.12);
        border-radius: 14px;
        padding: 14px 16px;
        color: {COLORS['text_dark']};
        box-shadow: 0 8px 18px rgba(15, 23, 42, 0.08);
        min-height: 0;
        text-align: left;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }}

    .safety-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 12px 24px rgba(15, 23, 42, 0.12);
    }}

    .safety-card .card-title {{
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 8px;
        color: {COLORS['primary_dark']};
    }}

    .safety-card .card-value {{
        font-size: 1.4rem;
        font-weight: 800;
        margin: 4px 0 6px;
    }}

    .safety-card .card-subtitle {{
        font-size: 0.82rem;
        color: {COLORS['text_light']};
        opacity: 0.9;
    }}
    
    .metric-card:hover {{
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 24px 48px rgba(107, 70, 193, 0.35);
    }}
    
    .metric-value {{
        font-size: 2.5rem;
        font-weight: 900;
        margin: 16px 0;
        letter-spacing: -1px;
    }}
    
    .metric-label {{
        font-size: 1rem;
        opacity: 0.95;
        font-weight: 600;
        letter-spacing: 0.5px;
    }}

    .dataset-card {{
        background: linear-gradient(135deg, rgba(107, 70, 193, 0.08), rgba(255, 255, 255, 0.95));
        border: 1px solid rgba(107, 70, 193, 0.15);
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 18px;
        color: {COLORS['text_dark']};
        box-shadow: 0 18px 40px rgba(107, 70, 193, 0.12);
        transition: transform 0.35s ease, box-shadow 0.35s ease, border-color 0.35s ease;
        min-height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}

    .dataset-card:hover {{
        transform: translateY(-6px);
        border-color: rgba(107, 70, 193, 0.3);
        box-shadow: 0 24px 52px rgba(107, 70, 193, 0.18);
    }}

    .dataset-card .dataset-title {{
        font-size: 1.1rem;
        font-weight: 700;
        color: {COLORS['primary_dark']};
        margin-bottom: 10px;
    }}

    .dataset-card .dataset-desc {{
        color: {COLORS['text_light']};
        font-size: 0.95rem;
        line-height: 1.5;
    }}

    .hero-box {{
        background: linear-gradient(135deg, rgba(107, 70, 193, 0.08), rgba(255, 255, 255, 0.95));
        border: 1px solid rgba(107, 70, 193, 0.18);
        border-radius: 24px;
        padding: 28px;
        margin-bottom: 24px;
        box-shadow: 0 18px 40px rgba(107, 70, 193, 0.12);
        overflow: hidden;
    }}

    .hero-content {{
        display: flex;
        gap: 24px;
        align-items: center;
        flex-wrap: wrap;
    }}

    .hero-copy {{
        flex: 1 1 360px;
        min-width: 320px;
    }}

    .hero-copy h1 {{
        font-size: 2.4rem;
        margin-bottom: 18px;
        color: {COLORS['text_dark']};
    }}

    .hero-copy p {{
        color: {COLORS['text_dark']};
        line-height: 1.7;
        margin-bottom: 14px;
    }}

    .hero-image {{
        flex: 1 1 320px;
        min-width: 280px;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 16px 35px rgba(15, 23, 42, 0.08);
    }}

    .hero-image img {{
        width: 100%;
        height: auto;
        display: block;
    }}

    .hero-caption {{
        color: {COLORS['text_light']};
        margin: 14px 16px 0;
        font-size: 0.95rem;
    }}

    .about-card, .feature-box {{
        background: {COLORS['text_white']};
        border: 1px solid rgba(107, 70, 193, 0.12);
        border-radius: 18px;
        padding: 20px 22px;
        box-shadow: 0 12px 28px rgba(15, 23, 42, 0.06);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        min-height: 180px;
        margin-bottom: 18px;
    }}

    .about-card:hover, .feature-box:hover {{
        transform: translateY(-3px);
        box-shadow: 0 16px 32px rgba(15, 23, 42, 0.1);
    }}

    .about-card h3, .feature-box strong {{
        color: {COLORS['primary_dark']};
        margin-bottom: 12px;
        font-size: 1.1rem;
    }}

    .about-card p, .feature-box p {{
        color: {COLORS['text_dark']};
        font-size: 0.95rem;
        line-height: 1.7;
    }}

    .feature-icon {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border-radius: 12px;
        background: rgba(107, 70, 193, 0.12);
        margin-right: 10px;
        font-size: 1rem;
    }}

    .stButton > button {{
        min-height: 48px !important;
        font-size: 0.95rem !important;
    }}
    
    /* ===== INFO BOX ===== */
    .info-box {{
        background: linear-gradient(135deg, rgba(107, 70, 193, 0.08), rgba(219, 39, 119, 0.05));
        border-left: 5px solid {COLORS['primary']};
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0; 
        box-shadow: 0 4px 16px rgba(107, 70, 193, 0.1);
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
    }}
    
    .info-box:hover {{
        box-shadow: 0 8px 24px rgba(107, 70, 193, 0.15);
        # transform: translateY(-2px);
    }}
    
    .info-box strong {{
        color: {COLORS['primary']};
        font-size: 1.05rem;
    }}
    
    .info-box p {{
        margin-top: 10px;
        color: {COLORS['text_dark']};
        font-size: 0.95rem;
        line-height: 1.6;
    }}
    
    /* ===== SUCCESS BOX ===== */
    .stSuccess {{
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.08), rgba(16, 185, 129, 0.04)) !important;
        border: 2px solid {COLORS['success']} !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.15) !important;
    }}
    
    .stSuccess svg {{
        color: {COLORS['success']} !important;
    }}
    
    /* ===== ERROR BOX ===== */
    .stError {{
        background: linear-gradient(135deg, rgba(220, 38, 38, 0.08), rgba(220, 38, 38, 0.04)) !important;
        border: 2px solid {COLORS['danger']} !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.15) !important;
    }}
    
    .stError svg {{
        color: {COLORS['danger']} !important;
    }}
    
    /* ===== WARNING BOX ===== */
    .stWarning {{
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.08), rgba(245, 158, 11, 0.04)) !important;
        border: 2px solid #F59E0B !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.15) !important;
    }}
    
    .stWarning svg {{
        color: #F59E0B !important;
    }}
    
    /* ===== INFO BOX ===== */
    .stInfo {{
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(59, 130, 246, 0.04)) !important;
        border: 2px solid #3B82F6 !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15) !important;
    }}
    
    .stInfo svg {{
        color: #3B82F6 !important;
    }}
    
    /* ===== DIVIDER ===== */
    hr {{
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, {COLORS['primary']}, transparent);
        margin: 28px 0;
        opacity: 0.7;
    }}
    
    /* ===== DATAFRAME ===== */
    [data-testid="stDataFrame"] {{
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08) !important;
    }}
    
    table {{
        border-collapse: collapse !important;
        width: 100%;
    }}
    
    th {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_light']} 100%) !important;
        color: {COLORS['text_white']} !important;
        font-weight: 700 !important;
        padding: 16px !important;
        text-align: left;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 8px rgba(107, 70, 193, 0.15);
    }}
    
    td {{
        border-bottom: 1px solid {COLORS['border']} !important;
        padding: 14px 16px !important;
        font-size: 0.95rem;
    }}
    
    tr:hover {{
        background: linear-gradient(90deg, rgba(107, 70, 193, 0.08), transparent) !important;
    }}
    
    tr:last-child td {{
        border-bottom: none !important;
    }}
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] button {{
        color: {COLORS['text_light']} !important;
        border-bottom: 3px solid transparent !important;
        transition: all 0.3s ease !important;
        font-weight: 600;
        letter-spacing: 0.3px;
    }}
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
        color: {COLORS['primary']} !important;
        border-bottom-color: {COLORS['primary']} !important;
    }}
    
    .stTabs [data-baseweb="tab-list"] button:hover {{
        color: {COLORS['primary']} !important;
    }}
    
    /* ===== SELECTBOX/MULTISELECT ===== */
    .stMultiSelect [data-baseweb="tag"] {{
        background: linear-gradient(135deg, {COLORS['primary']}, {COLORS['primary_light']}) !important;
        border-radius: 8px !important;
    }}
    
    /* ===== SLIDER ===== */
    .stSlider [data-testid="stSliderThumb"] {{
        background: {COLORS['primary']} !important;
        box-shadow: 0 2px 8px rgba(107, 70, 193, 0.3) !important;
    }}
    
    .stSlider [data-testid="stSliderTrack"] {{
        background: linear-gradient(90deg, {COLORS['border']}, {COLORS['primary']}) !important;
    }}
    
    /* ===== CHAT MESSAGE STYLING ===== */
    .chat-message {{
        padding: 18px;
        border-radius: 14px;
        margin-bottom: 14px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        animation: fadeInUp 0.3s ease-out;
        backdrop-filter: blur(5px);
    }}
    
    .chat-message.user {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_light']} 100%);
        color: {COLORS['text_white']};
        margin-left: auto;
        max-width: 80%;
        box-shadow: 0 6px 16px rgba(107, 70, 193, 0.25);
    }}
    
    .chat-message.assistant {{
        background: linear-gradient(135deg, {COLORS['bg_medium']} 0%, {COLORS['bg_light']} 100%);
        color: {COLORS['text_dark']};
        margin-right: auto;
        max-width: 80%;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    }}
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: linear-gradient(180deg, {COLORS['bg_light']}, {COLORS['bg_medium']});
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(180deg, {COLORS['primary']}, {COLORS['primary_light']});
        border-radius: 10px;
        box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.1);
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(180deg, {COLORS['primary_light']}, {COLORS['accent']});
        box-shadow: 0 0 12px rgba(107, 70, 193, 0.3) inset;
    }}
    
    /* ===== RESPONSIVE DESIGN ===== */
    @media (max-width: 768px) {{
        h1 {{ font-size: 2rem; }}
        h2 {{ font-size: 1.5rem; }}
        h3 {{ font-size: 1.25rem; }}
        
        .block-container {{ 
            padding: 1.5rem;
            margin: 0.5rem;
            border-radius: 16px;
        }}
        
        .metric-card {{
            padding: 20px;
            margin-bottom: 12px;
        }}
        
        .stButton > button {{
            padding: 12px 20px !important;
            font-size: 0.95rem !important;
        }}
        
        .chat-message.user,
        .chat-message.assistant {{
            max-width: 95%;
        }}
    }}
    
    @media (max-width: 640px) {{
        h1 {{ font-size: 1.75rem; }}
        h2 {{ font-size: 1.35rem; }}
        
        .block-container {{ 
            padding: 1rem;
            margin: 0.25rem;
        }}
        
        .metric-card {{
            padding: 16px;
            font-size: 0.9rem;
        }}
        
        .metric-value {{
            font-size: 2rem;
        }}
        
        .stButton > button {{
            padding: 10px 16px !important;
            font-size: 0.9rem !important;
        }}
    }}
    </style>
    """
    st.markdown(theme_css, unsafe_allow_html=True)


# ========== CARD COMPONENTS ==========
def metric_card(title, value, icon=""):
    """Create a styled metric card"""
    html = f"""
    <div class="metric-card">
        <div style="font-size: 2rem; margin-bottom: 8px;">{icon}</div>
        <div class="metric-label">{title}</div>
        <div class="metric-value">{value}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def info_box(title, content, icon="ℹ️"):
    """Create a styled info box"""
    html = f"""
    <div class="info-box">
        <strong>{icon} {title}</strong>
        <p style="margin-top: 8px; color: {COLORS['text_dark']};">{content}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


# ========== AUTHENTICATION STYLED CONTAINER ==========
def auth_page_setup(page_title):
    """Setup styling for authentication pages (login, register)"""
    auth_css = f"""
    <style>
    .stApp {{
        background: linear-gradient(135deg, {COLORS['primary_dark']} 0%, #2D1B69 50%, {COLORS['primary']} 100%);
        background-attachment: fixed;
    }}
    
    .block-container {{
        max-width: 450px;
        margin: 60px auto;
        background: {COLORS['text_white']};
        border-radius: 20px;
        padding: 3.5rem 2.5rem;
        box-shadow: 0 30px 80px rgba(0, 0, 0, 0.3),
                    0 0 1px rgba(107, 70, 193, 0.3);
        border: 1px solid rgba(107, 70, 193, 0.1);
        backdrop-filter: blur(10px);
        animation: slideInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        animation-fill-mode: both;
    }}
    
    @keyframes slideInUp {{
        from {{
            opacity: 0;
            transform: translateY(40px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    h1 {{
        text-align: center;
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['accent']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem !important;
        margin-bottom: 0.75rem;
        font-weight: 900;
        letter-spacing: -1px;
    }}
   
    .auth-subtitle {{
        text-align: center;
        color: {COLORS['text_light']};
        margin-bottom: 2.5rem;
        font-size: 1rem;
        line-height: 1.6;
    }}
    
    .stForm {{
        display: flex;
        flex-direction: column;
        gap: 1.25rem;
    }}
    
    .stForm button {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_light']} 100%) !important;
        color: {COLORS['text_white']} !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 24px rgba(107, 70, 193, 0.35) !important;
        position:relative;
        overflow: hidden;
    }}
    
    .stForm button:hover {{
        transform: translateY(-4px) !important;
        box-shadow: 0 16px 40px rgba(107, 70, 193, 0.45) !important;
    }}
    
    .stForm button:active {{
        transform: translateY(-1px) !important;
    }}
    
    
    .auth-link {{
        text-align: center;
        margin-top: 2rem;
        color: {COLORS['text_light']};
        font-size: 0.95rem;
    }}
    
    .auth-link a {{
        color: {COLORS['primary']};
        text-decoration: none;
        font-weight: 700;
        transition: all 0.3s ease;
    }}
    
    .auth-link a:hover {{
        color: {COLORS['accent']};
        text-decoration: underline;
    }}
    
    .stTextInput > div > div > input {{
        background-color: {COLORS['bg_light']} !important;
        border: 2px solid {COLORS['border']} !important;
        border-radius: 10px !important;
        padding: 14px 16px !important;
        color: {COLORS['text_dark']} !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {COLORS['primary']} !important;
        box-shadow: 0 0 0 4px rgba(107, 70, 193, 0.15) !important;
        background-color: rgba(139, 92, 246, 0.02) !important;
    }}
    
    label {{
        color: {COLORS['text_dark']} !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem;
    }}
    </style>
    """
    st.markdown(auth_css, unsafe_allow_html=True)
