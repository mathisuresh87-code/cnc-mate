import base64
import io
import math
import os
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import plotly.graph_objects as go

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
if "calc_results" not in st.session_state:
    st.session_state.calc_results = None
if "part_length" not in st.session_state:
    st.session_state.part_length = 122.5
if "stock_dia" not in st.session_state:
    st.session_state.stock_dia = 25.0
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
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4; margin-bottom: 5px;">Welcome to Megala CNC Mate 👋</div>', unsafe_allow_html=True)
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
        st.markdown('<div class="metric-card">🛠️<div style="font-weight:700; margin-top:8px;">G-Code Generator</div></div>', unsafe_allow_html=True)
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

# 2. ROD & TUBE CALCULATOR WITH LIVE 3D VISUALIZATION
elif st.session_state.nav_menu == "Rod & Tube Calculator":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Rod & Tube Calculator (3D Live Pro)</div>', unsafe_allow_html=True)

    def get_kg_per_meter(dia, shape):
        if dia <= 0: return 0.0
        if shape == "Round": return (dia**2) / 162
        elif shape == "Square": return (dia**2) / 127
        elif shape == "Hexagon": return (dia**2) / 147
        return (dia**2) / 162

    col1, col2 = st.columns(2)
    with col1:
        rod_type = st.selectbox("Rod Shape", ["Round", "Hexagon", "Square", "Tube"])
        rod_dia = st.number_input("Rod Diameter / Across Flats (mm)", min_value=0.0, value=25.0, step=0.5)
        unit_type = st.selectbox("Input Unit", ["Meter", "Kilogram"])
        rod_length_input = st.number_input("Input Value (Length in Meters OR Weight in Kg)", min_value=0.0, value=1.0, step=0.1)
        shift_hours = st.number_input("Working Hours per Shift / Day", min_value=0.0, value=8.0, step=0.5)
    with col2:
        part_length = st.number_input("Part Length (mm)", min_value=0.0, value=float(st.session_state.part_length), step=0.1, key="part_len_input")
        cutting_allowance = st.number_input("Cutting & Facing Allowance (mm)", min_value=0.0, value=3.0, step=0.1)
        required_qty = st.number_input("Required Quantity (Nos)", min_value=0, value=100, step=1)
        cycle_sec = st.number_input("Cycle Time (Seconds)", min_value=0.0, value=25.0, step=0.5)

    if st.button("Calculate & Render Live 3D Preview"):
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
            "parts_per_rod": parts_per_rod,
            "end_bit_mm": end_bit_mm,
            "required_rods": required_rods,
            "total_stock_len": total_stock_len,
            "prod_per_hr": prod_per_hr,
            "total_machine_time": total_machine_time,
            "total_days": total_days,
            "shift_hours": shift_hours,
            "prod_per_shift": prod_per_shift,
            "equivalent_kg": equivalent_kg,
            "total_rod_meters": total_rod_meters,
            "unit_type": unit_type,
            "rod_dia": rod_dia,
            "part_length": part_length
        }

    if st.session_state.calc_results is not None:
        res = st.session_state.calc_results
        st.markdown("---")
        st.subheader("🌐 Live 3D Interactive Part & Rod Visualizer")
        
        # Generate 3D Cylinder using Plotly for live visualization
        r_val = res["rod_dia"] / 2.0
        h_val = res["part_length"]
        theta = np.linspace(0, 2 * np.pi, 30)
        z_vals = np.linspace(0, h_val, 10)
        Theta, Z_grid = np.meshgrid(theta, z_vals)
        X_grid = r_val * np.cos(Theta)
        Y_grid = r_val * np.sin(Theta)

        fig = go.Figure(data=[go.Surface(x=X_grid, y=Y_grid, z=Z_grid, colorscale='Viridis', showscale=False)])
        fig.update_layout(
            title=f"3D Preview of Component (Diameter: {res['rod_dia']}mm, Length: {res['part_length']}mm)",
            scene=dict(
                xaxis_title='X (mm)',
                yaxis_title='Y (mm)',
                zaxis_title='Length Z (mm)',
                bgcolor='#0B132B'
            ),
            paper_bgcolor='#050B18',
            font=dict(color='white'),
            margin=dict(l=0, r=0, b=0, t=40)
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("📊 Calculation & Production Report Summary")
        st.info(f"🔄 **Conversion Details:** Equivalent Length: **{res['total_rod_meters']:.2f} Meters** | Equivalent Weight: **{res['equivalent_kg']:.2f} Kg**")

        r1, r2, r3 = st.columns(3)
        r1.success(f"**Parts / Rod:** {res['parts_per_rod']} Nos")
        r2.warning(f"**End Bit / Scrap:** {res['end_bit_mm']:.2f} mm")
        r3.success(f"**Required Rods:** {res['required_rods']} Nos")

        st.markdown("---")
        st.subheader("⏱️ Time & Scheduling Breakdown")
        t1, t2, t3 = st.columns(3)
        t1.info(f"**Total Machine Time:** {res['total_machine_time']:.2f} Hours")
        t2.info(f"**Estimated Days ({res['shift_hours']} hrs/day):** {res['total_days']:.2f} Days")
        t3.info(f"**Production Rate:** {res['prod_per_hr']} parts/hr (~ {res['prod_per_shift']} parts/shift)")

# 3. TRAUB COLLET, BAR FEED, RPM CALCULATOR & TROUBLESHOOTING MASTER
elif st.session_state.nav_menu == "Traub Collet & Bar Feed":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Traub Collet, Bar Feed, RPM & Troubleshooting Master</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #94A3B8; font-size: 13px; margin-bottom: 15px;">Calculate collet clearance, spindle RPM speed, follow step-by-step setup, and fix machine problems.</div>', unsafe_allow_html=True)

    t_col1, t_col2 = st.columns(2)
    with t_col1:
        traub_model = st.selectbox("Traub Machine Model", ["A15 / A25", "A32", "A42 / A60", "TD16 / TD26", "TNS"])
        collet_type = st.selectbox("Collet Profile", ["Round Collet (DIN 6343 / 144E)", "Hexagon Collet", "Square Collet", "Dead Length Collet"])
        raw_bar_dia = st.number_input("Raw Bar Diameter / Across Flats (mm)", min_value=1.0, value=16.0, step=0.5)
    with t_col2:
        tolerance_option = st.selectbox(
            "Bar Stock Tolerance Grade", 
            ["h6", "h7", "h8", "h9 (Standard Bright Bar)", "h10", "h11", "K12", "Custom / Manual Clearance"]
        )
        if "Custom" in tolerance_option:
            clearance = st.number_input("Enter Custom Clearance / Tolerance (mm)", min_value=0.0, value=0.05, step=0.01)
        else:
            if "h6" in tolerance_option or "h7" in tolerance_option:
                clearance = 0.02
            elif "h8" in tolerance_option or "h9" in tolerance_option:
                clearance = 0.05
            else:
                clearance = 0.10

        cutting_speed_vc = st.number_input("Cutting Speed (Vc in m/min) [For RPM Calc]", min_value=10.0, value=100.0, step=5.0)
        remnant_length = st.number_input("Target Remnant / End Piece Length (mm)", min_value=10.0, value=45.0, step=5.0)

    if st.button("Calculate Traub Collet & Spindle RPM"):
        recommended_collet_size = raw_bar_dia + clearance
        calculated_rpm = int((cutting_speed_vc * 1000) / (math.pi * raw_bar_dia)) if raw_bar_dia > 0 else 0
        
        st.markdown("---")
        st.subheader("⚙️ Traub Setup & Speed Recommendations")
        sc1, sc2, sc3 = st.columns(3)
        sc1.success(f"**Recommended Collet Bore:** {recommended_collet_size:.2f} mm")
        sc2.info(f"**Calculated Spindle RPM:** {calculated_rpm} RPM")
        sc3.warning(f"**Max Remnant Limit:** {remnant_length} mm")

    st.markdown("---")
    st.markdown("### 📚 Traub Learning & Troubleshooting Guide")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["1. ராட் & ஃபீடர் செட்", "2. காலெட் மாட்டுவது", "3. பார் ஸ்டாப் செட்டிங்", "4. டூல் செட்டிங்", "5. ⚠️ மிஷின் பிராப்ளம் & தீர்வு"])
    with tab1:
        st.markdown("* **படி 1:** உங்கள் மெஷின் மாடலுக்கு ஏற்ற ராடை ஸ்பிண்டில் குழாய்க்குள் செலுத்தவும்.\n* **படி 2:** Bar Feeder அல்லது கிராவிடேஷன் வெயிட் சரியாக உள்ளதா எனச் சரிபார்க்கவும்.")
    with tab2:
        st.markdown("* **படி 1:** ஸ்பிண்டில் முனையில் உள்ள Collet Cap-ஐக் கழற்றவும்.\n* **படி 2:** சரியான அளவுள்ள காலெட்டைப் பொருத்தவும்.")
    with tab3:
        st.markdown("* **படி 1:** Bar Stop டூலை ஸ்லைடில் பொருத்தவும்.\n* **படி 2:** நீளத்தை அளந்து துல்லியமாக அட்ஜஸ்ட் செய்யவும்.")
    with tab4:
        st.markdown("* **படி 1:** ஃபேசிங் டூலை ராட்டின் முகப்பில் சென்டரில் செட் செய்யவும்.")
    with tab5:
        st.markdown("* **பிரச்சனை 1: ராட் நழுவுவது** -> காலெட்டைத் துடைத்து டைட் செய்யவும்.")

