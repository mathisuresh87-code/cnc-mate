import math
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Megala CNC Mate - Smart CNC & Production",
    page_icon="⚙️",
    layout="wide",
)

# Multi-Language Dictionary (English, Tamil, Hindi, Kannada, Telugu)
translations = {
    "English": {
        "title": "⚙️ Megala CNC Mate",
        "subtitle": "**SMART CNC. SIMPLE WORK.** — Customer Quotation, Production & Stock Management System",
        "menu_title": "🧭 Navigation Menu",
        "home": "🏠 Home Dashboard",
        "rod_calc": "📏 Rod & Conversion Calculator",
        "prod_calc": "⏱️ Production Calculator",
        "cost_calc": "💰 Costing Calculator",
        "stock_mgmt": "📦 Stock Management",
        "ai_prog": "🤖 AI Drawing to G-Code Generator",
        "quotation": "📄 Quotation & PDF",
        "settings": "⚙️ Settings & Master",
        "hello": "Hello, Suresh! Good Morning 👋",
        "home_desc": "Manage all your shop floor calculations in one place.",
        "raw_dia": "Raw Material Dia (mm)",
        "part_len": "Part Length (mm)",
        "cutting_all": "Cutting Allowance / Groove (mm)",
        "std_rod_len": "Standard Rod Length (Meters)",
        "mode_label": "Select Material Input Mode:",
        "mode1": "1. By Rods Count / Meters",
        "mode2": "2. By Material Weight (KG)",
        "mode3": "3. By Required Part Quantity (Nos)",
        "calc_btn": "📊 Calculate",
        "results": "Calculation Results"
    },
    "தமிழ்": {
        "title": "⚙️ மேகலா CNC மேட்",
        "subtitle": "**SMART CNC. SIMPLE WORK.** — கஸ்டமர் கொட்டேஷன், உற்பத்தி மற்றும் ஸ்டாக் மேனேஜ்மெண்ட் சிஸ்டம்",
        "menu_title": "🧭 மெனு (Navigation Menu)",
        "home": "🏠 முகப்பு (Home Dashboard)",
        "rod_calc": "📏 ராட் & கன்வெர்ட்டர் கால்குலேட்டர்",
        "prod_calc": "⏱️ ப்ரொடக்ஷன் கால்குலேட்டர்",
        "cost_calc": "💰 காஸ்டிங் கால்குலேட்டர்",
        "stock_mgmt": "📦 ஸ்டாக் மேனேஜ்மெண்ட்",
        "ai_prog": "🤖 AI டிராயிங் & CNC ப்ரோக்ராம் ஜெனரேட்டர்",
        "quotation": "📄 கொட்டேஷன் & PDF",
        "settings": "⚙️ செட்டிங்ஸ் / More Menu",
        "hello": "வணக்கம் சுரேஷ்! இனிய காலை வணக்கம் 👋",
        "home_desc": "இப்போது உங்கள் ஷாப் ப்ளோர் கணக்கீடுகள் அனைத்தையும் ஒரே இடத்தில் கையாளலாம்.",
        "raw_dia": "ரா மெட்டீரியல் டயா (Raw Dia - mm)",
        "part_len": "பார்ட் நீளம் (Part Length - mm)",
        "cutting_all": "கட்டிங் அலவன்ஸ் / குருவ் (Cutting Allowance - mm)",
        "std_rod_len": "ஒரு ஸ்டாண்டர்ட் ராட் நீளம் (Standard Rod Length - Meters)",
        "mode_label": "உங்களிடம் உள்ள மெட்டீரியல் விபரம் என்ன முறையில் உள்ளது?",
        "mode1": "1. ராட் நீளம் & எண்ணிக்கை மூலம் (Meters / Rods Count)",
        "mode2": "2. கிலோ (KG) மூலம் மெட்டீரியல் உள்ளீடு",
        "mode3": "3. தேவையான பார்ட் எண்ணிக்கை மூலம் (Required Qty)",
        "calc_btn": "📊 கணக்கிடு (Calculate)",
        "results": "கணக்கீட்டு முடிவுகள் (Calculation Result)"
    },
    "हिंदी": {
        "title": "⚙️ मेगाला सीएनसी मेट",
        "subtitle": "**SMART CNC. SIMPLE WORK.** — ग्राहक उद्धरण, उत्पादन और स्टॉक प्रबंधन प्रणाली",
        "menu_title": "🧭 नेविगेशन मेनू",
        "home": "🏠 होम डैशबोर्ड",
        "rod_calc": "📏 रॉड और रूपांतरण कैलकुलेटर",
        "prod_calc": "⏱️ उत्पादन कैलकुलेटर",
        "cost_calc": "💰 लागत कैलकुलेटर",
        "stock_mgmt": "📦 स्टॉक प्रबंधन",
        "ai_prog": "🤖 ड्राइंग से जी-कोड जनरेटर",
        "quotation": "📄 उद्धरण और पीडीएफ",
        "settings": "⚙️ सेटिंग्स और मास्टर",
        "hello": "नमस्ते सुरेश! सुप्रभात 👋",
        "home_desc": "अब अपनी सभी शॉप फ्लोर गणनाओं को एक ही स्थान पर प्रबंधित करें।",
        "raw_dia": "रॉ मटेरियल व्यास (Raw Dia - mm)",
        "part_len": "पार्ट की लंबाई (Part Length - mm)",
        "cutting_all": "कटिंग अलाउंस / ग्रूव (Cutting Allowance - mm)",
        "std_rod_len": "मानक रॉड की लंबाई (Standard Rod Length - Meters)",
        "mode_label": "सामग्री इनपुट मोड चुनें:",
        "mode1": "1. रॉड संख्या / मीटर द्वारा",
        "mode2": "2. वजन (KG) द्वारा",
        "mode3": "3. आवश्यक पार्ट मात्रा (Qty) द्वारा",
        "calc_btn": "📊 गणना करें (Calculate)",
        "results": "गणना परिणाम (Calculation Results)"
    },
    "ಕನ್ನಡ": {
        "title": "⚙️ ಮೇಗಲಾ ಸಿಎನ್ಸಿ ಮೇಟ್",
        "subtitle": "**SMART CNC. SIMPLE WORK.** — ಗ್ರಾಹಕರ ಉಲ್ಲೇಖ, ಉತ್ಪಾದನೆ ಮತ್ತು ಸ್ಟಾಕ್ ನಿರ್ವಹಣಾ ವ್ಯವಸ್ಥೆ",
        "menu_title": "🧭 ನ್ಯಾವಿಗೇಷನ್ ಮೆನು",
        "home": "🏠 ಮುಖಪುಟ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "rod_calc": "📏 ರಾಡ್ ಮತ್ತು ಪರಿವರ್ತನೆ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
        "prod_calc": "⏱️ ಉತ್ಪಾದನಾ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
        "cost_calc": "💰 ವೆಚ್ಚ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
        "stock_mgmt": "📦 ಸ್ಟಾಕ್ ನಿರ್ವಹಣೆ",
        "ai_prog": "🤖 AI ಡ್ರಾಯಿಂಗ್ ಟು G-Code ಜನರೇಟರ್",
        "quotation": "📄 ಉಲ್ಲೇಖ ಮತ್ತು PDF",
        "settings": "⚙️ ಸೆಟ್ಟಿಂಗ್‌ಗಳು & ಮಾಸ್ಟರ್",
        "hello": "ನಮಸ್ಕಾರ ಸುರೇಶ್! ಶುಭೋದಯ 👋",
        "home_desc": "ಈಗ ನಿಮ್ಮ ಎಲ್ಲಾ ಶಾಪ್ ಫ್ಲೋರ್ ಲೆಕ್ಕಾಚಾರಗಳನ್ನು ಒಂದೇ ಸ್ಥಳದಲ್ಲಿ ನಿರ್ವಹಿಸಿ.",
        "raw_dia": "ರಾ ಮೆಟೀರಿಯಲ್ ವ್ಯಾಸ (Raw Dia - mm)",
        "part_len": "ಭಾಗದ ಉದ್ದ (Part Length - mm)",
        "cutting_all": "ಕಟಿಂಗ್ ಅಲೌನ್ಸ್ / ಗ್ರೂವ್ (Cutting Allowance - mm)",
        "std_rod_len": "ಪ್ರಮಾಣಿತ ರಾಡ್ ಉದ್ದ (Standard Rod Length - Meters)",
        "mode_label": "ಮೆಟೀರಿಯಲ್ ಇನ್ಪುಟ್ ಮೋಡ್ ಆಯ್ಕೆಮಾಡಿ:",
        "mode1": "1. ರಾಡ್ ಸಂಖ್ಯೆ / ಮೀಟರ್ ಮೂಲಕ",
        "mode2": "2. ತೂಕದ (KG) ಮೂಲಕ",
        "mode3": "3. ಅಗತ್ಯವಿರುವ ಭಾಗಗಳ ಸಂಖ್ಯೆ (Qty) ಮೂಲಕ",
        "calc_btn": "📊 ಲೆಕ್ಕಹಾಕಿ (Calculate)",
        "results": "ಲೆಕ್ಕಾಚಾರದ ಫಲಿತಾಂಶಗಳು (Calculation Results)"
    },
    "తెలుగు": {
        "title": "⚙️ మేగలా CNC మేట్",
        "subtitle": "**SMART CNC. SIMPLE WORK.** — కస్టమర్ కొటేషన్, ఉత్పత్తి మరియు స్టాక్ మేనేజ్‌మెంట్ సిస్టమ్",
        "menu_title": "🧭 నావిగేషన్ మెనూ",
        "home": "🏠 హోమ్ డ్యాష్‌బోర్డ్",
        "rod_calc": "📏 రాడ్ & మార్పిడి కాలిక్యులేటర్",
        "prod_calc": "⏱️ ప్రొడక్షన్ కాలిక్యులేటర్",
        "cost_calc": "💰 కాస్టింగ్ కాలిక్యులేటర్",
        "stock_mgmt": "📦 స్టాక్ మేనేజ్‌మెంట్",
        "ai_prog": "🤖 AI డ్రాయింగ్ నుండి G-Code జెనరేటర్",
        "quotation": "📄 కొటేషన్ & PDF",
        "settings": "⚙️ సెటింగ్స్ / మాస్టర్",
        "hello": "నమస్తే సురేష్! శుభోదయం 👋",
        "home_desc": "ఇప్పుడు మీ షాప్ ఫ్లోర్ లెక్కలన్నీ ఒకే చోట నిర్వహించండి.",
        "raw_dia": "రా మెటీరియల్ వ్యాసం (Raw Dia - mm)",
        "part_len": "భాగం పొడవు (Part Length - mm)",
        "cutting_all": "కటింగ్ అలవెన్స్ / గ్రూవ్ (Cutting Allowance - mm)",
        "std_rod_len": "ప్రామాణిక రాడ్ పొడవు (Standard Rod Length - Meters)",
        "mode_label": "మెటీరియల్ ఇన్పుట్ మోడ్ ఎంచుకోండి:",
        "mode1": "1. రాడ్ల సంఖ్య / మీటర్ల ద్వారా",
        "mode2": "2. బరువు (KG) ద్వారా",
        "mode3": "3. అవసరమైన భాగాల సంఖ్య (Qty) ద్వారా",
        "calc_btn": "📊 లెక్కించండి (Calculate)",
        "results": "ఫలితాలు (Calculation Results)"
    }
}

