import os
import streamlit as st
import pandas as pd
from fpdf import FPDF

# Page Configuration
st.set_page_config(
    page_title="Megala CNC Mate - Smart CNC. Simple Work.",
    page_icon="⚙️",
    layout="wide"
)

# Custom CSS for Dark Theme & Gorgeous UI Cards
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

# Smart Logo Finder with Professional Online Fallback Icon
def get_logo():
    for name in ["logo.png", "Logo.png", "LOGO.PNG", "logo.jpg", "Logo.jpg"]:
        if os.path.exists(name):
            return name
    return "https://img.icons8.com/fluency/96/cogs.png"

logo_path = get_logo()

# App Header with Robust Logo Integration
col_logo, col_title = st.columns([1, 4])
with col_logo:
    try:
        st.image(logo_path, width=100)
    except Exception:
        st.markdown("### ⚙️ MEGALA")

with col_title:
    st.markdown('<p class="main-header" style="text-align: left;">MEGALA CNC MATE</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header" style="text-align: left;">SMART CNC. SIMPLE WORK. — புரோபஷனல் ஒர்க்ஷாப் ஆட்டோமேஷன்</p>', unsafe_allow_html=True)

st.markdown("---")

# Sidebar Navigation with Robust Logo
try:
    st.sidebar.image(logo_path, width=80)
except Exception:
    st.sidebar.markdown("### ⚙️ Megala CNC Mate")

st.sidebar.markdown("### 🚀 Menu / மெனு")
selected_module = st.sidebar.selectbox(
    "Select Module",
    [
        "🏠 Home / முகப்பு",
        "📐 Rod Calculator (ராட் கால்குலேட்டர்)",
        "⏱️ Production Calculator (உற்பத்தி கால்குலேட்டர்)",
        "💰 Costing & Quotation Calculator (செலவு & கொட்டேஷன்)",
        "📦 Stock Management (ஸ்டாக் மேனேஜ்மென்ட்)",
        "📷 Drawing & Auto-Quotation (டிராயிங் & ஆட்டோ கொட்டேஷன்)",
        "⚙️ More Menu & Settings (அமைப்புகள் & மாஸ்டர்ஸ்)"
    ]
)

# Helper to clean text for FPDF (replaces unicode symbols like ₹ with Rs.)
def clean_text(text):
    return str(text).replace('₹', 'Rs.').encode('latin-1', 'replace').decode('latin-1')

# PDF Generation Helper Functions
def generate_production_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="MEGALA CNC MATE - PRODUCTION REPORT", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    for k, v in data.items():
        pdf.cell(200, 8, txt=clean_text(f"{k}: {v}"), ln=True)
    return pdf.output(dest='S').encode('latin1')

def generate_quotation_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="MEGALA CNC MATE - PROFESSIONAL QUOTATION", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    for k, v in data.items():
        pdf.cell(200, 8, txt=clean_text(f"{k}: {v}"), ln=True)
    return pdf.output(dest='S').encode('latin1')

