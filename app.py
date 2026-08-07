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
    page_title="Megala CNC Mate - Enterprise CNC Automation",
    page_icon="⚙️",
    layout="wide",
)

# Custom CSS for Uniform Layout, Buttons, and Mobile Optimization
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #090d1f 0%, #111827 40%, #1e1b4b 100%);
        color: #f8fafc;
        font-family: 'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    .main-title {
        font-size: 2.3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #38bdf8 0%, #c084fc 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: 1px;
        text-transform: uppercase;
        line-height: 1.2;
    }
    .sub-title {
        font-size: 0.8rem;
        color: #38bdf8;
        margin: 0;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }
    div[data-testid="column"] {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.85) 0%, rgba(49, 46, 129, 0.5) 100%);
        border: 1.5px solid rgba(139, 92, 246, 0.4);
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
        margin-bottom: 15px;
    }
    /* Uniform Button Styling */
    div.stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 50%, #ec4899 100%);
        color: #ffffff !important;
        border-radius: 12px;
        border: 1.5px solid rgba(236, 72, 153, 0.6);
        font-weight: 800;
        width: 100%;
        height: 48px;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        border-color: #38bdf8;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.5);
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070b19 0%, #0f172a 100%);
        border-right: 1.5px solid rgba(139, 92, 246, 0.3);
    }
    </style>
""",
    unsafe_allow_html=True,
)

LOGO_PATH = "company_logo_permanent.png"

module_list = [
    "🏠 Home / முகப்பு",
    "📐 Rod Calculator (ராட் கால்குலேட்டர்)",
    "⏱️ Production Calculator (உற்பத்தி கால்குலேட்டர்)",
    "💰 Costing & Quotation Calculator (செலவு & கொட்டேஷன்)",
    "📦 Stock Management (ஸ்டாக் மேனேஜ்மென்ட்)",
    "📷 Drawing & Multi-Op G-Code (டிராயிங் & ஆட்டோ ரிப்போர்ட்)",
    (
        "📋 Process Breakdown & Customer Quotation (புதிய கொட்டேஷன்"
        " மாடியூல்)"
    ),
    "⚙️ More Menu & Settings (அமைப்புகள் & மாஸ்டர்ஸ்)",
]

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


# Sidebar Navigation
st.sidebar.markdown(
    """<div style="text-align: center; padding: 5px 0 10px 0;"><h3"
    " style="color: #ec4899; margin: 0; font-size: 1.15rem; font-weight: 900;"
    " letter-spacing: 1.5px;">MEGALA CNC MATE</h3></div>""",
    unsafe_allow_html=True,
)

encoded_sidebar_img = get_base64_image(LOGO_PATH)
if encoded_sidebar_img:
  st.sidebar.markdown(
      f"""<div style="text-align: center; margin-bottom: 12px;"><div"
      " style="background: linear-gradient(135deg, rgba(236, 72, 153, 0.3),"
      " rgba(56, 189, 248, 0.3)); border: 2px solid #ec4899; width: 65px;"
      " height: 65px; border-radius: 50%; margin: 0 auto; display: flex;"
      " align-items: center; justify-content: center; overflow: hidden;"><img"
      f" src="data:image/png;base64,{encoded_sidebar_img}" style="width: 100%;" /></div></div>""",
      unsafe_allow_html=True,
  )
else:
  st.sidebar.markdown(
      """<div style="text-align: center; margin-bottom: 12px;"><div style="background:"
      " linear-gradient(135deg, #4f46e5, #ec4899); width: 65px; height: 65px;"
      " border-radius: 50%; margin: 0 auto; display: flex; align-items:"
      " center; justify-content: center; font-weight: 900; color: white; font-size:"
      ' 1rem;">MC</div></div>',
      unsafe_allow_html=True,
  )

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

# Header Layout with Permanent Logo Fallback Check
col_logo, col_title = st.columns([0.18, 0.82], vertical_alignment="center")
with col_logo:
  encoded_img = get_base64_image(LOGO_PATH)
  if encoded_img:
    st.markdown(
        f"""<div style="border: 2px solid #ec4899; width: 75px; height: 75px;"
        " border-radius: 50%; display: flex; align-items: center;"
        " justify-content: center; overflow: hidden; background: #0f172a;"><img"
        f" src="data:image/png;base64,{encoded_img}" style="width: 100%;" /></div>""",
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        """<div style="background: linear-gradient(135deg, #4f46e5, #ec4899);"
        " width: 75px; height: 75px; border-radius: 50%; display: flex;"
        " align-items: center; justify-content: center; font-weight: 900;"
        " color: white; font-size: 1.2rem; border: 2px solid #ec4899;">MC</div>""",
        unsafe_allow_html=True,
    )