# Sidebar Language Selection
lang_choice = st.sidebar.selectbox("🌐 மொழி / Language / भाषा / ಭಾಷೆ / భాష", ["தமிழ்", "English", "हिंदी", "ಕನ್ನಡ", "తెలుగు"])
t = translations[lang_choice]

st.title(t["title"])
st.markdown(t["subtitle"])
st.markdown("---")

menu = st.sidebar.selectbox(
    t["menu_title"],
    [
        t["home"],
        t["rod_calc"],
        t["prod_calc"],
        t["cost_calc"],
        t["stock_mgmt"],
        t["ai_prog"],
        t["quotation"],
        t["settings"],
    ]
)

# ==================== 1. HOME DASHBOARD ====================
if menu == t["home"]:
    st.markdown(f"### {t['hello']}")
    st.write(t["home_desc"])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"📏 **Rod & Conversion**\n\nMeter, KG & Qty Converter")
        st.info(f"📦 **Stock Management**\n\nStock levels & details")
    with col2:
        st.success(f"⏱️ **Production Calculator**\n\nCycle time & shift output")
        st.success(f"🤖 **AI Drawing to G-Code**\n\nUpload drawing & write program")
    with col3:
        st.warning(f"💰 **Costing Calculator**\n\nPart price & profit calculation")
        st.warning(f"📄 **Quotation & PDF**\n\nDrawing quotation & export")

