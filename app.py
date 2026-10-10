import base64
import io
import math
import os
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image

# Plotly library check for Live 3D Visualization & Toolpath
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# PDF Generation library check
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# Page Configuration
st.set_page_config(
    page_title="MEGALA CNC MATE - Industrial Suite & Quotation Master",
    page_icon="⚙️",
    layout="wide",
)

# Helper function to convert logo safely
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_base64 = get_image_base64("logo.png")

# Session states initialization
if "shop_floor_mode" not in st.session_state:
    st.session_state.shop_floor_mode = False
if "nav_menu" not in st.session_state:
    st.session_state.nav_menu = "Home Dashboard"
if "calc_results" not in st.session_state:
    st.session_state.calc_results = None
if "cloud_sync_status" not in st.session_state:
    st.session_state.cloud_sync_status = "Synced (Cloud Active)"

if "stock_db" not in st.session_state:
    st.session_state.stock_db = pd.DataFrame([
        {"Material": "EN8 Round Bar - 12mm", "Unit": "Meter", "Available Stock": 120.50, "Status": "In Stock"},
        {"Material": "MS Round Bar - 20mm", "Unit": "Kg", "Available Stock": 45.20, "Status": "Low Stock"},
        {"Material": "SS304 Round Bar - 25mm", "Unit": "Meter", "Available Stock": 85.00, "Status": "In Stock"},
    ])

# Dynamic CSS based on Shop Floor Mode (Touch Friendly & Large UI for Mobile)
sf_padding = "20px" if st.session_state.shop_floor_mode else "12px"
sf_font_size = "18px" if st.session_state.shop_floor_mode else "15px"
sf_button_height = "64px" if st.session_state.shop_floor_mode else "48px"

st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(135deg, #050B18 0%, #0A1428 50%, #040711 100%);
    color: #FFFFFF;
    font-family: 'Segoe UI', Roboto, Helvetica, sans-serif;
    touch-action: manipulation;
}}
.brand-container {{
    text-align: center;
    padding: 20px 0;
    background: radial-gradient(circle at center, #0F1C3F 0%, #070B19 100%);
    border-bottom: 2px solid #1E3A8A;
    margin-bottom: 15px;
    border-radius: 0 0 20px 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
}}
.logo-glow-box {{
    display: inline-block;
    padding: 8px;
    background: radial-gradient(circle, rgba(72, 202, 228, 0.3) 0%, rgba(10, 20, 40, 0.95) 100%);
    border-radius: 50%;
    box-shadow: 0 0 30px rgba(72, 202, 228, 0.8), inset 0 0 15px rgba(72, 202, 228, 0.5);
    border: 2px solid #48CAE4;
    margin-bottom: 10px;
}}
.logo-glow-box img {{
    width: 70px !important;
    height: auto !important;
    border-radius: 50%;
    display: block;
    margin: auto;
}}
.brand-title {{
    font-size: 28px;
    font-weight: 900;
    letter-spacing: 3px;
    background: linear-gradient(90deg, #48CAE4, #0077B6, #FFFFFF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: 4px;
    text-align: center;
    text-shadow: 0 0 25px rgba(72, 202, 228, 0.5);
}}
.brand-subtitle {{
    font-size: 11px;
    letter-spacing: 3px;
    color: #94A3B8;
    font-weight: 600;
    text-transform: uppercase;
    margin-top: 4px;
    text-align: center;
}}
.dashboard-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 25px;
}}
.dash-card {{
    background: linear-gradient(145deg, #111E38, #0B132B);
    padding: {sf_padding};
    border-radius: 16px;
    border: 1px solid #1E3A8A;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 140px;
    transition: all 0.3s ease;
}}
.dash-card:hover {{
    border-color: #48CAE4;
    box-shadow: 0 0 20px rgba(72, 202, 228, 0.4);
    transform: translateY(-3px);
}}
.dash-icon {{
    font-size: 32px;
    margin-bottom: 8px;
}}
.dash-label {{
    font-size: {sf_font_size};
    font-weight: 700;
    color: #F8FAFC;
    letter-spacing: 0.5px;
}}
.uniform-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    margin-bottom: 20px;
}}
.uniform-card {{
    background: linear-gradient(145deg, #111E38, #0B132B);
    padding: 15px;
    border-radius: 14px;
    border: 1px solid #1E3A8A;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 110px;
    box-sizing: border-box;
    transition: all 0.3s ease;
}}
.uniform-card:hover {{
    border-color: #48CAE4;
    box-shadow: 0 0 15px rgba(72, 202, 228, 0.4);
}}
.card-title {{
    font-size: 13px;
    font-weight: 700;
    color: #94A3B8;
    margin-bottom: 5px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
.card-value {{
    font-size: 18px;
    font-weight: 900;
    color: #48CAE4;
}}
.stButton>button {{
    width: 100%;
    background: linear-gradient(90deg, #1D4ED8, #00B4D8);
    color: white;
    font-weight: bold;
    border-radius: 12px;
    height: {sf_button_height};
    border: none;
    box-shadow: 0 4px 15px rgba(29, 78, 216, 0.4);
    transition: all 0.2s ease;
    font-size: {sf_font_size};
    cursor: pointer;
}}
.stButton>button:hover {{
    background: linear-gradient(90deg, #2563EB, #06B6D4);
    box-shadow: 0 6px 20px rgba(6, 182, 212, 0.6);
}}
.upload-status-box {{
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(6, 182, 212, 0.2));
    border: 2px solid #10B981;
    padding: 18px;
    border-radius: 14px;
    margin-top: 15px;
    margin-bottom: 20px;
    box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
}}
.ai-badge {{
    background: linear-gradient(90deg, #8B5CF6, #3B82F6);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    display: inline-block;
    margin-bottom: 8px;
}}
</style>
""", unsafe_allow_html=True)

# Top Header Banner
if logo_base64:
    logo_display_html = f'<div class="logo-glow-box"><img src="data:image/png;base64,{logo_base64}" /></div>'
else:
    logo_display_html = '<div style="font-size: 35px; margin-bottom: 2px;">⚙️</div>'

header_html = f"""
<div class="brand-container">
    {logo_display_html}
    <div class="brand-title">MEGALA CNC MATE</div>
    <div class="brand-subtitle">INDUSTRIAL CNC, TRAUB & PROFESSIONAL QUOTATION SUITE</div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

def navigate_to(menu_name):
    st.session_state.nav_menu = menu_name

# Helper for 3D Shape Mesh
def generate_3d_shape_mesh(shape, size, length, inner_dia=0.0):
    z_vals = np.linspace(0, length, 30)
    theta = np.linspace(0, 2 * np.pi, 60)
    Theta, Z = np.meshgrid(theta, z_vals)

    if shape == "Round":
        R = size / 2.0
        X = R * np.cos(Theta)
        Y = R * np.sin(Theta)
        return [go.Surface(x=X, y=Y, z=Z, colorscale='viridis', showscale=False)]
    elif shape == "Tube":
        R_out = size / 2.0
        R_in = max(0.1, inner_dia / 2.0)
        X_out = R_out * np.cos(Theta)
        Y_out = R_out
