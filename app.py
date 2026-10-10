import base64
import io
import math
import os
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image

# Plotly library check
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Page Configuration
st.set_page_config(
    page_title="MEGALA CNC MATE - Industrial Suite",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper function for logo
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_base64 = get_image_base64("logo.png")

# Session States
if "shop_floor_mode" not in st.session_state:
    st.session_state.shop_floor_mode = False
if "nav_menu" not in st.session_state:
    st.session_state.nav_menu = "Home Dashboard"
if "calc_results" not in st.session_state:
    st.session_state.calc_results = None

if "stock_db" not in st.session_state:
    st.session_state.stock_db = pd.DataFrame([
        {"Material": "EN8 Round Bar - 12mm", "Unit": "Meter", "Available Stock": 120.50, "Status": "In Stock"},
        {"Material": "MS Round Bar - 20mm", "Unit": "Kg", "Available Stock": 45.20, "Status": "Low Stock"},
        {"Material": "SS304 Round Bar - 25mm", "Unit": "Meter", "Available Stock": 85.00, "Status": "In Stock"},
    ])

# Dynamic CSS
sf_padding = "20px" if st.session_state.shop_floor_mode else "12px"
sf_font_size = "18px" if st.session_state.shop_floor_mode else "15px"
sf_button_height = "64px" if st.session_state.shop_floor_mode else "48px"

st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(135deg, #050B18 0%, #0A1428 50%, #040711 100%);
    color: #FFFFFF;
    font-family: 'Segoe UI', Roboto, sans-serif;
}}
.brand-container {{
    text-align: center;
    padding: 15px 0;
    background: radial-gradient(circle at center, #0F1C3F 0%, #070B19 100%);
    border-bottom: 2px solid #1E3A8A;
    margin-bottom: 15px;
    border-radius: 0 0 15px 15px;
}}
.brand-title {{
    font-size: 26px;
    font-weight: 900;
    letter-spacing: 2px;
    color: #48CAE4;
}}
.stButton>button {{
    width: 100%;
    background: linear-gradient(90deg, #1D4ED8, #00B4D8);
    color: white;
    font-weight: bold;
    border-radius: 12px;
    height: {sf_button_height};
    font-size: {sf_font_size};
    border: none;
}}
</style>
""", unsafe_allow_html=True)

# Banner
st.markdown("""
<div class="brand-container">
    <div class="brand-title">MEGALA CNC MATE</div>
    <div style="color: #94A3B8; font-size: 11px;">INDUSTRIAL CNC & PROFESSIONAL QUOTATION SUITE</div>
</div>
""", unsafe_allow_html=True)

# SIDEBAR NAVIGATION
st.sidebar.title("⚙️ மெனு (Menu)")

st.session_state.shop_floor_mode = st.sidebar.checkbox("🖥️ Shop Floor Touch Mode (Big UI)", value=st.session_state.shop_floor_mode)

menu_options = [
    "Home Dashboard",
    "Rod & Tube Calculator",
    "Traub Collet & Bar Feed",
    "Production & OEE Analyzer",
    "Stock Management",
    "Advanced G-Code & Toolpath Studio",
    "Professional Cost & Quotation Studio",
]

st.session_state.nav_menu = st.sidebar.radio("Navigation Menu", menu_options)

def get_kg_per_meter(dia, shape):
    if dia <= 0: return 0.0
    if shape == "Round": return (dia**2) / 162
    elif shape == "Square": return (dia**2) / 127
    elif shape == "Hexagon": return (dia**2) / 147
    return (dia**2) / 162

# 1. HOME DASHBOARD
if st.session_state.nav_menu == "Home Dashboard":
    st.subheader("Welcome Nithish 👋 (MEGALA CNC MATE Suite)")
    st.info("இடது பக்க மெனு மூலமாக அல்லது கீழே உள்ள பட்டன்கள் மூலம் நீங்கள் விரும்பிய பகுதிக்குச் செல்லலாம்.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📏 Rod & Weight Calculator"):
            st.session_state.nav_menu = "Rod & Tube Calculator"
            st.rerun()
        if st.button("🔧 Traub Collet Master"):
            st.session_state.nav_menu = "Traub Collet & Bar Feed"
            st.rerun()
        if st.button("📦 Stock Management"):
            st.session_state.nav_menu = "Stock Management"
            st.rerun()
    with col2:
        if st.button("⏱️ Production & OEE"):
            st.session_state.nav_menu = "Production & OEE Analyzer"
            st.rerun()
        if st.button("🖥️ G-Code Generator"):
            st.session_state.nav_menu = "Advanced G-Code & Toolpath Studio"
            st.rerun()
        if st.button("📄 Pro Quotation Studio"):
            st.session_state.nav_menu = "Professional Cost & Quotation Studio"
            st.rerun()

# 2. ROD CALCULATOR
elif st.session_state.nav_menu == "Rod & Tube Calculator":
    st.subheader("📏 Rod, Tube & Bulk Stock Calculator")
    col1, col2 = st.columns(2)
    with col1:
        rod_type = st.selectbox("Rod Shape", ["Round", "Hexagon", "Square"])
        rod_dia = st.number_input("Rod Diameter (mm)", min_value=0.0, value=51.0, step=0.5)
        rod_length_input = st.number_input("Total Stock Weight (Kg)", min_value=0.0, value=100.0, step=5.0)
    with col2:
        part_length = st.number_input("Component Length (mm)", min_value=0.0, value=38.7, step=0.1)
        cutting_allowance = st.number_input("Cutting Allowance (mm)", min_value=0.0, value=3.0, step=0.1)

    if st.button("Calculate Stock & Parts"):
        kg_per_m = get_kg_per_meter(rod_dia, rod_type)
        total_rod_meters = (rod_length_input / kg_per_m) if kg_per_m > 0 else 0.0
        total_part_len_mm = part_length + cutting_allowance
        parts_possible = int((total_rod_meters * 1000) / total_part_len_mm) if total_part_len_mm > 0 else 0
        
        st.success(f"**Total Meters:** {total_rod_meters:.2f} Meters")
        st.success(f"**Total Usable Parts:** {parts_possible} Nos")

# 3. TRAUB COLLET
elif st.session_state.nav_menu == "Traub Collet & Bar Feed":
    st.subheader("🔧 Traub Collet & RPM Master")
    raw_bar_dia = st.number_input("Raw Bar Diameter (mm)", min_value=1.0, value=16.0, step=0.5)
    cutting_speed_vc = st.number_input("Cutting Speed (Vc m/min)", min_value=10.0, value=100.0, step=5.0)

    if st.button("Calculate Collet & RPM"):
        rpm = int((cutting_speed_vc * 1000) / (math.pi * raw_bar_dia)) if raw_bar_dia > 0 else 0
        st.info(f"Recommended Collet Size: **{raw_bar_dia + 0.05:.2f} mm**")
        st.success(f"Calculated Spindle RPM: **{rpm} RPM**")

# 4. OEE ANALYZER
elif st.session_state.nav_menu == "Production & OEE Analyzer":
    st.subheader("⏱️ Production & OEE Analyzer")
    planned_time = st.number_input("Planned Time (Hours)", value=8.0)
    downtime = st.number_input("Downtime (Hours)", value=0.5)
    produced_parts = st.number_input("Total Parts Produced", value=1000)
    rejected_parts = st.number_input("Rejected Parts", value=15)

    if st.button("Calculate OEE"):
        operating_time = max(0.01, planned_time - downtime)
        availability = (operating_time / planned_time) * 100.0
        good_parts = max(0, produced_parts - rejected_parts)
        quality = (good_parts / produced_parts) * 100.0 if produced_parts > 0 else 0.0
        st.metric("Availability", f"{availability:.1f}%")
        st.metric("Quality", f"{quality:.1f}%")

# 5. STOCK MANAGEMENT
elif st.session_state.nav_menu == "Stock Management":
    st.subheader("📦 Stock Management")
    st.session_state.stock_db = st.data_editor(st.session_state.stock_db, num_rows="dynamic", use_container_width=True)

# 6. G-CODE
elif st.session_state.nav_menu == "Advanced G-Code & Toolpath Studio":
    st.subheader("🖥️ G-Code Generator")
    stock_dia = st.number_input("Stock Diameter (mm)", value=51.0)
    fin_dia = st.number_input("Finished Diameter (mm)", value=20.0)
    length = st.number_input("Length (mm)", value=38.7)

    if st.button("Generate G-Code"):
        gcode = f"""O1001 (CNC PROGRAM)
G21 G90 G40 G80
T0101 (TURNING TOOL)
G96 S200 M03
G00 X{stock_dia + 2.0} Z2.0
G01 X{fin_dia} Z-{length} F0.15
G00 Z50.0 M05
M30"""
        st.code(gcode, language="text")

# 7. QUOTATION STUDIO
elif st.session_state.nav_menu == "Professional Cost & Quotation Studio":
    st.subheader("📄 Professional Cost & Quotation Studio")
    client = st.text_input("Client Name", value="ABC Engineering")
    part_wt = st.number_input("Part Weight (Kg)", value=0.45)
    mat_rate = st.number_input("Material Rate (₹/Kg)", value=85.0)
    cycle_time = st.number_input("Cycle Time (Seconds)", value=30.0)
    eb_rate = st.number_input("EB Power & Rent Cost (₹/Hour)", value=75.0)
    profit = st.slider("Profit Margin (%)", min_value=0, max_value=50, value=20)

    if st.button("Calculate Quotation"):
        mat_cost = part_wt * mat_rate
        mfg_cost = (cycle_time / 3600.0) * eb_rate
        total_cost = mat_cost + mfg_cost
        selling_price = total_cost * (1 + profit/100.0)

        st.success(f"Raw Material Cost / Part: **₹ {mat_cost:.2f}**")
        st.success(f"Manufacturing Cost / Part: **₹ {mfg_cost:.2f}**")
        st.info(f"### Target Selling Price / Part: **₹ {selling_price:.2f}**")
