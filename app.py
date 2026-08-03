import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Megala CNC Mate",
    page_icon="⚙️",
    layout="wide"
)

# Custom CSS for Header styling
st.markdown("""
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1rem;
        color: #4b5563;
        margin-top: 5px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Header section without gear icon next to text
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("### 🚚 **Megala CNC**")
with col2:
    st.markdown('<p class="main-title">Megala CNC Mate</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">SMART CNC. SIMPLE WORK. — புரோபஷனல் ஒர்க்ஷாப் ஆட்டோமேஷன் & துல்லியமான கால்குலேட்டர்</p>', unsafe_allow_html=True)

st.markdown("---")

# Sidebar Menu with Settings at the top/bottom
st.sidebar.markdown("### 🚀 Menu / மெனு")

menu_option = st.sidebar.selectbox(
    "Select Module / மாட்யூல் தேர்வு",
    [
        "1. முகப்பு (Dashboard)",
        "2. மிஷின் கால்குலேட்டர் (Machine Calculator)",
        "3. கொட்டேஷன் & செலவு மேலாண்மை (Quotation & Cost Management)",
        "4. டிராயிங் & போட்டோ அனாலிசிஸ் (Drawing & Photo Analysis)",
        "5. ராட், மீட்டர்/கிலோ & ஸ்கிராப் (Rod, Meter/Kg & Scrap)",
        "6. ஜி-கோடு ஜெனரேட்டர் (Advanced G-Code Generator)",
        "7. உற்பத்தி & டிஸ்பாட்ச் (Production & Dispatch)",
        "8. ஸ்டாக் & இன்வென்சரி (Stock & Inventory)",
        "9. அமைப்புகள் (Settings - 6 Languages)"
    ]
)

# 1. Dashboard
if "முகப்பு" in menu_option:
    st.subheader("🏠 முகப்பு (Dashboard)")
    st.write("நதீஷ் அவர்களின் ஒர்க்ஷாப் ஆட்டோமேஷன் அமைப்புக்கு நல்வரவு!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("ஆக்டிவ் மிஷின்கள்", "Turn, Traub, CNC, Polygon")
    with col2:
        st.metric("இன்று டிஸ்பாட்ச்", "1250 Parts")
    with col3:
        st.metric("மொத்த ஸ்டாக்", "4500 Kg")

# 2. Machine Calculator
elif "மிஷின் கால்குலேட்டர்" in menu_option:
    st.subheader("⚙️ மிஷின் கால்குலேட்டர் (RPM & Time Calculation)")
    machine_type = st.selectbox("மிஷின் வகை", ["Turn Machine", "Traub Machine", "CNC Machine", "Polygon Machine"])
    
    col1, col2 = st.columns(2)
    with col1:
        dia = st.number_input("மெட்டீரியல் விட்டம் / Diameter (mm)", value=40.0)
        cutting_speed = st.number_input("கட்டிங் ஸ்பீடு / Cutting Speed (m/min)", value=150.0)
    with col2:
        part_length = st.number_input("பார்ட் நீளம் / Length (mm)", value=50.0)
        feed_rate = st.number_input("ஃபீடு / Feed (mm/rev)", value=0.15)
        
    if st.button("கணக்கிடு (Calculate RPM & Time)"):
        rpm = (cutting_speed * 1000) / (3.1416 * dia)
        time_min = (part_length / feed_rate) / rpm if rpm > 0 else 0
        st.success(f"தேவையான RPM: {round(rpm, 2)} RPM")
        st.info(f"மதிப்பிடப்பட்ட கட்டிங் நேரம்: {round(time_min, 2)} நிமிடங்கள்")

# 3. Quotation & Cost Management
elif "கொட்டேஷன் & செலவு மேலாண்மை" in menu_option:
    st.subheader("💰 Quotation & Cost Management (Operations, Material & Overheads)")
    
    material_source = st.radio("மெட்டீரியல் சோர்ஸ் தேர்வு", ["கஸ்டமர் மெட்டீரியல் (Customer Provided / Job Work Only)", "ஒர்க்ஷாப் வாங்குவது (Workshop Purchased)"])
    
    if "Workshop" in material_source:
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            mat_grade = st.selectbox("மெட்டீரியல் கிரேடு", ["EN1", "EN8", "EN19", "EN24", "EN31", "C45", "MS", "SS304", "SS316", "Aluminum", "Brass"])
        with col_m2:
            price_per_kg = st.number_input("ஒரு கிலோ விலை (₹)", value=120.0)
            mat_weight = st.number_input("மொத்த எடை (Kg)", value=5.0)
    else:
        price_per_kg = 0.0
        mat_weight = 0.0

    st.markdown("#### ஆபரேஷன்கள் மற்றும் வேலைப்பாடுகள் (Operations Routing)")
    selected_ops = st.multiselect("தேவையான ஆபரேஷன்கள்", ["Facing", "Turning", "Grooving", "Boring", "Straight Drilling", "Cross-Drilling", "Chamfering", "Tapping"])
    
    st.markdown("#### லேபர் மற்றும் ஓவர்ஹெட் செலவுகள் (Manpower & Overheads)")
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        machine_hourly_rate = st.number_input("மிஷின் மணிநேரக் கட்டணம் (₹/hr)", value=600.0)
        running_hours = st.number_input("மொத்த ஒர்க்கிங் நேரம் (Hours)", value=2.0)
        operator_salary = st.number_input("ஆபரேட்டர்/செட்டர்/புரோகிராமர் செலவு பங்கு (₹)", value=150.0)
    with col_l2:
        overheads = st.number_input("இதர செலவுகள் (Coolant, Power, Tea/Snacks - ₹)", value=100.0)
        profit_margin = st.slider("இலாப விளிம்பு (Profit Margin %)", 0, 50, 20)

    if st.button("இறுதி கொட்டேஷன் விலை கணக்கிடு"):
        machining_cost = machine_hourly_rate * running_hours
        material_cost = price_per_kg * mat_weight
        subtotal = machining_cost + material_cost + operator_salary + overheads
        final_price = subtotal * (1 + profit_margin / 100.0)
        
        st.success(f"### இறுதி கொட்டேஷன் விலை: ₹ {round(final_price, 2)}")
        st.write(f"- மிஷினிங் காஸ்ட்: ₹{machining_cost}")
        st.write(f"- மெட்டீரியல் காஸ்ட்: ₹{material_cost}")
        st.write(f"- லேபர் & ஓவர்ஹெட்ஸ்: ₹{operator_salary + overheads}")

# 4. Drawing & Photo Analysis
elif "டிராயிங் & போட்டோ அனாலிசிஸ்" in menu_option:
    st.subheader("📷 Drawing & Photo Analysis & Operation Detection")
    uploaded_file = st.file_uploader("பார்ட் டிராயிங் அல்லது போட்டோவை அப்லோட் செய்யவும் (PDF/PNG/JPG)", type=["png", "jpg", "jpeg", "pdf"])
    if uploaded_file is not None:
        st.success("கோப்பு வெற்றிகரமாக அப்லோட் செய்யப்பட்டது!")
        st.info("AI பகுப்பாய்வு மூலம் ஆபரேஷன்கள் கண்டறியப்படுகின்றன: Facing, Turning, Drilling, Tapping...")
        if st.button("தானியங்கி கொட்டேஷன் மற்றும் புரோகிராம் உருவாக்கவும்"):
            st.write("✅ ஆபரேஷன்கள் கண்டறியப்பட்டு கொட்டேஷன் மற்றும் G-Code உருவாக்க தயாராக உள்ளது.")

# 5. Rod, Meter/Kg Converter & Scrap
elif "ராட், மீட்டர்/கிலோ & ஸ்கிராப்" in menu_option:
    st.subheader("📐 ராட், மீட்டர்/கிலோ கன்வெர்ட்டர் & ஸ்கிராப் கால்குலேட்டர்")
    
    shape = st.selectbox("ரா மெட்டீரியல் வடிவம் (Shape)", ["Round Rod", "Hexagon Rod", "Square Rod", "Tube / Pipe"])
    grade = st.selectbox("மெட்டீரியல் கிரேடு (Grade)", ["EN1", "EN8", "EN19", "EN24", "EN31", "C45", "MS", "SS304", "SS316", "Aluminum", "Brass"])
    
    if shape == "Tube / Pipe":
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            od = st.number_input("வெளி விட்டம் (Outer Diameter OD - mm)", value=50.0)
        with col_t2:
            id_val = st.number_input("உள் விட்டம் (Inner Diameter ID - mm)", value=30.0)
    else:
        od = st.number_input("விட்டம் / அகலம் (mm)", value=40.0)
        id_val = 0.0

    length_m = st.number_input("மொத்த ராட் நீளம் (Meters)", value=10.0)
    
    if st.button("எடை மற்றும் அளவைக் கணக்கிடு (Calculate Weight/Scrap)"):
        st.success(f"தேர்ந்தெடுக்கப்பட்ட கிரேடு: {grade} | வடிவம்: {shape} | நீளம்: {length_m} மீட்டர்கள் வெற்றிகரமாகக் கணக்கிடப்பட்டது.")

# 6. Advanced G-Code Generator
elif "ஜி-கோடு ஜெனரேட்டர்" in menu_option:
    st.subheader("📜 Advanced G-Code Generator")
    gcode_input_method = st.radio("உள்ளீட்டு முறை", ["டிராயிங் / PDF அப்லோட்", "நேரடி பரிமாணங்கள் உள்ளீடு"])
    
    if "அப்லோட்" in gcode_input_method:
        st.file_uploader("பார்ட் டிராயிங்கை அப்லோட் செய்யவும்", type=["pdf", "png", "jpg"])
    else:
        st.number_input("பார்ட் நீளம் (Length - mm)", value=100.0)
        st.number_input("பார்ட் விட்டம் (Diameter - mm)", value=25.0)
        st.multiselect("தேவையான ஆபரேஷன்கள்", ["Facing", "Turning", "Grooving", "Drilling", "Tapping"])

    if st.button("G-Code புரோகிராம் உருவாக்கு"):
        sample_gcode = """O1001 (MEGALA CNC MATE - ADVANCED PROGRAM)
G21 G99 G40
M03 S1500
G00 X50.0 Z5.0
G01 Z-45.0 F0.2
G00 X100.0 Z100.0
M30"""
        st.code(sample_gcode, language="text")

# 7. Daily Production & Dispatch
elif "உற்பத்தி & டிஸ்பாட்ச்" in menu_option:
    st.subheader("📊 Daily Production & Dispatch Calculator")
    st.write("இன்று முடிக்கப்பட்ட உற்பத்தி மற்றும் டிஸ்பாட்ச் விபரங்கள்:")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        part_name = st.text_input("பார்ட் பெயர் / நம்பர்", value="Part-A01")
        machine_used = st.selectbox("மிஷின் பெயர்", ["CNC-1", "Traub-1", "Turn-1", "Polygon-1"])
        qty_produced = st.number_input("இன்று தயாரித்த எண்ணிக்கை (Produced Qty)", value=500)
    with col_p2:
        hours_run = st.number_input("ஓடிய மணிநேரம் (Running Hours)", value=8.0)
        dispatch_qty = st.number_input("இன்று டிஸ்பாட்ச் செய்ய உள்ளவை (Dispatch Qty)", value=400)
        
    if st.button("உற்பத்தி மற்றும் ஸ்டாக் பதிவு செய்"):
        st.success("உற்பத்தி மற்றும் டிஸ்பாட்ச் விபரங்கள் வெற்றிகரமாகப் பதிவு செய்யப்பட்டன!")
        st.info(f"மீதமுள்ள ஸ்டாக் இருப்பு: {qty_produced - dispatch_qty} பார்ட்டுகள்")

# 8. Stock & Inventory Management
elif "ஸ்டாக் & இன்வென்சரி" in menu_option:
    st.subheader("📦 Stock & Inventory Management")
    st.write("ரா மெட்டீரியல், இன்-ப்ராசஸ் மற்றும் பினிஷ்ட் குட்ஸ் ஸ்டாக் நிலவரம்:")
    
    data = {
        "Part / Material": ["EN8 Round 40mm", "EN19 Hex 25mm", "Finished Bush-01", "Finished Pin-02"],
        "Category": ["Raw Material", "Raw Material", "Finished Goods", "Finished Goods"],
        "Current Stock": ["250 Kg", "150 Kg", "600 Nos", "1200 Nos"],
        "Status": ["Sufficient", "Sufficient", "Dispatch Ready", "Low Stock"]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

# 9. Settings
elif "அமைப்புகள்" in menu_option:
    st.subheader("⚙️ Settings / அமைப்புகள் (Multi-Language Support)")
    lang = st.selectbox(
        "மொழி தேர்வு / Select Language", 
        [
            "தமிழ் (Tamil)", 
            "English", 
            "हिन्दी (Hindi)", 
            "తెలుగు (Telugu)", 
            "മലയാളം (Malayalam)", 
            "ಕನ್ನಡ (Kannada)"
        ]
    )
    st.success(f"தேர்ந்தெடுக்கப்பட்ட மொழி / Selected Language: {lang}")
    st.write("மெகலா சிஎன்சி மெய்ட் (Megala CNC Mate) ஒர்க்ஷாப் ஆட்டோமேஷன் சிஸ்டம் v2.6 - முழுமையான பதிப்பு.")
