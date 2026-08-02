import os
import math
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Megala CNC Mate - Smart CNC & Workshop Manager",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- HEADER SECTION WITH SAFE LOGO LOADER ---
col_logo, col_title = st.columns([1, 6])

with col_logo:
  if os.path.exists("Logo.png"):
    try:
      st.image("Logo.png", width=110)
    except Exception:
      st.markdown("⚙️ **[Logo Error]**")
  else:
    st.markdown("⚙️ **[Logo Here]**")

with col_title:
  st.title("⚙️ Megala CNC Mate")
  st.markdown(
      "**SMART CNC. SIMPLE WORK.** — Customer Quotation, Production, G-Code,"
      " Letter Cutting & Stock Management"
  )

st.markdown("---")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("📌 Menu Navigation")
app_mode = st.sidebar.selectbox(
    "Select Module",
    [
        "🏠 Dashboard",
        "💰 Customer Quotation",
        "🏭 Production Tracker",
        "📜 G-Code Generator",
        "🔤 Letter Cutting",
        "📦 Stock Management",
    ],
)

# --- 1. DASHBOARD MODULE ---
if app_mode == "🏠 Dashboard":
  st.header("📊 Welcome to Megala CNC Mate Dashboard")
  st.write(
      "Your ultimate smart automation tool for CNC machining, cost estimation,"
      " and workshop management."
  )

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(label="Active Modules", value="5 Ready")
  with col2:
    st.metric(label="System Status", value="Online 🟢")
  with col3:
    st.metric(label="Environment", value="Streamlit Cloud")
  with col4:
    st.metric(label="Version", value="Final v1.0")

  st.info(
      "💡 **Tip:** Use the sidebar menu to switch between Quotation, Production,"
      " G-Code, Letter Cutting, and Stock Management modules."
  )

# --- 2. CUSTOMER QUOTATION MODULE ---
elif app_mode == "💰 Customer Quotation":
  st.header("💰 Customer Quotation Calculator")
  st.write(
      "Calculate accurate machining costs, raw materials, and profit margins"
      " for your customers."
  )

  col1, col2 = st.columns(2)
  with col1:
    customer_name = st.text_input("Customer Name", "ABC Industries")
    part_name = st.text_input("Component Name", "Steel Bush / Shaft")
    material_cost = st.number_input(
        "Raw Material Cost per piece (₹)", min_value=0.0, value=150.0, step=10.0
    )
    machining_time = st.number_input(
        "Machining Time per piece (Minutes)", min_value=0.1, value=5.0, step=0.5
    )

  with col2:
    machine_rate_per_hour = st.number_input(
        "Machine Hourly Rate (₹/hr)", min_value=0.0, value=600.0, step=50.0
    )
    quantity = st.number_input(
        "Batch Quantity (Pieces)", min_value=1, value=100, step=10
    )
    profit_margin = st.slider("Profit Margin (%)", 0, 50, 20)

  if st.button("Calculate Quotation"):
    machining_cost_per_piece = (machine_rate_per_hour / 60) * machining_time
    total_cost_per_piece = material_cost + machining_cost_per_piece
    unit_price = total_cost_per_piece * (1 + profit_margin / 100)
    total_quotation = unit_price * quantity

    st.success("✅ Quotation Calculated Successfully!")
    st.markdown(f"### Quotation Summary for: **{customer_name}** ({part_name})")
    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric(
        label="Cost per Piece", value=f"₹{unit_price:.2f}", delta=f"+{profit_margin}% Profit"
    )
    res_col2.metric(label="Total Quantity", value=f"{quantity} Nos")
    res_col3.metric(label="Grand Total Price", value=f"₹{total_quotation:,.2f}")

# --- 3. PRODUCTION TRACKER MODULE ---
elif app_mode == "🏭 Production Tracker":
  st.header("🏭 Production & Batch Tracker")
  st.write("Track daily machining output, cycle times, and machine efficiency.")

  batch_no = st.text_input("Batch / Job Order Number", "JOB-2026-001")
  target_qty = st.number_input("Target Quantity", min_value=1, value=500)
  completed_qty = st.number_input("Completed Quantity", min_value=0, value=350)
  cycle_time = st.number_input("Cycle Time per part (Seconds)", value=45.0)

  if st.button("Calculate Production Metrics"):
    progress = (completed_qty / target_qty) * 100
    total_time_hours = (target_qty * cycle_time) / 3600

    st.progress(min(progress / 100.0, 1.0))
    st.write(f"**Completion Status:** {progress:.1f}% Done")
    st.info(
        f"⏱️ Estimated total time to complete target batch:"
        f" **{total_time_hours:.2f} Hours**"
    )

# --- 4. G-CODE GENERATOR MODULE ---
elif app_mode == "📜 G-Code Generator":
  st.header("📜 CNC G-Code Generator")
  st.write(
      "Generate standard G-code programs for turning, facing, and drilling"
      " operations."
  )

  operation = st.selectbox(
      "Select Operation", ["Face Turning", "Cylindrical Turning", "Drilling"]
  )
  start_z = st.number_input("Start Z Position", value=0.0)
  feed_rate = st.number_input("Feed Rate (F)", value=0.15)
  spindle_speed = st.number_input("Spindle Speed (S)", value=1500)

  if st.button("Generate G-Code"):
    gcode = f"""
O0001 (MEGALA CNC MATE PROGRAM)
G21 G90 G40 G80 G18
M03 S{spindle_speed}
G00 X52.0 Z2.0
(OPERATION: {operation.upper()})
G01 Z{start_z} F{feed_rate}
G00 Z50.0
M05
M30
"""
    st.code(gcode, language="text")
    st.download_button(
        label="📥 Download G-Code File (.nc / .txt)",
        data=gcode,
        file_name="program.nc",
        mime="text/plain",
    )

# --- 5. LETTER CUTTING MODULE ---
elif app_mode == "🔤 Letter Cutting":
  st.header("🔤 Letter & Engraving Module")
  st.write("Plan coordinates and parameters for engraving and letter cutting.")

  text_input = st.text_input(
      "Enter Text to Engrave", "MEGALA CNC", max_chars=20
  )
  font_height = st.number_input("Character Height (mm)", value=10.0)
  depth = st.number_input("Engraving Depth (mm)", value=0.5, step=0.1)

  if st.button("Generate Engraving Parameters"):
    st.success(f"Parameters ready for text: **{text_input}**")
    st.write(
        f"- **Font Height:** {font_height} mm\n- **Depth of Cut (Z):** -{depth}"
        f" mm\n- **Recommended Tool:** 60° V-Bit Cutter"
    )

# --- 6. STOCK MANAGEMENT MODULE ---
elif app_mode == "📦 Stock Management":
  st.header("📦 Stock & Inventory Management")
  st.write("Monitor raw materials, metal bars, and inserts stock levels.")

  material_type = st.selectbox(
      "Material Grade", ["EN8", "EN24", "Aluminum 6061", "Brass", "Mild Steel"]
  )
  stock_weight = st.number_input("Available Stock Weight (Kg)", value=125.0)
  min_limit = st.number_input(
      "Minimum Alert Limit (Kg)", value=30.0
  )

  if stock_weight <= min_limit:
    st.warning("⚠️ **Warning:** Stock is running low! Reorder required.")
  else:
    st.success("✅ Stock level is sufficient.")

  st.write(f"Current Stock of **{material_type}**: **{stock_weight} Kg**")

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>© 2026 Megala CNC Mate | Built"
    " for Smart Workshop Automation</p>",
    unsafe_allow_html=True,
)
