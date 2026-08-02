import math
import os
from PIL import Image
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Megala CNC Mate - Professional Workshop Manager",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- HEADER SECTION ---
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
      "**SMART CNC. SIMPLE WORK.** — Professional Workshop Automation & Exact"
      " Module Routing"
  )

st.markdown("---")

# --- LANGUAGE SUPPORT SETUP ---
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
st.sidebar.markdown("### 📌 Menu Navigation (முகப்பு மெனு)")

# --- DISTINCT MENU OPTIONS (No overlapping keywords to prevent routing bugs) ---
menu_options = {
    "தமிழ் (Tamil)": [
        "1. மெஷின் கால்குலேட்டர் (Machine RPM & Time)",
        "2. கொட்டேஷன் & செலவு மேலாண்மை (Quotation & Overheads)",
        "3. முகப்பு & டேஷ்போர்டு (Dashboard Overview)",
        "4. போட்டோ / டிராயிங் பகுப்பாய்வு (Drawing & Photo Analysis)",
        "5. ராட், எண்டு-பிட் & ஸ்கிராப் (Rod & Scrap Calculator)",
        "6. ஜி-கோடு ஜெனரேட்டர் (Advanced G-Code)",
        "7. உற்பத்தி நாட்கள் கால்குலேட்டர் (Production Days)",
        "8. ஸ்டாக் மேனேஜ்மென்ட் (Stock & Inventory)",
    ],
    "English": [
        "1. Machine Calculator (RPM & Time)",
        "2. Quotation & Cost Management (Overheads)",
        "3. Dashboard Overview",
        "4. Drawing & Photo Analysis",
        "5. Rod, End-Bit & Scrap Calculator",
        "6. Advanced G-Code Generator",
        "7. Production Days Calculator",
        "8. Stock & Inventory Management",
    ],
    "हिंदी (Hindi)": [
        "1. मशीन कैलकुलेटर (RPM & Time)",
        "2. कोटेशन और लागत प्रबंधन (Quotation)",
        "3. डैशबोर्ड अवलोकन (Dashboard)",
        "4. ड्राइंग और फोटो विश्लेषण (Analysis)",
        "5. रॉड और स्क्रैप कैलकुलेटर (Scrap)",
        "6. उन्नत जी-कोड जेनरेटर (G-Code)",
        "7. उत्पादन दिन कैलकुलेटर (Production)",
        "8. स्टॉक प्रबंधन (Stock)",
    ],
    "తెలుగు (Telugu)": [
        "1. మెషిన్ కాలిక్యులేటర్ (RPM & Time)",
        "2. కొటేషన్ & ఖర్చు నిర్వహణ (Quotation)",
        "3. డాష్‌బోర్డ్ అవలోకనం (Dashboard)",
        "4. డ్రాయింగ్ & ఫోటో విశ్లేషణ (Analysis)",
        "5. రాడ్ & స్క్రాప్ కాలిక్యులేటర్ (Scrap)",
        "6. అధునాతన జి-కోడ్ జనరేటర్ (G-Code)",
        "7. ఉత్పత్తి రోజుల కాలిక్యులేటర్ (Production)",
        "8. స్టాక్ నిర్వహణ (Stock)",
    ],
    "മലയാളം (Malayalam)": [
        "1. മെഷീൻ കാൽക്കുലേറ്റർ (RPM & Time)",
        "2. കൊട്ടേഷൻ & കോസ്റ്റ് മാനേജ്മെന്റ് (Quotation)",
        "3. ഡാഷ്‌ബോർഡ് അവലോകനം (Dashboard)",
        "4. ഡ്രോയിംഗ് & ഫോട്ടോ വിശകലനം (Analysis)",
        "5. റോഡ് & സ്ക്രാപ്പ് കാൽക്കുലേറ്റർ (Scrap)",
        "6. അഡ്വാൻസ്ഡ് ജി-കോഡ് ജെനറേറ്റർ (G-Code)",
        "7. പ്രൊഡക്ഷൻ ഡേയ്സ് കാൽക്കുലേറ്റർ (Production)",
        "8. സ്റ്റോക്ക് മാനേജ്മെന്റ് (Stock)",
    ],
    "ಕನ್ನಡ (Kannada)": [
        "1. ಮೆಷಿನ್ ಕ್ಯಾಲ್ಕುಲೇಟರ್ (RPM & Time)",
        "2. ಉಲ್ಲೇಖ ಮತ್ತು ವೆಚ್ಚ ನಿರ್ವಹಣೆ (Quotation)",
        "3. ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ ಅವಲೋಕನ (Dashboard)",
        "4. ಡ್ರಾಯಿಂಗ್ & ಫೋಟೋ ವಿಶ್ಲೇಷಣೆ (Analysis)",
        "5. ರಾಡ್ & ಸ್ಕ್ರ್ಯಾಪ್ ಕ್ಯಾಲ್ಕುలేಟರ್ (Scrap)",
        "6. ಸುಧಾರಿತ జి-కోడ్ ಜನರೇಟರ್ (G-Code)",
        "7. ಉತ್ಪಾದನಾ ದಿನಗಳ ಕ್ಯಾಲ್ಕುಲೇಟರ್ (Production)",
        "8. ಸ್ಟಾಕ್ ನಿರ್ವಹಣೆ (Stock)",
    ],
}

