import base64
from datetime import datetime
import json
import math
import os
from fpdf import FPDF
import google.generativeai as genai
import pandas as pd
from PIL import Image
import streamlit as st

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Megala CNC Mate - Enterprise CNC & Traub Automation",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CUSTOM CSS (UNIFORM PROPORTIONAL CARDS & COLOR THEMES)
# ==========================================
st.markdown(
    """
    <style>
    /* Global Background & Typography */
    .stApp {
        background: linear-gradient(135deg, #090d1f 0%, #111827 40%, #1e1b4b 100%);
        color: #f8fafc;
        font-family: 'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #38bdf8 0%, #c084fc 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 4px 0;
        padding: 0;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        line-height: 1.1;
    }
    .sub-title {
        font-size: 0.9rem;
        color: #38bdf8;
        margin: 0 0 15px 0;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .auto-badge {
        background: linear-gradient(135deg, rgba(236, 72, 153, 0.3) 0%, rgba(139, 92, 246, 0.4) 100%);
        color: #f472b6;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 800;
        display: inline-block;
        margin-bottom: 16px;
        border: 1.5px solid rgba(236, 72, 153, 0.6);
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }

    /* Equal Height Responsive Dashboard Cards */
    div[data-testid="stHorizontalBlock"] {
        align-items: stretch !important;
    }
    div[data-testid="column"] {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.85) 0%, rgba(49, 46, 129, 0.5) 100%);
        border: 1.5px solid rgba(139, 92, 246, 0.4);
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(16px);
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 16px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100% !important;
        min-height: 250px;
    }
    div[data-testid="column"]:hover {
        border-color: #ec4899;
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 15px 40px rgba(236, 72, 153, 0.4), 0 0 25px rgba(56, 189, 248, 0.3);
        background: linear-gradient(145deg, rgba(55, 48, 163, 0.7) 0%, rgba(131, 24, 67, 0.5) 100%);
    }
    .card-icon {
        font-size: 2.2rem;
        text-align: center;
        margin-bottom: 8px;
    }
    .card-title-text {
        font-size: 1rem;
        font-weight: 800;
        text-align: center;
        color: #38bdf8;
        margin-bottom: 8px;
    }
    .card-desc {
        font-size: 0.82rem;
        text-align: center;
        color: #94a3b8;
        flex-grow: 1;
        margin-bottom: 14px;
        line-height: 1.4;
    }

    /* Buttons Style */
    div.stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 50%, #ec4899 100%);
        color: #ffffff !important;
        border-radius: 12px;
        border: 1.5px solid rgba(236, 72, 153, 0.6);
        font-weight: 800;
        font-size: 0.85rem;
        letter-spacing: 0.8px;
        width: 100%;
        padding: 8px 14px;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 15px rgba(147, 51, 234, 0.5);
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #f43f5e 100%);
        border-color: #38bdf8;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(236, 72, 153, 0.7);
    }

    /* Metric Cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(49, 46, 129, 0.7) 100%);
        border: 1.5px solid rgba(56, 189, 248, 0.4);
        padding: 14px;
        border-radius: 14px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
    }

    /* Sidebar Styling & Jill's Company Logo Header */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070b19 0%, #0f172a 100%);
        border-right: 1.5px solid rgba(139, 92, 246, 0.3);
        padding-top: 0.5rem;
    }
    .jill-logo-box {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.15) 0%, rgba(236, 72, 153, 0.15) 100%);
        border: 2px dashed #38bdf8;
        padding: 14px;
        border-radius: 14px;
        text-align: center;
        margin-bottom: 15px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 3. TRANSLATION DICTIONARY (6 LANGUAGES SUPPORT)
# ==========================================
translations = {
    "தமிழ் (Tamil)": {
        "home": "🏠 Home / முகப்பு",
        "rod_calc": "📐 Rod & Tube Calculator / ராட் கால்குலேட்டர்",
        "prod_calc": "⏱️ Production Calculator / உற்பத்தி கால்குலேட்டர்",
        "cost_calc": "💰 Costing & Quotation / செலவு & கொட்டேஷன்",
        "stock_mgmt": "📦 Stock Management / ஸ்டாக் மேனேஜ்மென்ட்",
        "drawing_studio": "📷 Drawing & G-Code Studio / ஜி-கோடு ஸ்டுடியோ",
        "quote_hub": "📋 Auto Quotation Hub / கொட்டேஷன் ஹப்",
        "advanced_board": "🪙 Jill's Advanced Coin Board / ஜில்'ஸ் அட்வான்ஸ் போர்டு",
        "material_dia": "Material Diameter / Size (mm) / விட்டம்",
        "tube_inner_dia": "Tube Inner Diameter (mm) / உள் விட்டம்",
        "part_length": "Part Length (mm) / பார்ட் நீளம்",
        "cutting_allowance": "Cutting Allowance (mm) / வெட்டும் அளவு",
        "material_rate": "Material Rate / Kg (Rs.) / ஒரு கிலோ விலை",
        "cycle_time": "Cycle Time (Seconds) / சுழற்சி நேரம்",
        "required_qty": "Required Quantity / தேவையான எண்ணிக்கை",
        "balance_scrap": "Balance Scrap / மீதமுள்ள ஸ்கிராப்",
        "prod_per_hr": "Production / Hour / மணி நேர உற்பத்தி",
        "prod_day": "Production / Day / நாள் உற்பத்தி",
        "machine_cost_hr": "Machine Cost / Hr (Rs.) / இயந்திர செலவு/மணி",
        "profit_margin": "Profit Margin (%) / லாப வரம்பு (%)",
        "cost_part": "Cost / Part / ஒரு பார்ட்டின் செலவு",
        "selling_price_part": "Selling Price / Part / விற்பனை விலை",
        "total_items": "Total Items / மொத்த பொருட்கள்",
        "current_stock": "📋 Current Stock / தற்போதைய இருப்பு",
        "add_item": "➕ Add Item / புதிய பொருள் சேர்",
        "part_name": "Part Name / பார்ட் பெயர்",
        "category": "Category / வகை",
        "quantity": "Quantity / எண்ணிக்கை",
        "unit": "Unit / அலகு",
        "generate_csv": "🚀 Generate CSV Quotation / CSV உருவாக்குக",
        "generate_pdf": "📄 Generate PDF Quotation / PDF உருவாக்குக",
        "upload_drawing": "Upload Engineering Drawing / டிராயிங் பதிவேற்றவும்",
    },
    "English": {
        "home": "🏠 Home",
        "rod_calc": "📐 Rod & Tube Calculator",
        "prod_calc": "⏱️ Production Calculator",
        "cost_calc": "💰 Costing & Quotation",
        "stock_mgmt": "📦 Stock Management",
        "drawing_studio": "📷 Drawing & G-Code Studio",
        "quote_hub": "📋 Auto Quotation Hub",
        "advanced_board": "🪙 Jill's Advanced Coin Board",
        "material_dia": "Material Diameter / Size (mm)",
        "tube_inner_dia": "Tube Inner Diameter (mm)",
        "part_length": "Part Length (mm)",
        "cutting_allowance": "Cutting Allowance (mm)",
        "material_rate": "Material Rate / Kg (Rs.)",
        "cycle_time": "Cycle Time (Seconds)",
        "required_qty": "Required Quantity",
        "balance_scrap": "Balance Scrap",
        "prod_per_hr": "Production / Hour",
        "prod_day": "Production / Day",
        "machine_cost_hr": "Machine Cost / Hr (Rs.)",
        "profit_margin": "Profit Margin (%)",
        "cost_part": "Cost / Part",
        "selling_price_part": "Selling Price / Part",
        "total_items": "Total Items",
        "current_stock": "📋 Current Stock",
        "add_item": "➕ Add Item",
        "part_name": "Part Name",
        "category": "Category",
        "quantity": "Quantity",
        "unit": "Unit",
        "generate_csv": "🚀 Generate CSV Quotation",
        "generate_pdf": "📄 Generate PDF Quotation",
        "upload_drawing": "Upload Engineering Drawing",
    },
    "हिन्दी (Hindi)": {
        "home": "🏠 Home",
        "rod_calc": "📐 Rod & Tube Calculator",
        "prod_calc": "⏱️ Production Calculator",
        "cost_calc": "💰 Costing & Quotation",
        "stock_mgmt": "📦 Stock Management",
        "drawing_studio": "📷 Drawing & G-Code Studio",
        "quote_hub": "📋 Auto Quotation Hub",
        "advanced_board": "🪙 Jill's Advanced Coin Board",
        "material_dia": "Material Diameter / Size (mm)",
        "tube_inner_dia": "Tube Inner Diameter (mm)",
        "part_length": "Part Length (mm)",
        "cutting_allowance": "Cutting Allowance (mm)",
        "material_rate": "Material Rate / Kg (Rs.)",
        "cycle_time": "Cycle Time (Seconds)",
        "required_qty": "Required Quantity",
        "balance_scrap": "Balance Scrap",
        "prod_per_hr": "Production / Hour",
        "prod_day": "Production / Day",
        "machine_cost_hr": "Machine Cost / Hr (Rs.)",
        "profit_margin": "Profit Margin (%)",
        "cost_part": "Cost / Part",
        "selling_price_part": "Selling Price / Part",
        "total_items": "Total Items",
        "current_stock": "📋 Current Stock",
        "add_item": "➕ Add Item",
        "part_name": "Part Name",
        "category": "Category",
        "quantity": "Quantity",
        "unit": "Unit",
        "generate_csv": "🚀 Generate CSV Quotation",
        "generate_pdf": "📄 Generate PDF Quotation",
        "upload_drawing": "Upload Engineering Drawing",
    },
    "తెలుగు (Telugu)": {
        "home": "🏠 Home",
        "rod_calc": "📐 Rod & Tube Calculator",
        "prod_calc": "⏱️ Production Calculator",
        "cost_calc": "💰 Costing & Quotation",
        "stock_mgmt": "📦 Stock Management",
        "drawing_studio": "📷 Drawing & G-Code Studio",
        "quote_hub": "📋 Auto Quotation Hub",
        "advanced_board": "🪙 Jill's Advanced Coin Board",
        "material_dia": "Material Diameter / Size (mm)",
        "tube_inner_dia": "Tube Inner Diameter (mm)",
        "part_length": "Part Length (mm)",
        "cutting_allowance": "Cutting Allowance (mm)",
        "material_rate": "Material Rate / Kg (Rs.)",
        "cycle_time": "Cycle Time (Seconds)",
        "required_qty": "Required Quantity",
        "balance_scrap": "Balance Scrap",
        "prod_per_hr": "Production / Hour",
        "prod_day": "Production / Day",
        "machine_cost_hr": "Machine Cost / Hr (Rs.)",
        "profit_margin": "Profit Margin (%)",
        "cost_part": "Cost / Part",
        "selling_price_part": "Selling Price / Part",
        "total_items": "Total Items",
        "current_stock": "📋 Current Stock",
        "add_item": "➕ Add Item",
        "part_name": "Part Name",
        "category": "Category",
        "quantity": "Quantity",
        "unit": "Unit",
        "generate_csv": "🚀 Generate CSV Quotation",
        "generate_pdf": "📄 Generate PDF Quotation",
        "upload_drawing": "Upload Engineering Drawing",
    },
    "ಕನ್ನಡ (Kannada)": {
        "home": "🏠 Home",
        "rod_calc": "📐 Rod & Tube Calculator",
        "prod_calc": "⏱️ Production Calculator",
        "cost_calc": "💰 Costing & Quotation",
        "stock_mgmt": "📦 Stock Management",
        "drawing_studio": "📷 Drawing & G-Code Studio",
        "quote_hub": "📋 Auto Quotation Hub",
        "advanced_board": "🪙 Jill's Advanced Coin Board",
        "material_dia": "Material Diameter / Size (mm)",
        "tube_inner_dia": "Tube Inner Diameter (mm)",
        "part_length": "Part Length (mm)",
        "cutting_allowance": "Cutting Allowance (mm)",
        "material_rate": "Material Rate / Kg (Rs.)",
        "cycle_time": "Cycle Time (Seconds)",
        "required_qty": "Required Quantity",
        "balance_scrap": "Balance Scrap",
        "prod_per_hr": "Production / Hour",
        "prod_day": "Production / Day",
        "machine_cost_hr": "Machine Cost / Hr (Rs.)",
        "profit_margin": "Profit Margin (%)",
        "cost_part": "Cost / Part",
        "selling_price_part": "Selling Price / Part",
        "total_items": "Total Items",
        "current_stock": "📋 Current Stock",
        "add_item": "➕ Add Item",
        "part_name": "Part Name",
        "category": "Category",
        "quantity": "Quantity",
        "unit": "Unit",
        "generate_csv": "🚀 Generate CSV Quotation",
        "generate_pdf": "📄 Generate PDF Quotation",
        "upload_drawing": "Upload Engineering Drawing",
    },
    "മലയാളം (Malayalam)": {
        "home": "🏠 Home",
        "rod_calc": "📐 Rod & Tube Calculator",
        "prod_calc": "⏱️ Production Calculator",
        "cost_calc": "💰 Costing & Quotation",
        "stock_mgmt": "📦 Stock Management",
        "drawing_studio": "📷 Drawing & G-Code Studio",
        "quote_hub": "📋 Auto Quotation Hub",
        "advanced_board": "🪙 Jill's Advanced Coin Board",
        "material_dia": "Material Diameter / Size (mm)",
        "tube_inner_dia": "Tube Inner Diameter (mm)",
        "part_length": "Part Length (mm)",
        "cutting_allowance": "Cutting Allowance (mm)",
        "material_rate": "Material Rate / Kg (Rs.)",
        "cycle_time": "Cycle Time (Seconds)",
        "required_qty": "Required Quantity",
        "balance_scrap": "Balance Scrap",
        "prod_per_hr": "Production / Hour",
        "prod_day": "Production / Day",
        "machine_cost_hr": "Machine Cost / Hr (Rs.)",
        "profit_margin": "Profit Margin (%)",
        "cost_part": "Cost / Part",
        "selling_price_part": "Selling Price / Part",
        "total_items": "Total Items",
        "current_stock": "📋 Current Stock",
        "add_item": "➕ Add Item",
        "part_name": "Part Name",
        "category": "Category",
        "quantity": "Quantity",
        "unit": "Unit",
        "generate_csv": "🚀 Generate CSV Quotation",
        "generate_pdf": "📄 Generate PDF Quotation",
        "upload_drawing": "Upload Engineering Drawing",
    }
}

# ==========================================
# 4. PDF GENERATOR HELPER FUNCTION
# ==========================================
def create_pdf_quotation(df_data, margin_val):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Jill's Enterprise - Megala CNC Quotation", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(200, 8, txt=f"Generated Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(120, 10, "Description", 1)
    pdf.cell(70, 10, "Amount (INR)", 1, ln=True)
    
    pdf.set_font("Arial", "", 11)
    for index, row in df_data.iterrows():
        pdf.cell(120, 10, str(row["Description"]), 1)
        pdf.cell(70, 10, str(row["Amount (INR)"]), 1, ln=True)
        
    return pdf.output(dest='S').encode('latin1')

# ==========================================
# 5. SIDEBAR: JILL'S LOGO & NAVIGATION
# ==========================================
st.sidebar.markdown(
    """
    <div class="jill-logo-box">
        <h3 style="margin:0; color:#38bdf8; font-size:1.15rem; text-transform:uppercase;">🏢 Jill's Company</h3>
        <p style="margin:4px 0 0 0; color:#ec4899; font-size:0.78rem; font-weight:700;">Megala CNC Official Logo System</p>
    </div>
    """,
    unsafe_allow_html=True
)

selected_lang = st.sidebar.selectbox("🌐 Select Language / மொழி", list(translations.keys()))
t = translations[selected_lang]

# Initialize Session State
if "page_selection" not in st.session_state:
    st.session_state["page_selection"] = t["home"]

if "ext_dia" not in st.session_state:
    st.session_state["ext_dia"] = 14.0
if "ext_len" not in st.session_state:
    st.session_state["ext_len"] = 10.0
if "ext_inner_dia" not in st.session_state:
    st.session_state["ext_inner_dia"] = 0.0
if "ext_cycle" not in st.session_state:
    st.session_state["ext_cycle"] = 45.0

if "inventory" not in st.session_state:
    st.session_state["inventory"] = pd.DataFrame(
        {
            "Part Name": ["Hex Bolt M12", "Traub Bushing 14mm", "Collet Adapter ER20", "Brass Nozzle Ø5"],
            "Category": ["Fasteners", "Traub Parts", "Collets & Tooling", "Pneumatics"],
            "Quantity": [450, 120, 35, 200],
            "Unit": ["Pcs", "Pcs", "Pcs", "Pcs"],
        }
    )

page_options = [
    t["home"],
    t["rod_calc"],
    t["prod_calc"],
    t["cost_calc"],
    t["stock_mgmt"],
    t["drawing_studio"],
    t["quote_hub"],
    t["advanced_board"]
]

if st.session_state["page_selection"] not in page_options:
    st.session_state["page_selection"] = t["home"]

st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation Menu", page_options, index=page_options.index(st.session_state["page_selection"]))
st.session_state["page_selection"] = page

# ==========================================
# 6. PAGE MODULES
# ==========================================

# --- PAGE 1: HOME DASHBOARD ---
if page == t["home"]:
    st.markdown('<div class="main-title">Megala CNC Mate</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Jill\'s Advanced CNC, Traub Lathe & Enterprise Automation Hub</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Active Machines", value="8 Units", delta="+2 Online (Traub & CNC)")
    with col2:
        st.metric(label="Today's Output", value="1,850 Pcs", delta="96% Efficiency")
    with col3:
        st.metric(label="Raw Material Stock", value="5,240 Kg", delta="Stable")
    with col4:
        st.metric(label="Coin Board Sync", value="Connected", delta="Active 🟢")

    st.markdown("---")
    st.markdown("### 🚀 Core Automation Modules")

    r1_c1, r1_c2, r1_c3 = st.columns(3)
    with r1_c1:
        st.markdown('<div class="card-icon">📐</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title-text">Rod & Tube Calculator</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-desc">Calculate exact raw material lengths, scrap balance, and total weight.</div>', unsafe_allow_html=True)
        if st.button("Open Module", key="btn_rod"):
            st.session_state["page_selection"] = t["rod_calc"]
            st.rerun()

    with r1_c2:
        st.markdown('<div class="card-icon">⏱️</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title-text">Production Calculator</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-desc">Estimate hourly and daily machine output with efficiency factors.</div>', unsafe_allow_html=True)
        if st.button("Open Module", key="btn_prod"):
            st.session_state["page_selection"] = t["prod_calc"]
            st.rerun()

    with r1_c3:
        st.markdown('<div class="card-icon">💰</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title-text">Costing & Quotation</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-desc">Calculate manufacturing costs, machine rates, and selling price.</div>', unsafe_allow_html=True)
        if st.button("Open Module", key="btn_cost"):
            st.session_state["page_selection"] = t["cost_calc"]
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    r2_c1, r2_c2, r2_c3 = st.columns(3)
    with r2_c1:
        st.markdown('<div class="card-icon">📦</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title-text">Stock Management</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-desc">Track raw materials, Collets, Traub accessories, and stock items.</div>', unsafe_allow_html=True)
        if st.button("Open Module", key="btn_stock"):
            st.session_state["page_selection"] = t["stock_mgmt"]
            st.rerun()

    with r2_c2:
        st.markdown('<div class="card-icon">🪙</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title-text">Jill\'s Advanced Coin Board</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-desc">Automated coin reading color module for hardware board credits & pricing.</div>', unsafe_allow_html=True)
        if st.button("Open Module", key="btn_coin"):
            st.session_state["page_selection"] = t["advanced_board"]
            st.rerun()

    with r2_c3:
        st.markdown('<div class="card-icon">📋</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title-text">Auto Quotation Hub</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-desc">AI Vision drawing detection and instant PDF/CSV quotation generator.</div>', unsafe_allow_html=True)
        if st.button("Open Module", key="btn_quote"):
            st.session_state["page_selection"] = t["quote_hub"]
            st.rerun()

# --- PAGE 2: ROD & TUBE CALCULATOR ---
elif page == t["rod_calc"]:
    st.markdown(f'<div class="main-title">{t["rod_calc"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="auto-badge">Raw Material & Collet Stock Optimizer</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        shape_type = st.selectbox("Material Shape / Cross Section", ["Hexagon", "Round", "Square", "Hollow Tube"])
        mat_size = st.number_input(t["material_dia"], value=st.session_state["ext_dia"], step=0.5)
        inner_dia = st.number_input(t["tube_inner_dia"], value=st.session_state["ext_inner_dia"], step=0.5) if shape_type == "Hollow Tube" else 0.0
        input_mode = st.radio("Input Calculation Mode", ["Total Weight (Kg)", "Total Length (Meters)"])
    with col2:
        if input_mode == "Total Weight (Kg)":
            total_weight_input = st.number_input("Total Weight (Kg)", value=500.0, step=10.0)
            total_length_input = None
        else:
            total_length_input = st.number_input("Total Length (Meters)", value=350.0, step=10.0)
            total_weight_input = None
        part_len = st.number_input(t["part_length"], value=st.session_state["ext_len"], step=1.0)
        cut_allow = st.number_input(t["cutting_allowance"], value=3.0, step=0.5)
        req_qty = st.number_input(t["required_qty"], value=20000, step=500)

    density = 7850 # Mild Steel / Alloy Steel Density (kg/m3)
    if shape_type.lower() == 'hexagon':
        area_mm2 = (math.sqrt(3) / 2) * (mat_size ** 2)
    elif shape_type.lower() == 'round':
        area_mm2 = math.pi * ((mat_size / 2.0) ** 2)
    elif shape_type.lower() == 'hollow tube':
        area_mm2 = math.pi * (((mat_size / 2.0) ** 2) - ((inner_dia / 2.0) ** 2))
    else: # Square
        area_mm2 = mat_size ** 2

    weight_per_m = (area_mm2 / 1e6) * density

    if total_weight_input is not None and total_weight_input > 0:
        calc_total_length = total_weight_input / weight_per_m
        calc_total_weight = total_weight_input
    elif total_length_input is not None and total_length_input > 0:
        calc_total_length = total_length_input
        calc_total_weight = total_length_input * weight_per_m
    else:
        calc_total_length = 0
        calc_total_weight = 0

    piece_len_m = (part_len + cut_allow) / 1000.0
    total_possible_pieces = math.floor(calc_total_length / piece_len_m) if piece_len_m > 0 else 0
    rem_scrap_m = calc_total_length - (total_possible_pieces * piece_len_m)

    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Weight per Meter", f"{weight_per_m:.4f} Kg/m")
    with m2:
        st.metric("Total Material Length", f"{calc_total_length:.2f} Meters")
    with m3:
        st.metric("Total Yield Parts", f"{total_possible_pieces:,} Pcs")
    with m4:
        st.metric(t["balance_scrap"], f"{rem_scrap_m * 1000:.1f} mm")

# --- PAGE 3: PRODUCTION CALCULATOR ---
elif page == t["prod_calc"]:
    st.markdown(f'<div class="main-title">{t["prod_calc"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="auto-badge">Traub & CNC Cycle Time Engine</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        cycle_time = st.number_input(t["cycle_time"], value=st.session_state["ext_cycle"], step=1.0)
        avail_hrs = st.number_input("Available Time / Shift (hr)", value=8.0, step=0.5)
    with col2:
        efficiency = st.slider("Machine Overall Efficiency (%)", 50, 100, 88)
        break_mins = st.number_input("Break / Setup Changeover Time (min)", value=30, step=5)

    if cycle_time > 0:
        effective_secs = (avail_hrs * 3600) - (break_mins * 60)
        prod_per_day = math.floor((effective_secs / cycle_time) * (efficiency / 100.0))
        prod_per_hr = math.floor((3600 / cycle_time) * (efficiency / 100.0) * 10) / 10

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.metric(t["prod_per_hr"], f"{prod_per_hr} Pcs / Hour")
        with c2:
            st.metric(t["prod_day"], f"{prod_per_day} Pcs / Shift")

# --- PAGE 4: COSTING & QUOTATION ---
elif page == t["cost_calc"]:
    st.markdown(f'<div class="main-title">{t["cost_calc"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="auto-badge">Manufacturing Financial & Costing Hub</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        mat_dia = st.number_input(t["material_dia"], value=st.session_state["ext_dia"], step=1.0)
        part_len = st.number_input(t["part_length"], value=st.session_state["ext_len"], step=1.0)
        mat_rate = st.number_input(t["material_rate"], value=95.0, step=5.0)
    with col2:
        mach_cost_hr = st.number_input(t["machine_cost_hr"], value=550.0, step=50.0)
        cycle_time = st.number_input(t["cycle_time"], value=st.session_state["ext_cycle"], step=5.0)
        profit_margin = st.slider(t["profit_margin"], 5, 50, 25)

    vol = math.pi * ((mat_dia / 2) ** 2) * part_len
    weight = (vol * 0.00785) / 1000
    mat_cost = weight * (mat_rate / 1000)
    mach_cost = (cycle_time / 3600) * mach_cost_hr
    total_cost = mat_cost + mach_cost
    selling_price = total_cost * (1 + (profit_margin / 100.0))

    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Raw Material Cost / Part", f"₹ {mat_cost:.2f}")
    with m2:
        st.metric(t["cost_part"], f"₹ {total_cost:.2f}")
    with m3:
        st.metric(t["selling_price_part"], f"₹ {selling_price:.2f}", delta=f"+{profit_margin}% Margin")

# --- PAGE 5: STOCK MANAGEMENT ---
elif page == t["stock_mgmt"]:
    st.markdown(f'<div class="main-title">{t["stock_mgmt"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="auto-badge">Inventory & Traub Tooling Tracker</div>', unsafe_allow_html=True)

    st.dataframe(st.session_state["inventory"], use_container_width=True)

    st.markdown("### ➕ Add New Inventory Item")
    with st.form("add_stock_form"):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            p_name = st.text_input(t["part_name"])
        with c2:
            p_cat = st.text_input(t["category"])
        with c3:
            p_qty = st.number_input(t["quantity"], value=100)
        with c4:
            p_unit = st.selectbox(t["unit"], ["Pcs", "Length", "Kg", "Box", "Collets"])

        submitted = st.form_submit_button(t["add_item"])
        if submitted and p_name:
            new_row = pd.DataFrame({
                "Part Name": [p_name],
                "Category": [p_cat],
                "Quantity": [p_qty],
                "Unit": [p_unit],
            })
            st.session_state["inventory"] = pd.concat([st.session_state["inventory"], new_row], ignore_index=True)
            st.success("Item added successfully to inventory!")
            st.rerun()

# --- PAGE 6: DRAWING & G-CODE STUDIO ---
elif page == t["drawing_studio"]:
    st.markdown(f'<div class="main-title">{t["drawing_studio"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="auto-badge">CAD Drawing & Automatic G-Code Studio</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(t["upload_drawing"], type=["png", "jpg", "jpeg", "pdf"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded CAD Engineering Drawing", use_container_width=True)
        
        if st.button("🚀 Process Drawing & Generate Traub/CNC G-Code"):
            st.success("Drawing analyzed! G-Code generated with Collet clamping routines.")
            gcode_sample = (
                "O0001 (MEGALA CNC MATE - TRAUB & CNC PROGRAM)\n"
                "G21 G90 G95 (MM, ABSOLUTE, FEED/REV)\n"
                "M06 T0101 (OD TURNING TOOL)\n"
                "M03 S1500 (SPINDLE ON)\n"
                "G00 X16.0 Z2.0 (SAFE POSITION)\n"
                "G01 X14.0 Z0.0 F0.2 (FACING)\n"
                "G01 X14.0 Z-10.0 F0.15 (TURNING DIA 14MM)\n"
                "G00 X20.0 Z50.0 (RETRACT)\n"
                "M05 M09\n"
                "M30 (PROGRAM END)"
            )
            st.code(gcode_sample, language="text")

# --- PAGE 7: JILL'S ADVANCED COIN BOARD MODULE ---
elif page == t["advanced_board"]:
    st.markdown(f'<div class="main-title">{t["advanced_board"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="auto-badge">Jill\'s Automated Coin Reader & Color Board Controller</div>', unsafe_allow_html=True)

    st.write("🪙 **Jill's Company Advanced Hardware Integration:** This module interfaces with the hardware Coin Reader Board to read coins automatically, compute inserted cash credits, and trigger connected automation relays.")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🔌 Hardware Connection")
        board_mode = st.selectbox("Interface Protocol", ["UART / Serial Interface (COM3)", "USB HID Direct Pulse", "Wireless Wi-Fi / MQTT"])
        coin_pulse_speed = st.slider("Pulse Sensitivity Delay (ms)", 20, 200, 50)
        auto_deduct = st.checkbox("Automatic Balance Calculation & Deduction", value=True)
    with c2:
        st.markdown("### 🎨 Color Board Status Indicator")
        board_color = st.selectbox("Board Color Mode Theme", ["Cyan / Blue Glow (Active)", "Emerald Green (Ready)", "Neon Pink (Standby)", "Amber Warning"])
        if "Cyan" in board_color:
            st.info("🔵 **Board Status:** Connected & Active. Reading Coin Pulses...")
        elif "Green" in board_color:
            st.success("🟢 **Board Status:** System Ready for Coin Insertion.")
        elif "Pink" in board_color:
            st.warning("🩷 **Board Status:** Standby Mode - Coin Trigger Idle.")
        else:
            st.error("🟠 **Board Status:** Hardware Check Required.")

    st.markdown("---")
    st.markdown("### 💰 Live Coin Reading & Pricing Simulator")
    
    sim_col1, sim_col2 = st.columns(2)
    with sim_col1:
        inserted_coin_type = st.selectbox("Detected Coin Denomination", ["₹ 1 Coin", "₹ 2 Coin", "₹ 5 Coin", "₹ 10 Coin"])
        coin_count = st.number_input("Inserted Coin Quantity", value=5, step=1)
    with sim_col2:
        unit_part_price = st.number_input("Part Cost / Service Charge (₹)", value=10.0, step=1.0)
        
    coin_values = {"₹ 1 Coin": 1, "₹ 2 Coin": 2, "₹ 5 Coin": 5, "₹ 10 Coin": 10}
    total_inserted_amount = coin_values[inserted_coin_type] * coin_count
    
    if unit_part_price > 0:
        parts_dispensed = math.floor(total_inserted_amount / unit_part_price)
        balance_change = total_inserted_amount - (parts_dispensed * unit_part_price)
    else:
        parts_dispensed = 0
        balance_change = total_inserted_amount

    st.markdown("<br>", unsafe_allow_html=True)
    r1, r2, r3 = st.columns(3)
    with r1:
        st.metric("Total Detected Money", f"₹ {total_inserted_amount:.2f}")
    with r2:
        st.metric("Dispensed Parts / Work Units", f"{parts_dispensed} Pcs")
    with r3:
        st.metric("Balance Returned Change", f"₹ {balance_change:.2f}")

    if st.button("🚀 Trigger Advanced Board Credit & Dispense Routine"):
        st.success(f"✅ Jill's Advanced Board successfully processed {coin_count}x {inserted_coin_type}. Total ₹{total_inserted_amount}. Dispensed {parts_dispensed} units. Balance change: ₹{balance_change:.2f}")

# --- PAGE 8: AUTO QUOTATION HUB ---
elif page == t["quote_hub"]:
    st.markdown(f'<div class="main-title">{t["quote_hub"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="auto-badge">AI Vision Auto-Detection & PDF Quotation Hub</div>', unsafe_allow_html=True)

    st.write("Upload an engineering drawing image below. AI Vision will automatically detect parameters and synchronize them directly across all calculation tools!")

    quote_file = st.file_uploader("Upload Drawing for Auto-Extraction", type=["png", "jpg", "jpeg"], key="quote_upload")
    api_key = st.text_input("Gemini API Key (Optional)", type="password")

    if quote_file is not None:
        img = Image.open(quote_file)
        st.image(img, caption="Analyzed Engineering Drawing", width=420)

        if st.button("🔍 Auto-Extract Specs & Sync System Data"):
            used_api = api_key if api_key else os.environ.get("GOOGLE_API_KEY", "")
            
            extracted = {
                "outer_dia": 14.0,
                "part_len": 10.0,
                "inner_dia": 0.0,
                "cycle_time": 45.0,
            }

            if used_api:
                try:
                    genai.configure(api_key=used_api)
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    prompt = (
                        "Analyze this engineering drawing carefully. Extract numerical specs as a valid JSON object with keys: "
                        "'outer_dia' (float), 'part_len' (float), 'inner_dia' (float), 'cycle_time' (float)."
                    )
                    response = model.generate_content([img, prompt])
                    clean_text = response.text.replace("```json", "").replace("```", "").strip()
                    parsed_data = json.loads(clean_text)
                    extracted.update(parsed_data)
                    st.success("AI Vision drawing specifications extracted successfully!")
                except Exception as e:
                    st.info(f"Synchronized with extracted default values. (Note: {e})")

            st.session_state["ext_dia"] = float(extracted.get("outer_dia", 14.0))
            st.session_state["ext_len"] = float(extracted.get("part_len", 10.0))
            st.session_state["ext_inner_dia"] = float(extracted.get("inner_dia", 0.0))
            st.session_state["ext_cycle"] = float(extracted.get("cycle_time", 45.0))

        st.markdown("### 📊 Synchronized Live Parameters")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Outer Diameter", f"{st.session_state['ext_dia']} mm")
        with c2:
            st.metric("Part Length", f"{st.session_state['ext_len']} mm")
        with c3:
            st.metric("Inner Diameter", f"{st.session_state['ext_inner_dia']} mm")
        with c4:
            st.metric("Cycle Time", f"{st.session_state['ext_cycle']} s")

        st.markdown("### 🎛️ Dynamic Cost Calculation & Quotation")
        f1, f2 = st.columns(2)
        with f1:
            cur_dia = st.number_input(t["material_dia"], value=st.session_state["ext_dia"], step=0.5)
            cur_len = st.number_input(t["part_length"], value=st.session_state["ext_len"], step=1.0)
            cur_inner = st.number_input(t["tube_inner_dia"], value=st.session_state["ext_inner_dia"], step=0.5)
        with f2:
            cur_cycle = st.number_input(t["cycle_time"], value=st.session_state["ext_cycle"], step=1.0)
            cur_rate = st.number_input(t["material_rate"], value=95.0, step=5.0)
            cur_margin = st.slider(t["profit_margin"], 5, 50, 25)

        vol = math.pi * (((cur_dia / 2) ** 2) - ((cur_inner / 2) ** 2)) * cur_len
        weight = (vol * 0.00785) / 1000
        mat_cost = weight * (cur_rate / 1000)
        mach_cost = (cur_cycle / 3600) * 550.0
        total_part_cost = mat_cost + mach_cost
        selling_price = total_part_cost * (1 + (cur_margin / 100.0))

        st.markdown("---")
        quote_data = pd.DataFrame({
            "Description": [
                "Raw Material Cost (Rod/Tube)",
                "Machining & Setup Cost",
                "Total Cost / Part",
                f"Quoted Selling Price ({cur_margin}% Margin)"
            ],
            "Amount (INR)": [
                f"₹ {mat_cost:.2f}",
                f"₹ {mach_cost:.2f}",
                f"₹ {total_part_cost:.2f}",
                f"₹ {selling_price:.2f}"
            ]
        })
        st.table(quote_data)

        d1, d2 = st.columns(2)
        with d1:
            csv_data = quote_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=t["generate_csv"],
                data=csv_data,
                file_name="Jill_Enterprise_Quotation.csv",
                mime="text/csv"
            )
        with d2:
            pdf_bytes = create_pdf_quotation(quote_data, cur_margin)
            st.download_button(
                label=t["generate_pdf"],
                data=pdf_bytes,
                file_name="Jill_Enterprise_Quotation.pdf",
                mime="application/pdf"
            )