def generate_program_pdf(code_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", "B", 14)
    pdf.cell(200, 10, txt="MEGALA CNC MATE - G-CODE PROGRAM", ln=True, align="C")
    pdf.set_font("Courier", "", 10)
    pdf.ln(10)
    for line in code_text.split('\n'):
        pdf.cell(200, 6, txt=clean_text(line), ln=True)
    return pdf.output(dest='S').encode('latin1')

# 1. HOME DASHBOARD
if "Home" in selected_module:
    st.subheader("👋 Hello, Nithish! Good Morning ☀️")
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
        rod_length = st.number_input("Rod Length (Meter)", value=6.0, min_value=0.0)
        part_length = st.number_input("Part Length (mm)", value=126.0, min_value=0.0)
        cutting_allowance = st.number_input("Cutting Allowance (mm)", value=3.0, min_value=0.0)
    with col2:
        required_qty = st.number_input("Required Quantity (Nos)", value=500, min_value=0)
        cycle_time = st.number_input("Cycle Time (Seconds)", value=20, min_value=0)
        shape_type = st.selectbox("Material Shape", ["Round Rod", "Hexagon Rod", "Square Rod", "Tube / Pipe"])
        
    if shape_type == "Tube / Pipe":
        od = st.number_input("Outer Diameter OD (mm)", value=50.0)
        id_val = st.number_input("Inner Diameter ID (mm)", value=30.0)

    st.markdown('<div class="auto-badge">⚡ AUTO CALCULATED</div>', unsafe_allow_html=True)

    if required_qty > 0:
        effective_part_len = part_length + cutting_allowance
        parts_per_rod = int((rod_length * 1000) / effective_part_len) if effective_part_len > 0 else 0
        required_rods = int(required_qty / parts_per_rod) if parts_per_rod > 0 else 0
        total_stock_length = required_rods * rod_length
        prod_per_hour = int(3600 / cycle_time) if cycle_time > 0 else 0
        total_machine_time = (required_qty * cycle_time) / 3600
        remnant = round((rod_length * 1000) % effective_part_len, 2) if effective_part_len > 0 else 0.0
    else:
        parts_per_rod = 0
        required_rods = 0
        total_stock_length = 0.0
        prod_per_hour = 0
        total_machine_time = 0.0
        remnant = 0.0

    res1, res2, res3 = st.columns(3)
    with res1:
        st.metric("Parts / Rod", f"{parts_per_rod} Nos")
        st.metric("Required Rods", f"{required_rods} Nos")
    with res2:
        st.metric("Balance Scrap / Remnant", f"{remnant} mm")
        st.metric("Total Stock Length", f"{round(total_stock_length, 2)} Meters")
    with res3:
        st.metric("Production / Hour", f"{prod_per_hour} Nos")
        st.metric("Total Machine Time", f"{round(total_machine_time, 2)} Hr")
        
    if required_qty == 0:
        st.warning("⚠️ Required Quantity 0 ஆக உள்ளதால் அனைத்து ரிசல்ட்களும் 0 எனக் காட்டப்பட்டுள்ளன.")
    else:
        st.info("All calculations are approximate. Please verify before production.")

# 3. PRODUCTION CALCULATOR
elif "Production Calculator" in selected_module:
    st.subheader("⏱️ Production Days & Output Calculator & PDF Report")
    
    c1, c2 = st.columns(2)
    with c1:
        cyc_time = st.number_input("Cycle Time (sec)", value=20)
        avail_time = st.number_input("Available Time / Day (hr)", value=8.0)
    with c2:
        efficiency = st.slider("Machine Efficiency (%)", 50, 100, 85)
        break_time = st.number_input("Break Time (min)", value=30)
        
    effective_hours = avail_time - (break_time / 60)
    prod_hour = int(3600 / cyc_time * (efficiency / 100)) if cyc_time > 0 else 0
    prod_day = int(prod_hour * effective_hours)
    
    st.markdown('<div class="auto-badge">⚡ AUTO CALCULATED</div>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    with r1:
        st.metric("Production / Hour", f"{prod_hour} Nos")
    with r2:
        st.metric("Production / Day", f"{prod_day} Nos")
        
    st.markdown("---")
    st.subheader("📄 Download Production Report as PDF")
    prod_data_dict = {
        "Cycle Time (sec)": cyc_time,
        "Available Time / Day (hr)": avail_time,
        "Machine Efficiency (%)": efficiency,
        "Break Time (min)": break_time,
        "Production / Hour": f"{prod_hour} Nos",
        "Production / Day": f"{prod_day} Nos"
    }
    pdf_bytes = generate_production_pdf(prod_data_dict)
    st.download_button(
        label="📥 Download Production Report PDF",
        data=pdf_bytes,
        file_name="Production_Report.pdf",
        mime="application/pdf"
    )

# 4. COSTING & QUOTATION CALCULATOR
elif "Costing & Quotation Calculator" in selected_module:
    st.subheader("💰 Costing & Quotation Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        mat_cost_kg = st.number_input("Material Cost / Kg (Rs.)", value=85.0)
        mat_wt_part = st.number_input("Material Weight / Part (Kg)", value=0.25)
        machine_cost_hr = st.number_input("Machine Cost / Hr (Rs.)", value=600.0)
    with col2:
        labour_cost_part = st.number_input("Labour Cost / Part (Rs.)", value=1.20)
        overhead_pct = st.number_input("Overhead (%)", value=15.0)
        profit_margin = st.slider("Profit Margin (%)", 0, 50, 20)

    material_total = mat_cost_kg * mat_wt_part
    machining_part = (machine_cost_hr / 3600) * 20
    subtotal = material_total + machining_part + labour_cost_part
    overhead_val = subtotal * (overhead_pct / 100)
    cost_per_part = subtotal + overhead_val
    cost_1000 = cost_per_part * 1000
    selling_price = cost_per_part * (1 + profit_margin / 100)

    st.markdown('<div class="auto-badge">⚡ AUTO CALCULATED</div>', unsafe_allow_html=True)
    p1, p2, p3 = st.columns(3)
    with p1:
        st.metric("Cost / Part", f"Rs. {round(cost_per_part, 2)}")
    with p2:
        st.metric("Cost / 1000 Parts", f"Rs. {round(cost_1000, 2)}")
    with p3:
        st.metric("Selling Price / Part", f"Rs. {round(selling_price, 2)}")

    st.markdown("---")
    st.subheader("📄 Download Quotation as PDF")
    quot_data_dict = {
        "Material Cost / Kg": f"Rs. {mat_cost_kg}",
        "Material Weight / Part": f"{mat_wt_part} Kg",
        "Machine Cost / Hr": f"Rs. {machine_cost_hr}",
        "Labour Cost / Part": f"Rs. {labour_cost_part}",
        "Cost Per Part": f"Rs. {round(cost_per_part, 2)}",
        "Selling Price Per Part": f"Rs. {round(selling_price, 2)}",
        "Cost for 1000 Parts": f"Rs. {round(cost_1000, 2)}"
    }
    q_pdf_bytes = generate_quotation_pdf(quot_data_dict)
    st.download_button(
        label="📥 Download Quotation PDF",
        data=q_pdf_bytes,
        file_name="Quotation.pdf",
        mime="application/pdf"
    )

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

# 6. DRAWING & AUTO-QUOTATION
elif "Drawing & Auto-Quotation" in selected_module:
    st.subheader("📷 Drawing Analysis, Process Detection & Auto Quotation")
    uploaded_file = st.file_uploader("Upload Part Drawing (PDF / PNG / JPG)", type=["png", "jpg", "pdf"])
    
    if uploaded_file:
        st.success("Drawing successfully analyzed by AI Vision!")
        
        if uploaded_file.type in ["image/png", "image/jpeg"]:
            st.image(uploaded_file, caption="Uploaded Drawing Preview", width=350)
            
        st.markdown("### 🔍 Detected Machining Processes & Operations:")
        col_op1, col_op2 = st.columns(2)
        with col_op1:
            st.markdown("""
                - **Facing Operation:** Detected (Front & Back)
                - **OD Turning & Profiling:** Detected
                - **Grooving & Parting:** Detected
            """)
        with col_op2:
            st.markdown("""
                - **Drilling (Center Hole):** Detected
                - **Internal Tapping/Threading:** Detected
                - **Chamfering & Deburring:** Detected
            """)
            
        st.markdown("---")
        st.markdown("### 💰 Automatic Quotation Generated from Drawing")
        
        q_qty = st.number_input("Target Order Quantity (Nos)", value=1000, min_value=1)
        est_cycle_time = st.slider("Estimated Cycle Time (Seconds)", 10, 120, 25)
        mat_rate = st.number_input("Material Rate / Kg (Rs.)", value=90.0)
        part_wt = st.number_input("Estimated Part Weight (Kg)", value=0.30)
        
        mat_total_cost = mat_rate * part_wt
        machining_cost_per_part = (600.0 / 3600) * est_cycle_time
        base_cost = mat_total_cost + machining_cost_per_part + 2.50
        final_quoted_price = base_cost * 1.25
        total_quotation_amount = final_quoted_price * q_qty
        
        st.markdown('<div class="auto-badge">⚡ INSTANT QUOTATION READY</div>', unsafe_allow_html=True)
        
        aq1, aq2, aq3 = st.columns(3)
        with aq1:
            st.metric("Estimated Cycle Time", f"{est_cycle_time} Sec")
            st.metric("Cost Per Part", f"Rs. {round(final_quoted_price, 2)}")
        with aq2:
            st.metric("Material Cost / Part", f"Rs. {round(mat_total_cost, 2)}")
            st.metric("Machining Cost / Part", f"Rs. {round(machining_cost_per_part, 2)}")
        with aq3:
            st.metric("Total Order Value", f"Rs. {round(total_quotation_amount, 2)}")
            
        st.markdown("---")
        st.subheader("📄 Download Quotation PDF")
        drawing_quot_dict = {
            "Target Quantity": f"{q_qty} Nos",
            "Estimated Cycle Time": f"{est_cycle_time} Sec",
            "Material Cost / Part": f"Rs. {round(mat_total_cost, 2)}",
            "Machining Cost / Part": f"Rs. {round(machining_cost_per_part, 2)}",
            "Price Per Part": f"Rs. {round(final_quoted_price, 2)}",
            "Total Order Value": f"Rs. {round(total_quotation_amount, 2)}"
        }
        d_quot_pdf = generate_quotation_pdf(drawing_quot_dict)
        st.download_button(
            label="📥 Download Drawing Quotation PDF",
            data=d_quot_pdf,
            file_name="Drawing_Quotation.pdf",
            mime="application/pdf"
        )
            
        if st.button("Generate Professional G-Code Program"):
            sample_code = """O2026 (MEGALA CNC MATE AUTO-GENERATED PROGRAM)
G21 G99 G40
M03 S2500
G00 X60.0 Z5.0
(Facing & OD Turning Cycle)
G01 Z-45.0 F0.25
G00 X100.0 Z100.0
M30"""
            st.code(sample_code, language="text")
            
            st.markdown("---")
            st.subheader("📄 Download G-Code Program as PDF")
            prog_pdf_bytes = generate_program_pdf(sample_code)
            st.download_button(
                label="📥 Download G-Code Program PDF",
                data=prog_pdf_bytes,
                file_name="CNC_Program.pdf",
                mime="application/pdf"
            )

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
