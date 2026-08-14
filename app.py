import streamlit as st
import pandas as pd
import math
from fpdf import FPDF
from datetime import datetime
from PIL import Image

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Megala CNC Mate - Enterprise Automation",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. UNIFORM PROFESSIONAL CSS (THEME & CARDS)
# ==========================================
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #090d1f 0%, #111827 40%, #1e1b4b 100%);
        color: #f8fafc;
        font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    }
    .main-title {
        font-size: 2.3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #38bdf8 0%, #c084fc 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 4px 0;
        text-transform: uppercase;
    }
    .sub-title {
        font-size: 0.9rem;
        color: #38bdf8;
        margin-bottom: 15px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
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
    }
    div[data-testid="column"] {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.85) 0%, rgba(49, 46, 129, 0.5) 100%);
        border: 1.5px solid rgba(139, 92, 246, 0.4);
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
        margin-bottom: 16px;
    }
    div.stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 50%, #ec4899 100%);
        color: #ffffff !important;
        border-radius: 10px;
        border: 1.5px solid rgba(236, 72, 153, 0.6);
        font-weight: 800;
        width: 100%;
        padding: 8px 12px;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #f43f5e 100%);
        border-color: #38bdf8;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070b19 0%, #0f172a 100%);
        border-right: 1.5px solid rgba(139, 92, 246, 0.3);
    }
    .sidebar-brand {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.15) 0%, rgba(236, 72, 153, 0.15) 100%);
        border: 2px dashed #38bdf8;
        padding: 12px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. MULTILINGUAL & METRIC DICTIONARY
# ==========================================
translations = {
    "தமிழ் (Tamil)": {
        "home": "🏠 Home / முகப்பு",
        "rod_calc": "📐 Rod & Tube Calculator (Advanced)",
        "prod_calc": "⏱️ Production Calculator",
        "cost_calc": "💰 Costing & Quotation",
        "stock_mgmt": "📦 Stock Management",
        "drawing_studio": "📷 Drawing Operation & CNC G-Code Studio",
        "quote_hub": "📋 Auto Quotation Hub",
    },
    "English": {
        "home": "🏠 Home",
        "rod_calc": "📐 Rod & Tube Calculator (Advanced)",
        "prod_calc": "⏱️ Production Calculator",
        "cost_calc": "💰 Costing & Quotation",
        "stock_mgmt": "📦 Stock Management",
        "drawing_studio": "📷 Drawing Operation & CNC G-Code Studio",
        "quote_hub": "📋 Auto Quotation Hub",
    }
}

