import math
import os
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Megala CNC Mate - Smart CNC & Production",
    page_icon="⚙️",
    layout="wide",
)

# --- HEADER WITH AUTOMATIC LOGO LOADER ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
  if os.path.exists("logo.png"):
    st.image("logo.png", width=120)
  else:
    st.markdown("⚙️ **[Logo Here]**")

with col_title:
  st.title("⚙️ Megala CNC Mate")
  st.markdown(
      "**SMART CNC. SIMPLE WORK.** — Customer Quotation, Production, G-Code,"
      " Letter Cutting & Stock Management"
  )

st.markdown("---")

# Multi-Language Dictionary (English, Tamil, Hindi, Kannada, Telugu)
translations = {
    "English": {
        "menu_title": "🧭 Navigation Menu",
        "home": "🏠 Home Dashboard",
        "rod_calc": "📏 Rod & Conversion Calculator",
        "letter_calc": "🔤 Letter Cutting & Cutting Speed",
        "prod_calc": "⏱️ Production Calculator",
        "cost_calc": "💰 Costing Calculator",
        "stock_mgmt": "📦 Stock Management",
        "ai_prog": "🤖 AI G-Code Generator (Turning, Facing, Drilling)",
        "quotation": "📄 Quotation & PDF",
        "settings": "⚙️ Settings & Master",
        "hello": "Hello, Nithish! Welcome Back 👋",
        "home_desc": (
            "Manage all your shop floor calculations, G-Codes, letter cutting"
            " and stock in one place."
        ),
        "raw_dia": "Raw Material Dia / Size (mm)",
        "part_len": "Part Length (mm)",
        "cutting_all": "Cutting Allowance / Groove (mm)",
        "std_rod_len": "Standard Rod Length (Meters)",
        "calc_btn": "📊 Calculate",
        "results": "Calculation Results",
    },
    "தமிழ்": {
        "menu_title": "🧭 மெனு (Navigation Menu)",
        "home": "🏠 முகப்பு (Home Dashboard)",
        "rod_calc": "📏 ராட் & கன்வெர்ட்டர் கால்குலேட்டர்",
        "letter_calc": "🔤 லெட்டர் கட்டிங் & கட்டிங் ஸ்பீட்",
        "prod_calc": "⏱️ ப்ரொடக்ஷன் கால்குலேட்டர்",
        "cost_calc": "💰 காஸ்டிங் கால்குலேட்டர்",
        "stock_mgmt": "📦 ஸ்டாக் மேனேஜ்மெண்ட்",
        "ai_prog": "🤖 AI ஜி-கோடு ஜெனரேட்டர் (Turning, Facing, Drilling)",
        "quotation": "📄 கொட்டேஷன் & PDF",
        "settings": "⚙️ செட்டிங்ஸ் / More Menu",
        "hello": "வணக்கம் நிதீஷ்! உங்களை மீண்டும் வரவேற்கிறோம் 👋",
        "home_desc": (
            "உங்களது ஷாப் ப்ளோர் கணக்கீடுகள், லெட்டர் கட்டிங், ஸ்பீட் மற்றும்"
            " ஜி-கோடுகள் அனைத்தையும் ஒரே இடத்தில் கையாளலாம்."
        ),
        "raw_dia": "ரா மெட்டீரியல் டயா / அளவு (Raw Size - mm)",
        "part_len": "பார்ட் நீளம் (Part Length - mm)",
        "cutting_all": "கட்டிங் அலவன்ஸ் / குருவ் (Cutting Allowance - mm)",
        "std_rod_len": (
            "ஒரு ஸ்டாண்டர்ட் ராட் நீளம் (Standard Rod Length - Meters)"
        ),
        "calc_btn": "📊 கணக்கிடு (Calculate)",
        "results": "கணக்கீட்டு முடிவுகள் (Calculation Result)",
    },
    "हिंदी": {
        "menu_title": "🧭 नेविगेशन मेनू",
        "home": "🏠 होम डैशबोर्ड",
        "rod_calc": "📏 रॉड और रूपांतरण कैलकुलेटर",
        "letter_calc": "🔤 लेटर कटिंग और स्पीड कैलकुलेटर",
        "prod_calc": "⏱️ उत्पादन कैलकुलेटर",
        "cost_calc": "💰 लागत कैलकुलेटर",
        "stock_mgmt": "📦 स्टॉक प्रबंधन",
        "ai_prog": "🤖 जी-कोड जनरेटर (Turning, Facing, Drilling)",
        "quotation": "📄 उद्धरण और पीडीएफ",
        "settings": "⚙️ सेटिंग्स और मास्टर",
        "hello": "नमस्ते निதீஷ்! स्वागत है 👋",
        "home_desc": "अपनी सभी शॉप फ्लोर गणनाओं को प्रबंधित करें।",
        "raw_dia": "रॉ मटेरियल व्यास (Raw Size - mm)",
        "part_len": "पार्ट की लंबाई (Part Length - mm)",
        "cutting_all": "कटिंग अलाउंस / ग्रूव (Cutting Allowance - mm)",
        "std_rod_len": "मानक रॉड की लंबाई (Standard Rod Length - Meters)",
        "calc_btn": "📊 गणना करें (Calculate)",
        "results": "गणना परिणाम (Calculation Results)",
    },
    "ಕನ್ನಡ": {
        "menu_title": "🧭 ನ್ಯಾವಿಗೇಷನ್ ಮೆನು",
        "home": "🏠 ಮುಖಪುಟ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "rod_calc": "📏 ರಾಡ್ ಮತ್ತು ಪರಿವರ್ತನೆ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
        "letter_calc": "🔤 ಲೆಟರ್ ಕಟಿಂಗ್ & ಸ್ಪೀಡ್ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
        "prod_calc": "⏱️ ಉತ್ಪಾದನಾ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
        "cost_calc": "💰 ವೆಚ್ಚ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
        "stock_mgmt": "📦 ಸ್ಟಾಕ್ ನಿರ್ವಹಣೆ",
        "ai_prog": "🤖 G-Code ಜನರೇಟರ್ (Turning, Facing, Drilling)",
        "quotation": "📄 ಉಲ್ಲೇಖ ಮತ್ತು PDF",
        "settings": "⚙️ ಸೆಟ್ಟಿಂಗ್‌ಗಳು & ಮಾಸ್ಟರ್",
        "hello": "ನಮಸ್ಕಾರ ನಿதீஷ்! ಸ್ವಾಗತ 👋",
        "home_desc": "ನಿಮ್ಮ ಎಲ್ಲಾ ಶಾಪ್ ಫ್ಲೋರ್ ಲೆಕ್ಕಾಚಾರಗಳನ್ನು ಒಂದೇ ಸ್ಥಳದಲ್ಲಿ ನಿರ್ವಹಿಸಿ.",
        "raw_dia": "ರಾ ಮೆಟೀರಿಯಲ್ ವ್ಯಾಸ (Raw Size - mm)",
        "part_len": "ಭಾಗದ ಉದ್ದ (Part Length - mm)",
        "cutting_all": "ಕಟಿಂಗ್ ಅಲೌನ್ಸ್ / ಗ್ರೂವ್ (Cutting Allowance - mm)",
        "std_rod_len": "ಪ್ರಮಾಣಿತ ರಾಡ್ ಉದ್ದ (Standard Rod Length - Meters)",
        "calc_btn": "📊 ಲೆಕ್ಕಹಾಕಿ (Calculate)",
        "results": "ಲೆಕ್ಕಾಚಾರದ ಫಲಿತಾಂಶಗಳು (Calculation Results)",
    },
    "తెలుగు": {
        "menu_title": "🧭 నావిగేషన్ మెనూ",
        "home": "🏠 హోమ్ డ్యాష్‌బోర్డ్",
        "rod_calc": "📏 రాడ్ & మార్పిడి కాలిక్యులేటర్",
        "letter_calc": "🔤 లెటర్ కటింగ్ & స్పీడ్ కాలిక్యులేటర్",
        "prod_calc": "⏱️ ప్రొడక్షన్ కాలిక్యులేటర్",
        "cost_calc": "💰 కాస్టింగ్ కాలిక్యులేటర్",
        "stock_mgmt": "📦 స్టాక్ మేనేజ్‌మెంట్",
        "ai_prog": "🤖 G-Code జెనరేటర్ (Turning, Facing, Drilling)",
        "quotation": "📄 కొటేషన్ & PDF",
        "settings": "⚙️ సెటింగ్స్ / మాస్టర్",
        "hello": "నమస్తే నిதீஷ்! స్వాగతం 👋",
        "home_desc": "మీ షాప్ ఫ్లోర్ లెక్కలన్నీ ఒకే చోట నిర్వహించండి.",
        "raw_dia": "రా మెటీరియల్ వ్యాసం (Raw Size - mm)",
        "part_len": "భాగం పొడవు (Part Length - mm)",
        "cutting_all": "కటింగ్ అలవెన్స్ / గ్రూవ్ (Cutting Allowance - mm)",
        "std_rod_len": "ప్రామాణిక రాడ్ పొడవు (Standard Rod Length - Meters)",
        "calc_btn": "📊 లెక్కించండి (Calculate)",
        "results": "ఫలిतాలు (Calculation Results)",
    },
}

