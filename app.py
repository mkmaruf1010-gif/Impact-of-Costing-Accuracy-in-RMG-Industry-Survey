import streamlit as st
import pandas as pd
import os

# Page Config
st.set_page_config(
    page_title="RMG Costing Accuracy Survey & Admin Portal",
    page_icon="📋",
    layout="wide"
)

# File to store responses
DATA_FILE = "survey_responses.csv"

# Session State Initialization
if "custom_questions" not in st.session_state:
    st.session_state.custom_questions = []

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

st.title("📋 Impact of Costing Accuracy in RMG Industry Survey")
st.markdown("Academic Research Survey on Merchandising Performance, Profitability, Buyer Satisfaction, and Order Execution Efficiency.")
st.divider()

# ==========================================
# SIDEBAR: ADMIN LOGIN, CODING LEGEND & PANEL
# ==========================================
st.sidebar.header("🔐 Admin Portal Access")

admin_password_input = st.sidebar.text_input("Enter Admin Password:", type="password", placeholder="Enter password...")
ADMIN_SECRET_KEY = "admin123"

if admin_password_input == ADMIN_SECRET_KEY:
    st.session_state.is_admin = True
    st.sidebar.success("🔓 Admin Access Granted!")
else:
    if admin_password_input:
        st.sidebar.error("❌ Incorrect Password!")
    st.session_state.is_admin = False

# Scale & Coding Legend in Sidebar (সাইডবারে কোডিং লিস্ট)
st.sidebar.divider()
st.sidebar.header("📊 Scale & Coding Legend")
st.sidebar.markdown("""
* **Slider Scale (0-5):** 
  * `0` = Not Applicable / Strongly Disagree
  * `1` = Disagree
  * `2` = Neutral
  * `3` = Agree
  * `4` = Strongly Agree
  * `5` = Highly Significant
* **Grading Scale (1-5):** 
  * `1` = Low Impact / Dislike
  * `2` = Moderate
  * `3` = High
  * `4` = Severe
  * `5` = Critical / Destructive
* **Checkbox:** 
  * Checked = `1` (Yes / Active)
  * Unchecked = `0` (No / Inactive)
""")

# IF ADMIN IS LOGGED IN, SHOW ADMIN CONTROLS & DASHBOARD
if st.session_state.is_admin:
    st.sidebar.divider()
    st.sidebar.header("🛠️ Dynamic Question System")
    
    with st.sidebar.form("add_question_form", clear_on_submit=True):
        new_q_code = st.text_input("Question Code (e.g., CA6, MP5):", placeholder="CA6")
        new_q_text = st.text_area("Question Statement (English):", placeholder="Enter statement...")
        new_q_section = st.selectbox(
            "Select Section:",
            [
                "Part 1: Costing Accuracy (Sliders)",
                "Part 2: Costing Tools & Techniques (Checkboxes)",
                "Part 3: Financial & Operational Impact (Grading Scale)",
                "Part 4: Buyer Satisfaction & Execution (Sliders)"
            ]
        )
        # Select widget type for the new question
        new_q_type = st.selectbox(
            "Select Question Type:",
            ["Slider (0-5)", "Grading Scale (1-5)", "Checkbox"]
        )
        add_btn = st.form_submit_button("➕ Add Question")

        if add_btn:
            if new_q_code and new_q_text:
                st.session_state.custom_questions.append({
                    "code": new_q_code,
                    "text": new_q_text,
                    "section": new_q_section,
                    "type": new_q_type
                })
                st.sidebar.success(f"Question '{new_q_code}' added successfully!")
            else:
                st.sidebar.error("Please fill in both Code and Statement.")

    if st.session_state.custom_questions:
        st.sidebar.markdown("---")
        st.sidebar.subheader("Added Custom Questions:")
        for q in st.session_state.custom_questions:
            st.sidebar.caption(f"**[{q['code']}]** {q['text']} *({q['type']})*")
else:
    st.sidebar.info("💡 Admin features are locked. Enter the correct password above to unlock.")

