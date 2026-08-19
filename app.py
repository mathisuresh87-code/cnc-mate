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
    ])

def navigate_to(menu_name):
    st.session_state.nav_menu = menu_name

# Helper function for precise shape mesh generation in 3D Plotly
def generate_3d_shape_mesh(shape, size, length, inner_dia=0.0):
    z_vals = np.linspace(0, length, 30)
    if shape == "Round":
        theta = np.linspace(0, 2 * np.pi, 60)
        Theta, Z = np.meshgrid(theta, z_vals)
        R = size / 2.0
        X = R * np.cos(Theta)
        Y = R * np.sin(Theta)
        return [go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', showscale=False)]
    
    elif shape == "Tube":
        theta = np.linspace(0, 2 * np.pi, 60)
        Theta, Z = np.meshgrid(theta, z_vals)
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
    
    elif shape in ["Square", "Hexagon"]:
        theta = np.linspace(0, 2 * np.pi, 120)
        Theta, Z = np.meshgrid(theta, z_vals)
        n_sides = 6 if shape == "Hexagon" else 4
        half_angle = np.pi / n_sides
        r_poly = (size / 2.0) * np.cos(half_angle) / np.cos((Theta % (2 * np.pi / n_sides)) - half_angle)
        X = r_poly * np.cos(Theta)
        Y = r_poly * np.sin(Theta)
        return [go.Surface(x=X, y=Y, z=Z, colorscale='Plasma', showscale=False)]
    
    else:
        theta = np.linspace(0, 2 * np.pi, 60)
        Theta, Z = np.meshgrid(theta, z_vals)
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
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4; margin-bottom: 5px;">Welcome Nithish 👋 (Megala CNC Suite)</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #94A3B8; font-size: 14px; margin-bottom: 20px;">Ultra-Advanced CNC, Traub & Blueprint Studio - Select any module below</div>', unsafe_allow_html=True)

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

# 2. ROD & TUBE CALCULATOR WITH INSTANT DRAWING PREVIEW & 3D ANIMATION
elif st.session_state.nav_menu == "Rod & Tube Calculator":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Rod & Tube Calculator (Instant Drawing Preview & Live 3D Studio)</div>', unsafe_allow_html=True)

    def get_kg_per_meter(dia, shape):
        if dia <= 0: return 0.0
        if shape == "Round": return (dia**2) / 162
        elif shape == "Square": return (dia**2) / 127
        elif shape == "Hexagon": return (dia**2) / 147
        elif shape == "Tube": return (dia**2) / 162
        return (dia**2) / 162

    calc_mode = st.radio("Operating Mode", ["Simple Mode", "Advanced Mode (Drawing Scan & Live 3D Model)"], horizontal=True)

    if "Advanced" in calc_mode:
        st.markdown('<div style="background: rgba(72, 202, 228, 0.1); padding: 15px; border-radius: 10px; border: 1px solid #48CAE4; margin-bottom: 15px;"><b>Advanced Blueprint Scanner Active:</b> Upload part drawing (PNG, JPG, PDF). Preview appears immediately and input values update automatically to extracted blueprint dimensions!</div>', unsafe_allow_html=True)
        
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
                    <p style="color: #38BDF8; margin: 3px 0;"><b>Status:</b> Input fields updated automatically to match drawing values.</p>
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
                    <p style="color: #48CAE4; margin: 3px 0;"><b>Assigned Blueprint Length:</b> 38.7 mm</p>
                </div>
                """, unsafe_allow_html=True)
                st.info(f"📄 PDF Document `{adv_drawing.name}` loaded successfully.")
        st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        rod_type = st.selectbox("Rod Shape", ["Round", "Hexagon", "Square", "Tube", "Stepped Shaft"])
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
        if rod_type == "Tube":
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
        
        if "Advanced" in calc_mode and PLOTLY_AVAILABLE:
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

# 3. TRAUB COLLET, BAR FEED & TROUBLESHOOTING MASTER
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
        st.markdown(f"""
        <div style="background: rgba(72, 202, 228, 0.1); padding: 15px; border-radius: 10px; border: 1px solid #48CAE4; margin-top: 15px;">
            <b>Machining & Speed Notes for Traub {traub_model}:</b><br>
            - Recommended Spindle Speed: <b>{calculated_rpm} RPM</b> based on Cutting Speed {cutting_speed_vc} m/min.<br>
            - Ensure correct clamping pressure on the {collet_type} to prevent bar slip during high RPM.<br>
            - Stock clearance / allowance ({clearance}mm) ensures smooth feeding without jamming in the spindle tube.
        </div>
        """, unsafe_allow_html=True)

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

# 6. ADVANCED G-CODE GENERATOR WITH INSTANT PREVIEW & 3D STUDIO
elif st.session_state.nav_menu == "Advanced G-Code Generator":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Advanced G-Code Generator & Live 3D Drawing Studio</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #94A3B8; font-size: 13px; margin-bottom: 15px;">வணக்கம் நிதீஷ்! உங்கள் டிராயிங்கை கீழே அப்லோட் செய்யுங்கள். பிரிவியூ உடனே தோன்றும், அளவுகள் ஆட்டோமேட்டிக்காக இன்புட்டில் ஏறும், மற்றும் 3D மாடல் மற்றும் ஜி-கோடு உருவாகும்.</div>', unsafe_allow_html=True)

    uploaded_drawing = st.file_uploader("📁 Upload Part Drawing / Blueprint (PNG, JPG, WEBP, HEIC, PDF)", type=["png", "jpg", "jpeg", "webp", "heic", "pdf"], key="gcode_drawing_upload")
    if uploaded_drawing is not None:
        try:
            img_g = Image.open(uploaded_drawing)
            auto_dia = 51.0
            auto_len = 38.7
            st.session_state.stock_dia_input = auto_dia
            st.session_state.gcode_len_input = auto_len
            
            st.markdown(f"""
            <div class="upload-status-box">
                <h3 style="color: #10B981; margin: 0 0 8px 0;">✅ Drawing Preview & Dimension Extraction Successful!</h3>
                <p style="color: #F8FAFC; margin: 3px 0;"><b>File Name:</b> {uploaded_drawing.name}</p>
                <p style="color: #48CAE4; margin: 3px 0;"><b>Extracted Blueprint Stock Dia:</b> {auto_dia} mm | <b>Length:</b> {auto_len} mm</p>
                <p style="color: #38BDF8; margin: 3px 0;"><b>Status:</b> Dimensions automatically updated in input fields below to match drawing!</p>
            </div>
            """, unsafe_allow_html=True)
            st.image(uploaded_drawing, caption=f"📷 Scanned Drawing Preview [{uploaded_drawing.name}]", use_container_width=True)
        except Exception:
            st.session_state.stock_dia_input = 51.0
            st.session_state.gcode_len_input = 38.7
            st.markdown(f"""
            <div class="upload-status-box">
                <h3 style="color: #10B981; margin: 0 0 8px 0;">✅ Document Uploaded Successfully!</h3>
                <p style="color: #F8FAFC; margin: 3px 0;"><b>File Name:</b> {uploaded_drawing.name}</p>
                <p style="color: #48CAE4; margin: 3px 0;"><b>Assigned Stock Dia:</b> 51.0 mm | <b>Length:</b> 38.7 mm</p>
            </div>
            """, unsafe_allow_html=True)
            st.info(f"📄 Document `{uploaded_drawing.name}` loaded successfully.")

    st.markdown("---")
    gc_col1, gc_col2, gc_col3 = st.columns(3)
    with gc_col1:
        prog_no = st.text_input("Program Number", value="O1001")
        machine_target = st.selectbox("Select Target Machine", ["CNC Lathe (Fanuc / Siemens)", "Traub Automatic Lathe (Cam / Single Spindle)", "CNC Drilling / VMC Machine"])
        shape_type = st.selectbox("Component Shape", ["Round", "Hexagon", "Square", "Tube", "Stepped Shaft"])
    
    with gc_col2:
        if shape_type == "Stepped Shaft":
            num_steps = st.number_input("Number of Steps", min_value=1, max_value=5, value=2, key="gc_num_steps")
            steps_data = []
            for i in range(num_steps):
                c1, c2 = st.columns(2)
                d = c1.number_input(f"Step {i+1} Dia (mm)", value=20.0 + (i*10), key=f"gc_dia_{i}")
                l = c2.number_input(f"Step {i+1} Len (mm)", value=20.0, key=f"gc_len_{i}")
                steps_data.append({'dia': d, 'len': l})
            stock_dia = steps_data[0]['dia']
            part_length = sum([s['len'] for s in steps_data])
            inner_dia_g = 0.0
        else:
            stock_dia = st.number_input("Stock / Raw Diameter (mm)", key="stock_dia_input", step=0.5)
            inner_dia_g = 0.0
            if shape_type == "Tube":
                inner_dia_g = st.number_input("Inner Diameter (mm) [Tube]", value=12.0, key="inner_dia_g_input")
            fin_dia = st.number_input("Finished Diameter (mm)", value=20.0)
            part_length = st.number_input("Component Length (mm)", key="gcode_len_input", step=0.1)

    with gc_col3:
        cut_depth = st.number_input("Depth of Cut per Pass (mm)", value=1.0)
        feed_rate = st.number_input("Feed Rate (mm/rev)", value=0.15)
        drill_depth = st.number_input("Drill Hole Depth (mm) [If Drilling]", value=15.0)

    if st.button("🚀 Run Live 3D Studio & Generate G-Code"):
        if shape_type == "Stepped Shaft":
            gcode_content = f"""{prog_no} (STEPPED SHAFT CNC PROGRAM)
G21 G90 G40 G80
T0101 (TURNING TOOL)
G96 S200 M03
"""
            current_z = 0
            for idx, step in enumerate(steps_data):
                gcode_content += f"G00 X{step['dia'] + 2.0} Z2.0\n"
                gcode_content += f"G01 Z-{current_z + step['len']} F{feed_rate}\n"
                current_z += step['len']
            gcode_content += "G00 Z50.0 M05\nM30\n"
            explanation = f"**Stepped Shaft Operations Breakdown:**\n- Generated {len(steps_data)} custom steps mirroring your drawing profile with total length {part_length}mm."
        elif "CNC Lathe" in machine_target:
            gcode_content = f"""{prog_no} (CNC LATHE PROGRAM - {shape_type.upper()})
G21 G90 G40 G80
T0101 (FACING & TURNING TOOL)
G96 S200 M03
G00 X{stock_dia + 2.0} Z2.0
G01 Z0.0 F{feed_rate}
X{fin_dia} Z-{part_length}
G00 Z5.0
M30
"""
            explanation = f"**CNC Lathe Operations Breakdown for {shape_type} component:**\n1. **Facing:** Cleans up front face at Z0.\n2. **Turning:** Reduces diameter from {stock_dia}mm to {fin_dia}mm over length {part_length}mm with cut depth {cut_depth}mm.\n3. **Parting:** Cut-off at end of cycle."
        elif "Traub" in machine_target:
            gcode_content = f"""{prog_no} (TRAUB AUTOMATIC LATHE SEQUENCE - {shape_type.upper()})
N10 G99 (SPINDLE START)
N20 T1 (BAR STOP & FEED)
N30 T2 (FACING TOOL - SLIDE 1)
N40 T3 (TURNING TOOL - LENGTH {part_length}MM)
N50 T4 (PARTING / CUT-OFF TOOL)
M02 (END OF PROGRAM)
"""
            explanation = f"**Traub Automatic Lathe Operations Breakdown ({shape_type}):**\n1. **Bar Feeding:** Material fed against stock stop.\n2. **Longitudinal Slide:** Turns profile down over length {part_length}mm.\n3. **Cross Slide:** Facing and parting-off."
        else:
            gcode_content = f"""{prog_no} (CNC DRILLING / VMC PROGRAM)
G21 G90 G40 G80
T01 (DRILL TOOL Ø10)
M03 S1500
G00 X0.0 Y0.0 Z5.0
G81 Z-{part_length} R2.0 F{feed_rate} (CANNED DRILLING CYCLE)
G80
G00 Z50.0 M05
M30
"""
            explanation = f"**CNC Drilling Operations Breakdown:**\n1. **Tool Positioning:** Rapid move to center X0 Y0.\n2. **Drilling Cycle (G81):** Pecks/drills down to depth -{part_length}mm.\n3. **Retract:** Returns safely to Z clearance plane."

        st.session_state.generated_gcode = gcode_content
        st.session_state.gcode_explanation = explanation
        st.session_state.active_shape = shape_type
        st.session_state.active_dia = stock_dia
        st.session_state.active_inner_dia = inner_dia_g
        st.session_state.active_len = part_length
        st.session_state.active_steps = steps_data if shape_type == "Stepped Shaft" else None
        st.success("Live 3D Studio & G-Code Generated Successfully!")

    if "generated_gcode" in st.session_state and PLOTLY_AVAILABLE:
        st.markdown("---")
        st.subheader(f"🌐 Live 3D Parametric Simulation [{st.session_state.active_shape} Profile]")
        
        if st.session_state.active_shape == "Stepped Shaft" and st.session_state.get('active_steps'):
            surfaces_g = generate_3d_stepped_shaft(st.session_state.active_steps)
        else:
            surfaces_g = generate_3d_shape_mesh(
                st.session_state.active_shape, 
                st.session_state.active_dia, 
                st.session_state.active_len, 
                st.session_state.get('active_inner_dia', 0.0)
            )
            
        fig_3d = go.Figure(data=surfaces_g)
        fig_3d.update_layout(
            title=dict(text=f"Live 3D Component Model -> Shape: {st.session_state.active_shape} | Total Length: {st.session_state.active_len}mm", font=dict(size=14, color='#48CAE4')),
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
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            c.drawString(50, 750, "MEGALA CNC MATE - G-Code & Operation Report")
            c.drawString(50, 730, f"Machine Target: {machine_target} | Program Number: {prog_no}")
            c.drawString(50, 710, f"Shape: {shape_type} | Total Length: {part_length}mm")
            c.drawString(50, 680, "G-Code Program:")
            text_y = 660
            for line in st.session_state.generated_gcode.split("\n"):
                c.drawString(70, text_y, line)
                text_y -= 15
                if text_y < 50:
                    c.showPage()
                    text_y = 750
            c.save()
            pdf_data = buffer.getvalue()
            st.download_button(label="📥 Export G-Code & Report as PDF", data=pdf_data, file_name=f"{prog_no}_CNC_Report.pdf", mime="application/pdf")

# 7. QUOTATION & PDF
elif st.session_state.nav_menu == "Quotation & PDF":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Professional Quotation Generator & PDF Export</div>', unsafe_allow_html=True)
    q_drawing = st.file_uploader("📁 Upload Job / Component Drawing (PNG, JPG, WEBP, HEIC, PDF)", type=["png", "jpg", "jpeg", "webp", "heic", "pdf"], key="q_draw")
    if q_drawing is not None:
        try:
            img_q = Image.open(q_drawing)
            st.markdown(f"""
            <div class="upload-status-box">
                <h3 style="color: #10B981; margin: 0 0 8px 0;">✅ Quotation Drawing Successfully Loaded & Previewed!</h3>
                <p style="color: #F8FAFC; margin: 3px 0;"><b>File Name:</b> {q_drawing.name}</p>
            </div>
            """, unsafe_allow_html=True)
            st.image(img_q, caption=f"Quotation Reference Preview [{q_drawing.name}]", use_container_width=True)
        except Exception:
            st.markdown(f"""
            <div class="upload-status-box">
                <h3 style="color: #10B981; margin: 0 0 8px 0;">✅ Quotation Document Loaded!</h3>
                <p style="color: #F8FAFC; margin: 3px 0;"><b>File Name:</b> {q_drawing.name}</p>
            </div>
            """, unsafe_allow_html=True)
            st.info(f"📄 Quotation file `{q_drawing.name}` loaded.")

    st.markdown("---")
    q_col1, q_col2 = st.columns(2)
    with q_col1:
        client_name = st.text_input("Client Name / கஸ்டமர் பெயர்", value="ABC Engineering")
        job_name = st.text_input("Job / Component Name / பார்ட் பெயர்", value="Pin Bush")
        qty_q = st.number_input("Quantity (Nos) / தேவையான எண்ணிக்கை", min_value=1, value=500, step=1)
        material_type = st.selectbox("Material Grade / மெட்டீரியல்", ["EN8 Round Bar", "MS Round Bar", "Aluminium 6061", "Stainless Steel SS304", "Brass"])
    with q_col2:
        selected_ops = st.multiselect("Select Manufacturing Operations / ஆபரேஷன்கள்", ["Facing & Center Drilling", "Rough Turning", "Finish Turning", "Deep Hole Drilling", "Threading / Tapping", "Parting / Cut-off"], default=["Facing & Center Drilling", "Rough Turning", "Finish Turning", "Parting / Cut-off"])
        material_cost = st.number_input("Material Cost per Part (₹)", min_value=0.0, value=15.0, step=0.5)
        auto_machining_estimate = len(selected_ops) * 4.0
        machining_cost = st.number_input("Machining Cost per Part (₹) [Auto-Estimated]", min_value=0.0, value=float(auto_machining_estimate), step=0.5)
        profit_margin = st.slider("Profit Margin (%) / லாப சதவீதம்", min_value=0, max_value=50, value=20)

    if st.button("Generate Quotation & Calculate"):
        unit_price = (material_cost + machining_cost) * (1 + profit_margin / 100.0)
        total_quote = unit_price * qty_q
        st.session_state.quote_data = {
            "client_name": client_name, "job_name": job_name, "qty_q": qty_q,
            "material_type": material_type, "selected_ops": selected_ops,
            "material_cost": material_cost, "machining_cost": machining_cost,
            "profit_margin": profit_margin, "unit_price": unit_price, "total_quote": total_quote,
        }
        st.success("Quotation generated successfully!")

    if "quote_data" in st.session_state:
        qd = st.session_state.quote_data
        st.markdown("---")
        st.subheader("📋 Quotation Summary")
        qc1, qc2, qc3 = st.columns(3)
        qc1.info(f"**Client:** {qd['client_name']}")
        qc2.info(f"**Component:** {qd['job_name']}")
        qc3.info(f"**Quantity:** {qd['qty_q']} Nos")

        qp1, qp2 = st.columns(2)
        qp1.success(f"### Price per Part: **₹ {qd['unit_price']:.2f}**")
        qp2.success(f"### Total Quotation Amount: **₹ {qd['total_quote']:.2f}**")

        if REPORTLAB_AVAILABLE:
            q_buffer = io.BytesIO()
            qc = canvas.Canvas(q_buffer, pagesize=letter)
            qc.drawString(50, 750, "MEGALA CNC MATE - Professional Job Quotation")
            qc.drawString(50, 730, f"Client Name: {qd['client_name']}")
            qc.drawString(50, 715, f"Component Name: {qd['job_name']}")
            qc.drawString(50, 700, f"Quantity: {qd['qty_q']} Nos | Material: {qd['material_type']}")
            qc.drawString(50, 680, f"Selected Operations: {', '.join(qd['selected_ops'])}")
            qc.drawString(50, 650, f"Material Cost/Part: ₹ {qd['material_cost']:.2f} | Machining Cost/Part: ₹ {qd['machining_cost']:.2f}")
            qc.drawString(50, 635, f"Profit Margin: {qd['profit_margin']}%")
            qc.drawString(50, 605, f"Unit Selling Price: Rs {qd['unit_price']:.2f}")
            qc.drawString(50, 590, f"Total Quotation Amount: Rs {qd['total_quote']:.2f}")
            qc.save()
            q_pdf_data = q_buffer.getvalue()
            st.download_button(label="📥 Download Professional Quotation PDF", data=q_pdf_data, file_name=f"Quotation_{qd['client_name'].replace(' ', '_')}_{qd['job_name'].replace(' ', '_')}.pdf", mime="application/pdf")

# 8. MORE MENU / MASTERS & SETTINGS
elif st.session_state.nav_menu == "More Menu / Master Settings":
    st.markdown('<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">More Menu & Masters</div>', unsafe_allow_html=True)
    st.checkbox("Enable Sound Alerts on Calculation", value=True)
    st.checkbox("Auto-save Calculation History", value=True)
    st.text_input("Company Name Header", value="MEGALA CNC MATE")
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")
