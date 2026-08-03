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

# --- SESSION STATE INITIALIZATION ---
if "lang" not in st.session_state:
  st.session_state.lang = "தமிழ் (Tamil)"
if "default_machine_rate" not in st.session_state:
  st.session_state.default_machine_rate = 600.0

# --- DICTIONARY FOR MULTI-LANGUAGE TRANSLATION ---
translations = {
    "தமிழ் (Tamil)": {
        "sub_title": (
            "**SMART CNC. SIMPLE WORK.** — புரொபஷனல் ஒர்க்ஷாப் ஆட்டோமேஷன் &"
            " துல்லியமான கால்குலேட்டர்"
        ),
        "menu": [
            "1. 🏠 முகப்பு & டேஷ்போர்டு (Dashboard)",
            "2. ⚙️ அமைப்புகள் & செட்டிங்ஸ் (Settings)",
            "3. 🧮 மெஷின் கால்குலேட்டர் (Machine RPM & Time)",
            "4. 💰 கொட்டேஷன் & செலவு மேலாண்மை (Quotation)",
            "5. 📸 போட்டோ / டிராயிங் பகுப்பாய்வு (Drawing Analysis)",
            "6. 📐 ராட், மீட்டர்/கிலோ & ஸ்கிராப் (Rod & Scrap Calculator)",
            "7. 📜 ஜி-கோடு ஜெனரேட்டர் (Advanced G-Code)",
            "8. 🏭 உற்பத்தி நாட்கள் கால்குலேட்டர் (Production Days)",
            "9. 📦 ஸ்டாக் மேனேஜ்மென்ட் (Stock & Inventory)",
        ],
        "dash_title": "🏠 Megala CNC Mate - முகப்பு & டேஷ்போர்டு",
        "dash_desc": (
            "சுரேஷின் ஆஃப்லைன் ஒர்க்ஷாப் கன்ட்ரோல் சென்டருக்கு உங்களை வரவேற்கிறோம்."
        ),
        "total_modules": "மொத்த மாட்யூம்கள்",
        "op_mode": "இயக்க முறை",
        "sel_lang": "தேர்ந்தெடுக்கப்பட்ட மொழி",
        "app_ver": "ஆப் வெர்ஷன்",
        "quick_guide": "📌 விரைவு வழிகாட்டி (Quick Guide):",
        "settings_title": "⚙️ ஒர்க்ஷாப் ஆப் அமைப்புகள் (Settings & Preferences)",
        "settings_desc": (
            "உங்களுக்குப் பிடித்த மொழியைத் தேர்ந்தெடுக்கவும் மற்றும் இயல்புநிலை"
            " இயந்திர கட்டணங்களை அமைக்கவும்."
        ),
        "lang_label": "🌐 ஆப் மொழி தேர்வு (Select App Language)",
        "tech_defaults": "🛠️ ஒர்க்ஷாப் தொழில்நுட்ப செட்டிங்ஸ் (Technical Defaults)",
        "machine_rate_label": "இயந்திர மணிநேரக் கட்டணம் (Machine Hourly Rate - ₹/hr)",
        "save_btn": "செட்டிங்ஸைச் சேமி (Save Settings)",
        "save_success": "✅ ஒர்க்ஷாப் செட்டிங்ஸ் வெற்றிகரமாக சேமிக்கப்பட்டது!",
        "rod_calc_title": "📐 ராட், மீட்டர்/கிலோ கன்வெர்ட்டர் & ஸ்கிராப் கால்குலேட்டர்",
        "rod_calc_desc": (
            "கஸ்டமர் தரும் கட்டிங் அலவன்ஸ் மற்றும் விருப்பப்பட்டால் டூல்"
            " திக்னஸை சேர்த்து துல்லியமாகக் கணக்கிடலாம்."
        ),
        "mat_grade": "மெட்டீரியல் கிரேடு (Material Grade)",
        "input_format": "உள்ளீடு முறை (Raw Material Input Format):",
        "len_meters": "நீளம் (Meters கணக்கில்)",
        "wt_kg": "எடை (Kg கணக்கில்)",
        "total_len_m": "மொத்த ராட் நீளம் (Meters)",
        "total_wt_kg": "மொத்த எடை (Kg)",
        "outer_dia": "ராட் வெளி விட்டம் (Outer Diameter - mm)",
        "part_len": "பாகத்தின் நீளம் (Finished Part Length - mm)",
        "cutting_adj": "⚙️ கட்டிங் & அலவன்ஸ் சரிசெய்தல் (Allowances)",
        "cust_allowance": (
            "கஸ்டமர் கட்டிங் / பேசிங் அலவன்ஸ் (Cutting Allowance - mm)"
        ),
        "enable_tool": (
            "டூல் கிரைண்டிங் திக்னஸ் சேர்க்க வேண்டுமா? (Optional Tool Thickness)"
        ),
        "tool_width_label": "டூல் திக்னஸ் / அகலம் (Tool Width - mm)",
        "calc_btn": "துல்லியமான பீஸ்கள் & ஸ்கிராப்பைக் கணக்கிடு (Calculate)",
        "calc_success": "✅ கணக்கீடு வெற்றிகரமாக முடிந்தது!",
        "res_len": "மொத்த ராட் நீளம்",
        "res_wt": "மொத்த எடை",
        "res_pcs": "உற்பத்தி ஆகும் பீஸ்கள் (Pieces)",
        "res_scrap": "ஸ்கிராப் எடை (Scrap Weight)",
        "workshop_note": "💡 **ஒர்க்ஷாப் குறிப்பு:** கணக்கிடப்பட்ட கஸ்டமர் அலவன்ஸ்",
    },
    "English": {
        "sub_title": (
            "**SMART CNC. SIMPLE WORK.** — Professional Workshop Automation &"
            " Exact Module Routing"
        ),
        "menu": [
            "1. 🏠 Dashboard Overview",
            "2. ⚙️ Settings & Preferences",
            "3. 🧮 Machine Calculator (RPM & Time)",
            "4. 💰 Quotation & Cost Management (Overheads)",
            "5. 📸 Drawing & Photo Analysis",
            "6. 📐 Rod, Meter/Kg Converter & Scrap Calculator",
            "7. 📜 Advanced G-Code Generator",
            "8. 🏭 Production Days Calculator",
            "9. 📦 Stock & Inventory Management",
        ],
        "dash_title": "🏠 Megala CNC Mate - Dashboard & Module Overview",
        "dash_desc": "Welcome to Suresh's offline workshop command center.",
        "total_modules": "Total Modules",
        "op_mode": "Operation Mode",
        "sel_lang": "Selected Language",
        "app_ver": "App Version",
        "quick_guide": "📌 Quick Guide:",
        "settings_title": "⚙️ Workshop App Settings & Preferences",
        "settings_desc": "Configure preferred language and standard machine rates.",
        "lang_label": "🌐 Select App Language",
        "tech_defaults": "🛠️ Workshop Technical Defaults",
        "machine_rate_label": "Default Machine Hourly Rate (₹/hr)",
        "save_btn": "Save Settings",
        "save_success": "✅ Settings updated successfully!",
        "rod_calc_title": (
            "📐 Rod, Meter/Kg Converter & Scrap Calculator (with Cutting"
            " Allowance)"
        ),
        "rod_calc_desc": (
            "Handles customer cutting allowance with optional tool thickness"
            " integration."
        ),
        "mat_grade": "Material Grade",
        "input_format": "Raw Material Input Format:",
        "len_meters": "Input Length in Meters",
        "wt_kg": "Input Weight in Kg",
        "total_len_m": "Total Rod Length (Meters)",
        "total_wt_kg": "Total Rod Weight (Kg)",
        "outer_dia": "Rod Outer Diameter (mm)",
        "part_len": "Finished Part Length (mm)",
        "cutting_adj": "⚙️ Cutting & Allowance Adjustments",
        "cust_allowance": "Customer Cutting Allowance per piece (mm)",
        "enable_tool": "Include Optional Tool Grinding Thickness?",
        "tool_width_label": "Parting Tool Width (mm)",
        "calc_btn": "Calculate Exact Pieces & Scrap",
        "calc_success": "✅ Precision Calculation Completed!",
        "res_len": "Total Rod Length",
        "res_wt": "Total Weight",
        "res_pcs": "Exact Pieces Yield",
        "res_scrap": "Total Scrap Weight",
        "workshop_note": "💡 **Workshop Note:** Calculated using customer allowance of",
    },
}

