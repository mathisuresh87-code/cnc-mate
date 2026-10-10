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
        Y_out = R_out * np.sin(Theta)
        X_in = R_in * np.cos(Theta)
        Y_in = R_in * np.sin(Theta)
        return [
            go.Surface(x=X_out, y=Y_out, z=Z, colorscale='blues', showscale=False),
            go.Surface(x=X_in, y=Y_in, z=Z, colorscale='greys', showscale=False)
        ]
    elif shape == "Flange":
        z_vals_f = np.linspace(0, length * 0.3, 15)
        z_vals_b = np.linspace(length * 0.3, length, 20)
        Th_f, Z_f = np.meshgrid(theta, z_vals_f)
        Th_b, Z_b = np.meshgrid(theta, z_vals_b)
        R_flange = size * 0.8
        R_body = size * 0.4
        X_f = R_flange * np.cos(Th_f)
        Y_f = R_flange * np.sin(Th_f)
        X_b = R_body * np.cos(Th_b)
        Y_b = R_body * np.sin(Th_b)
        return [
            go.Surface(x=X_f, y=Y_f, z=Z_f, colorscale='plasma', showscale=False),
            go.Surface(x=X_b, y=Y_b, z=Z_b, colorscale='viridis', showscale=False)
        ]
    elif shape == "Bush":
        z_vals_b = np.linspace(0, length, 30)
        Th_b, Z_b = np.meshgrid(theta, z_vals_b)
        R_out = size / 2.0
        R_in = max(0.1, (size * 0.6) / 2.0)
        X_out = R_out * np.cos(Th_b)
        Y_out = R_out * np.sin(Th_b)
        X_in = R_in * np.cos(Th_b)
        Y_in = R_in * np.sin(Th_b)
        return [
            go.Surface(x=X_out, y=Y_out, z=Z_b, colorscale='teal', showscale=False),
            go.Surface(x=X_in, y=Y_in, z=Z_b, colorscale='copper', showscale=False)
        ]
    elif shape in ["Square", "Hexagon"]:
        n_sides = 6 if shape == "Hexagon" else 4
        half_angle = np.pi / n_sides
        r_poly = (size / 2.0) * np.cos(half_angle) / np.cos((Theta % (2 * np.pi / n_sides)) - half_angle)
        X = r_poly * np.cos(Theta)
        Y = r_poly * np.sin(Theta)
        return [go.Surface(x=X, y=Y, z=Z, colorscale='plasma', showscale=False)]
    else:
        R = size / 2.0
        X = R * np.cos(Theta)
        Y = R * np.sin(Theta)
        return [go.Surface(x=X, y=Y, z=Z, colorscale='viridis', showscale=False)]

def get_kg_per_meter(dia, shape):
    if dia <= 0: return 0.0
    if shape == "Round": return (dia**2) / 162
    elif shape == "Square": return (dia**2) / 127
    elif shape == "Hexagon": return (dia**2) / 147
    elif shape in ["Tube", "Bush"]: return (dia**2) / 162
    elif shape == "Flange": return (dia**2) / 150
    return (dia**2) / 162

# SIDEBAR CONTROL
if logo_base64:
    sidebar_logo_html = f"""
    <div style="text-align: center; padding: 10px 0 15px 0;">
        <div style="display: inline-block; padding: 6px; background: radial-gradient(circle, rgba(72, 202, 228, 0.3) 0%, rgba(10, 20, 40, 0.95) 100%); border-radius: 50%; box-shadow: 0 0 20px rgba(72, 202, 228, 0.7); border: 2px solid #48CAE4; margin-bottom: 8px;">
            <img src="data:image/png;base64,{logo_base64}" width="65" style="border-radius: 50%; display: block; margin: auto;">
        </div>
        <h2 style="color: #FFFFFF; margin: 5px 0 0 0; font-size: 18px; font-weight: 900; letter-spacing: 1.5px;">MEGALA CNC MATE</h2>
        <p style="color: #94A3B8; font-size: 10px; letter-spacing: 2px; text-transform: uppercase; margin-top: 3px;">Smart CNC. Simple Work.</p>
    </div>
    """
    st.sidebar.markdown(sidebar_logo_html, unsafe_allow_html=True)
