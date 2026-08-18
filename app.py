import base64
import os
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="MEGALA CNC MATE - Smart CNC. Simple Work.", page_icon="⚙️", layout="wide"
)

# --- INITIALIZING SESSION STATE (Data Persistence) ---
if "nav_menu" not in st.session_state:
    st.session_state.nav_menu = "Home Dashboard"
if "calc_results" not in st.session_state:
    st.session_state.calc_results = None
if "stock_db" not in st.session_state:
    st.session_state.stock_db = pd.DataFrame([
        {"Material": "EN8 Round Bar - 12mm", "Unit": "Meter", "Available Stock": 120.50, "Status": "In Stock"},
        {"Material": "MS Round Bar - 20mm", "Unit": "Kg", "Available Stock": 45.20, "Status": "Low Stock"},
    ])

# Helper function to convert logo
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_base64 = get_image_base64("logo.png")

# --- UI Styling (Neon Dark Theme) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #050B18 0%, #0A1428 50%, #040711 100%); color: #FFFFFF; }
    .brand-container { text-align: center; padding: 15px 0; background: radial-gradient(circle, #0F1C3F 0%, #070B19 100%); border-bottom: 2px solid #1E3A8A; margin-bottom: 15px; border-radius: 0 0 20px 20px; }
    .logo-glow-box { display: inline-block; padding: 8px; border-radius: 50%; box-shadow: 0 0 20px #48CAE4; border: 2px solid #48CAE4; }
    .logo-glow-box img { width: 60px !important; border-radius: 50%; }
    .brand-title { font-size: 28px; font-weight: 900; color: #48CAE4; letter-spacing: 2px; margin-top: 10px; text-transform: uppercase; }
    .metric-card { background: #111E38; padding: 20px; border-radius: 15px; border: 1px solid #1E3A8A; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# Top Header
st.markdown('<div class="brand-container">', unsafe_allow_html=True)
if logo_base64:
    st.markdown(f'<div class="logo-glow-box"><img src="data:image/png;base64,{logo_base64}" /></div>', unsafe_allow_html=True)
st.markdown('<div class="brand-title">MEGALA CNC MATE</div><div style="color: #94A3B8;">SMART CNC. SIMPLE WORK.</div></div>', unsafe_allow_html=True)

# SIDEBAR
st.sidebar.title("⚙️ MEGALA CNC MATE")
menu_options = ["Home Dashboard", "Rod & Tube Calculator", "Production & Cycle Time", "Stock Management", "Advanced G-Code Generator", "Quotation & PDF"]
selected_sidebar_menu = st.sidebar.radio("Navigation Menu", menu_options, index=menu_options.index(st.session_state.nav_menu))

if selected_sidebar_menu != st.session_state.nav_menu:
    st.session_state.nav_menu = selected_sidebar_menu
    st.rerun()

# --- PAGES ---

# 1. HOME DASHBOARD
if st.session_state.nav_menu == "Home Dashboard":
    st.subheader("Welcome, Operator! 👋")
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown('<div class="metric-card">📏<br>Rod Calc</div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="metric-card">⏱️<br>Production</div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="metric-card">📦<br>Stock Mgmt</div>', unsafe_allow_html=True)

# 2. ROD CALCULATOR
elif st.session_state.nav_menu == "Rod & Tube Calculator":
    st.header("📏 Rod & Tube Calculator")
    col1, col2 = st.columns(2)
    rod_len = col1.number_input("Total Rod Length (mm)", value=3000.0)
    part_len = col2.number_input("Part Length (mm)", value=100.0)
    qty = col1.number_input("Required Qty", value=100)
    
    if st.button("Calculate"):
        parts_per_rod = int(rod_len / part_len)
        st.session_state.calc_results = {"parts": parts_per_rod, "qty": qty}
        
    if st.session_state.calc_results:
        st.success(f"Parts per Rod: {st.session_state.calc_results['parts']}")

# 3. STOCK MANAGEMENT
elif st.session_state.nav_menu == "Stock Management":
    st.header("📦 Stock Management")
    st.write("இங்கே ஸ்டாக்குகளை எடிட் செய்யவும்:")
    # டேட்டா மாறாமல் இருக்க data_editor பயன்படுத்துகிறோம்
    st.session_state.stock_db = st.data_editor(st.session_state.stock_db, use_container_width=True)

# 4. PRODUCTION & CYCLE TIME
elif st.session_state.nav_menu == "Production & Cycle Time":
    st.header("⏱️ Production & Cycle Time")
    cycle = st.number_input("Cycle Time (sec)", value=20.0)
    if st.button("Calculate Production"):
        st.write(f"Production per Hour: {int(3600/cycle)} Nos")

# 5. G-CODE
elif st.session_state.nav_menu == "Advanced G-Code Generator":
    st.header("🛠️ Advanced G-Code Generator")
    if st.button("Generate"):
        st.code("O0001\nG21 G90\nM30", language="gcode")

# 6. QUOTATION
elif st.session_state.nav_menu == "Quotation & PDF":
    st.header("📄 Quotation & PDF")
    client = st.text_input("Client Name")
    if client:
        st.write(f"Preparing quote for {client}...")