# 4. PRODUCTION & CYCLE TIME
elif st.session_state.nav_menu == "Production & Cycle Time":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Production & Cycle Time Analyzer</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        machine_type = st.selectbox("Machine Type", ["CNC Lathe", "Traub Machine", "Drill Machine", "VMC"])
        operation_type = st.selectbox("Operation", ["Facing", "Turning", "Threading", "Tapping", "Drilling"])
        cycle_time_p = st.number_input("Cycle Time per Part (sec)", min_value=0.0, value=20.0)
    with col2:
        avail_time = st.number_input("Total Working Hours", min_value=0.0, value=12.0, step=0.5)
        machine_eff = st.slider("Machine Efficiency (%)", min_value=10, max_value=100, value=85)
        break_time = st.number_input("Break Time (min)", min_value=0, value=30)

    if st.button("Calculate Production Output"):
        effective_hours = avail_time - (break_time / 60.0) if avail_time > 0 else 0
        prod_per_hr = int((3600 / cycle_time_p) * (machine_eff / 100.0)) if cycle_time_p > 0 else 0
        prod_per_day = int(prod_per_hr * effective_hours) if effective_hours > 0 else 0
        st.markdown("---")
        c1, c2 = st.columns(2)
        c1.success(f"### Production / Hour: **{prod_per_hr} Nos**")
        c2.success(f"### Production for {avail_time} Hours: **{prod_per_day} Nos**")

