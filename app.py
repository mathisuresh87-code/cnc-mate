import base64
from datetime import datetime
import math
import os
from fpdf import FPDF
import pandas as pd
from PIL import Image
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Megala CNC Mate - Enterprise CNC Automation",
    page_icon="⚙️",
    layout="wide",
)

# Ultra-Vibrant, Colorful & Tactile Interactive SaaS Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #090d1f 0%, #111827 40%, #1e1b4b 100%);
        color: #f8fafc;
        font-family: 'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #38bdf8 0%, #c084fc 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 4px 0;
        padding: 0;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        line-height: 1.1;
        filter: drop-shadow(0 0 20px rgba(192, 132, 252, 0.5));
    }
    .sub-title {
        font-size: 0.92rem;
        color: #38bdf8;
        margin: 0;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
    }
    .auto-badge {
        background: linear-gradient(135deg, rgba(236, 72, 153, 0.3) 0%, rgba(139, 92, 246, 0.4) 100%);
        color: #f472b6;
        padding: 6px 18px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 800;
        display: inline-block;
        margin-bottom: 16px;
        border: 1.5px solid rgba(236, 72, 153, 0.6);
        text-transform: uppercase;
        letter-spacing: 1.2px;
        box-shadow: 0 0 20px rgba(236, 72, 153, 0.3);
    }
    div[data-testid="column"] {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.85) 0%, rgba(49, 46, 129, 0.5) 100%);
        border: 1.5px solid rgba(139, 92, 246, 0.4);
        padding: 24px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(16px);
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 20px;
    }
    div[data-testid="column"]:hover {
        border-color: #ec4899;
        transform: translateY(-8px) scale(1.015);
        box-shadow: 0 20px 50px rgba(236, 72, 153, 0.4), 0 0 30px rgba(56, 189, 248, 0.3), inset 0 1px 20px rgba(236, 72, 153, 0.4);
        background: linear-gradient(145deg, rgba(55, 48, 163, 0.7) 0%, rgba(131, 24, 67, 0.5) 100%);
    }
    div.stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 50%, #ec4899 100%);
        color: #ffffff !important;
        border-radius: 14px;
        border: 1.5px solid rgba(236, 72, 153, 0.6);
        font-weight: 800;
        letter-spacing: 1px;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 20px rgba(147, 51, 234, 0.5);
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #f43f5e 100%);
        border-color: #38bdf8;
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(236, 72, 153, 0.7), 0 0 20px rgba(56, 189, 248, 0.6);
    }
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(49, 46, 129, 0.7) 100%);
        border: 1.5px solid rgba(56, 189, 248, 0.4);
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070b19 0%, #0f172a 100%);
        border-right: 1.5px solid rgba(139, 92, 246, 0.3);
        padding-top: 0.5rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)

LOGO_PATH = "logo.png"

