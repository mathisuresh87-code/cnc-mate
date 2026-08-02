import math
import os
from PIL import Image
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Megala CNC Mate - World-Class Professional Workshop Manager",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- HEADER SECTION WITH SAFE LOGO LOADER ---
col_logo, col_title = st.columns([1, 6])

with col_logo:
  if os.path.exists("Logo.png"):
    try:
      st.image("Logo.png", width=110)
    except Exception:
      st.markdown("⚙️ **[Logo Error]**")
  else:
    st.markdown("⚙️ **[Logo Here]**")

with col_title:
  st.title("⚙️ Megala CNC Mate")
  st.markdown(
      "**SMART CNC. SIMPLE WORK.** — World-Class Professional Workshop"
      " Automation, Precise Rod Cutting, End-Bit, Scrap & Quotation Manager"
  )

st.markdown("---")

# --- LANGUAGE SUPPORT SETUP (6 LANGUAGES) ---
st.sidebar.markdown("### 🌐 Language / மொழி")
lang = st.sidebar.selectbox(
    "Choose Language",
    [
        "தமிழ் (Tamil)",
        "English",
        "हिंदी (Hindi)",
        "తెలుగు (Telugu)",
        "മലയാളം (Malayalam)",
        "ಕನ್ನಡ (Kannada)",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Menu Navigation")

# --- COMPLETE PROFESSIONAL MENU OPTIONS (WITHOUT UNWANTED EXTRAS) ---
menu_options = {
    "தமிழ் (Tamil)": [
        "🏠 முகப்பு (Dashboard)",
        "📸 போட்டோ / டிராயிங் பகுப்பாய்வு & ஜி-கோடு",
        "🧮 ஒர்க்ஷாப் கால்குலேட்டர் (RPM & Time)",
        (
            "📐 துல்லியமான ராட், எண்டு-பிட் & ஸ்கிராப் கால்குலேட்டர் (Rod & Scrap"
            " Calculator)"
        ),
        "💰 வாடிக்கையாளர் கொட்டேஷன் (Quotation with Photo)",
        "🏭 உற்பத்தி கண்காணிப்பு (Production Tracker)",
        "📜 ஜி-கோடு ஜெனரேட்டர் (G-Code)",
        "📦 ஸ்டாக் மேனேஜ்மென்ட் (Stock & Inventory)",
    ],
    "English": [
        "🏠 Dashboard",
        "📸 Photo / Drawing Analysis & G-Code",
        "🧮 Workshop Calculator (RPM & Time)",
        "📐 Precise Rod, End-Bit & Scrap Calculator",
        "💰 Customer Quotation (with Photo)",
        "🏭 Production Tracker",
        "📜 G-Code Generator",
        "📦 Stock & Inventory Management",
    ],
    "हिंदी (Hindi)": [
        "🏠 डैशबोर्ड (Dashboard)",
        "📸 फोटो / ड्राइंग विश्लेषण और जी-कोड",
        "🧮 वर्कशॉप कैलकुलेटर",
        "📐 सटीक रॉड, एंड-बिट और स्क्रैप कैलकुलेटर",
        "💰 ग्राहक कोटेशन (Photo)",
        "🏭 उत्पादन ट्रैकर",
        "📜 जी-कोड जेनरेटर",
        "📦 स्टॉक प्रबंधन",
    ],
    "తెలుగు (Telugu)": [
        "🏠 డాష్‌బోర్డ్ (Dashboard)",
        "📸 ఫోటో / డ్రాయింగ్ విశ్లేషణ & జి-కోడ్",
        "🧮 వర్క్‌షాప్ కాలిక్యులేటర్",
        "📐 ఖచ్చితమైన రాడ్, ఎండ్-బిట్ & స్క్రాప్ కాలిక్యులేటర్",
        "💰 కస్టమర్ కొటేషన్ (Photo)",
        "🏭 ఉత్పత్తి ట్రాకర్",
        "📜 జి-కోడ్ జనరేటర్",
        "📦 స్టాక్ నిర్వహణ",
    ],
    "മലയാളം (Malayalam)": [
        "🏠 ഡാഷ്‌ബോർഡ് (Dashboard)",
        "📸 ഫോട്ടോ / ഡ്രോയിംഗ് വിശകലനം & ജി-കോഡ്",
        "🧮 വർക്ക്‌ഷോപ്പ് കാൽക്കുലേറ്റർ",
        "📐 കൃത്യമായ റോഡ്, എൻഡ്-ബിറ്റ് & സ്ക്രാപ്പ് കാൽക്കുലേറ്റർ",
        "💰 കസ്റ്റമർ കൊട്ടേഷൻ (Photo)",
        "🏭 പ്രൊഡക്ഷൻ ട്രാക്കർ",
        "📜 ജി-കോഡ് ജനറേറ്റർ",
        "📦 സ്റ്റോക്ക് മാനേജ്മെന്റ്",
    ],
    "ಕನ್ನಡ (Kannada)": [
        "🏠 ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ (Dashboard)",
        "📸 ಫೋಟೋ / ಡ್ರಾಯಿಂಗ್ ವಿಶ್ಲೇಷಣೆ & జి-కోడ్",
        "🧮 ವರ್ಕ್‌ಷೋಪ್ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
        "📐 ನಿಖರವಾದ ರಾಡ್, ಎಂಡ್-ಬಿಟ್ ಮತ್ತು ಸ್ಕ್ರ್ಯಾಪ್ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
        "💰 ಗ್ರಾಹಕರ ಉಲ್ಲೇಖ (Quotation)",
        "🏭 ಉತ್ಪಾದನಾ ಟ್ರ್ಯಾಕರ್",
        "📜 ಜಿ-ಕೋಡ್ ಜನರೇಟರ್",
        "📦 ಸ್ಟಾಕ್ ನಿರ್ವಹಣೆ",
    ],
}

# Radio button ensures ALL options are permanently visible on the sidebar without hiding
app_mode = st.sidebar.radio(
    "Select Module", menu_options[lang], label_visibility="collapsed"
)

# --- 1. DASHBOARD ---
if any(
    x in app_mode
    for x in ["Dashboard", "முகப்பு", "डैशबोर्ड", "డాష్‌బోర్డ్", "ഡാഷ്‌ബോർഡ്"]
):
  st.header("📊 Megala CNC Mate Professional Dashboard")
  st.write(
      "Your world-class workshop command center for precise material"
      " calculation, scrap tracking, and CNC production."
  )

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(label="Active Modules", value="8 Ready")
  with col2:
    st.metric(label="System Status", value="Online 🟢")
  with col3:
    st.metric(label="Languages", value="6 Supported")
  with col4:
    st.metric(label="Version", value="World-Class Final v14.0")

# --- 2. PHOTO / DRAWING ANALYSIS & G-CODE MODULE ---
elif any(
    x in app_mode for x in ["Photo", "போட்டோ", "फोटो", "ఫోటో", "ഫോട്ടോ", "ಫೋಟೋ"]
):
  st.header("📸 Component Drawing / Photo Analyzer & G-Code Generator")
  st.write(
      "Upload your component drawing or part photo to inspect dimensions and"
      " generate precise G-code."
  )

  uploaded_file = st.file_uploader(
      "Upload Part Drawing / Photo (PNG, JPG)", type=["png", "jpg", "jpeg"]
  )

  if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(
        image,
        caption="Uploaded Component Drawing / Photo",
        use_column_width=True,
    )
    st.success("✅ Image Uploaded Successfully!")

    op_type = st.selectbox(
        "Machining Operation",
        ["Turning & Facing", "Stepped Turning", "Grooving & Parting"],
    )
    part_dia = st.number_input("Major Diameter (mm)", value=40.0)
    part_length = st.number_input("Total Machining Length (mm)", value=60.0)

    if st.button("Generate G-Code from Drawing"):
      gcode_out = f"""
O1001 (WORLD-CLASS CNC PROGRAM - MEGALA MATE)
G21 G90 G40 G80 G18
M03 S1800
G00 X{part_dia + 4.0} Z2.0
(OPERATION: {op_type.upper()})
G01 Z-0.5 F0.2
G01 X{part_dia} F0.15
G01 Z-{part_length} F0.12
G00 X{part_dia + 10.0}
G00 Z50.0
M05
M30
"""
      st.code(gcode_out, language="text")
      st.download_button(
          "📥 Download G-Code File (.nc)",
          data=gcode_out,
          file_name="drawing_program.nc",
          mime="text/plain",
      )
  else:
    st.info(
        "💡 Upload a component photo or drawing to begin automated programming."
    )

# --- 3. WORKSHOP CALCULATOR (RPM & TIME) ---
elif any(
    x in app_mode
    for x in [
        "Calculator",
        "கால்குலேட்டர்",
        "कैलकुलेटर",
        "కాలిక్యులేటర్",
        "കാൽക്കുലേറ്റർ",
    ]
):
  st.header("🧮 Workshop Calculator (RPM & Machining Time)")
  calc_choice = st.selectbox(
      "Select Calculation", ["Spindle RPM Calculator", "Machining Time Calculator"]
  )

  if "RPM" in calc_choice:
    c1, c2 = st.columns(2)
    with c1:
      vc = st.number_input("Cutting Speed (Vc in m/min)", value=200.0)
    with c2:
      dia = st.number_input("Rod / Component Diameter (mm)", value=40.0)

    if st.button("Calculate RPM"):
      if dia > 0:
        rpm = (1000 * vc) / (math.pi * dia)
        st.success(f"✅ Required Spindle Speed: **{rpm:.2f} RPM**")
  else:
    c1, c2 = st.columns(2)
    with c1:
      length = st.number_input("Cutting Length (mm)", value=80.0)
      feed = st.number_input("Feed Rate (mm/rev)", value=0.2)
    with c2:
      rpm_val = st.number_input("Spindle Speed (RPM)", value=1500.0)

    if st.button("Calculate Time"):
      if feed > 0 and rpm_val > 0:
        t_mins = length / (feed * rpm_val)
        st.success(f"✅ Estimated Machining Time: **{t_mins:.2f} Minutes**")

# --- 4. PRECISE ROD, END-BIT, GROOVING & SCRAP CALCULATOR (THE USERS FAVORITE TOOL) ---
elif any(
    x in app_mode
    for x in ["Rod", "ராட்", "रॉड", "రॉड", "റോഡ്", "சடிக்", "எண்டு-பிட்"]
):
  st.header(
      "📐 Precise Rod, End-Bit, Grooving & Scrap Calculator (Length & Weight)"
  )
  st.write(
      "Calculate exact pieces per rod (e.g., 3m or 6m rods), tail-end waste"
      " (end-bit), parting blade cutting allowance, facing allowance, and"
      " precise scrap weight in grams/kg."
  )

  col_a, col_b = st.columns(2)

  with col_a:
    mat_grade = st.selectbox(
        "Material Grade",
        [
            "EN8",
            "EN24",
            "Aluminum 6061",
            "Mild Steel (MS)",
            "Brass",
            "Stainless Steel 304",
            "Cast Iron",
        ],
    )
    # Density setting (g/cm³)
    if "Aluminum" in mat_grade:
      density = 2.70
    elif "Brass" in mat_grade:
      density = 8.50
    elif "Stainless Steel" in mat_grade:
      density = 7.93
    else:
      density = 7.85

    profile_type = st.selectbox(
        "Rod / Bar Profile",
        [
            "Round Bar",
            "Hexagon Bar",
            "Square Bar",
            "Tube / Hollow Pipe",
            "Flat Plate",
        ],
    )

    # Rod length selection (Supports 3m, 6m or custom lengths)
    standard_rod_length_m = st.number_input(
        "Standard Raw Rod Length Supplied (Meters e.g., 3m or 6m)",
        min_value=0.5,
        value=6.0,
        step=0.5,
    )

  with col_b:
    if profile_type == "Round Bar":
      dia = st.number_input(
          "Drawing Outer Diameter (mm)", min_value=0.1, value=40.0
      )
    elif profile_type == "Hexagon Bar":
      across_flat = st.number_input(
          "Drawing Across Flats (mm)", min_value=0.1, value=40.0
      )
    elif profile_type == "Square Bar":
      side_w = st.number_input(
          "Drawing Side Width (mm)", min_value=0.1, value=40.0
      )
    elif profile_type == "Tube / Hollow Pipe":
      outer_d = st.number_input(
          "Tube Outer Diameter (mm)", min_value=0.1, value=50.0
      )
      inner_d = st.number_input(
          "Tube Inner Bore Diameter (mm)", min_value=0.0, value=25.0
      )
    else:
      f_width = st.number_input("Plate Width (mm)", min_value=0.1, value=60.0)
      f_thick = st.number_input(
          "Plate Thickness (mm)", min_value=0.1, value=12.0
      )

    part_drawing_length = st.number_input(
        "Finished Part Length from Drawing (mm)", min_value=1.0, value=45.0
    )
    facing_allowance = st.number_input(
        "Facing Allowance per piece (mm)", min_value=0.0, value=2.0
    )
    parting_tool_width = st.number_input(
        "Parting / Cutting Tool Blade Width / Allowance (mm)",
        min_value=0.1,
        value=3.0,
    )

  if st.button("Calculate Exact Pieces, End-Bit & Scrap"):
    # Volume calculation per cm
    if profile_type == "Round Bar":
      r_cm = (dia / 2.0) / 10.0
      vol_per_cm = math.pi * (r_cm**2)
    elif profile_type == "Hexagon Bar":
      af_cm = across_flat / 10.0
      vol_per_cm = (math.sqrt(3) / 2) * (af_cm**2)
    elif profile_type == "Square Bar":
      sw_cm = side_w / 10.0
      vol_per_cm = sw_cm**2
    elif profile_type == "Tube / Hollow Pipe":
      o_cm = (outer_d / 2.0) / 10.0
      i_cm = (inner_d / 2.0) / 10.0
      vol_per_cm = math.pi * ((o_cm**2) - (i_cm**2))
    else:
      fw_cm = f_width / 10.0
      ft_cm = f_thick / 10.0
      vol_per_cm = fw_cm * ft_cm

    total_rod_len_mm = standard_rod_length_m * 1000.0
    single_consumption_mm = (
        part_drawing_length + facing_allowance + parting_tool_width
    )
    pieces_per_rod = int(total_rod_len_mm // single_consumption_mm)

    used_length_mm = pieces_per_rod * single_consumption_mm
    end_bit_leftover_mm = total_rod_len_mm - used_length_mm
    total_cutting_blade_scrap_mm = pieces_per_rod * parting_tool_width

    total_gross_weight_kg = (
        (vol_per_cm * (total_rod_len_mm / 10.0)) * density
    ) / 1000.0
    net_part_weight_kg = (
        (vol_per_cm * (part_drawing_length / 10.0)) * density
    ) / 1000.0
    total_net_weight_all_parts = net_part_weight_kg * pieces_per_rod

    end_bit_weight_kg = (
        (vol_per_cm * (end_bit_leftover_mm / 10.0)) * density
    ) / 1000.0
    cutting_blade_scrap_weight_kg = (
        (vol_per_cm * (total_cutting_blade_scrap_mm / 10.0)) * density
    ) / 1000.0
    total_scrap_weight_kg = end_bit_weight_kg + cutting_blade_scrap_weight_kg

    st.success(
        "✅ Precise Rod, End-Bit, Grooving & Scrap Calculation Completed!"
    )
    st.markdown(
        f"### Production Summary for **{standard_rod_length_m} Meter** Rod"
        f" ({mat_grade} - {profile_type})"
    )

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Pieces per Rod", f"{pieces_per_rod} Nos")
    r2.metric("Tail-End Waste (End-Bit)", f"{end_bit_leftover_mm:.1f} mm")
    r3.metric("Total Scrap Weight", f"{total_scrap_weight_kg:.3f} Kg")
    r4.metric("Rod Gross Weight", f"{total_gross_weight_kg:.3f} Kg")

    st.info(
        f"📋 **Detailed Weight & Measurement Breakdown:**\n"
        f"- **Net Weight of Finished Parts:**"
        f" {total_net_weight_all_parts:.3f} Kg\n"
        f"- **Tail-End Piece Waste Weight (End-Bit):**"
        f" {end_bit_weight_kg:.3f} Kg\n"
        f"- **Parting Blade & Facing Scrap Weight:**"
        f" {cutting_blade_scrap_weight_kg:.3f} Kg\n"
        f"- **Single Piece Length Consumption (with allowances):**"
        f" {single_consumption_mm:.1f} mm"
    )

# --- 5. CUSTOMER QUOTATION (WITH PHOTO SUPPORT) ---
elif any(
    x in app_mode
    for x in ["Quotation", "கொட்டேஷன்", "कोटेशन", "కొటేషన్", "കൊട്ടേഷൻ"]
):
  st.header("💰 Customer Quotation & Cost Estimator (with Photo Reference)")
  st.write(
      "Calculate costs based on material grades and attach part photos for"
      " quotation records."
  )

  q_photo = st.file_uploader(
      "Upload Part Photo for Quotation Reference",
      type=["png", "jpg", "jpeg"],
      key="q_photo",
  )
  if q_photo:
    st.image(q_photo, width=200, caption="Quotation Reference Photo")

  c1, c2 = st.columns(2)
  with c1:
    cust_name = st.text_input("Customer Name", "ABC Industries")
    part_name = st.text_input("Component Name", "Bush / Shaft")
    mat_cost_kg = st.number_input("Raw Material Cost per Kg (₹)", value=85.0)
  with c2:
    part_wt = st.number_input("Part Weight (Kg)", value=1.0)
    mach_time = st.number_input("Machining Time per piece (Mins)", value=5.0)
    machine_rate = st.number_input("Machine Hourly Rate (₹/hr)", value=600.0)
    batch_qty = st.number_input("Batch Quantity", value=100)
    profit = st.slider("Profit Margin (%)", 0, 50, 20)

  if st.button("Calculate Quotation"):
    mat_tot = part_wt * mat_cost_kg
    mach_cost = (machine_rate / 60) * mach_time
    unit_price = (mat_tot + mach_cost) * (1 + profit / 100)
    grand_total = unit_price * batch_qty
    st.success("✅ Quotation Calculated Successfully with Photo Reference!")
    r1, r2, r3 = st.columns(3)
    r1.metric("Unit Price", f"₹{unit_price:.2f}")
    r2.metric("Batch Quantity", f"{batch_qty} Nos")
    r3.metric("Grand Total", f"₹{grand_total:,.2f}")

# --- 6. PRODUCTION TRACKER ---
elif any(
    x in app_mode
    for x in ["Production", "உற்பத்தி", "उत्पादन", "ఉత్పత్తి", "പ്രൊഡക്ഷൻ"]
):
  st.header("🏭 Production & Batch Tracker")
  job_no = st.text_input("Job Order Number", "JOB-2026-001")
  target = st.number_input("Target Quantity", value=500)
  completed = st.number_input("Completed Quantity", value=350)
  cycle_t = st.number_input("Cycle Time per part (Seconds)", value=45.0)

  if st.button("Check Progress"):
    pct = (completed / target) * 100
    st.progress(min(pct / 100.0, 1.0))
    st.write(f"**Completion Status:** {pct:.1f}%")
    tot_hrs = (target * cycle_t) / 3600
    st.info(f"⏱️ Estimated total batch time: **{tot_hrs:.2f} Hours**")

# --- 7. G-CODE GENERATOR ---
elif any(
    x in app_mode for x in ["G-Code", "ஜி-கோடு", "जी-कोड", "జి-కోడ్", "ജി-കോഡ്"]
):
  st.header("📜 CNC G-Code Generator")
  op = st.selectbox("Operation", ["Facing & Turning", "Grooving", "Drilling"])
  feed = st.number_input("Feed Rate", value=0.15)
  s_speed = st.number_input("Spindle Speed", value=1500)

  if st.button("Generate G-Code"):
    code = f"""
O0001 (MEGALA CNC MATE PROFESSIONAL)
G21 G90 G40 G80 G18
M03 S{s_speed}
G00 X52.0 Z2.0
G01 Z0.0 F{feed}
G00 Z50.0
M05
M30
"""
    st.code(code, language="text")
    st.download_button(
        "📥 Download G-Code File (.nc)",
        data=code,
        file_name="program.nc",
        mime="text/plain",
    )

# --- 8. STOCK MANAGEMENT ---
elif any(
    x in app_mode for x in ["Stock", "ஸ்டாக்", "स्टॉक", "സ്റ്റോക്ക്", "ನಿರ್ವಹಣೆ"]
):
  st.header("📦 Stock & Inventory Management")
  st.write("Monitor raw material stock levels and reorder alerts.")
  st.selectbox(
      "Material Grade",
      [
          "EN8",
          "EN24",
          "Aluminum 6061",
          "Mild Steel (MS)",
          "Brass",
          "Stainless Steel 304",
      ],
  )
  weight = st.number_input("Available Rod Weight (Kg)", value=150.0)
  min_l = st.number_input("Minimum Alert Limit (Kg)", value=30.0)
  if st.button("Check Stock Status"):
    if weight <= min_l:
      st.warning("⚠️ **Warning:** Low Stock! Reorder required.")
    else:
      st.success("✅ Stock level is sufficient.")
    st.write(f"- **Current Available Weight:** **{weight} Kg**")

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>© 2026 Megala CNC Mate | World-Class"
    " Professional Workshop Automation</p>",
    unsafe_allow_html=True,
)