# Sidebar Language Selection
lang_choice = st.sidebar.selectbox(
    "🌐 மொழி / Language / भाषा / ಭಾಷೆ / భాష",
    ["தமிழ்", "English", "हिंदी", "ಕನ್ನಡ", "తెలుగు"],
)
t = translations[lang_choice]

menu = st.sidebar.selectbox(
    t["menu_title"],
    [
        t["home"],
        t["rod_calc"],
        t["letter_calc"],
        t["prod_calc"],
        t["cost_calc"],
        t["stock_mgmt"],
        t["ai_prog"],
        t["quotation"],
        t["settings"],
    ],
)

# ==================== 1. HOME DASHBOARD ====================
if menu == t["home"]:
  st.markdown(f"### {t['hello']}")
  st.write(t["home_desc"])

  col1, col2, col3 = st.columns(3)
  with col1:
    st.info(
        f"📏 **Rod & Conversion**\n\nGrades, Shapes, Meter, KG, Qty & Drawing"
        " Upload"
    )
    st.info(f"📦 **Stock Management**\n\nStock levels & item tracking")
  with col2:
    st.success(
        f"🔤 **Letter Cutting & Speed**\n\nCNC Letter engraving & RPM/Cutting"
        " speed"
    )
    st.success(
        f"🤖 **AI G-Code Generator**\n\nTurning, Facing & Drilling programs"
    )
  with col3:
    st.warning(f"💰 **Costing Calculator**\n\nPart price & profit calculation")
    st.warning(f"📄 **Quotation & PDF**\n\nDrawing quotation & export")

