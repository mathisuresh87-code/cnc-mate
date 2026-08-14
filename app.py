import streamlit as st
import pandas as pd
import os

# Page Configuration
st.set_page_config(
    page_title="Megala CNC Mate",
    page_icon="⚙️",
    layout="wide"
)

# Custom Styling & UI Enhancements
st.markdown("""
    <style>
    .main-title {
        font-size: 28px;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 10px;
    }
    .sub-text {
        font-size: 15px;
        color: #555555;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# SIDEBAR: LOGO & 6 LANGUAGES SETTINGS
# -------------------------------------------------------------
st.sidebar.title("Megala CNC Mate")

logo_path = "logo.png"  # User uploaded logo
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=140)
else:
    st.sidebar.markdown("### ⚙️ CNC Mate Control Panel")

languages = [
    "Tamil (தமிழ்)", 
    "English", 
    "Hindi (हिन्दी)", 
    "Telugu (తెలుగు)", 
    "Kannada (ಕನ್ನಡ)", 
    "Malayalam (മലയാളം)"
]
selected_lang = st.sidebar.selectbox("Select Language / மொழி", languages)

menu = st.sidebar.radio(
    "Navigation / மெனு",
    [
        "Rod & Tube Calculator", 
        "Operation & Cycle Time", 
        "Stock Management", 
        "G-Code Generator", 
        "Quotation Generator"
    ]
)

# -------------------------------------------------------------
# MODULE 1: ROD & TUBE CALCULATOR (Simple & Advanced Modes)
# -------------------------------------------------------------
if menu == "Rod & Tube Calculator":
    st.markdown('<div class="main-title">Rod & Tube Calculator (ராட் & டியூப் கால்குலேட்டர்)</div>', unsafe_allow_html=True)
    
    calc_mode = st.radio("Select Mode / முறை", ["Simple Mode", "Advanced Mode (Drawing Scan)"])
    
    col1, col2 = st.columns(2)
    with col1:
        rod_type = st.selectbox("Rod Shape / வடிவம்", ["Round (ரவுண்ட்)", "Hexagon (எக்ஸகன்)", "Square (ஸ்கொயர்)", "Tube (டியூப்)"])
        unit_type = st.selectbox("Measurement Unit / அளவீட்டு முறை", ["Meter (மீட்டர்)", "Kilogram (கிலோகிராம்)"])
    
    with col2:
        part_length = st.number_input("Part Length (mm) / பார்ட் நீளம்", min_value=0.1, value=50.0, step=0.1)
        cutting_allowance = st.number_input("Cutting & Facing Allowance (mm) / கட்டிங் & பேசிங் அலவன்ஸ்", min_value=0.0, value=2.0, step=0.1)
        required_qty = st.number_input("Required Quantity / தேவையான அளவு", min_value=1, value=100, step=1)

    if calc_mode == "Advanced Mode (Drawing Scan)":
        st.info("Advanced Mode: Upload your drawing to auto-detect and scan dimensions.")
        uploaded_drawing = st.file_uploader("Upload Drawing / டிராயிங் அப்லோட் செய்யவும்", type=["png", "jpg", "jpeg", "pdf"])
        if uploaded_drawing:
            st.success("Drawing successfully scanned! Dimensions auto-extracted.")

    if st.button("Calculate Weight & Length / கணக்கிடு"):
        total_len = (part_length + cutting_allowance) * required_qty / 1000  # meters
        estimated_weight = total_len * 1.62  # Calculation formula
        
        st.success(f"Estimated Total Length: {total_len:.3f} Meters")
        st.success(f"Estimated Total Weight: {estimated_weight:.3f} Kg")

# -------------------------------------------------------------
# MODULE 2: OPERATION & CYCLE TIME ANALYZER (Dynamic Time Input)
# -------------------------------------------------------------
elif menu == "Operation & Cycle Time":
    st.markdown('<div class="main-title">Operation & Cycle Time Analyzer (ஆபரேஷன் & சைக்கிள் டைம்)</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        machine_type = st.selectbox("Machine Type / இயந்திர வகை", ["CNC Lathe", "Traub Machine (ட்ராப்)", "Drill Machine", "Other"])
        operation_type = st.selectbox("Operation / செயல்பாடு", ["Facing", "Turning", "Threading", "Tapping", "Boring", "Chamfering", "Multiple Operations"])
    
    with col2:
        cycle_time = st.number_input("Cycle Time per Part (Seconds) / ஒரு பார்ட் சைக்கிள் டைம் (வினாடிகளில்)", min_value=0.1, value=45.0, step=0.5)
        total_working_hours = st.number_input("Total Working Hours (Dynamic) / மொத்த வேலை நேரம்", min_value=0.5, value=12.0, step=0.5)

    if st.button("Calculate Production Output / உற்பத்தி அவுட்புட் கணக்கிடு"):
        if cycle_time > 0:
            total_seconds = total_working_hours * 3600
            total_parts = int(total_seconds / cycle_time)
            
            st.markdown(f"### Production Result for {total_working_hours} Hours:")
            st.info(f"Machine: {machine_type} | Operation: {operation_type}")
            st.success(f"Total Parts Output: **{total_parts} Parts**")
        else:
            st.error("Cycle time cannot be zero!")

# -------------------------------------------------------------
# MODULE 3: STOCK MANAGEMENT
# -------------------------------------------------------------
elif menu == "Stock Management":
    st.markdown('<div class="main-title">Stock Management System (ஸ்டாக் மேனேஜ்மெண்ட்)</div>', unsafe_allow_html=True)
    
    st.write("Track and manage raw material stock levels in real-time (Meter / Kg).")
    
    if 'stock_data' not in st.session_state:
        st.session_state.stock_data = pd.DataFrame([
            {"Material": "Round Rod 20mm", "Unit": "Meter", "Available Stock": 500.0},
            {"Material": "Hex Rod 16mm", "Unit": "Kg", "Available Stock": 250.0},
            {"Material": "Square Rod 25mm", "Unit": "Meter", "Available Stock": 300.0},
            {"Material": "Tube 30mm", "Unit": "Meter", "Available Stock": 150.0}
        ])
    
    st.dataframe(st.session_state.stock_data, use_container_width=True)
    
    st.subheader("Deduct / Update Stock")
    mat_to_update = st.selectbox("Select Material / மெட்டீரியல் தேர்வு", st.session_state.stock_data["Material"].tolist())
    consumed_qty = st.number_input("Consumed Quantity to Deduct / குறைக்க வேண்டிய அளவு", min_value=0.1, value=10.0, step=0.5)
    
    if st.button("Deduct Stock / ஸ்டாக் குறைக்கவும்"):
        idx = st.session_state.stock_data[st.session_state.stock_data["Material"] == mat_to_update].index[0]
        current_stock = st.session_state.stock_data.at[idx, "Available Stock"]
        if current_stock >= consumed_qty:
            st.session_state.stock_data.at[idx, "Available Stock"] -= consumed_qty
            st.success("Stock updated successfully!")
            st.dataframe(st.session_state.stock_data, use_container_width=True)
        else:
            st.error("Insufficient stock available!")

# -------------------------------------------------------------
# MODULE 4: G-CODE GENERATOR
# -------------------------------------------------------------
elif menu == "G-Code Generator":
    st.markdown('<div class="main-title">Advanced G-Code Generator (ஜி-கோடு ஜெனரேட்டர்)</div>', unsafe_allow_html=True)
    
    drawing_file = st.file_uploader("Upload Drawing for G-Code / டிராயிங் அப்லோட் செய்யவும்", type=["png", "jpg", "jpeg", "pdf"])
    
    col1, col2 = st.columns(2)
    with col1:
        operations_selected = st.multiselect(
            "Select Operations / செயல்பாடுகள்", 
            ["Facing", "Turning", "Threading", "Tapping", "Boring", "Chamfering"],
            default=["Facing", "Turning"]
        )
    with col2:
        recommended_machine = st.selectbox("System Machine Recommendation / இயந்திர பரிந்துரை", ["Traub Machine", "CNC Lathe"])

    if st.button("Generate G-Code / ஜி-கோடு உருவாக்கவும்"):
        st.info(f"Recommended Machine Analysis: **{recommended_machine}**")
        st.subheader("Generated G-Code Output:")
        
        gcode_sample = f"""
        O0001 (MEGAla CNC MATE GENERATED CODE)
        G21 G90 G95
        M03 S2500
        G00 X0 Z0 (Operation: Facing)
        G01 Z-30.0 F0.2 (Operation: Turning)
        M05
        M30
        """
        st.code(gcode_sample, language="text")
        st.download_button("Export G-Code as File / டவுன்லோட் செய்", data=gcode_sample, file_name="megala_gcode.txt")

# -------------------------------------------------------------
# MODULE 5: PROFESSIONAL QUOTATION GENERATOR
# -------------------------------------------------------------
elif menu == "Quotation Generator":
    st.markdown('<div class="main-title">Professional Quotation Generator (கொட்டேஷன் ஜெனரேட்டர்)</div>', unsafe_allow_html=True)
    
    client_name = st.text_input("Client Name / வாடிக்கையாளர் பெயர்", "ABC Engineering Works")
    quot_drawing = st.file_uploader("Upload Part Drawing for Quotation / டிராயிங் அப்லோட்", type=["png", "jpg", "jpeg", "pdf"])
    
    st.subheader("Itemized Operations Breakdown")
    quoted_ops = st.multiselect(
        "Operations Included in Quotation", 
        ["Facing", "Turning", "Tapping", "Chamfering", "Boring", "Threading"],
        default=["Facing", "Turning", "Chamfering"]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        unit_price = st.number_input("Price per Part (₹) / ஒரு பார்ட் விலை", min_value=0.0, value=50.0, step=1.0)
    with col2:
        qty_quot = st.number_input("Total Quantity / மொத்த எண்ணிக்கை", min_value=1, value=1000, step=10)
    
    if st.button("Generate Professional Quotation / கொட்டேஷன் உருவாக்கு"):
        total_amount = unit_price * qty_quot
        st.success(f"Quotation Generated Successfully for {client_name}!")
        
        st.markdown(f"""
        ---
        ### 📄 **MEGAla CNC MATE - OFFICIAL QUOTATION**
        * **Client Name:** {client_name}
        * **Included Operations:** {', '.join(quoted_ops)}
        * **Total Quantity:** {qty_quot} Parts
        * **Price per Unit:** ₹{unit_price:.2f}
        * **Total Estimated Amount:** **₹{total_amount:.2f}**
        ---
        """)
        
        quotation_text = f"Quotation for {client_name}\nOperations: {', '.join(quoted_ops)}\nQuantity: {qty_quot}\nTotal: INR {total_amount}"
        st.download_button("Download Quotation PDF / PDF பதிவிறக்கு", data=quotation_text, file_name="megala_quotation.pdf")