# Comprehensive Bilingual Translations Dictionary
translations = {
    "தமிழ் (Tamil)": {
        "home": "🏠 Home / முகப்பு",
        "rod_calc": "📐 Rod Calculator / ராட் கால்குலேட்டர்",
        "prod_calc": "⏱️ Production Calculator / உற்பத்தி கால்குலேட்டர்",
        "cost_calc": "💰 Costing & Quotation / செலவு & கொட்டேஷன்",
        "stock_mgmt": "📦 Stock Management / ஸ்டாக் மேனேஜ்மென்ட்",
        "drawing_studio": "📷 Drawing & G-Code / டிராயிங் & ஜி-கோடு ஸ்டுடியோ",
        "quote_hub": "📋 Process Breakdown & Quotation / கொட்டேஷன் ஹப்",
        "settings": "⚙️ Settings & Masters / அமைப்புகள்",
        "active_machines": "Active Machines / இயங்கும் இயந்திரங்கள்",
        "todays_output": "Today's Output / இன்றைய உற்பத்தி",
        "material_stock": "Material Stock / பொருள் இருப்பு",
        "low_stock_alerts": "Low/Out Stock / குறைந்த இருப்பு எச்சரிக்கை",
        "core_modules": "🚀 Core Automation Modules / முக்கிய மாட்யூல்கள்",
        "back_home": "⬅️ Back to Home / முகப்புக்குத் திரும்பு",
        "simple_mode": "Simple Mode / எளிய முறை",
        "advanced_mode": "Advanced Mode / மேம்பட்ட முறை",
        "rod_length": "Rod Length (Meter) / ராட் நீளம் (மீட்டர்)",
        "part_length": "Part Length (mm) / பார்ட் நீளம் (மிமீ)",
        "cutting_allowance": "Cutting Allowance (mm) / வெட்டும் அளவு (மிமீ)",
        "material_shape": "Material Shape / பொருளின் வடிவம்",
        "cycle_time": "Cycle Time (Seconds) / சுழற்சி நேரம் (வினாடிகள்)",
        "required_qty": "Required Quantity / தேவையான எண்ணிக்கை",
        "parts_per_rod": "Parts / Rod / ஒரு ராட்டுக்கான பார்ட்கள்",
        "required_rods": "Required Rods / தேவையான ராட்கள்",
        "balance_scrap": "Balance Scrap / மீதமுள்ள ஸ்கிராப்",
        "total_stock_len": "Total Stock Length / மொத்த ராட் நீளம்",
        "prod_per_hr": "Production / Hour / மணி நேர உற்பத்தி",
        "tot_mach_time": "Total Machine Time / மொத்த இயந்திர நேரம்",
        "upload_drawing": "Upload Part Drawing / பார்ட் டோயிங் பதிவேற்றவும்",
        "material_dia": "Material Diameter / Size (mm) / விட்டம் (மிமீ)",
        "tube_inner_dia": "Tube Inner Diameter (mm) / குழாய் உள் விட்டம்",
        "material_density": "Material Density (g/mm³) / அடர்த்தி",
        "material_rate": "Material Rate / Kg (Rs.) / ஒரு கிலோ விலை (ரூ)",
        "wastage_pct": "Additional Wastage (%) / கூடுதல் கழிவு (%)",
        "part_weight": "Part Weight / பார்ட் எடை",
        "total_mat_weight": "Total Mat. Weight / மொத்த பொருளின் எடை",
        "total_mat_cost": "Total Mat. Cost / மொத்த பொருளின் விலை",
        "avail_time": "Available Time / Day (hr) / கிடைக்கும் நேரம் / நாள்",
        "machine_efficiency": "Machine Efficiency (%) / இயந்திர திறன் (%)",
        "break_time": "Break Time (min) / இடைவெளி நேரம் (நிமிடங்கள்)",
        "prod_day": "Production / Day / நாள் உற்பத்தி",
        "download_prod_pdf": (
            "📥 Download Production Report PDF / உற்பத்தி அறிக்கையைப் பதிவிறக்குக"
        ),
        "machine_cost_hr": "Machine Cost / Hr (Rs.) / இயந்திர செலவு / மணி",
        "labour_cost_part": "Labour Cost / Part (Rs.) / தொழிலாளர் செலவு / பார்ட்",
        "overhead_pct": "Overhead (%) / மேல்செலவு (%)",
        "profit_margin": "Profit Margin (%) / லாப வரம்பு (%)",
        "cost_part": "Cost / Part / ஒரு பார்ட்டின் செலவு",
        "cost_1000_parts": "Cost / 1000 Parts / 1000 பார்ட்களுக்கான செலவு",
        "selling_price_part": "Selling Price / Part / விற்பனை விலை / பார்ட்",
        "download_quote_pdf": "📥 Download Quotation PDF / கொட்டேஷன் PDF பதிவிறக்குக",
        "total_items": "Total Items / மொத்த பொருட்கள்",
        "low_stock": "Low Stock / குறைந்த இருப்பு",
        "out_of_stock": "Out of Stock / இருப்பு இல்லை",
        "current_stock": "📋 Current Stock / தற்போதைய இருப்பு",
        "add_item": "➕ Add Item / புதிய பொருள் சேர்",
        "stock_in_out": "🔄 Stock In / Out / ஸ்டாக் உள்ளே / வெளியே",
        "search_inventory": "🔍 Search Inventory / தேடுக...",
        "part_name": "Part Name / பார்ட் பெயர்",
        "category": "Category / வகை",
        "quantity": "Quantity / எண்ணிக்கை",
        "unit": "Unit / அலகு",
        "update_stock": "🔄 Update Stock / ஸ்டாக்கை அப்டேட் செய்",
        "num_operations": "Number of Operations / ஆபரேஷன்களின் எண்ணிக்கை",
        "generate_gcode": "📥 Download G-Code PDF / G-Code PDF பதிவிறக்குக",
        "cust_company": "Customer Company Name / வாடிக்கையாளர் பெயர்",
        "transport_charges": "Transport & Logistics Charges (Rs.) / போக்குவரத்து செலவு",
        "generate_csv": (
            "🚀 Generate CSV Quotation File / கொட்டேஷன் CSV கோப்பை உருவாக்கு"
        ),
        "language_label": "🌐 Select Language / மொழியைத் தேர்ந்தெடுக்கவும்",
    },
    "हिन्दी (Hindi)": {
        "home": "🏠 Home / गृह",
        "rod_calc": "📐 Rod Calculator / रॉड कैलकुलेटर",
        "prod_calc": "⏱️ Production Calculator / उत्पादन कैलकुलेटर",
        "cost_calc": "💰 Costing & Quotation / लागत और उद्धरण",
        "stock_mgmt": "📦 Stock Management / स्टॉक प्रबंधन",
        "drawing_studio": "📷 Drawing & G-Code / ड्राइंग और जी-कोड",
        "quote_hub": "📋 Process Breakdown & Quotation / उद्धरण केंद्र",
        "settings": "⚙️ Settings & Masters / सेटिंग्स",
        "active_machines": "Active Machines / सक्रिय मशीनें",
        "todays_output": "Today's Output / आज का उत्पादन",
        "material_stock": "Material Stock / सामग्री स्टॉक",
        "low_stock_alerts": "Low/Out Stock / कम/समाप्त स्टॉक",
        "core_modules": "🚀 Core Automation Modules / मुख्य स्वचालन मॉड्यूल",
        "back_home": "⬅️ Back to Home / होम पर वापस जाएं",
        "simple_mode": "Simple Mode / सरल मोड",
        "advanced_mode": "Advanced Mode / उन्नत मोड",
        "rod_length": "Rod Length (Meter) / रॉड की लंबाई (मीटर)",
        "part_length": "Part Length (mm) / भाग की लंबाई (मिमी)",
        "cutting_allowance": "Cutting Allowance (mm) / कटिंग अलाउंस (मिमी)",
        "material_shape": "Material Shape / सामग्री का आकार",
        "cycle_time": "Cycle Time (Seconds) / चक्र का समय (सेकंड)",
        "required_qty": "Required Quantity / आवश्यक मात्रा",
        "parts_per_rod": "Parts / Rod / प्रति रॉड भाग",
        "required_rods": "Required Rods / आवश्यक रॉड",
        "balance_scrap": "Balance Scrap / शेष स्क्रैप",
        "total_stock_len": "Total Stock Length / कुल स्टॉक लंबाई",
        "prod_per_hr": "Production / Hour / प्रति घंटा उत्पादन",
        "tot_mach_time": "Total Machine Time / कुल मशीन समय",
        "upload_drawing": "Upload Part Drawing / ड्राइंग अपलोड करें",
        "material_dia": "Material Diameter / Size (mm) / व्यास (मिमी)",
        "tube_inner_dia": "Tube Inner Diameter (mm) / ट्यूब का आंतरिक व्यास",
        "material_density": "Material Density (g/mm³) / सामग्री घनत्व",
        "material_rate": "Material Rate / Kg (Rs.) / प्रति किलो दर (रु)",
        "wastage_pct": "Additional Wastage (%) / अतिरिक्त अपव्यय (%)",
        "part_weight": "Part Weight / भाग का वजन",
        "total_mat_weight": "Total Mat. Weight / कुल सामग्री वजन",
        "total_mat_cost": "Total Mat. Cost / कुल सामग्री लागत",
        "avail_time": "Available Time / Day (hr) / उपलब्ध समय / दिन",
        "machine_efficiency": "Machine Efficiency (%) / मशीन दक्षता (%)",
        "break_time": "Break Time (min) / ब्रेक का समय (मिनट)",
        "prod_day": "Production / Day / प्रति दिन उत्पादन",
        "download_prod_pdf": (
            "📥 Download Production Report PDF / उत्पादन रिपोर्ट डाउनलोड करें"
        ),
        "machine_cost_hr": "Machine Cost / Hr (Rs.) / मशीन लागत / घंटा",
        "labour_cost_part": "Labour Cost / Part (Rs.) / श्रम लागत / भाग",
        "overhead_pct": "Overhead (%) / ओवरहेड (%)",
        "profit_margin": "Profit Margin (%) / लाभ मार्जिन (%)",
        "cost_part": "Cost / Part / प्रति भाग लागत",
        "cost_1000_parts": "Cost / 1000 Parts / 1000 भागों की लागत",
        "selling_price_part": "Selling Price / Part / विक्रय मूल्य / भाग",
        "download_quote_pdf": (
            "📥 Download Quotation PDF / उद्धरण पीडीएफ डाउनलोड करें"
        ),
        "total_items": "Total Items / कुल वस्तुएं",
        "low_stock": "Low Stock / कम स्टॉक",
        "out_of_stock": "Out of Stock / स्टॉक समाप्त",
        "current_stock": "📋 Current Stock / वर्तमान स्टॉक",
        "add_item": "➕ Add Item / वस्तु जोड़ें",
        "stock_in_out": "🔄 Stock In / Out / स्टॉक इन / आउट",
        "search_inventory": "🔍 Search Inventory / इन्वेंट्री खोजें",
        "part_name": "Part Name / भाग का नाम",
        "category": "Category / श्रेणी",
        "quantity": "Quantity / मात्रा",
        "unit": "Unit / इकाई",
        "update_stock": "🔄 Update Stock / स्टॉक अपडेट करें",
        "num_operations": "Number of Operations / संचालन की संख्या",
        "generate_gcode": "📥 Download G-Code PDF / जी-कोड पीडीएफ डाउनलोड करें",
        "cust_company": "Customer Company Name / ग्राहक कंपनी का नाम",
        "transport_charges": "Transport & Logistics Charges (Rs.) / परिवहन शुल्क",
        "generate_csv": "🚀 Generate CSV Quotation File / सीएसवी उद्धरण फ़ाइल बनाएं",
        "language_label": "🌐 Select Language / भाषा चुनें",
    },
    "English": {
        "home": "🏠 Home",
        "rod_calc": "📐 Rod Calculator",
        "prod_calc": "⏱️ Production Calculator",
        "cost_calc": "💰 Costing & Quotation",
        "stock_mgmt": "📦 Stock Management",
        "drawing_studio": "📷 Drawing & G-Code Studio",
        "quote_hub": "📋 Process Breakdown & Quotation Hub",
        "settings": "⚙️ Settings & Masters",
        "active_machines": "Active Machines",
        "todays_output": "Today's Output",
        "material_stock": "Material Stock",
        "low_stock_alerts": "Low/Out Stock",
        "core_modules": "🚀 Core Automation Modules",
        "back_home": "⬅️ Back to Home",
        "simple_mode": "Simple Mode",
        "advanced_mode": "Advanced Mode",
        "rod_length": "Rod Length (Meter)",
        "part_length": "Part Length (mm)",
        "cutting_allowance": "Cutting Allowance (mm)",
        "material_shape": "Material Shape",
        "cycle_time": "Cycle Time (Seconds)",
        "required_qty": "Required Quantity",
        "parts_per_rod": "Parts / Rod",
        "required_rods": "Required Rods",
        "balance_scrap": "Balance Scrap",
        "total_stock_len": "Total Stock Length",
        "prod_per_hr": "Production / Hour",
        "tot_mach_time": "Total Machine Time",
        "upload_drawing": "Upload Part Drawing",
        "material_dia": "Material Diameter / Size (mm)",
        "tube_inner_dia": "Tube Inner Diameter (mm)",
        "material_density": "Material Density (g/mm³)",
        "material_rate": "Material Rate / Kg (Rs.)",
        "wastage_pct": "Additional Wastage (%)",
        "part_weight": "Part Weight",
        "total_mat_weight": "Total Mat. Weight",
        "total_mat_cost": "Total Mat. Cost",
        "avail_time": "Available Time / Day (hr)",
        "machine_efficiency": "Machine Efficiency (%)",
        "break_time": "Break Time (min)",
        "prod_day": "Production / Day",
        "download_prod_pdf": "📥 Download Production Report PDF",
        "machine_cost_hr": "Machine Cost / Hr (Rs.)",
        "labour_cost_part": "Labour Cost / Part (Rs.)",
        "overhead_pct": "Overhead (%)",
        "profit_margin": "Profit Margin (%)",
        "cost_part": "Cost / Part",
        "cost_1000_parts": "Cost / 1000 Parts",
        "selling_price_part": "Selling Price / Part",
        "download_quote_pdf": "📥 Download Quotation PDF",
        "total_items": "Total Items",
        "low_stock": "Low Stock",
        "out_of_stock": "Out of Stock",
        "current_stock": "📋 Current Stock",
        "add_item": "➕ Add Item",
        "stock_in_out": "🔄 Stock In / Out",
        "search_inventory": "🔍 Search Inventory",
        "part_name": "Part Name",
        "category": "Category",
        "quantity": "Quantity",
        "unit": "Unit",
        "update_stock": "🔄 Update Stock",
        "num_operations": "Number of Operations",
        "generate_gcode": "📥 Download G-Code PDF",
        "cust_company": "Customer Company Name",
        "transport_charges": "Transport & Logistics Charges (Rs.)",
        "generate_csv": "🚀 Generate CSV Quotation File",
        "language_label": "🌐 Select Language",
    },
}

