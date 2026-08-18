import base64
import os
import pandas as pd
import streamlit as st

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

# Custom UI Styling with Compact Logo & Glowing Neon Background
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #050B18 0%, #0A1428 50%, #040711 100%);
        color: #FFFFFF;
        font-family: 'Segoe UI', Roboto, Helvetica, sans-serif;
    }
    .brand-container {
        text-align: center;
        padding: 15px 0 20px 0;
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
        margin-bottom: 0px;
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
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        text-align: center;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        border-color: #48CAE4;
        box-shadow: 0 10px 30px rgba(72, 202, 228, 0.3);
        transform: translateY(-3px);
    }
    .card-title {
        font-size: 16px;
        font-weight: bold;
        color: #F8FAFC;
        margin-top: 10px;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #1D4ED8, #00B4D8);
        color: white;
        font-weight: bold;
        border-radius: 12px;
        height: 48px;
        border: none;
        box-shadow: 0 4px 15px rgba(29, 78, 216, 0.5);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #2563EB, #48CAE4);
        box-shadow: 0 6px 20px rgba(72, 202, 228, 0.7);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Top Header Banner with Glowing Logo
st.markdown('<div class="brand-container">', unsafe_allow_html=True)
if logo_base64:
  st.markdown(
      f"""
        <div class="logo-glow-box">
            <img src="data:image/png;base64,{logo_base64}" />
        </div>
    """,
      unsafe_allow_html=True,
  )
else:
  st.markdown(
      '<div style="font-size: 35px; margin-bottom: 2px; text-align:'
      ' center;">⚙️</div>',
      unsafe_allow_html=True,
  )

st.markdown(
    """
        <div class="brand-title">MEGALA CNC MATE</div>
        <div class="brand-subtitle">SMART CNC. SIMPLE WORK.</div>
    </div>
""",
    unsafe_allow_html=True,
)

# Session state for navigation & results
if "nav_menu" not in st.session_state:
  st.session_state.nav_menu = "Home Dashboard"

if "calc_results" not in st.session_state:
  st.session_state.calc_results = None

if "stock_db" not in st.session_state:
  st.session_state.stock_db = pd.DataFrame([
      {
          "Material": "EN8 Round Bar - 12mm",
          "Unit": "Meter",
          "Available Stock": 120.50,
          "Status": "In Stock",
      },
      {
          "Material": "MS Round Bar - 20mm",
          "Unit": "Kg",
          "Available Stock": 45.20,
          "Status": "Low Stock",
      },
  ])


def navigate_to(menu_name):
  st.session_state.nav_menu = menu_name


# SIDEBAR
st.sidebar.title("⚙️ MEGALA CNC MATE")
st.sidebar.markdown("### Smart CNC. Simple Work.")

languages = [
    "Tamil (தமிழ்)",
    "English",
    "Hindi (हिन्दी)",
    "Telugu (తెలుగు)",
    "Kannada (ಕನ್ನಡ)",
    "Malayalam (മലയാളം)",
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
  st.markdown(
      '<div style="font-size: 24px; font-weight: 800; color: #F8FAFC;'
      ' margin-bottom: 5px;">Welcome, Operator! 👋</div>',
      unsafe_allow_html=True,
  )
  st.markdown(
      '<div style="color: #94A3B8; font-size: 14px; margin-bottom: 20px;">Smart'
      " CNC. Simple Work. - Select a module below to start working</div>",
      unsafe_allow_html=True,
  )

  col1, col2, col3 = st.columns(3)

  with col1:
    st.markdown(
        '<div class="metric-card">📏<div class="card-title">Rod Calculator &'
        " 3D</div></div>",
        unsafe_allow_html=True,
    )
    if st.button("Open Rod Calculator"):
      navigate_to("Rod & Tube Calculator")
      st.rerun()

    st.markdown(
        '<div class="metric-card">🛠️<div class="card-title">G-Code'
        " Generator</div></div>",
        unsafe_allow_html=True,
    )
    if st.button("Open G-Code Generator"):
      navigate_to("Advanced G-Code Generator")
      st.rerun()

  with col2:
    st.markdown(
        '<div class="metric-card">⏱️<div class="card-title">Production &'
        " Drilling</div></div>",
        unsafe_allow_html=True,
    )
    if st.button("Open Production Calculator"):
      navigate_to("Production & Cycle Time")
      st.rerun()

    st.markdown(
        '<div class="metric-card">📦<div class="card-title">Stock'
        " Management</div></div>",
        unsafe_allow_html=True,
    )
    if st.button("Open Stock Management"):
      navigate_to("Stock Management")
      st.rerun()

  with col3:
    st.markdown(
        '<div class="metric-card">📄<div class="card-title">Quotation &'
        " PDF</div></div>",
        unsafe_allow_html=True,
    )
    if st.button("Open Quotation Generator"):
      navigate_to("Quotation & PDF")
      st.rerun()

    st.markdown(
        '<div class="metric-card">⚙️<div class="card-title">Settings &'
        " Masters</div></div>",
        unsafe_allow_html=True,
    )
    if st.button("Open Settings"):
      navigate_to("More Menu / Master Settings")
      st.rerun()

# 2. ROD & TUBE CALCULATOR
elif st.session_state.nav_menu == "Rod & Tube Calculator":
  st.markdown(
      '<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Rod &'
      " Tube Calculator (3D Pro)</div>",
      unsafe_allow_html=True,
  )
  st.markdown(
      '<div style="color: #94A3B8; font-size: 13px; margin-bottom: 20px;">Flexible'
      " input mode with End Bit calculation & Live Part Photo Preview.</div>",
      unsafe_allow_html=True,
  )

  calc_mode = st.radio(
      "Operating Mode",
      ["Simple Mode", "Advanced Mode (Drawing Scan & 3D)"],
      horizontal=True,
  )
  auto_operations = ["Facing", "Turning"]

  if calc_mode == "Advanced Mode (Drawing Scan & 3D)":
    uploaded_drawing = st.file_uploader(
        "Upload Part Drawing Photo (PNG, JPG)", type=["png", "jpg", "jpeg"]
    )
    if uploaded_drawing is not None:
      st.image(
          uploaded_drawing,
          caption="Uploaded Part Drawing Preview",
          use_container_width=True,
      )
      auto_operations = ["Facing", "Turning", "Drilling", "Chamfering"]

  col1, col2 = st.columns(2)
  with col1:
    rod_type = st.selectbox(
        "Rod Shape / வடிவம்",
        ["Round (ரவுண்ட்)", "Hexagon (எக்ஸகன்)", "Square (ஸ்கொயர்)", "Tube (டியூப்)"],
    )
    unit_type = st.selectbox(
        "Measurement Unit / அளவீட்டு முறை", ["Meter (மீட்டர்)", "Kilogram (கிலோகிராம்)"]
    )
    rod_length_input = st.number_input(
        "Rod Length / Weight Input", min_value=0.0, value=4.0, step=0.1
    )
  with col2:
    part_length = st.number_input(
        "Part Length (mm) / பார்ட் நீளம்", min_value=0.0, value=122.5, step=0.1
    )
    cutting_allowance = st.number_input(
        "Cutting & Facing Allowance (mm)", min_value=0.0, value=3.0, step=0.1
    )
    required_qty = st.number_input(
        "Required Quantity (Nos) / தேவையான அளவு", min_value=0, value=100, step=1
    )
    cycle_sec = st.number_input(
        "Cycle Time (Seconds)", min_value=0.0, value=17.0, step=0.5
    )

  if st.button("Calculate & Render Part Preview"):
    total_part_len = part_length + cutting_allowance
    rod_total_mm = rod_length_input * 1000
    parts_per_rod = (
        int(rod_total_mm / total_part_len)
        if (total_part_len > 0 and rod_length_input > 0)
        else 0
    )
    used_length_mm = parts_per_rod * total_part_len
    end_bit_mm = (
        rod_total_mm - used_length_mm if rod_length_input > 0 else 0.0
    )
    required_rods = (
        int(required_qty / parts_per_rod)
        if (parts_per_rod > 0 and required_qty > 0)
        else 0
    )
    total_stock_len = (
        required_rods * rod_length_input if required_rods > 0 else 0.0
    )
    prod_per_hr = int(3600 / cycle_sec) if cycle_sec > 0 else 0
    total_machine_time = (
        (required_qty * cycle_sec) / 3600 if required_qty > 0 else 0.0
    )

    st.session_state.calc_results = {
        "parts_per_rod": parts_per_rod,
        "end_bit_mm": end_bit_mm,
        "required_rods": required_rods,
        "total_stock_len": total_stock_len,
        "prod_per_hr": prod_per_hr,
        "total_machine_time": total_machine_time,
        "rod_type": rod_type,
        "part_length": part_length,
        "calc_mode": calc_mode,
        "auto_operations": auto_operations,
    }

  if st.session_state.calc_results is not None:
    res = st.session_state.calc_results
    st.markdown("---")
    st.subheader("📊 Calculation Result Summary")
    r1, r2, r3 = st.columns(3)
    r1.success(f"**Parts / Rod:** {res['parts_per_rod']} Nos")
    r2.warning(f"**End Bit / Scrap:** {res['end_bit_mm']:.2f} mm")
    r3.success(f"**Required Rods:** {res['required_rods']} Nos")

    r4, r5, r6 = st.columns(3)
    r4.info(f"**Total Stock Length:** {res['total_stock_len']:.2f} m")
    r5.info(f"**Production / Hour:** {res['prod_per_hr']} Nos")
    r6.info(f"**Total Machine Time:** {res['total_machine_time']:.2f} Hr")

# 3. PRODUCTION & CYCLE TIME
elif st.session_state.nav_menu == "Production & Cycle Time":
  st.markdown(
      '<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Production'
      " & Cycle Time Analyzer</div>",
      unsafe_allow_html=True,
  )
  col1, col2 = st.columns(2)
  with col1:
    machine_type = st.selectbox(
        "Machine Type", ["CNC Lathe", "Traub Machine", "Drill Machine", "VMC"]
    )
    operation_type = st.selectbox(
        "Operation", ["Facing", "Turning", "Threading", "Tapping", "Drilling"]
    )
    cycle_time_p = st.number_input(
        "Cycle Time per Part (sec)", min_value=0.0, value=20.0
    )
  with col2:
    avail_time = st.number_input(
        "Total Working Hours", min_value=0.0, value=12.0, step=0.5
    )
    machine_eff = st.slider(
        "Machine Efficiency (%)", min_value=10, max_value=100, value=85
    )
    break_time = st.number_input("Break Time (min)", min_value=0, value=30)

  if st.button("Calculate Production Output"):
    effective_hours = avail_time - (break_time / 60.0) if avail_time > 0 else 0
    prod_per_hr = (
        int((3600 / cycle_time_p) * (machine_eff / 100.0))
        if cycle_time_p > 0
        else 0
    )
    prod_per_day = int(prod_per_hr * effective_hours) if effective_hours > 0 else 0
    st.markdown("---")
    c1, c2 = st.columns(2)
    c1.success(f"### Production / Hour: **{prod_per_hr} Nos**")
    c2.success(f"### Production for {avail_time} Hours: **{prod_per_day} Nos**")

# 4. STOCK MANAGEMENT
elif st.session_state.nav_menu == "Stock Management":
  st.markdown(
      '<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Stock'
      " Management System</div>",
      unsafe_allow_html=True,
  )
  # Using st.data_editor so that user changes/stocks are interactive and persisted without data loss
  st.session_state.stock_db = st.data_editor(
      st.session_state.stock_db, num_rows="dynamic", use_container_width=True
  )

# 5. ADVANCED G-CODE GENERATOR
elif st.session_state.nav_menu == "Advanced G-Code Generator":
  st.markdown(
      '<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Advanced'
      " G-Code Generator</div>",
      unsafe_allow_html=True,
  )
  if st.button("Generate G-Code & Export"):
    gcode_sample = "O0001\nG21 G90\nM30"
    st.code(gcode_sample, language="text")

# 6. QUOTATION & PDF
elif st.session_state.nav_menu == "Quotation & PDF":
  st.markdown(
      '<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">Quotation'
      " Generator</div>",
      unsafe_allow_html=True,
  )

# 7. MORE MENU / MASTERS & SETTINGS
elif st.session_state.nav_menu == "More Menu / Master Settings":
  st.markdown(
      '<div style="font-size: 24px; font-weight: 800; color: #48CAE4;">More Menu'
      " & Masters</div>",
      unsafe_allow_html=True,
  )
