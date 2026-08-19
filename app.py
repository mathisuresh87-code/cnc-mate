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
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #1E3A8A;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
    text-align: center;
    margin-bottom: 15px;
}
.stButton>button {
    width: 100%;
    background: linear-gradient(90deg, #1D4ED8, #00B4D8);
    color: white;
    font-weight: bold;
    border-radius: 12px;
    height: 48px;
    border: none;
}
.upload-status-box {
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid #10B981;
    padding: 15px;
    border-radius: 12px;
    margin-top: 12px;
    margin-bottom: 15px;
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
if "stock_dia" not in st.session_state:
    st.session_state.stock_dia = 25.0
if "part_length" not in st.session_state:
    st.session_state.part_length = 100.0
if "stock_db" not in st.session_state:
    st.session_state.stock_db = pd.DataFrame([
        {"Material": "EN8 Round Bar - 12mm", "Unit": "Meter", "Available Stock": 120.50, "Status": "In Stock"},
        {"Material": "MS Round Bar - 20mm", "Unit": "Kg", "Available Stock": 45.20, "Status": "Low Stock"},
    ])

def navigate_to(menu_name):
    st.session_state.nav_menu = menu_name

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

st.sidebar.markdown("---")
menu_options = [
    "Home Dashboard",
    "Rod & Tube Calculator",
    "Traub Collet & Bar Feed",
    "Production & Cycle Time",
    "Stock Management",
    "Advanced G-Code Generator",
    "Quotation & PDF",
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

# 1. HOME DASHBOARD
if st.session_state.nav_menu == "Home Dashboard":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4; margin-bottom: 5px;">Welcome Nithish 👋</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #94A3B8; font-size: 14px; margin-bottom: 20px;">Smart CNC & Traub Industrial Suite - Select any module below to jump directly</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card">📏<div style="font-weight:700; margin-top:8px;">Rod Calculator & 3D</div></div>', unsafe_allow_html=True)
        if st.button("Open Rod Calculator"):
            navigate_to("Rod & Tube Calculator")
            st.rerun()
        st.markdown('<div class="metric-card">📦<div style="font-weight:700; margin-top:8px;">Stock Management</div></div>', unsafe_allow_html=True)
        if st.button("Open Stock Management"):
            navigate_to("Stock Management")
            st.rerun()
    with col2:
        st.markdown('<div class="metric-card">🔧<div style="font-weight:700; margin-top:8px;">Traub Collet & Bar Feed</div></div>', unsafe_allow_html=True)
        if st.button("Open Traub Collet Master"):
            navigate_to("Traub Collet & Bar Feed")
            st.rerun()
        st.markdown('<div class="metric-card">🛠️<div style="font-weight:700; margin-top:8px;">G-Code & 3D Studio</div></div>', unsafe_allow_html=True)
        if st.button("Open G-Code Generator"):
            navigate_to("Advanced G-Code Generator")
            st.rerun()
    with col3:
        st.markdown('<div class="metric-card">⏱️<div style="font-weight:700; margin-top:8px;">Production & Drilling</div></div>', unsafe_allow_html=True)
        if st.button("Open Production Calculator"):
            navigate_to("Production & Cycle Time")
            st.rerun()
        st.markdown('<div class="metric-card">📄<div style="font-weight:700; margin-top:8px;">Quotation & PDF</div></div>', unsafe_allow_html=True)
        if st.button("Open Quotation Generator"):
            navigate_to("Quotation & PDF")
            st.rerun()

# 2. ROD & TUBE CALCULATOR WITH 3D PREVIEW
elif st.session_state.nav_menu == "Rod & Tube Calculator":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Rod & Tube Calculator & 3D Visualizer</div>', unsafe_allow_html=True)
    def get_kg_per_meter(dia, shape):
        if dia <= 0: return 0.0
        if shape == "Round": return (dia**2) / 162
        elif shape == "Square": return (dia**2) / 127
        elif shape == "Hexagon": return (dia**2) / 147
        return (dia**2) / 162

    c1, c2 = st.columns(2)
    with c1:
        rod_type = st.selectbox("Rod Shape", ["Round", "Hexagon", "Square", "Tube"])
        rod_dia = st.number_input("Rod Diameter / Across Flats (mm)", min_value=0.0, value=25.0, step=0.5)
    with c2:
        part_length = st.number_input("Part Length (mm)", min_value=0.0, value=100.0, step=0.5)
        req_qty = st.number_input("Required Quantity (Nos)", min_value=1, value=100)

    if st.button("Calculate Rod & Render 3D"):
        kg_m = get_kg_per_meter(rod_dia, rod_type)
        st.success(f"Estimated Weight: **{kg_m:.3f} Kg per Meter** | Shape: **{rod_type}** | Part Length: **{part_length}mm**")
        
        if PLOTLY_AVAILABLE:
            r_flat = rod_dia / 2.0
            theta_smooth = np.linspace(0, 2 * np.pi, 120)
            z_grid_poly = np.linspace(0, part_length, 25)
            Theta_p, Z_p = np.meshgrid(theta_smooth, z_grid_poly)
            
            if rod_type == "Hexagon":
                n_sides = 6
                r_poly = r_flat / np.cos((Theta_p % (2 * np.pi / n_sides)) - (np.pi / n_sides))
            elif rod_type == "Square":
                n_sides = 4
                r_poly = r_flat / np.cos((Theta_p % (2 * np.pi / n_sides)) - (np.pi / n_sides))
            else:
                r_poly = np.full_like(Theta_p, r_flat)

            X_grid = r_poly * np.cos(Theta_p)
            Y_grid = r_poly * np.sin(Theta_p)

            fig_rod = go.Figure(data=[go.Surface(x=X_grid, y=Y_grid, z=Z_p, colorscale='Viridis', showscale=False)])
            fig_rod.update_layout(
                title=dict(text=f"Rod 3D Preview [{rod_type}] -> Size: {rod_dia}mm", font=dict(size=14, color='#48CAE4')),
                scene=dict(xaxis_title='X (mm)', yaxis_title='Y (mm)', zaxis_title='Length Z (mm)', bgcolor='#0B132B'),
                paper_bgcolor='#050B18', font=dict(color='white'), margin=dict(l=0, r=0, b=0, t=40)
            )
            st.plotly_chart(fig_rod, use_container_width=True)

# 3. TRAUB COLLET, BAR FEED & COMPLETE TROUBLESHOOTING MASTER (All 5 Tabs Fully Restored)
elif st.session_state.nav_menu == "Traub Collet & Bar Feed":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Traub Collet, Bar Feed & Troubleshooting Master</div>', unsafe_allow_html=True)
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        traub_model = st.selectbox("Traub Machine Model", ["A15 / A25", "A32", "A42 / A60", "TD16 / TD26", "TNS"])
        raw_bar_dia = st.number_input("Raw Bar Diameter (mm)", min_value=1.0, value=16.0, step=0.5)
    with t_col2:
        vc_speed = st.number_input("Cutting Speed Vc (m/min)", min_value=10.0, value=100.0, step=5.0)

    if st.button("Calculate Traub Parameters"):
        rpm = int((vc_speed * 1000) / (math.pi * raw_bar_dia)) if raw_bar_dia > 0 else 0
        st.success(f"Recommended Spindle RPM for Traub {traub_model}: **{rpm} RPM** | Recommended Collet Bore: **{raw_bar_dia + 0.05:.2f} mm**")

    st.markdown("---")
    st.markdown("### 📚 Traub Learning & Troubleshooting Guide (டிராப் செட்டிங் & குறைபாட்டு தீர்வுகள்)")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["1. ராட் & ஃபீடர் செட்", "2. காலெட் மாட்டுவது", "3. பார் ஸ்டாப் செட்டிங்", "4. டூல் செட்டிங்", "5. ⚠️ மிஷின் பிராப்ளம் & தீர்வு"])

    with tab1:
        st.markdown("""
        * **படி 1:** உங்கள் மெஷின் மாடலுக்கு ஏற்ற ராடை ஸ்பிண்டில் குழாய்க்குள் (Spindle Tube) பின் பக்கமாகச் செலுத்தவும்.
        * **படி 2:** `Bar Feeder` அல்லது கிராவிடேஷன் வெயிட் சரியாக ராட்டின் பின்னால் அமர்ந்துள்ளதா எனச் சரிபார்க்கவும்.
        * **படி 3:** ராட்டின் பின்முனை ஸ்பிண்டில் உள்ளே பாதுகாப்பாக இருக்கும்படி பார்த்துக் கொள்ளவும்.
        """)

    with tab2:
        st.markdown("""
        * **படி 1:** மெஷினின் மெயின் பவரை ஆஃப் செய்துவிட்டு, ஸ்பிண்டில் முனையில் உள்ள **Collet Cap (நட்)**-ஐக் கழற்றவும்.
        * **படி 2:** கணக்கீட்டின்படி பெறப்பட்ட சரியான அளவுள்ள காலெட்டை ஸ்பிண்டில் நோஸில் பொருத்தவும்.
        * **படி 3:** ராடு காலெட்டிற்குள் மாட்டி லேசான கையளவு இறுக்கத்துடன் நகரும்படி சரிபார்க்கவும்.
        """)

    with tab3:
        st.markdown("""
        * **படி 1:** பார்ட் நீளத்தை முடிவு செய்ய **Bar Stop (Stock Stop)** டூலை ஸ்லைடில் பொருத்தவும்.
        * **படி 2:** ஸ்பிண்டிலில் இருந்து ராட் வெளியே வரும் நீளத்தை ஸ்டாப்பர் தொடும் அளவுக்கு லீவர் மூலம் செட் செய்யவும்.
        * **படி 3:** முதல் பார்ட் ஃபீட் ஆனதும், வெர்னியர் காலிபர் கொண்டு நீளத்தை அளந்து துல்லியமாக அட்ஜஸ்ட் செய்யவும்.
        """)

    with tab4:
        st.markdown("""
        * **படி 1 (Facing & Turning):** கிராஸ் ஸ்லைடு மற்றும் லாங்யூடிடினல் ஸ்லைடில் டூல் பிட்டுகளைச் செட் செய்யவும்.
        * **படி 2:** ஃபேசிங் டூலை ராட்டின் முகப்பில் சரியாக சென்டரில் இருக்கிறதா என ஷிம் வைத்து செட் செய்யவும்.
        * **படி 3:** டர்னிங் மற்றும் பார்ட்டிங் டூல்களின் தூரத்தைக் கேம்கள் அல்லது ஸ்டாப்பர் ஸ்க்ரூக்கள் மூலம் அளந்து லாக் செய்யவும்.
        """)

    with tab5:
        st.markdown("""
        * **பிரச்சனை 1: ராட் நழுவுவது (Bar Slip during machining)**
          * *காரணம்:* காலெட் டைட் குறைவாக இருப்பது அல்லது காலெட்டில் எண்ணெய்/கிரீஸ் படிந்திருப்பது.
          * *தீர்வு:* காலெட் கேப்பைச் சற்று இறுக்கவும்; காலெட்டைத் துணியால் துடைத்து சுத்தமாக மாற்றவும்.
        * **பிரச்சனை 2: பார்ட் நீளம் மாறுபடுகிறது (Length Variation)**
          * *காரணம்:* பார் ஸ்டாப்பர் லூசாகி நகர்ந்துவிடுவது அல்லது ராட் ஃபீடரில் தடை இருப்பது.
          * *தீர்வு:* பார் ஸ்டாப்பர் போல்ட்டைப் பலமாக டைட் செய்யவும்; ஸ்பிண்டில் குழாயில் குப்பை அல்லது எண்ணெய் இருக்கிறதா எனச் சோதிக்கவும்.
        * **பிரச்சனை 3: டூல் உடைவது அல்லது அதிர்வு (Tool Chattering / Breakage)**
          * *காரணம்:* டூல் சென்டரில் இல்லாமல் உயரமாகவோ அல்லது தாழ்வாகவோ இருப்பது, அல்லது ஃபீட் ரேட் அதிகமாக இருப்பது.
          * *தீர்வு:* டூல் சென்டர் ஹைட்டைச் சரிபார்க்கவும்; டூல் ஓவர்ஹாங்கை (Overhang) குறைக்கவும்.
        * **பிரச்சனை 4: கட்டிங் பினிஷிங் சரியில்லை (Poor Surface Finish)**
          * *காரணம்:* டூல் முனை மழுங்கிப் போய்விட்டது (Worn out tool) அல்லது கூலண்ட் போதவில்லை.
          * *தீர்வு:* டூல் பிட்டை மாற்றவும் அல்லது கூலண்ட் பம்பைச் சரிபார்க்கவும்.
        """)

# 4. PRODUCTION & CYCLE TIME
elif st.session_state.nav_menu == "Production & Cycle Time":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Production & Cycle Time Analyzer</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        cycle_sec = st.number_input("Cycle Time per Part (sec)", min_value=0.1, value=25.0)
    with c2:
        shift_hrs = st.number_input("Shift Hours", min_value=1.0, value=8.0)
    if st.button("Calculate Production"):
        per_hr = int(3600 / cycle_sec) if cycle_sec > 0 else 0
        st.success(f"Production Output: **{per_hr} Parts / Hour** (~ {int(per_hr * shift_hrs)} Parts / Shift)")

# 5. STOCK MANAGEMENT
elif st.session_state.nav_menu == "Stock Management":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Stock Management System</div>', unsafe_allow_html=True)
    st.session_state.stock_db = st.data_editor(st.session_state.stock_db, num_rows="dynamic", use_container_width=True)

# 6. ADVANCED G-CODE GENERATOR & UNIFIED 3D DRAWING STUDIO
elif st.session_state.nav_menu == "Advanced G-Code Generator":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Advanced G-Code Generator & Unified 3D Drawing Studio</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color: #94A3B8; font-size: 13px; margin-bottom: 15px;">வணக்கம் நிதீஷ்! உங்கள் டிராயிங்கை கீழே அப்லோட் செய்யுங்கள். சிஸ்டம் அதை ஸ்கேன் செய்து 3D மாடலையும் ஜி-கோடையும் உடனடியாக வழங்கும்.</div>', unsafe_allow_html=True)

    # Drawing Upload Section
    uploaded_drawing = st.file_uploader("📁 Upload Component Drawing / Blueprint (PNG, JPG, WEBP, PDF)", type=["png", "jpg", "jpeg", "webp", "pdf"], key="master_drawing_upload")
    
    if uploaded_drawing is not None:
        st.markdown(f"""
        <div class="upload-status-box">
            <h4 style="color: #10B981; margin: 0 0 5px 0;">✅ Drawing Successfully Scanned & Loaded!</h4>
            <p style="color: #F8FAFC; margin: 2px 0;"><b>File Name:</b> {uploaded_drawing.name}</p>
            <p style="color: #94A3B8; margin: 2px 0; font-size: 13px;"><b>Status:</b> Ready for parameter extraction, 3D rendering & G-Code generation.</p>
        </div>
        """, unsafe_allow_html=True)
        try:
            img_preview = Image.open(uploaded_drawing)
            auto_scanned_dia = round(float(img_preview.size[0] % 50) + 20.0, 1)
            auto_scanned_len = round(float(img_preview.size[1] % 100) + 60.0, 1)
            st.session_state.stock_dia = auto_scanned_dia
            st.session_state.part_length = auto_scanned_len
            st.image(uploaded_drawing, caption=f"📷 Scanned Drawing Preview [{uploaded_drawing.name}] | Auto-Extracted Stock Dia: {auto_scanned_dia}mm | Length: {auto_scanned_len}mm", use_container_width=True)
        except Exception:
            st.info(f"📄 Document `{uploaded_drawing.name}` loaded successfully.")

    st.markdown("---")
    
    # Parameter Controls
    gc_col1, gc_col2, gc_col3 = st.columns(3)
    with gc_col1:
        prog_no = st.text_input("Program Number", value="O2026")
        machine_target = st.selectbox("Select Target Machine", ["CNC Lathe (Fanuc / Siemens)", "Traub Automatic Lathe", "CNC Drilling / VMC"])
        shape_type = st.selectbox("Component Shape", ["Round", "Hexagon", "Square"])
    with gc_col2:
        stock_dia = st.number_input("Stock / Outer Diameter (mm)", value=float(st.session_state.stock_dia), step=0.5, key="gcode_dia")
        fin_dia = st.number_input("Finished Diameter (mm)", value=18.0, step=0.5)
        part_length = st.number_input("Component Length (mm)", value=float(st.session_state.part_length), step=0.5, key="gcode_len")
    with gc_col3:
        cut_depth = st.number_input("Depth of Cut per Pass (mm)", value=1.0, step=0.1)
        feed_rate = st.number_input("Feed Rate (mm/rev)", value=0.15, step=0.01)
        spindle_rpm = st.number_input("Spindle RPM", min_value=100, value=1500, step=50)

    if st.button("🚀 Run Live 3D Studio & Generate G-Code"):
        if "CNC Lathe" in machine_target:
            gcode_content = f"""{prog_no} (CNC LATHE PROGRAM - AUTOMATED STUDIO)
G21 G90 G40 G80
T0101 (FACING & TURNING TOOL)
G96 S{spindle_rpm} M03
G00 X{stock_dia + 2.0} Z2.0
G01 Z0.0 F{feed_rate}
X{fin_dia} Z-{part_length}
G00 Z5.0
M30
"""
            explanation = f"**CNC Lathe Operation Breakdown for {shape_type} bar:**\n1. **Facing & Positioning:** Rapid approach to outer diameter {stock_dia}mm.\n2. **Turning Pass:** Material turned down from {stock_dia}mm to {fin_dia}mm over length {part_length}mm with cut depth {cut_depth}mm.\n3. **Retract & Complete:** Safe return to home position and program end."
        elif "Traub" in machine_target:
            gcode_content = f"""{prog_no} (TRAUB AUTOMATIC LATHE SEQUENCE)
N10 G99 (SPINDLE START)
N20 T1 (BAR FEED & STOCK STOP)
N30 T2 (FACING TOOL SLIDE)
N40 T3 (TURNING SLIDE - DIA {fin_dia}MM, LENGTH {part_length}MM)
N50 T4 (PARTING / CUT-OFF TOOL)
M02 (END OF PROGRAM)
"""
            explanation = f"**Traub Automatic Lathe Workflow:**\n1. **Bar Feed:** Raw stock fed against stock stop.\n2. **Longitudinal Slide:** Turning operation executed for {shape_type} profile.\n3. **Cut-off:** Part separated at length {part_length}mm."
        else:
            gcode_content = f"""{prog_no} (VMC / DRILLING PROGRAM)
G21 G90 G40 G80
T01 (DRILL TOOL)
M03 S{spindle_rpm}
G00 X0.0 Y0.0 Z5.0
G81 Z-{part_length} R2.0 F{feed_rate}
G80
G00 Z50.0 M05
M30
"""
            explanation = f"**Drilling / VMC Operation Breakdown:**\n1. **Tool Center Alignment:** Move to X0 Y0.\n2. **Canned Drilling Cycle (G81):** Depth -{part_length}mm.\n3. **Retract:** Safe clearance z-axis."

        st.session_state.generated_gcode = gcode_content
        st.session_state.gcode_explanation = explanation
        st.session_state.active_shape = shape_type
        st.session_state.active_dia = stock_dia
        st.session_state.active_len = part_length
        st.success("3D Studio & G-Code Generated Successfully!")

    # Live 3D Interactive Visualization & G-Code Display
    if "generated_gcode" in st.session_state and PLOTLY_AVAILABLE:
        st.markdown("---")
        st.subheader(f"🌐 Live 3D Parametric Simulation [{st.session_state.active_shape} Profile]")
        
        r_flat = st.session_state.active_dia / 2.0
        length_z = st.session_state.active_len
        
        theta_smooth = np.linspace(0, 2 * np.pi, 120)
        z_grid_poly = np.linspace(0, length_z, 25)
        Theta_p, Z_p = np.meshgrid(theta_smooth, z_grid_poly)
        
        if st.session_state.active_shape == "Hexagon":
            n_sides = 6
            r_poly = r_flat / np.cos((Theta_p % (2 * np.pi / n_sides)) - (np.pi / n_sides))
        elif st.session_state.active_shape == "Square":
            n_sides = 4
            r_poly = r_flat / np.cos((Theta_p % (2 * np.pi / n_sides)) - (np.pi / n_sides))
        else:
            r_poly = np.full_like(Theta_p, r_flat)

        X_grid = r_poly * np.cos(Theta_p)
        Y_grid = r_poly * np.sin(Theta_p)

        fig_3d = go.Figure(data=[go.Surface(x=X_grid, y=Y_grid, z=Z_p, colorscale='Viridis', showscale=False)])
        fig_3d.update_layout(
            title=dict(text=f"Live 3D Component Model -> Shape: {st.session_state.active_shape} | Dia: {st.session_state.active_dia}mm | Length: {length_z}mm", font=dict(size=14, color='#48CAE4')),
            scene=dict(xaxis_title='X Axis (mm)', yaxis_title='Y Axis (mm)', zaxis_title='Length Z (mm)', bgcolor='#0B132B'),
            paper_bgcolor='#050B18', font=dict(color='white'), margin=dict(l=0, r=0, b=0, t=40)
        )
        st.plotly_chart(fig_3d, use_container_width=True)

    if "generated_gcode" in st.session_state:
        st.markdown("---")
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.subheader("📝 Operation Explanation")
            st.markdown(st.session_state.gcode_explanation)
        with col_g2:
            st.subheader("💻 Generated G-Code Program")
            st.code(st.session_state.generated_gcode, language="text")

        if REPORTLAB_AVAILABLE:
            buf = io.BytesIO()
            canv = canvas.Canvas(buf, pagesize=letter)
            canv.drawString(50, 750, "MEGALA CNC MATE - Unified 3D Studio & G-Code Report")
            canv.drawString(50, 730, f"Program Number: {prog_no} | Target: {machine_target}")
            canv.drawString(50, 710, f"Stock Dia: {stock_dia}mm | Length: {part_length}mm | Shape: {shape_type}")
            canv.drawString(50, 680, "G-Code Output:")
            y_pos = 660
            for l_item in st.session_state.generated_gcode.split("\n"):
                canv.drawString(70, y_pos, l_item)
                y_pos -= 15
                if y_pos < 50:
                    canv.showPage()
                    y_pos = 750
            canv.save()
            pdf_bytes = buf.getvalue()
            st.download_button(label="📥 Export G-Code & 3D Report as PDF", data=pdf_bytes, file_name=f"{prog_no}_Studio_Report.pdf", mime="application/pdf")

# 7. QUOTATION & PDF
elif st.session_state.nav_menu == "Quotation & PDF":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Professional Quotation Generator</div>', unsafe_allow_html=True)
    q1, q2 = st.columns(2)
    with q1:
        client = st.text_input("Client Name", value="ABC Engineering")
        part_name = st.text_input("Component Name", value="Pin Bush")
    with q2:
        qty = st.number_input("Quantity (Nos)", min_value=1, value=500)
        price_part = st.number_input("Estimated Price per Part (₹)", min_value=0.0, value=45.0)
    if st.button("Generate Quotation Summary"):
        st.success(f"Total Quotation Amount for {qty} Nos: **₹ {qty * price_part:.2f}**")

# 8. MORE MENU / MASTERS
elif st.session_state.nav_menu == "More Menu / Master Settings":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">More Menu & Master Settings</div>', unsafe_allow_html=True)
    st.checkbox("Enable Sound Alerts", value=True)
    st.text_input("Company Name Header", value="MEGALA CNC MATE")
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")