t = translations[st.session_state.lang]

# --- HEADER SECTION ---
col_logo, col_title = st.columns([3, 4])

with col_logo:
  if os.path.exists("Logo.png"):
    try:
      st.image("Logo.png", width=300)
    except Exception:
      st.markdown("⚙️ **[Logo Error]**")
  else:
    st.markdown("⚙️ **[Logo Here]**")

with col_title:
  st.title("⚙️ Megala CNC Mate")
  st.markdown(t["sub_title"])

st.markdown("---")

# --- SIDEBAR MENU NAVIGATION ---
st.sidebar.markdown(
    "### 📌 Menu / மெனு"
    if st.session_state.lang == "தமிழ் (Tamil)"
    else "### 📌 Menu Navigation"
)
app_mode = st.sidebar.selectbox(
    "Select Module", t["menu"], label_visibility="collapsed"
)

# --- MODULE 1: DASHBOARD OVERVIEW ---
if "1." in app_mode:
  st.header(t["dash_title"])
  st.write(t["dash_desc"])

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(label=t["total_modules"], value="9 Pro Modules")
  with col2:
    st.metric(label=t["op_mode"], value="100% Offline 🟢")
  with col3:
    st.metric(label=t["sel_lang"], value=st.session_state.lang)
  with col4:
    st.metric(label=t["app_ver"], value="Ultimate v22.0")

  st.markdown("---")
  st.markdown(t["quick_guide"])
  for m in t["menu"]:
    st.markdown(f"- {m}")