else:
    st.sidebar.title("MEGALA CNC MATE")

# 100% Mobile Touch-Friendly Checkbox Control for Shop Floor Mode
st.sidebar.markdown("---")
st.session_state.shop_floor_mode = st.sidebar.checkbox(
    "🖥️ Shop Floor Touch Mode (Big UI)", 
    value=st.session_state.shop_floor_mode
)
if st.session_state.shop_floor_mode:
    st.sidebar.success("✅ Touch Mode Active (Big UI)")

st.sidebar.markdown(f"☁️ **Cloud Sync Status:** `{st.session_state.cloud_sync_status}`")

languages = ["Tamil (தமிழ்)", "English", "Hindi (हिन्दी)"]
selected_lang = st.sidebar.selectbox("Select Language / மொழி", languages)

st.sidebar.markdown("---")
menu_options = [
    "Home Dashboard",
    "Rod & Tube Calculator",
    "Traub Collet & Bar Feed",
    "Production & OEE Analyzer",
    "Stock Management",
    "Advanced G-Code & Toolpath Studio",
    "Professional Cost & Quotation Studio",
    "Master Settings"
]

selected_sidebar_menu = st.sidebar.radio(
    "Navigation Menu",
    menu_options,
    index=menu_options.index(st.session_state.nav_menu) if st.session_state.nav_menu in menu_options else 0,
)
if selected_sidebar_menu != st.session_state.nav_menu:
    st.session_state.nav_menu = selected_sidebar_menu
    st.rerun()