# 5. STOCK MANAGEMENT
elif st.session_state.nav_menu == "Stock Management":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Stock Management System</div>', unsafe_allow_html=True)
    st.session_state.stock_db = st.data_editor(st.session_state.stock_db, num_rows="dynamic", use_container_width=True)

# 6. ADVANCED G-CODE GENERATOR
elif st.session_state.nav_menu == "Advanced G-Code Generator":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Advanced G-Code Generator & Operation Explainer</div>', unsafe_allow_html=True)
    uploaded_drawing = st.file_uploader("📁 Upload Part Drawing / Blueprint", type=["png", "jpg", "jpeg", "webp", "pdf"], key="gcode_drawing_upload")
    if uploaded_drawing is not None:
        st.success("Drawing loaded successfully!")

    gc_col1, gc_col2 = st.columns(2)
    with gc_col1:
        prog_no = st.text_input("Program Number", value="O1001")
        machine_target = st.selectbox("Select Target Machine", ["CNC Lathe (Fanuc / Siemens)", "Traub Automatic Lathe", "CNC Drilling / VMC Machine"])
        stock_dia = st.number_input("Stock / Raw Diameter (mm)", value=25.0)
        fin_dia = st.number_input("Finished Diameter (mm)", value=20.0)
    with gc_col2:
        cut_depth = st.number_input("Depth of Cut per Pass (mm)", value=1.0)
        feed_rate = st.number_input("Feed Rate (mm/rev)", value=0.15)
        drill_depth = st.number_input("Drill Hole Depth (mm)", value=15.0)
        operation_notes = st.text_area("Operation Details", value="Facing -> Turning -> Parting")

    if st.button("Generate G-Code & Operations Report"):
        gcode_content = f"{prog_no}\nG21 G90 G40 G80\nT0101\nG96 S200 M03\nG00 X{stock_dia + 2.0} Z2.0\nM30"
        st.code(gcode_content, language="text")

# 7. QUOTATION & PDF
elif st.session_state.nav_menu == "Quotation & PDF":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Professional Quotation Generator & PDF Export</div>', unsafe_allow_html=True)
    client_name = st.text_input("Client Name", value="ABC Engineering")
    job_name = st.text_input("Job Name", value="Pin Bush")
    qty_q = st.number_input("Quantity (Nos)", min_value=1, value=500)
    if st.button("Generate Quotation"):
        st.success(f"Quotation generated for {client_name}!")

# 8. MORE MENU / MASTERS & SETTINGS
elif st.session_state.nav_menu == "More Menu / Master Settings":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">More Menu & Masters</div>', unsafe_allow_html=True)
    st.checkbox("Enable Sound Alerts", value=True)
    st.text_input("Company Name Header", value="MEGALA CNC MATE")
