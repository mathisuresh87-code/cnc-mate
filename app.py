import streamlit as st
import math

# Page Configuration - அப்ளிகேஷனின் தலைப்பு மற்றும் வடிவமைப்பு அமைப்பு
st.set_page_config(page_title="Megala CNC Mate - Smart CNC & Production Assistant", layout="centered")

# --- 1. மொழித் தேர்வு பகுதி (Multi-Language Support) ---
# தமிழ், ஆங்கிலம் மற்றும் ஹிந்தி மொழிகளில் அப்ளிகேஷன் இயங்குவதற்கான மெனு
lang = st.selectbox("🌐 Select Language / மொழியைத் தேர்ந்தெடுக்கவும் / भाषा चुनें:", 
                    ["தமிழ் (Tamil)", "English", "हिंदी (Hindi)"])

# மொழிக்கேற்ப வார்த்தைகளை மாற்றியமைக்கும் அகராதி (Text Dictionary)
if lang == "தமிழ் (Tamil)":
    title = "⚙️ MEGALA CNC MATE - உற்பத்தி மற்றும் கால்குலேட்டர்"
    cust_label = "கஸ்டமர் / கம்பெனி பெயர் (Customer Name)"
    part_name_label = "பார்ட் பெயர் / டிராயிங் எண் (Part Name / Drawing No)"
    mat_label = "மெட்டீரியல் வகை (Material Type)"
    od_label = "வெளி விட்டம் (OD - mm)"
    id_label = "உள் விட்டம் (ID - mm)"
    len_label = "மொத்த நீளம் (Total Meters)"
    part_len_label = "ஒரு பார்ட் நீளம் (Part Length - mm)"
    kerf_label = "கட்டிங் அலவன்ஸ் / கெர்ஃப் (Kerf - mm)"
    cycle_label = "ஒரு பார்ட்டுக்கான சைக்கிள் டைம் (Seconds)"
    calc_btn = "🧮 கணக்கிடு (Calculate)"
    result_title = "📊 உற்பத்தி மற்றும் ஸ்கிராப் முடிவு (Output Summary)"
    w_label = "மொத்த மூலப்பொருள் எடை"
    p_label = "தயாராகும் மொத்த பார்ட்டுகள்"
    hr_label = "1 மணி நேர உற்பத்தி"
    shift_label = "8 மணி நேர ஷிப்ட் உற்பத்தி"
    scrap_label = "ஸ்கிராப் விவரங்கள் (Scrap Breakdown)"
    kerf_scrap = "பிளேடு சிப்ஸ் இழப்பு (Kerf Scrap)"
    end_scrap = "கஸ்டமர் எண்டு பீஸ் (End Remnant)"
elif lang == "हिंदी (Hindi)":
    title = "⚙️ CNC MATE - स्मार्ट सीएनसी और प्रोडक्शन असिस्टेंट"
    cust_label = "कस्टमर / कंपनी का नाम (Customer Name)"
    part_name_label = "पार्ट का नाम / ड्राइंग नंबर (Part Name)"
    mat_label = "मटेरियल का प्रकार (Material Type)"
    od_label = "बाहरी व्यास OD (mm)"
    id_label = "भीतरी व्यास ID (mm)"
    len_label = "कुल लंबाई (Total Meters)"
    part_len_label = "एक पार्ट की लंबाई (Part Length - mm)"
    kerf_label = "कटिंग एलाउंस / केर्फ (Kerf - mm)"
    cycle_label = "साइकिल टाइम प्रति पार्ट (Seconds)"
    calc_btn = "🧮 गणना करें (Calculate)"
    result_title = "📊 उत्पादन और स्क्रैप रिपोर्ट (Output Summary)"
    w_label = "कुल कच्चे माल का वजन"
    p_label = "कुल तैयार पार्ट्स"
    hr_label = "प्रति घंटे उत्पादन (Pcs/Hr)"
    shift_label = "8 घंटे की शिफ्ट उत्पादन"
    scrap_label = "स्क्रैप विवरण (Scrap Breakdown)"
    kerf_scrap = "ब्लेड कर्फ़ स्क्रैप (Kerf Scrap)"
    end_scrap = "कस्टमर एंड रिमन्ट स्क्रैप"
