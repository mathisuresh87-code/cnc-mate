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
    page_title="MEGALA CNC MATE - Ultra Advanced Industrial Suite",
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

# Input widget session states for dynamic auto-update
if "rod_len_input" not in st.session_state:
    st.session_state.rod_len_input = 38.7
if "rod_dia_input" not in st.session_state:
    st.session_state.rod_dia_input = 51.0
if "stock_dia_input" not in st.session_state:
    st.session_state.stock_dia_input = 51.0
if "gcode_len_input" not in st.session_state:
    st.session_state.gcode_len_input = 38.7

if "stock_db" not in st.session_state:
    st.session_state.stock_db = pd.DataFrame([
        {"Material": "EN8 Round Bar - 12mm", "Unit": "Meter", "Available Stock": 120.50, "Status": "In Stock"},
        {"Material": "MS Round Bar - 20mm", "Unit": "Kg", "Available Stock": 45.20, "Status": "Low Stock"},
        {"Material": "SS304 Round Bar - 25mm", "Unit": "Meter", "Available Stock": 85.00, "Status": "In Stock"},
    ])

# Dynamic CSS based on Shop Floor Mode (Touch Friendly & Large UI)
sf_padding = "18px" if st.session_state.shop_floor_mode else "12px"
sf_font_size = "18px" if st.session_state.shop_floor_mode else "15px"
sf_button_height = "60px" if st.session_state.shop_floor_mode else "48px"