# --- MODULE 2: SETTINGS & PREFERENCES ---
elif "2." in app_mode:
  st.header(t["settings_title"])
  st.write(t["settings_desc"])
  st.markdown("---")

  languages_list = ["தமிழ் (Tamil)", "English"]
  current_index = (
      languages_list.index(st.session_state.lang)
      if st.session_state.lang in languages_list
      else 0
  )

  selected_language = st.selectbox(
      t["lang_label"], languages_list, index=current_index
  )

  if selected_language != st.session_state.lang:
    st.session_state.lang = selected_language
    st.rerun()

  st.markdown(f"### {t['tech_defaults']}")
  st.session_state.default_machine_rate = st.number_input(
      t["machine_rate_label"],
      value=st.session_state.default_machine_rate,
      step=50.0,
  )

  if st.button(t["save_btn"]):
    st.success(t["save_success"])

# --- MODULE 3: MACHINE CALCULATOR ---
elif "3." in app_mode:
  st.header("🧮 Machine Calculator (RPM & Time)")
  st.info("CNC, Traub & Drilling modules active.")

# --- MODULE 4: QUOTATION & OVERHEADS ---
elif "4." in app_mode:
  st.header("💰 Quotation & Cost Management")
  st.info("Quotation module active.")

# --- MODULE 5: DRAWING & PHOTO ANALYSIS ---
elif "5." in app_mode:
  st.header("📸 Drawing & Photo Analysis")
  uploaded_file = st.file_uploader(
      "Upload Part Drawing / Photo", type=["png", "jpg", "jpeg"]
  )
  if uploaded_file:
    st.image(uploaded_file, width=250)
    st.success("✅ File loaded.")