app_mode = st.sidebar.radio(
    "Select Module", menu_options[lang], label_visibility="collapsed"
)

# --- EXACT STRING MATCHING FOR EACH MODULE (Ensures zero routing overlap) ---

# MODULE 1: MACHINE CALCULATOR
if (
    app_mode.startswith("1.")
    or "Machine Calculator" in app_mode
    or "மெஷின் கால்குலேட்டர்" in app_mode
):
  st.header("🧮 Machine-Specific Workshop Calculator (CNC / Traub / Drilling)")
  st.write(
      "Choose your exact machine type. Calculations adjust automatically"
      " according to CNC, Traub, or Drilling mechanics."
  )

  machine_choice = st.selectbox(
      "Select Your Machine Type",
      [
          "1. CNC Turning Lathe (Feed in mm/rev)",
          "2. Traub Automatic Lathe (Cam Cycle / Slide Speed)",
          "3. Vertical Drilling Machine (Feed in mm/min or Manual)",
      ],
  )

  if "CNC" in machine_choice:
    st.info(
        "💡 **CNC Calculator Mode:** Uses Spindle RPM and Feed per Revolution"
        " (mm/rev)."
    )
    sub_calc = st.selectbox(
        "CNC Calculation", ["Spindle RPM from Vc", "CNC Machining Time"]
    )
    if "RPM" in sub_calc:
      c1, c2 = st.columns(2)
      with c1:
        vc = st.number_input("Cutting Speed (Vc in m/min)", value=200.0)
      with c2:
        dia = st.number_input("Component Diameter (mm)", value=40.0)
      if st.button("Calculate CNC RPM"):
        if dia > 0:
          rpm = (1000 * vc) / (math.pi * dia)
          st.success(
              f"✅ CNC Spindle Speed: **{rpm:.2f} RPM** (Formula: (1000*Vc)/(pi*D))"
          )
    else:
      c1, c2 = st.columns(2)
      with c1:
        length = st.number_input("Total Cutting Length (mm)", value=80.0)
        feed_rev = st.number_input(
            "Feed Rate (mm/rev) [e.g., 0.15 to 0.25]", value=0.2
        )
      with c2:
        rpm_val = st.number_input("Spindle Speed (RPM)", value=1500.0)
      if st.button("Calculate CNC Time"):
        if feed_rev > 0 and rpm_val > 0:
          t_mins = length / (feed_rev * rpm_val)
          st.success(
              f"✅ CNC Machining Time: **{t_mins:.2f} Minutes** (approx"
              f" {t_mins*60:.1f} Seconds)"
          )

  elif "Traub" in machine_choice:
    st.info(
        "💡 **Traub Automatic Lathe Mode (A25/A42):** Calculated based on Cam"
        " feed rate and Production per Hour."
    )
    c1, c2 = st.columns(2)
    with c1:
      traub_pieces_per_hr = st.number_input(
          "Estimated Production (Pieces per Hour)", value=120.0
      )
      total_order_qty = st.number_input(
          "Total Order Quantity (Pieces)", value=5000.0
      )
    with c2:
      cam_efficiency = st.slider("Traub Machine Efficiency (%)", 50, 100, 85)

    if st.button("Calculate Traub Production Hours"):
      actual_pieces_hr = traub_pieces_per_hr * (cam_efficiency / 100.0)
      total_hours = total_order_qty / actual_pieces_hr
      st.success(
          f"✅ Traub Production Time for {total_order_qty} Nos: **{total_hours:.1f}"
          f" Hours** (~{total_hours/8:.1f} Working Shifts of 8 hrs)"
      )

  else:
    st.info(
        "💡 **Drilling Machine Mode:** Calculated using Feed Rate in mm/min or"
        " Manual feed estimation."
    )
    c1, c2 = st.columns(2)
    with c1:
      drill_depth = st.number_input("Hole Depth / Travel Length (mm)", value=30.0)
      drill_rpm = st.number_input("Drill Spindle RPM", value=800.0)
    with c2:
      feed_per_min = st.number_input(
          "Feed Rate (mm/min) [Drilling Feed]", value=60.0
      )

    if st.button("Calculate Drilling Time"):
      if feed_per_min > 0:
        drill_time_mins = drill_depth / feed_per_min
        st.success(
            f"✅ Drilling Time per Hole: **{drill_time_mins:.2f} Minutes**"
            f" ({drill_time_mins*60:.1f} Seconds)"
        )

