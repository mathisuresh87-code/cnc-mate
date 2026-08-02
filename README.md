import math
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Megala CNC Mate - Smart CNC & Production",
    page_icon="⚙️",
    layout="wide",
)

# Custom Styling for Dashboard
st.markdown("""
    <style>
    .main-title { font-size: 28px; font-weight: bold; color: #1E3A8A; }
    .sub-title { font-size: 16px; color: #6B7280; }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("⚙️ மேகலா CNC மேட் (Megala CNC Mate)")
st.markdown("**SMART CNC. SIMPLE WORK.** — கஸ்டமர் கொட்டேஷன், உற்பத்தி மற்றும் ஸ்டாக் மேனேஜ்மெண்ட் சிஸ்டம்")
st.markdown("---")

# Navigation Menu matching the UI Dashboard
menu = st.sidebar.selectbox(
    "🧭 மெனு (Navigation Menu)",
    [
        "🏠 முகப்பு (Home Dashboard)",
        "📏 ராட் கால்குலேட்டர் (Rod Calculator)",
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

    # Dashboard Grid Layout matching the image
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("📏 **Rod Calculator**\n\nரா மெட்டீரியல் மற்றும் ஸ்கிராப் கணக்கீடு")
        st.info("📦 **Stock Management**\n\nஸ்டாக் இருப்பு மற்றும் விவரங்கள்")
    with col2:
        st.success("⏱️ **Production Calculator**\n\nசைக்கிள் டைம் மற்றும் ஷிப்ட் உற்பத்தி")
        st.success("📄 **Quotation & PDF**\n\nடிராயிங் அடிப்படையிலான கொட்டேஷன்")
    with col3:
        st.warning("💰 **Costing Calculator**\n\nபார்ட் விலை மற்றும் லாபக் கணக்கீடு")
        st.warning("⚙️ **Settings & Master**\n\nகஸ்டமர் மற்றும் மெஷின் மாஸ்டர்")

    st.markdown("---")
    st.subheader("📌 சமீபத்திய கணக்கீடுகள் (Recent Calculations)")
    st.markdown("""
    * **Trunion - MS EN8** | 22 May 2026 | 10:30 AM 
    * **Latch Pin** | 22 May 2026 | 09:15 AM
    """)

# ==================== 2. ROD CALCULATOR ====================
elif menu == "📏 ராட் கால்குலேட்டர் (Rod Calculator)":
    st.header("📏 ராட் மற்றும் ஸ்கிராப் கால்குலேட்டர்")
    
    mode = st.radio("Mode Selection", ["Simple Mode", "Advanced Mode"], horizontal=True)

    col1, col2 = st.columns(2)
    with col1:
        rod_length = st.number_input("ராட் நீளம் (Rod Length - Meters)", min_value=0.1, value=6.0, step=0.5)
        part_length = st.number_input("பார்ட் நீளம் (Part Length - mm)", min_value=1.0, value=126.0, step=1.0)
        cutting_allowance = st.number_input("கட்டிங் அலவன்ஸ் / குருவ் (Cutting Allowance - mm)", min_value=0.0, value=3.0, step=0.5)
    with col2:
        required_qty = st.number_input("தேவையான பார்ட்டுகள் (Required Qty - Nos)", min_value=1, value=500, step=10)
        cycle_time = st.number_input("சைக்கிள் டைம் (Cycle Time - Seconds)", min_value=1.0, value=20.0, step=1.0)

    if st.button("📊 ஆட்டோ கணக்கிடு (Auto Calculate)", type="primary"):
        effective_len = part_length + cutting_allowance
        rod_total_mm = rod_length * 1000
        parts_per_rod = int(rod_total_mm // effective_len)
        balance_mm = rod_total_mm % effective_len
        required_rods = math.ceil(required_qty / parts_per_rod) if parts_per_rod > 0 else 0
        total_stock_length = required_rods * rod_length
        pcs_per_hr = 3600 / cycle_time if cycle_time > 0 else 0
        total_machine_time_hrs = (cycle_time * required_qty) / 3600

        st.markdown("---")
        st.subheader("📈 கணக்கீட்டு முடிவுகள் (Calculation Result)")

        res_c1, res_c2, res_c3 = st.columns(3)
        with res_c1:
            st.metric("பார்ட் / ராட் (Parts / Rod)", f"{parts_per_rod} Nos")
            st.metric("தேவையான ராடுகள் (Required Rods)", f"{required_rods} Nos")
        with res_c2:
            st.metric("மீதம் (Balance / Scrap)", f"{balance_mm:.2f} mm")
            st.metric("மொத்த ராட் நீளம் (Total Stock Length)", f"{total_stock_length:.2f} m")
        with res_c3:
            st.metric("உற்பத்தி / மணி நேரம் (Production / Hour)", f"{int(pcs_per_hr)} Nos")
            st.metric("மொத்த மிஷின் நேரம் (Total Machine Time)", f"{total_machine_time_hrs:.2f} Hr")

# ==================== 3. PRODUCTION CALCULATOR ====================
elif menu == "⏱️ ப்ரொடக்ஷன் கால்குலேட்டர் (Production Calculator)":
    st.header("⏱️ ப்ரொடக்ஷன் மற்றும் ஷிப்ட் கால்குலேட்டர்")

    p1, p2 = st.columns(2)
    with p1:
        c_time = st.number_input("சைக்கிள் டைம் (Seconds)", min_value=1.0, value=20.0)
        avail_time = st.number_input("கிடைக்கும் நேரம் / நாள் (Hours)", min_value=1.0, value=8.0)
    with p2:
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

    cc1, cc2 = st.columns(2)
    with cc1:
        mat_cost_kg = st.number_input("1 KG மெட்டீரியல் விலை (₹)", value=85.0)
        mat_wt_part = st.number_input("பார்ட் எடை (Material Weight / Part - Kg)", value=0.25)
        machine_cost_hr = st.number_input("1 மணி நேர மிஷின் கட்டணம் (₹)", value=600.0)
    with cc2:
        labour_cost_part = st.number_input("லேபர் செலவு / பார்ட் (₹)", value=1.20)
        overhead_pct = st.number_input("மேலதிகச் செலவு / Overhead (%)", value=15.0)

    if st.button("📊 விலையைக் கணக்கிடு", type="primary"):
        material_total = mat_cost_kg * mat_wt_part
        machine_part_cost = (machine_cost_hr / 3600) * 20  # assuming 20 sec cycle
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

    q_col1, q_col2 = st.columns(2)
    with q_col1:
        cust_name = st.text_input("கஸ்டமர் கம்பெனி பெயர்", "ABC Industries")
        part_no = st.text_input("டிராயிங் எண் / பார்ட் பெயர்", "TR-001 - Trunion")
        uploaded_drawing = st.file_uploader("கஸ்டமர் டிராயிங் அப்லோட் (Image / PDF)", type=["png", "jpg", "jpeg", "pdf"])
    with q_col2:
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