# ==================== 2. ROD & CONVERSION CALCULATOR ====================
elif menu == t["rod_calc"]:
    st.header(t["rod_calc"])
    st.write("ரா மெட்டீரியல் மீட்டர், கிலோ (KG) அல்லது பார்ட் எண்ணிக்கையாக எப்படி வந்தாலும் துல்லியமாகக் கணக்கிடலாம்.")

    col1, col2 = st.columns(2)
    with col1:
        raw_dia = st.number_input(t["raw_dia"], min_value=1.0, value=20.0, step=0.5)
        part_length = st.number_input(t["part_len"], min_value=1.0, value=126.0, step=1.0)
    with col2:
        cutting_allowance = st.number_input(t["cutting_all"], min_value=0.0, value=3.0, step=0.5)
        rod_standard_length = st.number_input(t["std_rod_len"], min_value=1.0, value=6.0, step=0.5)

    st.markdown("---")
    
    calc_mode = st.radio(
        t["mode_label"],
        (
            t["mode1"],
            t["mode2"],
            t["mode3"]
        )
    )

    effective_len = part_length + cutting_allowance
    weight_per_mm = math.pi * ((raw_dia / 2) ** 2) * 0.00000785
    weight_per_meter = weight_per_mm * 1000
    standard_rod_weight = rod_standard_length * weight_per_meter

    if t["mode1"] in calc_mode:
        st.subheader("📌 முறை 1: ராட் எண்ணிக்கையைக் கொண்டு கணக்கிடுதல்")
        num_rods = st.number_input("ராடுகளின் எண்ணிக்கை (Number of Rods)", min_value=1, value=10, step=1)
        
        if st.button(t["calc_btn"], type="primary"):
            total_length_mm = num_rods * rod_standard_length * 1000
            parts_per_rod = int((rod_standard_length * 1000) // effective_len) if effective_len > 0 else 0
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

    elif t["mode2"] in calc_mode:
        st.subheader("📌 முறை 2: கிலோ (KG) எடையைக் கொண்டு கணக்கிடுதல்")
        total_available_kg = st.number_input("உள்ளீடு மெட்டீரியல் எடை (Total KG Available)", min_value=0.1, value=50.0, step=1.0)

        if st.button(t["calc_btn"], type="primary"):
            total_length_meters = total_available_kg / weight_per_meter if weight_per_meter > 0 else 0
            total_length_mm = total_length_meters * 1000
            total_possible_parts = int(total_length_mm // effective_len) if effective_len > 0 else 0
            total_weight_used = total_possible_parts * (effective_len * weight_per_mm)
            scrap_weight_kg = total_available_kg - total_weight_used

            st.markdown(f"### 📊 {t['results']}")
            rc1, rc2 = st.columns(2)
            with rc1:
                st.metric("கிடைக்கும் மொத்த நீளம்", f"{total_length_meters:.2f} Meters")
                st.metric("உற்பத்தி செய்யக்கூடிய பார்ட்டுகள் (Qty)", f"{total_possible_parts} Nos")
            with rc2:
                st.metric("பயன்படுத்தப்பட்ட பார்ட் எடை", f"{total_weight_used:.2f} KG")
                st.metric("மீதமுள்ள ஸ்கிராப் எடை", f"{scrap_weight_kg:.2f} KG")

    else:
        st.subheader("📌 முறை 3: தேவையான பார்ட் எண்ணிக்கையைக் (Qty) கொண்டு ராட் / KG கணக்கிடுதல்")
        required_qty = st.number_input("தேவையான பார்ட் எண்ணிக்கை (Required Qty)", min_value=1, value=500, step=10)

        if st.button(t["calc_btn"], type="primary"):
            parts_per_rod = int((rod_standard_length * 1000) // effective_len) if effective_len > 0 else 0
            required_rods = math.ceil(required_qty / parts_per_rod) if parts_per_rod > 0 else 0
            total_kg_needed = required_rods * standard_rod_weight
            actual_parts_produced = parts_per_rod * required_rods
            total_scrap_mm = (required_rods * ((rod_standard_length * 1000) % effective_len))
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
                st.metric("மொத்த ராட் நீளம்", f"{required_rods * rod_standard_length:.2f} Meters")
                st.metric("ஸ்கிராப் நீளம்", f"{total_scrap_mm / 1000:.2f} Meters")

# ==================== 3. PRODUCTION CALCULATOR ====================
elif menu == t["prod_calc"]:
    st.header(t["prod_calc"])
    c_time = st.number_input("சைக்கிள் டைம் (Cycle Time - Seconds)", min_value=1.0, value=20.0)
    avail_time = st.number_input("கிடைக்கும் நேரம் / நாள் (Working Hours)", min_value=1.0, value=8.0)
    efficiency = st.number_input("மிஷின் எபிஷியன்சி (%)", min_value=1.0, value=85.0)
    break_time = st.number_input("ஓய்வு நேரம் / பிரேக் (Break Minutes)", min_value=0.0, value=30.0)

    if st.button(t["calc_btn"], type="primary"):
        net_working_hours = avail_time - (break_time / 60)
        pcs_per_hour = (3600 / c_time) * (efficiency / 100) if c_time > 0 else 0
        total_day_prod = pcs_per_hour * net_working_hours
        st.markdown("---")
        mc1, mc2 = st.columns(2)
        with mc1:
            st.metric("1 மணி நேர உற்பத்தி (Production / Hour)", f"{int(pcs_per_hour)} Nos")
        with mc2:
            st.metric("1 நாள் உற்பத்தி (Production / Day)", f"{int(total_day_prod)} Nos")

# ==================== 4. COSTING CALCULATOR ====================
elif menu == t["cost_calc"]:
    st.header(t["cost_calc"])
    mat_cost_kg = st.number_input("1 KG மெட்டீரியல் விலை (₹)", value=85.0)
    mat_wt_part = st.number_input("பார்ட் எடை (Material Weight / Part - Kg)", value=0.25)
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
            st.metric("பரிந்துரைக்கப்பட்ட விற்பனை விலை", f"₹ {total_cost_per_part * 1.25:.2f}")

# ==================== 5. STOCK MANAGEMENT ====================
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

# ==================== 6. AI DRAWING TO G-CODE GENERATOR ====================
elif menu == t["ai_prog"]:
    st.header(t["ai_prog"])
    st.write("கஸ்டமர் டிராயிங் அல்லது பார்ட் போட்டோவை அப்லோட் செய்து, அதற்கான CNC G-Code ப்ரோக்ராமை உடն உருவாக்கலாம்.")
    
    uploaded_drawing = st.file_uploader("பார்ட் டிராயிங் / போட்டோவை அப்லோட் செய்யவும் (Upload Drawing / Image)", type=["png", "jpg", "jpeg"])
    
    col1, col2 = st.columns(2)
    with col1:
        part_name = st.text_input("பார்ட் பெயர் / நம்பர் (Part Name / No)", "Part-01")
        prog_num = st.text_input("ப்ரோக்ராம் எண் (Program Number)", "O1001")
        raw_d = st.number_input("ரா மெட்டீரியல் டயா (Raw Dia - mm)", min_value=1.0, value=25.0, step=0.5)
    with col2:
        finish_d = st.number_input("பினிஷ்ட் டயா (Finished Dia - mm)", min_value=1.0, value=20.0, step=0.5)
        p_len = st.number_input("பார்ட் நீளம் (Part Length - mm)", min_value=1.0, value=50.0, step=1.0)
        feed = st.number_input("ஃபீட் ரேட் (Feed Rate - mm/rev)", min_value=0.01, value=0.15, step=0.01)
        
    if st.button("⚙️ CNC G-Code ப்ரோக்ராமை உருவாக்கு", type="primary"):
        if uploaded_drawing is not None:
            st.image(uploaded_drawing, caption="Uploaded Drawing Preview", width=350)
            
        gcode_content = f"""%
{prog_num}
(PART NAME: {part_name})
(RAW DIA: {raw_d} | FINISHED DIA: {finish_d} | LENGTH: {p_len})
G21 G40 G99 G18
G28 U0.0 W0.0
T0101 (TURNING TOOL)
G97 S2000 M03
G00 X{raw_d + 2.0} Z2.0
G01 Z0.0 F0.2
X{finish_d} F{feed}
Z-{p_len}
G00 X{raw_d + 5.0}
G28 U0.0 W0.0
M05
M30
%"""
        st.success("✅ CNC G-Code ப்ரோக்ராம் வெற்றிகரமாக உருவாக்கப்பட்டது!")
        st.code(gcode_content, language="gcode")
        st.download_button("⬇️ Download G-Code File (.nc)", data=gcode_content, file_name=f"{part_name}.nc", mime="text/plain")

# ==================== 7. QUOTATION & PDF ====================
elif menu == t["quotation"]:
    st.header(t["quotation"])
    cust_name = st.text_input("கஸ்டமர் கம்பெனி பெயர்", "ABC Industries")
    part_no = st.text_input("டிராயிங் எண் / பார்ட் பெயர்", "TR-001 - Trunion")
    uploaded_file_q = st.file_uploader("கஸ்டமர் டிராயிங் அப்லோட் (Image / PDF)", type=["png", "jpg", "jpeg", "pdf"], key="q_file")
    quoted_qty = st.number_input("கொட்டேஷன் தேவைப்படும் அளவு (Qty)", value=500)
    unit_price_q = st.number_input("ஒரு பார்ட்டுக்கான இறுதி விலை (₹)", value=9.00)

    if st.button("📄 PDF கொட்டேஷனை உருவாக்கு", type="primary"):
        st.success("✅ கொட்டேஷன் வெற்றிகரமாகத் தயாரிக்கப்பட்டது!")
        if uploaded_file_q is not None:
            if uploaded_file_q.type in ["image/png", "image/jpeg", "image/jpg"]:
                st.image(uploaded_file_q, caption="Uploaded Drawing Preview", width=300)
        st.info(f"📥 கஸ்டமர்: {cust_name} | பார்ட்: {part_no} | மொத்தம்: ₹ {quoted_qty * unit_price_q:,.2f}")
        st.download_button("⬇️ Download Quotation PDF", data="Sample PDF Content", file_name="Quotation_MegalaCNC.pdf")

# ==================== 8. SETTINGS / MORE MENU ====================
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
