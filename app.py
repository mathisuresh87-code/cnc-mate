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
        "profit_margin":
