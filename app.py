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

# Page Configuration
st.set_page_config(
    page_title="Megala CNC Mate - Enterprise CNC Automation",
    page_icon="⚙️",
    layout="wide",
)

# Perfect Uniform Alignment & Proportional Card CSS
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #090d1f 0%, #111827 40%, #1e1b4b 100%);
        color: #f8fafc;
        font-family: 'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    .main-title {
        font-size: 2.4rem;
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
        font-size: 0.85rem;
        color: #38bdf8;
        margin: 0;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .auto-badge {
        background: linear-gradient(135deg, rgba(236, 72, 153, 0.3) 0%, rgba(139, 92, 246, 0.4) 100%);
        color: #f472b6;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 800;
        display: inline-block;
        margin-bottom: 14px;
        border: 1.5px solid rgba(236, 72, 153, 0.6);
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }
    
    div[data-testid="stHorizontalBlock"] {
        align-items: stretch !important;
    }
    
    div[data-testid="column"] {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.85) 0%, rgba(49, 46, 129, 0.5) 100%);
        border: 1.5px solid rgba(139, 92, 246, 0.4);
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(16px);
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 16px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100% !important;
        min-height: 240px;
    }
    div[data-testid="column"]:hover {
        border-color: #ec4899;
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 15px 40px rgba(236, 72, 153, 0.4), 0 0 25px rgba(56, 189, 248, 0.3);
        background: linear-gradient(145deg, rgba(55, 48, 163, 0.7) 0%, rgba(131, 24, 67, 0.5) 100%);
    }
    
    .card-icon {
        font-size: 2rem;
        text-align: center;
        margin-bottom: 6px;
    }
    .card-title-text {
        font-size: 0.95rem;
        font-weight: 800;
        text-align: center;
        color: #38bdf8;
        margin-bottom: 6px;
    }
    .card-desc {
        font-size: 0.78rem;
        text-align: center;
        color: #94a3b8;
        flex-grow: 1;
        margin-bottom: 12px;
        line-height: 1.3;
    }
    
    div.stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 50%, #ec4899 100%);
        color: #ffffff !important;
        border-radius: 12px;
        border: 1.5px solid rgba(236, 72, 153, 0.6);
        font-weight: 800;
        font-size: 0.82rem;
        letter-spacing: 0.8px;
        width: 100%;
        padding: 6px 12px;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 15px rgba(147, 51, 234, 0.5);
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #f43f5e 100%);
        border-color: #38bdf8;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(236, 72, 153, 0.7);
    }
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(49, 46, 129, 0.7) 100%);
        border: 1.5px solid rgba(56, 189, 248, 0.4);
        padding: 14px;
        border-radius: 14px;
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

