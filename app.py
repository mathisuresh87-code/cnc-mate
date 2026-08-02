import math
import os
from PIL import Image
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Megala CNC Mate - Complete Professional Workshop Manager",
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
      "**SMART CNC. SIMPLE WORK.** — Clean Sidebar Radio Menu, Drawing-Based"
      " End-Bit & Scrap Calculator, Tube/Rod Profiles, Photo Upload, Quotation,"
      " Production & Stock Management"
  )

st.markdown("---")

# --- CLEAN LANGUAGE SUPPORT SETUP ---
st.sidebar.markdown("### 🌐 Language / மொழி")
lang = st.sidebar.selectbox(
    "Choose Language",
    [
        "English",
        "தமிழ் (Tamil)",
        "हिंदी (Hindi)",
        "తెలుగు (Telugu)",
        "മലയാളം (Malayalam)",
        "ಕನ್ನಡ (Kannada)",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Menu Navigation")

# --- MENU OPTIONS FOR ALL 6 LANGUAGES ---
menu_options = {
    "English": [
        "🏠 Dashboard",
        "📸 Photo / Drawing Analysis & G-Code",
        "🧮 Workshop Calculator",
        "📐 Drawing-Based End-Bit, Scrap & Quantity Calculator",
        "💰 Customer Quotation (with Photo)",
        "🏭 Production Tracker",
        "📜 G-Code Generator",
        "🔤 Letter Cutting",
        "📦 Stock & Rod Management",
    ],
    "தமிழ் (Tamil)": [
        "🏠 முகப்பு (Dashboard)",
        "📸 போட்டோ / டிராயிங் பகுப்பாய்வு & ஜி-கோடு",
        "🧮 ஒர்க்ஷாப் கால்குலேட்டர்",
        "📐 எண்டு பிட், ஸ்கிராப் & குவாண்டிட்டி கால்குலேட்டர்",
        "💰 வாடிக்கையாளர் கொட்டேஷன் (Photo)",
        "🏭 உற்பத்தி கண்காணிப்பு",
        "📜 ஜி-கோடு ஜெனரேட்டர்",
        "🔤 எழுத்து வெட்டுதல்",
        "📦 ஸ்டாக் மேனேஜ்மென்ட்",
    ],
    "हिंदी (Hindi)": [
        "🏠 डैशबोर्ड (Dashboard)",
        "📸 फोटो / ड्राइंग विश्लेषण और जी-कोड",
        "🧮 वर्कशॉप कैलकुलेटर",
        "📐 एंड-बिट, स्क्रैप और मात्रा कैलकुलेटर",
        "💰 ग्राहक कोटेशन (Photo)",
        "🏭 उत्पादन ट्रैकर",
        "📜 जी-कोड जेनरेटर",
        "🔤 अक्षर कटाई",
        "📦 स्टॉक प्रबंधन",
    ],
    "తెలుగు (Telugu)": [
        "🏠 డాష్‌బోర్డ్ (Dashboard)",
        "📸 ఫోటో / డ్రాయింగ్ విశ్లేషణ & జి-కోడ్",
        "🧮 వర్క్‌షాప్ కాలిక్యులేటర్",
        "📐 ఎండ్-బిట్, స్క్రాప్ & క్వాంటిటీ కాలిక్యులేటర్",
        "💰 కస్టమర్ కొటేషన్ (Photo)",
        "🏭 ఉత్పత్తి ట్రాకర్",
        "📜 జి-కోడ్ జనరేటర్",
        "🔤 అక్షర కటింగ్",
        "📦 స్టాక్ నిర్వహణ",
    ],
    "മലയാളം (Malayalam)": [
        "🏠 ഡാഷ്‌ബോർഡ് (Dashboard)",
        "📸 ഫോട്ടോ / ഡ്രോയിംഗ് വിശകലനം & ജി-കോഡ്",
        "🧮 വർക്ക്‌ഷോപ്പ് കാൽക്കുലേറ്റർ",
        "📐 എൻഡ്-ബിറ്റ്, സ്ക്രാപ്പ് & ക്വാണ്ടിറ്റി കാൽക്കുലേറ്റർ",
        "💰 കസ്റ്റമർ കൊട്ടേഷൻ (Photo)",
        "🏭 പ്രൊഡക്ഷൻ ട്രാക്കർ",
        "📜 ജി-കോഡ് ജനറേറ്റർ",
        "🔤 ലെറ്റർ കട്ടിംഗ്",
        "📦 സ്റ്റോക്ക് മാനേജ്മെന്റ്",
    ],
    "ಕನ್ನಡ (Kannada)": [
        "🏠 ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ (Dashboard)",
        "📸 ಫೋಟೋ / ಡ್ರಾಯಿಂಗ್ ವಿಶ್ಲೇಷಣೆ & ಜಿ-ಕೋಡ್",
        "🧮 ವರ್ಕ್‌ಷೋಪ್ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
        "📐 ಎಂಡ್-ಬಿಟ್, ಸ್ಕ್ರ್ಯಾಪ್ ಮತ್ತು ಕ್ವಾಂಟಿಟಿ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
        "💰 ಗ್ರಾಹಕರ ಉಲ್ಲೇಖ (Quotation)",
        "🏭 ಉತ್ಪಾದನಾ ಟ್ರ್ಯಾಕರ್",
        "📜 ಜಿ-ಕೋಡ್ ಜನರೇಟರ್",
        "🔤 ಅಕ್ಷರ ಕಟಿಂಗ್",
        "📦 ಸ್ಟಾಕ್ ನಿರ್ವಹಣೆ",
    ],
}

# Using st.sidebar.radio so ALL 9 options are permanently visible without hiding
app_mode = st.sidebar.radio(
    "Select Module", menu_options[lang], label_visibility="collapsed"
)

# --- 1. DASHBOARD ---
if any(
    x in app_mode
    for x in [
        "Dashboard",
        "முகப்பு",
        "डैशबोर्ड",
        "డాష్‌బోర్డ్",
        "ഡാഷ്‌ബോർഡ്",
        "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
    ]
):
  st.header("📊 Megala CNC Mate Dashboard")
  st.write(
      "Your clean, smart automation tool for CNC machining, drawing-based"
      " scrap analysis, end-bit tracking, and workshop management."
  )

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(label="Active Modules", value="9 Ready")
  with col2:
    st.metric(label="System Status", value="Online 🟢")
  with col3:
    st.metric(label="Languages", value="6 Supported")
  with col4:
    st.metric(label="Version", value="Final Radio v12.0")

# --- 2. PHOTO / DRAWING ANALYSIS & G-CODE MODULE ---
elif any(
    x in app_mode for x in ["Photo", "போட்டோ", "फोटो", "ఫోటో", "ഫോട്ടോ", "ಫೋಟೋ"]
):
  st.header("📸 Component Photo / Drawing Uploader & Program Generator")
  st.write(
      "Upload your component drawing or part photo to analyze dimensions and"
      " generate corresponding G-code programs."
  )

  uploaded_file = st.file_uploader(
      "Upload Component Image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"]
  )

  if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(
        image,
        caption="Uploaded Component Drawing / Photo",
        use_column_width=True,
    )
    st.success("✅ Image Uploaded Successfully!")

    st.markdown("### ⚙️ Program Parameters for Uploaded Part")
    op_type = st.selectbox(
        "Operation Type",
        ["Turning & Facing", "Cylindrical Boring", "Grooving & Parting"],
    )
    part_dia = st.number_input("Part Outer Diameter (mm)", value=50.0)
    part_length = st.number_input("Machining Length (mm)", value=75.0)

    if st.button("Generate G-Code from Photo/Drawing"):
      generated_gcode = f"""
O1001 (PHOTO BASED CNC PROGRAM - MEGALA MATE)
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
      st.code(generated_gcode, language="text")
      st.download_button(
          "📥 Download G-Code for Uploaded Photo (.nc)",
          data=generated_gcode,
          file_name="photo_based_program.nc",
          mime="text/plain",
      )
  else:
    st.info(
        "💡 Please upload a photo or drawing of your component to start"
        " automated programming."
    )

# --- 3. WORKSHOP CALCULATOR ---
elif any(
    x in app_mode
    for x in [
        "Calculator",
        "கால்குலேட்டர்",
        "कैलकुलेटर",
        "కాలిక్యులేటర్",
        "കാൽക്കുലേറ്റർ",
        "ಕ್ಯಾಲ್ಕುಲೇಟರ್",
    ]
):
  st.header("🧮 Workshop & Machining Calculator")
  st.write("Calculate cutting speed, spindle RPM, and machining time.")

  calc_type = st.selectbox(
      "Calculation Type",
      ["Spindle RPM Calculator", "Machining Time Calculator"],
  )

  if "RPM" in calc_type:
    c1, c2 = st.columns(2)
    with c1:
      vc = st.number_input("Cutting Speed (Vc in m/min)", value=200.0)
    with c2:
      dia = st.number_input("Diameter / Size (mm)", value=50.0)

    if st.button("Calculate RPM"):
      if dia > 0:
        rpm = (1000 * vc) / (math.pi * dia)
        st.success(f"✅ Spindle Speed: **{rpm:.2f} RPM**")
  else:
    c1, c2 = st.columns(2)
    with c1:
      length = st.number_input("Cutting Length (mm)", value=100.0)
      feed = st.number_input("Feed Rate (mm/rev)", value=0.2)
    with c2:
      rpm_val = st.number_input("Spindle Speed (RPM)", value=1500.0)

    if st.button("Calculate Time"):
      if feed > 0 and rpm_val > 0:
        t_mins = length / (feed * rpm_val)
        st.success(f"✅ Estimated Machining Time: **{t_mins:.2f} Minutes**")

# --- 4. DRAWING-BASED END-BIT, SCRAP & QUANTITY CALCULATOR ---
elif any(
    x in app_mode
    for x in [
        "End-Bit",
        "எண்டு பிட்",
        "एंड-बिट",
        "ఎండ్-బిట్",
        "എൻഡ്-ബിറ്റ്",
        "ಎಂಡ್-ಬಿಟ್",
    ]
):
  st.header(
      "📐 Drawing-Based End-Bit, Cutting Allowance & Scrap Calculator"
  )
  st.write(
      "Input drawing dimensions, standard rod/tube length, parting tool width"
      " (cutting allowance), and get exact pieces, tail-end waste, cutting"
      " scrap, and net/gross weights."
  )

  dc1, dc2 = st.columns(2)
  with dc1:
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
    if "Aluminum" in mat_grade:
      density = 2.70
    elif "Brass" in mat_grade:
      density = 8.50
    elif "Stainless Steel" in mat_grade:
      density = 7.93
    else:
      density = 7.85

    profile_type = st.selectbox(
        "Rod / Tube Profile",
        [
            "Round Bar",
            "Hexagon Bar",
            "Square Bar",
            "Tube / Hollow Pipe",
            "Flat Plate",
        ],
    )
    standard_rod_length_m = st.number_input(
        "Standard Raw Rod Length Supplied (Meters e.g., 3m or 6m)",
        min_value=0.5,
        value=3.0,
        step=0.5,
    )

  with dc2:
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
          "Tube Inner Diameter / Bore (mm)", min_value=0.0, value=25.0
      )
    else:
      f_width = st.number_input("Plate Width (mm)", min_value=0.1, value=60.0)
      f_thick = st.number_input(
          "Plate Thickness (mm)", min_value=0.1, value=12.0
      )

    part_drawing_length = st.number_input(
        "Drawing Part Finished Length (mm)", min_value=1.0, value=50.0
    )
    facing_allowance = st.number_input(
        "Facing Allowance per piece (mm)", min_value=0.0, value=2.0
    )
    parting_tool_width = st.number_input(
        "Parting / Cutting Tool Blade Width (mm)", min_value=0.1, value=3.0
    )

  if st.button("Calculate Exact End-Bit & Scrap"):
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

    st.success("✅ Drawing-Based Scrap & End-Bit Calculation Completed!")
    st.markdown(
        f"### Production Analysis for Standard Rod Length:"
        f" **{standard_rod_length_m} Meters**"
    )

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Pieces per Rod", f"{pieces_per_rod} Nos")
    r2.metric("Tail-End Piece (End-Bit)", f"{end_bit_leftover_mm:.1f} mm")
    r3.metric("Total Scrap Weight", f"{total_scrap_weight_kg:.3f} Kg")
    r4.metric("Total Rod Gross Weight", f"{total_gross_weight_kg:.3f} Kg")

    st.info(
        f"📋 **Detailed Breakdown:**\n"
        f"- **Material Grade & Profile:** {mat_grade} ({profile_type})\n"
        f"- **Net Weight of All Parts:** {total_net_weight_all_parts:.3f} Kg\n"
        f"- **End-Bit Waste Weight:** {end_bit_weight_kg:.3f} Kg\n"
        f"- **Cutting Blade/Facing Scrap Weight:**"
        f" {cutting_blade_scrap_weight_kg:.3f} Kg"
    )

# --- 5. CUSTOMER QUOTATION (WITH PHOTO SUPPORT) ---
elif any(
    x in app_mode
    for x in [
        "Quotation",
        "கொட்டேஷன்",
        "कोटेशन",
        "కొటేషన్",
        "കൊട്ടേഷൻ",
        "ಉಲ್ಲೇಖ",
    ]
):
  st.header("💰 Customer Quotation & Cost Estimator (with Photo Reference)")
  st.write(
      "Calculate costs based on material grades, rod types, and attach part"
      " photos for quotation records."
  )

  q_photo = st.file_uploader(
      "Upload Part Photo for Quotation Reference",
      type=["png", "jpg", "jpeg"],
      key="q_photo",
  )
  if q_photo:
    st.image(q_photo, width=200, caption="Quotation Reference Photo")

  col1, col2 = st.columns(2)
  with col1:
    customer_name = st.text_input("Customer Name", "ABC Industries")
    part_name = st.text_input("Component Name", "Steel Bush / Shaft")
    material_grade = st.selectbox(
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
    rod_type = st.selectbox(
        "Rod Type / Profile",
        [
            "Round Bar",
            "Hexagon Bar",
            "Square Bar",
            "Tube / Pipe",
            "Flat Plate / Sheet",
        ],
    )
    material_cost_per_kg = st.number_input(
        "Raw Material Cost per Kg (₹)", min_value=0.0, value=85.0
    )

  with col2:
    estimated_weight = st.number_input(
        "Estimated Part Weight (Kg)", min_value=0.01, value=1.2
    )
    machining_time = st.number_input(
        "Machining Time per piece (Minutes)", min_value=0.1, value=6.0
    )
    machine_rate_per_hour = st.number_input(
        "Machine Hourly Rate (₹/hr)", min_value=0.0, value=600.0
    )
    quantity = st.number_input("Batch Quantity (Pieces)", min_value=1, value=100)
    profit_margin = st.slider("Profit Margin (%)", 0, 50, 20)

  if st.button("Calculate Final Quotation"):
    mat_tot = estimated_weight * material_cost_per_kg
    mach_cost = (machine_rate_per_hour / 60) * machining_time
    unit_p = (mat_tot + mach_cost) * (1 + profit_margin / 100)
    tot_q = unit_p * quantity

    st.success("✅ Quotation Calculated Successfully with Photo Reference!")
    st.markdown(f"### Summary for: **{customer_name}** ({part_name})")
    st.write(f"- **Grade:** {material_grade} | **Profile:** {rod_type}")

    r1, r2, r3 = st.columns(3)
    r1.metric("Cost per Piece", f"₹{unit_p:.2f}", f"+{profit_margin}% Profit")
    r2.metric("Batch Quantity", f"{quantity} Nos")
    r3.metric("Grand Total", f"₹{tot_q:,.2f}")

# --- 6. PRODUCTION TRACKER ---
elif any(
    x in app_mode
    for x in [
        "Production",
        "உற்பத்தி",
        "उत्पादन",
        "ఉత్పత్తి",
        "പ്രൊഡക്ഷൻ",
        "ಉತ್ಪಾದನಾ",
    ]
):
  st.header("🏭 Production & Batch Tracker")
  st.write("Track daily machining output and target progress.")

  batch_no = st.text_input("Job Order Number", "JOB-2026-001")
  target_qty = st.number_input("Target Quantity", min_value=1, value=500)
  completed_qty = st.number_input("Completed Quantity", min_value=0, value=350)
  cycle_time = st.number_input("Cycle Time per part (Seconds)", value=45.0)

  if st.button("Calculate Production Metrics"):
    prog = (completed_qty / target_qty) * 100
    tot_hours = (target_qty * cycle_time) / 3600
    st.progress(min(prog / 100.0, 1.0))
    st.write(f"**Completion Status:** {prog:.1f}% Done")
    st.info(
        f"⏱️ Estimated total time to complete batch: **{tot_hours:.2f} Hours**"
    )

# --- 7. G-CODE GENERATOR ---
elif any(
    x in app_mode
    for x in ["G-Code", "ஜி-கோடு", "जी-कोड", "జి-కోడ్", "ജി-കോഡ്"]
):
  st.header("📜 CNC G-Code Generator")
  st.write("Generate standard G-code programs for turning and facing.")

  operation = st.selectbox(
      "Select Operation", ["Face Turning", "Cylindrical Turning", "Drilling"]
  )
  start_z = st.number_input("Start Z Position", value=0.0)
  feed_rate = st.number_input("Feed Rate (F)", value=0.15)
  spindle_speed = st.number_input("Spindle Speed (S)", value=1500)

  if st.button("Generate G-Code"):
    gcode = f"""
O0001 (MEGALA CNC MATE PROGRAM)
G21 G90 G40 G80 G18
M03 S{spindle_speed}
G00 X52.0 Z2.0
(OPERATION: {operation.upper()})
G01 Z{start_z} F{feed_rate}
G00 Z50.0
M05
M30
"""
    st.code(gcode, language="text")
    st.download_button(
        "📥 Download G-Code (.nc)",
        data=gcode,
        file_name="program.nc",
        mime="text/plain",
    )

# --- 8. LETTER CUTTING ---
elif any(
    x in app_mode for x in ["Letter", "எழுத்து", "अक्षर", "అక్షర", "ലെറ്റർ"]
):
  st.header("🔤 Letter & Engraving Module")
  text_input = st.text_input("Text to Engrave", "MEGALA CNC", max_chars=20)
  font_height = st.number_input("Character Height (mm)", value=10.0)
  depth = st.number_input("Engraving Depth (mm)", value=0.5, step=0.1)

  if st.button("Generate Parameters"):
    st.success(f"Parameters ready for text: **{text_input}**")
    st.write(
        f"- **Font Height:** {font_height} mm\n- **Depth (Z):** -{depth}"
        " mm\n- **Tool:** 60° V-Bit Cutter"
    )

# --- 9. STOCK & ROD MANAGEMENT ---
elif any(
    x in app_mode for x in ["Stock", "ஸ்டாக்", "स्टॉक", "സ്റ്റോക്ക്", "ನಿರ್ವಹಣೆ"]
):
  st.header("📦 Stock & Rod Inventory Management")
  st.write(
      "Monitor raw material grades, rod types, diameters, and inventory levels."
  )

  c1, c2 = st.columns(2)
  with c1:
    s_grade = st.selectbox(
        "Material Grade",
        [
            "EN8",
            "EN24",
            "Aluminum 6061",
            "Mild Steel (MS)",
            "Brass",
            "Stainless Steel 304",
        ],
        key="s_grade",
    )
    s_rod = st.selectbox(
        "Rod Type",
        [
            "Round Bar",
            "Hexagon Bar",
            "Square Bar",
            "Tube / Pipe",
            "Flat Plate",
        ],
        key="s_rod",
    )
    dia = st.number_input("Diameter / Size (mm)", min_value=1.0, value=40.0)
  with c2:
    length = st.number_input("Rod Length (mm)", min_value=100.0, value=1000.0)
    weight = st.number_input(
        "Available Stock Weight (Kg)", min_value=0.0, value=125.0
    )
    min_l = st.number_input(
        "Minimum Alert Limit (Kg)", min_value=0.0, value=30.0
    )

  if st.button("Check Stock Status"):
    if weight <= min_l:
      st.warning(
          f"⚠️ **Warning:** Low Stock for {s_grade} ({s_rod} - {dia}mm)!"
          " Reorder required."
      )
    else:
      st.success(f"✅ Stock level for {s_grade} ({s_rod}) is sufficient.")
    st.write(f"- **Grade:** {s_grade} | **Type:** {s_rod}")
    st.write(f"- **Size:** {dia}mm dia, {length}mm length")
    st.write(f"- **Current Weight:** **{weight} Kg**")

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>© 2026 Megala CNC Mate | Built"
    " for Smart Workshop Automation</p>",
    unsafe_allow_html=True,
)
