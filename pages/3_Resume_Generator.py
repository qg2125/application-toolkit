import streamlit as st
import datetime
from langchain.memory import ConversationBufferMemory
from utils import generate_resume_content, generate_date, get_chat_response

st.set_page_config(layout="wide")



st.title("简历生成助手 ResumeCraft AI Assistant")



st.subheader("🗓️ 日期生成 Date formatting")
start, end, date_format = st.columns(3)
with start:
    start_date = st.date_input("请选择开始时间Start date", datetime.date(2024, 1, 1))
with end:
    end_date = st.date_input("请选择结束时间End date", datetime.date(2024, 1, 1))
with date_format:
    format_selection = st.selectbox("请选择生成的日期格式Date formats", ["缩写Abbrev.", "全拼Full"])


submit_date = st.button("生成日期 Generate")
if submit_date: 
    correct_date = generate_date(start_date,end_date, format_selection)
    st.session_state['generated_date']=correct_date
if 'generated_date' in st.session_state:
    st.write(st.session_state['generated_date'])

#-------------------------------------------------------------
st.divider()
st.subheader("📝 经历生成 Generating experience")

with st.form("my_form"):
    Date = st.write("请先使用上面的工具生成符合格式的日期 👆🏻") if 'generated_date' not in st.session_state else st.session_state['generated_date']
    ResearchTitle = st.text_input("Research title (only used for research exeprience)")
    Role = st.text_input("Your role, such as Undergraduate Research Assistant, Machine Learning Intern")
    Institution = st.text_input("Company, institution, organization, or university")
    Location = st.text_input("Location")
    # Ensure Date is initialized somewhere in your app, e.g., in a date picker input
    Advisor = st.text_input("Your advisor (only used for research exeprience)")
    Experience = st.text_area("复制或者输入经历的描述（中英文夹杂没关系，语言支离破碎也没关系），拉拽文本框的右下角增加文本框长度。Go ahead and paste or type out your experiences — it's totally fine if it's a mix of English and Chinese. Drag the bottom right corner of the text box to expand it as needed!")
    
    # Every form must have a submit button.
    submitted = st.form_submit_button("生成经历 Generate")
if submitted:
    resume_data = {
        'ResearchTitle': ResearchTitle,
        'Role': Role,
        'Institution': Institution,
        'Location': Location,
        'Date': Date,
        'Advisor': Advisor,
        'Experience': Experience
    }
    with st.spinner("你的AI小助手正在努力工作嘤...Your AI assistant is working..."):
        resume_gpt, resume_gemini, resume_claude  = generate_resume_content(resume_data)
        st.session_state['generated_experience'] = (resume_gpt, resume_gemini, resume_claude)
    
if 'generated_experience' in st.session_state:
    
    gpt_col, blank1, gemini_col, blank2, claude_col = st.columns([2, 0.05, 2, 0.05, 2])
    with gpt_col:
        st.markdown("#### GPT Version:")
        st.write(st.session_state['generated_experience'][0])
    with blank1:
        st.html(
            '''
                <div class="divider-vertical-line"></div>
                <style>
                    .divider-vertical-line {
                        border-left: 2px solid rgba(49, 51, 63, 0.2);
                        height: 800px;
                        margin: auto;
                    }
                </style>
            '''
        )
    with gemini_col:
        st.markdown("#### Gemini Version:")
        st.write(st.session_state['generated_experience'][1])
    with blank2:
        st.html(
            '''
                <div class="divider-vertical-line"></div>
                <style>
                    .divider-vertical-line {
                        border-left: 2px solid rgba(49, 51, 63, 0.2);
                        height: 800px;
                        margin: auto;
                    }
                </style>
            '''
        )
    with claude_col:
        st.markdown("#### Claude Version:")
        st.write(st.session_state['generated_experience'][2])

    

