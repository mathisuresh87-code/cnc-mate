import base64
import io
import os
import math
from PIL import Image
import pandas as pd
import streamlit as st

# PDF Generation library check
try:
  from reportlab.lib.pagesizes import letter
  from reportlab.pdfgen import canvas
  REPORTLAB_AVAILABLE = True
except ImportError:
  REPORTLAB_AVAILABLE = False

# Page Configuration
st.set_page_config(
    page_title="MEGALA CNC MATE - Smart CNC. Simple Work.",
    page_icon="⚙️",
    layout="wide",
)

# Helper function to convert logo safely
def get_image_base64(path):
  if os.path.exists(path):
    with open(path, "rb") as f:
      return base64.b64encode(f.read()).decode()
  return ""

logo_base64 = get_image_base64("logo.png")

# Custom UI Styling
st.markdown(
    """
<style>
.stApp { background: linear-gradient(135deg, #050B18 0%, #0A1428 50%, #040711 100%); color: #FFFFFF; }
.brand-container { text-align: center; padding: 20px 0; background: radial-gradient(circle at center, #0F1C3F 0%, #070B19 100%); border-bottom: 2px solid #1E3A8A; margin-bottom: 15px; border-radius: 0 0 20px 20px; }
.logo-glow-box { display: inline-block; padding: 8px; background: radial-gradient(circle, rgba(72, 202, 228, 0.3) 0%, rgba(10, 20, 40, 0.95) 100%); border-radius: 50%; border: 2px solid #48CAE4; margin-bottom: 10px; }
.brand-title { font-size: 28px; font-weight: 900; background: linear-gradient(90deg, #48CAE4, #0077B6, #FFFFFF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.metric-card { background: linear-gradient(145deg, #111E38, #0B132B); padding: 20px; border-radius: 16px; border: 1px solid #1E3A8A; text-align: center; margin-bottom: 15px; }
.stButton>button { width: 100%; background: linear-gradient(90deg, #1D4ED8, #00B4D8); color: white; font-weight: bold; border-radius: 12px; height: 48px; border: none; }
.upload-status-box { background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; padding: 15px; border-radius: 12px; margin-top: 12px; }
</style>
""",
    unsafe_allow_html=True,
)

# Header
if logo_base64:
  logo_display_html = f"""<div class="logo-glow-box"><img src="data:image/png;base64,{logo_base64}" width="60" /></div>"""
else:
  logo_display_html = '<div style="font-size: 35px; margin-bottom: 2px;">⚙️</div>'

st.markdown(f'<div class="brand-container">{logo_display_html}<div class="brand-title">MEGALA CNC MATE</div></div>', unsafe_allow_html=True)

# Session States
if "nav_menu" not in st.session_state: st.session_state.nav_menu = "Home Dashboard"
if "calc_results" not in st.session_state: st.session_state.calc_results = None

# Sidebar
menu_options = ["Home Dashboard", "Rod & Tube Calculator", "Production & Cycle Time", "Stock Management", "Advanced G-Code Generator", "Quotation & PDF"]
selected_sidebar_menu = st.sidebar.radio("Navigation Menu", menu_options, index=menu_options.index(st.session_state.nav_menu))
if selected_sidebar_menu != st.session_state.nav_menu:
  st.session_state.nav_menu = selected_sidebar_menu
  st.rerun()

# --- MODULES ---

# 1. HOME DASHBOARD
if st.session_state.nav_menu == "Home Dashboard":
  st.subheader("Welcome, Operator! 👋")
  col1, col2 = st.columns(2)
  if col1.button("Open Rod Calculator"): st.session_state.nav_menu = "Rod & Tube Calculator"; st.rerun()
  if col2.button("Open Quotation Generator"): st.session_state.nav_menu = "Quotation & PDF"; st.rerun()

# 2. ROD & TUBE CALCULATOR (Enhanced)
elif st.session_state.nav_menu == "Rod & Tube Calculator":
  st.subheader("Rod & Tube Calculator (3D Pro)")
  
  adv_drawing = st.file_uploader("📁 Upload Part Drawing (Reference)", type=["png", "jpg", "pdf"])
  if adv_drawing:
      st.markdown('<div class="upload-status-box">✅ Drawing Loaded Successfully!</div>', unsafe_allow_html=True)
      st.image(adv_drawing, caption="Uploaded Drawing Reference", use_container_width=True)

  c1, c2 = st.columns(2)
  with c1:
      rod_len = st.number_input("Available Rod Length (Meter)", value=4.0)
      part_len = st.number_input("Part Length (mm)", value=122.50)
      cut_allowance = st.number_input("Cutting/Facing Allowance (mm)", value=3.00)
  with c2:
      req_qty = st.number_input("Required Quantity (Nos)", value=100)
      cycle_sec = st.number_input("Cycle Time (Seconds)", value=17.0)
      shift_hours = st.number_input("Working Hours per Shift", value=8.0)

  if st.button("Calculate & Render Detailed Report"):
      eff_part_len = part_len + cut_allowance
      parts_per_rod = int((rod_len * 1000) / eff_part_len) if eff_part_len > 0 else 0
      total_rods_needed = math.ceil(req_qty / parts_per_rod) if parts_per_rod > 0 else 0
      scrap_per_rod = (rod_len * 1000) - (parts_per_rod * eff_part_len)
      
      # Time Calculations
      total_hours = (req_qty * cycle_sec) / 3600
      total_days = total_hours / shift_hours if shift_hours > 0 else 0
      prod_per_hr = int(3600 / cycle_sec) if cycle_sec > 0 else 0

      st.markdown("---")
      st.markdown("### 📊 Detailed Production Report")
      r1, r2, r3 = st.columns(3)
      r1.metric("Parts per Rod", f"{parts_per_rod} Nos")
      r2.metric("Total Rods Needed", f"{total_rods_needed} Nos")
      r3.metric("Scrap per Rod", f"{scrap_per_rod:.2f} mm")
      
      st.markdown("---")
      st.markdown("### ⏱️ Time & Scheduling")
      t1, t2, t3 = st.columns(3)
      t1.metric("Total Machine Time", f"{total_hours:.2f} Hours")
      t2.metric("Total Days (Required)", f"{total_days:.2f} Days")
      t3.metric("Production Rate", f"{prod_per_hr} parts/hr")

# 3. PRODUCTION & CYCLE TIME
elif st.session_state.nav_menu == "Production & Cycle Time":
    st.subheader("Production & Efficiency Analysis")
    # ... (Keep previous logic here) ...

# 4. STOCK MANAGEMENT
elif st.session_state.nav_menu == "Stock Management":
    st.subheader("Stock Management")
    # ... (Keep previous logic here) ...

# 5. ADVANCED G-CODE GENERATOR
elif st.session_state.nav_menu == "Advanced G-Code Generator":
    st.subheader("G-Code Generator")
    # ... (Keep previous logic here) ...

# 6. QUOTATION & PDF
elif st.session_state.nav_menu == "Quotation & PDF":
    st.subheader("Quotation Generator")
    # ... (Keep previous logic here) ...