# MODULE 2: QUOTATION & OVERHEADS
elif (
    app_mode.startswith("2.")
    or "Quotation" in app_mode
    or "கொட்டேஷன்" in app_mode
):
  st.header(
      "💰 Comprehensive Customer Quotation & Cost Estimator (with All Overheads)"
  )
  st.write(
      "Prepare a 100% practical quotation including Material, Machining Time,"
      " Tool/Drill Wear, EB, Coolant, and Worker Food/Snacks expenses."
  )

  input_mode = st.radio(
      "Select Quotation Input Method:",
      [
          "📁 Option 1: Upload Drawing / Part Photo (Visual Reference)",
          "✍️ Option 2: Manual Data & Dimension Entry",
      ],
  )

  if "Option 1" in input_mode:
    q_photo = st.file_uploader(
        "Upload Part Drawing / Photo for Quotation Reference",
        type=["png", "jpg", "jpeg"],
        key="q_photo_up",
    )
    if q_photo:
      st.image(q_photo, width=250, caption="Quotation Reference Drawing/Photo")
      st.success("✅ Drawing uploaded successfully. Enter costing details below:")

  st.markdown("---")
  st.subheader("📊 Detailed Cost Breakdown (உண்மையான ஒர்க்ஷாப் செலவு கணக்கீடு)")

  c1, c2 = st.columns(2)
  with c1:
    cust_name = st.text_input("Customer Name / Company", "ABC Industries")
    part_name = st.text_input("Component Name", "Bush / Shaft / Pin")
    batch_qty = st.number_input("Batch Order Quantity (Nos)", value=500)
    mat_cost_kg = st.number_input(
        "Raw Material Cost per Kg (₹)", value=85.0, step=1.0
    )
    part_wt = st.number_input("Finished Part Weight (Kg)", value=0.5, step=0.05)

  with c2:
    mach_time = st.number_input(
        "Machining Time per piece (Minutes)", value=4.0, step=0.5
    )
    machine_rate = st.number_input(
        "Machine Hourly Rate (₹/hr) [Depreciation & Rent]",
        value=600.0,
        step=50.0,
    )
    tool_drill_cost = st.number_input(
        "Tool, Insert & Drill Bit Cost allowance per piece (₹)",
        value=3.5,
        step=0.5,
    )
    eb_coolant_cost = st.number_input(
        "EB Bill & Coolant Oil allowance per piece (₹)", value=2.0, step=0.5
    )
    food_snacks_cost = st.number_input(
        "Workers Food, Tea & Snacks allowance per piece (₹)",
        value=2.5,
        step=0.5,
    )
    profit = st.slider("Target Profit Margin (%)", 0, 50, 25)

  if st.button("Generate Professional Quotation"):
    material_total = part_wt * mat_cost_kg
    machining_cost = (machine_rate / 60.0) * mach_time
    total_unit_cost = (
        material_total
        + machining_cost
        + tool_drill_cost
        + eb_coolant_cost
        + food_snacks_cost
    )
    unit_selling_price = total_unit_cost * (1 + profit / 100.0)
    grand_total_amount = unit_selling_price * batch_qty

    st.success("✅ Professional Quotation Generated Successfully!")

    st.markdown(f"### 📋 Quotation Summary for: **{cust_name}**")
    st.write(f"- **Component:** {part_name} | **Batch Qty:** {batch_qty} Nos")

    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Material Cost / pc", f"₹{material_total:.2f}")
    col_b.metric("Machining Cost / pc", f"₹{machining_cost:.2f}")
    col_c.metric(
        "Overheads (Tool+EB+Food)/pc",
        f"₹{tool_drill_cost + eb_coolant_cost + food_snacks_cost:.2f}",
    )
    col_d.metric("Target Profit", f"{profit}%")

    st.markdown("---")
    r1, r2 = st.columns(2)
    r1.metric("Final Unit Selling Price", f"₹{unit_selling_price:.2f} per pc")
    r2.metric(
        f"Grand Total for {batch_qty} Nos", f"₹{grand_total_amount:,.2f}"
    )