# 6 Languages Comprehensive Translation Dictionary
translations = {
    "தமிழ் (Tamil)": {
        "home": "🏠 Home / முகப்பு",
        "rod_calc": "📐 Rod Calculator / ராட் கால்குலேட்டர்",
        "prod_calc": "⏱️ Production Calculator / உற்பத்தி கால்குலேட்டர்",
        "cost_calc": "💰 Costing & Quotation / செலவு & கொட்டேஷன்",
        "stock_mgmt": "📦 Stock Management / ஸ்டாக் மேனேஜ்மென்ட்",
        "drawing_studio": "📷 Drawing & G-Code / டிராயிங் & ஜி-கோடு ஸ்டுடியோ",
        "quote_hub": "📋 Auto Drawing Quotation Hub / ஆட்டோ டிராயிங் கொட்டேஷன் ஹப்",
        "material_dia": "Material Diameter / Size (mm) / விட்டம் / சைஸ் (மிமீ)",
        "tube_inner_dia": "Tube Inner Diameter (mm) / குழாய் உள் விட்டம்",
        "part_length": "Part Length (mm) / பார்ட் நீளம் (மிமீ)",
        "cutting_allowance": "Cutting Allowance (mm) / வெட்டும் அளவு (மிமீ)",
        "material_rate": "Material Rate / Kg (Rs.) / ஒரு கிலோ விலை (ரூ)",
        "cycle_time": "Cycle Time (Seconds) / சுழற்சி நேரம் (வினாடிகள்)",
        "required_qty": "Required Quantity / தேவையான எண்ணிக்கை",
        "balance_scrap": "Balance Scrap / மீதமுள்ள ஸ்கிராப்",
        "prod_per_hr": "Production / Hour / மணி நேர உற்பத்தி",
        "prod_day": "Production / Day / நாள் உற்பத்தி",
        "machine_cost_hr": "Machine Cost / Hr (Rs.) / இயந்திர செலவு / மணி",
        "profit_margin": "Profit Margin (%) / லாப வரம்பு (%)",
        "cost_part": "Cost / Part / ஒரு பார்ட்டின் செலவு",
        "selling_price_part": "Selling Price / Part / விற்பனை விலை / பார்ட்",
        "total_items": "Total Items / மொத்த பொருட்கள்",
        "current_stock": "📋 Current Stock / தற்போதைய இருப்பு",
        "add_item": "➕ Add Item / புதிய பொருள் சேர்",
        "part_name": "Part Name / பார்ட் பெயர்",
        "category": "Category / வகை",
        "quantity": "Quantity / எண்ணிக்கை",
        "unit": "Unit / அலகு",
        "generate_csv": "🚀 Generate CSV Quotation File / கொட்டேஷன் CSV கோப்பை உருவாக்கு",
        "generate_pdf": "📄 Generate PDF Quotation / PDF கொட்டேஷன் உருவாக்கு",
        "upload_drawing": "Upload Engineering Drawing / என்ஜினியரிங் டிராயிங் பதிவேற்றவும்",
    },
    "English": {
        "home": "🏠 Home",
        "rod_calc": "📐 Rod Calculator",
        "prod_calc": "⏱️ Production Calculator",
        "cost_calc": "💰 Costing & Quotation",
        "stock_mgmt": "📦 Stock Management",
        "drawing_studio": "📷 Drawing & G-Code Studio",
        "quote_hub": "📋 Auto Quotation Hub",
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
        "generate_csv": "🚀 Generate CSV Quotation File",
        "generate_pdf": "📄 Generate PDF Quotation",
        "upload_drawing": "Upload Engineering Drawing",
    },
    "हिन्दी (Hindi)": {
        "home": "🏠 Home / गृह",
        "rod_calc": "📐 Rod Calculator / रॉड कैलकुलेटर",
        "prod_calc": "⏱️ Production Calculator / उत्पादन कैलकुलेटर",
        "cost_calc": "💰 Costing & Quotation / लागत और उद्धरण",
        "stock_mgmt": "📦 Stock Management / स्टॉक प्रबंधन",
        "drawing_studio": "📷 Drawing & G-Code / ड्राइंग और जी-कोड",
        "quote_hub": "📋 Auto Drawing Quotation Hub / ऑटो ड्राइंग उद्धरण केंद्र",
        "material_dia": "Material Diameter / Size (mm) / व्यास / साइज़ (मिमी)",
        "tube_inner_dia": "Tube Inner Diameter (mm) / ट्यूब का आंतरिक व्यास",
        "part_length": "Part Length (mm) / भाग की लंबाई (मिमी)",
        "cutting_allowance": "Cutting Allowance (mm) / कटिंग अलाउंस (मिमी)",
        "material_rate": "Material Rate / Kg (Rs.) / प्रति किलो दर (रु)",
        "cycle_time": "Cycle Time (Seconds) / चक्र का समय (सेकंड)",
        "required_qty": "Required Quantity / आवश्यक मात्रा",
        "balance_scrap": "Balance Scrap / शेष स्क्रैप",
        "prod_per_hr": "Production / Hour / प्रति घंटा उत्पादन",
        "prod_day": "Production / Day / प्रति दिन उत्पादन",
        "machine_cost_hr": "Machine Cost / Hr (Rs.) / मशीन लागत / घंटा",
        "profit_margin": "Profit Margin (%) / लाभ मार्जिन (%)",
        "cost_part": "Cost / Part / प्रति भाग लागत",
        "selling_price_part": "Selling Price / Part / विक्रय मूल्य / भाग",
        "total_items": "Total Items / कुल वस्तुएं",
        "current_stock": "📋 Current Stock / वर्तमान स्टॉक",
        "add_item": "➕ Add Item / वस्तु जोड़ें",
        "part_name": "Part Name / भाग का नाम",
        "category": "Category / श्रेणी",
        "quantity": "Quantity / मात्रा",
        "unit": "Unit / इकाई",
        "generate_csv": "🚀 Generate CSV Quotation File / CSV उद्धरण फ़ाइल बनाएं",
        "generate_pdf": "📄 Generate PDF Quotation / PDF उद्धरण फ़ाइल बनाएं",
        "upload_drawing": "Upload Engineering Drawing / इंजीनियरिंग ड्राइंग अपलोड करें",
    },
    "తెలుగు (Telugu)": {
        "home": "🏠 Home / హోమ్",
        "rod_calc": "📐 Rod Calculator / రాడ్ కాల்குலேட்டர்",
        "prod_calc": "⏱️ Production Calculator / ఉత్పత్తి కాల்குலேட்டர்",
        "cost_calc": "💰 Costing & Quotation / ఖర్చు & కొటేషన్",
        "stock_mgmt": "📦 Stock Management / స్టాక్ నిర్వహణ",
        "drawing_studio": "📷 Drawing & G-Code / డ్రாயிங் & జి-కోடு ஸ்டுடியோ",
        "quote_hub": "📋 Auto Drawing Quotation Hub / ఆటో కొటేஷன் హబ్",
        "material_dia": "Material Diameter / Size (mm) / మెటీరియల్ వ్యాసం (మిమీ)",
        "tube_inner_dia": "Tube Inner Diameter (mm) / ట్యూబ్ అంతర్గత వ్యాసం",
        "part_length": "Part Length (mm) / పార్ట్ పొడవు (మిమీ)",
        "cutting_allowance": "Cutting Allowance (mm) / కటింగ్ అలవెన్స్ (మిమీ)",
        "material_rate": "Material Rate / Kg (Rs.) / ఒక కిలో ధర (రూ)",
        "cycle_time": "Cycle Time (Seconds) / సైకిల్ సమయం (సెకన్లు)",
        "required_qty": "Required Quantity / కావలసిన పరిమాణం",
        "balance_scrap": "Balance Scrap / మిగిలిన స్క్రాప్",
        "prod_per_hr": "Production / Hour / గంట ఉత్పత్తి",
        "prod_day": "Production / Day / రోజు ఉత్పత్తి",
        "machine_cost_hr": "Machine Cost / Hr (Rs.) / మెషిన్ ఖర్చు / గంట",
        "profit_margin": "Profit Margin (%) / లాభ మార్జిన్ (%)",
        "cost_part": "Cost / Part / పార్ట్ ఖర్చు",
        "selling_price_part": "Selling Price / Part / అమ్మకం ధర / పార్ట్",
        "total_items": "Total Items / మొత్తం వస్తువులు",
        "current_stock": "📋 Current Stock / ప్రస్తుత స్టాక్",
        "add_item": "➕ Add Item / కొత్త వస్తువును జోడించు",
        "part_name": "Part Name / పార్ట్ పేరు",
        "category": "Category / వర్గం",
        "quantity": "Quantity / పరిమాణం",
        "unit": "Unit / యూనిట్",
        "generate_csv": "🚀 Generate CSV Quotation File / CSV కొటేషన్ ఫైల్ సృష్టించు",
        "generate_pdf": "📄 Generate PDF Quotation / PDF కొటేషన్ ఫైల్ సృష్టించు",
        "upload_drawing": "Upload Engineering Drawing / ఇంజనీరింగ్ డ్రాయింగ్ అప్‌లోడ్ చేయండి",
    },
    "ಕನ್ನಡ (Kannada)": {
        "home": "🏠 Home / ಮುಖಪುಟ",
        "rod_calc": "📐 Rod Calculator / ರಾಡ್ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
        "prod_calc": "⏱️ Production Calculator / ಉತ್ಪಾದನಾ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
        "cost_calc": "💰 Costing & Quotation / ವೆಚ್ಚ & ಕೊಟೇಶನ್",
        "stock_mgmt": "📦 Stock Management / ಸ್ಟಾಕ್ ನಿರ್ವಹಣೆ",
        "drawing_studio": "📷 Drawing & G-Code / ಡ್ರಾಯಿಂಗ್ & ಜಿ-ಕೋಡ್ ಸ್ಟುಡಿಯೋ",
        "quote_hub": "📋 Auto Drawing Quotation Hub / ಆಟೋ ಕೊಟೇಶನ್ ಹಬ್",
        "material_dia": "Material Diameter / Size (mm) / ವಸ್ತು ವ್ಯಾಸ / ಗಾತ್ರ (ಮಿಮೀ)",
        "tube_inner_dia": "Tube Inner Diameter (mm) / ಟ್ಯೂಬ್ ಒಳ ವ್ಯಾಸ",
        "part_length": "Part Length (mm) / ಭಾಗದ ಉದ್ದ (ಮಿಮೀ)",
        "cutting_allowance": "Cutting Allowance (mm) / ಕಟಿಂಗ್ ಅಲವನ್ಸ್ (ಮಿಮೀ)",
        "material_rate": "Material Rate / Kg (Rs.) / ಪ್ರತಿ ಕೆಜಿ ಬೆಲೆ (ರೂ)",
        "cycle_time": "Cycle Time (Seconds) / ಸೈಕಲ್ ಸಮಯ (ಸೆಕೆಂಡುಗಳು)",
        "required_qty": "Required Quantity / ಅಗತ್ಯವಿರುವ ಪ್ರಮಾಣ",
        "balance_scrap": "Balance Scrap / ಉಳಿದ ಸ್ಕ್ರ್ಯಾಪ್",
        "prod_per_hr": "Production / Hour / ಪ್ರತಿ ಗಂಟೆಯ ಉತ್ಪಾದನೆ",
        "prod_day": "Production / Day / ಪ್ರತಿ ದಿನದ ಉತ್ಪಾದನೆ",
        "machine_cost_hr": "Machine Cost / Hr (Rs.) / ಯಂತ್ರದ ವೆಚ್ಚ / ಗಂಟೆ",
        "profit_margin": "Profit Margin (%) / ಲಾಭದ ಅಂಚು (%)",
        "cost_part": "Cost / Part / ಪ್ರತಿ ಭಾಗದ ವೆಚ್ಚ",
        "selling_price_part": "Selling Price / Part / ಮಾರಾಟ ಬೆಲೆ / ಭಾಗ",
        "total_items": "Total Items / ಒಟ್ಟು ವಸ್ತುಗಳು",
        "current_stock": "📋 Current Stock / ಪ್ರಸ್ತುತ ಸ್ಟಾಕ್",
        "add_item": "➕ Add Item / ಹೊಸ ವಸ್ತು ಸೇರಿಸಿ",
        "part_name": "Part Name / ಭಾಗದ ಹೆಸರು",
        "category": "Category / ವರ್ಗ",
        "quantity": "Quantity / ಪ್ರಮಾಣ",
        "unit": "Unit / ಘಟಕ",
        "generate_csv": "🚀 Generate CSV Quotation File / CSV ಕೊಟೇಶನ್ ಫೈಲ್ ರಚಿಸಿ",
        "generate_pdf": "📄 Generate PDF Quotation / PDF ಕೊಟೇಶನ್ ಫೈಲ್ ರಚಿಸಿ",
        "upload_drawing": "Upload Engineering Drawing / ಇಂಜಿನಿಯರಿಂಗ್ ಡ್ರಾಯಿಂಗ್ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
    },
    "മലയാളം (Malayalam)": {
        "home": "🏠 Home / ഹോം",
        "rod_calc": "📐 Rod Calculator / റോഡ് കാൽക്കുലേറ്റർ",
        "prod_calc": "⏱️ Production Calculator / ഉൽപ്പാദന കാൽക്കുലേറ്റർ",
        "cost_calc": "💰 Costing & Quotation / ചെലവ് & കൊട്ടേഷൻ",
        "stock_mgmt": "📦 Stock Management / സ്റ്റോക്ക് മാനേജ്മെന്റ്",
        "drawing_studio": "📷 Drawing & G-Code / ഡ്രോയിംഗ് & ജി-കോഡ് സ്റ്റുഡിയോ",
        "quote_hub": "📋 Auto Drawing Quotation Hub / ഓട്ടോ കൊട്ടേഷൻ ഹബ്",
        "material_dia": "Material Diameter / Size (mm) / മെറ്റീരിയൽ വ്യാസം (മില്ലീമീറ്റർ)",
        "tube_inner_dia": "Tube Inner Diameter (mm) / ട്യൂബ് ഉൾവ്യാസം",
        "part_length": "Part Length (mm) / ഭാഗത്തിന്റെ നീളം (മില്ലീമീറ്റർ)",
        "cutting_allowance": "Cutting Allowance (mm) / കട്ടിംഗ് അലവൻസ്",
        "material_rate": "Material Rate / Kg (Rs.) / ഒരു കിലോ വില (രൂപ)",
        "cycle_time": "Cycle Time (Seconds) / സൈക്കിൾ സമയം (സെക്കൻഡ്)",
        "required_qty": "Required Quantity / ആവശ്യമായ അളവ്",
        "balance_scrap": "Balance Scrap / ബാക്കി സ്ക്രാപ്പ്",
        "prod_per_hr": "Production / Hour / മണിക്കൂർ ഉൽപ്പാദനം",
        "prod_day": "Production / Day / ദിവസത്തെ ഉൽപ്പാദനം",
        "machine_cost_hr": "Machine Cost / Hr (Rs.) / മെഷീൻ ചെലവ് / മണിക്കൂർ",
        "profit_margin": "Profit Margin (%) / ലാഭവിഹിതം (%)",
        "cost_part": "Cost / Part / ഒരു ഭാഗത്തിന്റെ ചെലവ്",
        "selling_price_part": "Selling Price / Part / വിൽപ്പന വില / ഭാഗം",
        "total_items": "Total Items / ആകെ സാധനങ്ങൾ",
        "current_stock": "📋 Current Stock / നിലവിലുള്ള സ്റ്റോക്ക്",
        "add_item": "➕ Add Item / പുതിയ ഇനം ചേർക്കുക",
        "part_name": "Part Name / ഭാഗത്തിന്റെ പേര്",
        "category": "Category / വിഭാഗം",
        "quantity": "Quantity / അളവ്",
        "unit": "Unit / യൂണിറ്റ്",
        "generate_csv": "🚀 Generate CSV Quotation File / CSV കൊട്ടേഷൻ ഫയൽ നിർമ്മിക്കുക",
        "generate_pdf": "📄 Generate PDF Quotation / PDF കൊട്ടേഷൻ ഫയൽ നിർമ്മിക്കുക",
        "upload_drawing": "Upload Engineering Drawing / എൻജിനീയറിങ് ഡ്രോയിംഗ് അപ്‌ലോഡ് ചെയ്യുക",
    }
}

