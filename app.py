import math
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Megala CNC Mate - Smart CNC & Production",
    page_icon="⚙️",
    layout="wide",
)

# --- HEADER WITH USER LOGO & TITLE ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
  try:
    st.image("logo.png", width=120)
  except:
    st.write("⚙️ [Logo]")

with col_title:
  st.title("⚙️ Megala CNC Mate")
  st.markdown(
      "**SMART CNC, SIMPLE WORK.** — Customer Quotation, Production, Stock"
      " Management & CNC Calculator System"
  )

st.markdown("---")

# Sidebar Navigation
st.sidebar.title("Navigation / மெனு")
menu = st.sidebar.radio(
    "Choose Option / பிரிவைத் தேர்ந்தெடுக்கவும்:",
    [
        "🏠 Home / முகப்பு",
        "🧮 CNC & Traub Calculator",
        "📜 G-Code Generator",
        "📋 Customer Quotation",
        "📦 Stock & Production Mgmt",
    ],
)

if menu == "🏠 Home / முகப்பு":
  st.header("Welcome to Megala CNC Mate, Suresh! 🙏")
  st.write(
      "இந்த சாஃப்ட்வேர் உங்கள் ஒர்க்ஷாப் (Workshop) மற்றும் CNC மிஷின் பணிகளை"
      " மிக எளிமையாகவும் துல்லியமாகவும் நிர்வகிக்க உதவுகிறது."
  )

  col1, col2, col3 = st.columns(3)
  with col1:
    st.info("🧮 **CNC & Traub Calculator**\n\nCutting Speed, RPM, Cycle Time")
  with col2:
    st.success("📜 **G-Code Generator**\n\nTurning, Facing & Drilling Codes")
  with col3:
    st.warning("📋 **Quotation & Stock**\n\nCustomer Billing & Inventory Tracking")

  st.markdown("---")
  st.subheader("💡 Quick Tips for Suresh:")
  st.write(
      "1. **GitHub** இல் `logo.png` சரியாகப் பதிவேற்றப்பட்டுள்ளதை உறுதிப்படுத்திக்"
      " கொள்ளவும்.\n2. அனைத்து கால்குலேட்டர் மற்றும் ஜி-கோடு வசதிகளையும்"
      " சைடுபார் மூலம் அணுகலாம்."
  )