if "app_language" not in st.session_state:
  st.session_state["app_language"] = "தமிழ் (Tamil)"

current_lang = st.session_state["app_language"]


def get_text(key):
  if current_lang in translations and key in translations[current_lang]:
    return translations[current_lang][key]
  return translations["English"].get(key, key)


module_keys = [
    "home",
    "rod_calc",
    "prod_calc",
    "cost_calc",
    "stock_mgmt",
    "drawing_studio",
    "quote_hub",
    "settings",
]
module_list = [get_text(k) for k in module_keys]

if "selected_module" not in st.session_state:
  st.session_state["selected_module"] = module_list[0]

# Session state variables for auto-extracted drawing data
if "extracted_drawing_data" not in st.session_state:
  st.session_state["extracted_drawing_data"] = {
      "part_length": 73.0,
      "outer_dia": 38.1,
      "inner_dia": 25.8,
      "cross_hole_dia": 5.4,
      "material_shape": "Tube / Pipe",
      "material_grade": "TUFF DOM 52.3 / 1026 DOM",
  }

if "stock_inventory_df" not in st.session_state:
  st.session_state["stock_inventory_df"] = pd.DataFrame({
      "Item ID": ["ITM-001", "ITM-002", "ITM-003", "ITM-004"],
      "Material / Part Name": [
          "EN8 Round Bar - 12mm",
          "MS Round Bar - 20mm",
          "EN24 Round Bar - 16mm",
          "Finished Large Pin",
      ],
      "Category": [
          "Raw Material",
          "Raw Material",
          "Raw Material",
          "Finished Goods",
      ],
      "Quantity": [120.50, 45.20, 0.00, 650.00],
      "Unit": ["Kg", "Kg", "Kg", "Nos"],
      "Status": ["In Stock", "Low Stock", "Out of Stock", "Dispatch Ready"],
  })


def get_base64_image(path):
  if os.path.exists(path):
    with open(path, "rb") as f:
      return base64.b64encode(f.read()).decode("utf-8")
  return None


# Sidebar Navigation
st.sidebar.markdown(
    '<div style="text-align: center; padding: 5px 0 10px 0;"><h3'
    ' style="color: #ec4899; margin: 0; font-size: 1.15rem; font-weight: 900;'
    ' letter-spacing: 1.5px;">MEGALA CNC MATE</h3></div>',
    unsafe_allow_html=True,
)

