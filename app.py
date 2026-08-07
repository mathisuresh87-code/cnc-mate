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
    .header-container {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 10px 0 20px 0;
        border-bottom: 2px solid rgba(236, 72, 153, 0.3);
        margin-bottom: 25px;
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

# Global Language Initialization
if "app_language" not in st.session_state:
  st.session_state["app_language"] = "தமிழ் (Tamil)"

# Sidebar Language Selection
st.sidebar.markdown(
    '<div style="text-align: center; padding: 5px 0 10px 0;"><h3'
    ' style="color: #ec4899; margin: 0; font-size: 1.15rem; font-weight: 900;'
    ' letter-spacing: 1.5px;">MEGALA CNC MATE</h3></div>',
    unsafe_allow_html=True,
)

selected_lang = st.sidebar.selectbox(
    "🌐 Language / மொழி",
    [
        "English",
        "தமிழ் (Tamil)",
        "हिन्दी (Hindi)",
        "తెలుగు (Telugu)",
        "ಕನ್ನಡ (Kannada)",
        "മലയാളം (Malayalam)",
    ],
    index=[
        "English",
        "தமிழ் (Tamil)",
        "हिन्दी (Hindi)",
        "తెలుగు (Telugu)",
        "ಕನ್ನಡ (Kannada)",
        "മലയാളം (Malayalam)",
    ].index(st.session_state["app_language"]),
)
if selected_lang != st.session_state["app_language"]:
  st.session_state["app_language"] = selected_lang
  st.rerun()

curr_lang = st.session_state["app_language"]

# Multi-Language Dictionary Setup
translations = {
    "English": {
        "back_home": "⬅️ Back to Home",
        "modules": [
            "🏠 Home",
            "📐 Rod Calculator",
            "⏱️ Production Calculator",
            "💰 Costing & Quotation",
            "📦 Stock Management",
            "📷 Drawing & Multi-Op G-Code",
            "📋 Process Breakdown & Customer Quotation",
            "⚙️ More Menu & Settings",
        ],
        "q_title": "Process Breakdown & Customer Quotation Generator",
        "q_desc": (
            "Easily configure operations (Facing, Turning, Grooving, Drilling,"
            " Boring, Chamfering, Tapping, etc.) from the dropdown for your"
            " parts."
        ),
        "cust_name": "Customer Company Name",
        "part_name": "Part Name / Component Name",
        "order_qty": "Order Quantity (Nos)",
        "transport_charges": "Transport & Logistics Charges (Rs.)",
        "configure_ops": "Configure Operations",
        "num_ops": "Number of Operations for this Part",
        "op_name": "Operation Name",
        "machine": "Machine",
        "unit_rate": "Unit Rate (Rs.)",
        "gen_csv": "Generate CSV Quotation File",
    },
    "தமிழ் (Tamil)": {
        "back_home": "⬅️ Back to Home / முகப்புக்குத் திரும்பு",
        "modules": [
            "🏠 Home / முகப்பு",
            "📐 Rod Calculator (ராட் கால்குலேட்டர்)",
            "⏱️ Production Calculator (உற்பத்தி கால்குலேட்டர்)",
            "💰 Costing & Quotation Calculator (செலவு & கொட்டேஷன்)",
            "📦 Stock Management (ஸ்டாக் மேனேஜ்மென்ட்)",
            "📷 Drawing & Multi-Op G-Code (டிராயிங் & ஆட்டோ ரிப்போர்ட்)",
            "📋 Process Breakdown & Customer Quotation (புதிய கொட்டேஷன் மாடியூல்)",
            "⚙️ More Menu & Settings (அமைப்புகள் & மாஸ்டர்ஸ்)",
        ],
        "q_title": (
            "Process Breakdown & Customer Quotation Generator (புதிய கொட்டேஷன்"
            " மாடியூல்)"
        ),
        "q_desc": (
            "உங்கள் பார்ட்டுகளுக்கு தேவையான ஆபரேஷன்களை (Facing, Turning,"
            " Grooving, Drilling, Boring, Chamfering, Tapping போன்றவை)"
            " டிராப்-டவுனில் இருந்து எளிதாகத் தேர்வு செய்யலாம்."
        ),
        "cust_name": "Customer Company Name / வாடிக்கையாளர் பெயர்",
        "part_name": (
            "Part Name / Component Name (உங்கள் பார்ட் பெயர் அல்லது புதிய"
            " பார்ட்)"
        ),
        "order_qty": "Order Quantity / ஆர்டர் எண்ணிக்கை (Nos)",
        "transport_charges": "Transport & Logistics Charges (Rs.)",
        "configure_ops": (
            "Configure Operations (ஆபரேஷன் பெயர்களை டிராப்-டவுனில் இருந்து தேர்வு"
            " செய்யவும்)"
        ),
        "num_ops": (
            "Number of Operations for this Part (இந்த பார்ட்டுக்கு எத்தனை"
            " ஆபரேஷன்கள் உள்ளன?)"
        ),
        "op_name": "Operation Name",
        "machine": "Machine",
        "unit_rate": "Unit Rate (Rs.)",
        "gen_csv": "Generate CSV Quotation File",
    },
    "हिन्दी (Hindi)": {
        "back_home": "⬅️ Back to Home / होम पर वापस जाएं",
        "modules": [
            "🏠 Home / होम",
            "📐 Rod Calculator / रॉड कैलकुलेटर",
            "⏱️ Production Calculator / प्रोडक्शन कैलकुलेटर",
            "💰 Costing & Quotation / कॉस्टिंग और कोटेशन",
            "📦 Stock Management / स्टॉक मैनेजमेंट",
            "📷 Drawing & Multi-Op G-Code / ड्राइंग और जी-कोड",
            "📋 Process Breakdown & Customer Quotation / प्रोसेस और कोटेशन",
            "⚙️ More Menu & Settings / सेटिंग्स",
        ],
        "q_title": (
            "Process Breakdown & Customer Quotation Generator (प्रक्रिया और"
            " कोटेशन जनरेटर)"
        ),
        "q_desc": (
            "अपने पार्ट्स के लिए ड्रॉप-डाउन से आसानी से ऑपरेशन (Facing, Turning,"
            " Grooving, Drilling, Boring, Chamfering, Tapping आदि) चुनें।"
        ),
        "cust_name": "Customer Company Name / ग्राहक कंपनी का नाम",
        "part_name": "Part Name / Component Name / पार्ट का नाम",
        "order_qty": "Order Quantity / ऑर्डर मात्रा (Nos)",
        "transport_charges": "Transport & Logistics Charges (Rs.) / परिवहन शुल्क",
        "configure_ops": (
            "Configure Operations (ड्रॉप-डाउन से ऑपरेशन चुनें)"
        ),
        "num_ops": (
            "Number of Operations for this Part / इस पार्ट के लिए ऑपरेशन की"
            " संख्या"
        ),
        "op_name": "Operation Name / ऑपरेशन का नाम",
        "machine": "Machine / मशीन",
        "unit_rate": "Unit Rate (Rs.) / यूनिट रेट",
        "gen_csv": "Generate CSV Quotation File / कोटेशन फाइल जेनरेट करें",
    },
    "తెలుగు (Telugu)": {
        "back_home": "⬅️ Back to Home / హోమ్‌కి వెళ్లండి",
        "modules": [
            "🏠 Home / హోమ్",
            "📐 Rod Calculator / రాడ్ కాలిక్యులేటర్",
            "⏱️ Production Calculator / ప్రొడక్షన్ కాలిక్యులేటర్",
            "💰 Costing & Quotation / కాస్టింగ్ & కొటేషన్",
            "📦 Stock Management / స్టాక్ మేనేజ్‌మెంట్",
            "📷 Drawing & Multi-Op G-Code / డ్రాయింగ్ & జి-కోడ్",
            "📋 Process Breakdown & Customer Quotation / ప్రాసెస్ & కొటేషన్",
            "⚙️ More Menu & Settings / సెట్టింగ్‌లు",
        ],
        "q_title": (
            "Process Breakdown & Customer Quotation Generator (కొటేషన్ జనరేటర్)"
        ),
        "q_desc": (
            "మీ భాగాల కోసం డ్రాప్-డౌన్ నుండి ఆపరేషన్‌లను (Facing, Turning,"
            " Grooving, Drilling, Boring, Chamfering, Tapping మొదలైనవి)"
            " సులభంగా ఎంచుకోండి."
        ),
        "cust_name": "Customer Company Name / కస్టమర్ కంపెనీ పేరు",
        "part_name": "Part Name / Component Name / పార్ట్ పేరు",
        "order_qty": "Order Quantity / ఆర్డర్ పరిమాణం (Nos)",
        "transport_charges": "Transport & Logistics Charges (Rs.) / రవాణా ఛార్జీలు",
        "configure_ops": (
            "Configure Operations (డ్రాప్-డౌన్ నుండి ఆపరేషన్‌లను ఎంచుకోండి)"
        ),
        "num_ops": (
            "Number of Operations for this Part / ఈ పార్ట్ కోసం ఆపరేషన్‌ల"
            " సంఖ్య"
        ),
        "op_name": "Operation Name / ఆపరేషన్ పేరు",
        "machine": "Machine / మెషిన్",
        "unit_rate": "Unit Rate (Rs.) / యూనిట్ రేట్",
        "gen_csv": "Generate CSV Quotation File",
    },
    "ಕನ್ನಡ (Kannada)": {
        "back_home": "⬅️ Back to Home / ಮುಖಪುಟಕ್ಕೆ ಹಿಂತಿರುಗಿ",
        "modules": [
            "🏠 Home / ಮುಖಪುಟ",
            "📐 Rod Calculator / ರಾಡ್ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
            "⏱️ Production Calculator / ಉತ್ಪಾದನಾ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
            "💰 Costing & Quotation / ವೆಚ್ಚ ಮತ್ತು ಉಲ್ಲೇಖ",
            "📦 Stock Management / ಸ್ಟಾಕ್ ನಿರ್ವಹಣೆ",
            "📷 Drawing & Multi-Op G-Code / ಡ್ರಾಯಿಂಗ್ ಮತ್ತು ಜಿ-ಕೋಡ್",
            "📋 Process Breakdown & Customer Quotation / ಪ್ರಕ್ರಿಯೆ ಮತ್ತು ಉಲ್ಲೇಖ",
            "⚙️ More Menu & Settings / ಸೆಟ್ಟಿಂಗ್‌ಗಳು",
        ],
        "q_title": (
            "Process Breakdown & Customer Quotation Generator (ಉಲ್ಲೇಖ ಜನರೇಟರ್)"
        ),
        "q_desc": (
            "ನಿಮ್ಮ ಭಾಗಗಳಿಗಾಗಿ ಡ್ರಾಪ್-ಡೌನ್‌ನಿಂದ ಆಪರೇಷನ್‌ಗಳನ್ನು (Facing, Turning,"
            " Grooving, Drilling, Boring, Chamfering, Tapping ಇತ್ಯಾದಿ) ಸುಲಭವಾಗಿ"
            " ಆಯ್ಕೆಮಾಡಿ."
        ),
        "cust_name": "Customer Company Name / ಗ್ರಾಹಕರ ಕಂಪನಿಯ ಹೆಸರು",
        "part_name": "Part Name / Component Name / ಭಾಗದ ಹೆಸರು",
        "order_qty": "Order Quantity / ಆದೇಶದ ಪ್ರಮಾಣ (Nos)",
        "transport_charges": "Transport & Logistics Charges (Rs.) / ಸಾರಿಗೆ ಶುಲ್ಕ",
        "configure_ops": (
            "Configure Operations (ಡ್ರಾಪ್-ಡೌನ್‌ನಿಂದ ಕಾರ್ಯಾಚರಣೆಗಳನ್ನು ಆಯ್ಕೆಮಾಡಿ)"
        ),
        "num_ops": (
            "Number of Operations for this Part / ಈ ಭಾಗಕ್ಕೆ ಕಾರ್ಯಾಚರಣೆಗಳ ಸಂಖ್ಯೆ"
        ),
        "op_name": "Operation Name / ಕಾರ್ಯಾಚರಣೆಯ ಹೆಸರು",
        "machine": "Machine / ಯಂತ್ರ",
        "unit_rate": "Unit Rate (Rs.) / ಯುನಿಟ್ ದರ",
        "gen_csv": "Generate CSV Quotation File",
    },
    "മലയാളം (Malayalam)": {
        "back_home": "⬅️ Back to Home / ഹോമിലേക്ക് മടങ്ങുക",
        "modules": [
            "🏠 Home / ഹോം",
            "📐 Rod Calculator / റോഡ് കാൽക്കുലേറ്റർ",
            "⏱️ Production Calculator / പ്രൊഡക്ഷൻ കാൽക്കുലേറ്റർ",
            "💰 Costing & Quotation / കോസ്റ്റിംഗ് & കൊട്ടേഷൻ",
            "📦 Stock Management / സ്റ്റോക്ക് മാനേജ്മെന്റ്",
            "📷 Drawing & Multi-Op G-Code / ഡ്രോയിംഗ് & ജി-കോഡ്",
            "📋 Process Breakdown & Customer Quotation / പ്രോസസ്സ് & കൊട്ടേഷൻ",
            "⚙️ More Menu & Settings / ക്രമീകരണങ്ങൾ",
        ],
        "q_title": (
            "Process Breakdown & Customer Quotation Generator (കൊട്ടേഷൻ"
            " ജനറേറ്റർ)"
        ),
        "q_desc": (
            "നിങ്ങളുടെ ഭാഗങ്ങൾക്കായി ഡ്രോപ്പ്-ഡൗണിൽ നിന്ന് പ്രവർത്തനങ്ങൾ"
            " (Facing, Turning, Grooving, Drilling, Boring, Chamfering,"
            " Tapping തുടങ്ങിയവ) എളുപ്പത്തിൽ തിരഞ്ഞെടുക്കുക."
        ),
        "cust_name": "Customer Company Name / കസ്റ്റമർ കമ്പനിയുടെ പേര്",
        "part_name": "Part Name / Component Name / ഭാഗത്തിന്റെ പേര്",
        "order_qty": "Order Quantity / ഓർഡർ അളവ് (Nos)",
        "transport_charges": "Transport & Logistics Charges (Rs.) / ഗതാഗത നിരക്കുകൾ",
        "configure_ops": (
            "Configure Operations (ഡ്രോപ്പ്-ഡൗണിൽ നിന്ന് പ്രവർത്തനങ്ങൾ"
            " തിരഞ്ഞെടുക്കുക)"
        ),
        "num_ops": (
            "Number of Operations for this Part / ഈ ഭാഗത്തിനുള്ള"
            " പ്രവർത്തനങ്ങളുടെ എണ്ണം"
        ),
        "op_name": "Operation Name / ഓപ്പറേഷന്റെ പേര്",
        "machine": "Machine / മെഷീൻ",
        "unit_rate": "Unit Rate (Rs.) / യൂണിറ്റ് റേറ്റ്",
        "gen_csv": "Generate CSV Quotation File",
    },
}

t = translations[curr_lang]
module_list = t["modules"]

if "selected_module" not in st.session_state:
  st.session_state["selected_module"] = module_list[0]

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


# Sidebar Logo & Navigation
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

uploaded_logo = st.sidebar.file_uploader(
    "Upload Permanent Logo",
    type=["png", "jpg", "jpeg"],
    key="sidebar_logo_upload",
    label_visibility="collapsed",
)
if uploaded_logo is not None:
  try:
    Image.open(uploaded_logo).save(LOGO_PATH)
    st.sidebar.success("✅ Logo Saved!")
    st.rerun()
  except Exception as e:
    st.sidebar.error(f"Error: {e}")

st.sidebar.markdown("---")
selected_module = st.sidebar.selectbox(
    "Select Module",
    module_list,
    index=(
        module_list.index(st.session_state["selected_module"])
        if st.session_state["selected_module"] in module_list
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
if "Home" in selected_module:
  m1, m2, m3, m4 = st.columns(4)
  with m1:
    st.metric("Active Machines", "4 Units", "Running 🚀")
  with m2:
    st.metric("Today's Output", "1,850 Nos", "+12% 📈")
  with m3:
    st.metric("Material Stock Items", "4 Items", "Optimal ✨")
  with m4:
    st.metric("Stock Alerts", "0 Alerts", "Check Stock ⚠️")

  st.markdown("<br>", unsafe_allow_html=True)
  st.markdown("### 🚀 Core Modules")

  col1, col2, col3 = st.columns(3)
  with col1:
    if st.button("🚀 Rod Calculator", use_container_width=True, key="bh1"):
      st.session_state["selected_module"] = module_list[1]
      st.rerun()
  with col2:
    if st.button("🚀 Production Calc", use_container_width=True, key="bh2"):
      st.session_state["selected_module"] = module_list[2]
      st.rerun()
  with col3:
    if st.button("🚀 Costing & Quote", use_container_width=True, key="bh3"):
      st.session_state["selected_module"] = module_list[3]
      st.rerun()

# 2. ROD CALCULATOR
elif "Rod Calculator" in selected_module:
  if st.button(t["back_home"]):
    st.session_state["selected_module"] = module_list[0]
    st.rerun()
  st.subheader("📐 Rod Calculator")
  st.write("Rod calculation module active.")

# 3. PRODUCTION CALCULATOR
elif "Production Calculator" in selected_module:
  if st.button(t["back_home"]):
    st.session_state["selected_module"] = module_list[0]
    st.rerun()
  st.subheader("⏱️ Production Calculator")
  st.write("Production calculation module active.")

# 4. COSTING & QUOTATION
elif "Costing & Quotation" in selected_module:
  if st.button(t["back_home"]):
    st.session_state["selected_module"] = module_list[0]
    st.rerun()
  st.subheader("💰 Costing & Quotation Calculator")
  st.write("Costing module active.")

# 5. STOCK MANAGEMENT
elif "Stock Management" in selected_module:
  if st.button(t["back_home"]):
    st.session_state["selected_module"] = module_list[0]
    st.rerun()
  st.subheader("📦 Stock Management")
  st.dataframe(st.session_state["stock_inventory_df"], use_container_width=True)

# 6. DRAWING & MULTI-OP G-CODE
elif "Drawing" in selected_module:
  if st.button(t["back_home"]):
    st.session_state["selected_module"] = module_list[0]
    st.rerun()
  st.subheader("📷 Drawing Studio & G-Code")
  st.write("Drawing studio module active.")

# 7. PROCESS BREAKDOWN & CUSTOMER QUOTATION (FULLY DYNAMIC LANGUAGE DROPDOWNS)
elif "Process Breakdown" in selected_module:
  if st.button(t["back_home"]):
    st.session_state["selected_module"] = module_list[0]
    st.rerun()

  st.subheader(f"📋 {t['q_title']}")
  st.write(t["q_desc"])

  col_q1, col_q2 = st.columns(2)
  with col_q1:
    cust_name = st.text_input(t["cust_name"], value="M/s Precision Engineering Ltd")
    part_name_input = st.text_input(
        t["part_name"], value="Custom Component / Coin Part"
    )
  with col_q2:
    order_qty = st.number_input(t["order_qty"], value=1000, min_value=1)
    transport_amt = st.number_input(t["transport_charges"], value=1500.0)

  st.markdown("---")
  st.subheader(f"⚙️ {t['configure_ops']}")

  num_ops = st.number_input(t["num_ops"], min_value=1, max_value=10, value=3)

  # Language-based Operations and Machines Lists
  if curr_lang == "English":
    op_dropdown_options = [
        "Facing",
        "Turning - Rough & Finish",
        "Grooving",
        "Drilling",
        "Boring",
        "Chamfering",
        "Tapping",
        "Parting / Cut-off",
        "Thread Cutting",
        "Milling",
        "Deburring & Finishing",
        "Special Operation",
    ]
    mach_dropdown_options = [
        "CNC Turning",
        "VMC / Milling",
        "Drilling Machine",
        "Traub Lathe",
        "Manual / Bench",
        "Special Setup",
    ]
  elif curr_lang == "தமிழ் (Tamil)":
    op_dropdown_options = [
        "Facing (பேசிங்)",
        "Turning - Rough & Finish (டர்னிங்)",
        "Grooving (குரூவிங்)",
        "Drilling (ட்ரில்லிங்)",
        "Boring (போரிங்)",
        "Chamfering (சாம்பர்)",
        "Tapping (டாப்பிங்)",
        "Parting / Cut-off (பார்ட்டிங்)",
        "Thread Cutting (த்ரெட்டிங்)",
        "Milling (மில்லிங்)",
        "Deburring & Finishing (பினிஷிங்)",
        "Special Operation (ஸ்பெஷல் ஆபரேஷன்)",
    ]
    mach_dropdown_options = [
        "CNC Turning (சிஎன்சி டர்னிங்)",
        "VMC / Milling (விஎம்சி / மில்லிங்)",
        "Drilling Machine (ட்ரில்லிங் மிஷின்)",
        "Traub Lathe (ட்ராப் லேத்)",
        "Manual / Bench (மேனுவல் / பெஞ்ச்)",
        "Special Setup (ஸ்பெஷல் செட்டப்)",
    ]
  elif curr_lang == "हिन्दी (Hindi)":
    op_dropdown_options = [
        "Facing (फेसिंग)",
        "Turning - Rough & Finish (टर्निंग)",
        "Grooving (ग्रूविंग)",
        "Drilling (ड्रिलिंग)",
        "Boring (बोरिंग)",
        "Chamfering (चमफेरिंग)",
        "Tapping (टैपिंग)",
        "Parting / Cut-off (पार्टिंग)",
        "Thread Cutting (थ्रेड कटिंग)",
        "Milling (मिलिंग)",
        "Deburring & Finishing (फिनिशिंग)",
        "Special Operation (विशेष ऑपरेशन)",
    ]
    mach_dropdown_options = [
        "CNC Turning (सीएनसी टर्निंग)",
        "VMC / Milling (वीएमसी / मिलिंग)",
        "Drilling Machine (ड्रिलिंग मशीन)",
        "Traub Lathe (ट्रॉब लेथ)",
        "Manual / Bench (मैनुअल / बेंच)",
        "Special Setup (विशेष सेटअप)",
    ]
  elif curr_lang == "తెలుగు (Telugu)":
    op_dropdown_options = [
        "Facing (ఫేసింగ్)",
        "Turning - Rough & Finish (టర్నింగ్)",
        "Grooving (గ్రూవింగ్)",
        "Drilling (డ్రిల్లింగ్)",
        "Boring (బోరింగ్)",
        "Chamfering (చాంపరింగ్)",
        "Tapping (టాపింగ్)",
        "Parting / Cut-off (పార్టింగ్)",
        "Thread Cutting (థ్రెడ్ కటింగ్)",
        "Milling (మిల్లింగ్)",
        "Deburring & Finishing (ఫినిషింగ్)",
        "Special Operation (స్పెషల్ ఆపరేషన్)",
    ]
    mach_dropdown_options = [
        "CNC Turning (సిఎన్‌సి టర్నింగ్)",
        "VMC / Milling (విఎంసి / మిల్లింగ్)",
        "Drilling Machine (డ్రిల్లింగ్ మెషిన్)",
        "Traub Lathe (ట్రాబ్ లేత్)",
        "Manual / Bench (మాన్యువల్ / బెంచ్)",
        "Special Setup (స్పెషల్ సెటప్)",
    ]
  elif curr_lang == "ಕನ್ನಡ (Kannada)":
    op_dropdown_options = [
        "Facing (ಫೇಸಿಂಗ್)",
        "Turning - Rough & Finish (ಟರ್ನಿಂಗ್)",
        "Grooving (ಗ್ರೂವಿಂಗ್)",
        "Drilling (ಡ್ರಿಲ್ಲಿಂಗ್)",
        "Boring (ಬೋರಿಂಗ್)",
        "Chamfering (ಚಾಂಫರಿಂಗ್)",
        "Tapping (ಟ್ಯಾಪಿಂಗ್)",
        "Parting / Cut-off (ಪಾರ್ಟಿಂಗ್)",
        "Thread Cutting (ಥ್ರೆಡ್ ಕಟಿಂಗ್)",
        "Milling (ಮಿಲಿಂಗ್)",
        "Deburring & Finishing (ಫಿನಿಶಿಂಗ್)",
        "Special Operation (ವಿಶೇಷ ಕಾರ್ಯಾಚರಣೆ)",
    ]
    mach_dropdown_options = [
        "CNC Turning (ಸಿಎನ್‌ಸಿ ಟರ್ನಿಂಗ್)",
        "VMC / Milling (ವಿಎಮ್‌ಸಿ / ಮಿಲ್ಲಿಂಗ್)",
        "Drilling Machine (ಡ್ರಿಲ್ಲಿಂಗ್ ಮೆಷಿನ್)",
        "Traub Lathe (ಟ್ರಾಬ್ ಲೇಥ್)",
        "Manual / Bench (ಮ್ಯಾನುವಲ್ / ಬೆಂಚ್)",
        "Special Setup (ವಿಶೇಷ ಸೆಟಪ್)",
    ]
  else:  # Malayalam
    op_dropdown_options = [
        "Facing (ഫേസിംഗ്)",
        "Turning - Rough & Finish (ടേണിംഗ്)",
        "Grooving (ഗ്രൂവിംഗ്)",
        "Drilling (ഡ്രില്ലിംഗ്)",
        "Boring (ബോറിംഗ്)",
        "Chamfering (ചാമ്പറിംഗ്)",
        "Tapping (ടാപ്പിംഗ്)",
        "Parting / Cut-off (പാർട്ടിംഗ്)",
        "Thread Cutting (ത്രെഡ് കട്ടിംഗ്)",
        "Milling (മില്ലിംഗ്)",
        "Deburring & Finishing (ഫിനിഷിംഗ്)",
        "Special Operation (സ്പെഷ്യൽ ഓപ്പറേഷൻ)",
    ]
    mach_dropdown_options = [
        "CNC Turning (സിഎൻസി ടേണിംഗ്)",
        "VMC / Milling (വിഎംസി / മില്ലിംഗ്)",
        "Drilling Machine (ഡ്രില്ലിംഗ് മെഷീൻ)",
        "Traub Lathe (ട്രോബ് ലേത്)",
        "Manual / Bench (മാനുവൽ / ബെഞ്ച്)",
        "Special Setup (സ്പെഷ്യൽ സെറ്റപ്പ്)",
    ]

  edited_ops = []
  for i in range(int(num_ops)):
    st.markdown(f"**Operation {i+1} Setup**")
    col_a, col_b, col_c = st.columns([3, 2, 2])
    with col_a:
      op_name = st.selectbox(
          f"{t['op_name']} {i+1}",
          op_dropdown_options,
          index=min(i, len(op_dropdown_options) - 1),
          key=f"dyn_op_n_{i}",
      )
    with col_b:
      mach_name = st.selectbox(
          f"{t['machine']} {i+1}",
          mach_dropdown_options,
          key=f"dyn_op_m_{i}",
      )
    with col_c:
      op_rate = st.number_input(
          f"{t['unit_rate']} {i+1}",
          value=15.0 + (i * 5.0),
          key=f"dyn_op_r_{i}",
      )

    edited_ops.append({
        "name": op_name,
        "machine": mach_name,
        "qty": order_qty,
        "rate": op_rate,
    })

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button(f"🚀 {t['gen_csv']}", use_container_width=True):
    csv_data = generate_quotation_csv(
        cust_name, part_name_input, edited_ops, transport_amt
    )
    filename = f"Megala_Industries_Quotation_{part_name_input.replace(' ', '_').replace('/', '_')}.csv"
    st.success(f"✅ CSV successfully generated: {filename}")
    st.download_button(
        "📥 Download CSV Quotation (.csv)",
        data=csv_data,
        file_name=filename,
        mime="text/csv",
    )

# 8. MORE MENU & SETTINGS
elif "More Menu" in selected_module:
  if st.button(t["back_home"]):
    st.session_state["selected_module"] = module_list[0]
    st.rerun()
  st.subheader("⚙️ Settings & Language Preferences")
  lang_choice = st.selectbox(
      "🌐 Select Language / மொழி",
      [
          "English",
          "தமிழ் (Tamil)",
          "हिन्दी (Hindi)",
          "తెలుగు (Telugu)",
          "ಕನ್ನಡ (Kannada)",
          "മലയാളം (Malayalam)",
      ],
      index=[
          "English",
          "தமிழ் (Tamil)",
          "हिन्दी (Hindi)",
          "తెలుగు (Telugu)",
          "ಕನ್ನಡ (Kannada)",
          "മലയാളം (Malayalam)",
      ].index(curr_lang),
  )
  if lang_choice != st.session_state["app_language"]:
    st.session_state["app_language"] = lang_choice
    st.success(f"Language updated to: {lang_choice}")
    st.rerun()
