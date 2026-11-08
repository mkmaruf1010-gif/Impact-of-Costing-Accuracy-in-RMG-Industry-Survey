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
# SIDEBAR: ADMIN LOGIN & PANEL
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

# IF ADMIN IS LOGGED IN, SHOW ADMIN CONTROLS & DASHBOARD
if st.session_state.is_admin:
    st.sidebar.divider()
    st.sidebar.header("🛠️ Dynamic Question System")
    
    with st.sidebar.form("add_question_form", clear_on_submit=True):
        new_q_code = st.text_input("Question Code (e.g., CA6, MP5):", placeholder="CA6")
        new_q_text = st.text_area("Question Statement:", placeholder="Enter statement here...")
        new_q_section = st.selectbox(
            "Select Section:",
            [
                "Part 1: Costing Accuracy (Independent Variable)",
                "Part 2: Merchandising Performance (Dependent Variable)",
                "Part 3: Factory Profitability (Dependent Variable)",
                "Part 4: Buyer Satisfaction & Retention (Dependent Variable)",
                "Part 5: Order Execution Efficiency (Dependent Variable)",
                "Part 6: Digital ERP & Moderating Factors"
            ]
        )
        add_btn = st.form_submit_button("➕ Add Question")

        if add_btn:
            if new_q_code and new_q_text:
                st.session_state.custom_questions.append({
                    "code": new_q_code,
                    "text": new_q_text,
                    "section": new_q_section
                })
                st.sidebar.success(f"Question '{new_q_code}' added successfully!")
            else:
                st.sidebar.error("Please fill in both Code and Statement.")

    if st.session_state.custom_questions:
        st.sidebar.markdown("---")
        st.sidebar.subheader("Added Custom Questions:")
        for q in st.session_state.custom_questions:
            st.sidebar.caption(f"**[{q['code']}]** {q['text']}")
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
    
    st.header("SECTION B: Core Research Variables (Advanced Regression Scale)")
    st.info("Scale: 0 = Not Applicable / Strongly Disagree, 1 = Disagree, 2 = Neutral, 3 = Agree, 4 = Strongly Agree, 5 = Highly Significant")
    
    # Expanded sections with comprehensive questions for robust regression & factor analysis
    sections_dict = {
        "Part 1: Costing Accuracy (Independent Variable)": [
            ("CA1", "Our pre-costing accurately reflects actual production costs (fabric consumption, trims, CM, logistics)."),
            ("CA2", "We systematically account for fabric waste, shrinkage, and buffer margins in our cost sheets."),
            ("CA3", "Post-costing variance analysis is regularly conducted after shipment to evaluate estimation errors."),
            ("CA4", "Material price volatility (yarn, Dyes, accessories) is well-predicted and integrated into our quotes."),
            ("CA5", "We apply scientific consumption formulas rather than traditional approximations during costing.")
        ],
        "Part 2: Merchandising Performance (Dependent Variable)": [
            ("MP1", "Accurate costing helps me negotiate better price points with buyers without losing the order."),
            ("MP2", "Precise cost sheets reduce internal conflicts between management, production, and merchandising teams."),
            ("MP3", "I can finalize T&A (Time and Action) calendars much smoother when costing and material budgets are precise."),
            ("MP4", "Costing accuracy reduces my stress levels and enhances my daily operational decision-making efficiency."),
            ("MP5", "Accurate costing enables faster quotation generation and response times to buyer inquiries.")
        ],
        "Part 3: Factory Profitability (Dependent Variable)": [
            ("FP1", "Accurate costing directly minimizes unexpected budget overruns and hidden losses during order execution."),
            ("FP2", "We rarely face unexpected negative margins or financial penalties due to costing errors."),
            ("FP3", "Precise margin calculation significantly improves the overall net profit margin and financial health of our factory."),
            ("FP4", "Cost accuracy optimization has lowered our overall operational cost wastage over the past year.")
        ],
        "Part 4: Buyer Satisfaction & Retention (Dependent Variable)": [
            ("BS1", "Transparent and accurate pricing builds long-term trust and strategic partnership with international buyers."),
            ("BS2", "We experience fewer financial disputes or post-order price adjustment claims from buyers."),
            ("BS3", "Accurate initial quotes and smooth execution lead to higher repeat order rates (re-orders) from buyers."),
            ("BS4", "Buyer audit ratings on our pricing transparency and compliance have improved due to accurate cost documentation.")
        ],
        "Part 5: Order Execution Efficiency (Dependent Variable)": [
            ("OE1", "Precise costing prevents material procurement shortages and delays in the factory floor."),
            ("OE2", "We rarely need to use expensive air freight for delayed raw materials because material budgets are properly managed."),
            ("OE3", "Costing accuracy directly contributes to achieving On-Time Delivery (OTD) targets consistently."),
            ("OE4", "Production efficiency increases because material approvals align seamlessly with the financial budget.")
        ],
        "Part 6: Digital ERP & Moderating Factors": [
            ("MOD1", "Our factory utilizes advanced ERP software or digital automated tools for costing and inventory tracking."),
            ("MOD2", "Top management provides adequate training and resources for advanced cost estimation practices."),
            ("MOD3", "Market volatility (external economic shocks, inflation) heavily disrupts our standard costing accuracy.")
        ]
    }
    
    # Append custom questions dynamically if added by admin
    for custom_q in st.session_state.custom_questions:
        sec = custom_q["section"]
        if sec in sections_dict:
            sections_dict[sec].append((custom_q["code"], custom_q["text"]))

    likert_responses = {}
    for section_title, questions in sections_dict.items():
        st.subheader(section_title)
        for code, text in questions:
            label_text = f"[{code}] {text}"
            # Slider default value is set to 0 as requested ("জিরোতে থাকবে")
            likert_responses[code] = st.select_slider(
                label_text,
                options=[0, 1, 2, 3, 4, 5],
                value=0,
                key=code
            )
        st.divider()
        
    st.header("SECTION C: Open-Ended / Qualitative Feedback")
    q_challenges = st.text_area("1. What are the major challenges you face while preparing pre-costing sheets for complex garment styles?")
    q_erp = st.text_area("2. How does your factory leverage digital tools (like ERP software or advanced Excel models) to improve costing accuracy?")
    
    submit_button = st.form_submit_button("🚀 Submit Survey Response", type="primary")

