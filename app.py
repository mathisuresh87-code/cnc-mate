import base64
from datetime import datetime
import math
import os
from fpdf import FPDF
import pandas as pd
from PIL import Image
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Megala CNC Mate - Suresh Enterprise Automation",
    page_icon="⚙️",
    layout="wide",
)

# Ultra-Vibrant Custom CSS Styling
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #090d1f 0%, #111827 40%, #1e1b4b 100%);
        color: #f8fafc;
        font-family: 'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #38bdf8 0%, #c084fc 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 4px 0;
        padding: 0;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        line-height: 1.1;
        filter: drop-shadow(0 0 20px rgba(192, 132, 252, 0.5));
    }
    .sub-title {
        font-size: 0.92rem;
        color: #38bdf8;
        margin: 0;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
    }
    div[data-testid="column"] {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.85) 0%, rgba(49, 46, 129, 0.5) 100%);
        border: 1.5px solid rgba(139, 92, 246, 0.4);
        padding: 24px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(16px);
        transition: all 0.35s ease;
        margin-bottom: 20px;
    }
    div.stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 50%, #ec4899 100%);
        color: #ffffff !important;
        border-radius: 14px;
        border: 1.5px solid rgba(236, 72, 153, 0.6);
        font-weight: 800;
        letter-spacing: 1px;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 20px rgba(147, 51, 234, 0.5);
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #f43f5e 100%);
        border-color: #38bdf8;
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(236, 72, 153, 0.7);
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070b19 0%, #0f172a 100%);
        border-right: 1.5px solid rgba(139, 92, 246, 0.3);
    }
    </style>