else:
    title = "⚙️ CNC MATE - Smart CNC & Production Assistant"
    cust_label = "Customer / Company Name"
    part_name_label = "Part Name / Drawing No"
    mat_label = "Material Type"
    od_label = "Outer Diameter OD (mm)"
    id_label = "Inner Diameter ID (mm)"
    len_label = "Total Purchase Length (Meters)"
    part_len_label = "Single Part Length (mm)"
    kerf_label = "Cutting Allowance / Kerf (mm)"
    cycle_label = "Cycle Time per Part (Seconds)"
    calc_btn = "🧮 Calculate"
    result_title = "📊 Production & Scrap Output Summary"
    w_label = "Total Raw Material Weight"
    p_label = "Total Output Parts"
    hr_label = "Estimated Parts / Hour"
    shift_label = "8-Hour Shift Output"
    scrap_label = "Scrap Breakdown"
    kerf_scrap = "Blade Kerf Scrap"
    end_scrap = "Customer End Remnant Scrap"

st.title(title)
st.markdown("---")

# --- 2. டைனமிக் உள்ளீடுகள் (Dynamic Inputs for Customer & Part) ---
# எந்தக் கஸ்டமராக இருந்தாலும் சரி, அவர்களின் பெயரையும் பார்ட் பெயரையும் நாமே டைப் செய்யக்கூடிய பாக்ஸ்கள்
customer_name = st.text_input(cust_label, value="ABC Engineering")
part_name = st.text_input(part_name_label, value="Stepped Pin")

# --- 3. மெட்டீரியல் மற்றும் அளவீட்டு உள்ளீடு (Material & Dimensions) ---
material_type = st.selectbox(mat_label, ["MS Tube / Hollow Bar", "Solid Round Rod", "Hexagon Rod"])

col1, col2 = st.columns(2)
with col1:
    dim1 = st.number_input(od_label, value=80.0)
with col2:
    if "Tube" in material_type:
        dim2 = st.number_input(id_label, value=50.0)
    else:
        dim2 = 0.0

total_meters = st.number_input(len_label, value=100.0)
part_len = st.number_input(part_len_label, value=150.0)
kerf_allowance = st.number_input(kerf_label, value=3.0)
cycle_time_sec = st.number_input(cycle_label, value=80.0)

density = 0.00785  # எஃகுக்கான அடர்த்தி (Steel density g/mm³)

# --- 4. கணக்கீட்டு இன்ஜின் பகுதி (Calculation Logic) ---
if st.button(calc_btn):
    # மெட்டீரியல் வடிவத்திற்கேற்ப குறுக்கு வெட்டுப் பரப்பு (Cross-Section Area) கணக்கீடு
    if "Tube" in material_type:
        area = (math.pi / 4) * ((dim1 ** 2) - (dim2 ** 2))
    elif "Solid" in material_type:
        area = (math.pi / 4) * (dim1 ** 2)
    else:
        area = (math.sqrt(3) / 6.0) * (dim1 ** 2)

    total_len_mm = total_meters * 1000.0
    bar_len_mm = 6000.0  # நிலையான 6 மீட்டர் பார் நீளம்
    total_bars = max(1, int(total_len_mm // bar_len_mm))
    
    weight_per_m = area * 1000 * density / 1000.0
    total_raw_weight = total_meters * weight_per_m

    single_part_total = part_len + kerf_allowance
    pieces_per_bar = int(bar_len_mm // single_part_total) if single_part_total > 0 else 1
    total_pieces = pieces_per_bar * total_bars
    
    used_len_per_bar = pieces_per_bar * single_part_total
    end_scrap_mm = bar_len_mm - used_len_per_bar
    total_end_scrap_mm = end_scrap_mm * total_bars
    total_kerf_mm = total_pieces * kerf_allowance

    end_scrap_wt = area * total_end_scrap_mm * density / 1000.0
    kerf_scrap_wt = area * total_kerf_mm * density / 1000.0

    parts_per_hour = 3600 / cycle_time_sec if cycle_time_sec > 0 else 0
    shift_output_8hrs = parts_per_hour * 8

    # --- 5. ரிப்போர்ட் வெளியீடு பகுதி (Display Results) ---
    st.success(f"{result_title} - {customer_name} ({part_name})")
    
    st.metric(label=w_label, value=f"{round(total_raw_weight, 2)} KG")
    st.metric(label=p_label, value=f"{total_pieces:,} Pcs")
    st.metric(label=hr_label, value=f"{round(parts_per_hour)} Pcs/Hr")
    st.metric(label=shift_label, value=f"{round(shift_output_8hrs)} Pcs")
    
    st.markdown(f"### ♻️ {scrap_label}")
    st.write(f"• **{kerf_scrap}:** {round(kerf_scrap_wt, 2)} KG")
    st.write(f"• **{end_scrap}:** {round(end_scrap_wt, 2)} KG")
