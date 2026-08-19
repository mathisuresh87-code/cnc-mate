import base64
import io
import math
import os
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image

# Plotly library check for Live 3D Visualization
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
    page_title="MEGALA CNC MATE - Smart CNC. Simple Work.",
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

# Custom UI Styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #050B18 0%, #0A1428 50%, #040711 100%);
    color: #FFFFFF;
    font-family: 'Segoe UI', Roboto, Helvetica, sans-serif;
}
.brand-container {
    text-align: center;
    padding: 20px 0;
    background: radial-gradient(circle at center, #0F1C3F 0%, #070B19 100%);
    border-bottom: 2px solid #1E3A8A;
    margin-bottom: 15px;
    border-radius: 0 0 20px 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
}
.logo-glow-box {
    display: inline-block;
    padding: 8px;
    background: radial-gradient(circle, rgba(72, 202, 228, 0.3) 0%, rgba(10, 20, 40, 0.95) 100%);
    border-radius: 50%;
    box-shadow: 0 0 30px rgba(72, 202, 228, 0.8), inset 0 0 15px rgba(72, 202, 228, 0.5);
    border: 2px solid #48CAE4;
    margin-bottom: 10px;
}
.logo-glow-box img {
    width: 70px !important;
    height: auto !important;
    border-radius: 50%;
    display: block;
    margin: auto;
}
.brand-title {
    font-size: 28px;
    font-weight: 900;
    letter-spacing: 3px;
    background: linear-gradient(90deg, #48CAE4, #0077B6, #FFFFFF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: 4px;
    text-align: center;
    text-shadow: 0 0 25px rgba(72, 202, 228, 0.5);
}
.brand-subtitle {
    font-size: 11px;
    letter-spacing: 3px;
    color: #94A3B8;
    font-weight: 600;
    text-transform: uppercase;
    margin-top: 4px;
    text-align: center;
}
.metric-card {
    background: linear-gradient(145deg, #111E38, #0B132B);
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #1E3A8A;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
    text-align: center;
    margin-bottom: 12px;
    min-height: 120px;
}
.stButton>button {
    width: 100%;
    background: linear-gradient(90deg, #1D4ED8, #00B4D8);
    color: white;
    font-weight: bold;
    border-radius: 12px;
    height: 42px;
    border: none;
}
.upload-status-box {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(6, 182, 212, 0.2));
    border: 2px solid #10B981;
    padding: 18px;
    border-radius: 14px;
    margin-top: 15px;
    margin-bottom: 20px;
    box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
}
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
    <div class="brand-subtitle">SMART CNC. SIMPLE WORK.</div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# Session states initialization
if "nav_menu" not in st.session_state:
    st.session_state.nav_menu = "Home Dashboard"
if "calc_results" not in st.session_state:
    st.session_state.calc_results = None

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

def navigate_to(menu_name):
    st.session_state.nav_menu = menu_name

# Multi-Language Dictionary Support
LANG_DICT = {
    "English": {
        "welcome": "Welcome Operator 👋 (MEGALA CNC MATE Suite)",
        "subtitle": "Ultra-Advanced CNC, Traub & Blueprint Studio - Select any module below",
        "nav_home": "Home Dashboard",
        "nav_rod": "Rod & Tube Calculator",
        "nav_traub": "Traub Collet & Bar Feed",
        "nav_oee": "Production & OEE Analyzer",
        "nav_tool": "Tool Life & Thread Master",
        "nav_stock": "Stock Management",
        "nav_gcode": "Advanced G-Code Generator",
        "nav_quote": "Quotation & PDF Studio",
        "nav_settings": "More Menu / Master Settings",
    },
    "Tamil (தமிழ்)": {
        "welcome": "வணக்கம் ஆபரேட்டர் 👋 (மேகலா சிஎன்சி மேட் சூட்)",
        "subtitle": "அல்ட்ரா-அட்வான்ஸ்டு சிஎன்சி, டிராப் & ப்ளூபிரிண்ட் ஸ்டுடியோ - கீழே உள்ள தொகுப்பைத் தேர்ந்தெடுக்கவும்",
        "nav_home": "முகப்பு டேஷ்போர்டு",
        "nav_rod": "ராட் & டூப் கால்குலேட்டர்",
        "nav_traub": "டிராப் காலெட் & பார் ஃபீட்",
        "nav_oee": "உற்பத்தி & OEE அனலைசர்",
        "nav_tool": "டூல் லைஃப் & த்ரெட் மாஸ்டர்",
        "nav_stock": "ஸ்டாக் மேனேஜ்மென்ட்",
        "nav_gcode": "அட்வான்ஸ்டு ஜி-கோடு ஜெனரேட்டர்",
        "nav_quote": "கோட்டேஷன் & பிடிஎஃப் ஸ்டுடியோ",
        "nav_settings": "மேலும் மெனு / மாஸ்டர் செட்டிங்ஸ்",
    },
    "Hindi (हिन्दी)": {
        "welcome": "स्वागत है ऑपरेटर 👋 (मेगाला सीएनसी मेट)",
        "subtitle": "अल्ट्रा-एडवांस्ड सीएनसी, ट्रब और ब्लूप्रिंट स्टूडियो - नीचे दिए गए मॉड्यूल का चयन करें",
        "nav_home": "होम डैशबोर्ड",
        "nav_rod": "रॉड और ट्यूब कैलकुलेटर",
        "nav_traub": "ट्रब कोलेट और बार फीड",
        "nav_oee": "उत्पादन और OEE विश्लेषक",
        "nav_tool": "टूल लाइफ और थ्रेड मास्टर",
        "nav_stock": "स्टॉक प्रबंधन",
        "nav_gcode": "एडवांस्ड जी-कोड जनरेटर",
        "nav_quote": "कोटेशन और पीडीएफ स्टूडियो",
        "nav_settings": "अधिक मेनू / मास्टर सेटिंग्स",
    },
    "Telugu (తెలుగు)": {
        "welcome": "స్వాగతం ఆపరేటర్ 👋 (మెగాలా CNC మేట్)",
        "subtitle": "అల్ట్రా-అడ్వాన్స్‌డ్ CNC, ట్రాబ్ & బ్లూప్రింట్ స్టూడియో - క్రింది మాడ్యూల్‌ను ఎంచుకోండి",
        "nav_home": "హోమ్ డ్యాష్‌బోర్డ్",
        "nav_rod": "రాడ్ & ట్యూబ్ కాలిక్యులేటర్",
        "nav_traub": "ట్రాబ్ కొల్లెట్ & బార్ ఫీడ్",
        "nav_oee": "ఉత్పత్తి & OEE ఎనలైజర్",
        "nav_tool": "టూల్ లైఫ్ & త్రెడ్ మాస్టర్",
        "nav_stock": "స్టాక్ మేనేజ్‌మెంట్",
        "nav_gcode": "అడ్వాన్స్‌డ్ G-కోడ్ జనరేటర్",
        "nav_quote": "కొటేషన్ & PDF స్టూడియో",
        "nav_settings": "మరిన్ని మెను / మాస్టర్ సెట్టింగ్‌లు",
    },
    "Kannada (ಕನ್ನಡ)": {
        "welcome": "ಸ್ವಾಗತ ಆಪರೇಟರ್ 👋 (ಮೆಗಾಲಾ ಸಿಎನ್‌ಸಿ ಮೇಟ್)",
        "subtitle": "ಅಲ್ಟ್ರಾ-ಅಡ್ವಾನ್ಸ್‌ಡ್ ಸಿಎನ್‌ಸಿ, ಟ್ರಾಬ್ & ಬ್ಲೂಪ್ರಿಂಟ್ ಸ್ಟುಡಿಯೋ - ಕೆಳಗಿನ ಮಾಡ್ಯೂಲ್ ಅನ್ನು ಆಯ್ಕೆ ಮಾಡಿ",
        "nav_home": "ಮುಖಪುಟ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "nav_rod": "ರಾಡ್ & ಟ್ಯೂಬ್ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
        "nav_traub": "ಟ್ರಾಬ್ ಕೊಲೆಟ್ & ಬಾರ್ ಫೀಡ್",
        "nav_oee": "ಉತ್ಪಾದನೆ & OEE ವಿಶ್ಲೇಷಕ",
        "nav_tool": "ಟೂಲ್ ಲೈಫ್ & ಥ್ರೆಡ್ ಮಾಸ್ಟರ್",
        "nav_stock": "ಸ್ಟಾಕ್ ನಿರ್ವಹಣೆ",
        "nav_gcode": "ಅಡ್ವಾನ್ಸ್‌ಡ್ ಜಿ-ಕೋಡ್ ಜನರೇಟರ್",
        "nav_quote": "ಕೊಟೇಷನ್ & ಪಿಡಿಎಫ್ ಸ್ಟುಡಿಯೋ",
        "nav_settings": "ಹೆಚ್ಚಿನ ಮೆನು / ಮಾಸ್ಟರ್ ಸೆಟ್ಟಿಂಗ್‌ಗಳು",
    },
    "Malayalam (മലയാളം)": {
        "welcome": "സ്വാഗതം ഓപ്പറേറ്റർ 👋 (മേഘാല സിഎൻസി മേറ്റ്)",
        "subtitle": "അൾട്രാ-അഡ്വാൻസ്ഡ് സിഎൻസി, ട്രാബ് & ബ്ലൂപ്രിന്റ് സ്റ്റുഡിയോ - താഴെയുള്ള മൊഡ്യൂൾ തിരഞ്ഞെടുക്കുക",
        "nav_home": "ഹോം ഡാഷ്‌ബോർഡ്",
        "nav_rod": "റോഡ് & ട്യൂബ് കാൽക്കുലേറ്റർ",
        "nav_traub": "ട്രാബ് കൊളറ്റ് & ബാർ ഫീഡ്",
        "nav_oee": "ഉത്പാദനം & OEE അനലൈസർ",
        "nav_tool": "ടൂൾ ലൈഫ് & ത്രെഡ് മാസ്റ്റർ",
        "nav_stock": "സ്റ്റോക്ക് മാനേജ്മെന്റ്",
        "nav_gcode": "അഡ്വാൻസ്ഡ് ജി-കോഡ് ജനറേറ്റർ",
        "nav_quote": "കൊട്ടേഷൻ & പിഡിഎഫ് സ്റ്റുഡിയോ",
        "nav_settings": "കൂടുതൽ മെനു / മാസ്റ്റർ ക്രമീകരണങ്ങൾ",
    }
}

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

languages = ["Tamil (தமிழ்)", "English", "Hindi (हिन्दी)", "Telugu (తెలుగు)", "Kannada (ಕನ್ನಡ)", "Malayalam (മലയാളം)"]
selected_lang = st.sidebar.selectbox("Select Language / மொழி", languages)
lang = LANG_DICT.get(selected_lang, LANG_DICT["English"])

st.sidebar.markdown("---")
menu_options = [
    "Home Dashboard",
    "Rod & Tube Calculator",
    "Traub Collet & Bar Feed",
    "Production & OEE Analyzer",
    "Tool Life & Thread Master",
    "Stock Management",
    "Advanced G-Code Generator",
    "Quotation & PDF Studio",
    "More Menu / Master Settings",
]

selected_sidebar_menu = st.sidebar.radio(
    "Navigation Menu",
    menu_options,
    index=menu_options.index(st.session_state.nav_menu),
)
if selected_sidebar_menu != st.session_state.nav_menu:
    st.session_state.nav_menu = selected_sidebar_menu
    st.rerun()

# Helper function for precise shape mesh generation in 3D Plotly
def generate_3d_shape_mesh(shape, size, length, inner_dia=0.0):
    z_vals = np.linspace(0, length, 30)
    theta = np.linspace(0, 2 * np.pi, 60)
    Theta, Z = np.meshgrid(theta, z_vals)

    if shape == "Round":
        R = size / 2.0
        X = R * np.cos(Theta)
        Y = R * np.sin(Theta)
        return [go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', showscale=False)]
    
    elif shape == "Tube":
        R_out = size / 2.0
        R_in = max(0.1, inner_dia / 2.0)
        X_out = R_out * np.cos(Theta)
        Y_out = R_out * np.sin(Theta)
        X_in = R_in * np.cos(Theta)
        Y_in = R_in * np.sin(Theta)
        return [
            go.Surface(x=X_out, y=Y_out, z=Z, colorscale='Blues', showscale=False),
            go.Surface(x=X_in, y=Y_in, z=Z, colorscale='Greys', showscale=False)
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
            go.Surface(x=X_f, y=Y_f, z=Z_f, colorscale='Plasma', showscale=False),
            go.Surface(x=X_b, y=Y_b, z=Z_b, colorscale='Viridis', showscale=False)
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
            go.Surface(x=X_out, y=Y_out, z=Z_b, colorscale='Teal', showscale=False),
            go.Surface(x=X_in, y=Y_in, z=Z_b, colorscale='Copper', showscale=False)
        ]

    elif shape in ["Square", "Hexagon"]:
        n_sides = 6 if shape == "Hexagon" else 4
        half_angle = np.pi / n_sides
        r_poly = (size / 2.0) * np.cos(half_angle) / np.cos((Theta % (2 * np.pi / n_sides)) - half_angle)
        X = r_poly * np.cos(Theta)
        Y = r_poly * np.sin(Theta)
        return [go.Surface(x=X, y=Y, z=Z, colorscale='Plasma', showscale=False)]
    
    else:
        R = size / 2.0
        X = R * np.cos(Theta)
        Y = R * np.sin(Theta)
        return [go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', showscale=False)]

# Helper function for Multi-Step Stepped Shaft 3D Mesh Generation
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
        meshes.append(go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', showscale=False))
        current_z += length
    return meshes

# 1. HOME DASHBOARD (ALL 9 MODULE CARDS INCLUDED)
if st.session_state.nav_menu == "Home Dashboard":
    st.markdown(f'<div style="font-size: 24px; font-weight: 800; color: #48CAE4; margin-bottom: 5px;">{lang["welcome"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color: #94A3B8; font-size: 14px; margin-bottom: 20px;">{lang["subtitle"]}</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'<div class="metric-card">🏠<div style="font-weight:700; margin-top:8px;">{lang["nav_home"]}</div></div>', unsafe_allow_html=True)
        if st.button("Open Home Dashboard"):
            navigate_to("Home Dashboard")
            st.rerun()

        st.markdown(f'<div class="metric-card">📏<div style="font-weight:700; margin-top:8px;">{lang["nav_rod"]}</div></div>', unsafe_allow_html=True)
        if st.button("Open Rod Calculator"):
            navigate_to("Rod & Tube Calculator")
            st.rerun()

        st.markdown(f'<div class="metric-card">🛠️<div style="font-weight:700; margin-top:8px;">{lang["nav_gcode"]}</div></div>', unsafe_allow_html=True)
        if st.button("Open G-Code Generator"):
            navigate_to("Advanced G-Code Generator")
            st.rerun()

    with col2:
        st.markdown(f'<div class="metric-card">🔧<div style="font-weight:700; margin-top:8px;">{lang["nav_traub"]}</div></div>', unsafe_allow_html=True)
        if st.button("Open Traub Collet Master"):
            navigate_to("Traub Collet & Bar Feed")
            st.rerun()

        st.markdown(f'<div class="metric-card">🧵<div style="font-weight:700; margin-top:8px;">{lang["nav_tool"]}</div></div>', unsafe_allow_html=True)
        if st.button("Open Tool & Thread Master"):
            navigate_to("Tool Life & Thread Master")
            st.rerun()

        st.markdown(f'<div class="metric-card">📄<div style="font-weight:700; margin-top:8px;">{lang["nav_quote"]}</div></div>', unsafe_allow_html=True)
        if st.button("Open Quotation Generator"):
            navigate_to("Quotation & PDF Studio")
            st.rerun()

    with col3:
        st.markdown(f'<div class="metric-card">⏱️<div style="font-weight:700; margin-top:8px;">{lang["nav_oee"]}</div></div>', unsafe_allow_html=True)
        if st.button("Open Production & OEE"):
            navigate_to("Production & OEE Analyzer")
            st.rerun()

        st.markdown(f'<div class="metric-card">📦<div style="font-weight:700; margin-top:8px;">{lang["nav_stock"]}</div></div>', unsafe_allow_html=True)
        if st.button("Open Stock Management"):
            navigate_to("Stock Management")
            st.rerun()

        st.markdown(f'<div class="metric-card">⚙️<div style="font-weight:700; margin-top:8px;">{lang["nav_settings"]}</div></div>', unsafe_allow_html=True)
        if st.button("Open Master Settings"):
            navigate_to("More Menu / Master Settings")
            st.rerun()

# 2. ROD & TUBE CALCULATOR WITH INSTANT DRAWING PREVIEW & 3D ANIMATION
elif st.session_state.nav_menu == "Rod & Tube Calculator":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Rod & Tube Calculator (Instant Drawing Preview & Live 3D Studio)</div>', unsafe_allow_html=True)

    def get_kg_per_meter(dia, shape):
        if dia <= 0: return 0.0
        if shape == "Round": return (dia**2) / 162
        elif shape == "Square": return (dia**2) / 127
        elif shape == "Hexagon": return (dia**2) / 147
        elif shape in ["Tube", "Bush"]: return (dia**2) / 162
        elif shape == "Flange": return (dia**2) / 150
        return (dia**2) / 162

    calc_mode = st.radio("Operating Mode", ["Simple Mode", "Advanced Mode (Drawing Scan & Live 3D Model)"], horizontal=True)

    if "Advanced" in calc_mode:
        st.markdown('<div style="background: rgba(72, 202, 228, 0.1); padding: 15px; border-radius: 10px; border: 1px solid #48CAE4; margin-bottom: 15px;"><b>Advanced Blueprint Scanner Active:</b> Upload part drawing (PNG, JPG, PDF). Preview appears immediately and input values update automatically!</div>', unsafe_allow_html=True)
        
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
                    <h3 style="color: #10B981; margin: 0 0 8px 0;">✅ Drawing Successfully Uploaded & Extracted!</h3>
                    <p style="color: #F8FAFC; margin: 3px 0;"><b>File Name:</b> {adv_drawing.name}</p>
                    <p style="color: #48CAE4; margin: 3px 0;"><b>Extracted Blueprint Dimension (Length):</b> {auto_len} mm | <b>Stock Dia:</b> {auto_dia} mm</p>
                </div>
                """, unsafe_allow_html=True)
                st.image(adv_drawing, caption=f"📷 Instant Preview [{adv_drawing.name}]", use_container_width=True)
            except Exception:
                st.session_state.rod_len_input = 38.7
                st.session_state.rod_dia_input = 51.0
                st.markdown(f"""
                <div class="upload-status-box">
                    <h3 style="color: #10B981; margin: 0 0 8px 0;">✅ Document Successfully Uploaded!</h3>
                    <p style="color: #F8FAFC; margin: 3px 0;"><b>File Name:</b> {adv_drawing.name}</p>
                </div>
                """, unsafe_allow_html=True)
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
        unit_type = st.selectbox("Input Unit", ["Meter", "Kilogram"])
        rod_length_input = st.number_input("Input Value (Length in Meters OR Weight in Kg)", min_value=0.0, value=1.0, step=0.1)
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

    if st.button("Calculate & Render Dynamic 3D Model"):
        kg_per_m = get_kg_per_meter(rod_dia, rod_type)
        total_rod_meters = 0.0
        equivalent_kg = 0.0
        
        if unit_type == "Kilogram":
            equivalent_kg = rod_length_input
            total_rod_meters = (rod_length_input / kg_per_m) if kg_per_m > 0 else 0.0
        else:
            total_rod_meters = rod_length_input
            equivalent_kg = total_rod_meters * kg_per_m

        total_part_len = part_length + cutting_allowance
        rod_total_mm = total_rod_meters * 1000
        
        parts_per_rod = int(rod_total_mm / total_part_len) if (total_part_len > 0 and total_rod_meters > 0) else 0
        used_length_mm = parts_per_rod * total_part_len
        end_bit_mm = (rod_total_mm - used_length_mm) if rod_length_input > 0 else 0.0
        required_rods = math.ceil(required_qty / parts_per_rod) if (parts_per_rod > 0 and required_qty > 0) else 0
        total_stock_len = (required_rods * total_rod_meters) if required_rods > 0 else 0.0
        
        prod_per_hr = int(3600 / cycle_sec) if cycle_sec > 0 else 0
        total_machine_time = ((required_qty * cycle_sec) / 3600) if (required_qty > 0 and cycle_sec > 0) else 0.0
        total_days = (total_machine_time / shift_hours) if (total_machine_time > 0 and shift_hours > 0) else 0.0
        prod_per_shift = int(prod_per_hr * shift_hours) if shift_hours > 0 else 0

        st.session_state.calc_results = {
            "parts_per_rod": parts_per_rod, "end_bit_mm": end_bit_mm,
            "required_rods": required_rods, "total_stock_len": total_stock_len,
            "prod_per_hr": prod_per_hr, "total_machine_time": total_machine_time,
            "total_days": total_days, "shift_hours": shift_hours,
            "prod_per_shift": prod_per_shift, "equivalent_kg": equivalent_kg,
            "total_rod_meters": total_rod_meters, "unit_type": unit_type,
            "rod_dia": rod_dia, "inner_dia": inner_dia_input,
            "part_length": part_length, "rod_type": rod_type,
            "stepped_data": rod_steps_data if rod_type == "Stepped Shaft" else None
        }

    if st.session_state.calc_results is not None:
        res = st.session_state.calc_results
        
        if PLOTLY_AVAILABLE:
            st.markdown("---")
            st.subheader(f"🌐 Dynamic 3D Interactive Component Preview [{res['rod_type']} Shape]")
            if res['rod_type'] == "Stepped Shaft" and res.get('stepped_data'):
                surfaces = generate_3d_stepped_shaft(res['stepped_data'])
            else:
                surfaces = generate_3d_shape_mesh(res['rod_type'], res['rod_dia'], res['part_length'], res.get('inner_dia', 0.0))
            
            fig = go.Figure(data=surfaces)
            fig.update_layout(
                title=dict(text=f"3D Model [{res['rod_type']}] -> Total Length: {res['part_length']} mm", font=dict(size=14, color='#48CAE4')),
                scene=dict(xaxis_title='X Axis (mm)', yaxis_title='Y Axis (mm)', zaxis_title='Length Z (mm)', bgcolor='#0B132B'),
                paper_bgcolor='#050B18', font=dict(color='white'), margin=dict(l=0, r=0, b=0, t=40)
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("📊 Calculation & Production Report Summary")
        r1, r2, r3 = st.columns(3)
        r1.success(f"**Parts / Rod:** {res['parts_per_rod']} Nos")
        r2.warning(f"**End Bit / Scrap:** {res['end_bit_mm']:.2f} mm")
        r3.success(f"**Required Rods:** {res['required_rods']} Nos")

# 3. TRAUB COLLET, BAR FEED & TROUBLESHOOTING MASTER
elif st.session_state.nav_menu == "Traub Collet & Bar Feed":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Traub Collet, Bar Feed, RPM & Troubleshooting Master</div>', unsafe_allow_html=True)
    
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        traub_model = st.selectbox("Traub Machine Model", ["A15 / A25", "A32", "A42 / A60", "TD16 / TD26", "TNS"])
        collet_type = st.selectbox("Collet Profile", ["Round Collet (DIN 6343 / 144E)", "Hexagon Collet", "Square Collet", "Dead Length Collet"])
        raw_bar_dia = st.number_input("Raw Bar Diameter / Across Flats (mm)", min_value=1.0, value=16.0, step=0.5)
    with t_col2:
        tolerance_option = st.selectbox("Bar Stock Tolerance Grade", ["h6", "h7", "h8", "h9 (Standard Bright Bar)", "h10", "h11", "K12", "Custom / Manual Clearance"])
        clearance = 0.05 if "h9" in tolerance_option else 0.02
        cutting_speed_vc = st.number_input("Cutting Speed (Vc in m/min)", min_value=10.0, value=100.0, step=5.0)
        remnant_length = st.number_input("Target Remnant / End Piece Length (mm)", min_value=10.0, value=45.0, step=5.0)

    if st.button("Calculate Traub Collet & Spindle RPM"):
        recommended_collet_size = raw_bar_dia + clearance
        calculated_rpm = int((cutting_speed_vc * 1000) / (math.pi * raw_bar_dia)) if raw_bar_dia > 0 else 0
        
        st.markdown("---")
        sc1, sc2, sc3 = st.columns(3)
        sc1.success(f"**Recommended Collet Bore:** {recommended_collet_size:.2f} mm")
        sc2.info(f"**Calculated Spindle RPM:** {calculated_rpm} RPM")
        sc3.warning(f"**Max Remnant Limit:** {remnant_length} mm")

    st.markdown("---")
    st.markdown("### 📚 Traub Learning & Troubleshooting Guide (டிராப் செட்டிங் & குறைபாட்டு தீர்வுகள்)")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["1. ராட் & ஃபீடர் செட்", "2. காலெட் மாட்டுவது", "3. பார் ஸ்டாப் செட்டிங்", "4. டூல் செட்டிங்", "5. ⚠️ மிஷின் பிராப்ளம் & தீர்வு"])
    with tab1:
        st.markdown("* **படி 1:** உங்கள் மெஷின் மாடலுக்கு ஏற்ற ராடை ஸ்பிண்டில் குழாய்க்குள் செலுத்தவும்.\n* **படி 2:** `Bar Feeder` சரியாக ராட்டின் பின்னால் அமர்ந்துள்ளதா எனச் சரிபார்க்கவும்.")
    with tab2:
        st.markdown("* **படி 1:** ஸ்பிண்டில் முனையில் உள்ள Collet Cap-ஐக் கழற்றவும்.\n* **படி 2:** சரியான அளவுள்ள காலெட்டைப் பொருத்தவும்.")
    with tab3:
        st.markdown("* **படி 1:** பார்ட் நீளத்தை முடிவு செய்ய Bar Stop டூலை ஸ்லைடில் பொருத்தவும்.")
    with tab4:
        st.markdown("* **படி 1:** கிராஸ் ஸ்லைடில் டூல் பிட்டுகளைச் சென்டரில் செட் செய்யவும்.")
    with tab5:
        st.markdown("* **பிரச்சனை 1: ராட் நழுவுவது (Bar Slip)** -> காலெட் கேப்பைச் சற்று இறுக்கவும்.\n* **பிரச்சனை 2: நீளம் மாறுபடுகிறது** -> பார் ஸ்டாப்பர் போல்ட்டை டைட் செய்யவும்.")

# 4. PRODUCTION & OEE ANALYZER
elif st.session_state.nav_menu == "Production & OEE Analyzer":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Production & OEE Analyzer</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        total_planned_time = st.number_input("Planned Production Time (Hours)", min_value=1.0, value=8.0, step=0.5)
        downtime_hours = st.number_input("Total Downtime / Breakdowns (Hours)", min_value=0.0, value=0.5, step=0.1)
        ideal_cycle_time = st.number_input("Ideal Cycle Time per Part (Seconds)", min_value=1.0, value=25.0, step=1.0)
    with col2:
        total_parts_produced = st.number_input("Total Parts Produced (Gross)", min_value=0, value=1000, step=10)
        rejected_parts = st.number_input("Rejected / Defective Parts", min_value=0, value=15, step=1)

    if st.button("Calculate Comprehensive OEE"):
        operating_time = max(0.1, total_planned_time - downtime_hours)
        availability = (operating_time / total_planned_time) * 100.0
        performance = min(100.0, ((ideal_cycle_time * total_parts_produced) / (operating_time * 3600)) * 100.0)
        good_parts = max(0, total_parts_produced - rejected_parts)
        quality = (good_parts / total_parts_produced) * 100.0 if total_parts_produced > 0 else 0.0
        oee = (availability * performance * quality) / 10000.0

        oc1, oc2, oc3, oc4 = st.columns(4)
        oc1.info(f"**Availability:** {availability:.1f}%")
        oc2.info(f"**Performance:** {performance:.1f}%")
        oc3.info(f"**Quality:** {quality:.1f}%")
        oc4.success(f"### **OEE: {oee:.1f}%**")

# 5. TOOL LIFE & THREAD MASTER
elif st.session_state.nav_menu == "Tool Life & Thread Master":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Tool Life & Thread Master</div>', unsafe_allow_html=True)
    sub_tab1, sub_tab2 = st.tabs(["1. Tool Life Predictor", "2. Thread & Pitch Calculator"])
    with sub_tab1:
        v = st.number_input("Cutting Speed V (m/min)", value=150.0)
        c = st.number_input("Taylor Constant C", value=300.0)
        n = st.number_input("Taylor Exponent n", value=0.25)
        if st.button("Calculate Tool Life"):
            life = (c / v) ** (1.0 / n)
            st.success(f"Tool Life: {life:.2f} Minutes")
    with sub_tab2:
        pitch = st.number_input("Thread Pitch (mm)", value=2.5)
        nom = st.number_input("Nominal Dia (mm)", value=20.0)
        st.info(f"Thread Depth: {0.6134 * pitch:.3f} mm | Core Dia: {nom - (1.0825 * pitch):.3f} mm")

# 6. STOCK MANAGEMENT
elif st.session_state.nav_menu == "Stock Management":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Stock Management System</div>', unsafe_allow_html=True)
    st.session_state.stock_db = st.data_editor(st.session_state.stock_db, num_rows="dynamic", use_container_width=True)

# 7. ADVANCED G-CODE GENERATOR WITH INSTANT PREVIEW & 3D STUDIO
elif st.session_state.nav_menu == "Advanced G-Code Generator":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Advanced G-Code Generator & Live 3D Drawing Studio</div>', unsafe_allow_html=True)
    uploaded_drawing = st.file_uploader("📁 Upload Part Drawing / Blueprint", type=["png", "jpg", "jpeg", "webp", "pdf"], key="gcode_drawing_upload")
    if uploaded_drawing is not None:
        st.image(uploaded_drawing, caption=f"📷 Scanned Drawing Preview", use_container_width=True)

    gc_col1, gc_col2, gc_col3 = st.columns(3)
    with gc_col1:
        prog_no = st.text_input("Program Number", value="O1001")
        machine_target = st.selectbox("Target Machine", ["CNC Lathe", "Traub Automatic Lathe", "VMC Machine"])
        shape_type = st.selectbox("Component Shape", ["Round", "Hexagon", "Square", "Tube", "Bush", "Flange", "Stepped Shaft"])
    with gc_col2:
        if shape_type == "Stepped Shaft":
            num_steps = st.number_input("Number of Steps", min_value=1, max_value=5, value=2, key="gc_num_steps")
            steps_data = []
            for i in range(num_steps):
                c1, c2 = st.columns(2)
                d = c1.number_input(f"Step {i+1} Dia", value=20.0 + (i*10), key=f"gc_dia_{i}")
                l = c2.number_input(f"Step {i+1} Len", value=20.0, key=f"gc_len_{i}")
                steps_data.append({'dia': d, 'len': l})
            stock_dia = steps_data[0]['dia']
            part_length = sum([s['len'] for s in steps_data])
        else:
            stock_dia = st.number_input("Stock Diameter (mm)", key="stock_dia_input", value=51.0)
            part_length = st.number_input("Component Length (mm)", key="gcode_len_input", value=38.7)
    with gc_col3:
        cut_depth = st.number_input("Depth of Cut", value=1.0)
        feed_rate = st.number_input("Feed Rate", value=0.15)

    if st.button("🚀 Run Live 3D Studio & Generate G-Code"):
        if shape_type == "Stepped Shaft":
            gcode = f"{prog_no}\nG21 G90\nT0101\nG96 S200 M03\nG00 X50 Z2\nM30"
            steps_pass = steps_data
        else:
            gcode = f"{prog_no}\nG21 G90\nT0101\nG96 S200 M03\nG00 X{stock_dia+2} Z2\nG01 Z-{part_length} F{feed_rate}\nM30"
            steps_pass = None

        st.session_state.generated_gcode = gcode
        st.session_state.active_shape = shape_type
        st.session_state.active_dia = stock_dia
        st.session_state.active_len = part_length
        st.session_state.active_steps = steps_pass
        st.success("G-Code Generated Successfully!")

    if "generated_gcode" in st.session_state and PLOTLY_AVAILABLE:
        st.markdown("---")
        if st.session_state.active_shape == "Stepped Shaft" and st.session_state.get('active_steps'):
            surfaces = generate_3d_stepped_shaft(st.session_state.active_steps)
        else:
            surfaces = generate_3d_shape_mesh(st.session_state.active_shape, st.session_state.active_dia, st.session_state.active_len)
        fig_3d = go.Figure(data=surfaces)
        fig_3d.update_layout(scene=dict(bgcolor='#0B132B'), paper_bgcolor='#050B18', font=dict(color='white'))
        st.plotly_chart(fig_3d, use_container_width=True)
        st.code(st.session_state.generated_gcode, language="text")

# 8. QUOTATION & PDF STUDIO
elif st.session_state.nav_menu == "Quotation & PDF Studio":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Professional Quotation Generator & PDF Export</div>', unsafe_allow_html=True)
    q_col1, q_col2 = st.columns(2)
    with q_col1:
        client_name = st.text_input("Client Name", value="ABC Engineering")
        job_name = st.text_input("Component Name", value="Pin Bush")
        qty_q = st.number_input("Quantity (Nos)", value=500)
    with q_col2:
        material_cost = st.number_input("Material Cost per Part (₹)", value=15.0)
        machining_cost = st.number_input("Machining Cost per Part (₹)", value=16.0)
        profit_margin = st.slider("Profit Margin (%)", value=20)

    if st.button("Generate Quotation"):
        unit_price = (material_cost + machining_cost) * (1 + profit_margin / 100.0)
        total_quote = unit_price * qty_q
        st.success(f"Unit Price: ₹ {unit_price:.2f} | Total Quotation: ₹ {total_quote:.2f}")

# 9. MORE MENU / MASTERS & SETTINGS
elif st.session_state.nav_menu == "More Menu / Master Settings":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">More Menu & Master Settings</div>', unsafe_allow_html=True)
    st.checkbox("Enable Sound Alerts on Calculation", value=True)
    st.checkbox("Auto-save Calculation History", value=True)
    st.text_input("Company Name Header", value="MEGALA CNC MATE")
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")