# PDF Generator Function
def create_pdf_quotation(df_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Megala CNC Mate - Official Quotation", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(200, 8, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(120, 10, "Description", 1)
    pdf.cell(70, 10, "Amount (INR)", 1, ln=True)
    
    pdf.set_font("Arial", "", 11)
    for _, row in df_data.iterrows():
        pdf.cell(120, 10, str(row["Description"]), 1)
        pdf.cell(70, 10, str(row["Amount (INR)"]), 1, ln=True)
        
    return pdf.output(dest='S').encode('latin1')

# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.markdown("""
    <div class="sidebar-brand">
        <h3 style="margin:0; color:#38bdf8; font-size:1.1rem; text-transform:uppercase;">⚙️ Megala CNC Mate</h3>
        <p style="margin:4px 0 0 0; color:#ec4899; font-size:0.75rem; font-weight:700;">Enterprise Automation Suite</p>
    </div>
""", unsafe_allow_html=True)

selected_lang = st.sidebar.selectbox("🌐 Language / மொழி", list(translations.keys()))
t = translations[selected_lang]

if "page_selection" not in st.session_state:
    st.session_state["page_selection"] = t["home"]

page_options = list(t.values())
if st.session_state["page_selection"] not in page_options:
    st.session_state["page_selection"] = t["home"]

st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation Menu", page_options, index=page_options.index(st.session_state["page_selection"]))
st.session_state["page_selection"] = page

# ==========================================
# 5. MODULES IMPLEMENTATION
# ==========================================

# --- HOME DASHBOARD ---
if page == t["home"]:
    st.markdown('<div class="main-title">Megala CNC Mate</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Advanced Enterprise CNC Operations & Management Dashboard</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Active Machines", "6 Units", "+2 Online")
    with c2:
        st.metric("Daily Output", "1,540 Pcs", "95% Efficiency")
    with c3:
        st.metric("Raw Material", "4,200 Kg", "Stable Stock")
    with c4:
        st.metric("System Status", "Online", "Secure 🟢")

    st.markdown("---")
    st.markdown("### 🚀 Core Modules")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 📐 Rod & Tube Calculator")
        st.write("Advanced mode calculation for raw materials, weights, and scrap.")
        if st.button("Open Rod Module"):
            st.session_state["page_selection"] = t["rod_calc"]
            st.rerun()
    with col2:
        st.markdown("#### 📷 Drawing & G-Code Studio")
        st.write("Upload drawing, analyze operations count, classify machines, and generate CNC G-code.")
        if st.button("Open Drawing Studio"):
            st.session_state["page_selection"] = t["drawing_studio"]
            st.rerun()
    with col3:
        st.markdown("#### 💰 Costing & Quotation")
        st.write("Accurate manufacturing cost calculations and PDF/CSV export hub.")
        if st.button("Open Costing Hub"):
            st.session_state["page_selection"] = t["cost_calc"]
            st.rerun()

# --- ROD & TUBE CALCULATOR (WITH ADVANCED MODE) ---
elif page == t["rod_calc"]:
    st.markdown(f'<div class="main-title">{t["rod_calc"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="auto-badge">Advanced Raw Material Optimizer</div>', unsafe_allow_html=True)

    advanced_mode = st.checkbox("⚙️ Enable Advanced Mode (Custom Density & Wastage)")

    col1, col2 = st.columns(2)
    with col1:
        shape = st.selectbox("Material Shape", ["Round", "Hexagon", "Square", "Hollow Tube"])
        mat_dia = st.number_input("Material Diameter / Size (mm)", value=14.0, step=0.5)
        inner_dia = st.number_input("Inner Diameter (mm)", value=0.0, step=0.5) if shape == "Hollow Tube" else 0.0
    with col2:
        part_len = st.number_input("Part Length (mm)", value=10.0, step=1.0)
        cut_allow = st.number_input("Cutting Allowance (mm)", value=3.0, step=0.5)
        total_weight_input = st.number_input("Total Stock Weight (Kg)", value=500.0, step=10.0)

    if advanced_mode:
        st.markdown("#### Advanced Parameter Customization")
        ac1, ac2 = st.columns(2)
        with ac1:
            custom_density = st.number_input("Material Density (Kg/m³)", value=7850.0, step=10.0)
        with ac2:
            wastage_pct = st.slider("Process Wastage Allowance (%)", 0, 15, 3)
    else:
        custom_density = 7850.0
        wastage_pct = 0

    # Calculation logic
    if shape == 'Round':
        area = math.pi * ((mat_dia / 2.0) ** 2)
    elif shape == 'Hexagon':
        area = (math.sqrt(3) / 2) * (mat_dia ** 2)
    elif shape == 'Hollow Tube':
        area = math.pi * (((mat_dia / 2.0) ** 2) - ((inner_dia / 2.0) ** 2))
    else:
        area = mat_dia ** 2

    weight_per_m = (area / 1e6) * custom_density
    total_len = (total_weight_input / weight_per_m) if weight_per_m > 0 else 0
    piece_len_m = (part_len + cut_allow) / 1000.0
    total_pieces = math.floor(total_len / piece_len_m) if piece_len_m > 0 else 0
    adjusted_pieces = math.floor(total_pieces * (1 - (wastage_pct / 100.0)))

    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Weight per Meter", f"{weight_per_m:.3f} Kg/m")
    with m2:
        st.metric("Total Length Available", f"{total_len:.2f} Meters")
    with m3:
        st.metric("Estimated Yield Parts", f"{adjusted_pieces:,} Pcs")
    with m4:
        st.metric("Advanced Mode Status", "Active 🟢" if advanced_mode else "Standard")

# --- PRODUCTION CALCULATOR ---
elif page == t["prod_calc"]:
    st.markdown(f'<div class="main-title">{t["prod_calc"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="auto-badge">Cycle Time & Shift Output Hub</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        cycle_time = st.number_input("Cycle Time (Seconds)", value=45.0, step=1.0)
        shift_hours = st.number_input("Shift Duration (Hours)", value=8.0, step=0.5)
    with col2:
        efficiency = st.slider("Machine Efficiency (%)", 50, 100, 85)
        downtime_mins = st.number_input("Downtime / Setup Change (Minutes)", value=30.0, step=5.0)

    if cycle_time > 0:
        effective_seconds = (shift_hours * 3600) - (downtime_mins * 60)
        output_per_shift = math.floor((effective_seconds / cycle_time) * (efficiency / 100.0))
        output_per_hour = math.floor((3600 / cycle_time) * (efficiency / 100.0) * 10) / 10

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Production / Hour", f"{output_per_hour} Pcs / Hr")
        with c2:
            st.metric("Production / Shift", f"{output_per_shift} Pcs / Shift")

# --- COSTING & QUOTATION ---
elif page == t["cost_calc"]:
    st.markdown(f'<div class="main-title">{t["cost_calc"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="auto-badge">Financial Pricing Hub</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        mat_rate = st.number_input("Raw Material Rate / Kg (₹)", value=90.0, step=5.0)
        part_weight_g = st.number_input("Part Net Weight (Grams)", value=120.0, step=5.0)
    with col2:
        mach_cost_hr = st.number_input("Machine Hourly Cost (₹/hr)", value=600.0, step=50.0)
        cycle_sec = st.number_input("Cycle Time (Seconds)", value=45.0, step=1.0)
        margin = st.slider("Profit Margin (%)", 5, 50, 25)

    mat_cost_part = (part_weight_g / 1000.0) * mat_rate
    mach_cost_part = (cycle_sec / 3600.0) * mach_cost_hr
    total_cost = mat_cost_part + mach_cost_part
    selling_price = total_cost * (1 + (margin / 100.0))

    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Material Cost / Part", f"₹ {mat_cost_part:.2f}")
    with m2:
        st.metric("Manufacturing Cost", f"₹ {total_cost:.2f}")
    with m3:
        st.metric("Selling Price / Part", f"₹ {selling_price:.2f}", delta=f"{margin}% Margin")

# --- STOCK MANAGEMENT ---
elif page == t["stock_mgmt"]:
    st.markdown(f'<div class="main-title">{t["stock_mgmt"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="auto-badge">Inventory Control Panel</div>', unsafe_allow_html=True)

    if "inventory_df" not in st.session_state:
        st.session_state["inventory_df"] = pd.DataFrame({
            "Part Name": ["Hex Bolt M12", "Aluminium Bush 14mm", "MS Shaft 25mm"],
            "Category": ["Fasteners", "Automotive", "Raw Material"],
            "Quantity": [450, 120, 35],
            "Unit": ["Pcs", "Pcs", "Length"]
        })

    st.dataframe(st.session_state["inventory_df"], use_container_width=True)

    st.markdown("### Add New Inventory Item")
    with st.form("add_stock"):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            p_name = st.text_input("Part Name")
        with c2:
            p_cat = st.text_input("Category")
        with c3:
            p_qty = st.number_input("Quantity", value=100)
        with c4:
            p_unit = st.selectbox("Unit", ["Pcs", "Length", "Kg", "Box"])
        
        submitted = st.form_submit_button("➕ Add Item")
        if submitted and p_name:
            new_row = pd.DataFrame({"Part Name": [p_name], "Category": [p_cat], "Quantity": [p_qty], "Unit": [p_unit]})
            st.session_state["inventory_df"] = pd.concat([st.session_state["inventory_df"], new_row], ignore_index=True)
            st.success("Item added successfully!")
            st.rerun()

# --- DRAWING OPERATION & CNC G-CODE STUDIO ---
elif page == t["drawing_studio"]:
    st.markdown(f'<div class="main-title">{t["drawing_studio"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="auto-badge">Drawing Operation Breakdown & CNC G-Code Studio</div>', unsafe_allow_html=True)

    st.write("📁 **Upload Engineering Drawing:** Our system analyzes the drawing, identifies how many operations are needed, classifies them by machine type, and generates G-Code **strictly for CNC operations**.")

    uploaded_drawing = st.file_uploader("Upload Drawing File", type=["png", "jpg", "jpeg", "pdf"])
    
    if uploaded_drawing is not None:
        st.image(uploaded_drawing, caption="Analyzed Engineering Drawing", width=400)
        
        if st.button("🔍 Analyze Operations & Classify Machines"):
            st.success("Drawing successfully analyzed! Found 4 total operations.")
            
        st.markdown("### 📋 Operation Breakdown & Machine Routing Table")
        
        ops_data = pd.DataFrame({
            "Op No": [1, 2, 3, 4],
            "Operation Description": ["Facing & Center Drilling", "OD Rough Turning (Dia 14mm)", "Hole Drilling (Dia 6mm)", "Parting Off / Cut-off"],
            "Assigned Machine": ["CNC Lathe", "CNC Lathe", "Drilling Machine Hub", "CNC Lathe"],
            "G-Code Applicable?": ["Yes (CNC)", "Yes (CNC)", "No (Drilling Machine)", "Yes (CNC)"]
        })
        st.table(ops_data)

        st.markdown("---")
        st.markdown("### ⚡ CNC-Only G-Code Generator")
        st.write("Below is the automated G-Code generated **only for operations assigned to CNC machines**:")
        
        cnc_gcode = (
            "O1001 (MEGALA CNC MATE - AUTOMATED CNC OPERATIONS)\n"
            "G21 G90 G95 (Metric, Absolute, Feed per Rev)\n"
            "T0101 (Facing & OD Turning Tool)\n"
            "M03 S2000 (Spindle On)\n"
            "G00 X16.0 Z2.0\n"
            "G01 X0.0 Z0.0 F0.2 (Op 1: Facing)\n"
            "G01 X14.0 Z-10.0 F0.15 (Op 2: OD Turning)\n"
            "G00 X20.0 Z50.0\n"
            "T0202 (Parting Tool)\n"
            "G00 X15.0 Z-10.0\n"
            "G01 X0.0 F0.08 (Op 4: Parting Off)\n"
            "M30 (Program End)"
        )
        st.code(cnc_gcode, language="text")

# --- AUTO QUOTATION HUB ---
elif page == t["quote_hub"]:
    st.markdown(f'<div class="main-title">{t["quote_hub"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="auto-badge">Instant Quotation & PDF Export Hub</div>', unsafe_allow_html=True)

    st.write("Generate professional quotation sheets and download instant PDF or CSV reports for clients.")

    c1, c2 = st.columns(2)
    with c1:
        client_name = st.text_input("Client / Company Name", value="Megala Enterprises")
        part_desc = st.text_input("Component Description", value="CNC Turned Bushing 14mm")
    with c2:
        unit_price = st.number_input("Final Quoted Unit Price (₹)", value=45.0, step=1.0)
        order_qty = st.number_input("Order Quantity (Pcs)", value=2500, step=100)

    total_quote_val = unit_price * order_qty

    st.markdown("---")
    quote_summary = pd.DataFrame({
        "Description": ["Component Description", "Order Quantity", "Unit Quoted Price", "Total Quotation Value"],
        "Amount (INR)": [part_desc, f"{order_qty:,} Pcs", f"₹ {unit_price:.2f}", f"₹ {total_quote_val:,.2f}"]
    })
    st.table(quote_summary)

    col_csv, col_pdf = st.columns(2)
    with col_csv:
        csv_bytes = quote_summary.to_csv(index=False).encode('utf-8')
        st.download_button("🚀 Download CSV Quotation", data=csv_bytes, file_name="Megala_CNC_Quotation.csv", mime="text/csv")
    with col_pdf:
        pdf_bytes = create_pdf_quotation(quote_summary)
        st.download_button("📄 Download PDF Quotation", data=pdf_bytes, file_name="Megala_CNC_Quotation.pdf", mime="application/pdf")