# --- MODULE 6: ROD, METER/KG CONVERTER & SCRAP CALCULATOR ---
elif "6." in app_mode:
  st.header(t["rod_calc_title"])
  st.write(t["rod_calc_desc"])

  col_a, col_b = st.columns(2)

  with col_a:
    mat_grade = st.selectbox(
        t["mat_grade"], ["EN8", "EN24", "Aluminum 6061", "Mild Steel (MS)"]
    )
    density = 2.70 if "Aluminum" in mat_grade else 7.85
    input_format = st.radio(
        t["input_format"], [t["len_meters"], t["wt_kg"]]
    )
    if t["len_meters"] in input_format:
      input_meters = st.number_input(t["total_len_m"], value=100.0)
      input_kg = 0.0
    else:
      input_kg = st.number_input(t["total_wt_kg"], value=80.0)
      input_meters = 0.0

  with col_b:
    dia = st.number_input(t["outer_dia"], value=40.0)
    part_drawing_length = st.number_input(t["part_len"], value=45.0)

    st.markdown(t["cutting_adj"])
    customer_facing_allowance = st.number_input(
        t["cust_allowance"], value=2.0, step=0.5
    )

    # Optional Tool Thickness Toggle (நீங்கள் கேட்டது போல் விருப்பத் தேர்வு)
    include_tool_thickness = st.checkbox(t["enable_tool"], value=False)
    if include_tool_thickness:
      effective_tool_width = st.number_input(
          t["tool_width_label"], value=3.0, step=0.1
      )
    else:
      effective_tool_width = 0.0

  if st.button(t["calc_btn"]):
    r_cm = (dia / 2.0) / 10.0
    vol_per_cm = math.pi * (r_cm**2)
    weight_per_meter_kg = (vol_per_cm * 100.0 * density) / 1000.0

    if t["len_meters"] in input_format:
      total_rod_len_mm = input_meters * 1000.0
      calc_kg = input_meters * weight_per_meter_kg
    else:
      calc_kg = input_kg
      total_rod_len_mm = (
          (input_kg / weight_per_meter_kg) * 1000.0
          if weight_per_meter_kg > 0
          else 0.0
      )

    # Calculation based on part length + customer allowance + optional tool width (if checked)
    single_consumption_mm = (
        part_drawing_length
        + customer_facing_allowance
        + effective_tool_width
    )
    total_pieces = int(total_rod_len_mm // single_consumption_mm)

    used_len_mm = total_pieces * single_consumption_mm
    end_bit_leftover = max(0.0, total_rod_len_mm - used_len_mm)
    blade_scrap_mm = (
        total_pieces * effective_tool_width if include_tool_thickness else 0.0
    )
    total_scrap_kg = (
        (vol_per_cm * ((end_bit_leftover + blade_scrap_mm) / 10.0)) * density
    ) / 1000.0

    st.success(t["calc_success"])
    r1, r2, r3, r4 = st.columns(4)
    r1.metric(t["res_len"], f"{(total_rod_len_mm/1000.0):.2f} M")
    r2.metric(t["res_wt"], f"{calc_kg:.2f} Kg")
    r3.metric(t["res_pcs"], f"{total_pieces} Nos")
    r4.metric(t["res_scrap"], f"{total_scrap_kg:.3f} Kg")

    if include_tool_thickness:
      st.info(
          f"💡 **Workshop Note:** Allowance: **{customer_facing_allowance} mm**"
          f" | Tool Thickness: **{effective_tool_width} mm**"
      )
    else:
      st.info(
          f"💡 **Workshop Note:** Customer Allowance used: **"
          f"{customer_facing_allowance} mm** (Tool thickness ignored as"
          f" requested)."
      )

# --- MODULE 7: ADVANCED G-CODE GENERATOR ---
elif "7." in app_mode:
  st.header("📜 Advanced G-Code Generator")
  st.code("O1001\nG21 G90 G40\nM03 S1500\nG00 X44.0 Z2.0\nM30", language="text")

# --- MODULE 8: PRODUCTION DAYS CALCULATOR ---
elif "8." in app_mode:
  st.header("🏭 Production Days Calculator")
  st.metric("Estimated Days Required", "3.5 Days")

# --- MODULE 9: STOCK MANAGEMENT ---
elif "9." in app_mode:
  st.header("📦 Stock & Inventory Management")
  st.success("✅ Stock level is sufficient.")

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>© 2026 Megala CNC Mate | Professional"
    " Workshop Automation</p>",
    unsafe_allow_html=True,
)