# MODULE 3: DASHBOARD OVERVIEW
elif (
    app_mode.startswith("3.")
    or "Dashboard" in app_mode
    or "முகப்பு" in app_mode
):
  st.header("🏠 Megala CNC Mate - Dashboard & Module Overview")
  st.write(
      "Welcome to your offline workshop command center. Here is the summary of"
      " all available modules designed specifically for Nithish's Workshop."
  )

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(label="Total Modules", value="8 Pro Modules")
  with col2:
    st.metric(label="Operation Mode", value="100% Offline 🟢")
  with col3:
    st.metric(label="Language Support", value="6 Languages")
  with col4:
    st.metric(label="App Version", value="Ultimate v17.0")

  st.markdown("---")
  st.subheader("📌 Quick Guide to Available Features in this App:")
  st.markdown("""
    1. **🧮 Machine Calculator:** Accurate calculations tailored for CNC Turning, Traub Automatic Lathes, and Drilling machines.
    2. **💰 Quotation & Overheads:** Includes photo upload or manual entry, plus EB bills, coolant oil, drill/tool wear, and worker food/snacks.
    3. **📸 Drawing & Photo Analysis:** Upload drawings to inspect dimensions and auto-generate G-code.
    4. **📐 Rod & Scrap Calculator:** Calculates pieces per 3m/6m rod, end-bit leftovers, parting blade widths, and scrap weights in Kg.
    5. **📜 Advanced G-Code Generator:** Generates turning, grooving, boring, and drilling programs.
    6. **🏭 Production Days Calculator:** Calculates estimated working days for large target quantities.
    7. **📦 Stock & Inventory Management:** Monitors raw material stock levels and triggers low-stock warnings.
    """)