elif menu == "🧮 CNC & Traub Calculator":
  st.header("🧮 CNC & Traub Calculator / மிஷினிங் கணக்கீடுகள்")

  calc_type = st.selectbox(
      "Select Calculation Type:",
      [
          "RPM & Cutting Speed (சுழற்சி வேகம்)",
          "Rod/Bar Weight Calculator (பொருள் எடை)",
          "Cycle Time Estimation (நேரக் கணக்கீடு)",
      ],
  )

  if calc_type == "RPM & Cutting Speed (சுழற்சி வேகம்)":
    col1, col2 = st.columns(2)
    with col1:
      vc = st.number_input(
          "Cutting Speed (Vc in m/min):", value=150.0, step=10.0
      )
      dia = st.number_input(
          "Component Diameter (D in mm):", value=50.0, step=1.0
      )
    with col2:
      if dia > 0:
        rpm = (vc * 1000) / (math.pi * dia)
        st.success(f"### Calculated RPM: **{rpm:.2f} rev/min**")
        st.write(
            f"Formula: (Vc × 1000) / (π × D) = ({vc} × 1000) / (3.1416 ×"
            f" {dia})"
        )
      else:
        st.error("Diameter must be greater than 0.")

  elif calc_type == "Rod/Bar Weight Calculator (பொருள் எடை)":
    col1, col2 = st.columns(2)
    with col1:
      mat_type = st.selectbox(
          "Material Type:", ["Steel / Iron", "Aluminum", "Brass", "Copper"]
      )
      shape = st.selectbox(
          "Bar Shape:", ["Round (உருண்டை)", "Hexagon (அறுகோணம்)"]
      )
      d_rod = st.number_input("Diameter / Across Flat (mm):", value=25.0)
      length = st.number_input(
          "Length per piece (mm):", value=100.0, step=10.0
      )
      qty = st.number_input("Quantity (Nos):", value=100, step=1)
    with col2:
      densities = {
          "Steel / Iron": 0.00785,
          "Aluminum": 0.0027,
          "Brass": 0.0085,
          "Copper": 0.00896,
      }
      rho = densities[mat_type]

      if shape == "Round (உருண்டை)":
        r = d_rod / 2.0
        vol = math.pi * (r**2) * length
        wt_single_g = vol * (rho / 1000.0)
        total_wt_kg = (wt_single_g * qty) / 1000.0

        st.success(f"### Single Piece Weight: **{wt_single_g:.2f} grams**")
        st.info(f"### Total Weight ({qty} Nos): **{total_wt_kg:.3f} kg**")
      else:
        s = d_rod
        area = (math.sqrt(3) / 2.0) * (s**2)
        vol = area * length
        wt_single_g = vol * (rho / 1000.0)
        total_wt_kg = (wt_single_g * qty) / 1000.0
        st.success(f"### Single Piece Weight: **{wt_single_g:.2f} grams**")
        st.info(f"### Total Weight ({qty} Nos): **{total_wt_kg:.3f} kg**")

  elif calc_type == "Cycle Time Estimation (நேரக் கணக்கீடு)":
    st.write("Enter machining parameters for cycle time estimation:")
    l_cut = st.number_input("Cutting Length (mm):", value=50.0)
    f_rate = st.number_input("Feed Rate (mm/rev):", value=0.15)
    rpm_val = st.number_input("Spindle RPM:", value=1200.0)
    passes = st.number_input("Number of Passes:", value=2, step=1)

    if f_rate > 0 and rpm_val > 0:
      time_per_pass_min = l_cut / (f_rate * rpm_val)
      total_time_sec = time_per_pass_min * passes * 60
      st.success(
          "Estimated Cutting Time per piece: **"
          f"{total_time_sec:.1f} seconds**"
      )
    else:
      st.error("Feed rate and RPM must be greater than 0.")

elif menu == "📜 G-Code Generator":
  st.header("📜 G-Code Generator / ஜி-கோடு தயாரிப்பு")
  op_type = st.selectbox(
      "Select Operation:",
      ["Simple Turning (வெளி டர்னிங்)", "Facing (பேசிங்)", "Drilling (ட்ரில்லிங்)"],
  )

  if op_type == "Simple Turning (வெளி டர்னிங்)":
    stock_d = st.number_input("Initial Diameter (mm):", value=50.0)
    fin_d = st.number_input("Final Diameter (mm):", value=45.0)
    z_len = st.number_input("Turning Length (mm Z):", value=-60.0)
    feed = st.number_input("Feed (F):", value=0.2)
    spindle = st.number_input("Spindle Speed (S):", value=1500)

    if st.button("Generate G-Code"):
      gcode = f"""O0001 (MEGALA CNC - TURNING PROGRAM)
G21 G40 G97 G99
M03 S{spindle}
G00 X{stock_d + 2.0} Z2.0
G01 Z0.0 F{feed}
G01 X{fin_d}
G01 Z{z_len}
G00 X{stock_d + 5.0}
G00 Z50.0
M05
M30"""
      st.code(gcode, language="text")

  elif op_type == "Facing (பேசிங்)":
    start_d = st.number_input("Starting Diameter (mm):", value=50.0)
    feed = st.number_input("Feed (F):", value=0.15)
    spindle = st.number_input("Spindle Speed (S):", value=1800)

    if st.button("Generate G-Code"):
      gcode = f"""O0002 (MEGALA CNC - FACING PROGRAM)
G21 G40 G97 G99
M03 S{spindle}
G00 X{start_d + 2.0} Z0.0
G01 X-0.5 F{feed}
G00 Z2.0
G00 X{start_d + 5.0}
M05
M30"""
      st.code(gcode, language="text")

  elif op_type == "Drilling (ட்ரில்லிங்)":
    drill_z = st.number_input("Drilling Depth (mm, -ve value):", value=-30.0)
    peck = st.number_input("Peck Increment (Q in microns/mm):", value=2.0)
    feed = st.number_input("Feed (F):", value=0.1)
    spindle = st.number_input("Spindle Speed (S):", value=1000)

    if st.button("Generate G-Code"):
      gcode = f"""O0003 (MEGALA CNC - DRILLING PROGRAM)
G21 G40 G97 G99
M03 S{spindle}
G00 X0.0 Z5.0
G83 Z{drill_z} R1.0 Q{peck * 1000} F{feed}
G80
G00 Z50.0
M05
M30"""
      st.code(gcode, language="text")