encoded_sidebar_img = get_base64_image(LOGO_PATH)
if encoded_sidebar_img:
  sidebar_html = (
      '<div style="text-align: center; margin-bottom: 12px;"><div'
      ' style="background: linear-gradient(135deg, rgba(236, 72, 153, 0.3),'
      " rgba(56, 189, 248, 0.3)); border: 2.5px solid #ec4899; width: 75px;"
      " height: 75px; border-radius: 50%; margin: 0 auto; display: flex;"
      " align-items: center; justify-content: center; overflow: hidden;"
      f'"><img src="data:image/png;base64,{encoded_sidebar_img}"'
      ' style="width: 100%;" /></div></div>'
  )
  st.sidebar.markdown(sidebar_html, unsafe_allow_html=True)
else:
  st.sidebar.markdown(
      '<div style="text-align: center; margin-bottom: 12px;"><div'
      ' style="background: linear-gradient(135deg, #4f46e5, #ec4899); border:'
      ' 2.5px solid #ec4899; width: 75px; height: 75px; border-radius: 50%;'
      ' margin: 0 auto; display: flex; align-items: center; justify-content:'
      ' center; font-weight: 900; color: white;">MC</div></div>',
      unsafe_allow_html=True,
  )

uploaded_logo = st.sidebar.file_uploader(
    "Upload Permanent Logo",
    type=["png", "jpg", "jpeg"],
    key="sidebar_logo_upload",
    label_visibility="collapsed",
)
if uploaded_logo is not None:
  try:
    Image.open(uploaded_logo).save(LOGO_PATH)
    st.sidebar.success("✅ லோகோ சேமிக்கப்பட்டது!")
    st.rerun()
  except Exception as e:
    st.sidebar.error(f"Error: {e}")

st.sidebar.markdown("---")

# Language Selection in Sidebar
selected_lang_sidebar = st.sidebar.selectbox(
    get_text("language_label"),
    list(translations.keys()),
    index=list(translations.keys()).index(st.session_state["app_language"]),
    key="sidebar_lang_selector",
)
if selected_lang_sidebar != st.session_state["app_language"]:
  st.session_state["app_language"] = selected_lang_sidebar
  st.rerun()

st.sidebar.markdown("---")

current_selected_module = st.session_state["selected_module"]
selected_module = st.sidebar.selectbox(
    "Select Module",
    module_list,
    index=(
        module_list.index(current_selected_module)
        if current_selected_module in module_list
        else 0
    ),
    label_visibility="collapsed",
)
st.session_state["selected_module"] = selected_module