# ==========================================
# MAIN FORM (FOR RESPONDENTS)
# ==========================================
with st.form("rmg_survey_form"):
    
    st.header("SECTION A: Demographic & Organizational Profile")
    col1, col2 = st.columns(2)
    
    with col1:
        factory_type = st.selectbox("1. Type of Factory / Organization:", ["Knitwear", "Woven", "Sweater", "Denim/Bottoms", "Buying House"])
        position = st.selectbox("2. Your Current Position/Role:", ["Merchandiser / Assistant Merchandiser", "Senior Merchandiser / Manager", "Head of Merchandising / Director", "Costing & Pricing Analyst"])
    with col2:
        experience = st.selectbox("3. Total Years of Experience in RMG Merchandising:", ["1–3 years", "4–7 years", "8–12 years", "12+ years"])
        turnover = st.selectbox("4. Annual Export Turnover (USD):", ["Less than $5 Million", "$5M - $15M", "$15M - $30M", "Above $30M"])
        
    st.divider()
    
    st.header("SECTION B: Core Research Variables")
    
    survey_responses = {}
    checkbox_responses = {}

    # ==========================================
    # PART 1: SLIDER QUESTIONS
    # ==========================================
    st.subheader("Part 1: Costing Accuracy & Pre-Calculation")
    part1_questions = [
        ("CA1", "Our pre-costing accurately reflects actual production costs (fabric consumption, trims, CM, logistics)."),
        ("CA2", "We systematically account for fabric waste, shrinkage, and buffer margins in our cost sheets."),
        ("CA3", "Post-costing variance analysis is regularly conducted after shipment to evaluate estimation errors."),
        ("CA4", "Material price volatility (yarn, dyes, accessories) is well-predicted and integrated into quotes.")
    ]
    
    for code, text in part1_questions:
        survey_responses[code] = st.select_slider(
            f"[{code}] {text}",
            options=[0, 1, 2, 3, 4, 5],
            value=0,
            key=code
        )
    st.divider()

    # ==========================================
    # PART 2: CHECKBOX QUESTIONS
    # ==========================================
    st.subheader("Part 2: Costing Tools & Strategies Used")
    st.write("Select all tools, software, or strategies your factory regularly utilizes:")
    
    tool_options = {
        "TOOL_EXCEL": "Advanced Excel-based Costing Models & Macros",
        "TOOL_ERP": "Enterprise Resource Planning (ERP) Software e.g., SAP, BlueCherry",
        "TOOL_CAD": "Automated CAD Marker & Fabric Consumption Calculators",
        "TOOL_AI": "AI-driven or Predictive Costing Tools",
        "TOOL_HISTORICAL": "Historical Database of Past Orders for Benchmarking",
        "TOOL_BUFFER": "Standardized Buffer Pricing for Raw Material Fluctuations"
    }
    
    for key, label in tool_options.items():
        checkbox_responses[key] = st.checkbox(label, key=key)
    st.divider()

    # ==========================================
    # PART 3: GRADING SCALE (RADIO BUTTONS)
    # ==========================================
    st.subheader("Part 3: Impact of Costing Errors on Factory Performance")
    grading_questions = [
        ("IMP1", "Impact of inaccurate costing on unexpected profit/margin loss:"),
        ("IMP2", "Impact of costing mistakes on delayed material procurement and lead time overruns:"),
        ("IMP3", "Impact on buyer relationship trust and frequency of price dispute claims:"),
        ("IMP4", "Frequency of emergency air-shipment costs incurred due to poor initial budgeting:")
    ]
    
    for code, text in grading_questions:
        survey_responses[code] = st.radio(
            f"[{code}] {text}",
            options=[1, 2, 3, 4, 5],
            index=0,
            horizontal=True,
            key=code
        )
    st.divider()

    # ==========================================
    # PART 4: SLIDER QUESTIONS
    # ==========================================
    st.subheader("Part 4: Buyer Satisfaction & Order Execution Efficiency")
    part4_questions = [
        ("BS1", "Transparent and accurate pricing builds long-term strategic partnership with buyers."),
        ("BS2", "Accurate initial quotes and smooth execution lead to higher repeat order rates from buyers."),
        ("OE1", "Precise costing prevents material shortages and procurement delays on the factory floor."),
        ("OE2", "Costing accuracy directly contributes to achieving On-Time Delivery (OTD) targets consistently.")
    ]
    
    for code, text in part4_questions:
        survey_responses[code] = st.select_slider(
            f"[{code}] {text}",
            options=[0, 1, 2, 3, 4, 5],
            value=0,
            key=code
        )
    st.divider()

    # Render Dynamically Added Custom Questions from Admin
    if st.session_state.custom_questions:
        st.subheader("Additional / Custom Questions")
        for custom_q in st.session_state.custom_questions:
            code = custom_q["code"]
            text = custom_q["text"]
            q_type = custom_q.get("type", "Slider (0-5)")
            
            if q