with col_title:
  st.markdown(
      '<h1 class="main-title">MEGALA INDUSTRIES</h1>', unsafe_allow_html=True
  )
  st.markdown(
      '<p class="sub-title">PRECISION CNC MACHINING & AUTOMATION</p>',
      unsafe_allow_html=True,
  )

st.markdown(
    "<hr style='margin-top: 5px; border-color: rgba(236, 72, 153, 0.3);'>",
    unsafe_allow_html=True,
)

# 1. HOME DASHBOARD (Default View)
if "Home" in selected_module:
  inv_df = st.session_state["stock_inventory_df"]
  m1, m2, m3, m4 = st.columns(4)
  with m1:
    st.metric("Active Machines", "4 Units", "Running 🚀")
  with m2:
    st.metric("Today's Output", "1,850 Nos", "+12% 📈")
  with m3:
    st.metric("Stock Items", f"{len(inv_df)} Items", "Optimal ✨")
  with m4:
    st.metric("Low Stock", "2 Alerts", "Check ⚠️")

  st.markdown("<br>", unsafe_allow_html=True)
  st.markdown("### 🚀 Core Automation Modules / முக்கிய மாட்யூல்கள்")

  c1, c2, c3 = st.columns(3)
  with c1:
    st.markdown("#### 📐 Rod Calculator")
    if st.button("Open Rod Calc", key="bh1"):
      st.session_state["selected_module"] = "📐 Rod Calculator (ராட் கால்குலேட்டர்)"
      st.rerun()
  with c2:
    st.markdown("#### ⏱️ Production Calc")
    if st.button("Open Prod Calc", key="bh2"):
      st.session_state["selected_module"] = (
          "⏱️ Production Calculator (உற்பத்தி கால்குலேட்டர்)"
      )
      st.rerun()
  with c3:
    st.markdown("#### 💰 Costing & Quote")
    if st.button("Open Costing", key="bh3"):
      st.session_state["selected_module"] = (
          "💰 Costing & Quotation Calculator (செலவு & கொட்டேஷன்)"
      )
      st.rerun()

  c4, c5, c6, c7 = st.columns(4)
  with c4:
    st.markdown("#### 📦 Stock")
    if st.button("Open Stock", key="bh4"):
      st.session_state["selected_module"] = (
          "📦 Stock Management (ஸ்டாக் மேனேஜ்மென்ட்)"
      )
      st.rerun()
  with c5:
    st.markdown("#### 📷 Drawing")
    if st.button("Open Drawing", key="bh5"):
      st.session_state["selected_module"] = (
          "📷 Drawing & Multi-Op G-Code (டிராயிங் & ஆட்டோ ரிப்போர்ட்)"
      )
      st.rerun()
  with c6:
    st.markdown("#### 📋 Quote Hub")
    if st.button("Open Quote", key="bh6"):
      st.session_state["selected_module"] = (
          "📋 Process Breakdown & Customer Quotation (புதிய கொட்டேஷன் மாடியூல்)"
      )
      st.rerun()
  with c7:
    st.markdown("#### ⚙️ Settings")
    if st.button("Open Settings", key="bh7"):
      st.session_state["selected_module"] = (
          "⚙️ More Menu & Settings (அமைப்புகள் & மாஸ்டர்ஸ்)"
      )
      st.rerun()
else:
  st.info(f"Selected Module: {selected_module}")
  if st.button("⬅️ Back to Home / முகப்புக்குத் திரும்பு", key="back_home_btn"):
    st.session_state["selected_module"] = "🏠 Home / முகப்பு"
    st.rerun()
