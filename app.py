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
        new_q_text = st.text_area("Question Statement (English & বাংলা):", placeholder="Enter statement with Bengali translation...")
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
        factory_type = st.selectbox("1. Type of Factory / Organization (কারখানার ধরণ):", ["Knitwear", "Woven", "Sweater", "Denim/Bottoms", "Buying House"])
        position = st.selectbox("2. Your Current Position/Role (আপনার বর্তমান পদবী):", ["Merchandiser / Assistant Merchandiser", "Senior Merchandiser / Manager", "Head of Merchandising / Director", "Costing & Pricing Analyst"])
    with col2:
        experience = st.selectbox("3. Total Years of Experience in RMG Merchandising (কাজের অভিজ্ঞতা):", ["1–3 years", "4–7 years", "8–12 years", "12+ years"])
        turnover = st.selectbox("4. Annual Export Turnover (USD) (বার্ষিক রপ্তানি টার্নওভার):", ["Less than $5 Million", "$5M - $15M", "$15M - $30M", "Above $30M"])
        
    st.divider()
    
    st.header("SECTION B: Core Research Variables (মূল গবেষণা ভেরিয়েবল)")
    
    # Scale Coding Legend (নিয়ন্ত্রণ ও কোডিং গাইড)
    st.info("""
    **📊 Scale & Coding Legend (কোডিং নির্দেশিকা):**
    * **Slider Scale (0-5):** 0 = Not Applicable / Strongly Disagree (প্রযোজ্য নয় / তীব্র দ্বিমত), 1 = Disagree (দ্বিমত), 2 = Neutral (নিরপেক্ষ), 3 = Agree (সম্মত), 4 = Strongly Agree (দৃঢ়ভাবে সম্মত), 5 = Highly Significant (অত্যন্ত তাৎপর্যপূর্ণ)
    * **Grading Scale (1-5):** 1 = Low Impact / Dislike (কম প্রভাব / অপছন্দ), 2 = Moderate (মাঝারি), 3 = High (উচ্চ), 4 = Severe (তীব্র), 5 = Critical / Destructive (মারাত্মক)
    * **Checkbox:** Selected = 1 (হ্যাঁ / সক্রিয়), Unselected = 0 (না / নিষ্ক্রিয়)
    """)
    
    survey_responses = {}
    checkbox_responses = {}

    # ==========================================
    # PART 1: SLIDER QUESTIONS
    # ==========================================
    st.subheader("Part 1: Costing Accuracy & Pre-Calculation (কস্টিং সঠিকতা ও প্রাক-হিসাব)")
    part1_questions = [
        ("CA1", "Our pre-costing accurately reflects actual production costs (fabric consumption, trims, CM, logistics). (আমাদের প্রাক-কস্টিং প্রকৃত উৎপাদন খরচ নিখুঁতভাবে প্রতিফলন করে।)"),
        ("CA2", "We systematically account for fabric waste, shrinkage, and buffer margins in our cost sheets. (আমরা কস্ট শিটে ফেব্রিক ওয়েস্টেজ, সংকোচন এবং বাফার মার্জিন হিসাব করি।)"),
        ("CA3", "Post-costing variance analysis is regularly conducted after shipment to evaluate estimation errors. (শিপমেন্টের পর অনুমান ত্রুটি মূল্যায়নের জন্য নিয়মিত পোস্ট-কস্টিং বিশ্লেষণ করা হয়।)"),
        ("CA4", "Material price volatility (yarn, dyes, accessories) is well-predicted and integrated into quotes. (কাঁচামালের মূল্য ওঠানামা সঠিকভাবে পূর্বাভাস দিয়ে কোটেশনে যুক্ত করা হয়।)")
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
    st.subheader("Part 2: Costing Tools & Strategies Used (কস্টিং টুলস ও কৌশল - Checkboxes)")
    st.write("Select all tools, software, or strategies your factory regularly utilizes: (আপনার কারখানায় ব্যবহৃত টুলস ও কৌশলগুলো সিলেক্ট করুন)")
    
    tool_options = {
        "TOOL_EXCEL": "Advanced Excel-based Costing Models & Macros (উন্নত এক্সেলভিত্তিক কস্টিং মডেল ও ম্যাক্রোস)",
        "TOOL_ERP": "Enterprise Resource Planning (ERP) Software e.g., SAP, BlueCherry (ইআরপি সফটওয়্যার যেমন- SAP, BlueCherry)",
        "TOOL_CAD": "Automated CAD Marker & Fabric Consumption Calculators (অটোমেটেড সিএডি ও ফেব্রিক কনজাম্পশন ক্যালকুলেটর)",
        "TOOL_AI": "AI-driven or Predictive Costing Tools (এআই বা ভবিষ্যৎ পূর্বাভাসভিত্তিক কস্টিং টুল)",
        "TOOL_HISTORICAL": "Historical Database of Past Orders for Benchmarking (পূর্ববর্তী অর্ডারের হিস্টোরিকাল ডাটাবেস)",
        "TOOL_BUFFER": "Standardized Buffer Pricing for Raw Material Fluctuations (কাঁচামাল ওঠানামার জন্য বাফার প্রাইসিং)"
    }
    
    for key, label in tool_options.items():
        checkbox_responses[key] = st.checkbox(label, key=key)
    st.divider()

    # ==========================================
    # PART 3: GRADING SCALE (RADIO BUTTONS)
    # ==========================================
    st.subheader("Part 3: Impact of Costing Errors on Factory Performance (কস্টিং ভুলের প্রভাব - Grading Scale)")
    grading_questions = [
        ("IMP1", "Impact of inaccurate costing on unexpected profit/margin loss: (অনির্দিষ্ট কস্টিংয়ের কারণে অপ্রত্যাশিত প্রফিট বা মার্জিন হ্রাসের প্রভাব)"),
        ("IMP2", "Impact of costing mistakes on delayed material procurement and lead time overruns: (কস্টিং ভুলের কারণে কাঁচামাল সংগ্রহে বিলম্ব ও লিড টাইম ওভাররানের প্রভাব)"),
        ("IMP3", "Impact on buyer relationship trust and frequency of price dispute claims: (বায়েদের সাথে আস্থার সম্পর্ক এবং মূল্য বিরোধের দাবির প্রভাব)"),
        ("IMP4", "Frequency of emergency air-shipment costs incurred due to poor initial budgeting: (প্রাথমিক বাজেটিংয়ের ত্রুটির কারণে জরুরি এয়ার শিপমেন্ট খরচ)")
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
    st.subheader("Part 4: Buyer Satisfaction & Order Execution Efficiency (বায়ার সন্তুষ্টি ও অর্ডার এক্সিকিউশন দক্ষতা)")
    part4_questions = [
        ("BS1", "Transparent and accurate pricing builds long-term strategic partnership with buyers. (স্বচ্ছ ও নির্ভুল মূল্য নির্ধারণ দীর্ঘমেয়াদী অংশীদারিত্ব তৈরি করে।)"),
        ("BS2", "Accurate initial quotes and smooth execution lead to higher repeat order rates from buyers. (নির্ভুল প্রারম্ভিক কোটেশন রি-অর্ডার বৃদ্ধিতে সহায়তা করে।)"),
        ("OE1", "Precise costing prevents material shortages and procurement delays on the factory floor. (নির্ভুল কস্টিং কারখানায় কাঁচামালের ঘাটতি ও সংগ্রহ বিলম্ব রোধ করে।)"),
        ("OE2", "Costing accuracy directly contributes to achieving On-Time Delivery (OTD) targets consistently. (কস্টিং সঠিকতা অন-টাইম ডেলিভারি (OTD) লক্ষ্য অর্জনে সরাসরি অবদান রাখে।)")
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
        st.subheader("Additional / Custom Questions (অতিরিক্ত প্রশ্নসমূহ)")
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

    # ==========================================
    # SECTION C: QUALITATIVE FEEDBACK
    # ==========================================
    st.header("SECTION C: Open-Ended / Qualitative Feedback (গুণগত ফিডব্যাক)")
    q_challenges = st.text_area("1. What are the major challenges you face while preparing pre-costing sheets for complex garment styles? (জটিল স্টাইলের কস্টিং তৈরিতে প্রধান চ্যালেঞ্জগুলো কী?)")
    q_erp = st.text_area("2. How does your factory leverage digital tools to improve overall cost efficiency? (আপনার কারখানা কীভাবে ডিজিটাল টুলস ব্যবহার করে?)")
    
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
        **survey_responses,
        **{k: (1 if v else 0) for k, v in checkbox_responses.items()},
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