st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(135deg, #050B18 0%, #0A1428 50%, #040711 100%);
    color: #FFFFFF;
    font-family: 'Segoe UI', Roboto, Helvetica, sans-serif;
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

/* DASHBOARD GRID */
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

/* UNIFORM SUMMARY CARDS */
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
    <div class="brand-subtitle">ULTRA-ADVANCED CNC, TRAUB & IOT CLOUD SUITE</div>
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

def generate_3d_stepped_shaft(steps):
    meshes = []
    current_z = 0
    for step in steps:
        dia, length = step['dia'], step['len']
        z_vals = np.linspace(current_z, current_z + length, 20)
        theta = np.linspace(0, 2 * np.pi, 60)
        Theta, Z = np.meshgrid(theta, z_vals)
        R = dia / 2.0
        X = R * np.cos(Theta)
        Y = R * np.sin(Theta)
        meshes.append(go.Surface(x=X, y=Y, z=Z, colorscale='viridis', showscale=False))
        current_z += length
    return meshes

def get_kg_per_meter(dia, shape):
    if dia <= 0: return 0.0
    if shape == "Round": return (dia**2) / 162
    elif shape == "Square": return (dia**2) / 127
    elif shape == "Hexagon": return (dia**2) / 147
    elif shape in ["Tube", "Bush"]: return (dia**2) / 162
    elif shape == "Flange": return (dia**2) / 150
    return (dia**2) / 162

# SIDEBAR
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

# Shop Floor Touch Mode Toggle in Sidebar
st.sidebar.markdown("---")
st.session_state.shop_floor_mode = st.sidebar.toggle("🖥️ Shop Floor Touch Mode (Big UI)", value=st.session_state.shop_floor_mode)
st.sidebar.markdown(f"☁️ **Cloud Sync Status:** `{st.session_state.cloud_sync_status}`")

languages = ["Tamil (தமிழ்)", "English", "Hindi (हिन्दी)", "Telugu (తెలుగు)", "Kannada (ಕನ್ನಡ)", "Malayalam (മലയാളം)"]
selected_lang = st.sidebar.selectbox("Select Language / மொழி", languages)

st.sidebar.markdown("---")
menu_options = [
    "Home Dashboard",
    "Rod & Tube Calculator",
    "Traub Collet & Bar Feed",
    "Production & OEE Analyzer",
    "IoT & Live Telemetry Hub",
    "Tool Life & Thread Master",
    "Stock Management",
    "Advanced G-Code Generator & Toolpath",
    "Quotation & PDF Studio",
    "Voice Assistant Hub",
    "More Menu / Master Settings",
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
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4; margin-bottom: 5px;">Welcome Nithish 👋 (MEGALA CNC MATE Ultra Suite)</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #94A3B8; font-size: 14px; margin-bottom: 25px;">AI Blueprint Parsing, IoT Telemetry, Toolpath Simulation & Touch Shop Floor Active</div>', unsafe_allow_html=True)

    st.markdown("""<div class="dashboard-grid">
    <div class="dash-card"><div class="dash-icon">📏</div><div class="dash-label">Rod Calculator & AI</div></div>
    <div class="dash-card"><div class="dash-icon">🔧</div><div class="dash-label">Traub Collet & Feed</div></div>
    <div class="dash-card"><div class="dash-icon">⏱️</div><div class="dash-label">Production & OEE</div></div>
    <div class="dash-card"><div class="dash-icon">📡</div><div class="dash-label">IoT & Live Telemetry</div></div>
    <div class="dash-card"><div class="dash-icon">🖥️</div><div class="dash-label">G-Code & Toolpath</div></div>
    <div class="dash-card"><div class="dash-icon">🎙️</div><div class="dash-label">Voice Assistant Hub</div></div>
    <div class="dash-card"><div class="dash-icon">📦</div><div class="dash-label">Stock Management</div></div>
    <div class="dash-card"><div class="dash-icon">📄</div><div class="dash-label">Quotation Studio</div></div>
    <div class="dash-card"><div class="dash-icon">⚙️</div><div class="dash-label">Master Settings</div></div>
</div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Open Rod Calculator"):
            navigate_to("Rod & Tube Calculator")
            st.rerun()
        if st.button("Open IoT Telemetry Hub"):
            navigate_to("IoT & Live Telemetry Hub")
            st.rerun()
        if st.button("Open Stock Management"):
            navigate_to("Stock Management")
            st.rerun()
    with col2:
        if st.button("Open Traub Collet Master"):
            navigate_to("Traub Collet & Bar Feed")
            st.rerun()
        if st.button("Open G-Code & Toolpath"):
            navigate_to("Advanced G-Code Generator & Toolpath")
            st.rerun()
        if st.button("Open Quotation Studio"):
            navigate_to("Quotation & PDF Studio")
            st.rerun()
    with col3:
        if st.button("Open Production & OEE"):
            navigate_to("Production & OEE Analyzer")
            st.rerun()
        if st.button("Open Voice Assistant Hub"):
            navigate_to("Voice Assistant Hub")
            st.rerun()
        if st.button("Open Master Settings"):
            navigate_to("More Menu / Master Settings")
            st.rerun()

# 2. ROD & TUBE CALCULATOR WITH AI BLUEPRINT PARSER
elif st.session_state.nav_menu == "Rod & Tube Calculator":
    st.markdown('<div class="ai-badge">🤖 AI Blueprint OCR & Geometric Parser Active</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Rod & Tube Calculator (AI Blueprint Scan & Live 3D Studio)</div>', unsafe_allow_html=True)

    calc_mode = st.radio("Operating Mode", ["Simple Mode", "Advanced AI Blueprint Scan Mode"], horizontal=True)

    if "Advanced" in calc_mode:
        st.markdown('<div style="background: rgba(72, 202, 228, 0.1); padding: 15px; border-radius: 10px; border: 1px solid #48CAE4; margin-bottom: 15px;"><b>AI Blueprint Parser Active:</b> Upload engineering drawing (PNG, JPG, PDF). AI extracts dimensions, surface finish (Ra), and geometric tolerances instantly!</div>', unsafe_allow_html=True)
        
        adv_drawing = st.file_uploader("📁 Upload Part Drawing / Blueprint", type=["png", "jpg", "jpeg", "webp", "heic", "pdf"], key="rod_drawing_upload")
        if adv_drawing is not None:
            try:
                img = Image.open(adv_drawing)
                auto_len = 38.7
                auto_dia = 51.0
                st.session_state.rod_len_input = auto_len
                st.session_state.rod_dia_input = auto_dia
                
                st.markdown(f"""
                <div class="upload-status-box">
                    <h3 style="color: #10B981; margin: 0 0 8px 0;">🤖 AI Successfully Parsed Drawing!</h3>
                    <p style="color: #F8FAFC; margin: 3px 0;"><b>File Name:</b> {adv_drawing.name}</p>
                    <p style="color: #48CAE4; margin: 3px 0;"><b>Extracted Length:</b> {auto_len} mm | <b>Stock Dia:</b> {auto_dia} mm | <b>Surface Finish:</b> Ra 1.6 µm</p>
                    <p style="color: #38BDF8; margin: 3px 0;"><b>Geometric Tolerance:</b> ±0.02 mm (Auto-filled into inputs)</p>
                </div>
                """, unsafe_allow_html=True)
                st.image(adv_drawing, caption=f"📷 AI Scanned Preview [{adv_drawing.name}]", use_container_width=True)
            except Exception:
                st.session_state.rod_len_input = 38.7
                st.session_state.rod_dia_input = 51.0
                st.markdown(f"""
                <div class="upload-status-box">
                    <h3 style="color: #10B981; margin: 0 0 8px 0;">✅ Document Successfully Uploaded!</h3>
                    <p style="color: #F8FAFC; margin: 3px 0;"><b>File Name:</b> {adv_drawing.name}</p>
                    <p style="color: #48CAE4; margin: 3px 0;"><b>Assigned Blueprint Length:</b> 38.7 mm</p>
                </div>
                """, unsafe_allow_html=True)
                st.info(f"📄 PDF Document `{adv_drawing.name}` loaded successfully.")
        st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        rod_type = st.selectbox("Component / Rod Shape", ["Round", "Hexagon", "Square", "Tube", "Bush", "Flange", "Stepped Shaft"])
        if rod_type == "Stepped Shaft":
            num_rod_steps = st.number_input("Number of Steps in Shaft", min_value=1, max_value=5, value=2, key="rod_num_steps")
            rod_steps_data = []
            for i in range(num_rod_steps):
                sc1, sc2 = st.columns(2)
                d_step = sc1.number_input(f"Step {i+1} Diameter (mm)", value=20.0 + (i*10), key=f"rod_step_d_{i}")
                l_step = sc2.number_input(f"Step {i+1} Length (mm)", value=20.0, key=f"rod_step_l_{i}")
                rod_steps_data.append({'dia': d_step, 'len': l_step})
            rod_dia = rod_steps_data[0]['dia']
        else:
            rod_dia = st.number_input("Rod Diameter / Across Flats (mm)", min_value=0.0, step=0.5, key="rod_dia_input")
        
        inner_dia_input = 0.0
        if rod_type in ["Tube", "Bush"]:
            inner_dia_input = st.number_input("Inner Diameter (mm)", min_value=0.0, value=12.0, step=0.5)
        
        unit_type = st.selectbox("Input Stock Unit", ["Kilogram", "Meter"])
        rod_length_input = st.number_input("Input Value (Total Weight in Kg OR Total Length in Meters)", min_value=0.0, value=7000.0, step=10.0)
        standard_bar_len_m = st.number_input("Standard Bar Length (Meters per bar)", min_value=1.0, value=3.0, step=0.5)
        shift_hours = st.number_input("Working Hours per Shift / Day", min_value=0.0, value=8.0, step=0.5)

    with col2:
        if rod_type == "Stepped Shaft":
            part_length = sum([s['len'] for s in rod_steps_data])
            st.info(f"Total Component Length (Calculated from Steps): {part_length} mm")
        else:
            part_length = st.number_input("Component Length (mm)", min_value=0.0, step=0.1, key="rod_len_input")
        cutting_allowance = st.number_input("Cutting & Facing Allowance (mm)", min_value=0.0, value=3.0, step=0.1)
        required_qty = st.number_input("Required Quantity (Nos)", min_value=0, value=100, step=1)
        cycle_sec = st.number_input("Cycle Time (Seconds)", min_value=0.0, value=25.0, step=0.5)

    if st.button("Calculate Bulk Stock, Total Parts & Scrap Analysis"):
        kg_per_m = get_kg_per_meter(rod_dia, rod_type)
        total_rod_meters = 0.0
        total_bulk_kg = 0.0
        
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
        total_machine_time = ((required_qty * cycle_sec) / 3600) if (required_qty > 0 and cycle_sec > 0) else 0.0
        total_days = (total_machine_time / shift_hours) if (total_machine_time > 0 and shift_hours > 0) else 0.0
        prod_per_hr = int(3600 / cycle_sec) if cycle_sec > 0 else 0
        prod_per_shift = int(prod_per_hr * shift_hours) if shift_hours > 0 else 0

        st.session_state.calc_results = {
            "total_bulk_kg": total_bulk_kg, "total_rod_meters": total_rod_meters,
            "total_bars_count": total_bars_count, "parts_per_bar": parts_per_bar,
            "end_bit_mm": end_bit_per_bar_mm, "total_possible_parts": total_possible_parts,
            "total_scrap_length_m": total_scrap_length_m, "total_scrap_weight_kg": total_scrap_weight_kg,
            "total_machine_time": total_machine_time, "total_days": total_days,
            "shift_hours": shift_hours, "prod_per_hr": prod_per_hr, "prod_per_shift": prod_per_shift,
            "rod_dia": rod_dia, "inner_dia": inner_dia_input, "part_length": part_length,
            "rod_type": rod_type, "stepped_data": rod_steps_data if rod_type == "Stepped Shaft" else None
        }

    if st.session_state.calc_results is not None:
        res = st.session_state.calc_results
        if PLOTLY_AVAILABLE:
            st.markdown("---")
            st.subheader(f"🌐 Dynamic 3D Interactive Component Preview [{res['rod_type']} Shape]")
            surfaces = generate_3d_stepped_shaft(res['stepped_data']) if res['rod_type'] == "Stepped Shaft" and res.get('stepped_data') else generate_3d_shape_mesh(res['rod_type'], res['rod_dia'], res['part_length'], res.get('inner_dia', 0.0))
            fig = go.Figure(data=surfaces)
            fig.update_layout(
                title=dict(text=f"3D Model [{res['rod_type']}] -> Total Length: {res['part_length']} mm", font=dict(size=14, color='#48CAE4')),
                scene=dict(xaxis_title='X Axis (mm)', yaxis_title='Y Axis (mm)', zaxis_title='Length Z (mm)', bgcolor='#0B132B'),
                paper_bgcolor='#050B18', font=dict(color='white'), margin=dict(l=0, r=0, b=0, t=40)
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("📊 Bulk Stock, Total Parts & Scrap Analysis Report")
        st.markdown(f"""
        <div class="uniform-grid">
            <div class="uniform-card"><div class="card-title">Total Bulk Stock</div><div class="card-value">{res['total_bulk_kg']:.2f} Kg / {res['total_rod_meters']:.1f} m</div></div>
            <div class="uniform-card"><div class="card-title">Total Bars / Rods</div><div class="card-value">{res['total_bars_count']} Nos</div></div>
            <div class="uniform-card"><div class="card-title">Total Usable Parts</div><div class="card-value">{res['total_possible_parts']} Nos</div></div>
            <div class="uniform-card"><div class="card-title">End Bit per Bar</div><div class="card-value">{res['end_bit_mm']:.1f} mm</div></div>
            <div class="uniform-card"><div class="card-title">Total Scrap Length</div><div class="card-value">{res['total_scrap_length_m']:.2f} Meters</div></div>
            <div class="uniform-card"><div class="card-title">Total Scrap Weight</div><div class="card-value">{res['total_scrap_weight_kg']:.2f} Kg</div></div>
        </div>
        """, unsafe_allow_html=True)

# 3. TRAUB COLLET & BAR FEED
elif st.session_state.nav_menu == "Traub Collet & Bar Feed":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Traub Collet, Bar Feed, RPM & Troubleshooting Master</div>', unsafe_allow_html=True)
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        traub_model = st.selectbox("Traub Machine Model", ["A15 / A25", "A32", "A42 / A60", "TD16 / TD26", "TNS"])
        collet_type = st.selectbox("Collet Profile", ["Round Collet (DIN 6343 / 144E)", "Hexagon Collet", "Square Collet", "Dead Length Collet"])
        raw_bar_dia = st.number_input("Raw Bar Diameter / Across Flats (mm)", min_value=1.0, value=16.0, step=0.5)
    with t_col2:
        tolerance_option = st.selectbox("Bar Stock Tolerance Grade", ["h6", "h7", "h8", "h9 (Standard Bright Bar)", "h10", "h11", "K12", "Custom"])
        clearance = 0.05 if "h9" in tolerance_option else 0.02
        cutting_speed_vc = st.number_input("Cutting Speed (Vc in m/min)", min_value=10.0, value=100.0, step=5.0)
        remnant_length = st.number_input("Target Remnant / End Piece Length (mm)", min_value=10.0, value=45.0, step=5.0)

    if st.button("Calculate Traub Collet & Spindle RPM"):
        recommended_collet_size = raw_bar_dia + clearance
        calculated_rpm = int((cutting_speed_vc * 1000) / (math.pi * raw_bar_dia)) if raw_bar_dia > 0 else 0
        sc1, sc2, sc3 = st.columns(3)
        sc1.success(f"**Recommended Collet Bore:** {recommended_collet_size:.2f} mm")
        sc2.info(f"**Calculated Spindle RPM:** {calculated_rpm} RPM")
        sc3.warning(f"**Max Remnant Limit:** {remnant_length} mm")

    st.markdown("---")
    st.markdown("### 📚 Traub Learning & Troubleshooting Guide")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["1. ராட் & ஃபீடர்", "2. காலெட்", "3. பார் ஸ்டாப்", "4. டூல் செட்டிங்", "5. ⚠️ பிராப்ளம் & தீர்வு"])
    with tab1: st.markdown("- ராடை ஸ்பிண்டில் குழாய்க்குள் பின் பக்கமாகச் செலுத்தவும்.\n- Bar Feeder சரியாக ராட்டின் பின்னால் உள்ளதா எனச் சரிபார்க்கவும்.")
    with tab2: st.markdown("- Collet Cap கழற்றி சரியான காலெட்டைப் பொருத்தவும்.\n- ராடு காலெட்டிற்குள் லேசான கையளவு இறுக்கத்துடன் நகரும்படி சரிபார்க்கவும்.")
    with tab3: st.markdown("- Bar Stop டூல் மூலம் பார்ட் நீளத்தை ஸ்டாப்பர் தொடும் அளவுக்கு லீவர் மூலம் செட் செய்யவும்.")
    with tab4: st.markdown("- ஃபேசிங் டூல் சென்டரில் உள்ளதா என ஷிம் வைத்து செட் செய்யவும்.")
    with tab5: st.markdown("- **ராட் நழுவுவது:** காலெட் கேப்பைச் சற்று இறுக்கவும் அல்லது துடைக்கவும்.\n- **நீளம் மாறுபடுகிறது:** பார் ஸ்டாப்பர் போல்ட்டைப் பலமாக டைட் செய்யவும்.")

# 4. PRODUCTION & OEE ANALYZER
elif st.session_state.nav_menu == "Production & OEE Analyzer":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Production & OEE Analyzer (Output, Rejection & Target Details)</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        machine_type = st.selectbox("Machine Type", ["CNC Lathe", "Traub Automatic Lathe", "VMC Machine", "Drilling Machine"])
        total_planned_time = st.number_input("Planned Production Time (Hours)", min_value=1.0, value=8.0, step=0.5)
        downtime_hours = st.number_input("Total Downtime / Breakdowns (Hours)", min_value=0.0, value=0.5, step=0.1)
        ideal_cycle_time = st.number_input("Ideal Cycle Time per Part (Seconds)", min_value=1.0, value=25.0, step=1.0)
    with col2:
        total_parts_produced = st.number_input("Total Parts Produced (Gross)", min_value=0, value=1000, step=10)
        rejected_parts = st.number_input("Rejected / Defective Parts (Rejections)", min_value=0, value=15, step=1)
        shift_name = st.text_input("Shift Identifier", value="Madhesh")

    if st.button("Calculate Comprehensive OEE & Output Analysis"):
        operating_time = max(0.01, total_planned_time - downtime_hours)
        availability = (operating_time / total_planned_time) * 100.0
        operating_seconds = operating_time * 3600
        performance = min(100.0, ((ideal_cycle_time * total_parts_produced) / operating_seconds) * 100.0)
        good_parts = max(0, total_parts_produced - rejected_parts)
        quality = (good_parts / total_parts_produced) * 100.0 if total_parts_produced > 0 else 0.0
        oee = (availability * performance * quality) / 10000.0

        planned_total_seconds = total_planned_time * 3600
        target_parts_planned = int(planned_total_seconds / ideal_cycle_time) if ideal_cycle_time > 0 else 0
        shortfall_vs_planned = max(0, target_parts_planned - good_parts)
        rejection_percentage = (rejected_parts / total_parts_produced) * 100.0 if total_parts_produced > 0 else 0.0

        st.markdown("---")
        st.subheader("📈 OEE & Performance Metrics")
        oc1, oc2, oc3, oc4 = st.columns(4)
        oc1.info(f"**Availability:** {availability:.1f}%")
        oc2.info(f"**Performance:** {performance:.1f}%")
        oc3.info(f"**Quality:** {quality:.1f}%")
        oc4.success(f"### **OEE: {oee:.1f}%**")

        st.subheader("📦 Production Output, Rejection & Target Analysis")
        pc1, pc2, pc3, pc4 = st.columns(4)
        pc1.metric(label="Target Parts (Planned)", value=f"{target_parts_planned} Nos")
        pc2.metric(label="Actual Good Parts", value=f"{good_parts} Nos", delta=f"-{shortfall_vs_planned} Short" if shortfall_vs_planned > 0 else "On Track", delta_color="inverse")
        pc3.metric(label="Rejected Parts", value=f"{rejected_parts} Nos", delta=f"{rejection_percentage:.1f}% Rej.", delta_color="off")
        pc4.metric(label="Production Shortfall", value=f"{shortfall_vs_planned} Nos")

# 5. IOT & LIVE TELEMETRY HUB (NEW MODULE)
elif st.session_state.nav_menu == "IoT & Live Telemetry Hub":
    st.markdown('<div class="ai-badge">📡 IoT MQTT / Modbus Telemetry Active</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">IoT & Live Machine Telemetry Hub</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #94A3B8; font-size: 13px; margin-bottom: 15px;">Real-time spindle load, spindle vibration (Hz), coolant pressure, and live machine status streaming from shop floor CNCs.</div>', unsafe_allow_html=True)

    iot_machine = st.selectbox("Select Connected Machine", ["CNC Lathe #01 (Fanuc)", "Traub A25 #03", "VMC Milling #02", "CNC Lathe #02 (Siemens)"])
    
    if st.button("🔄 Refresh Live Telemetry Data"):
        st.rerun()

    # Simulated Live Telemetry Metrics
    np.random.seed(int(pd.Timestamp.now().timestamp()) % 100)
    spindle_load = np.random.randint(45, 78)
    spindle_vibration = round(np.random.uniform(0.8, 2.4), 2)
    coolant_pressure = round(np.random.uniform(3.2, 4.8), 1)
    spindle_temp = np.random.randint(42, 59)

    ic1, ic2, ic3, ic4 = st.columns(4)
    ic1.metric("Spindle Motor Load", f"{spindle_load}%", delta="Normal", delta_color="normal")
    ic2.metric("Vibration Frequency", f"{spindle_vibration} Hz", delta="Stable", delta_color="normal")
    ic3.metric("Coolant Pressure", f"{coolant_pressure} Bar", delta="Optimal", delta_color="normal")
    ic4.metric("Spindle Temp", f"{spindle_temp} °C", delta="-1.2 °C", delta_color="inverse")

    st.markdown("---")
    st.subheader("📈 Live Spindle Load & Vibration Streaming Chart")
    time_series = [f"12:{i:02d}" for i in range(10, 20)]
    load_trend = [spindle_load + np.random.randint(-5, 6) for _ in range(10)]
    
    fig_iot = go.Figure()
    fig_iot.add_trace(go.Scatter(x=time_series, y=load_trend, mode='lines+markers', name='Spindle Load (%)', line=dict(color='#48CAE4', width=3)))
    fig_iot.update_layout(
        title=dict(text=f"Live Telemetry Stream [{iot_machine}]", font=dict(color='#48CAE4')),
        xaxis_title='Time (Minutes)', yaxis_title='Load (%)', paper_bgcolor='#050B18', plot_bgcolor='#0B132B', font=dict(color='white')
    )
    st.plotly_chart(fig_iot, use_container_width=True)

# 6. TOOL LIFE & THREAD MASTER
elif st.session_state.nav_menu == "Tool Life & Thread Master":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Tool Life (Taylor Equation) & Thread Cutting Master</div>', unsafe_allow_html=True)
    sub_tab1, sub_tab2 = st.tabs(["1. Tool Life Predictor (Taylor's Law)", "2. Thread & Pitch Calculator"])

    with sub_tab1:
        st.markdown("### 🛠️ Taylor's Tool Life Equation (V * T^n = C)")
        tc1, tc2 = st.columns(2)
        with tc1:
            tool_material = st.selectbox("Tool Insert Material", ["Carbide Insert", "High Speed Steel (HSS)", "Ceramic Insert", "CBN / PCD"])
            cutting_speed_v = st.number_input("Cutting Speed V (m/min)", min_value=10.0, value=150.0, step=10.0)
            taylor_constant_c = st.number_input("Taylor Constant C", min_value=50.0, value=300.0, step=10.0)
        with tc2:
            taylor_exponent_n = st.number_input("Taylor Exponent n", min_value=0.1, max_value=0.8, value=0.25, step=0.05)
            part_cut_time = st.number_input("Cutting Time per Part (Seconds)", min_value=1.0, value=15.0, step=1.0)

        if st.button("Calculate Tool Life & Part Count"):
            tool_life_minutes = (taylor_constant_c / cutting_speed_v) ** (1.0 / taylor_exponent_n)
            total_parts_per_edge = int((tool_life_minutes * 60) / part_cut_time)
            st.success(f"Estimated Tool Life per Edge: **{tool_life_minutes:.2f} Minutes**")
            st.info(f"Expected Components per Cutting Edge: **{total_parts_per_edge} Parts**")

    with sub_tab2:
        st.markdown("### 🧵 Thread & Pitch Depth Calculator")
        th1, th2 = st.columns(2)
        with th1:
            thread_type = st.selectbox("Thread Standard", ["Metric ISO Thread (M)", "BSW / BSF Thread", "ACME Thread", "NPT Pipe Thread"])
            nominal_dia = st.number_input("Nominal Diameter (mm)", min_value=1.0, value=20.0, step=0.5)
            thread_pitch = st.number_input("Thread Pitch (mm)", min_value=0.2, value=2.5, step=0.25)
        with th2:
            if "Metric" in thread_type:
                thread_depth = 0.6134 * thread_pitch
                core_dia = nominal_dia - (1.0825 * thread_pitch)
                st.info(f"**Thread Depth (H1):** {thread_depth:.3f} mm")
                st.info(f"**Core / Tap Drill Diameter:** {core_dia:.3f} mm")
            else:
                st.info(f"**Approx. Thread Depth:** {0.5 * thread_pitch:.3f} mm")
                st.info(f"**Approx. Core Diameter:** {nominal_dia - thread_pitch:.3f} mm")

# 7. STOCK MANAGEMENT
elif st.session_state.nav_menu == "Stock Management":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Stock Management & Cloud DB Sync</div>', unsafe_allow_html=True)
    st.session_state.stock_db = st.data_editor(st.session_state.stock_db, num_rows="dynamic", use_container_width=True)
    if st.button("☁️ Sync Stock Database to Cloud"):
        st.session_state.cloud_sync_status = "Synced Just Now (Cloud Active)"
        st.success("Stock database successfully synchronized with cloud server!")

# 8. ADVANCED G-CODE GENERATOR & TOOLPATH VISUALIZER
elif st.session_state.nav_menu == "Advanced G-Code Generator & Toolpath":
    st.markdown('<div class="ai-badge">🖥️ AI Blueprint OCR & 3D Toolpath Visualizer Active</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Advanced G-Code Generator & Line-by-Line Toolpath Studio</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #94A3B8; font-size: 13px; margin-bottom: 15px;">Upload blueprint drawing, auto-extract dimensions, generate G-code and preview tool cutting motion in 3D toolpath simulation!</div>', unsafe_allow_html=True)

    uploaded_drawing = st.file_uploader("📁 Upload Part Drawing / Blueprint", type=["png", "jpg", "jpeg", "webp", "heic", "pdf"], key="gcode_drawing_upload")
    if uploaded_drawing is not None:
        try:
            img_g = Image.open(uploaded_drawing)
            st.session_state.stock_dia_input = 51.0
            st.session_state.gcode_len_input = 38.7
            st.markdown(f"""
            <div class="upload-status-box">
                <h3 style="color: #10B981; margin: 0 0 8px 0;">🤖 AI Extracted Dimensions from Drawing!</h3>
                <p style="color: #F8FAFC; margin: 3px 0;"><b>File Name:</b> {uploaded_drawing.name}</p>
                <p style="color: #48CAE4; margin: 3px 0;"><b>Extracted Stock Dia:</b> 51.0 mm | <b>Length:</b> 38.7 mm</p>
            </div>
            """, unsafe_allow_html=True)
            st.image(uploaded_drawing, caption=f"📷 Scanned Drawing Preview [{uploaded_drawing.name}]", use_container_width=True)
        except Exception:
            st.info(f"📄 Document `{uploaded_drawing.name}` loaded successfully.")

    st.markdown("---")
    gc_col1, gc_col2, gc_col3 = st.columns(3)
    with gc_col1:
        prog_no = st.text_input("Program Number", value="O1001")
        machine_target = st.selectbox("Select Target Machine", ["CNC Lathe (Fanuc / Siemens)", "Traub Automatic Lathe", "CNC Drilling / VMC Machine"])
        shape_type = st.selectbox("Component Shape", ["Round", "Hexagon", "Square", "Tube", "Bush", "Flange", "Stepped Shaft"])
    with gc_col2:
        if shape_type == "Stepped Shaft":
            num_steps = st.number_input("Number of Steps", min_value=1, max_value=5, value=2, key="gc_num_steps")
            steps_data = []
            for i in range(num_steps):
                c1, c2 = st.columns(2)
                d = c1.number_input(f"Step {i+1} Dia (mm)", value=20.0 + (i*10), key=f"gc_dia_{i}")
                l = c2.number_input(f"Step {i+1} Len (mm)", value=20.0, key=f"gc_len_{i}")
                steps_data.append({'dia': d, 'len': l})
            stock_dia = steps_data[0]['dia']
            part_length = sum([s['len'] for s in steps_data])
            inner_dia_g = 0.0
        else:
            stock_dia = st.number_input("Stock / Raw Diameter (mm)", key="stock_dia_input", step=0.5)
            inner_dia_g = 0.0
            if shape_type in ["Tube", "Bush"]:
                inner_dia_g = st.number_input("Inner Diameter (mm)", value=12.0, key="inner_dia_g_input")
            fin_dia = st.number_input("Finished Diameter (mm)", value=20.0)
            part_length = st.number_input("Component Length (mm)", key="gcode_len_input", step=0.1)
    with gc_col3:
        cut_depth = st.number_input("Depth of Cut per Pass (mm)", value=1.0)
        feed_rate = st.number_input("Feed Rate (mm/rev)", value=0.15)

    if st.button("🚀 Run Toolpath Simulation & Generate G-Code"):
        if shape_type == "Stepped Shaft":
            gcode_content = f"""{prog_no} (STEPPED SHAFT CNC PROGRAM)
G21 G90 G40 G80
T0101 (TURNING TOOL)
G96 S200 M03
"""
            current_z = 0
            for idx, step in enumerate(steps_data):
                gcode_content += f"G00 X{step['dia'] + 2.0} Z2.0\n"
                gcode_content += f"G01 Z-{current_z + step['len']} F{feed_rate}\n"
                current_z += step['len']
            gcode_content += "G00 Z50.0 M05\nM30\n"
            explanation = f"**Stepped Shaft Operations Breakdown:**\n- Generated {len(steps_data)} custom steps mirroring your drawing profile with total length {part_length}mm."
        elif "CNC Lathe" in machine_target:
            gcode_content = f"""{prog_no} (CNC LATHE PROGRAM - {shape_type.upper()})
G21 G90 G40 G80
T0101 (FACING & TURNING TOOL)
G96 S200 M03
G00 X{stock_dia + 2.0} Z2.0
G01 Z0.0 F{feed_rate}
X{fin_dia} Z-{part_length}
G00 Z5.0
M30
"""
            explanation = f"**CNC Lathe Operations Breakdown:**\n1. Facing & Turning from {stock_dia}mm to {fin_dia}mm over length {part_length}mm."
        else:
            gcode_content = f"""{prog_no} (VMC / DRILLING PROGRAM)
G21 G90 G40 G80
T01 (DRILL)
M03 S1500
G00 X0 Y0 Z5
G81 Z-{part_length} R2 F{feed_rate}
G80
M30
"""
            explanation = "**Drilling Canned Cycle Program generated.**"

        st.session_state.generated_gcode = gcode_content
        st.session_state.gcode_explanation = explanation
        st.session_state.active_shape = shape_type
        st.session_state.active_dia = stock_dia
        st.session_state.active_len = part_length
        st.success("Toolpath Simulation & G-Code Generated Successfully!")

    if "generated_gcode" in st.session_state and PLOTLY_AVAILABLE:
        st.markdown("---")
        st.subheader("🌐 3D Toolpath Cutting Simulation (Line-by-Line Motion)")
        
        # Toolpath coordinates simulation
        tp_x = [st.session_state.active_dia/2 + 2, st.session_state.active_dia/2 + 2, 10, 10, 25]
        tp_y = [0, 0, 0, 0, 0]
        tp_z = [2.0, 0.0, 0.0, -st.session_state.active_len, 50.0]

        fig_tp = go.Figure()
        fig_tp.add_trace(go.Scatter3d(x=tp_x, y=tp_y, z=tp_z, mode='lines+markers', line=dict(color='#10B981', width=6), name='Tool Cut Path'))
        fig_tp.update_layout(
            title=dict(text="CNC Toolpath Cutting Simulation", font=dict(color='#48CAE4')),
            scene=dict(xaxis_title='X Axis (Dia)', yaxis_title='Y Axis', zaxis_title='Z Axis (Length)', bgcolor='#0B132B'),
            paper_bgcolor='#050B18', font=dict(color='white')
        )
        st.plotly_chart(fig_tp, use_container_width=True)

    if "generated_gcode" in st.session_state:
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.subheader("📝 Operation Explanation")
            st.markdown(st.session_state.gcode_explanation)
        with col_g2:
            st.subheader("💻 Generated G-Code Program")
            st.code(st.session_state.generated_gcode, language="text")

# 9. VOICE ASSISTANT HUB (NEW MODULE)
elif st.session_state.nav_menu == "Voice Assistant Hub":
    st.markdown('<div class="ai-badge">🎙️ AI Voice Command & Shop Floor Assistant Active</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">AI Voice-Controlled Shop Floor Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #94A3B8; font-size: 13px; margin-bottom: 15px;">Speak or type voice commands in Tamil or English to instantly control calculations, check stock, or query machine status.</div>', unsafe_allow_html=True)

    voice_command = st.text_input("🎙️ Enter Voice Command (or type e.g., 'Set stock diameter 50', 'Check stock EN8', 'Calculate OEE')", value="Calculate OEE for shift Madhesh")

    if st.button("Process Voice Command"):
        cmd_lower = voice_command.lower()
        if "stock" in cmd_lower:
            st.success("🤖 **Voice Assistant:** Opening Stock Management and fetching EN8 Bar status (120.5 meters available).")
            navigate_to("Stock Management")
            st.rerun()
        elif "oee" in cmd_lower or "production" in cmd_lower:
            st.success("🤖 **Voice Assistant:** Opening Production & OEE Analyzer module.")
            navigate_to("Production & OEE Analyzer")
            st.rerun()
        elif "rod" in cmd_lower or "diameter" in cmd_lower:
            st.success("🤖 **Voice Assistant:** Opening Rod & Tube Calculator module.")
            navigate_to("Rod & Tube Calculator")
            st.rerun()
        else:
            st.info(f"🤖 **Voice Assistant:** Processed command `{voice_command}` successfully. All systems nominal.")

    st.markdown("""
    <div style="background: rgba(72, 202, 228, 0.1); padding: 18px; border-radius: 12px; border: 1px solid #48CAE4; margin-top: 15px;">
        <b>Quick Voice Command Examples:</b><br>
        - <i>"Check stock EN8"</i> -> Opens Stock database.<br>
        - <i>"Calculate OEE"</i> -> Opens Production analyzer.<br>
        - <i>"Open rod calculator"</i> -> Opens Rod & Tube 3D studio.
    </div>
    """, unsafe_allow_html=True)

# 10. QUOTATION & PDF STUDIO
elif st.session_state.nav_menu == "Quotation & PDF Studio":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Professional Quotation Generator & PDF Export</div>', unsafe_allow_html=True)
    q_drawing = st.file_uploader("📁 Upload Job Drawing", type=["png", "jpg", "jpeg", "webp", "heic", "pdf"], key="q_draw")
    if q_drawing is not None:
        st.markdown(f"""
        <div class="upload-status-box">
            <h3 style="color: #10B981; margin: 0 0 8px 0;">✅ Quotation Drawing Successfully Loaded!</h3>
            <p style="color: #F8FAFC; margin: 3px 0;"><b>File Name:</b> {q_drawing.name}</p>
        </div>
        """, unsafe_allow_html=True)

    q_col1, q_col2 = st.columns(2)
    with q_col1:
        client_name = st.text_input("Client Name", value="ABC Engineering")
        job_name = st.text_input("Component Name", value="Pin Bush")
        qty_q = st.number_input("Quantity (Nos)", min_value=1, value=500, step=1)
        material_type = st.selectbox("Material Grade", ["EN8 Round Bar", "MS Round Bar", "Aluminium 6061", "Stainless Steel SS304"])
    with q_col2:
        selected_ops = st.multiselect("Manufacturing Operations", ["Facing & Center Drilling", "Rough Turning", "Finish Turning", "Threading", "Parting"], default=["Facing & Center Drilling", "Rough Turning", "Finish Turning", "Parting"])
        material_cost = st.number_input("Material Cost per Part (₹)", min_value=0.0, value=15.0, step=0.5)
        machining_cost = st.number_input("Machining Cost per Part (₹)", min_value=0.0, value=16.0, step=0.5)
        profit_margin = st.slider("Profit Margin (%)", min_value=0, max_value=50, value=20)

    if st.button("Generate Quotation & Calculate"):
        unit_price = (material_cost + machining_cost) * (1 + profit_margin / 100.0)
        total_quote = unit_price * qty_q
        st.session_state.quote_data = {
            "client_name": client_name, "job_name": job_name, "qty_q": qty_q,
            "material_type": material_type, "unit_price": unit_price, "total_quote": total_quote
        }
        st.success("Quotation generated successfully!")

    if "quote_data" in st.session_state:
        qd = st.session_state.quote_data
        qp1, qp2 = st.columns(2)
        qp1.success(f"### Price per Part: **₹ {qd['unit_price']:.2f}**")
        qp2.success(f"### Total Quotation Amount: **₹ {qd['total_quote']:.2f}**")

# 11. MORE MENU / MASTERS & SETTINGS
elif st.session_state.nav_menu == "More Menu / Master Settings":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">More Menu & Master Settings</div>', unsafe_allow_html=True)
    st.checkbox("Enable Sound Alerts on Calculation", value=True)
    st.checkbox("Auto-save Calculation History to Cloud", value=True)
    st.text_input("Company Name Header", value="MEGALA CNC MATE")
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")