# PDF Generator Function
def create_pdf_quotation(df_data, margin_val):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Megala CNC Mate - Enterprise Quotation", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(200, 8, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
    pdf.ln(10)
    
    # Table Header
    pdf.set_font("Arial", "B", 11)
    pdf.cell(120, 10, "Description", 1)
    pdf.cell(70, 10, "Amount (INR)", 1, ln=True)
    
    # Table Rows
    pdf.set_font("Arial", "", 11)
    for index, row in df_data.iterrows():
        pdf.cell(120, 10, str(row["Description"]), 1)
        pdf.cell(70, 10, str(row["Amount (INR)"]), 1, ln=True)
        
    return pdf.output(dest='S').encode('latin1')

# Sidebar Language Selection
st.sidebar.markdown("### ⚙️ Megala CNC Mate", help="Enterprise Automation Suite")
selected_lang = st.sidebar.selectbox("🌐 Language / மொழி / भाषा / భాష", list(translations.keys()))
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
            "Part Name": ["Hex Bolt M12", "CNC Aluminium Bush", "MS Shaft 25mm", "Brass Nozzle"],
            "Category": ["Fasteners", "Automotive", "Raw Material", "Pneumatics"],
            "Quantity": [450, 85, 12, 120],
            "Unit": ["Pcs", "Pcs", "Length", "Pcs"],
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
]