# MODULE 4: DRAWING & PHOTO ANALYSIS
elif (
    app_mode.startswith("4.") or "Analysis" in app_mode or "பகுப்பாய்வு" in app_mode
):
  st.header("📸 Component Drawing / Photo Analyzer & G-Code Generator")
  uploaded_file = st.file_uploader(
      "Upload Part Drawing / Photo (PNG, JPG)", type=["png", "jpg", "jpeg"]
  )

  if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Drawing Reference", use_column_width=True)
    st.success("✅ Image Uploaded Successfully for Reference!")

    op_type = st.selectbox(
        "Machining Operation",
        ["Turning & Facing", "Stepped Turning", "Grooving", "Boring"],
    )
    part_dia = st.number_input("Major Diameter / Hole Diameter (mm)", value=40.0)
    part_length = st.number_input("Total Machining Length (mm)", value=60.0)

    if st.button("Generate Program from Drawing"):
      gcode_out = f"""
O1001 (MEGALA CNC MATE - DRAWING PROGRAM)
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
    st.info("💡 Upload a component photo or drawing to begin.")

# MODULE 5: ROD, END-BIT & SCRAP CALCULATOR
elif app_mode.startswith("5.") or "Scrap" in app_mode or "ராட்" in app_mode:
  st.header(
      "📐 Precise Rod, End-Bit, Grooving & Scrap Calculator (Length & Weight)"
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
        ],
    )
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
    standard_rod_length_m = st.number_input(
        "Standard Raw Rod Length Supplied (Meters)", value=6.0
    )

  with col_b:
    if profile_type == "Round Bar":
      dia = st.number_input("Outer Diameter (mm)", value=40.0)
    elif profile_type == "Hexagon Bar":
      across_flat = st.number_input("Across Flats (mm)", value=40.0)
    elif profile_type == "Square Bar":
      side_w = st.number_input("Side Width (mm)", value=40.0)
    elif profile_type == "Tube / Hollow Pipe":
      outer_d = st.number_input("Outer Diameter (mm)", value=50.0)
      inner_d = st.number_input("Inner Bore Diameter (mm)", value=25.0)
    else:
      f_width = st.number_input("Plate Width (mm)", value=60.0)
      f_thick = st.number_input("Plate Thickness (mm)", value=12.0)

    part_drawing_length = st.number_input(
        "Finished Part Length (mm)", value=45.0
    )
    facing_allowance = st.number_input(
        "Facing Allowance per piece (mm)", value=2.0
    )
    parting_tool_width = st.number_input(
        "Parting / Grooving Tool Blade Width (mm)", value=3.0
    )

  if st.button("Calculate Exact Pieces, End-Bit & Scrap"):
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
    end_bit_weight_kg = (
        (vol_per_cm * (end_bit_leftover_mm / 10.0)) * density
    ) / 1000.0
    cutting_blade_scrap_weight_kg = (
        (vol_per_cm * (total_cutting_blade_scrap_mm / 10.0)) * density
    ) / 1000.0
    total_scrap_weight_kg = end_bit_weight_kg + cutting_blade_scrap_weight_kg

    st.success("✅ Rod & Scrap Calculation Completed!")
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Pieces per Rod", f"{pieces_per_rod} Nos")
    r2.metric("End-Bit Waste", f"{end_bit_leftover_mm:.1f} mm")
    r3.metric("Total Scrap Weight", f"{total_scrap_weight_kg:.3f} Kg")
    r4.metric("Rod Gross Weight", f"{total_gross_weight_kg:.3f} Kg")

# MODULE 6: ADVANCED G-CODE GENERATOR
elif app_mode.startswith("6.") or "G-Code" in app_mode or "ஜி-கோடு" in app_mode:
  st.header("📜 Advanced CNC G-Code Generator (Turning, Grooving & Boring)")
  op_choice = st.selectbox(
      "Select Operation",
      [
          "OD Turning & Facing",
          "OD Grooving & Parting",
          "ID Boring",
          "Drilling Cycle",
      ],
  )

  c1, c2 = st.columns(2)
  with c1:
    prog_no = st.text_input("Program Number", "O0001")
    s_speed = st.number_input("Spindle Speed (RPM)", value=1500)
    feed_rate = st.number_input("Feed Rate (mm/rev)", value=0.15)
  with c2:
    if "Turning" in op_choice:
      dia_val = st.number_input("Target Outer Diameter (mm)", value=40.0)
      len_val = st.number_input("Machining Length (mm)", value=50.0)
    elif "Grooving" in op_choice:
      groove_z = st.number_input(
          "Groove Distance from Reference Z (mm)", value=-25.0
      )
      groove_w = st.number_input("Groove Width (mm)", value=3.0)
      groove_d = st.number_input("Groove Depth Diameter (mm)", value=32.0)
    elif "Boring" in op_choice:
      bore_dia = st.number_input("Final Bore Hole Diameter (mm)", value=25.0)
      bore_depth = st.number_input("Boring Depth (mm)", value=40.0)
    else:
      drill_depth = st.number_input("Drill Hole Depth (mm)", value=30.0)

  if st.button("Generate Complete G-Code"):
    if "Turning" in op_choice:
      gcode_final = f"""
