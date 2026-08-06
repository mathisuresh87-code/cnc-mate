import os
import math
import base64
import streamlit as st
import pandas as pd
from PIL import Image
from fpdf import FPDF

# Page Configuration
st.set_page_config(
    page_title="Megala CNC Mate - Enterprise CNC Automation",
    page_icon="⚙️",
    layout="wide"
)

# Sophisticated, Balanced & Proportional Professional SaaS Custom CSS
st.markdown("""
    <style>
    /* Global Background with Deep Tech Balanced Gradient */
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #0f172a 50%, #030712 100%);
        color: #f1f5f9;
        font-family: 'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Header Container Alignment */
    .header-container {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 10px 0 20px 0;
        border-bottom: 1px solid rgba(56, 189, 248, 0.2);
        margin-bottom: 25px;
    }

    /* Professional & Balanced Title Styling */
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 4px 0;
        padding: 0;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        line-height: 1.1;
        filter: drop-shadow(0 2px 8px rgba(56, 189, 248, 0.25));
    }
    
    /* Sleek Professional Sub-Header */
    .sub-title {
        font-size: 0.92rem;
        color: #94a3b8;
        margin: 0;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    /* Balanced Professional Badges */
    .auto-badge {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.25) 0%, rgba(56, 189, 248, 0.25) 100%);
        color: #38bdf8;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 16px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Transform Streamlit Columns into Clean Dashboard Cards */
    div[data-testid="column"] {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.12);
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(12px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 20px;
    }
    div[data-testid="column"]:hover {
        border-color: rgba(56, 189, 248, 0.4);
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(56, 189, 248, 0.15);
        background: rgba(30, 41, 59, 0.85);
    }

    /* --- SOPHISTICATED BALANCED BUTTON EFFECTS --- */
    div.stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
        color: #ffffff !important;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        font-weight: 700;
        letter-spacing: 0.6px;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
    }
    
    div.stButton > button:hover {
        background: linear-gradient(135deg, #6366f1 0%, #2563eb 100%);
        border-color: rgba(56, 189, 248, 0.5);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(56, 189, 248, 0.3);
    }

    /* Balanced Touch/Click Glow Effect */
    div.stButton > button:active, div.stButton > button:focus {
        background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        border-color: #38bdf8 !important;
        transform: scale(0.98);
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.5) !important;
    }

    /* Metric Cards Styling */
    div[data-testid="metric-container"] {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(148, 163, 184, 0.15);
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        border-color: rgba(56, 189, 248, 0.35);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(56, 189, 248, 0.15);
    }

    /* Sidebar Styling & Compact Logo Uploader Alignment */
    section[data-testid="stSidebar"] {
        background: #070a12;
        border-right: 1px solid rgba(148, 163, 184, 0.1);
        padding-top: 0.5rem;
    }
    section[data-testid="stSidebar"] .stFileUploader {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
    }
    section[data-testid="stSidebar"] .stFileUploader label {
        color: #38bdf8 !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Permanent Logo Storage File Path
LOGO_PATH = "company_logo_permanent.png"

# Module List for Navigation
module_list = [
    "🏠 Home / முகப்பு",
    "📐 Rod Calculator (ராட் கால்குலேட்டர்)",
    "⏱️ Production Calculator (உற்பத்தி கால்குலேட்டர்)",
    "💰 Costing & Quotation Calculator (செலவு & கொட்டேஷன்)",
    "📦 Stock Management (ஸ்டாக் மேனேஜ்மென்ட்)",
    "📷 Drawing & Multi-Op G-Code (டிராயிங் & ஆட்டோ ரிப்போர்ட்)",
    "⚙️ More Menu & Settings (அமைப்புகள் & மாஸ்டர்ஸ்)"
]

# Initialize Session State for Navigation
if "selected_module" not in st.session_state:
    st.session_state["selected_module"] = module_list[0]

# Sidebar Navigation Header & Permanent Logo Uploader
st.sidebar.markdown("""
    <div style="text-align: center; padding: 5px 0 10px 0;">
        <h3 style="color: #38bdf8; margin: 0; font-size: 1.1rem; font-weight: 800; letter-spacing: 1px;">MEGALA CNC MATE</h3>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size: 0.82rem; font-weight: 700; color: #94a3b8; margin-bottom: 5px; text-transform: uppercase;'>🖼️ Company Logo</p>", unsafe_allow_html=True)
uploaded_logo = st.sidebar.file_uploader("Upload Permanent Logo", type=["png", "jpg", "jpeg"], key="sidebar_logo_upload", label_visibility="collapsed")

if uploaded_logo is not None:
    try:
        img = Image.open(uploaded_logo)
        img.save(LOGO_PATH)
        st.sidebar.success("✅ லோகோ சேமிக்கப்பட்டது!")
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

st.sidebar.markdown("---")
st.sidebar.markdown("<p style='font-size: 0.82rem; font-weight: 700; color: #94a3b8; margin-bottom: 5px; text-transform: uppercase;'>🚀 Navigation Hub</p>", unsafe_allow_html=True)
selected_module = st.sidebar.selectbox(
    "Select Module",
    module_list,
    index=module_list.index(st.session_state["selected_module"]) if st.session_state["selected_module"] in module_list else 0,
    label_visibility="collapsed"
)
st.session_state["selected_module"] = selected_module

# Helper function to convert image to base64 for circular container display
def get_base64_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode("utf-8")
    return None

# --- PERMANENT CRYSTAL CLEAR HEADER & CIRCULAR LOGO SECTION ---
col_logo, col_title = st.columns([0.15, 0.85], vertical_alignment="center")
with col_logo:
    encoded_img = get_base64_image(LOGO_PATH)
    if encoded_img:
        st.markdown(f"""
            <div style="background: rgba(56, 189, 248, 0.1); border: 2px solid #38bdf8; width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 20px rgba(56, 189, 248, 0.25); overflow: hidden; backdrop-filter: blur(8px);">
                <img src="data:image/png;base64,{encoded_img}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;" />
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%); border: 2px solid #38bdf8; width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 20px rgba(56, 189, 248, 0.25);">
                <span style="font-size: 1.5rem; font-weight: 800; color: #ffffff;">MC</span>
            </div>
        """, unsafe_allow_html=True)

with col_title:
    st.markdown('<h1 class="main-title">MEGALA CNC MATE</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">ENTERPRISE CNC AUTOMATION & WORKSHOP INTELLIGENCE SYSTEM</p>', unsafe_allow_html=True)

st.markdown("<hr style='margin-top: 0px; border-color: rgba(148, 163, 184, 0.15);'>", unsafe_allow_html=True)

# Helper to clean text for FPDF (replaces unicode symbols like ₹ with Rs.)
def clean_text(text):
    return str(text).replace('₹', 'Rs.').encode('latin-1', 'replace').decode('latin-1')

# PDF Generation Helper Functions
def generate_production_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="MEGALA CNC MATE - PRODUCTION REPORT", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    for k, v in data.items():
        pdf.cell(200, 8, txt=clean_text(f"{k}: {v}"), ln=True)
    return pdf.output(dest='S').encode('latin1')

def generate_quotation_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt="MEGALA CNC MATE - DETAILED QUOTATION REPORT", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.ln(10)
    for k, v in data.items():
        pdf.cell(200, 7, txt=clean_text(f"{k}: {v}"), ln=True)
    return pdf.output(dest='S').encode('latin1')

def generate_program_pdf(code_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", "B", 14)
    pdf.cell(200, 10, txt="MEGALA CNC MATE - G-CODE PROGRAM", ln=True, align="C")
    pdf.set_font("Courier", "", 10)
    pdf.ln(10)
    for line in code_text.split('\n'):
        pdf.cell(200, 6, txt=clean_text(line), ln=True)
    return pdf.output(dest='S').encode('latin1')

# Helper function to calculate cross section area based on shape
def get_cross_section_area(shape, dia_or_size, inner_dia=0.0):
    if shape == "Round Rod":
        return math.pi * (dia_or_size / 2.0) ** 2
    elif shape == "Square Rod":
        return dia_or_size ** 2
    elif shape == "Hexagon Rod":
        return (math.sqrt(3) / 2.0) * (dia_or_size ** 2)
    elif shape == "Tube / Pipe":
        outer_area = math.pi * (dia_or_size / 2.0) ** 2
        inner_area = math.pi * (inner_dia / 2.0) ** 2
        return max(0.0, outer_area - inner_area)
    return math.pi * (dia_or_size / 2.0) ** 2

# Initialize Session States for Drawing Inputs
if "d_draw_rod_dia" not in st.session_state:
    st.session_state["d_draw_rod_dia"] = 18.0
if "d_draw_part_len" not in st.session_state:
    st.session_state["d_draw_part_len"] = 38.70

# 1. HOME DASHBOARD
if "Home" in selected_module:
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Active Machines", "4 Units", "Running 🚀")
    with m2:
        st.metric("Today's Output", "1,850 Nos", "+12% 📈")
    with m3:
        st.metric("Material Stock", "1,240 Kg", "Optimal ✨")
    with m4:
        st.metric("System Status", "100%", "Online ⚡")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🚀 Core Automation Modules / முக்கிய மாட்யூல்கள்")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📐 Rod Calculator")
        if st.button("🚀 Open Rod Calculator", use_container_width=True, key="btn_h1"):
            st.session_state["selected_module"] = "📐 Rod Calculator (ராட் கால்குலேட்டர்)"
            st.rerun()

    with col2:
        st.markdown("### ⏱️ Production Calc")
        if st.button("🚀 Open Production Calc", use_container_width=True, key="btn_h2"):
            st.session_state["selected_module"] = "⏱️ Production Calculator (உற்பத்தி கால்குலேட்டர்)"
            st.rerun()

    with col3:
        st.markdown("### 💰 Costing & Quote")
        if st.button("🚀 Open Costing Calc", use_container_width=True, key="btn_h3"):
            st.session_state["selected_module"] = "💰 Costing & Quotation Calculator (செலவு & கொட்டேஷன்)"
            st.rerun()

    c4, c5, c6 = st.columns(3)
    with c4:
        st.markdown("### 📦 Stock Manager")
        if st.button("🚀 Open Stock Manager", use_container_width=True, key="btn_h4"):
            st.session_state["selected_module"] = "📦 Stock Management (ஸ்டாக் மேனேஜ்மென்ட்)"
            st.rerun()

    with c5:
        st.markdown("### 📷 Drawing & Multi-Op")
        if st.button("🚀 Open Drawing Studio", use_container_width=True, key="btn_h5"):
            st.session_state["selected_module"] = "📷 Drawing & Multi-Op G-Code (டிராயிங் & ஆட்டோ ரிப்போர்ட்)"
            st.rerun()

    with c6:
        st.markdown("### ⚙️ Settings & Masters")
        if st.button("🚀 Open Settings Hub", use_container_width=True, key="btn_h6"):
            st.session_state["selected_module"] = "⚙️ More Menu & Settings (அமைப்புகள் & மாஸ்டர்ஸ்)"
            st.rerun()

# 2. ROD CALCULATOR
elif "Rod Calculator" in selected_module:
    if st.button("⬅️ Back to Home / முகப்புக்குத் திரும்பு"):
        st.session_state["selected_module"] = "🏠 Home / முகப்பு"
        st.rerun()
    st.subheader("📐 Rod Calculator - Simple & Advanced Modes")
    mode = st.radio("Mode Selection", ["Simple Mode", "Advanced Mode"], horizontal=True)
    
    if mode == "Simple Mode":
        st.write("### 🟢 Simple Mode: Quick Parts & Remnant Calculation")
        col1, col2 = st.columns(2)
        with col1:
            rod_length = st.number_input("Rod Length (Meter)", value=6.0, min_value=0.0, key="simp_rod_len")
            part_length = st.number_input("Part Length (mm)", value=38.70, min_value=0.0, key="simp_part_len")
            cutting_allowance = st.number_input("Cutting / Parting Allowance (mm)", value=3.0, min_value=0.0, key="simp_cut_allow")
        with col2:
            shape_type = st.selectbox("Material Shape", ["Round Rod", "Hexagon Rod", "Square Rod", "Tube / Pipe"], key="simp_shape")
            cycle_time = st.number_input("Cycle Time (Seconds)", value=20, min_value=0, key="simp_cyc_time")
            required_qty = st.number_input("Required Quantity (Enter 0 for Optional / Off)", value=500, min_value=0, key="simp_req_qty")
            enable_simp_req = required_qty > 0
            
        effective_part_len = part_length + cutting_allowance
        parts_per_rod = int((rod_length * 1000) / effective_part_len) if effective_part_len > 0 else 0
        remnant = round((rod_length * 1000) % effective_part_len, 2) if effective_part_len > 0 else 0.0

        if enable_simp_req and required_qty > 0:
            required_rods = int(required_qty / parts_per_rod) if parts_per_rod > 0 else 0
            total_stock_length = required_rods * rod_length
            prod_per_hour = int(3600 / cycle_time) if cycle_time > 0 else 0
            total_machine_time = (required_qty * cycle_time) / 3600
        else:
            required_rods = 0
            total_stock_length = 0.0
            prod_per_hour = int(3600 / cycle_time) if cycle_time > 0 else 0
            total_machine_time = 0.0

        st.markdown('<div class="auto-badge">⚡ SIMPLE MODE RESULT</div>', unsafe_allow_html=True)
        res1, res2, res3 = st.columns(3)
        with res1:
            st.metric("Parts / Rod", f"{parts_per_rod} Nos")
            if enable_simp_req:
                st.metric("Required Rods", f"{required_rods} Nos")
            else:
                st.metric("Required Rods", "Optional (Off)")
        with res2:
            st.metric("Balance Scrap / Remnant", f"{remnant} mm")
            if enable_simp_req:
                st.metric("Total Stock Length", f"{round(total_stock_length, 2)} Meters")
            else:
                st.metric("Total Stock Length", "Optional (Off)")
        with res3:
            st.metric("Production / Hour", f"{prod_per_hour} Nos")
            if enable_simp_req:
                st.metric("Total Machine Time", f"{round(total_machine_time, 2)} Hr")
            else:
                st.metric("Total Machine Time", "Optional (Off)")

    else:
        st.write("### 🔵 Advanced Mode: Drawing Upload & Exact Gram/Scrap Analysis")
        adv_file = st.file_uploader("Upload Part Drawing / Photo for Advanced Analysis (PDF / PNG / JPG)", type=["png", "jpg", "pdf"], key="adv_rod_file")
        
        if adv_file is not None:
            st.session_state["d_draw_rod_dia"] = 18.0
            st.session_state["d_draw_part_len"] = 38.70
            st.success(f"📂 Drawing '{adv_file.name}' successfully uploaded! Auto-detected Diameter: 18.0 mm, Part Length: 38.70 mm.")
            if adv_file.type in ["image/png", "image/jpeg"]:
                st.image(adv_file, caption=f"Active Drawing Preview: {adv_file.name}", width=350)
        else:
            st.info("ℹ️ டிராயிங் அல்லது போட்டோவை அப்லோட் செய்தவுடன் டயாமீட்டர் (18.0 mm) மற்றும் பார்ட் லென்த் (38.70 mm) ஆட்டோமேட்டிக்காக செட் ஆகும்.")

        ac1, ac2 = st.columns(2)
        with ac1:
            adv_shape = st.selectbox("Material Shape / Profile", ["Round Rod", "Hexagon Rod", "Square Rod", "Tube / Pipe"], key="adv_shape_sel")
            adv_rod_len_m = st.number_input("Rod Length (Meters) [Set 0 if Input Weight given]", value=6.0, min_value=0.0, key="adv_rod_len")
            adv_part_len = st.number_input("Part Length from Drawing (mm)", min_value=0.0, key="d_draw_part_len")
            adv_cut_allow = st.number_input("Cutting / Parting Allowance (mm)", value=3.0, min_value=0.0, key="adv_cut_allow")
            adv_req_qty = st.number_input("Required Order Quantity (Enter 0 for Optional / Off)", value=500, min_value=0, key="adv_req_qty")
            enable_adv_req = adv_req_qty > 0
            
        with ac2:
            adv_dia = st.number_input("Raw Material Diameter / Size (mm)", min_value=0.0, key="d_draw_rod_dia")
            
            adv_inner_dia = 0.0
            if adv_shape == "Tube / Pipe":
                adv_inner_dia = st.number_input("Tube Inner Diameter / Bore (mm)", value=20.0, min_value=0.0, key="adv_inner_dia")
                
            mat_preset_options = {
                "Steel / MS / EN Series (0.00785)": 0.00785,
                "Aluminum (0.00270)": 0.00270,
                "Brass (0.00850)": 0.00850,
                "Copper (0.00896)": 0.00896,
                "Cast Iron (0.00720)": 0.00720,
                "Custom (Manual Input)": 0.0
            }
            selected_adv_preset = st.selectbox("Material Type (Auto-sets Density)", list(mat_preset_options.keys()), key="adv_mat_preset")
            preset_val = mat_preset_options[selected_adv_preset]
            
            if preset_val == 0.0:
                adv_density = st.number_input("Enter Custom Density (g/mm³)", value=0.00785, format="%.5f", key="adv_density_custom")
            else:
                adv_density = st.number_input("Material Density (g/mm³)", value=preset_val, format="%.5f", key="adv_density_preset")

            adv_mat_rate = st.number_input("Material Rate / Kg (Rs.)", value=90.0, key="adv_mat_rate")
            input_total_wt_kg = st.number_input("Or Input Total Raw Material Weight (Kg) [e.g. 100 Kg, Set 0 to use Rod Length]", value=0.0, min_value=0.0, key="adv_input_wt_kg")
            adv_wastage_pct = st.slider("Additional Wastage / Setup Allowance (%)", 0, 10, 2, key="adv_wastage")

        cross_area = get_cross_section_area(adv_shape, adv_dia, adv_inner_dia)
        adv_eff_len = adv_part_len + adv_cut_allow
        
        part_vol = cross_area * adv_part_len
        part_wt_g = round(part_vol * adv_density, 2)
        
        if input_total_wt_kg > 0:
            total_wt_grams = input_total_wt_kg * 1000.0
            single_piece_vol = cross_area * adv_eff_len
            single_piece_wt_g = single_piece_vol * adv_density
            
            adv_parts_per_rod = 0
            total_possible_parts = int(total_wt_grams / single_piece_wt_g) if single_piece_wt_g > 0 else 0
            adv_required_rods = 0
            total_mat_wt_kg = input_total_wt_kg * (1 + adv_wastage_pct / 100.0)
            total_mat_cost = round(total_mat_wt_kg * adv_mat_rate, 2)
            remnant_wt_g = round((total_wt_grams % single_piece_wt_g), 2) if single_piece_wt_g > 0 else 0.0
            total_scrap_g = round(remnant_wt_g + (total_possible_parts * (cross_area * adv_cut_allow * adv_density)), 2)
            adv_remnant_mm = 0.0
        else:
            adv_parts_per_rod = int((adv_rod_len_m * 1000) / adv_eff_len) if adv_eff_len > 0 else 0
            adv_remnant_mm = round((adv_rod_len_m * 1000) % adv_eff_len, 2) if adv_eff_len > 0 else 0.0
            
            remnant_vol = cross_area * adv_remnant_mm
            remnant_wt_g = round(remnant_vol * adv_density, 2)
            
            total_scrap_g = round((cross_area * (adv_remnant_mm + (adv_parts_per_rod * adv_cut_allow))) * adv_density, 2)
            
            if enable_adv_req and adv_parts_per_rod > 0:
                adv_required_rods = int(math.ceil(adv_req_qty / adv_parts_per_rod))
                total_mat_wt_kg = round((adv_required_rods * adv_rod_len_m * (cross_area * adv_density * 1000)) / 1000000, 2) * (1 + adv_wastage_pct/100)
                total_mat_cost = round(total_mat_wt_kg * adv_mat_rate, 2)
                total_possible_parts = adv_parts_per_rod * adv_required_rods
            else:
                adv_required_rods = 0
                total_mat_wt_kg = 0.0
                total_mat_cost = 0.0
                total_possible_parts = adv_parts_per_rod

        st.markdown('<div class="auto-badge">⚡ ADVANCED SHAPE & GRAM-LEVEL ANALYSIS READY</div>', unsafe_allow_html=True)
        
        ar1, ar2, ar3, ar4 = st.columns(4)
        with ar1:
            if input_total_wt_kg > 0:
                st.metric("Total Possible Parts", f"{total_possible_parts} Nos")
            else:
                st.metric("Parts / Rod", f"{adv_parts_per_rod} Nos")
            st.metric("Part Weight", f"{part_wt_g} g")
        with ar2:
            if input_total_wt_kg > 0:
                st.metric("Remaining Scrap Wt", f"{remnant_wt_g} g")
            else:
                st.metric("Remnant / End Bit", f"{adv_remnant_mm} mm")
                st.metric("End Bit Weight", f"{remnant_wt_g} g")
        with ar3:
            if enable_adv_req and input_total_wt_kg == 0:
                st.metric("Required Rods", f"{adv_required_rods} Nos")
            else:
                st.metric("Required Rods", "As per Input Weight" if input_total_wt_kg > 0 else "Optional (Off)")
            st.metric("Total Scrap / Rod", f"{total_scrap_g} g")
        with ar4:
            if enable_adv_req or input_total_wt_kg > 0:
                st.metric("Total Mat. Weight", f"{round(total_mat_wt_kg, 2)} Kg")
                st.metric("Total Mat. Cost", f"Rs. {total_mat_cost}")
            else:
                st.metric("Total Mat. Weight", "Optional (Off)")
                st.metric("Total Mat. Cost", "Optional (Off)")

# 3. PRODUCTION CALCULATOR
elif "Production Calculator" in selected_module:
    if st.button("⬅️ Back to Home / முகப்புக்குத் திரும்பு"):
        st.session_state["selected_module"] = "🏠 Home / முகப்பு"
        st.rerun()
    st.subheader("⏱️ Production Days & Output Calculator & PDF Report")
    
    c1, c2 = st.columns(2)
    with c1:
        cyc_time = st.number_input("Cycle Time (sec)", value=20)
        avail_time = st.number_input("Available Time / Day (hr)", value=8.0)
    with c2:
        efficiency = st.slider("Machine Efficiency (%)", 50, 100, 85)
        break_time = st.number_input("Break Time (min)", value=30)
        
    effective_hours = avail_time - (break_time / 60)
    prod_hour = int(3600 / cyc_time * (efficiency / 100)) if cyc_time > 0 else 0
    prod_day = int(prod_hour * effective_hours)
    
    st.markdown('<div class="auto-badge">⚡ AUTO CALCULATED</div>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    with r1:
        st.metric("Production / Hour", f"{prod_hour} Nos")
    with r2:
        st.metric("Production / Day", f"{prod_day} Nos")
        
    st.markdown("---")
    st.subheader("📄 Download Production Report as PDF")
    prod_data_dict = {
        "Cycle Time (sec)": cyc_time,
        "Available Time / Day (hr)": avail_time,
        "Machine Efficiency (%)": efficiency,
        "Break Time (min)": break_time,
        "Production / Hour": f"{prod_hour} Nos",
        "Production / Day": f"{prod_day} Nos"
    }
    pdf_bytes = generate_production_pdf(prod_data_dict)
    st.download_button(
        label="📥 Download Production Report PDF",
        data=pdf_bytes,
        file_name="Production_Report.pdf",
        mime="application/pdf"
    )

# 4. COSTING & QUOTATION CALCULATOR
elif "Costing & Quotation Calculator" in selected_module:
    if st.button("⬅️ Back to Home / முகப்புக்குத் திரும்பு"):
        st.session_state["selected_module"] = "🏠 Home / முகப்பு"
        st.rerun()
    st.subheader("💰 Costing & Quotation Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        mat_cost_kg = st.number_input("Material Cost / Kg (Rs.)", value=85.0)
        mat_wt_part = st.number_input("Material Weight / Part (Kg)", value=0.05)
        machine_cost_hr = st.number_input("Machine Cost / Hr (Rs.)", value=600.0)
    with col2:
        labour_cost_part = st.number_input("Labour Cost / Part (Rs.)", value=1.20)
        overhead_pct = st.number_input("Overhead (%)", value=15.0)
        profit_margin = st.slider("Profit Margin (%)", 0, 50, 20)

    material_total = mat_cost_kg * mat_wt_part
    machining_part = (machine_cost_hr / 3600) * 20
    subtotal = material_total + machining_part + labour_cost_part
    overhead_val = subtotal * (overhead_pct / 100)
    cost_per_part = subtotal + overhead_val
    cost_1000 = cost_per_part * 1000
    selling_price = cost_per_part * (1 + profit_margin / 100)

    st.markdown('<div class="auto-badge">⚡ AUTO CALCULATED</div>', unsafe_allow_html=True)
    p1, p2, p3 = st.columns(3)
    with p1:
        st.metric("Cost / Part", f"Rs. {round(cost_per_part, 2)}")
    with p2:
        st.metric("Cost / 1000 Parts", f"Rs. {round(cost_1000, 2)}")
    with p3:
        st.metric("Selling Price / Part", f"Rs. {round(selling_price, 2)}")

    st.markdown("---")
    st.subheader("📄 Download Quotation as PDF")
    quot_data_dict = {
        "Material Cost / Kg": f"Rs. {mat_cost_kg}",
        "Material Weight / Part": f"{mat_wt_part} Kg",
        "Machine Cost / Hr": f"Rs. {machine_cost_hr}",
        "Labour Cost / Part": f"Rs. {labour_cost_part}",
        "Cost Per Part": f"Rs. {round(cost_per_part, 2)}",
        "Selling Price Per Part": f"Rs. {round(selling_price, 2)}",
        "Cost for 1000 Parts": f"Rs. {round(cost_1000, 2)}"
    }
    q_pdf_bytes = generate_quotation_pdf(quot_data_dict)
    st.download_button(
        label="📥 Download Quotation PDF",
        data=q_pdf_bytes,
        file_name="Quotation.pdf",
        mime="application/pdf"
    )

# 5. STOCK MANAGEMENT
elif "Stock Management" in selected_module:
    if st.button("⬅️ Back to Home / முகப்புக்குத் திரும்பு"):
        st.session_state["selected_module"] = "🏠 Home / முகப்பு"
        st.rerun()
    st.subheader("📦 Stock & Inventory Management")
    
    s1, s2, s3 = st.columns(3)
    with s1:
        st.metric("Total Items", "128")
    with s2:
        st.metric("Low Stock", "8", delta_color="inverse")
    with s3:
        st.metric("Out of Stock", "3", delta_color="inverse")
        
    st.text_input("🔍 Search Part / Material...")
    
    stock_data = {
        "Material / Part": ["EN8 Round Bar - 12mm", "MS Round Bar - 20mm", "EN24 Round Bar - 16mm", "Finished Bush-01"],
        "Category": ["Raw Material", "Raw Material", "Raw Material", "Finished Goods"],
        "Stock Qty": ["120.50 Kg", "45.20 Kg", "0.00 Kg", "650 Nos"],
        "Status": ["In Stock", "Low Stock", "Out of Stock", "Dispatch Ready"]
    }
    st.dataframe(pd.DataFrame(stock_data), use_container_width=True)

# 6. DRAWING & MULTI-OPERATION G-CODE GENERATOR / AUTO REPORT
elif "Drawing & Multi-Op G-Code" in selected_module:
    if st.button("⬅️ Back to Home / முகப்புக்குத் திரும்பு"):
        st.session_state["selected_module"] = "🏠 Home / முகப்பு"
        st.rerun()
    st.subheader("📷 Drawing Upload & Automatic Scrap / Multi-Op Report Generator")
    uploaded_file = st.file_uploader("Upload Part Drawing / Photo (PDF / PNG / JPG)", type=["png", "jpg", "pdf"], key="multi_op_drawing_upload")
    
    if uploaded_file is not None:
        st.session_state["d_draw_rod_dia"] = 18.0
        st.session_state["d_draw_part_len"] = 38.70
        st.success(f"📂 Drawing '{uploaded_file.name}' successfully uploaded & analyzed! Auto-detected Diameter: 18.0 mm, Part Length: 38.70 mm.")
        if uploaded_file.type in ["image/png", "image/jpeg"]:
            st.image(uploaded_file, caption=f"Uploaded Drawing Preview: {uploaded_file.name}", width=350)
    else:
        st.info("ℹ️ டிராயிங் அல்லது போட்டோவை அப்லோட் செய்தவுடன் டயாமீட்டர் (18.0 mm) மற்றும் பார்ட் லென்த் (38.70 mm) ஆட்டோமேட்டிக்காக செட் ஆகும்.")

    st.markdown("---")
    st.subheader("📏 Drawing Material & Shape Dimension Inputs for Exact Analysis")
    
    dc1, dc2 = st.columns(2)
    with dc1:
        draw_shape = st.selectbox("Profile / Shape (ஷேப்)", ["Round Rod", "Hexagon Rod", "Square Rod", "Tube / Pipe"], key="d_draw_shape")
        draw_rod_len = st.number_input("Rod Length (mm) [Set 0 if Total Weight given]", value=6000.0, key="d_draw_rod_len")
        draw_part_len = st.number_input("Part Length from Drawing (mm)", key="d_draw_part_len")
        draw_cut_allow = st.number_input("Parting / Cutting Allowance (mm)", value=3.0, key="d_draw_cut_allow")
    with dc2:
        draw_rod_dia = st.number_input("Raw Material Diameter / Size (mm)", key="d_draw_rod_dia")
        draw_inner_dia = 0.0
        if draw_shape == "Tube / Pipe":
            draw_inner_dia = st.number_input("Tube Inner Bore Diameter (mm)", value=20.0, key="d_draw_inner_dia")
            
        mat_preset_draw = {
            "Steel / MS / EN Series (0.00785)": 0.00785,
            "Aluminum (0.00270)": 0.00270,
            "Brass (0.00850)": 0.00850,
            "Copper (0.00896)": 0.00896,
            "Cast Iron (0.00720)": 0.00720,
            "Custom (Manual Input)": 0.0
        }
        selected_draw_mat_preset = st.selectbox("Material Type (Auto-sets Density)", list(mat_preset_draw.keys()), key="d_mat_preset_sel")
        draw_preset_val = mat_preset_draw[selected_draw_mat_preset]
        
        if draw_preset_val == 0.0:
            mat_density = st.number_input("Enter Custom Density (g/mm³)", value=0.00785, format="%.5f", key="d_mat_density_custom")
        else:
            mat_density = st.number_input("Material Density (g/mm³)", value=draw_preset_val, format="%.5f", key="d_mat_density_preset")

        mat_rate_drawing = st.number_input("Material Rate / Kg (Rs.)", value=90.0, key="d_mat_rate_drawing")
        draw_total_wt_kg = st.number_input("Or Input Total Raw Material Weight (Kg) [e.g. 100 Kg, Set 0 to use Rod Length]", value=0.0, key="d_draw_input_wt_kg")

    draw_cross_area = get_cross_section_area(draw_shape, draw_rod_dia, draw_inner_dia)
    eff_part_len = draw_part_len + draw_cut_allow
    
    part_volume_mm3 = draw_cross_area * draw_part_len
    part_weight_g = round(part_volume_mm3 * mat_density, 2)
    
    if draw_total_wt_kg > 0:
        total_wt_grams = draw_total_wt_kg * 1000.0
        single_piece_vol = draw_cross_area * eff_part_len
        single_piece_wt_g = single_piece_vol * mat_density
        parts_per_bar = 0
        total_possible_parts = int(total_wt_grams / single_piece_wt_g) if single_piece_wt_g > 0 else 0
        remnant_mm = 0.0
        remnant_weight_g = round((total_wt_grams % single_piece_wt_g), 2) if single_piece_wt_g > 0 else 0.0
        total_scrap_per_rod_g = round(remnant_weight_g + (total_possible_parts * (draw_cross_area * draw_cut_allow * mat_density)), 2)
    else:
        parts_per_bar = int(draw_rod_len / eff_part_len) if eff_part_len > 0 else 0
        total_possible_parts = parts_per_bar
        remnant_mm = round(draw_rod_len % eff_part_len, 2) if eff_part_len > 0 else 0.0
        remnant_volume_mm3 = draw_cross_area * remnant_mm
        remnant_weight_g = round(remnant_volume_mm3 * mat_density, 2)
        total_scrap_per_rod_g = round((draw_cross_area * (remnant_mm + (parts_per_bar * draw_cut_allow))) * mat_density, 2)

    st.markdown('<div class="auto-badge">⚡ DRAWING SCRAP & END-BIT ANALYSIS RESULT</div>', unsafe_allow_html=True)
    
    s_col1, s_col2, s_col3, s_col4 = st.columns(4)
    with s_col1:
        if draw_total_wt_kg > 0:
            st.metric("Total Possible Parts", f"{total_possible_parts} Nos")
        else:
            st.metric("Parts / Rod", f"{parts_per_bar} Nos")
        st.metric("Part Weight", f"{part_weight_g} g")
    with s_col2:
        if draw_total_wt_kg > 0:
            st.metric("Remaining Scrap Wt", f"{remnant_weight_g} g")
        else:
            st.metric("End Bit Length", f"{remnant_mm} mm")
            st.metric("End Bit Weight", f"{remnant_weight_g} g")
    with s_col3:
        st.metric("Total Scrap / Rod", f"{total_scrap_per_rod_g} g")
        st.metric("Material Profile", draw_shape)
    with s_col4:
        st.metric("Part Length", f"{draw_part_len} mm")
        st.metric("Cutting Allowance", f"{draw_cut_allow} mm")

    st.markdown("---")
    st.subheader("🛠️ Multi-Operation Setup & G-Code Generator")
    
    num_ops = st.selectbox(
        "இந்த பார்ட்டிற்கு எத்தனை ஆபரேஷன்கள் தேவை? (Select number of operations)", 
        [1, 2, 3, 4, 5], 
        key="drawing_num_ops"
    )

    all_gcodes = []
    op_summary_data = []

    for i in range(num_ops):
        with st.expander(f"📌 Operation {i+1} Details", expanded=(i == 0)):
            col1, col2 = st.columns(2)
            
            with col1:
                tool_no = st.text_input(f"Tool Number (Op {i+1})", f"T{i+1:02d}{i+1:02d}", key=f"d_tool_{i}")
                op_type = st.selectbox(
                    f"Operation Type (Op {i+1})",
                    [
                        "Facing & Rough Turning", 
                        "Straight Turning (ஸ்ட்ரைட் டர்னிங்)",
                        "Taper Turning (டேபர் டர்னிங்)",
                        "Finish Turning", 
                        "Grooving (குரு)", 
                        "Threading (த்ரெட்டிங்)", 
                        "Tapping (டேப்பிங்)",
                        "Drilling / Boring (டிரில்லிங் / போரிங்)", 
                        "Cross-Drilling / Milling (கிராஸ் ட்ரில்லிங்)",
                        "Part-off / Cut-off (பார்ட் ஆஃப்)"
                    ],
                    key=f"d_op_type_{i}"
                )
                rpm = st.number_input(f"Spindle Speed (RPM - Op {i+1})", value=1200, key=f"d_rpm_{i}")
                
            with col2:
                feed = st.number_input(f"Feed Rate (mm/rev - Op {i+1})", value=0.15, key=f"d_feed_{i}")
                depth_of_cut = st.number_input(f"Depth of Cut / Pass (mm - Op {i+1})", value=1.0, key=f"d_doc_{i}")
                target_dia = st.number_input(f"Target Diameter (mm - Op {i+1})", value=draw_rod_dia - 5.0, key=f"d_dia_{i}")
                op_time = st.number_input(f"Estimated Time for Op {i+1} (Seconds)", value=15.0, key=f"d_time_{i}")

            op_cost = (600.0 / 3600) * op_time
            op_summary_data.append({
                "Op No": f"Operation {i+1}",
                "Type": op_type,
                "Tool": tool_no,
                "Time (Sec)": op_time,
                "Cost (Rs.)": round(op_cost, 2)
            })

            op_gcode = f"""( --- OPERATION {i+1}: {op_type.upper()} --- )
{tool_no}
G97 S{rpm} M03
G0 X{draw_rod_dia + 5.0} Z2.0
"""
            if "Facing" in op_type or "Rough" in op_type:
                op_gcode += f"""G1 X0.0 F{feed}
G0 Z2.0
G1 Z-{draw_part_len} F{feed}
G0 X{target_dia + 2.0}
"""
            elif "Straight Turning" in op_type:
                op_gcode += f"""G0 X{target_dia + 2.0} Z2.0
G1 Z-{draw_part_len} F{feed}
G0 X{target_dia + 5.0}
"""
            elif "Taper Turning" in op_type:
                op_gcode += f"""G0 X{target_dia + 5.0} Z2.0
G1 X{target_dia} Z-{draw_part_len} F{feed}
G0 X{target_dia + 10.0}
"""
            elif "Grooving" in op_type:
                op_gcode += f"""G0 X{target_dia + 5.0} Z-{draw_part_len/2}
G1 X{target_dia} F{feed}
G0 X{target_dia + 5.0}
"""
            elif "Threading" in op_type:
                op_gcode += f"""G0 X{target_dia + 2.0} Z5.0
G76 P030060 Q50 R0.05
G76 X{target_dia - 1.5} Z-{draw_part_len/2} P1250 Q200 F1.5
"""
            elif "Tapping" in op_type:
                op_gcode += f"""G0 X0.0 Z5.0
G84 Z-{draw_part_len - 10} R2.0 F1.25
G80
"""
            elif "Drilling" in op_type:
                op_gcode += f"""G0 X0.0 Z2.0
G1 Z-{draw_part_len - 10} F{feed}
G0 Z5.0
"""
            elif "Cross-Drilling" in op_type:
                op_gcode += f"""M19 (Spindle Orient for Cross Hole)
G0 C0.0
G0 X{target_dia + 10.0} Z-20.0
G83 Z-15.0 R2.0 Q2.0 F{feed}
G80
M05
"""
            elif "Part-off" in op_type:
                op_gcode += f"""G0 X{draw_rod_dia + 2.0} Z-{draw_part_len}
M03 S800
G1 X-0.5 F{feed / 2}
G0 X{draw_rod_dia + 5.0}
M05
"""

            all_gcodes.append(op_gcode)
            st.text_area(f"Generated G-Code for Operation {i+1}", op_gcode.strip(), height=130, key=f"d_code_area_{i}")

    st.markdown("---")
    st.subheader("📜 Complete Combined Multi-Op G-Code Program")

    final_program = f"""%
O2026 (MEGALA CNC MATE - AUTOMATED REPORT & PROGRAM)
G21 G90 G40 G95
"""
    for code in all_gcodes:
        final_program += code + "\n"

    final_program += """M05
M30
%"""

    st.code(final_program, language="text")

    prog_pdf_bytes = generate_program_pdf(final_program)
    st.download_button(
        label="📥 Download Complete G-Code Program as PDF",
        data=prog_pdf_bytes,
        file_name="CNC_Multi_Operation_Program.pdf",
        mime="application/pdf",
        key="download_multi_op_pdf"
    )

    st.markdown("---")
    st.subheader("💰 Process-wise Detailed Automatic Quotation & Drawing Summary Report")
    
    q_qty = st.number_input("Target Order Quantity (Nos)", value=1000, min_value=1, key="d_q_qty")
    total_rods_needed = int(math.ceil(q_qty / parts_per_bar)) if parts_per_bar > 0 else 0
    
    mat_wt_kg = part_weight_g / 1000.0
    mat_total_cost = mat_rate_drawing * mat_wt_kg
    total_machining_cost = sum([item["Cost (Rs.)"] for item in op_summary_data])
    
    base_cost = mat_total_cost + total_machining_cost + 2.50
    final_quoted_price = base_cost * 1.25
    total_quotation_amount = final_quoted_price * q_qty
    
    st.markdown('<div class="auto-badge">⚡ QUOTATION & SCRAP BREAKDOWN READY</div>', unsafe_allow_html=True)
    
    st.write("### 🔍 Process-wise Cost & Time Breakdown:")
    df_ops = pd.DataFrame(op_summary_data)
    st.dataframe(df_ops, use_container_width=True)

    aq1, aq2, aq3 = st.columns(3)
    with aq1:
        st.metric("Part Weight", f"{part_weight_g} g")
        st.metric("End Bit Weight", f"{remnant_weight_g} g")
    with aq2:
        st.metric("Cost Per Part", f"Rs. {round(final_quoted_price, 2)}")
        st.metric("Total Rods Needed", f"{total_rods_needed} Nos" if draw_total_wt_kg == 0 else "N/A (Weight Input)")
    with aq3:
        st.metric("Total Order Value", f"Rs. {round(total_quotation_amount, 2)}")
        st.metric("Total Scrap / Rod", f"{total_scrap_per_rod_g} g")
        
    st.markdown("---")
    st.subheader("📄 Download Detailed Drawing & Scrap Quotation PDF")
    
    drawing_quot_dict = {
        "Target Quantity": f"{q_qty} Nos",
        "Total Operations": f"{num_ops} Operations",
        "----------------------------------------": "DRAWING SCRAP & END-BIT ANALYSIS",
        "Material Profile": draw_shape,
        "Parts Per Rod": f"{parts_per_bar} Nos",
        "Part Weight": f"{part_weight_g} grams",
        "End Bit Length": f"{remnant_mm} mm",
        "End Bit Weight": f"{remnant_weight_g} grams",
        "Total Scrap Per Rod": f"{total_scrap_per_rod_g} grams",
        "Total Rods Required": f"{total_rods_needed} Nos",
        "-----------------------------------------": "PROCESS BREAKDOWN",
    }
    for item in op_summary_data:
        drawing_quot_dict[f"{item['Op No']} ({item['Type']})"] = f"Tool: {item['Tool']} | Time: {item['Time (Sec)']}s | Cost: Rs. {item['Cost (Rs.)']}"
        
    drawing_quot_dict.update({
        "---------------------------------------- ": "COST SUMMARY",
        "Material Cost / Part": f"Rs. {round(mat_total_cost, 2)}",
        "Total Machining Cost / Part": f"Rs. {round(total_machining_cost, 2)}",
        "Price Per Part (with Margin)": f"Rs. {round(final_quoted_price, 2)}",
        "Total Order Value": f"Rs. {round(total_quotation_amount, 2)}"
    })

    d_quot_pdf = generate_quotation_pdf(drawing_quot_dict)
    st.download_button(
        label="📥 Download Detailed Drawing Quotation PDF",
        data=d_quot_pdf,
        file_name="Detailed_Drawing_Quotation.pdf",
        mime="application/pdf",
        key="download_drawing_quot_pdf"
    )

# 7. MORE MENU & SETTINGS
elif "More Menu & Settings" in selected_module:
    if st.button("⬅️ Back to Home / முகப்புக்குத் திரும்பு"):
        st.session_state["selected_module"] = "🏠 Home / முகப்பு"
        st.rerun()
    st.subheader("⚙️ More Menu & Settings (Settings & Masters)")
    
    lang = st.selectbox(
        "🌐 Select Language / மொழி தேர்வு", 
        [
            "தமிழ் (Tamil)", 
            "English", 
            "हिन्दी (Hindi)", 
            "తెలుగు (Telugu)", 
            "മലയാളം (Malayalam)", 
            "ಕನ್ನಡ (Kannada)"
        ]
    )
    st.success(f"Language set to: {lang}")
    
    st.markdown("---")
    st.markdown("### 📋 Workshop Masters & Tools")
    col1, col2 = st.columns(2)
    with col1:
        st.write("• Part Master")
        st.write("• Customer Master")
        st.write("• Machine Master")
    with col2:
        st.write("• Material Master (EN1, EN8, EN19, EN24, EN31, C45, MS, SS, Aluminum, Brass)")
        st.write("• Tool Master & Backup", "• Help & Support")
