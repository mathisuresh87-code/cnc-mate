import os
import math
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Megala CNC Mate - Professional CNC & Workshop Manager",
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
      "**SMART CNC. SIMPLE WORK.** — Complete Quotation, Production, G-Code,"
      " Letter Cutting & Advanced Stock Management (Rod Grades & Types)"
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
        "📦 Stock & Rod Management",
    ],
)

# --- 1. DASHBOARD MODULE ---
if app_mode == "🏠 Dashboard":
  st.header("📊 Welcome to Megala CNC Mate Dashboard")
  st.write(
      "Your ultimate smart automation tool for CNC machining, cost estimation,"
      " rod inventory, and workshop management."
  )

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(label="Active Modules", value="6 Ready")
  with col2:
    st.metric(label="System Status", value="Online 🟢")
  with col3:
    st.metric(label="Environment", value="Streamlit Cloud")
  with col4:
    st.metric(label="Version", value="Final Pro v2.0")

  st.info(
      "💡 **Tip:** Use the sidebar to access Quotation, Production, G-Code,"
      " Letter Cutting, and Stock/Rod Management modules."
  )

# --- 2. CUSTOMER QUOTATION MODULE ---
elif app_mode == "💰 Customer Quotation":
  st.header("💰 Customer Quotation Calculator")
  st.write(
      "Calculate accurate machining costs, material grades, rod types, and profit margins."
  )

  col1, col2 = st.columns(2)
  with col1:
    customer_name = st.text_input("Customer Name", "ABC Industries")
    part_name = st.text_input("Component Name", "Steel Bush / Shaft")
    
    material_grade = st.selectbox(
        "Select Material Grade",
        ["EN8", "EN24", "Aluminum 6061", "Mild Steel (MS)", "Brass", "Stainless Steel 304", "Cast Iron"],
    )
    rod_type = st.selectbox(
        "Select Rod Type / Profile",
        ["Round Bar", "Hexagon Bar", "Square Bar", "Flat Plate / Sheet"],
    )
    
    material_cost_per_kg = st.number_input(
        "Raw Material Cost per Kg (₹)", min_value=0.0, value=85.0, step=5.0
    )

  with col2:
    estimated_weight = st.number_input("Estimated Part Weight (Kg)", min_value=0.01, value=1.2, step=0.1)
    machining_time = st.number_input(
        "Machining Time per piece (Minutes)", min_value=0.1, value=6.0, step=0.5
    )
    machine_rate_per_hour = st.number_input(
        "Machine Hourly Rate (₹/hr)", min_value=0.0, value=600.0, step=50.0
    )
    quantity = st.number_input(
        "Batch Quantity (Pieces)", min_value=1, value=100, step=10
    )
    profit_margin = st.slider("Profit Margin (%)", 0, 50, 20)

  if st.button("Calculate Final Quotation"):
    material_total_cost = estimated_weight * material_cost_per_kg
    machining_cost_per_piece = (machine_rate_per_hour / 60) * machining_time
    total_cost_per_piece = material_total_cost + machining_cost_per_piece
    unit_price = total_cost_per_piece * (1 + profit_margin / 100)
    total_quotation = unit_price * quantity

    st.success("✅ Quotation Calculated Successfully!")
    st.markdown(f"### Quotation Summary for: **{customer_name}** ({part_name})")
    st.write(f"- **Grade:** {material_grade} | **Profile:** {rod_type}")
    
    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric(
        label="Cost per Piece", value=f"₹{unit_price:.2f}", delta=f"+{profit_margin}% Profit"
    )
    res_col2.metric(label="Batch Quantity", value=f"{quantity} Nos")
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
      "Generate standard G-code programs for turning, facing, and drilling operations."
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

# --- 6. STOCK & ROD MANAGEMENT MODULE ---
elif app_mode == "📦 Stock & Rod Management":
  st.header("📦 Stock & Rod Inventory Management")
  st.write("Monitor raw material grades, rod types, diameters, and stock levels.")

  col1, col2 = st.columns(2)
  with col1:
    stock_grade = st.selectbox(
        "Material Grade", ["EN8", "EN24", "Aluminum 6061", "Mild Steel (MS)", "Brass", "Stainless Steel 304", "Cast Iron"], key="stock_grade"
    )
    stock_rod_type = st.selectbox(
        "Rod Type / Profile", ["Round Bar", "Hexagon Bar", "Square Bar", "Flat Plate"], key="stock_rod"
    )
    diameter_size = st.number_input("Rod Diameter / Size (mm)", min_value=1.0, value=40.0, step=1.0)

  with col2:
    length_mm = st.number_input("Rod Length (mm)", min_value=100.0, value=1000.0, step=50.0)
    available_weight = st.number_input("Available Stock Weight (Kg)", min_value=0.0, value=125.0)
    min_limit = st.number_input("Minimum Alert Limit (Kg)", min_value=0.0, value=30.0)

  if st.button("Check Stock Status"):
    if available_weight <= min_limit:
      st.warning(f"⚠️ **Warning:** Low Stock for {stock_grade} ({stock_rod_type} - {diameter_size}mm)! Reorder required.")
    else:
      st.success(f"✅ Stock level for {stock_grade} ({stock_rod_type}) is sufficient.")

    st.write(f"### Inventory Details:")
    st.write(f"- **Grade:** {stock_grade}")
    st.write(f"- **Type:** {stock_rod_type}")
    st.write(f"- **Size:** {diameter_size} mm diameter, {length_mm} mm length")
    st.write(f"- **Current Stock Weight:** **{available_weight} Kg**")

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>© 2026 Megala CNC Mate | Built for Smart Workshop Automation</p>",
    unsafe_allow_html=True,
)