elif menu == "📋 Customer Quotation":
  st.header("📋 Customer Quotation & Billing / வாடிக்கையாளர் மதிப்பீடு")
  cust_name = st.text_input("Customer Name:", value="ABC Engineering")
  part_name = st.text_input("Component Name:", value="Pin / Bush")
  qty_q = st.number_input("Order Quantity (Nos):", value=500, step=10)
  raw_cost = st.number_input("Raw Material Cost per piece (₹):", value=45.0)
  mach_cost = st.number_input(
      "Machining & Labor Cost per piece (₹):", value=25.0
  )
  profit_margin = st.slider("Profit Margin (%)", 5, 50, 20)

  if st.button("Calculate Quotation"):
    unit_cost = raw_cost + mach_cost
    unit_price = unit_cost * (1 + profit_margin / 100.0)
    total_price = unit_price * qty_q

    st.success("### Quotation Summary")
    st.write(f"**Customer:** {cust_name}")
    st.write(f"**Component:** {part_name}")
    st.write(f"**Quantity:** {qty_q} Nos")
    st.write(f"**Cost per piece:** ₹{unit_cost:.2f}")
    st.write(f"**Quoted Price per piece:** ₹{unit_price:.2f}")
    st.markdown(f"### **Total Quotation Amount: ₹{total_price:,.2f}**")

elif menu == "📦 Stock & Production Mgmt":
  st.header(
      "📦 Stock & Production Management / பொருள் மற்றும் உற்பத்தி மேலாண்மை"
  )
  st.write("Manage raw materials inventory and track daily production status.")

  col1, col2 = st.columns(2)
  with col1:
    st.subheader("Raw Material Stock (காঁচப்பொருள் இருப்பு)")
    material_name = st.text_input("Material Grade / Size", value="EN8 Rod 40mm")
    stock_qty = st.number_input("Available Stock Weight (kg):", value=250.0)
    min_level = st.number_input("Minimum Reorder Level (kg):", value=50.0)

    if stock_qty <= min_level:
      st.error(
          "⚠️ Stock is LOW! Reorder required. "
          f"({stock_qty} kg <= {min_level} kg)"
      )
    else:
      st.success(f"✅ Stock is sufficient. ({stock_qty} kg available)")

  with col2:
    st.subheader("Daily Production Tracker (தினசரி உற்பத்தி)")
    shift = st.selectbox(
        "Select Shift:", ["Shift 1 (Morning)", "Shift 2 (Night)"]
    )
    produced_qty = st.number_input(
        "Components Produced Today:", value=450, step=10
    )
    rejected_qty = st.number_input("Rejected Components:", value=5, step=1)

    ok_qty = produced_qty - rejected_qty
    efficiency = (ok_qty / produced_qty * 100) if produced_qty > 0 else 0.0
    st.info(f"**OK Components:** {ok_qty} Nos")
    st.info(f"**Production Efficiency:** {efficiency:.1f}%")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>© 2026 Megala CNC Mate |"
    " Designed for Suresh | SMART CNC, SIMPLE WORK.</p>",
    unsafe_allow_html=True,
)