# 1. HOME DASHBOARD
if st.session_state.nav_menu == "Home Dashboard":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4; margin-bottom: 5px;">Welcome Nithish 👋 (MEGALA CNC MATE Suite)</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #94A3B8; font-size: 14px; margin-bottom: 25px;">Industrial CNC Calculations, 3D Toolpath & Professional Manufacturing Cost Quotation Engine Active</div>', unsafe_allow_html=True)

    st.markdown("""<div class="dashboard-grid">
    <div class="dash-card"><div class="dash-icon">📏</div><div class="dash-label">Rod & Weight Calculator</div></div>
    <div class="dash-card"><div class="dash-icon">🔧</div><div class="dash-label">Traub Collet & RPM</div></div>
    <div class="dash-card"><div class="dash-icon">⏱️</div><div class="dash-label">Production & OEE</div></div>
    <div class="dash-card"><div class="dash-icon">📦</div><div class="dash-label">Stock Management</div></div>
    <div class="dash-card"><div class="dash-icon">🖥️</div><div class="dash-label">G-Code & Toolpath Studio</div></div>
    <div class="dash-card"><div class="dash-icon">📄</div><div class="dash-label">Pro Quotation Studio</div></div>
</div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Open Rod Calculator"):
            navigate_to("Rod & Tube Calculator")
            st.rerun()
        if st.button("Open Stock Management"):
            navigate_to("Stock Management")
            st.rerun()
    with col2:
        if st.button("Open Traub Collet Master"):
            navigate_to("Traub Collet & Bar Feed")
            st.rerun()
        if st.button("Open G-Code & Toolpath"):
            navigate_to("Advanced G-Code & Toolpath Studio")
            st.rerun()
    with col3:
        if st.button("Open Production & OEE"):
            navigate_to("Production & OEE Analyzer")
            st.rerun()
        if st.button("Open Pro Quotation Studio"):
            navigate_to("Professional Cost & Quotation Studio")
            st.rerun()

# 2. ROD & TUBE CALCULATOR
elif st.session_state.nav_menu == "Rod & Tube Calculator":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Rod, Tube & Bulk Stock Calculator (3D Preview)</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        rod_type = st.selectbox("Component / Rod Shape", ["Round", "Hexagon", "Square", "Tube", "Bush", "Flange"])
        rod_dia = st.number_input("Rod Diameter / Across Flats (mm)", min_value=0.0, value=51.0, step=0.5)
        inner_dia_input = 0.0
        if rod_type in ["Tube", "Bush"]:
            inner_dia_input = st.number_input("Inner Diameter (mm)", min_value=0.0, value=12.0, step=0.5)
        unit_type = st.selectbox("Input Stock Unit", ["Kilogram", "Meter"])
        rod_length_input = st.number_input("Input Value (Total Weight in Kg OR Length in Meters)", min_value=0.0, value=7000.0, step=10.0)
        standard_bar_len_m = st.number_input("Standard Bar Length (Meters per bar)", min_value=1.0, value=3.0, step=0.5)

    with col2:
        part_length = st.number_input("Component Length (mm)", min_value=0.0, value=38.7, step=0.1)
        cutting_allowance = st.number_input("Cutting & Facing Allowance (mm)", min_value=0.0, value=3.0, step=0.1)
        required_qty = st.number_input("Required Quantity (Nos)", min_value=0, value=100, step=1)
        shift_hours = st.number_input("Working Hours per Shift", min_value=0.0, value=8.0, step=0.5)
        cycle_sec = st.number_input("Cycle Time (Seconds)", min_value=0.0, value=25.0, step=0.5)

    if st.button("Calculate Bulk Stock, Total Parts & Scrap"):
        kg_per_m = get_kg_per_meter(rod_dia, rod_type)
        if unit_type == "Kilogram":
            total_bulk_kg = rod_length_input
            total_rod_meters = (total_bulk_kg / kg_per_m) if kg_per_m > 0 else 0.0
        else:
            total_rod_meters = rod_length_input
            total_bulk_kg = total_rod_meters * kg_per_m

        total_part_len_mm = part_length + cutting_allowance
        parts_per_bar = int((standard_bar_len_m * 1000) / total_part_len_mm) if total_part_len_mm > 0 else 0
        end_bit_per_bar_mm = (standard_bar_len_m * 1000) - (parts_per_bar * total_part_len_mm) if parts_per_bar > 0 else 0.0
        total_bars_count = math.ceil(total_rod_meters / standard_bar_len_m) if standard_bar_len_m > 0 else 0
        total_possible_parts = total_bars_count * parts_per_bar
        total_scrap_length_m = (total_bars_count * end_bit_per_bar_mm) / 1000.0
        total_scrap_weight_kg = total_scrap_length_m * kg_per_m

        st.session_state.calc_results = {
            "total_bulk_kg": total_bulk_kg, "total_rod_meters": total_rod_meters,
            "total_bars_count": total_bars_count, "parts_per_bar": parts_per_bar,
            "end_bit_mm": end_bit_per_bar_mm, "total_possible_parts": total_possible_parts,
            "total_scrap_length_m": total_scrap_length_m, "total_scrap_weight_kg": total_scrap_weight_kg,
            "rod_dia": rod_dia, "inner_dia": inner_dia_input, "part_length": part_length, "rod_type": rod_type
        }

    if st.session_state.calc_results is not None:
        res = st.session_state.calc_results
        if PLOTLY_AVAILABLE:
            st.markdown("---")
            st.subheader(f"🌐 3D Interactive Component Preview [{res['rod_type']}]")
            surfaces = generate_3d_shape_mesh(res['rod_type'], res['rod_dia'], res['part_length'], res.get('inner_dia', 0.0))
            fig = go.Figure(data=surfaces)
            fig.update_layout(
                title=dict(text=f"3D Model [{res['rod_type']}] -> Length: {res['part_length']} mm", font=dict(size=14, color='#48CAE4')),
                scene=dict(xaxis_title='X Axis (mm)', yaxis_title='Y Axis (mm)', zaxis_title='Z Axis (mm)', bgcolor='#0B132B'),
                paper_bgcolor='#050B18', font=dict(color='white'), margin=dict(l=0, r=0, b=0, t=40)
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("📊 Analysis Report")
        st.markdown(f"""
        <div class="uniform-grid">
            <div class="uniform-card"><div class="card-title">Total Bulk Stock</div><div class="card-value">{res['total_bulk_kg']:.2f} Kg / {res['total_rod_meters']:.1f} m</div></div>
            <div class="uniform-card"><div class="card-title">Total Bars</div><div class="card-value">{res['total_bars_count']} Nos</div></div>
            <div class="uniform-card"><div class="card-title">Total Usable Parts</div><div class="card-value">{res['total_possible_parts']} Nos</div></div>
            <div class="uniform-card"><div class="card-title">End Bit
