import streamlit as st
import pandas as pd

# 1. பக்கத்தின் அடிப்படை அமைப்புகள் (Page Configuration)
st.set_page_config(
    page_title="Megala CNC Mate",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. நவீன டார்க் தீம் மற்றும் கார்டு CSS ஸ்டைல்கள்
st.markdown("""
<style>
    /* Dark Theme Background */
    .stApp {
        background-color: #0e1117;
        color: #e0e6ed;
    }
    
    /* Header Banner Styling */
    .header-banner {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        margin-bottom: 25px;
        text-align: center;
    }
    .header-banner h1 {
        color: #38bdf8;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
    }
    .header-banner p {
        color: #94a3b8;
        font-size: 1.0rem;
        margin-top: 5px;
    }

    /* Interactive Card Layout */
    .card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .card:hover {
        border-color: #38bdf8;
        box-shadow: 0 6px 16px rgba(56, 189, 248, 0.2);
    }
    .card-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #f8fafc;
        margin-bottom: 8px;
    }
    .card-desc {
        font-size: 0.88rem;
        color: #94a3b8;
    }
    
    /* Metric Display Box */
    .metric-box {
        background: #0f172a;
        border: 1px solid #334155;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #38bdf8;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
    }
</style>
""", unsafe_allow_html=True)

# 3. ஹெடர் பேனர் (Header Banner)
st.markdown("""
<div class="header-banner">
    <h1>⚙️ MEGALA CNC MATE</h1>
    <p>தொழில்முறை சிஎன்சி & டிராப் மெஷினரி ஒருங்கிணைக்கப்பட்ட மேலாண்மைத் தளம் (Industrial CNC & Traub Suite)</p>
</div>
""", unsafe_allow_html=True)

# 4. பக்கவாட்டு மெனு (Sidebar Navigation)
st.sidebar.title("Megala CNC Mate")
st.sidebar.markdown("---")

selected_tab = st.sidebar.radio(
    "பிரிவைத் தேர்ந்தெடுக்கவும் (Navigation):",
    [
        "🏠 முகப்பு (Dashboard)",
        "🧮 சிஎன்சி கணக்கீடுகள் (CNC Calc)",
        "⚙️ டிராப் காலெட் செட்டிங்ஸ் (Traub Settings)",
        "📊 உற்பத்தி திறன் (OEE & Production)",
        "📑 அறிக்கை தயாரிப்பு (Reports)",
        "🤖 AI ப்ளூபிரிண்ட் & IoT (AI & IoT)"
    ]
)

# ---------------------------------------------------------
# TAB 1: முகப்பு (DASHBOARD)
# ---------------------------------------------------------
if selected_tab == "🏠 முகப்பு (Dashboard)":
    st.subheader("📌 முதன்மை கட்டுப்பாட்டு மையம் (Quick Access Cards)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-title">🧮 சிஎன்சி கணக்கீடுகள்</div>
            <div class="card-desc">RPM, Cutting Speed, Feed Rate மற்றும் Cycle Time கணக்கிடும் கருவி.</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-title">⚙️ டிராப் காலெட் வழிகாட்டி</div>
            <div class="card-desc">Traub Collet வகைகள், Guide Bush இடைவெளி மற்றும் செட்டிங்ஸ் அளவுகள்.</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
            <div class="card-title">📊 உற்பத்தி திறன் & OEE</div>
            <div class="card-desc">ஷிப்ட் உற்பத்தி இலக்கு, டவுன்டைம் பகுப்பாய்வு மற்றும் OEE கணக்கீடு.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📈 இன்றைய லைவ் உற்பத்தி நிலை (Live Shift Summary)")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown('<div class="metric-box"><div class="metric-value">450 Pcs</div><div class="metric-label">உற்பத்தி செய்யப்பட்டவை</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="metric-box"><div class="metric-value">94.2%</div><div class="metric-label">ஒட்டுமொத்த திறன் (OEE)</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="metric-box"><div class="metric-value">15 Min</div><div class="metric-label">டவுன்டைம் (Downtime)</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown('<div class="metric-box"><div class="metric-value">0.8%</div><div class="metric-label">நிராகரிப்பு விகிதம்</div></div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: சிஎன்சி கணக்கீடுகள் (CNC CALC)
# ---------------------------------------------------------
elif selected_tab == "🧮 சிஎன்சி கணக்கீடுகள் (CNC Calc)":
    st.subheader("🧮 CNC Speed, Feed & Cycle Time Calculator")
    
    calc_option = st.selectbox("கணக்கீட்டின் வகையைத் தேர்ந்தெடுக்கவும்:", [
        "Spindle Speed (RPM) & Cutting Speed (Vc)",
        "Feed Rate (mm/min)",
        "Machining Cycle Time"
    ])
    
    if calc_option == "Spindle Speed (RPM) & Cutting Speed (Vc)":
        c1, c2 = st.columns(2)
        with c1:
            diameter = st.number_input("பொருளின் விட்டம் (Workpiece Diameter - D in mm):", value=25.0, step=1.0)
            vc = st.number_input("Cutting Speed (Vc in m/min):", value=120.0, step=5.0)
        with c2:
            if diameter > 0:
                rpm = (vc * 1000) / (3.14159 * diameter)
                st.success(f"🎯 கணக்கிடப்பட்ட Spindle Speed (RPM): **{int(rpm)} RPM**")
                st.caption("Formula: RPM = (Vc × 1000) / (π × D)")

    elif calc_option == "Feed Rate (mm/min)":
        c1, c2 = st.columns(2)
        with c1:
            rpm_input = st.number_input("Spindle Speed (RPM):", value=1500, step=100)
            feed_per_rev = st.number_input("Feed per Rev (f in mm/rev):", value=0.15, step=0.01)
        with c2:
            table_feed = rpm_input * feed_per_rev
            st.success(f"🎯 கணக்கிடப்பட்ட Feed Rate: **{table_feed:.2f} mm/min**")
            st.caption("Formula: F = RPM × f")

    elif calc_option == "Machining Cycle Time":
        c1, c2 = st.columns(2)
        with c1:
            length = st.number_input("வெட்டும் நீளம் (Length - L in mm):", value=50.0, step=5.0)
            feed_rate = st.number_input("Feed Rate (F in mm/min):", value=225.0, step=10.0)
            num_passes = st.number_input("பாஸ்களின் எண்ணிக்கை (Passes):", value=2, step=1)
        with c2:
            if feed_rate > 0:
                time_sec = ((length * num_passes) / feed_rate) * 60
                st.success(f"🎯 ஒரு பாகத்திற்கான நேரம் (Cycle Time): **{time_sec:.1f} வினாடிகள்**")

# ---------------------------------------------------------
# TAB 3: டிராப் காலெட் செட்டிங்ஸ் (TRAUB SETTINGS)
# ---------------------------------------------------------
elif selected_tab == "⚙️ டிராப் காலெட் செட்டிங்ஸ் (Traub Settings)":
    st.subheader("⚙️ டிராப் தானியங்கி லேத் காலெட் வழிகாட்டி (Traub Settings)")
    
    machine_model = st.selectbox("டிராப் மெஷின் மாடல்:", ["Traub A15 / A25", "Traub A42 / A60", "Traub TB42"])
    
    col1, col2 = st.columns(2)
    with col1:
        stock_shape = st.radio("ராட் வடிவம் (Stock Profile):", ["Round (வட்ட வடிவம்)", "Hexagonal (அறுகோணம்)", "Square (சதுரம்)"])
        size_mm = st.number_input("ராட் அளவு (Material Size in mm):", value=12.0, step=0.5)
    
    with col2:
        st.markdown("### 📋 பரிந்துரைக்கப்பட்ட செட்டிங்ஸ்:")
        st.info(f"• **மாடல்:** {machine_model}\n"
                f"• **காலெட் வகை:** {stock_shape} Collet ({size_mm} mm)\n"
                f"• **Guide Bush Clearance:** 0.015 mm - 0.025 mm\n"
                f"• **Gripping Pressure:** Medium-High")

# ---------------------------------------------------------
# TAB 4: உற்பத்தி திறன் (OEE)
# ---------------------------------------------------------
elif selected_tab == "📊 உற்பத்தி திறன் (OEE & Production)":
    st.subheader("📊 OEE கணக்கீடு & உற்பத்தி பகுப்பாய்வு")
    
    col1, col2 = st.columns(2)
    with col1:
        planned_time = st.number_input("திட்டமிடப்பட்ட நேரம் (Planned Time in min):", value=480)
        downtime = st.number_input("தடைபட்ட நேரம் (Downtime in min):", value=30)
        ideal_cycle_time = st.number_input("ஒரு பாகத்தின் நேரம் (Cycle Time in sec):", value=45.0)
        total_produced = st.number_input("மொத்த உற்பத்தி (Pieces):", value=500)
        good_pieces = st.number_input("சரியான பாகங்கள் (Good Pieces):", value=490)
    
    with col2:
        operating_time = planned_time - downtime
        availability = (operating_time / planned_time) * 100 if planned_time > 0 else 0
        performance = ((ideal_cycle_time * total_produced) / (operating_time * 60)) * 100 if operating_time > 0 else 0
        quality = (good_pieces / total_produced) * 100 if total_produced > 0 else 0
        oee = (availability * performance * quality) / 10000
        
        st.markdown("### 🏆 OEE முடிவுகள்:")
        st.write(f"• **Availability:** {availability:.1f}%")
        st.write(f"• **Performance:** {performance:.1f}%")
        st.write(f"• **Quality:** {quality:.1f}%")
        st.markdown(f"## 🎯 **ஒட்டுமொத்த OEE: {oee:.1f}%**")

# ---------------------------------------------------------
# TAB 5: அறிக்கை தயாரிப்பு (REPORTS)
# ---------------------------------------------------------
elif selected_tab == "📑 அறிக்கை தயாரிப்பு (Reports)":
    st.subheader("📑 ஷிப்ட் உற்பத்தி அறிக்கை (Shift Production Report)")
    
    df = pd.DataFrame({
        'Machine': ['CNC Lathe 01', 'Traub A25', 'CNC VMC 02', 'Traub A42'],
        'Target (Pcs)': [600, 800, 350, 700],
        'Actual (Pcs)': [580, 790, 340, 680],
        'Rejection (Pcs)': [5, 12, 3, 8],
        'Efficiency (%)': ['96.6%', '98.7%', '97.1%', '97.1%']
    })
    
    st.dataframe(df, use_container_width=True)
    
    st.download_button(
        label="📥 CSV அறிக்கையாகப் பதிவிறக்கு",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='shift_production_report.csv',
        mime='text/csv'
    )

# ---------------------------------------------------------
# TAB 6: AI ப்ளூபிரிண்ட் & IOT
# ---------------------------------------------------------
elif selected_tab == "🤖 AI ப்ளூபிரிண்ட் & IoT (AI & IoT)":
    st.subheader("🤖 ஏஐ ப்ளூபிரிண்ட் ஸ்கேனர் & ஐஓடி (Advanced Features)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📸 2D Blueprint Scanner")
        st.file_uploader("வரைபடத்தைப் பதிவேற்றவும் (Upload Blueprint PDF/Image):", type=['png', 'jpg', 'pdf'])
    with col2:
        st.markdown("### 🎙️ வாய்ஸ் அசிஸ்டென்ட்")
        st.button("🎙️ குரல் வழி கட்டளையைத் தொடங்கு (Start Voice)")

st.sidebar.markdown("---")
st.sidebar.caption("Megala Enterprises © 2026 | Megala CNC Mate v2.0")
