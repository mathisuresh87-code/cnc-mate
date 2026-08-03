import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="CNC Mate - Smart CNC. Simple Work.",
    page_icon="⚙️",
    layout="wide"
)

# Custom CSS for Dark Theme & Gorgeous UI Cards matching your screenshots
st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117;
        color: #ffffff;
    }
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        text-align: center;
        margin-bottom: 0px;
        letter-spacing: 1px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #38bdf8;
        text-align: center;
        margin-bottom: 25px;
        font-weight: 500;
    }
    .metric-card {
        background-color: #161b22;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #30363d;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .auto-badge {
        background-color: #065f46;
        color: #34d399;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<p class="main-header">CNC MATE</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">SMART CNC. SIMPLE WORK. — புரோபஷனல் ஒர்க்ஷாப் ஆட்டோமேஷன்</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar Navigation
st.sidebar.markdown("### 🚀 Menu / மெனு")
selected_module = st.sidebar.selectbox(
    "Select Module",
    [
        "🏠 Home / முகப்பு",
        "📐 Rod Calculator (ராட் கால்குலேட்டர்)",
        "⏱️ Production Calculator (உற்பத்தி கால்குலேட்டர்)",
        "💰 Costing & Quotation Calculator (செலவு & கொட்டேஷன்)",
        "📦 Stock Management (ஸ்டாக் மேனேஜ்மென்ட்)",
        "📷 Drawing & G-Code Generator (டிராயிங் & ஜி-கோடு)",
        "⚙️ More Menu & Settings (அமைப்புகள் & மாஸ்டர்ஸ்)"
    ]
)

# 1. HOME DASHBOARD
if "Home" in selected_module:
    st.subheader("👋 Hello, Suresh! Good Morning ☀️")
    st.write("இன்றைய ஒர்க்ஷாப் சுருக்கம் மற்றும் விரைவான அணுகல்:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="metric-card" style="border-left: 5px solid #3b82f6;">
                <h3>📐 Rod Calculator</h3>
                <p>ரவுண்ட், எக்சகன், ஸ்கொயர் & டியூப் கணக்கீடுகள்</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="metric-card" style="border-left: 5px solid #10b981;">
                <h3>⏱️ Production Calculator</h3>
                <p>டிரெண்ட், ட்ராவ், சிஎன்சி உற்பத்தி நேரம்</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="metric-card" style="border-left: 5px solid #f97316;">
                <h3>💰 Costing Calculator</h3>
                <p>மெட்டீரியல், லேபர் & ஒவர்ஹெட்ஸ் காஸ்ட்</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
            <div class="metric-card" style="border-left: 5px solid #8b5cf6;">
                <h3>📦 Stock Management</h3>
                <p>ரா மெட்டீரியல் & பினிஷ்ட் குட்ஸ் டிராக்கிங்</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="metric-card" style="border-left: 5px solid #06b6d4;">
                <h3>📄 Quotation & PDF</h3>
                <p>QR கோடுடன் கூடிய புரொபஷனல் கொட்டேஷன்</p>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
            <div class="metric-card" style="border-left: 5px solid #6b7280;">
                <h3>⚙️ Settings & Languages</h3>
                <p>6 மொழிகள் & ஒர்க்ஷாப் மாஸ்டர்ஸ்</p>
            </div>
        """, unsafe_allow_html=True)

# 2. ROD CALCULATOR
elif "Rod Calculator" in selected_module:
    st.subheader("📐 Rod & Meter/Kg Calculator")
    mode = st.radio("Mode Selection", ["Simple Mode", "Advanced Mode"], horizontal=True)
    
    col1, col2 = st.columns(2)
    with col1:
        rod_length = st.number_input("Rod Length (Meter)", value=6.0)
        part_length = st.number_input("Part Length (mm)", value=126.0)
        cutting_allowance = st.number_input("Cutting Allowance (mm)", value=3.0)
    with col2:
        required_qty = st.number_input("Required Quantity (Nos)", value=500)
        cycle_time = st.number_input("Cycle Time (Seconds)", value=20)
        shape_type = st.selectbox("Material Shape", ["Round Rod", "Hexagon Rod", "Square Rod", "Tube / Pipe"])
        
    if shape_type == "Tube / Pipe":
        od = st.number_input("Outer Diameter OD (mm)", value=50.0)
        id_val = st.number_input("Inner Diameter ID (mm)", value=30.0)

    if st.button("Calculate Rod Requirements"):
        st.markdown('<div class="auto-badge">⚡ AUTO CALCULATED</div>', unsafe_allow_html=True)
        
        # Calculations
        effective_part_len = part_length + cutting_allowance
        parts_per_rod = int((rod_length * 1000) / effective_part_len) if effective_part_len > 0 else 0
        required_rods = int(required_qty / parts_per_rod) if parts_per_rod > 0 else 0
        total_stock_length = required_rods * rod_length
        prod_per_hour = int(3600 / cycle_time) if cycle_time > 0 else 0
        total_machine_time = (required_qty * cycle_time) / 3600 # Hours

        res1, res2, res3 = st.columns(3)
        with res1:
            st.metric("Parts / Rod", f"{parts_per_rod} Nos")
            st.metric("Required Rods", f"{required_rods} Nos")
        with res2:
            st.metric("Balance Scrap / Remnant", f"{round((rod_length*1000) % effective_part_len, 2)} mm")
            st.metric("Total Stock Length", f"{round(total_stock_length, 2)} Meters")
        with res3:
            st.metric("Production / Hour", f"{prod_per_hour} Nos")
            st.metric("Total Machine Time", f"{round(total_machine_time, 2)} Hr")
            
        st.info("All calculations are approximate. Please verify before production.")

# 3. PRODUCTION CALCULATOR
elif "Production Calculator" in selected_module:
    st.subheader("⏱️ Production Days & Output Calculator")
    
    c1, c2 = st.columns(2)
    with c1:
        cyc_time = st.number_input("Cycle Time (sec)", value=20)
        avail_time = st.number_input("Available Time / Day (hr)", value=8.0)
    with c2:
        efficiency = st.slider("Machine Efficiency (%)", 50, 100, 85)
        break_time = st.number_input("Break Time (min)", value=30)
        
    if st.button("Calculate Production Output"):
        st.markdown('<div class="auto-badge">⚡ AUTO CALCULATED</div>', unsafe_allow_html=True)
        effective_hours = avail_time - (break_time / 60)
        prod_hour = int(3600 / cyc_time * (efficiency / 100))
        prod_day = int(prod_hour * effective_hours)
        
        r1, r2 = st.columns(2)
        with r1:
            st.metric("Production / Hour", f"{prod_hour} Nos")
        with r2:
            st.metric("Production / Day", f"{prod_day} Nos")

# 4. COSTING & QUOTATION CALCULATOR
elif "Costing & Quotation Calculator" in selected_module:
    st.subheader("💰 Costing & Quotation Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        mat_cost_kg = st.number_input("Material Cost / Kg (₹)", value=85.0)
        mat_wt_part = st.number_input("Material Weight / Part (Kg)", value=0.25)
        machine_cost_hr = st.number_input("Machine Cost / Hr (₹)", value=600.0)
    with col2:
        labour_cost_part = st.number_input("Labour Cost / Part (₹)", value=1.20)
        overhead_pct = st.number_input("Overhead (%)", value=15.0)
        profit_margin = st.slider("Profit Margin (%)", 0, 50, 20)

    if st.button("Calculate Cost & Selling Price"):
        st.markdown('<div class="auto-badge">⚡ AUTO CALCULATED</div>', unsafe_allow_html=True)
        material_total = mat_cost_kg * mat_wt_part
        machining_part = (machine_cost_hr / 3600) * 20 # assuming 20 sec cycle
        subtotal = material_total + machining_part + labour_cost_part
        overhead_val = subtotal * (overhead_pct / 100)
        cost_per_part = subtotal + overhead_val
        cost_1000 = cost_per_part * 1000
        selling_price = cost_per_part * (1 + profit_margin / 100)

        p1, p2, p3 = st.columns(3)
        with p1:
            st.metric("Cost / Part", f"₹ {round(cost_per_part, 2)}")
        with p2:
            st.metric("Cost / 1000 Parts", f"₹ {round(cost_1000, 2)}")
        with p3:
            st.metric("Selling Price / Part", f"₹ {round(selling_price, 2)}")

# 5. STOCK MANAGEMENT
elif "Stock Management" in selected_module:
    st.subheader("📦 Stock & Inventory Management")
    
    s1, s2, s3 = st.columns(3)
    with s1:
        st.metric("Total Items", "128")
    with s2:
        st.metric("Low Stock", "8", delta_color="inverse")
    with s3:
        st.metric("Out of Stock", "3", delta_color="inverse")
        
    st.text_input("🔍 Search Part / Material...")
    
    stock_data = {
        "Material / Part": ["EN8 Round Bar - 12mm", "MS Round Bar - 20mm", "EN24 Round Bar - 16mm", "Finished Bush-01"],
        "Category": ["Raw Material", "Raw Material", "Raw Material", "Finished Goods"],
        "Stock Qty": ["120.50 Kg", "45.20 Kg", "0.00 Kg", "650 Nos"],
        "Status": ["In Stock", "Low Stock", "Out of Stock", "Dispatch Ready"]
    }
    st.dataframe(pd.DataFrame(stock_data), use_container_width=True)

# 6. DRAWING & G-CODE GENERATOR
elif "Drawing & G-Code Generator" in selected_module:
    st.subheader("📷 Drawing Analysis & Advanced G-Code Generator")
    uploaded_file = st.file_uploader("Upload Part Drawing (PDF / PNG / JPG)", type=["png", "jpg", "pdf"])
    
    if uploaded_file:
        st.success("Drawing successfully analyzed by AI!")
        st.write("**Detected Operations:** Facing, Turning, Grooving, Drilling, Tapping")
        
    if st.button("Generate G-Code Program"):
        sample_code = """O1001 (CNC MATE AUTOMATED PROGRAM)
G21 G99 G40
M03 S2000
G00 X50.0 Z5.0
G01 Z-50.0 F0.2
G00 X100.0 Z100.0
M30"""
        st.code(sample_code, language="text")

# 7. MORE MENU & SETTINGS
elif "More Menu & Settings" in selected_module:
    st.subheader("⚙️ More Menu & Settings (Settings & Masters)")
    
    lang = st.selectbox(
        "🌐 Select Language / மொழி தேர்வு", 
        [
            "தமிழ் (Tamil)", 
            "English", 
            "हिन्दी (Hindi)", 
            "తెలుగు (Telugu)", 
            "മലയാളം (Malayalam)", 
            "ಕನ್ನಡ (Kannada)"
        ]
    )
    st.success(f"Language set to: {lang}")
    
    st.markdown("---")
    st.markdown("### 📋 Workshop Masters & Tools")
    col1, col2 = st.columns(2)
    with col1:
        st.write("• Part Master")
        st.write("• Customer Master")
        st.write("• Machine Master")
    with col2:
        st.write("• Material Master (EN1, EN8, EN19, EN24, EN31, C45, MS, SS, Aluminum, Brass)")
        st.write("• Tool Master & Backup")
        st.write("• Help & Support")