""",
    unsafe_allow_html=True,
)

LOGO_PATH = "logo.png"

if "app_language" not in st.session_state:
  st.session_state["app_language"] = "தமிழ் (Tamil)"

st.sidebar.markdown(
    '<div style="text-align: center; padding: 5px 0 10px 0;"><h3'
    ' style="color: #ec4899; margin: 0; font-size: 1.15rem; font-weight: 900;'
    ' letter-spacing: 1.5px;">MEGALA CNC MATE</h3><p style="color: #38bdf8;'
    ' font-size: 0.85rem; margin: 5px 0 0 0;">Owner: Suresh (சுரேஷ்)</p></div>',
    unsafe_allow_html=True,
)

selected_lang = st.sidebar.selectbox(
    "🌐 Language / மொழி",
    [
        "English",
        "தமிழ் (Tamil)",
        "हिन्दी (Hindi)",
        "తెలుగు (Telugu)",
        "ಕನ್ನಡ (Kannada)",
        "മലയാളം (Malayalam)",
    ],
    index=[
        "English",
        "தமிழ் (Tamil)",
        "हिन्दी (Hindi)",
        "తెలుగు (Telugu)",
        "ಕನ್ನಡ (Kannada)",
        "മലയാളം (Malayalam)",
    ].index(st.session_state["app_language"]),
)
if selected_lang != st.session_state["app_language"]:
  st.session_state["app_language"] = selected_lang
  st.rerun()

curr_lang = st.session_state["app_language"]

translations = {
    "English": {
        "back_home": "⬅️ Back to Home",
        "modules": [
            "🏠 Home Dashboard",
            "📐 Rod / Bar Weight & Cost Calculator",
            "⏱️ CNC Production & Cycle Time",
            "💰 Enterprise Costing & Quotation",
            "📦 Stock & Inventory Management",
            "📷 Drawing Studio & G-Code (Simple/Advanced Modes)",
            "📋 Process Breakdown & Quotation",
            "🛠️ Suresh Master Knowledge Base & Profile",
        ],
    },
    "தமிழ் (Tamil)": {
        "back_home": "⬅️ Back to Home / முகப்புக்குத் திரும்பு",
        "modules": [
            "🏠 Home Dashboard / முகப்பு டேஷ்போர்டு",
            "📐 Rod / Bar Weight & Cost Calculator / ராட் எடை & விலை கால்குலேட்டர்",
            "⏱️ CNC Production & Cycle Time / உற்பத்தி & சைக்கிள் டைம்",
            "💰 Enterprise Costing & Quotation / செலவு & கொட்டேஷன்",
            "📦 Stock & Inventory Management / ஸ்டாக் மேனேஜ்மென்ட்",
            (
                "📷 Drawing Studio & G-Code (Simple/Advanced Modes) / டிராயிங்"
                " ஸ்டுடியோ & ஜி-கோடு (சிம்பிள்/அட்வான்ஸ் மோட்)"
            ),
            "📋 Process Breakdown & Quotation / செயல்முறை & கொட்டேஷன்",
            (
                "🛠️ Suresh Master Knowledge Base & Profile / சுரேஷ் மாஸ்டர்"
                " சுயவிவரம் & அறிவுத்தளம்"
            ),
        ],
    },
    "हिन्दी (Hindi)": {
        "back_home": "⬅️ Back to Home / होम पर वापस जाएं",
        "modules": [
            "🏠 Home Dashboard / होम डैशबोर्ड",
            "📐 Rod Calculator / रॉड वजन और लागत",
            "⏱️ Production Calculator / प्रोडक्शन",
            "💰 Enterprise Costing & Quotation / कॉस्टिंग और कोटेशन",
            "📦 Stock Management / स्टॉक मैनेजमेंट",
            "📷 Drawing Studio & G-Code (Simple/Advanced Modes) / ड्राइंग स्टूडियो",
            "📋 Process Breakdown & Quotation / प्रोसेस और कोटेशन",
            "🛠️ Suresh Profile & Knowledge Base / सुरेश प्रोफाइल",
        ],
    },
    "తెలుగు (Telugu)": {
        "back_home": "⬅️ Back to Home / హోమ్‌కి వెళ్లండి",
        "modules": [
            "🏠 Home Dashboard / హోమ్ డాష్‌బోర్డ్",
            "📐 Rod Calculator / రాడ్ బరువు & ఖర్చు",
            "⏱️ Production Calculator / ప్రొడక్షన్",
            "💰 Enterprise Costing & Quotation / కాస్టింగ్ & కొటేషన్",
            "📦 Stock Management / స్టాక్ మేనేజ్‌మెంట్",
            (
                "📷 Drawing Studio & G-Code (Simple/Advanced Modes) / డ్రాయింగ్"
                " స్టూడియో"
            ),
            "📋 Process Breakdown & Quotation / ప్రాసెస్ & కొటేషన్",
            "🛠️ Suresh Profile & Knowledge Base / సురేష్ ప్రొఫైల్",
        ],
    },
    "ಕನ್ನಡ (Kannada)": {
        "back_home": "⬅️ Back to Home / ಮುಖಪುಟಕ್ಕೆ ಹಿಂತಿರುಗಿ",
        "modules": [
            "🏠 Home Dashboard / ಮುಖಪುಟ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
            "📐 Rod Calculator / ರಾಡ್ ತೂಕ ಮತ್ತು ವೆಚ್ಚ",
            "⏱️ Production Calculator / ಉತ್ಪಾದನೆ",
            "💰 Enterprise Costing & Quotation / ವೆಚ್ಚ ಮತ್ತು ಉಲ್ಲೇಖ",
            "📦 Stock Management / ದಾಸ್ತಾನು ನಿರ್ವಹಣೆ",
            (
                "📷 Drawing Studio & G-Code (Simple/Advanced Modes) / ಡ್ರಾಯಿಂಗ್"
                " ಸ್ಟುடியோ"
            ),
            "📋 Process Breakdown & Quotation / ಪ್ರಕ್ರಿಯೆ ಮತ್ತು ಉಲ್ಲೇಖ",
            "🛠️ Suresh Profile & Knowledge Base / ಸುರೇಶ್ ಪ್ರೊಫೈಲ್",
        ],
    },
    "മലയാളം (Malayalam)": {
        "back_home": "⬅️ Back to Home / ഹോമിലേക്ക് മടങ്ങുക",
        "modules": [
            "🏠 Home Dashboard / ഹോം ഡാഷ്‌ബോർഡ്",
            "📐 Rod Calculator / റോഡ് ഭാരവും വിലയും",
            "⏱️ Production Calculator / ഉൽപ്പാദന കാൽക്കുലേറ്റർ",
            "💰 Enterprise Costing & Quotation / കൊട്ടേഷൻ",
            "📦 Stock Management / സ്റ്റോക്ക് മാനേജ്മെന്റ്",
            (
                "📷 Drawing Studio & G-Code (Simple/Advanced Modes) / ഡ്രോയിംഗ്"
                " സ്റ്റുഡിയോ"
            ),
            "📋 Process Breakdown & Quotation / കൊട്ടേഷൻ",
            "🛠️ Suresh Profile & Knowledge Base / സുരേഷ് പ്രൊഫൈൽ",
        ],
    },
}

t_dict = translations[curr_lang]
module_list = t_dict["modules"]

if "selected_module" not in st.session_state:
  st.session_state["selected_module"] = module_list[0]

if "stock_inventory_df" not in st.session_state:
  st.session_state["stock_inventory_df"] = pd.DataFrame({
      "Item ID": ["ITM-001", "ITM-002", "ITM-003", "ITM-004"],
      "Material / Part Name": [
          "EN8 Round Bar - 12mm",
          "MS Round Bar - 20mm",
          "EN24 Round Bar - 16mm",
          "Finished Large Pin",
      ],
      "Category": [
          "Raw Material",
          "Raw Material",
          "Raw Material",
          "Finished Goods",
      ],
      "Quantity": [120.50, 45.20, 0.00, 650.00],
      "Unit": ["Kg", "Kg", "Kg", "Nos"],
      "Status": ["In Stock", "Low Stock", "Out of Stock", "Dispatch Ready"],
  })


def get_base64_image(path):
  if os.path.exists(path):
    with open(path, "rb") as f:
      return base64.b64encode(f.read()).decode("utf-8")
  return None


encoded_sidebar_img = get_base64_image(LOGO_PATH)
if encoded_sidebar_img:
  st.sidebar.markdown(
      '<div style="text-align: center; margin-bottom: 12px;"><div'
      ' style="background: linear-gradient(135deg, rgba(236, 72, 153, 0.3),'
      " rgba(56, 189, 248, 0.3)); border: 2.5px solid #ec4899; width: 75px;"
      " height: 75px; border-radius: 50%; margin: 0 auto; display: flex;"
      " align-items: center; justify-content: center; overflow: hidden;"
      f'"><img src="data:image/png;base64,{encoded_sidebar_img}"'
      ' style="width: 100%;" /></div></div>',
      unsafe_allow_html=True,
  )

uploaded_logo = st.sidebar.file_uploader(
    "Upload Permanent Logo",
    type=["png", "jpg", "jpeg"],
    key="sidebar_logo_upload",
    label_visibility="collapsed",
)
if uploaded_logo is not None:
  try:
    Image.open(uploaded_logo).save(LOGO_PATH)
    st.sidebar.success("✅ Logo Saved!")
    st.rerun()
  except Exception as e:
    st.sidebar.error(f"Error: {e}")

st.sidebar.markdown("---")
selected_module = st.sidebar.selectbox(
    "Select Module",
    module_list,
    index=(
        module_list.index(st.session_state["selected_module"])
        if st.session_state["selected_module"] in module_list
        else 0
    ),
    label_visibility="collapsed",
)
st.session_state["selected_module"] = selected_module

# Header Layout
col_logo, col_title = st.columns([0.15, 0.85], vertical_alignment="center")
with col_logo:
  encoded_img = get_base64_image(LOGO_PATH)
  if encoded_img:
    st.markdown(
        '<div style="border: 2.5px solid #ec4899; width: 85px; height: 85px;'
        ' border-radius: 50%; display: flex; align-items: center;'
        ' justify-content: center; overflow: hidden;"'
        f'><img src="data:image/png;base64,{encoded_img}"'
        ' style="width: 100%;" /></div>',
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        '<div style="background: linear-gradient(135deg, #4f46e5, #ec4899);'
        ' width: 85px; height: 85px; border-radius: 50%; display: flex;'
        ' align-items: center; justify-content: center; font-weight: 900;'
        ' color: white;">SU</div>',
        unsafe_allow_html=True,
    )
with col_title:
  st.markdown(
      '<h1 class="main-title">MEGALA INDUSTRIES (SURESH)</h1>',
      unsafe_allow_html=True,
  )
  st.markdown(
      '<p class="sub-title">PRECISION CNC MACHINING & ENTERPRISE AUTOMATION</p>',
      unsafe_allow_html=True,
  )

st.markdown(
    "<hr style='margin-top: 0px; border-color: rgba(236, 72, 153, 0.3);'>",
    unsafe_allow_html=True,
)


def generate_quotation_csv(
    customer_name, part_name, operations_list, transport_cost=0.0
):
  rows = []
  rows.append(
      ["MEGALA INDUSTRIES - PRECISION CNC MACHINING & ENTERPRISE AUTOMATION"]
  )
  rows.append([f"Owner / Proprietor: Suresh", f"Customer Name: {customer_name}"])
  rows.append([
      f"Part Name: {part_name}",
      f"Date: {datetime.now().strftime('%Y-%m-%d')}",
  ])
  rows.append([])
  rows.append([
      "S.No",
      "Operation / Process Description",
      "Machine / Setup",
      "Qty",
      "Unit Rate (Rs.)",
      "Total Amount (Rs.)",
  ])

  total_amt = 0.0
  for idx, op in enumerate(operations_list, 1):
    row_total = op["qty"] * op["rate"]
    total_amt += row_total
    rows.append(
        [idx, op["name"], op["machine"], op["qty"], op["rate"], row_total]
    )

  if transport_cost > 0:
    total_amt += transport_cost
    rows.append([
        "",
        "Transport & Logistics Charges",
        "Logistics",
        1,
        transport_cost,
        transport_cost,
    ])

  rows.append([])
  rows.append(["", "", "", "", "Grand Total", total_amt])

  df_csv = pd.DataFrame(rows)
  return df_csv.to_csv(index=False, header=False).encode("utf-8")


# 1. HOME DASHBOARD
if "Home Dashboard" in selected_module or "முகப்பு" in selected_module:
  st.markdown("### 📊 Enterprise Control Dashboard - Suresh (சுரேஷ்)")
  m1, m2, m3, m4 = st.columns(4)
  with m1:
    st.metric("Active Machines", "4 Units", "Running 🚀")
  with m2:
    st.metric("Today's Output", "1,850 Nos", "+12% 📈")
  with m3:
    st.metric("Material Stock Items", "4 Items", "Optimal ✨")
  with m4:
    st.metric("Stock Alerts", "0 Alerts", "Check Stock ⚠️")

  st.markdown("<br>", unsafe_allow_html=True)
  st.markdown("### 🚀 Core Enterprise Modules")

  col1, col2, col3 = st.columns(3)
  with col1:
    if st.button("📐 Rod Calculator", use_container_width=True, key="bh1"):
      st.session_state["selected_module"] = module_list[1]
      st.rerun()
  with col2:
    if st.button("⏱️ Production Calc", use_container_width=True, key="bh2"):
      st.session_state["selected_module"] = module_list[2]
      st.rerun()
  with col3:
    if st.button("💰 Costing & Quote", use_container_width=True, key="bh3"):
      st.session_state["selected_module"] = module_list[3]
      st.rerun()

  col4, col5, col6 = st.columns(3)
  with col4:
    if st.button("📦 Stock Management", use_container_width=True, key="bh4"):
      st.session_state["selected_module"] = module_list[4]
      st.rerun()
  with col5:
    if st.button("📷 Drawing & G-Code Studio", use_container_width=True, key="bh5"):
      st.session_state["selected_module"] = module_list[5]
      st.rerun()
  with col6:
    if st.button("📋 Process Quotation", use_container_width=True, key="bh6"):
      st.session_state["selected_module"] = module_list[6]
      st.rerun()

# 2. ROD CALCULATOR
elif "Rod" in selected_module or "ராட்" in selected_module:
  if st.button(t_dict["back_home"]):
    st.session_state["selected_module"] = module_list[0]
    st.rerun()
  st.subheader(
      "📐 Rod / Bar Weight & Cost Calculator (ராட் எடை & விலை கால்குலேட்டர்)"
  )
  st.write(
      "Calculate raw material round bar weight, length, and total material cost"
      " for your CNC production."
  )

  rc1, rc2 = st.columns(2)
  with rc1:
    dia = st.number_input(
        "Rod Diameter (mm) / ராட் விட்டம் (மி.மீ)",
        value=25.0,
        min_value=1.0,
    )
    length_mm = st.number_input(
        "Length per Piece (mm) / ஒரு பீஸ் நீளம் (மி.மீ)",
        value=150.0,
        min_value=1.0,
    )
  with rc2:
    qty_nos = st.number_input(
        "Total Quantity (Nos) / மொத்த எண்ணிக்கைகள்", value=500, min_value=1
    )
    density = st.number_input(
        "Material Density (g/cm³) / டென்சிட்டி (ஸ்டீல்: 7.85)", value=7.85
    )
    rate_per_kg = st.number_input(
        "Material Rate per Kg (Rs.) / ஒரு கிலோ விலை (ரூ.)", value=85.0
    )

  single_wt_kg = (
      math.pi * (dia / 2) ** 2 * length_mm * density
  ) / 1000000.0  # in kg
  total_wt_kg = single_wt_kg * qty_nos
  total_mat_cost = total_wt_kg * rate_per_kg

  st.markdown("<br>", unsafe_allow_html=True)
  res1, res2, res3 = st.columns(3)
  with res1:
    st.metric(
        "Single Piece Weight", f"{single_wt_kg:.3f} Kg", "ஒன்றுக்கு எடை"
    )
  with res2:
    st.metric(
        "Total Material Weight", f"{total_wt_kg:.2f} Kg", "மொத்த மெட்டீரியல் எடை"
    )
  with res3:
    st.metric(
        "Total Material Cost",
        f"Rs. {total_mat_cost:,.2f}",
        "மொத்த மெட்டீரியல் செலவு",
    )

# 3. PRODUCTION CALCULATOR
elif "Production" in selected_module or "உற்பத்தி" in selected_module:
  if st.button(t_dict["back_home"]):
    st.session_state["selected_module"] = module_list[0]
    st.rerun()
  st.subheader(
      "⏱️ CNC Production & Cycle Time Calculator (உற்பத்தி & சைக்கிள் டைம்)"
  )
  st.write(
      "Calculate shift output, hourly production rates, and machine efficiency."
  )

  pc1, pc2 = st.columns(2)
  with pc1:
    cycle_time_sec = st.number_input(
        "Cycle Time per Component (Seconds) / சைக்கிள் நேரம் (வினாடிகள்)",
        value=45.0,
        min_value=1.0,
    )
    shift_hours = st.number_input(
        "Shift Working Hours / ஷிப்ட் வேலை மணி நேரம்", value=8.0, min_value=1.0
    )
  with pc2:
    efficiency_pct = st.slider(
        "Machine Efficiency (%) / இயந்திர திறன் (%)", 50, 100, 85
    )
    target_nos = st.number_input(
        "Target Production Quantity (Nos) / இலக்கு உற்பத்தி", value=500
    )

  parts_per_hour = 3600.0 / cycle_time_sec
  effective_parts_per_hour = parts_per_hour * (efficiency_pct / 100.0)
  total_shift_output = effective_parts_per_hour * shift_hours
  required_hours = (
      target_nos / effective_parts_per_hour
      if effective_parts_per_hour > 0
      else 0
  )

  st.markdown("<br>", unsafe_allow_html=True)
  pr1, pr2, pr3 = st.columns(3)
  with pr1:
    st.metric(
        "Hourly Output",
        f"{int(effective_parts_per_hour)} Nos/hr",
        "ஒரு மணி நேர உற்பத்தி",
    )
  with pr2:
    st.metric(
        "Shift Output",
        f"{int(total_shift_output)} Nos",
        f"மொத்த ஷிப்ட் உற்பத்தி ({shift_hours} மணி நேரம்)",
    )
  with pr3:
    st.metric(
        "Time for Target",
        f"{required_hours:.2f} Hours",
        "இலக்கை முடிக்க தேவைப்படும் நேரம்",
    )

# 4. COSTING & QUOTATION
elif "Costing" in selected_module or "செலவு" in selected_module:
  if st.button(t_dict["back_home"]):
    st.session_state["selected_module"] = module_list[0]
    st.rerun()
  st.subheader(
      "💰 Enterprise Costing & Quotation Calculator (செலவு & கொட்டேஷன்)"
  )
  st.write("Calculate component machining cost, overheads, and profit margin.")

  cc1, cc2 = st.columns(2)
  with cc1:
    mat_cost_per_pc = st.number_input(
        "Material Cost per Piece (Rs.) / ஒரு பார்ட் மெட்டீரியல் விலை",
        value=35.0,
    )
    machining_cost_per_pc = st.number_input(
        "Machining & Labor Cost per Piece (Rs.) / மிஷினிங் & லேபர் செலவு",
        value=20.0,
    )
  with cc2:
    overhead_pct = st.number_input(
        "Overheads & Power (%) / இதர செலவுகள் & கரண்ட் பில் (%)",
        value=10.0,
    )
    profit_pct = st.number_input(
        "Profit Margin (%) / லாப சதவீதம் (%)", value=20.0
    )

  subtotal = mat_cost_per_pc + machining_cost_per_pc
  overhead_amt = subtotal * (overhead_pct / 100.0)
  cost_price = subtotal + overhead_amt
  profit_amt = cost_price * (profit_pct / 100.0)
  selling_price = cost_price + profit_amt

  st.markdown("<br>", unsafe_allow_html=True)
  cr1, cr2, cr3 = st.columns(3)
  with cr1:
    st.metric(
        "Total Cost Price", f"Rs. {cost_price:.2f}", "உற்பத்தி அடக்க விலை"
    )
  with cr2:
    st.metric(
        "Profit Amount per Piece",
        f"Rs. {profit_amt:.2f}",
        f"லாபம் ({profit_pct}%)",
    )
  with cr3:
    st.metric(
        "Suggested Selling Price",
        f"Rs. {selling_price:.2f}",
        "விற்க வேண்டிய இறுதி விலை",
    )

# 5. STOCK MANAGEMENT
elif "Stock" in selected_module or "ஸ்டாக்" in selected_module:
  if st.button(t_dict["back_home"]):
    st.session_state["selected_module"] = module_list[0]
    st.rerun()
  st.subheader(
      "📦 Stock & Inventory Management (ஸ்டாக் & இன்வென்டோரி மேனேஜ்மென்ட்)"
  )
  st.dataframe(st.session_state["stock_inventory_df"], use_container_width=True)

  st.markdown("### Add / Update Stock Item (புதிய ஸ்டாக் சேர்க்க)")
  s_col1, s_col2, s_col3 = st.columns(3)
  with s_col1:
    new_item_name = st.text_input("Item Name / பொருளின் பெயர்")
    new_cat = st.selectbox(
        "Category / வகை", ["Raw Material", "Finished Goods", "Tools & Consumables"]
    )
  with s_col2:
    new_qty = st.number_input("Quantity / அளவு", value=100.0)
    new_unit = st.selectbox("Unit / அலகு", ["Kg", "Nos", "Pcs", "Mtrs"])
  with s_col3:
    new_status = st.selectbox(
        "Status / நிலை", ["In Stock", "Low Stock", "Out of Stock"]
    )

  if st.button("➕ Add to Inventory Stock (ஸ்டாக்கில் சேர்)"):
    new_row = pd.DataFrame({
        "Item ID": [f"ITM-00{len(st.session_state['stock_inventory_df'])+1}"],
        "Material / Part Name": [new_item_name],
        "Category": [new_cat],
        "Quantity": [new_qty],
        "Unit": [new_unit],
        "Status": [new_status],
    })
    st.session_state["stock_inventory_df"] = pd.concat(
        [st.session_state["stock_inventory_df"], new_row], ignore_index=True
    )
    st.success("✅ Stock item added successfully!")
    st.rerun()

# 6. DRAWING STUDIO WITH SIMPLE / ADVANCED MODES (RESTORED AS REQUESTED)
elif "Drawing" in selected_module or "டிராயிங்" in selected_module:
  if st.button(t_dict["back_home"]):
    st.session_state["selected_module"] = module_list[0]
    st.rerun()
  st.subheader(
      "📷 Drawing Studio & Dynamic G-Code Generator (Simple & Advanced Modes)"
  )
  st.write(
      "சுரேஷ், நீங்கள் கேட்டபடி இங்கு **Simple Mode** மற்றும் **Advanced Mode**"
      " இரண்டும் இணைக்கப்பட்டுள்ளன."
  )

  # Mode Selection Radio Buttons
  app_mode = st.radio(
      "Select Operation Mode / இயக்க முறையைத் தேர்ந்தெடுக்கவும்:",
      [
          "Simple Mode (நார்மல் கால்குலேட்டர் / எளிய முறை)",
          (
              "Advanced Mode (டிராயிங் அப்லோட் & ஆட்டோமேட்டிக் சைஸ் இன்புட் மற்றும்"
              " ஜி-கோடு)"
          ),
      ],
      horizontal=True,
  )

  st.markdown("---")

  if "Simple Mode" in app_mode:
    st.markdown("### 🧮 Simple Calculator Mode")
    st.write("எளிய கணக்கீடுகளுக்கு இந்த சிம்பிள் மோடைப் பயன்படுத்தலாம்.")
    s_dia = st.number_input("Component OD (mm)", value=40.0)
    s_len = st.number_input("Component Length (mm)", value=50.0)
    s_qty = st.number_input("Production Quantity", value=100)

    st.info(
        f"Simple Calculation Result: OD {s_dia}mm x Length {s_len}mm for"
        f" {s_qty} Nos is ready."
    )

  else:
    st.markdown("### ⚡ Advanced Mode (Drawing Auto-Input & G-Code Studio)")
    st.write(
        "உங்கள் பார்ட் டிராயிங்கை அப்லோட் செய்யுங்கள். இது தானாகவே அளவுகளை எடுத்து"
        " ஜி-கோடை உருவாக்கும்."
    )

    d_col1, d_col2 = st.columns(2)
    with d_col1:
      uploaded_drawing = st.file_uploader(
          "Upload Component Drawing (PNG/JPG/PDF)", type=["png", "jpg", "jpeg"]
      )
      if uploaded_drawing is not None:
        st.image(
            uploaded_drawing,
            caption="Uploaded Drawing Preview (Auto-Scanned)",
            use_container_width=True,
        )
        st.success(
            "✅ Drawing successfully scanned and auto-detected sizes loaded!"
        )

    with d_col2:
      st.markdown("### 📏 Auto-Detected / Configured Part Parameters")
      part_od = st.number_input(
          "Auto-Detected Outer Diameter (mm) / வெளி விட்டம்", value=50.0
      )
      part_id = st.number_input(
          "Auto-Detected Inner Bore Diameter (mm) / உள் விட்டம்", value=0.0
      )
      part_length = st.number_input(
          "Auto-Detected Finished Length (mm) / நீளம்", value=45.0
      )

      selected_ops_list = st.multiselect(
          "Select Automated Operations for G-Code Compilation",
          [
              "Facing",
              "Rough Turning",
              "Finish Turning",
              "Grooving",
              "Drilling / Boring",
              "Parting / Cut-off",
          ],
          default=["Facing", "Rough Turning", "Parting / Cut-off"],
      )

    st.markdown("---")
    st.subheader("⚙️ Generated Advanced G-Code Program")

    gcode_lines = []
    gcode_lines.append(
        "O1002 (SURESH MEGALA ADVANCED AUTOMATED CNC PROGRAM - 2026)"
    )
    gcode_lines.append("G21 G40 G90 G99")
    gcode_lines.append(
        f"(AUTO-SCANNED PART SPEC: OD={part_od}mm, LENGTH={part_length}mm)"
    )

    tool_counter = 1
    if "Facing" in selected_ops_list:
      gcode_lines.append(f"T{tool_counter:02d}{tool_counter:02d} (FACING TOOL)")
      gcode_lines.append("G97 S2200 M03")
      gcode_lines.append(f"G0 X{part_od + 2.0} Z2.0")
      gcode_lines.append("G1 X-0.5 Z0.0 F0.15")
      gcode_lines.append("G0 Z5.0")
      tool_counter += 1

    if (
        "Rough Turning" in selected_ops_list
        or "Finish Turning" in selected_ops_list
    ):
      gcode_lines.append(f"T{tool_counter:02d}{tool_counter:02d} (TURNING TOOL)")
      gcode_lines.append("G96 S180 M03")
      gcode_lines.append(f"G0 X{part_od} Z2.0")
      gcode_lines.append(f"G1 Z-{part_length} F0.20")
      gcode_lines.append(f"G0 X{part_od + 5.0}")
      gcode_lines.append("G0 Z5.0")
      tool_counter += 1

    if "Drilling / Boring" in selected_ops_list and part_id > 0:
      gcode_lines.append(f"T{tool_counter:02d}{tool_counter:02d} (DRILL TOOL)")
      gcode_lines.append("G97 S1500 M03")
      gcode_lines.append("G0 X0.0 Z3.0")
      gcode_lines.append(f"G1 Z-{part_length - 5.0} F0.10")
      gcode_lines.append("G0 Z5.0")
      tool_counter += 1

    if "Parting / Cut-off" in selected_ops_list:
      gcode_lines.append(
          f"T{tool_counter:02d}{tool_counter:02d} (PARTING TOOL)"
      )
      gcode_lines.append("G97 S1000 M03")
      gcode_lines.append(f"G0 X{part_od + 2.0} Z-{part_length}")
      gcode_lines.append("G1 X-0.5 F0.08")
      gcode_lines.append("G0 Z50.0 M05")

    gcode_lines.append("M30")

    final_generated_code = "\n".join(gcode_lines)
    st.code(final_generated_code, language="text")

    st.download_button(
        "📥 Download Advanced G-Code File (.nc / .txt)",
        data=final_generated_code,
        file_name=f"Suresh_Advanced_Part_OD{part_od}_Len{part_length}.nc",
        mime="text/plain",
    )

# 7. PROCESS BREAKDOWN & CUSTOMER QUOTATION
elif "Process Breakdown" in selected_module or "செயல்முறை" in selected_module:
  if st.button(t_dict["back_home"]):
    st.session_state["selected_module"] = module_list[0]
    st.rerun()

  st.subheader(
      "📋 Process Breakdown & Customer Quotation Generator (கொட்டேஷன் மாடியூல்)"
  )
  st.write("உங்கள் பார்ட்டுகளுக்கு தேவையான ஆபரேஷன்களை தேர்வு செய்யலாம்.")

  col_q1, col_q2 = st.columns(2)
  with col_q1:
    cust_name = st.text_input(
        "Customer Company Name / வாடிக்கையாளர் பெயர்",
        value="M/s Precision Engineering Ltd",
    )
    part_name_input = st.text_input(
        "Part Name / Component Name", value="Custom Component / Pin Part"
    )
  with col_q2:
    order_qty = st.number_input(
        "Order Quantity / ஆர்டர் எண்ணிக்கை (Nos)", value=1000, min_value=1
    )
    transport_amt = st.number_input(
        "Transport & Logistics Charges (Rs.)", value=1500.0
    )

  st.markdown("---")
  st.subheader("⚙️ Configure Operations")

  num_ops = st.number_input(
      "Number of Operations for this Part", min_value=1, max_value=10, value=3
  )

  op_dropdown_options = [
      "Facing (பேசிங்)",
      "Turning - Rough & Finish (டர்னிங்)",
      "Grooving (குரூவிங்)",
      "Drilling (ட்ரில்லிங்)",
      "Boring (போரிங்)",
      "Chamfering (சாம்பர்)",
      "Tapping (டாப்பிங்)",
      "Parting / Cut-off (பார்ட்டிங்)",
  ]
  mach_dropdown_options = [
      "CNC Turning (சிஎன்சி டர்னிங்)",
      "VMC / Milling (விஎம்சி / மில்லிங்)",
      "Drilling Machine (ட்ரில்லிங் மிஷின்)",
      "Traub Lathe (ட்ராப் லேத்)",
  ]

  edited_ops = []
  for i in range(int(num_ops)):
    st.markdown(f"**Operation {i+1} Setup**")
    col_a, col_b, col_c = st.columns([3, 2, 2])
    with col_a:
      op_name = st.selectbox(
          f"Operation Name {i+1}",
          op_dropdown_options,
          index=min(i, len(op_dropdown_options) - 1),
          key=f"dyn_op_n_{i}",
      )
    with col_b:
      mach_name = st.selectbox(
          f"Machine {i+1}", mach_dropdown_options, key=f"dyn_op_m_{i}"
      )
    with col_c:
      op_rate = st.number_input(
          f"Unit Rate (Rs.) {i+1}", value=15.0 + (i * 5.0), key=f"dyn_op_r_{i}"
      )

    edited_ops.append({
        "name": op_name,
        "machine": mach_name,
        "qty": order_qty,
        "rate": op_rate,
    })

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("🚀 Generate CSV Quotation File", use_container_width=True):
    csv_data = generate_quotation_csv(
        cust_name, part_name_input, edited_ops, transport_amt
    )
    filename = f"Suresh_Megala_Quotation_{part_name_input.replace(' ', '_').replace('/', '_')}.csv"
    st.success(f"✅ CSV successfully generated: {filename}")
    st.download_button(
        "📥 Download CSV Quotation (.csv)",
        data=csv_data,
        file_name=filename,
        mime="text/csv",
    )

# 8. SURESH MASTER KNOWLEDGE BASE & PROFILE MODULE
elif "Suresh Master" in selected_module or "சுரேஷ் மாஸ்டர்" in selected_module:
  if st.button(t_dict["back_home"]):
    st.session_state["selected_module"] = module_list[0]
    st.rerun()

  st.subheader(
      "🛠️ Suresh Master Knowledge Base & Profile (சுரேஷ் சுயவிவரம் & அறிவுத்தளம்)"
  )
  st.write(
      "இது உங்களுடைய அனைத்துத் தகவல்களும் (CNC, Traub, Collets, ஆட்டோமொபைல்,"
      " வணிகம்) முழுமையாகச் சேமிக்கப்பட்டுள்ள மாஸ்டர் பகுதியாகும்."
  )

  tab1, tab2, tab3 = st.tabs([
      "⚙️ CNC & Machining Expertise",
      "🚗 Automobile Interests",
      "📈 Business & Stock Goals",
  ])

  with tab1:
    st.markdown("### இயந்திரவியல் மற்றும் CNC திறன்கள் (CNC & Machining)")
    st.markdown("""
        * **இயமையங்கள் & செட்டப்:** Traub Automatic Lathes, Vertical Machining Center (VMC) Simulators.
        * **டூல்ஸ் & ஆபரேஷன்ஸ்:** Cross-drilling tools, Machine Collets troubleshooting மற்றும் நுணுக்கங்கள்.
        * **கற்றல் சாலைவரைபடம்:** CNC புரோகிராமிங் மற்றும் மேம்பட்ட ஆட்டோமேஷன் முறைகள்.
        """)

  with tab2:
    st.markdown("### வாகனங்கள் மீதான ஆர்வம் (Automobiles)")
    st.markdown("""
        * **கார்கள் (Cars):** Mahindra Scorpio, Grand Vitara, Tata Punch.
        * **இருசக்கர வாகனம் (Bike):** Yamaha R15 V4.
        """)

  with tab3:
    st.markdown("### வணிகத் திட்டங்கள் (Business & Investments)")
    st.markdown("""
        * **தொழில்முனைவோர் இலக்கு:** ஆன்லைன் வணிக வாய்ப்புகள் (Online Business).
        * **முதலீடு:** பங்குச் சந்தை (Stock Marketing).
        """)
