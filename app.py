import math
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Megala CNC Mate - Smart CNC & Production",
    page_icon="⚙️",
    layout="wide",
)

st.title("⚙️ மேகலா CNC மேட் (Megala CNC Mate)")
st.markdown("**SMART CNC. SIMPLE WORK.** — கஸ்டமர் கொட்டேஷன், உற்பத்தி மற்றும் ஸ்டாக் மேனேஜ்மெண்ட் சிஸ்டம்")
st.markdown("---")

menu = st.sidebar.selectbox(
    "🧭 மெனு (Navigation Menu)",
    [
        "🏠 முகப்பு (Home Dashboard)",
        "📏 ராட் & கன்வெர்ட்டர் கால்குலேட்டர் (Rod & Conversion)",
        "⏱️ ப்ரொடக்ஷன் கால்குலேட்டர் (Production Calculator)",
        "💰 காஸ்டிங் கால்குலேட்டர் (Costing Calculator)",
        "📦 ஸ்டாக் மேனேஜ்மெண்ட் (Stock Management)",
        "📄 கொட்டேஷன் & PDF (Quotation & PDF)",
        "⚙️ செட்டிங்ஸ் / More Menu",
    ]
)

# ==================== 1. HOME DASHBOARD ====================
if menu == "🏠 முகப்பு (Home Dashboard)":
    st.markdown("### Hello, Suresh! Good Morning 👋")
    st.write("இப்போது உங்கள் ஷாப் ப்ளோர் கணக்கீடுகள் அனைத்தையும் ஒரே இடத்தில் கையாளலாம்.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📏 **Rod & Conversion**\n\nமெட்டீரியல் மீட்டர், KG மற்றும் Qty கன்வெர்ட்டர்")
        st.info("📦 **Stock Management**\n\nஸ்டாக் இருப்பு மற்றும் விவரங்கள்")
    with col2:
        st.success("⏱️ **Production Calculator**\n\nசைக்கிள் டைம் மற்றும் ஷிப்ட் உற்பத்தி")
        st.success("📄 **Quotation & PDF**\n\nடிராயிங் அடிப்படையிலான கொட்டேஷன்")
    with col3:
        st.warning("💰 **Costing Calculator**\n\nபார்ட் விலை மற்றும் லாபக் கணக்கீடு")
        st.warning("⚙️ **Settings & Master**\n\nகஸ்டமர் மற்றும் மெஷின் மாஸ்டர்")

