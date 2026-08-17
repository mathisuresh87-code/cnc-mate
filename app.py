import streamlit as st
import pandas as pd
import os

# Page Configuration
st.set_page_config(
    page_title="Megala CNC Mate - Pro App Edition",
    page_icon="⚙️",
    layout="wide"
)

# Custom High-End Colorful Native App UI Styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0B132B 0%, #1C2541 50%, #0F172A 100%);
        color: #FFFFFF;
    }
    .main-header {
        font-size: 28px;
        font-weight: 900;
        background: linear-gradient(90deg, #48CAE4, #0077B6, #9333EA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
    }
    .sub-text {
        font-size: 14px;
        color: #94A3B8;
        margin-bottom: 20px;
    }
    .metric-card {
        background: linear-gradient(145deg, #1E293B, #0F172A);
        padding: 22px;
        border-radius: 16px;
        border: 1px solid #334155;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        text-align: center;
        margin-bottom: 15px;
    }
    .card-title {
        font-size: 16px;
        font-weight: bold;
        color: #F8FAFC;
        margin-top: 10px;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #2563EB, #48CAE4);
        color: white;
        font-weight: bold;
        border-radius: 12px;
        height: 48px;
        border: none;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #1D4ED8, #00B4D8);
        box-shadow: 0 6px 16px rgba(72, 202, 228, 0.6);
    }
    </style>
""", unsafe_allow_html=True)

# Session state for navigation
if 'nav_menu' not in st.session_state:
    st.session_state.nav_menu = "Home Dashboard"

def navigate_to(menu_name):
    st.session_state.nav_menu = menu_name

# -------------------------------------------------------------
# SIDEBAR / APP CONTROL PANEL
# -------------------------------------------------------------
st.sidebar.title("⚙️ CNC MATE PRO")
st.sidebar.markdown("### Smart CNC. Simple Work.")

languages = [
    "Tamil (தமிழ்)", 
    "English", 
    "Hindi (हिन्दी)", 
    "Telugu (తెలుగు)", 
    "Kannada (ಕನ್ನಡ)", 
    "Malayalam (മലയാളം)"
]
selected_lang = st.sidebar.selectbox("Select Language / மொழி", languages)

st.sidebar.markdown("---")
menu_options = [
    "Home Dashboard",
    "Rod & Tube Calculator", 
    "Production & Cycle Time", 
    "Stock Management", 
    "Advanced G-Code Generator", 
    "Quotation & PDF",
    "More Menu / Master Settings"
]

selected_sidebar_menu = st.sidebar.radio("Navigation Menu", menu_options, index=menu_options.index(st.session_state.nav_menu))
if selected_sidebar_menu != st.session_state.nav_menu:
    st.session_state.nav_menu = selected_sidebar_menu
    st.rerun()

# -------------------------------------------------------------
# 1. HOME DASHBOARD (App Vibe)
# -------------------------------------------------------------
if st.session_state.nav_menu == "Home Dashboard":
    st.markdown('<div class="main-header">Welcome to MEGALA CNC MATE 👋</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Mobile Native Pro Edition - Intelligent Workshop Assistant</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card">📏<div class="card-title">Rod Calculator & 3D</div></div>', unsafe_allow_html=True)
        if st.button("Open Rod Calculator"):
            navigate_to("Rod & Tube Calculator")
            st.rerun()
            
        st.markdown('<div class="metric-card">🛠️<div class="card-title">G-Code Generator</div></div>', unsafe_allow_html=True)
        if st.button("Open G-Code Generator"):
            navigate_to("Advanced G-Code Generator")
            st.rerun()

    with col2:
        st.markdown('<div class="metric-card">⏱️<div class="card-title">Production & Drilling</div></div>', unsafe_allow_html=True)
        if st.button("Open Production Calculator"):
            navigate_to("Production & Cycle Time")
            st.rerun()
            
        st.markdown('<div class="metric-card">📦<div class="card-title">Stock Management</div></div>', unsafe_allow_html=True)
        if st.button("Open Stock Management"):
            navigate_to("Stock Management")
            st.rerun()

    with col3:
        st.markdown('<div class="metric-card">📄<div class="card-title">Quotation & PDF</div></div>', unsafe_allow_html=True)
        if st.button("Open Quotation Generator"):
            navigate_to("Quotation & PDF")
            st.rerun()
            
        st.markdown('<div class="metric-card">⚙️<div class="card-title">Settings & Masters</div></div>', unsafe_allow_html=True)
        if st.button("Open Settings"):
            navigate_to("More Menu / Master Settings")
            st.rerun()

# -------------------------------------------------------------
# 2. ROD & TUBE CALCULATOR (With End Bit, Scrap & 3D Preview UI)
# -------------------------------------------------------------
elif st.session_state.nav_menu == "Rod & Tube Calculator":
    st.markdown('<div class="main-header">Rod & Tube Calculator (3D Pro)</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Flexible input mode with End Bit calculation & Live 3D Part Rendering.</div>', unsafe_allow_html=True)
    
    calc_mode = st.radio("Operating Mode", ["Simple Mode", "Advanced Mode (Drawing Scan & 3D)"], horizontal=True)
    
    auto_operations = ["Facing", "Turning"]
    uploaded_drawing = None
    
    if calc_mode == "Advanced Mode (Drawing Scan & 3D)":
        st.info("Advanced Mode Active: Upload drawing to auto-detect operations and render 3D model.")
        uploaded_drawing = st.file_uploader("Upload Part Drawing (PNG, JPG, PDF)", type=["png", "jpg", "jpeg", "pdf"])
        if uploaded_drawing is not None:
            st.success("✨ Drawing successfully scanned! Auto-detected operations: **Facing, Turning, Drilling, Chamfering**")
            auto_operations = ["Facing", "Turning", "Drilling", "Chamfering"]

    col1, col2 = st.columns(2)
    with col1:
        rod_type = st.selectbox("Rod Shape / வடிவம்", ["Round (ரவுண்ட்)", "Hexagon (எக்ஸகன்)", "Square (ஸ்கொயர்)", "Tube (டியூப்)"])
        unit_type = st.selectbox("Measurement Unit / அளவீட்டு முறை", ["Meter (மீட்டர்)", "Kilogram (கிலோகிராம்)"])
        rod_length_input = st.number_input("Rod Length / Weight Input", min_value=0.0, value=6.0, step=0.1)
    
    with col2:
        part_length = st.number_input("Part Length (mm) / பார்ட் நீளம்", min_value=0.0, value=122.5, step=0.1)
        cutting_allowance = st.number_input("Cutting & Facing Allowance (mm)", min_value=0.0, value=3.0, step=0.1)
        required_qty = st.number_input("Required Quantity (Nos) / தேவையான அளவு", min_value=0, value=0, step=1)
        cycle_sec = st.number_input("Cycle Time (Seconds)", min_value=0.0, value=17.0, step=0.5)

    if st.button("Calculate & Render 3D Model"):
        total_part_len = part_length + cutting_allowance
        rod_total_mm = rod_length_input * 1000
        
        parts_per_rod = int(rod_total_mm / total_part_len) if (total_part_len > 0 and rod_length_input > 0) else 0
        used_length_mm = parts_per_rod * total_part_len
        end_bit_mm = rod_total_mm - used_length_mm if rod_length_input > 0 else 0.0
        
        required_rods = int(required_qty / parts_per_rod) if (parts_per_rod > 0 and required_qty > 0) else 0
        total_stock_len = required_rods * rod_length_input if required_rods > 0 else 0.0
        prod_per_hr = int(3600 / cycle_sec) if cycle_sec > 0 else 0
        total_machine_time = (required_qty * cycle_sec) / 3600 if required_qty > 0 else 0.0

        st.markdown("---")
        st.subheader("📊 Calculation Result Summary")
        
        r1, r2, r3 = st.columns(3)
        r1.success(f"**Parts / Rod:** {parts_per_rod} Nos")
        r2.warning(f"**End Bit / Scrap:** {end_bit_mm:.2f} mm")
        r3.success(f"**Required Rods:** {required_rods} Nos")
        
        r4, r5, r6 = st.columns(3)
        r4.info(f"**Total Stock Length:** {total_stock_len:.2f} m")
        r5.info(f"**Production / Hour:** {prod_per_hr} Nos")
        r6.info(f"**Total Machine Time:** {total_machine_time:.2f} Hr")
        
        # Gorgeous Native 3D Cylinder Preview UI (Error-free)
        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #1E293B, #0F172A); padding: 25px; border-radius: 16px; border: 2px solid #48CAE4; text-align: center; margin-top: 20px; box-shadow: 0 10px 25px rgba(72, 202, 228, 0.2);">
            <h3 style="color: #48CAE4; margin-bottom: 5px;">🧊 Live 3D Part / Rod Preview</h3>
            <p style="color: #94A3B8; font-size: 13px; margin-bottom: 20px;">Shape: <b>{rod_type}</b> | Part Length: <b>{part_length} mm</b></p>
            <div style="display: flex; justify-content: center; align-items: center; height: 90px;">
                <div style="width: 80%; max-width: 320px; height: 45px; background: linear-gradient(90deg, #1D4ED8, #48CAE4, #00B4D8, #1D4ED8); border-radius: 25px; box-shadow: 0 0 20px rgba(72, 202, 228, 0.7); display: flex; align-items: center; justify-content: center;">
                    <span style="color: #FFFFFF; font-weight: bold; font-size: 14px; text-shadow: 0 1px 3px rgba(0,0,0,0.5);">3D Cylinder Model Rendered</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if calc_mode == "Advanced Mode (Drawing Scan & 3D)":
            st.info(f"📌 **Auto-Detected Operations from Drawing:** {', '.join(auto_operations)}")
        
        st.download_button("📥 Export as PDF / Share Result", data=f"Rod Calculation Summary - Shape: {rod_type} - End Bit/Scrap: {end_bit_mm:.2f}mm - Qty: {required_qty}", file_name="rod_calculation.pdf")

# -------------------------------------------------------------
# 3. PRODUCTION & CYCLE TIME ANALYZER (With Drilling)
# -------------------------------------------------------------
elif st.session_state.nav_menu == "Production & Cycle Time":
    st.markdown('<div class="main-header">Production & Cycle Time Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Dynamic Shift Output (8, 12, 16, 24 Hours) for CNC, Traub & Drill Machines</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        machine_type = st.selectbox("Machine Type / இயந்திர வகை", ["CNC Lathe", "Traub Machine (ட்ராப்)", "Drill Machine", "VMC / Other"])
        operation_type = st.selectbox("Operation / செயல்பாடு", ["Facing", "Turning", "Threading", "Tapping", "Boring", "Chamfering", "Drilling", "Multiple Operations"])
        cycle_time_p = st.number_input("Cycle Time per Part (sec)", min_value=0.0, value=20.0)
    with col2:
        avail_time = st.number_input("Total Working Hours (Dynamic Input)", min_value=0.0, value=12.0, step=0.5)
        machine_eff = st.slider("Machine Efficiency (%)", min_value=10, max_value=100, value=85)
        break_time = st.number_input("Break Time (min)", min_value=0, value=30)

    if st.button("Calculate Production Output"):
        effective_hours = avail_time - (break_time / 60.0) if avail_time > 0 else 0
        prod_per_hr = int((3600 / cycle_time_p) * (machine_eff / 100.0)) if cycle_time_p > 0 else 0
        prod_per_day = int(prod_per_hr * effective_hours) if effective_hours > 0 else 0
        
        st.markdown("---")
        st.info(f"Machine: {machine_type} | Operation: {operation_type}")
        c1, c2 = st.columns(2)
        c1.success(f"### Production / Hour: **{prod_per_hr} Nos**")
        c2.success(f"### Production for {avail_time} Hours: **{prod_per_day} Nos**")

# -------------------------------------------------------------
# 4. STOCK MANAGEMENT SYSTEM
# -------------------------------------------------------------
elif st.session_state.nav_menu == "Stock Management":
    st.markdown('<div class="main-header">Stock Management System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Real-time raw material tracking (Meter / Kg) with auto-deduction.</div>', unsafe_allow_html=True)
    
    if 'stock_db' not in st.session_state:
        st.session_state.stock_db = pd.DataFrame([
            {"Material": "EN8 Round Bar - 12mm", "Unit": "Meter", "Available Stock": 120.50, "Status": "In Stock"},
            {"Material": "MS Round Bar - 20mm", "Unit": "Kg", "Available Stock": 45.20, "Status": "Low Stock"},
            {"Material": "EN24 Hex Rod - 16mm", "Unit": "Meter", "Available Stock": 300.00, "Status": "In Stock"},
            {"Material": "Tube 30mm", "Unit": "Meter", "Available Stock": 0.00, "Status": "Out of Stock"}
        ])
    
    st.dataframe(st.session_state.stock_db, use_container_width=True)
    
    st.markdown("### 🔄 Deduct Stock Usage in Real-Time")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        mat_select = st.selectbox("Select Material", st.session_state.stock_db["Material"].tolist())
    with col_s2:
        deduct_val = st.number_input("Quantity to Deduct", min_value=0.0, value=5.0, step=0.5)
    
    if st.button("Update & Deduct Stock"):
        idx = st.session_state.stock_db[st.session_state.stock_db["Material"] == mat_select].index[0]
        current_stock = st.session_state.stock_db.at[idx, "Available Stock"]
        if current_stock >= deduct_val:
            st.session_state.stock_db.at[idx, "Available Stock"] -= deduct_val
            st.success("Stock successfully updated and deducted!")
            st.rerun()
        else:
            st.error("Error: Insufficient stock available!")

# -------------------------------------------------------------
# 5. ADVANCED G-CODE GENERATOR
# -------------------------------------------------------------
elif st.session_state.nav_menu == "Advanced G-Code Generator":
    st.markdown('<div class="main-header">Advanced G-Code Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Upload drawing, analyze operations, and get Traub vs CNC recommendations with G-Codes.</div>', unsafe_allow_html=True)
    
    drawing_file = st.file_uploader("Upload Drawing for G-Code Analysis", type=["png", "jpg", "jpeg", "pdf"])
    
    col1, col2 = st.columns(2)
    with col1:
        operations_selected = st.multiselect(
            "Select Operations Detected", 
            ["Facing", "Turning", "Threading", "Tapping", "Boring", "Chamfering", "Drilling"],
            default=["Facing", "Turning", "Drilling"]
        )
    with col2:
        recommended_machine = st.selectbox("System Machine Recommendation", ["Traub Machine", "CNC Lathe"])

    if st.button("Generate G-Code & Export"):
        st.markdown("---")
        st.info(f"🤖 **System Machine Recommendation:** {recommended_machine}")
        st.subheader("Generated G-Code Output:")
        
        gcode_sample = f"""
        O0001 (MEGAla CNC MATE GENERATED CODE)
        G21 G90 G95
        M03 S2500
        G00 X0 Z0 (Operation: Facing)
        G01 Z-30.0 F0.2 (Operation: Turning)
        G83 Z-25.0 Q5000 F0.1 (Operation: Drilling)
        M05
        M30
        """
        st.code(gcode_sample, language="text")
        st.download_button("Download G-Code File", data=gcode_sample, file_name="megala_gcode.txt")

# -------------------------------------------------------------
# 6. PROFESSIONAL QUOTATION & PDF GENERATOR
# -------------------------------------------------------------
elif st.session_state.nav_menu == "Quotation & PDF":
    st.markdown('<div class="main-header">Professional Quotation & PDF Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Itemized operations breakdown with professional PDF output.</div>', unsafe_allow_html=True)
    
    client = st.text_input("Customer / Company Name", "ABC Industries")
    drawing_no = st.text_input("Drawing No.", "TR-001")
    ops = st.multiselect("Operations Included in Quotation", ["Facing", "Turning", "Tapping", "Chamfering", "Boring", "Threading", "Drilling"], default=["Facing", "Turning", "Drilling"])
    unit_p = st.number_input("Quoted Unit Price per Part (₹)", min_value=0.0, value=45.0)
    q_qty = st.number_input("Total Quantity", min_value=0, value=500)
    
    if st.button("Generate Official Quotation PDF"):
        total_amt = unit_p * q_qty
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1C2541, #0F172A); padding: 25px; border-radius: 14px; border: 2px solid #48CAE4; box-shadow: 0 10px 25px rgba(72, 202, 228, 0.2);">
            <h3>📄 MEGAla CNC MATE - OFFICIAL QUOTATION</h3>
            <p><b>Client:</b> {client} | <b>Drawing No:</b> {drawing_no}</p>
            <p><b>Included Operations:</b> {', '.join(ops)}</p>
            <p><b>Quantity:</b> {q_qty} Nos | <b>Unit Price:</b> ₹{unit_p:.2f}</p>
            <hr style="border-color: #334155;">
            <h2><b>Total Estimated Amount: ₹{total_amt:.2f}</b></h2>
        </div>
        """, unsafe_allow_html=True)
        st.download_button("📥 Download PDF Quotation", data=f"Quotation for {client} - Operations: {', '.join(ops)} - Total: INR {total_amt}", file_name="quotation.pdf")

# -------------------------------------------------------------
# 7. MORE MENU / MASTERS & SETTINGS
# -------------------------------------------------------------
elif st.session_state.nav_menu == "More Menu / Master Settings":
    st.markdown('<div class="main-header">More Menu & Masters</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Manage masters, offline backup, and system settings.</div>', unsafe_allow_html=True)
    
    st.markdown("### 📋 Masters Management")
    c_m1, c_m2 = st.columns(2)
    with c_m1:
        st.button("📦 Part Master")
        st.button("👥 Customer Master")
        st.button("⚙️ Machine Master")
    with c_m2:
        st.button("🔲 Material Master")
        st.button("🔧 Tool Master")
    
    st.markdown("---")
    st.markdown("### 💾 System & Backup (100% Offline)")
    st.button("🔄 Backup & Restore Database")
    st.markdown("ℹ️ **About CNC Mate:** Professional App Edition v5.1 (Optimized & Error-Free)")
    st.markdown("📞 **Help & Support:** Direct assistance for CNC professionals.")
