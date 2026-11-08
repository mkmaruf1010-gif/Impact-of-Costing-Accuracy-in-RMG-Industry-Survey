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
st.markdown("""
*Academic Research Survey on Merchandising Performance, Profitability, Buyer Satisfaction, and Order Execution Efficiency.*
""")
st.divider()

# ==========================================
# SIDEBAR: ADMIN LOGIN & PANEL
# ==========================================
st.sidebar.header("🔐 Admin Portal Access")

# Password input
admin_password_input = st.sidebar.text_input("Enter Admin Password:", type="password", placeholder="Enter password...")

# Default admin password is set to "admin123" (You can change it here)
ADMIN_SECRET_KEY = "admin123"

if admin_password_input == ADMIN_SECRET_KEY:
    st.session_state.is_admin = True
    st.sidebar.success("🔓 Admin Access Granted!")
else:
    if admin_password_input:
        st.sidebar.error("❌ Incorrect Password!")
    st.session_state.is_admin = False

# IF ADMIN IS LOGGED IN, SHOW ADMIN CONTROLS & DASHBOARD
if st.session_state.is_admin:
    st.sidebar.divider()
    st.sidebar.header("🛠️ Dynamic Question System")
    
    with st.sidebar.form("add_question_form", clear_on_submit=True):
        new_q_code = st.text_input("Question Code (e.g., CA5, MP5):", placeholder="CA5")
        new_q_text = st.text_area("Question Statement:", placeholder="Enter statement here...")
        new_q_section = st.selectbox(
            "Select Section:",
            [
                "Part 1: Costing Accuracy",
                "Part 2: Merchandising Performance",
                "Part 3: Factory Profitability",
                "Part 4: Buyer Satisfaction & Retention",
                "Part 5: Order Execution Efficiency"
            ]
        )
        add_btn = st.form_submit_button("➕ Add Question")

        if add_btn:
            if new_q_code and new_q_text:
                st.session_state.custom_questions.append({
                    "code": new_q_code,
                    "text": new_q_text,
                    "section": new_q_section
                }) # <--- এখানে অতিরিক্ত '>' চিহ্নটি সরিয়ে ঠিক করা হয়েছে
                st.sidebar.success(f"Question '{new_q_code}' added successfully!")
            else:
                st.sidebar.error("Please fill in both Code and Statement.")

    if st.session_state.custom_questions:
        st.sidebar.markdown("---")
        st.sidebar.subheader("Added Custom Questions:")
        for q in st.session_state.custom_questions:
            st.sidebar.caption(f"**[{q['code']}]** {q['text']}")
else:
    st.sidebar.info("💡 Admin features (Adding questions & viewing data) are locked. Enter the correct password above to unlock.")

# ==========================================
# MAIN FORM (FOR RESPONDENTS)
# ==========================================
with st.form("rmg_survey_form"):
    
    st.header("SECTION A: Demographic & Organizational Profile")
    col1, col2 = st.columns(2)
    
    with col1:
        factory_type = st.selectbox(
            "1. Type of Factory / Organization:",
            ["Knitwear", "Woven", "Sweater", "Denim/Bottoms", "Buying House"]
        )
        position = st.selectbox(
            "2. Your Current Position/Role:",
            ["Merchandiser / Assistant Merchandiser", "Senior Merchandiser / Manager", "Head of Merchandising / Director", "Costing & Pricing Analyst"]
        )
    with col2:
        experience = st.selectbox(
            "3. Total Years of Experience in RMG Merchandising:",
            ["1–3 years", "4–7 years", "8–12 years", "12+ years"]
        )
        turnover = st.selectbox(
            "4. Annual Export Turnover (USD):",
            ["Less than $5 Million", "$5M - $15M", "$15M - $30M", "Above $30M"]
        )
        
    st.divider()
    
    st.header("SECTION B: Core Research Variables")
    st.info("Scale: 1 = Strongly Disagree, 2 = Disagree, 3 = Neutral, 4 = Agree, 5 = Strongly Agree")
    
    sections_dict = {
        "Part 1: Costing Accuracy": [
            ("CA1", "Our pre-costing accurately reflects actual production costs (fabric consumption, trims, CM, logistics)."),
            ("CA2", "We systematically account for fabric waste and buffer margins in our cost sheets."),
            ("CA3", "Post-costing analysis is regularly conducted after shipment to evaluate estimation errors."),
            ("CA4", "Material price volatility (yarn/accessories) is well-predicted and integrated into our quotes.")
        ],
        "Part 2: Merchandising Performance": [
            ("MP1", "Accurate costing helps me negotiate better with buyers without losing the order."),
            ("MP2", "Precise cost sheets reduce internal conflicts between management, production, and merchandising teams."),
            ("MP3", "I can finalize T&A (Time and Action) calendars much smoother when costing is precise."),
            ("MP4", "Costing accuracy reduces my stress levels and enhances my daily operational decision-making.")
        ],
        "Part 3: Factory Profitability": [
            ("FP1", "Accurate costing directly minimizes unexpected budget overruns during execution."),
            ("FP2", "We rarely face unexpected financial losses or negative margins due to costing errors."),
            ("FP3", "Precise margin calculation improves the overall financial health of our organization.")
        ],
        "Part 4: Buyer Satisfaction & Retention": [
            ("BS1", "Transparent and accurate pricing builds long-term trust with international buyers."),
            ("BS2", "We experience fewer disputes over post-order price adjustments or revisions."),
            ("BS3", "Accurate initial quotes lead to higher repeat orders (re-orders) from buyers.")
        ],
        "Part 5: Order Execution Efficiency": [
            ("OE1", "Precise costing prevents material shortages and procurement delays."),
            ("OE2", "We rarely need to use expensive air freight because material budgets are properly managed."),
            ("OE3", "Costing accuracy significantly contributes to achieving On-Time Delivery (OTD) targets.")
        ]
    }
    
    # Append custom questions dynamically
    for custom_q in st.session_state.custom_questions:
        sec = custom_q["section"]
        if sec in sections_dict:
            sections_dict[sec].append((custom_q["code"], custom_q["text"]))

    likert_responses = {}
    for section_title, questions in sections_dict.items():
        st.subheader(section_title)
        for code, text in questions:
            likert_responses[code] = st.select_slider(
                f"**[{code}]** {text}",
                options=[1, 2, 3, 4, 5],
                value=3,
                key=code
            )
        st.markdown