# ==========================================
# DATA SAVING LOGIC
# ==========================================
if submit_button:
    response_data = {
        "Factory Type": factory_type,
        "Position": position,
        "Experience": experience,
        "Turnover": turnover,
        **likert_responses,
        "Challenges": q_challenges,
        "ERP Usage": q_erp
    }
    
    new_df = pd.DataFrame([response_data])
    
    if not os.path.isfile(DATA_FILE):
        new_df.to_csv(DATA_FILE, index=False)
    else:
        new_df.to_csv(DATA_FILE, mode='a', header=False, index=False)
        
    st.balloons()
    st.success("ধন্যবাদ! আপনার সার্ভে রেসপন্স সফলভাবে সংরক্ষিত হয়েছে।")

# ==========================================
# ADMIN DASHBOARD (LOCKED UNLESS AUTHENTICATED)
# ==========================================
if st.session_state.is_admin:
    st.divider()
    st.header("📊 Admin Dashboard & Data Export")
    
    if os.path.exists(DATA_FILE):
        df_saved = pd.read_csv(DATA_FILE)
        st.metric(label="Total Survey Responses Collected", value=len(df_saved))
        
        st.subheader("Live Response Data Preview:")
        st.dataframe(df_saved, use_container_width=True)
        
        csv_data = df_saved.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Survey Responses as CSV",
            data=csv_data,
            file_name="rmg_costing_survey_responses.csv",
            mime="text/csv",
            type="primary"
        )
    else:
        st.warning("No survey responses recorded yet.")