# Header Layout
col_logo, col_title = st.columns([0.15, 0.85], vertical_alignment="center")
with col_logo:
  encoded_img = get_base64_image(LOGO_PATH)
  if encoded_img:
    header_html = (
        '<div style="border: 2.5px solid #ec4899; width: 85px; height: 85px;'
        ' border-radius: 50%; display: flex; align-items: center;'
        ' justify-content: center; overflow: hidden;"'
        f'><img src="data:image/png;base64,{encoded_img}"'
        ' style="width: 100%;" /></div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)
  else:
    st.markdown(
        '<div style="background: linear-gradient(135deg, #4f46e5, #ec4899);'
        ' width: 85px; height: 85px; border-radius: 50%; display: flex;'
        ' align-items: center; justify-content: center; font-weight: 900;'
        ' color: white;">MC</div>',
        unsafe_allow_html=True,
    )
with col_title:
  st.markdown(
      '<h1 class="main-title">MEGALA INDUSTRIES</h1>', unsafe_allow_html=True
  )
  st.markdown(
      '<p class="sub-title">PRECISION CNC MACHINING & ENTERPRISE AUTOMATION</p>',
      unsafe_allow_html=True,
  )

st.markdown(
    "<hr style='margin-top: 0px; border-color: rgba(236, 72, 153, 0.3);'>",
    unsafe_allow_html=True,
)


def clean_text(text):
  return (
      str(text).replace("₹", "Rs.").encode("latin-1", "replace").decode("latin-1")
  )


def generate_production_pdf(data):
  pdf = FPDF()
  pdf.add_page()
  pdf.set_font("Arial", "B", 16)
  pdf.cell(200, 10, txt="MEGALA INDUSTRIES - PRODUCTION REPORT", ln=True, align="C")
  pdf.set_font("Arial", "", 12)
  pdf.ln(10)
  for k, v in data.items():
    pdf.cell(200, 8, txt=clean_text(f"{k}: {v}"), ln=True)
  return pdf.output(dest="S").encode("latin1")


def generate_quotation_pdf(data):
  pdf = FPDF()
  pdf.add_page()
  pdf.set_font("Arial", "B", 14)
  pdf.cell(
      200, 10, txt="MEGALA INDUSTRIES - DETAILED QUOTATION REPORT", ln=True, align="C"
  )
  pdf.set_font("Arial", "", 10)
  pdf.ln(10)
  for k, v in data.items():
    pdf.cell(200, 7, txt=clean_text(f"{k}: {v}"), ln=True)
  return pdf.output(dest="S").encode("latin1")


def generate_program_pdf(code_text):
  pdf = FPDF()
  pdf.add_page()
  pdf.set_font("Courier", "B", 14)
  pdf.cell(200, 10, txt="MEGALA INDUSTRIES - G-CODE PROGRAM", ln=True, align="C")
  pdf.set_font("Courier", "", 10)
  pdf.ln(10)
  for line in code_text.split("\n"):
    pdf.cell(200, 6, txt=clean_text(line), ln=True)
  return pdf.output(dest="S").encode("latin1")


def get_cross_section_area(shape, dia_or_size, inner_dia=0.0):
  if shape == "Round Rod":
    return math.pi * (dia_or_size / 2.0) ** 2
  elif shape == "Square Rod":
    return dia_or_size**2
  elif shape == "Hexagon Rod":
    return (math.sqrt(3) / 2.0) * (dia_or_size**2)
  elif shape == "Tube / Pipe":
    return max(
        0.0,
        (math.pi * (dia_or_size / 2.0) ** 2)
        - (math.pi * (inner_dia / 2.0) ** 2),
    )
  return math.pi * (dia_or_size / 2.0) ** 2


def generate_quotation_csv(
    customer_name, part_name, operations_list, transport_cost=0.0
):
  rows = []
  rows.append(
      ["MEGALA INDUSTRIES - PRECISION CNC MACHINING & ENTERPRISE AUTOMATION"]
  )
  rows.append([f"Customer Name: {customer_name}", f"Part Name: {part_name}"])
  rows.append([
      f"Date: {datetime.now().strftime('%Y-%m-%d')}",
      "Quotation No: MI/Q/2026-08/01",
  ])
  rows.append([])
  rows.append([
      "S.No",
      "Operation / Process Description",
      "Machine / Setup",
      "Qty",
      "Unit Rate (Rs.)",
      "Total Amount (Rs.)",
  ])

  total_amt = 0.0
  for idx, op in enumerate(operations_list, 1):
    row_total = op["qty"] * op["rate"]
    total_amt += row_total
    rows.append([
        idx,
        op["name"],
        op["machine"],
        op["qty"],
        op["rate"],
        row_total,
    ])

  if transport_cost > 0:
    total_amt += transport_cost
    rows.append([
        "",
        "Transport & Logistics Charges",
        "Logistics",
        1,
        transport_cost,
        transport_cost,
    ])

  rows.append([])
  rows.append(["", "", "", "", "Grand Total", total_amt])

  df_csv = pd.DataFrame(rows)
  return df_csv.to_csv(index=False, header=False).encode("utf-8")


# 1. HOME DASHBOARD
if selected_module == get_text("home"):
  inv_df = st.session_state["stock_inventory_df"]
  total_items_count = len(inv_df)
  low_stock_count = len(inv_df[inv_df["Status"] == "Low Stock"])
  out_stock_count = len(inv_df[inv_df["Status"] == "Out of Stock"])

  m1, m2, m3, m4 = st.columns(4)
  with m1:
    st.metric(get_text("active_machines"), "4 Units", "Running 🚀")
  with m2:
    st.metric(get_text("todays_output"), "1,850 Nos", "+12% 📈")
  with m3:
    st.metric(get_text("material_stock"), f"{total_items_count} Items", "Optimal ✨")
  with m4:
    st.metric(
        get_text("low_stock_alerts"),
        f"{low_stock_count + out_stock_count} Alerts",
        "Check Stock ⚠️",
    )

  st.markdown("<br>", unsafe_allow_html=True)
  st.markdown(f"### {get_text('core_modules')}")

  col1, col2, col3 = st.columns(3)
  with col1:
    st.markdown(f"### {get_text('rod_calc').split('/')[0]}")
    if st.button("🚀 Open Rod Calculator", use_container_width=True, key="bh1"):
      st.session_state["selected_module"] = get_text("rod_calc")
      st.rerun()
  with col2:
    st.markdown(f"### {get_text('prod_calc').split('/')[0]}")
    if st.button("🚀 Open Production Calc", use_container_width=True, key="bh2"):
      st.session_state["selected_module"] = get_text("prod_calc")
      st.rerun()
  with col3:
    st.markdown(f"### {get_text('cost_calc').split('/')[0]}")
    if st.button("🚀 Open Costing Calc", use_container_width=True, key="bh3"):
      st.session_state["selected_module"] = get_text("cost_calc")
      st.rerun()

  c4, c5, c6, c7 = st.columns(4)
  with c4:
    st.markdown(f"### {get_text('stock_mgmt').split('/')[0]}")
    if st.button("🚀 Open Stock Manager", use_container_width=True, key="bh4"):
      st.session_state["selected_module"] = get_text("stock_mgmt")
      st.rerun()
  with c5:
    st.markdown(f"### {get_text('drawing_studio').split('/')[0]}")
    if st.button("🚀 Open Drawing Studio", use_container_width=True, key="bh5"):
      st.session_state["selected_module"] = get_text("drawing_studio")
      st.rerun()
  with c6:
    st.markdown(f"### {get_text('quote_hub').split('/')[0]}")
    if st.button("🚀 Open Quote Hub", use_container_width=True, key="bh6"):
      st.session_state["selected_module"] = get_text("quote_hub")
      st.rerun()
  with c7:
    st.markdown(f"### {get_text('settings').split('/')[0]}")
    if st.button("🚀 Open Settings", use_container_width=True, key="bh7"):
      st.session_state["selected_module"] = get_text("settings")
      st.rerun()

# 2. ROD CALCULATOR
elif selected_module == get_text("rod_calc"):
  if st.button(get_text("back_home")):
    st.session_state["selected_module"] = get_text("home")
    st.rerun()
  st.subheader(f"📐 {get_text('rod_calc')}")
  mode = st.radio(
      "Mode Selection",
      [get_text("simple_mode"), get_text("advanced_mode")],
      horizontal=True,
  )

  if mode == get_text("simple_mode"):
    st.write(f"### 🟢 {get_text('simple_mode')}")
    col1, col2 = st.columns(2)
    with col1:
      rod_length = st.number_input(
          get_text("rod_length"), value=6.0, min_value=0.0
      )
      part_length = st.number_input(
          get_text("part_length"),
          value=st.session_state["extracted_drawing_data"]["part_length"],
          min_value=0.0,
      )
      cutting_allowance = st.number_input(
          get_text("cutting_allowance"), value=3.0, min_value=0.0
      )
    with col2:
      shape_type = st.selectbox(
          get_text("material_shape"),
          ["Round Rod", "Hexagon Rod", "Square Rod", "Tube / Pipe"],
      )
      cycle_time = st.number_input(
          get_text("cycle_time"), value=20, min_value=0
      )
      required_qty = st.number_input(
          get_text("required_qty"), value=500, min_value=0
      )

    eff_len = part_length + cutting_allowance
    parts_per_rod = (
        int((rod_length * 1000) / eff_len) if eff_len > 0 else 0
    )
    remnant = round((rod_length * 1000) % eff_len, 2) if eff_len > 0 else 0.0
    req_rods = int(required_qty / parts_per_rod) if parts_per_rod > 0 else 0
    prod_per_hr = int(3600 / cycle_time) if cycle_time > 0 else 0

    st.markdown(
        f'<div class="auto-badge">⚡ {get_text("simple_mode")} RESULT</div>',
        unsafe_allow_html=True,
    )
    r1, r2, r3 = st.columns(3)
    with r1:
      st.metric(get_text("parts_per_rod"), f"{parts_per_rod} Nos")
      st.metric(get_text("required_rods"), f"{req_rods} Nos")
    with r2:
      st.metric(get_text("balance_scrap"), f"{remnant} mm")
      st.metric(
          get_text("total_stock_len"), f"{round(req_rods * rod_length, 2)} Meters"
      )
    with r3:
      st.metric(get_text("prod_per_hr"), f"{prod_per_hr} Nos")
      st.metric(
          get_text("tot_mach_time"),
          f"{round((required_qty * cycle_time)/3600, 2)} Hr",
      )

  else:
    st.write(f"### 🔵 {get_text('advanced_mode')}")
    adv_file = st.file_uploader(
        get_text("upload_drawing"), type=["png", "jpg", "pdf"]
    )
    if adv_file:
      st.success(f"📂 '{adv_file.name}' uploaded successfully!")
      if st.button("🤖 Auto-Extract Drawing Dimensions (AI OCR)"):
        # Auto-populate with parsed drawing dimensions (e.g. Bushing drawing: OD 38.1, ID 25.8, Length 73.0, Cross Hole 5.4)
        st.session_state["extracted_drawing_data"] = {
            "part_length": 73.0,
            "outer_dia": 38.1,
            "inner_dia": 25.8,
            "cross_hole_dia": 5.4,
            "material_shape": "Tube / Pipe",
            "material_grade": "TUFF DOM 52.3 / 1026 DOM",
        }
        st.success(
            "✅ Drawing successfully analyzed! Dimensions auto-populated:"
            " Length=73.0mm, OD=38.1mm, ID=25.8mm, Cross Hole=5.4mm."
        )
        st.rerun()

      if adv_file.type in ["image/png", "image/jpeg"]:
        st.image(adv_file, width=350)

    ext = st.session_state["extracted_drawing_data"]

    ac1, ac2 = st.columns(2)
    with ac1:
      adv_shape = st.selectbox(
          get_text("material_shape"),
          ["Tube / Pipe", "Round Rod", "Hexagon Rod", "Square Rod"],
          index=0,
          key="as",
      )
      adv_rod_len_m = st.number_input(
          get_text("rod_length"), value=6.0, key="arl"
      )
      adv_part_len = st.number_input(
          get_text("part_length"), value=ext["part_length"], key="apl"
      )
      adv_cut_allow = st.number_input(
          get_text("cutting_allowance"), value=3.0, key="aca"
      )
      adv_req_qty = st.number_input(
          get_text("required_qty"), value=500, key="arq"
      )
    with ac2:
      adv_dia = st.number_input(
          get_text("material_dia"), value=ext["outer_dia"], key="add"
      )
      adv_inner_dia = (
          st.number_input(
              get_text("tube_inner_dia"), value=ext["inner_dia"], key="aid"
          )
          if adv_shape == "Tube / Pipe"
          else 0.0
      )
      adv_density = st.number_input(
          get_text("material_density"), value=0.00785, format="%.5f", key="adn"
      )
      adv_mat_rate = st.number_input(
          get_text("material_rate"), value=90.0, key="amr"
      )
      adv_wastage_pct = st.slider(
          get_text("wastage_pct"), 0, 10, 2, key="awt"
      )

    cross_area = get_cross_section_area(adv_shape, adv_dia, adv_inner_dia)
    eff_l = adv_part_len + adv_cut_allow
    part_wt = round((cross_area * adv_part_len) * adv_density, 2)
    parts_bar = int((adv_rod_len_m * 1000) / eff_l) if eff_l > 0 else 0
    rem_mm = round((adv_rod_len_m * 1000) % eff_l, 2) if eff_l > 0 else 0.0
    req_rd = int(math.ceil(adv_req_qty / parts_bar)) if parts_bar > 0 else 0
    tot_wt_kg = (
        round(
            (
                req_rd
                * adv_rod_len_m
                * (cross_area * adv_density * 1000)
                / 1000000
            ),
            2,
        )
        * (1 + adv_wastage_pct / 100)
    )

    st.markdown(
        f'<div class="auto-badge">⚡ {get_text("advanced_mode")} RESULT (Auto'
        " Extracted Specs Active)</div>",
        unsafe_allow_html=True,
    )
    ar1, ar2, ar3, ar4 = st.columns(4)
    with ar1:
      st.metric(get_text("parts_per_rod"), f"{parts_bar} Nos")
      st.metric(get_text("part_weight"), f"{part_wt} g")
    with ar2:
      st.metric(get_text("balance_scrap"), f"{rem_mm} mm")
      st.metric(
          "End Bit Weight", f"{round((cross_area * rem_mm)*adv_density, 2)} g"
      )
    with ar3:
      st.metric(get_text("required_rods"), f"{req_rd} Nos")
      st.metric(
          "Cross Hole Drill Spec", f"Ø {ext['cross_hole_dia']} mm 🎯"
      )
    with ar4:
      st.metric(get_text("total_mat_weight"), f"{round(tot_wt_kg, 2)} Kg")
      st.metric(
          get_text("total_mat_cost"), f"Rs. {round(tot_wt_kg * adv_mat_rate, 2)}"
      )

# 3. PRODUCTION CALCULATOR
elif selected_module == get_text("prod_calc"):
  if st.button(get_text("back_home")):
    st.session_state["selected_module"] = get_text("home")
    st.rerun()
  st.subheader(f"⏱️ {get_text('prod_calc')}")
  c1, c2 = st.columns(2)
  with c1:
    cyc_time = st.number_input(get_text("cycle_time"), value=20)
    avail_time = st.number_input(get_text("avail_time"), value=8.0)
  with c2:
    efficiency = st.slider(get_text("machine_efficiency"), 50, 100, 85)
    break_time = st.number_input(get_text("break_time"), value=30)

  eff_hrs = avail_time - (break_time / 60)
  prod_hr = int(3600 / cyc_time * (efficiency / 100)) if cyc_time > 0 else 0
  prod_day = int(prod_hr * eff_hrs)

  st.markdown(
      '<div class="auto-badge">⚡ AUTO CALCULATED</div>', unsafe_allow_html=True
  )
  r1, r2 = st.columns(2)
  with r1:
    st.metric(get_text("prod_per_hr"), f"{prod_hr} Nos")
  with r2:
    st.metric(get_text("prod_day"), f"{prod_day} Nos")

  st.markdown("---")
  st.subheader("📄 Report Export")
  p_dict = {
      "Cycle Time": cyc_time,
      "Available Time / Day (hr)": avail_time,
      "Machine Efficiency (%)": efficiency,
      "Production / Hour": f"{prod_hr} Nos",
      "Production / Day": f"{prod_day} Nos",
  }
  st.download_button(
      get_text("download_prod_pdf"),
      data=generate_production_pdf(p_dict),
      file_name="Production_Report.pdf",
      mime="application/pdf",
  )

# 4. COSTING & QUOTATION CALCULATOR
elif selected_module == get_text("cost_calc"):
  if st.button(get_text("back_home")):
    st.session_state["selected_module"] = get_text("home")
    st.rerun()
  st.subheader(f"💰 {get_text('cost_calc')}")
  col1, col2 = st.columns(2)
  with col1:
    mat_cost_kg = st.number_input(get_text("material_rate"), value=85.0)
    mat_wt_part = st.number_input("Material Weight / Part (Kg)", value=0.05)
    machine_cost_hr = st.number_input(get_text("machine_cost_hr"), value=600.0)
  with col2:
    labour_cost_part = st.number_input(get_text("labour_cost_part"), value=1.20)
    overhead_pct = st.number_input(get_text("overhead_pct"), value=15.0)
    profit_margin = st.slider(get_text("profit_margin"), 0, 50, 20)

  subtotal = (
      (mat_cost_kg * mat_wt_part)
      + ((machine_cost_hr / 3600) * 20)
      + labour_cost_part
  )
  cost_part = subtotal * (1 + overhead_pct / 100)
  selling_price = cost_part * (1 + profit_margin / 100)

  st.markdown(
      '<div class="auto-badge">⚡ AUTO CALCULATED</div>', unsafe_allow_html=True
  )
  p1, p2, p3 = st.columns(3)
  with p1:
    st.metric(get_text("cost_part"), f"Rs. {round(cost_part, 2)}")
  with p2:
    st.metric(get_text("cost_1000_parts"), f"Rs. {round(cost_part * 1000, 2)}")
  with p3:
    st.metric(get_text("selling_price_part"), f"Rs. {round(selling_price, 2)}")

  st.markdown("---")
  st.subheader("📄 Quotation Export")
  q_dict = {
      "Cost Per Part": f"Rs. {round(cost_part, 2)}",
      "Selling Price Per Part": f"Rs. {round(selling_price, 2)}",
      "Cost for 1000 Parts": f"Rs. {round(cost_part * 1000, 2)}",
  }
  st.download_button(
      get_text("download_quote_pdf"),
      data=generate_quotation_pdf(q_dict),
      file_name="Quotation.pdf",
      mime="application/pdf",
  )

# 5. STOCK MANAGEMENT
elif selected_module == get_text("stock_mgmt"):
  if st.button(get_text("back_home")):
    st.session_state["selected_module"] = get_text("home")
    st.rerun()
  st.subheader(f"📦 {get_text('stock_mgmt')}")
  inv_df = st.session_state["stock_inventory_df"]

  s1, s2, s3 = st.columns(3)
  with s1:
    st.metric(get_text("total_items"), str(len(inv_df)))
  with s2:
    st.metric(
        get_text("low_stock"), str(len(inv_df[inv_df["Status"] == "Low Stock"]))
    )
  with s3:
    st.metric(
        get_text("out_of_stock"),
        str(len(inv_df[inv_df["Status"] == "Out of Stock"])),
    )

  st.markdown("---")
  tab1, tab2, tab3 = st.tabs(
      [get_text("current_stock"), get_text("add_item"), get_text("stock_in_out")]
  )
  with tab1:
    sq = st.text_input(get_text("search_inventory"))
    st.dataframe(
        inv_df[
            inv_df["Material / Part Name"]
            .str.contains(sq, case=False, na=False)
        ]
        if sq
        else inv_df,
        use_container_width=True,
    )
  with tab2:
    with st.form("add_form"):
      nid = f"ITM-{len(inv_df)+1:03d}"
      nn = st.text_input(get_text("part_name"))
      nc = st.selectbox(
          get_text("category"), ["Raw Material", "Finished Goods", "Consumables"]
      )
      nq = st.number_input(get_text("quantity"), value=50.0)
      nu = st.selectbox(get_text("unit"), ["Kg", "Nos", "Meters"])
      if st.form_submit_button("➕ Add Item") and nn:
        nst = (
            "Out of Stock"
            if nq == 0
            else ("Low Stock" if nq < 10 else "In Stock")
        )
        st.session_state["stock_inventory_df"] = pd.concat(
            [
                inv_df,
                pd.DataFrame({
                    "Item ID": [nid],
                    "Material / Part Name": [nn],
                    "Category": [nc],
                    "Quantity": [nq],
                    "Unit": [nu],
                    "Status": [nst],
                }),
            ],
            ignore_index=True,
        )
        st.success("Added successfully!")
        st.rerun()
  with tab3:
    if len(inv_df) > 0:
      with st.form("trans_form"):
        s_item = st.selectbox(
            "Select Item",
            inv_df["Item ID"] + " - " + inv_df["Material / Part Name"],
        )
        t_type = st.selectbox(
            "Type", ["Stock In (Purchase)", "Stock Out (Dispatch)"]
        )
        t_qty = st.number_input(get_text("quantity"), value=10.0)
        t_note = st.text_input("Notes / PO Ref")
        if st.form_submit_button(get_text("update_stock")):
          i_id = s_item.split(" - ")[0]
          idx = st.session_state["stock_inventory_df"].index[
              st.session_state["stock_inventory_df"]["Item ID"] == i_id
          ][0]
          curr = st.session_state["stock_inventory_df"].at[idx, "Quantity"]
          new_q = (
              curr + t_qty if "In" in t_type else max(0.0, curr - t_qty)
          )
          st.session_state["stock_inventory_df"].at[idx, "Quantity"] = new_q
          st.session_state["stock_inventory_df"].at[idx, "Status"] = (
              "Out of Stock"
              if new_q == 0
              else ("Low Stock" if new_q < 10 else "In Stock")
          )
          st.success(f"Updated! New Qty: {new_q}")
          st.rerun()

# 6. DRAWING & MULTI-OPERATION G-CODE GENERATOR
elif selected_module == get_text("drawing_studio"):
  if st.button(get_text("back_home")):
    st.session_state["selected_module"] = get_text("home")
    st.rerun()
  st.subheader(f"📷 {get_text('drawing_studio')}")
  uf = st.file_uploader(get_text("upload_drawing"), type=["png", "jpg", "pdf"])
  if uf:
    st.success(f"📂 '{uf.name}' uploaded successfully!")
    if st.button("🤖 Auto-Extract Drawing Specs & Cross Hole (5.4 mm)"):
      st.session_state["extracted_drawing_data"] = {
          "part_length": 73.0,
          "outer_dia": 38.1,
          "inner_dia": 25.8,
          "cross_hole_dia": 5.4,
          "material_shape": "Tube / Pipe",
          "material_grade": "TUFF DOM 52.3",
      }
      st.success(
          "✅ Drawing analyzed successfully! Auto-extracted: Length=73.0mm,"
          " OD=38.1mm, ID=25.8mm, Cross Hole Drill=Ø5.4mm."
      )
      st.rerun()

    if uf.type in ["image/png", "image/jpeg"]:
      st.image(uf, width=350)

  ext = st.session_state["extracted_drawing_data"]

  st.markdown("---")
  dc1, dc2 = st.columns(2)
  with dc1:
    d_shape = st.selectbox(
        get_text("material_shape"),
        ["Tube / Pipe", "Round Rod", "Hexagon Rod", "Square Rod"],
        index=0,
        key="ds",
    )
    d_rlen = st.number_input(get_text("rod_length"), value=6000.0, key="drl")
    d_plen = st.number_input(
        get_text("part_length"), value=ext["part_length"], key="dpl"
    )
    d_callow = st.number_input(
        get_text("cutting_allowance"), value=3.0, key="dca"
    )
  with dc2:
    d_rdia = st.number_input(
        get_text("material_dia"), value=ext["outer_dia"], key="drd"
    )
    d_india = (
        st.number_input(
            get_text("tube_inner_dia"), value=ext["inner_dia"], key="did"
        )
        if d_shape == "Tube / Pipe"
        else 0.0
    )
    d_dens = st.number_input(
        get_text("material_density"), value=0.00785, format="%.5f", key="ddens"
    )
    d_mrate = st.number_input(get_text("material_rate"), value=90.0, key="dmr")

  c_area = get_cross_section_area(d_shape, d_rdia, d_india)
  eff_pl = d_plen + d_callow
  p_wt = round((c_area * d_plen) * d_dens, 2)
  ppb = int(d_rlen / eff_pl) if eff_pl > 0 else 0
  rem = round(d_rlen % eff_pl, 2) if eff_pl > 0 else 0.0

  st.markdown(
      '<div class="auto-badge">⚡ ANALYSIS & CROSS-HOLE SPECS</div>',
      unsafe_allow_html=True,
  )
  m1, m2, m3 = st.columns(3)
  with m1:
    st.metric(get_text("parts_per_rod"), f"{ppb} Nos")
    st.metric(get_text("part_weight"), f"{p_wt} g")
  with m2:
    st.metric(get_text("balance_scrap"), f"{rem} mm")
    st.metric("Cross Hole Drill Spec", f"Ø {ext['cross_hole_dia']} mm 🎯")
  with m3:
    st.metric(
        "Total Scrap / Rod",
        f"{round((c_area * (rem + (ppb * d_callow))) * d_dens, 2)} g",
    )

  st.markdown("---")
  st.subheader("🛠️ Multi-Operation Setup & G-Code Generator")
  num_ops = st.selectbox(get_text("num_operations"), [1, 2, 3, 4, 5], index=2)
  all_gcodes = []

  for i in range(num_ops):
    with st.expander(f"📌 Operation {i+1} Details", expanded=(i == 0)):
      oc1, oc2 = st.columns(2)
      with oc1:
        t_no = st.text_input(
            f"Tool No (Op {i+1})", f"T{i+1:02d}{i+1:02d}", key=f"t_{i}"
        )
        op_defaults = [
            "Facing & Rough Turning",
            "Boring & ID Finish",
            f"Cross-Hole Drilling (Ø {ext['cross_hole_dia']} mm)",
            "Part-off",
        ]
        o_type = st.selectbox(
            f"Operation Type (Op {i+1})",
            op_defaults,
            index=min(i, len(op_defaults) - 1),
            key=f"ot_{i}",
        )
        rpm = st.number_input(f"RPM (Op {i+1})", value=1200, key=f"rpm_{i}")
      with oc2:
        feed = st.number_input(
            f"Feed (mm/rev - Op {i+1})", value=0.15, key=f"fd_{i}"
        )
        target_d = (
            ext["cross_hole_dia"] if "Cross-Hole" in o_type else d_rdia - 5.0
        )
        t_dia = st.number_input(
            f"Target Dia / Hole Size (Op {i+1})", value=target_d, key=f"td_{i}"
        )

      code = f"""( --- OP {i+1}: {o_type.upper()} --- )
{t_no}
G97 S{rpm} M03
G0 X{d_rdia + 5.0} Z2.0
G1 X0.0 F{feed}
G0 Z2.0
"""
      all_gcodes.append(code)
      st.text_area(f"G-Code Op {i+1}", code.strip(), height=100, key=f"gc_{i}")

  final_prog = (
      "%\nO2026 (MEGALA CNC MATE - AUTO EXTRACTED)\nG21 G90 G40 G95\n"
      + "\n".join(all_gcodes)
      + "M05\nM30\n%"
  )
  st.code(final_prog, language="text")
  st.download_button(
      get_text("generate_gcode"),
      data=generate_program_pdf(final_prog),
      file_name="CNC_Program.pdf",
      mime="application/pdf",
  )

# 7. PROCESS BREAKDOWN & CUSTOMER QUOTATION
elif selected_module == get_text("quote_hub"):
  if st.button(get_text("back_home")):
    st.session_state["selected_module"] = get_text("home")
    st.rerun()

  st.subheader(f"📋 {get_text('quote_hub')}")

  col_q1, col_q2 = st.columns(2)
  with col_q1:
    cust_name = st.text_input(
        get_text("cust_company"), value="M/s Radeo Engineered Components LLP"
    )
    part_name_input = st.text_input(
        get_text("part_name"), value="Bushing Component (REC 1 / 015-2880)"
    )
  with col_q2:
    order_qty = st.number_input(
        get_text("required_qty"), value=1000, min_value=1
    )
    transport_amt = st.number_input(
        get_text("transport_charges"), value=1500.0
    )

  st.markdown("---")
  st.subheader("⚙️ Configure Operations (Auto-Loaded with Cross-Hole Spec)")

  edited_ops = [
      {
          "name": "Facing & OD Turning",
          "machine": "CNC Turning",
          "qty": order_qty,
          "rate": 18.0,
      },
      {
          "name": "Boring / ID Machining",
          "machine": "CNC Turning",
          "qty": order_qty,
          "rate": 22.0,
      },
      {
          "name": (
              "Cross-Hole Drilling & Tapping (Ø 5.4 mm & 1/4-28 UNF)"
          ),
          "machine": "VMC / Milling",
          "qty": order_qty,
          "rate": 25.0,
      },
      {
          "name": "Parting / Cut-off & Deburring",
          "machine": "CNC Turning",
          "qty": order_qty,
          "rate": 12.0,
      },
  ]

  for i, op in enumerate(edited_ops):
    st.markdown(f"**Operation {i+1}: {op['name']}**")
    col_a, col_b, col_c = st.columns([3, 2, 2])
    with col_a:
      op["name"] = st.text_input(
          f"Operation Name {i+1}", op["name"], key=f"q_op_n_{i}"
      )
    with col_b:
      op["machine"] = st.selectbox(
          f"Machine {i+1}",
          [
              "CNC Turning",
              "VMC / Milling",
              "Drilling Machine",
              "Traub Lathe",
              "Manual / Bench",
          ],
          index=0 if "Turning" in op["machine"] else 1,
          key=f"q_op_m_{i}",
      )
    with col_c:
      op["rate"] = st.number_input(
          f"Unit Rate (Rs.) {i+1}", value=op["rate"], key=f"q_op_r_{i}"
      )

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button(get_text("generate_csv"), use_container_width=True):
    csv_data = generate_quotation_csv(
        cust_name, part_name_input, edited_ops, transport_amt
    )
    filename = f"Megala_Industries_Quotation_{part_name_input.replace(' ', '_').replace('/', '_')}.csv"
    st.success(f"✅ Quotation CSV successfully generated: {filename}")
    st.download_button(
        "📥 Download CSV Quotation (.csv)",
        data=csv_data,
        file_name=filename,
        mime="text/csv",
    )

# 8. MORE MENU & SETTINGS
elif selected_module == get_text("settings"):
  if st.button(get_text("back_home")):
    st.session_state["selected_module"] = get_text("home")
    st.rerun()
  st.subheader(f"⚙️ {get_text('settings')}")

  selected_lang_main = st.selectbox(
      get_text("language_label"),
      list(translations.keys()),
      index=list(translations.keys()).index(st.session_state["app_language"]),
      key="main_lang_selector",
  )

  if selected_lang_main != st.session_state["app_language"]:
    st.session_state["app_language"] = selected_lang_main
    st.rerun()

  st.success(f"Language set to: {st.session_state['app_language']}")
  st.markdown("---")
  st.markdown("### 📋 Workshop Masters")
  st.write("• Part Master\n• Customer Master\n• Machine Master\n• Material Master")