# ==================== 2. ROD & CONVERSION CALCULATOR ====================
elif menu == "📏 ராட் & கன்வெர்ட்டர் கால்குலேட்டர் (Rod & Conversion)":
    st.header("📏 ராட், மீட்டர், KG மற்றும் ஸ்கிராப் கன்வெர்ட்டர் கால்குலேட்டர்")
    st.write("ரா மெட்டீரியல் மீட்டர், கிலோ (KG) அல்லது பார்ட் எண்ணிக்கையாக எப்படி வந்தாலும் துல்லியமாகக் கணக்கிடலாம்.")

    # Common Inputs for Material
    col1, col2 = st.columns(2)
    with col1:
        raw_dia = st.number_input("ரா மெட்டீரியல் டயா (Raw Dia - mm)", min_value=1.0, value=20.0, step=0.5)
        part_length = st.number_input("பார்ட் நீளம் (Part Length - mm)", min_value=1.0, value=126.0, step=1.0)
    with col2:
        cutting_allowance = st.number_input("கட்டிங் அலவன்ஸ் / குருவ் (Cutting Allowance - mm)", min_value=0.0, value=3.0, step=0.5)
        rod_standard_length = st.number_input("ஒரு ஸ்டாண்டர்ட் ராட் நீளம் (Standard Rod Length - Meters)", min_value=1.0, value=6.0, step=0.5)

    st.markdown("---")
    
    # Selection of Input Type
    calc_mode = st.radio(
        "உங்களிடம் உள்ள மெட்டீரியல் விபரம் என்ன முறையில் உள்ளது?",
        (
            "1. ராட் நீளம் & எண்ணிக்கை மூலம் (Meters / Rods Count)",
            "2. கிலோ (KG) மூலம் மெட்டீரியல் உள்ளீடு",
            "3. தேவையான பார்ட் எண்ணிக்கை மூலம் (Required Qty)"
        )
    )

    # Formulas for weight & length conversion (Steel density approx 0.00000785 kg/mm3)
    effective_len = part_length + cutting_allowance  # mm per part including cut
    weight_per_mm = math.pi * ((raw_dia / 2) ** 2) * 0.00000785  # kg per mm
    weight_per_meter = weight_per_mm * 1000  # kg per meter
    standard_rod_weight = rod_standard_length * weight_per_meter  # kg per standard rod (e.g., 6m)

    if "1. ராட் நீளம்" in calc_mode:
        st.subheader("📌 முறை 1: ராட் எண்ணிக்கையைக் கொண்டு கணக்கிடுதல்")
        num_rods = st.number_input("உள்ள bei ராடுகளின் எண்ணிக்கை (Number of Rods)", min_value=1, value=10, step=1)
        
        if st.button("📊 கணக்கிடு (Calculate Meters, Qty & Scrap)", type="primary"):
            total_length_mm = num_rods * rod_standard_length * 1000
            parts_per_rod = int((rod_standard_length * 1000) // effective_len) if effective_len > 0 else 0
            total_parts = parts_per_rod * num_rods
            balance_mm_per_rod = (rod_standard_length * 1000) % effective_len
            total_scrap_mm = balance_mm_per_rod * num_rods
            total_weight_kg = num_rods * standard_rod_weight
            total_scrap_weight_kg = total_scrap_mm * weight_per_mm

            st.markdown("---")
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

    elif "2. கிலோ (KG)" in calc_mode:
        st.subheader("📌 முறை 2: கிலோ (KG) எடையைக் கொண்டு கணக்கிடுதல்")
        total_available_kg = st.number_input("உள்ளீடு மெட்டீரியல் எடை (Total KG Available)", min_value=0.1, value=50.0, step=1.0)

        if st.button("📊 KG-ஐ பார்ட் மற்றும் மீட்டராக மாற்று", type="primary"):
            total_length_meters = total_available_kg / weight_per_meter if weight_per_meter > 0 else 0
            total_length_mm = total_length_meters * 1000
            total_possible_parts = int(total_length_mm // effective_len) if effective_len > 0 else 0
            total_weight_used = total_possible_parts * (effective_len * weight_per_mm)
            scrap_weight_kg = total_available_kg - total_weight_used

            st.markdown("---")
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

        if st.button("📊 தேவைப்படும் ராட் & KG கணக்கிடு", type="primary"):
            parts_per_rod = int((rod_standard_length * 1000) // effective_len) if effective_len > 0 else 0
            required_rods = math.ceil(required_qty / parts_per_rod) if parts_per_rod > 0 else 0
            total_kg_needed = required_rods * standard_rod_weight
            actual_parts_produced = parts_per_rod * required_rods
            total_scrap_mm = (required_rods * ((rod_standard_length * 1000) % effective_len))
            total_scrap_kg = total_scrap_mm * weight_per_mm

            st.markdown("---")
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
elif menu == "⏱️ ப்ரொடக்ஷன் கால்குலேட்டர் (Production Calculator)":
    st.header("⏱️ ப்ரொடக்ஷன் மற்றும் ஷிப்ட் கால்குலேட்டர்")
    c_time = st.number_input("சைக்கிள் டைம் (Seconds)", min_value=1.0, value=20.0)
    avail_time = st.number_input("கிடைக்கும் நேரம் / நாள் (Hours)", min_value=1.0, value=8.0)
    efficiency = st.number_input("மிஷின் எபிஷியன்சி (%)", min_value=1.0, value=85.0)
    break_time = st.number_input("ஓய்வு நேரம் / பிரேக் (Minutes)", min_value=0.0, value=30.0)

    if st.button("⚙️ உற்பத்தித் திறனைக் கணக்கிடு", type="primary"):
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
elif menu == "💰 காஸ்டிங் கால்குலேட்டர் (Costing Calculator)":
    st.header("💰 காஸ்டிங் மற்றும் விலை நிர்ணய கால்குலேட்டர்")
    mat_cost_kg = st.number_input("1 KG மெட்டீரியல் விலை (₹)", value=85.0)
    mat_wt_part = st.number_input("பார்ட் எடை (Material Weight / Part - Kg)", value=0.25)
    machine_cost_hr = st.number_input("1 மணி நேர மிஷின் கட்டணம் (₹)", value=600.0)
    labour_cost_part = st.number_input("லேபர் செலவு / பார்ட் (₹)", value=1.20)
    overhead_pct = st.number_input("மேலதிகச் செலவு / Overhead (%)", value=15.0)

    if st.button("📊 விலையைக் கணக்கிடு", type="primary"):
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
elif menu == "📦 ஸ்டாக் மேனேஜ்மெண்ட் (Stock Management)":
    st.header("📦 ஸ்டாக் மேனேஜ்மெண்ட் மற்றும் இருப்பு விபரங்கள்")
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

# ==================== 6. QUOTATION & PDF ====================
elif menu == "📄 கொட்டேஷன் & PDF (Quotation & PDF)":
    st.header("📄 டிராயிங் அடிப்படையிலான கொட்டேஷன் & PDF தயாரிப்பு")
    cust_name = st.text_input("கஸ்டமர் கம்பெனி பெயர்", "ABC Industries")
    part_no = st.text_input("டிராயிங் எண் / பார்ட் பெயர்", "TR-001 - Trunion")
    uploaded_drawing = st.file_uploader("கஸ்டமர் டிராயிங் அப்லோட் (Image / PDF)", type=["png", "jpg", "jpeg", "pdf"])
    quoted_qty = st.number_input("கொட்டேஷன் தேவைப்படும் அளவு (Qty)", value=500)
    unit_price_q = st.number_input("ஒரு பார்ட்டுக்கான இறுதி விலை (₹)", value=9.00)

    if st.button("📄 PDF கொட்டேஷனை உருவாக்கு", type="primary"):
        st.success("✅ கொட்டேஷன் வெற்றிகரமாகத் தயாரிக்கப்பட்டது!")
        if uploaded_drawing is not None:
            if uploaded_drawing.type in ["image/png", "image/jpeg", "image/jpg"]:
                st.image(uploaded_drawing, caption="Uploaded Drawing Preview", width=300)
        st.info(f"📥 கஸ்டமர்: {cust_name} | பார்ட்: {part_no} | மொத்தம்: ₹ {quoted_qty * unit_price_q:,.2f}")
        st.download_button("⬇️ Download Quotation PDF", data="Sample PDF Content", file_name="Quotation_MegalaCNC.pdf")

# ==================== 7. SETTINGS / MORE MENU ====================
elif menu == "⚙️ செட்டிங்ஸ் / More Menu":
    st.header("⚙️ கணினி மற்றும் மாஸ்டர் செட்டிங்ஸ்")
    st.markdown("""
    * 👤 **Part Master** (பார்ட் விவரங்களை நிர்வகிக்க)
    * 🏢 **Customer Master** (கஸ்டமர் பட்டியலை நிர்வகிக்க)
    * ⚙️ **Machine Master** (மிஷின் விவரங்களை நிர்வகிக்க)
    * 🔩 **Material Master** (மெட்டீரியல் கிரேடு மற்றும் விலை)
    * 🛠️ **Tool Master** (டூல் மற்றும் இன்செர்ட் விபரங்கள்)
    * 💾 **Backup & Restore** (டேட்டா பேக்கப் எடுக்க)
    * ℹ️ **About CNC Mate** (சாஃப்ட்வேர் தகவல்)
    """)