({prog_no} - MEGALA MATE OD TURNING)
G21 G90 G40 G80 G18
M03 S{s_speed}
G00 X{dia_val + 4.0} Z2.0
G01 Z0.0 F{feed_rate}
G01 X{dia_val} F0.12
G01 Z-{len_val} F{feed_rate}
G00 X{dia_val + 5.0}
G00 Z50.0
M05
M30
"""
    elif "Grooving" in op_choice:
      gcode_final = f"""
({prog_no} - MEGALA MATE GROOVING)
G21 G90 G40 G80 G18
M03 S{int(s_speed * 0.7)}
G00 X{groove_d + 10.0} Z{groove_z}
G01 X{groove_d} F0.08
G04 P500 (DWELL FOR CHIP BREAK)
G00 X{groove_d + 10.0}
G00 Z50.0
M05
M30
"""
    elif "Boring" in op_choice:
      gcode_final = f"""
({prog_no} - MEGALA MATE ID BORING)
G21 G90 G40 G80 G18
M03 S{s_speed}
G00 X{bore_dia - 2.0} Z2.0
G01 Z-{bore_depth} F{feed_rate}
G01 X{bore_dia} F0.1
G00 Z50.0
M05
M30
"""
    else:
      gcode_final = f"""
({prog_no} - MEGALA MATE DRILLING)
G21 G90 G40 G80 G18
M03 S{s_speed}
G00 X0.0 Z2.0
G83 Z-{drill_depth} R1.0 Q5.0 F{feed_rate}
G80
G00 Z50.0
M05
M30
"""
    st.code(gcode_final, language="text")
    st.download_button(
        "📥 Download G-Code File (.nc)",
        data=gcode_final,
        file_name="program.nc",
        mime="text/plain",
    )

# MODULE 7: PRODUCTION DAYS CALCULATOR
elif (
    app_mode.startswith("7.")
    or "Production" in app_mode
    or "உற்பத்தி" in app_mode
):
  st.header("🏭 Production & Large Order Days Calculator")
  c1, c2 = st.columns(2)
  with c1:
    job_no = st.text_input("Job Order Number", "JOB-2026-5000")
    total_target = st.number_input(
        "Total Target Quantity (Pieces)", value=5000.0
    )
    cycle_time_sec = st.number_input(
        "Cycle Time per Piece (Seconds)", value=45.0
    )
  with c2:
    completed_qty = st.number_input(
        "Already Completed Quantity", value=1200.0
    )
    shift_hours = st.selectbox(
        "Working Hours per Day", [8, 10, 12, 16, 24], index=2
    )
    efficiency = st.slider("Machine Efficiency (%)", 50, 100, 85)

  if st.button("Calculate Completion Days"):
    remaining_qty = max(0.0, total_target - completed_qty)
    total_rem_seconds = remaining_qty * cycle_time_sec
    actual_rem_hours = (total_rem_seconds / 3600.0) / (efficiency / 100.0)
    required_days = actual_rem_hours / shift_hours
    pct = (completed_qty / total_target) * 100
    st.progress(min(pct / 100.0, 1.0))

    st.success("✅ Production & Timeline Analysis Completed!")
    r1, r2, r3 = st.columns(3)
    r1.metric("Completion Status", f"{pct:.1f}%")
    r2.metric("Remaining Hours", f"{actual_rem_hours:.1f} Hours")
    r3.metric("Estimated Days Required", f"{required_days:.1f} Days")

# MODULE 8: STOCK MANAGEMENT
elif app_mode.startswith("8.") or "Stock" in app_mode or "ஸ்டாக்" in app_mode:
  st.header("📦 Stock & Inventory Management")
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
    "<p style='text-align: center; color: gray;'>© 2026 Megala CNC Mate | Professional"
    " Workshop Automation (100% Offline Ready)</p>",
    unsafe_allow_html=True,
)