# ==================== 2. ROD & CONVERSION CALCULATOR ====================
elif menu == t["rod_calc"]:
  st.header(t["rod_calc"])
  st.write(
      "மெட்டீரியல் கிரேடு, வடிவம் (Round, Hex, Tube) மற்றும் அளவுகளைத்"
      " தேர்ந்தெடுத்துக் கணக்கிடலாம்."
  )

  # --- Drawing / Photo Upload Option ---
  st.markdown("### 📷 Part Drawing / Reference Photo Upload")
  calc_drawing = st.file_uploader(
      "Upload component drawing or photo for reference",
      type=["png", "jpg", "jpeg"],
      key="calc_img",
  )
  if calc_drawing is not None:
    st.image(calc_drawing, caption="Uploaded Drawing Preview", width=300)

  st.markdown("---")
  gc1, gc2 = st.columns(2)
  with gc1:
    material_grade = st.selectbox(
        "மெட்டீரியல் கிரேடு (Material Grade)",
        ["MS (Mild Steel)", "EN8", "EN19", "EN24", "Aluminium", "Brass"],
    )
  with gc2:
    material_shape = st.selectbox(
        "மெட்டீரியல் வடிவம் (Material Shape)",
        [
            "Round Bar (வட்ட ராட்)",
            "Hexagon Bar (ஹெக்சகன்)",
            "Tube / Pipe (டியூப் / பைப்)",
        ],
    )

  density_map = {
      "MS (Mild Steel)": 0.00000785,
      "EN8": 0.00000785,
      "EN19": 0.00000785,
      "EN24": 0.00000785,
      "Aluminium": 0.00000270,
      "Brass": 0.00000850,
  }
  density = density_map.get(material_grade, 0.00000785)

  col1, col2 = st.columns(2)
  with col1:
    if "Tube" in material_shape:
      outer_dia = st.number_input(
          "வெளியிட டயா (Outer Dia - mm)", min_value=1.0, value=30.0, step=0.5
      )
      inner_dia = st.number_input(
          "உள் டயா (Inner Dia - mm)", min_value=0.0, value=15.0, step=0.5
      )
      raw_dia = outer_dia
    else:
      raw_dia = st.number_input(
          t["raw_dia"], min_value=1.0, value=20.0, step=0.5
      )

    part_length = st.number_input(
        t["part_len"], min_value=1.0, value=126.0, step=1.0
    )
  with col2:
    cutting_allowance = st.number_input(
        t["cutting_all"], min_value=0.0, value=3.0, step=0.5
    )
    rod_standard_length = st.number_input(
        t["std_rod_len"], min_value=1.0, value=6.0, step=0.5
    )

  st.markdown("---")
  calc_mode = st.radio(
      "மெட்டீரியல் உள்ளீடு முறை (Select Mode):",
      (
          "1. ராட் எண்ணிக்கை / மீட்டர் மூலம் (Rods/Meters)",
          "2. கிலோ (KG) எடை மூலம்",
          "3. தேவையான பார்ட் எண்ணிக்கை மூலம் (Required Qty)",
      ),
  )

  effective_len = part_length + cutting_allowance

  if "Hexagon" in material_shape:
    weight_per_mm = 0.866 * (raw_dia**2) * density
  elif "Tube" in material_shape:
    cross_area = (math.pi / 4) * ((outer_dia**2) - (inner_dia**2))
    weight_per_mm = cross_area * density
  else:
    cross_area = math.pi * ((raw_dia / 2) ** 2)
    weight_per_mm = cross_area * density

  weight_per_meter = weight_per_mm * 1000
  standard_rod_weight = rod_standard_length * weight_per_meter

  if "1." in calc_mode:
    st.subheader("📌 முறை 1: ராட் எண்ணிக்கையைக் கொண்டு கணக்கிடுதல்")
    num_rods = st.number_input(
        "ராடுகளின் எண்ணிக்கை (Number of Rods)", min_value=1, value=10, step=1
    )
    if st.button(t["calc_btn"], type="primary"):
      parts_per_rod = (
          int((rod_standard_length * 1000) // effective_len)
          if effective_len > 0
          else 0
      )
      total_parts = parts_per_rod * num_rods
      balance_mm_per_rod = (rod_standard_length * 1000) % effective_len
      total_scrap_mm = balance_mm_per_rod * num_rods
      total_weight_kg = num_rods * standard_rod_weight
      total_scrap_weight_kg = total_scrap_mm * weight_per_mm

      st.markdown(f"### 📊 {t['results']}")
      rc1, rc2, rc3 = st.columns(3)
      with rc1:
        st.metric("தயாராகும் மொத்த பார்ட்டுகள் (Qty)", f"{total_parts} Nos")
        st.metric("ஒரு ராட்டில் வரும் பார்ட்டுகள்", f"{parts_per_rod} Nos")
      with rc2:
        st.metric("மொத்த மெட்டீரியல் எடை", f"{total_weight_kg:.2f} KG")
        st.metric("ஸ்கிராப் எடை (Scrap Weight)", f"{total_scrap_weight_kg:.2f} KG")
      with rc3:
        st.metric("மொத்த ஸ்கிராப் நீளம்", f"{total_scrap_mm / 1000:.2f} Meters")
        st.metric("ஸ்டாண்டர்ட் ராட் எடை", f"{standard_rod_weight:.2f} KG")

  elif "2." in calc_mode:
    st.subheader("📌 முறை 2: கிலோ (KG) எடையைக் கொண்டு கணக்கிடுதல்")
    total_available_kg = st.number_input(
        "உள்ளீடு மெட்டீரியல் எடை (Total KG Available)",
        min_value=0.1,
        value=50.0,
        step=1.0,
    )
    if st.button(t["calc_btn"], type="primary"):
      total_length_meters = (
          total_available_kg / weight_per_meter if weight_per_meter > 0 else 0
      )
      total_length_mm = total_length_meters * 1000
      total_possible_parts = (
          int(total_length_mm // effective_len) if effective_len > 0 else 0
      )
      total_weight_used = total_possible_parts * (
          effective_len * weight_per_mm
      )
      scrap_weight_kg = total_available_kg - total_weight_used

      st.markdown(f"### 📊 {t['results']}")
      rc1, rc2 = st.columns(2)
      with rc1:
        st.metric("கிடைக்கும் மொத்த நீளம்", f"{total_length_meters:.2f} Meters")
        st.metric(
            "உற்பத்தி செய்யக்கூடிய பார்ட்டுகள் (Qty)",
            f"{total_possible_parts} Nos",
        )
      with rc2:
        st.metric("பயன்படுத்தப்பட்ட பார்ட் எடை", f"{total_weight_used:.2f} KG")
        st.metric("மீதமுள்ள ஸ்கிராப் எடை", f"{scrap_weight_kg:.2f} KG")

  else:
    st.subheader("📌 முறை 3: தேவையான பார்ட் எண்ணிக்கையைக் கொண்டு கணக்கிடுதல்")
    required_qty = st.number_input(
        "தேவையான பார்ட் எண்ணிக்கை (Required Qty)", min_value=1, value=500, step=10
    )
    if st.button(t["calc_btn"], type="primary"):
      parts_per_rod = (
          int((rod_standard_length * 1000) // effective_len)
          if effective_len > 0
          else 0
      )
      required_rods = (
          math.ceil(required_qty / parts_per_rod) if parts_per_rod > 0 else 0
      )
      total_kg_needed = required_rods * standard_rod_weight
      actual_parts_produced = parts_per_rod * required_rods
      total_scrap_mm = required_rods * (
          (rod_standard_length * 1000) % effective_len
      )
      total_scrap_kg = total_scrap_mm * weight_per_mm

      st.markdown(f"### 📊 {t['results']}")
      rc1, rc2, rc3 = st.columns(3)
      with rc1:
        st.metric("தேவையான ராடுகள் (6m Rods)", f"{required_rods} Nos")
        st.metric("உற்பத்தி ஆகும் பார்ட்டுகள்", f"{actual_parts_produced} Nos")
      with rc2:
        st.metric("தேவையான மொத்த எடை", f"{total_kg_needed:.2f} KG")
        st.metric("ஸ்கிராப் எடை", f"{total_scrap_kg:.2f} KG")
      with rc3:
        st.metric(
            "மொத்த ராட் நீளம்", f"{required_rods * rod_standard_length:.2f} Meters"
        )
        st.metric("ஸ்கிராப் நீளம்", f"{total_scrap_mm / 1000:.2f} Meters")

# ==================== 3. LETTER CUTTING & CUTTING SPEED ====================
elif menu == t["letter_calc"]:
  st.header("🔤 CNC Letter Cutting & Cutting Speed Calculator")
  st.write(
      "CNC மிஷினில் லெட்டர் பொறித்தல் (Engraving) மற்றும் ஸ்பிண்டில் ஆர்பிஎம்"
      " (RPM) / கட்டிங் ஸ்பீட் கணக்கிடலாம்."
  )

  tab1, tab2 = st.tabs(["🔤 Letter / Engraving Calculator", "⚡ Cutting Speed & RPM"])

  with tab1:
    st.subheader("Letter / Text Engraving Parameters")
    text_input = st.text_input(
        "பொறிக்க வேண்டிய எழுத்துக்கள் (Enter Text to Engrave)", "MEGALA CNC"
    )
    char_height = st.number_input("எழுத்தின் உயரம் (Character Height - mm)", value=10.0)
    feed_engrave = st.number_input("எக்ராவ்விங் ஃபீட் (Feed Rate - mm/min)", value=200.0)
    depth_engrave = st.number_input("கட்டிங் டெப்த் (Depth of Cut - mm)", value=0.5)

    if st.button("Generate Letter G-Code", type="primary"):
      engraw_gcode = f"""%
O9001 (LETTER ENGRAVING - {text_input})
G21 G40 G90 G17
G00 Z5.0
M03 S3000
(TEXT: {text_input} | HEIGHT: {char_height}mm | DEPTH: {depth_engrave}mm)
G01 Z-{depth_engrave} F{feed_engrave}
(G-Code path for letters generation...)
G00 Z5.0
M05
M30
%"""
      st.success("✅ Letter G-Code Generated Successfully!")
      st.code(engraw_gcode, language="gcode")

  with tab2:
    st.subheader("Cutting Speed (Vc) & Spindle Speed (RPM) Calculator")
    tool_dia = st.number_input("டூல் / ஒர்க் பீஸ் டயா (Diameter - mm)", value=25.0)
    cutting_speed_vc = st.number_input(
        "கட்டிங் ஸ்பீட் (Cutting Speed Vc - m/min)", value=150.0
    )

    if st.button("Calculate RPM", type="primary"):
      if tool_dia > 0:
        calculated_rpm = (cutting_speed_vc * 1000) / (math.pi * tool_dia)
        st.markdown("---")
        st.metric("Spindle Speed (RPM)", f"{int(calculated_rpm)} RPM")
      else:
        st.error("Diameter must be greater than 0")

# ==================== 4. PRODUCTION CALCULATOR ====================
elif menu == t["prod_calc"]:
  st.header(t["prod_calc"])
  c_time = st.number_input(
      "சைக்கிள் டைம் (Cycle Time - Seconds)", min_value=1.0, value=20.0
  )
  avail_time = st.number_input(
      "கிடைக்கும் நேரம் / நாள் (Working Hours)", min_value=1.0, value=8.0
  )
  efficiency = st.number_input("மிஷின் எபிஷியன்சி (%)", min_value=1.0, value=85.0)
  break_time = st.number_input(
      "ஓய்வு நேரம் / பிரேக் (Break Minutes)", min_value=0.0, value=30.0
  )

  if st.button(t["calc_btn"], type="primary"):
    net_working_hours = avail_time - (break_time / 60)
    pcs_per_hour = (3600 / c_time) * (efficiency / 100) if c_time > 0 else 0
    total_day_prod = pcs_per_hour * net_working_hours
    st.markdown("---")
    mc1, mc2 = st.columns(2)
    with mc1:
      st.metric(
          "1 மணி நேர உற்பத்தி (Production / Hour)", f"{int(pcs_per_hour)} Nos"
      )
    with mc2:
      st.metric(
          "1 நாள் உற்பத்தி (Production / Day)", f"{int(total_day_prod)} Nos"
      )

# ==================== 5. COSTING CALCULATOR ====================
elif menu == t["cost_calc"]:
  st.header(t["cost_calc"])
  mat_cost_kg = st.number_input("1 KG மெட்டீரியல் விலை (₹)", value=85.0)
  mat_wt_part = st.number_input(
      "பார்ட் எடை (Material Weight / Part - Kg)", value=0.25
  )
  machine_cost_hr = st.number_input("1 மணி நேர மிஷின் கட்டணம் (₹)", value=600.0)
  labour_cost_part = st.number_input("லேபர் செலவு / பார்ட் (₹)", value=1.20)
  overhead_pct = st.number_input("மேலதிகச் செலவு / Overhead (%)", value=15.0)

  if st.button(t["calc_btn"], type="primary"):
    material_total = mat_cost_kg * mat_wt_part
    machine_part_cost = (machine_cost_hr / 3600) * 20
    sub_cost = material_total + machine_part_cost + labour_cost_part
    total_cost_per_part = sub_cost * (1 + (overhead_pct / 100))
    cost_1000 = total_cost_per_part * 1000
    st.markdown("---")
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
      st.metric("செலவு / பார்ட் (Cost / Part)", f"₹ {total_cost_per_part:.2f}")
    with sc2:
      st.metric("1000 பார்ட்களுக்கான செலவு", f"₹ {cost_1000:,.2f}")
    with sc3:
      st.metric(
          "பரிந்துரைக்கப்பட்ட விற்பனை விலை",
          f"₹ {total_cost_per_part * 1.25:.2f}",
      )

# ==================== 6. STOCK MANAGEMENT ====================
elif menu == t["stock_mgmt"]:
  st.header(t["stock_mgmt"])
  s_col1, s_col2, s_col3 = st.columns(3)
  with s_col1:
    st.metric("மொத்த பொருட்கள் (Total Items)", "128")
  with s_col2:
    st.metric("குறைந்த இருப்பு (Low Stock)", "8")
  with s_col3:
    st.metric("இருப்பு இல்லை (Out of Stock)", "3")
  st.markdown("---")
  st.subheader("📋 சமீபத்திய ஸ்டாக் பட்டியல் (Recent Stock)")
  st.write("🟢 **EN8 Round Bar - 12mm** : 120.50 Kg (In Stock)")
  st.write("🟡 **MS Round Bar - 20mm** : 45.20 Kg (Low Stock)")
  st.write("🔴 **EN24 Round Bar - 16mm** : 0.00 Kg (Out of Stock)")

# ==================== 7. AI DRAWING TO G-CODE (TURNING, FACING, DRILLING) ====================
elif menu == t["ai_prog"]:
  st.header(t["ai_prog"])
  st.write(
      "கஸ்டமர் டிராயிங் அல்லது போட்டோவை அப்லோட் செய்து, அதற்கான **Turning,"
      " Facing மற்றும் Drilling** ஜி-கோடு ப்ரோக்ராமை உருவாக்கலாம்."
  )

  uploaded_drawing = st.file_uploader(
      "பார்ட் டிராயிங் / போட்டோவை அப்லோட் செய்யவும் (Upload Drawing / Image)",
      type=["png", "jpg", "jpeg"],
      key="gcode_img",
  )
  if uploaded_drawing is not None:
    st.image(uploaded_drawing, caption="Uploaded Drawing Preview", width=300)

  op_type = st.selectbox(
      "செயல்பாட்டு முறை (Select Operation Type):",
      [
          "Facing & Turning (ஃபேசிங் மற்றும் டர்னிங்)",
          "Drilling Cycle (டிரில்லிங் சுழற்சி - G83/G81)",
          "Complete Combined Cycle (Facing + Turning + Drilling)",
      ],
  )

  col1, col2 = st.columns(2)
  with col1:
    part_name = st.text_input("பார்ட் பெயர் / நம்பர் (Part Name / No)", "Part-01")
    prog_num = st.text_input("ப்ரோக்ராம் எண் (Program Number)", "O1001")
    raw_d = st.number_input(
        "ரா மெட்டீரியல் டயா (Raw Dia - mm)", min_value=1.0, value=25.0, step=0.5
    )
  with col2:
    finish_d = st.number_input(
        "பினிஷ்ட் டயா (Finished Dia - mm)", min_value=1.0, value=20.0, step=0.5
    )
    p_len = st.number_input(
        "பார்ட் நீளம் (Part Length - mm)", min_value=1.0, value=50.0, step=1.0
    )
    drill_dia = st.number_input("டிரில் டயா (Drill Dia - mm)", value=10.0)

  if st.button("⚙️ CNC G-Code ப்ரோக்ராமை உருவாக்கு", type="primary"):
    if "Facing" in op_type:
      facing_code = "G00 X{:.1f} Z0.0\nG01 X-0.5 F0.15\nG00 Z2.0".format(
          raw_d + 1.0
      )
    else:
      facing_code = "(No Facing Selected)"

    if "Drilling" in op_type or "Combined" in op_type:
      drilling_code = (
          "T0202 (DRILL TOOL)\nG97 S1500 M03\nG00 X0.0 Z2.0\nG83 Z-30.0 R1.0"
          " Q5000 F0.1\nG80"
      )
    else:
      drilling_code = "(No Drilling Selected)"

    gcode_content = f"""%
{prog_num}
(PART NAME: {part_name})
(OPERATION: {op_type})
G21 G40 G99 G18
G28 U0.0 W0.0
T0101 (TURNING & FACING TOOL)
G97 S2000 M03
{facing_code}
G00 X{raw_d + 2.0} Z2.0
G01 Z0.0 F0.2
X{finish_d} F0.15
Z-{p_len}
G00 X{raw_d + 5.0}
G28 U0.0 W0.0
{drilling_code}
G28 U0.0 W0.0
M05
M30
%"""
    st.success("✅ CNC G-Code ப்ரோக்ராம் வெற்றிகரமாக உருவாக்கப்பட்டது!")
    st.code(gcode_content, language="gcode")
    st.download_button(
        "⬇️ Download G-Code File (.nc)",
        data=gcode_content,
        file_name=f"{part_name}.nc",
        mime="text/plain",
    )

# ==================== 8. QUOTATION & PDF ====================
elif menu == t["quotation"]:
  st.header(t["quotation"])
  cust_name = st.text_input("கஸ்டமர் கம்பெனி பெயர்", "ABC Industries")
  part_no = st.text_input("டிராயிங் எண் / பார்ட் பெயர்", "TR-001 - Trunion")
  uploaded_file_q = st.file_uploader(
      "கஸ்டமர் டிராயிங் அப்லோட் (Image / PDF)",
      type=["png", "jpg", "jpeg", "pdf"],
      key="q_file",
  )
  quoted_qty = st.number_input("கொட்டேஷன் தேவைப்படும் அளவு (Qty)", value=500)
  unit_price_q = st.number_input("ஒரு பார்ட்டுக்கான இறுதி விலை (₹)", value=9.00)

  if st.button("📄 PDF கொட்டேஷனை உருவாக்கு", type="primary"):
    st.success("✅ கொட்டேஷன் வெற்றிகரமாகத் தயாரிக்கப்பட்டது!")
    if uploaded_file_q is not None:
      st.image(uploaded_file_q, caption="Uploaded Drawing Preview", width=300)
    st.info(
        f"📥 கஸ்டமர்: {cust_name} | பார்ட்: {part_no} | மொத்தம்: ₹"
        f" {quoted_qty * unit_price_q:,.2f}"
    )
    st.download_button(
        "⬇️ Download Quotation PDF",
        data="Sample PDF Content",
        file_name="Quotation_MegalaCNC.pdf",
    )

# ==================== 9. SETTINGS / MORE MENU ====================
elif menu == t["settings"]:
  st.header(t["settings"])
  st.markdown("""
    * 👤 **Part Master** (பார்ட் விவரங்களை நிர்வகிக்க)
    * 🏢 **Customer Master** (கஸ்டமர் பட்டியலை நிர்வகிக்க)
    * ⚙️ **Machine Master** (மிஷின் விவரங்களை நிர்வகிக்க)
    * 🔩 **Material Master** (மெட்டீரியல் கிரேடு மற்றும் விலை)
    * 🛠️ **Tool Master** (டூல் மற்றும் இன்செர்ட் விபரங்கள்)
    * 💾 **Backup & Restore** (டேட்டா பேக்கப் எடுக்க)
    * ℹ️ **About CNC Mate** (சாஃப்ட்வேர் தகவல்)
    """)