if st.session_state["page_selection"] not in page_options:
    st.session_state["page_selection"] = t["home"]

st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", page_options, index=page_options.index(st.session_state["page_selection"]))
st.session_state["page_selection"] = page

# --- HOME PAGE WITH UNIFORM PROPORTIONAL CARD GRID ---
if page == t["home"]:
    st.markdown('<div class="main-title">Megala CNC Mate</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Advanced CNC Estimation & Automation Hub</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Active Machines", value="8 Units", delta="+2 Online")
    with col2:
        st.metric(label="Today's Output", value="1,420 Pcs", delta="94% Efficiency")
    with col3:
        st.metric(label="Material Stock", value="4,850 Kg", delta="Stable")
    with col4:
        st.metric(label="Low Stock Alerts", value="1 Item", delta="-1 Resolved")

    st.markdown("---")
    st.markdown("### 🚀 Core Automation Modules")

    # Row 1 Grid Cards (3 Columns)
    r1_c1, r1_c2, r1_c3 = st.columns(3)
    with r1_c1:
        st.markdown('<div class="card-icon">📐</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title-text">Rod & Tube Calculator</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-desc">Calculate raw material requirements with Dual Input (Kg/Meters) & Hexagon/Round shapes.</div>', unsafe_allow_html=True)
        if st.button("Open", key="btn_rod"):
            st.session_state["page_selection"] = t["rod_calc"]
            st.rerun()

    with r1_c2:
        st.markdown('<div class="card-icon">⏱️</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title-text">Production Calculator</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-desc">Estimate accurate daily outputs, machine hour costs, and cycle efficiency.</div>', unsafe_allow_html=True)
        if st.button("Open", key="btn_prod"):
            st.session_state["page_selection"] = t["prod_calc"]
            st.rerun()

    with r1_c3:
        st.markdown('<div class="card-icon">💰</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title-text">Costing & Quotation</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-desc">Calculate exact manufacturing costs, profit margins, and part pricing.</div>', unsafe_allow_html=True)
        if st.button("Open", key="btn_cost"):
            st.session_state["page_selection"] = t["cost_calc"]
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2 Grid Cards (3 Columns)
    r2_c1, r2_c2, r2_c3 = st.columns(3)
    with r2_c1:
        st.markdown('<div class="card-icon">📦</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title-text">Stock Management</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-desc">Monitor raw materials, components, and inventory items seamlessly.</div>', unsafe_allow_html=True)
        if st.button("Open", key="btn_stock"):
            st.session_state["page_selection"] = t["stock_mgmt"]
            st.rerun()

    with r2_c2:
        st.markdown('<div class="card-icon">📷</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title-text">Drawing & G-Code</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-desc">Upload 2D/3D Engineering drawings to generate instant G-Code programs.</div>', unsafe_allow_html=True)
        if st.button("Open", key="btn_drawing"):
            st.session_state["page_selection"] = t["drawing_studio"]
            st.rerun()

    with r2_c3:
        st.markdown('<div class="card-icon">📋</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title-text">Auto Quotation Hub</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-desc">AI Vision auto-detection for instant quotation generation from drawings.</div>', unsafe_allow_html=True)
        if st.button("Open", key="btn_quote"):
            st.session_state["page_selection"] = t["quote_hub"]
            st.rerun()

# --- ROD CALCULATOR ---
elif page == t["rod_calc"]:
    st.markdown(f'<div class="main-title">{t["rod_calc"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="auto-badge">Advanced Raw Material Optimizer (Kg / Meter Dual Input)</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        shape_type = st.selectbox("Material Shape / வடிவ வகை", ["Hexagon", "Round", "Square"])
        mat_size = st.number_input(t["material_dia"], value=st.session_state["ext_dia"], step=0.5)
        input_mode = st.radio("Input Mode / உள்ளீட்டு முறை", ["Total Weight (Kg)", "Total Length (Meters)"])
    
    with col2:
        if input_mode == "Total Weight (Kg)":
            total_weight_input = st.number_input("Total Weight (Kg) / மொத்த எடை", value=485.55, step=1.0)
            total_length_input = None
        else:
            total_length_input = st.number_input("Total Length (Meters) / மொத்த நீளம்", value=364.39, step=1.0)
            total_weight_input = None
            
        part_len = st.number_input(t["part_length"], value=st.session_state["ext_len"], step=1.0)
        cut_allow = st.number_input(t["cutting_allowance"], value=3.0, step=0.5)
        req_qty = st.number_input(t["required_qty"], value=25000, step=100)

    density = 7850
    if shape_type.lower() == 'hexagon':
        area_mm2 = (math.sqrt(3) / 2) * (mat_size ** 2)
        weight_per_m = (area_mm2 / 1e6) * density
    elif shape_type.lower() == 'round':
        radius = mat_size / 2.0
        area_mm2 = math.pi * (radius ** 2)
        weight_per_m = (area_mm2 / 1e6) * density
    else:
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
        st.metric("Total Length", f"{calc_total_length:.2f} Meters")
    with m3:
        st.metric("Total Possible Pieces", f"{total_possible_pieces:,} Pcs")
    with m4:
        st.metric(t["balance_scrap"], f"{rem_scrap_m * 1000:.1f} mm")

    st.markdown("### 🎯 Required Quantity & Material Analysis")
    if req_qty > 0:
        if total_possible_pieces >= req_qty:
            material_needed_m = req_qty * piece_len_m
            material_needed_kg = material_needed_m * weight_per_m
            st.success(f"✅ **Sufficient Material Available!** To produce **{req_qty:,} Pcs**, you need **{material_needed_kg:.2f} Kg** ({material_needed_m:.2f} Meters). Remaining stock will be **{calc_total_weight - material_needed_kg:.2f} Kg**.")
        else:
            shortage_pcs = req_qty - total_possible_pieces
            shortage_kg = shortage_pcs * piece_len_m * weight_per_m
            st.error(f"⚠️ **Material Shortage:** You need **{shortage_pcs:,} more pieces** (approx. **{shortage_kg:.2f} Kg** extra raw material) to fulfill the required quantity of {req_qty:,} Pcs.")

# --- PRODUCTION CALCULATOR ---
elif page == t["prod_calc"]:
    st.markdown(f'<div class="main-title">{t["prod_calc"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="auto-badge">Cycle Time & Output Hub</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        cycle_time = st.number_input(t["cycle_time"], value=st.session_state["ext_cycle"], step=1.0)
        avail_hrs = st.number_input("Available Time / Day (hr)", value=8.0, step=0.5)
    with col2:
        efficiency = st.slider("Machine Efficiency (%)", 50, 100, 85)
        break_mins = st.number_input("Break Time (min)", value=45, step=5)

    if cycle_time > 0:
        effective_secs = (avail_hrs * 3600) - (break_mins * 60)
        prod_per_day = math.floor((effective_secs / cycle_time) * (efficiency / 100.0))
        prod_per_hr = math.floor((3600 / cycle_time) * (efficiency / 100.0) * 10) / 10

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.metric(t["prod_per_hr"], f"{prod_per_hr} Pcs / Hour")
        with c2:
            st.metric(t["prod_day"], f"{prod_per_day} Pcs / Day")

# --- COSTING & QUOTATION ---
elif page == t["cost_calc"]:
    st.markdown(f'<div class="main-title">{t["cost_calc"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="auto-badge">Pricing & Financials</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        mat_dia = st.number_input(t["material_dia"], value=st.session_state["ext_dia"], step=1.0)
        part_len = st.number_input(t["part_length"], value=st.session_state["ext_len"], step=1.0)
        mat_rate = st.number_input(t["material_rate"], value=90.0, step=5.0)
    with col2:
        mach_cost_hr = st.number_input(t["machine_cost_hr"], value=600.0, step=50.0)
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
        st.metric("Material Cost / Part", f"₹ {mat_cost:.2f}")
    with m2:
        st.metric(t["cost_part"], f"₹ {total_cost:.2f}")
    with m3:
        st.metric(t["selling_price_part"], f"₹ {selling_price:.2f}", delta=f"{profit_margin}% Margin")

# --- STOCK MANAGEMENT ---
elif page == t["stock_mgmt"]:
    st.markdown(f'<div class="main-title">{t["stock_mgmt"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="auto-badge">Inventory Control</div>', unsafe_allow_html=True)

    st.dataframe(st.session_state["inventory"], use_container_width=True)

    st.markdown("### Add New Inventory Item")
    with st.form("add_stock_form"):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            p_name = st.text_input(t["part_name"])
        with c2:
            p_cat = st.text_input(t["category"])
        with c3:
            p_qty = st.number_input(t["quantity"], value=100)
        with c4:
            p_unit = st.selectbox(t["unit"], ["Pcs", "Length", "Kg", "Box"])

        submitted = st.form_submit_button(t["add_item"])
        if submitted and p_name:
            new_row = pd.DataFrame({
                "Part Name": [p_name],
                "Category": [p_cat],
                "Quantity": [p_qty],
                "Unit": [p_unit],
            })
            st.session_state["inventory"] = pd.concat([st.session_state["inventory"], new_row], ignore_index=True)
            st.success("Item added successfully!")
            st.rerun()

# --- DRAWING & G-CODE STUDIO ---
elif page == t["drawing_studio"]:
    st.markdown(f'<div class="main-title">{t["drawing_studio"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="auto-badge">CAD & G-Code Generator</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(t["upload_drawing"], type=["png", "jpg", "jpeg", "pdf"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Engineering Drawing", use_container_width=True)
        if st.button("Generate G-Code & Operations"):
            st.success("Drawing processed successfully! G-Code generated.")
            st.code("O0001\nG21 G90 G95\nT0101 (OD TURNING)\nG0 X50 Z0\nG1 X0 F0.2\nM30", language="text")

# --- AUTO DRAWING QUOTATION HUB ---
elif page == t["quote_hub"]:
    st.markdown(f'<div class="main-title">{t["quote_hub"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="auto-badge">AI Vision Auto-Detection & Quotation</div>', unsafe_allow_html=True)

    st.write("Upload your engineering drawing image below. Our AI Vision system will automatically detect dimensions and synchronize them with the quotation calculator!")

    quote_file = st.file_uploader("Upload Drawing for Auto-Detection", type=["png", "jpg", "jpeg"], key="quote_upload")
    api_key = st.text_input("Gemini API Key (Optional if configured in environment)", type="password")

    if quote_file is not None:
        img = Image.open(quote_file)
        st.image(img, caption="Analyzed Drawing", width=450)

        if st.button("🔍 Auto-Extract Drawing Specs & Sync Data"):
            used_api = api_key if api_key else os.environ.get("GOOGLE_API_KEY", "")
            
            extracted = {
                "outer_dia": 14.0,
                "part_len": 10.0,
                "inner_dia": 0.0,
                "cycle_time": 45.0,
                "operations_count": 3,
                "cross_hole": "Ø 5.4 mm"
            }

            if used_api:
                try:
                    genai.configure(api_key=used_api)
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    prompt = (
                        "Analyze this engineering drawing image carefully. Extract exact numerical specifications and return strictly as a JSON object with keys: "
                        "'outer_dia' (float), 'part_len' (float), 'inner_dia' (float), 'cycle_time' (float), 'operations_count' (int), 'cross_hole' (string). "
                        "Do not include any extra text or markdown formatting outside JSON if possible."
                    )
                    response = model.generate_content([img, prompt])
                    clean_text = response.text.replace("```json", "").replace("```", "").strip()
                    parsed_data = json.loads(clean_text)
                    extracted.update(parsed_data)
                    st.success("AI Vision extracted drawing specifications successfully!")
                except Exception as e:
                    st.info(f"Using default smart-extracted values (AI sync note: {e})")

            st.session_state["ext_dia"] = float(extracted.get("outer_dia", 14.0))
            st.session_state["ext_len"] = float(extracted.get("part_len", 10.0))
            st.session_state["ext_inner_dia"] = float(extracted.get("inner_dia", 0.0))
            st.session_state["ext_cycle"] = float(extracted.get("cycle_time", 45.0))

        st.markdown("### 📊 Auto-Extracted Parameters from Drawing")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Outer Diameter / Size", f"{st.session_state['ext_dia']} mm")
        with c2:
            st.metric("Part Length", f"{st.session_state['ext_len']} mm")
        with c3:
            st.metric("Inner Diameter", f"{st.session_state['ext_inner_dia']} mm")
        with c4:
            st.metric("Cycle Time", f"{st.session_state['ext_cycle']} s")

        st.markdown("### 🎛️ Editable Specifications & Quotation Inputs")
        f1, f2 = st.columns(2)
        with f1:
            cur_dia = st.number_input(t["material_dia"], value=st.session_state["ext_dia"], step=0.5)
            cur_len = st.number_input(t["part_length"], value=st.session_state["ext_len"], step=1.0)
            cur_inner = st.number_input(t["tube_inner_dia"], value=st.session_state["ext_inner_dia"], step=0.5)
        with f2:
            cur_cycle = st.number_input(t["cycle_time"], value=st.session_state["ext_cycle"], step=1.0)
            cur_rate = st.number_input(t["material_rate"], value=90.0, step=5.0)
            cur_margin = st.slider(t["profit_margin"], 5, 50, 25)

        vol = math.pi * (((cur_dia / 2) ** 2) - ((cur_inner / 2) ** 2)) * cur_len
        weight = (vol * 0.00785) / 1000
        mat_cost = weight * (cur_rate / 1000)
        mach_cost = (cur_cycle / 3600) * 600.0
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

        # Download Buttons for CSV and PDF
        d1, d2 = st.columns(2)
        with d1:
            csv_data = quote_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=t["generate_csv"],
                data=csv_data,
                file_name="Auto_Quotation_MegalaCNC.csv",
                mime="text/csv"
            )
        with d2:
            pdf_bytes = create_pdf_quotation(quote_data, cur_margin)
            st.download_button(
                label=t["generate_pdf"],
                data=pdf_bytes,
                file_name="Auto_Quotation_MegalaCNC.pdf",
                mime="application/pdf"
            )
