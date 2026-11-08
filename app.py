import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Page Config
st.set_page_config(
    page_title="RMG Costing Accuracy Survey & Admin Portal",
    page_icon="📋",
    layout="wide"
)

# Google Sheets Connection using gspread & secrets with automated key cleaning
def get_gsheet_client():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    raw_key = st.secrets["connections"]["gsheets"]["private_key"]
    if "\\n" in raw_key:
        formatted_key = raw_key.replace("\\n", "\n")
    else:
        formatted_key = raw_key

    creds_dict = {
        "type": st.secrets["connections"]["gsheets"]["type"],
        "project_id": st.secrets["connections"]["gsheets"]["project_id"],
        "private_key_id": st.secrets["connections"]["gsheets"]["private_key_id"],
        "private_key": formatted_key,
        "client_email": st.secrets["connections"]["gsheets"]["client_email"],
        "client_id": st.secrets["connections"]["gsheets"]["client_id"],
        "auth_uri": st.secrets["connections"]["gsheets"]["auth_uri"],
        "token_uri": st.secrets["connections"]["gsheets"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["connections"]["gsheets"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["connections"]["gsheets"]["client_x509_cert_url"],
        "universe_domain": st.secrets["connections"]["gsheets"].get("universe_domain", "googleapis.com")
    }
    
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    return client

# Spreadsheet URL
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1UnDMS2Ko5XGS8Fu4CugtV1lKhCTNQ8BVKEA5HCGmPFQ/edit"

def load_data_from_sheet():
    try:
        client = get_gsheet_client()
        sheet = client.open_by_url(SPREADSHEET_URL).sheet1
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        return pd.DataFrame()

def save_data_to_sheet(new_row_df):
    try:
        client = get_gsheet_client()
        sheet = client.open_by_url(SPREADSHEET_URL).sheet1
        
        # Convert numpy types (int64, float64) to native python types to fix JSON serialization error
        raw_values = [val.item() if hasattr(val, "item") else val for val in new_row_df.iloc[0]]
        row_values = ["" if pd.isna(v) else v for v in raw_values]
        
        sheet.append_row(row_values)
        return True
    except Exception as e:
        st.error(f"Error saving to Google Sheets: {e}")
        return False

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

# Scale & Coding Legend in Sidebar
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

# IF ADMIN IS LOGGED IN, SHOW ADMIN CONTROLS
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
# MAIN SURVEY FORM
# ==========================================
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

# PART 1: SLIDER QUESTIONS
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

# PART 2: CHECKBOX QUESTIONS
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

# PART 3: GRADING SCALE
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

# PART 4: SLIDER QUESTIONS
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

# Dynamic Custom Questions Injection
if st.session_state.custom_questions:
    st.subheader("Additional / Custom Questions")
    for custom_q in st.session_state.custom_questions:
        code = custom_q["code"]
        text = custom_q["text"]
        q_type = custom_q.get("type", "Slider (0-5)")
        
        if q_type == "Slider (0-5)":
            survey_responses[code] = st.select_slider(
                f"[{code}] {text}",
                options=[0, 1, 2, 3, 4, 5],
                value=0,
                key=code
            )
        elif q_type == "Grading Scale (1-5)":
            survey_responses[code] = st.radio(
                f"[{code}] {text}",
                options=[1, 2, 3, 4, 5],
                index=0,
                horizontal=True,
                key=code
            )
        elif q_type == "Checkbox":
            checkbox_responses[code] = st.checkbox(
                f"[{code}] {text}",
                key=code
            )
    st.divider()

# SECTION C: QUALITATIVE FEEDBACK & SUBMIT
st.header("SECTION C: Open-Ended / Qualitative Feedback")
q_challenges = st.text_area("1. What are the major challenges you face while preparing pre-costing sheets for complex garment styles?")
q_erp = st.text_area("2. How does your factory leverage digital tools to improve overall cost efficiency?")

submit_button = st.button("🚀 Submit Survey Response", type="primary")

# ==========================================
# DATA SAVING TO GOOGLE SHEETS
# ==========================================
if submit_button:
    response_data = {
        "Factory Type": factory_type,
        "Position": position,
        "Experience": experience,
        "Turnover": turnover,
        **survey_responses,
        **{k: (1 if v else 0) for k, v in checkbox_responses.items()},
        "Challenges": q_challenges,
        "ERP Usage": q_erp
    }
    
    new_df = pd.DataFrame([response_data])
    if save_data_to_sheet(new_df):
        st.balloons()
        st.success("ধন্যবাদ! আপনার সার্ভে রেসপন্স সফলভাবে গুগল শিটসে সংরক্ষিত হয়েছে।")

# ==========================================
# ADMIN DASHBOARD & DATA DELETION
# ==========================================
if st.session_state.is_admin:
    st.divider()
    st.header("📊 Admin Dashboard & Data Export")
    
    df_saved = load_data_from_sheet()
    if not df_saved.empty:
        st.metric(label="Total Survey Responses Collected", value=len(df_saved))
        
        st.subheader("Live Response Data Preview (Google Sheets):")
        st.dataframe(df_saved, use_container_width=True)
        
        # CSV Download Option
        csv_data = df_saved.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Survey Responses as CSV",
            data=csv_data,
            file_name="rmg_costing_survey_responses.csv",
            mime="text/csv",
            type="primary"
        )
    else:
        st.warning("No survey responses recorded yet or unable to connect to Google Sheet.")
