import streamlit as st
import datetime
from langchain.memory import ConversationBufferMemory
from utils import generate_resume_content, generate_date, get_chat_response

st.set_page_config(layout="wide")

resume_assistant, blank, chat_assistant = st.columns([2,0.1,1])
with resume_assistant:
    st.title("简历生成助手 ResumeCraft AI Assistant")
    # Initialize or retrieve the selected model from session state
    if 'selected_model' not in st.session_state:
        st.session_state['selected_model'] = 'gemini'  # Default model

    with st.expander("请选择使用的语言模型 Please choose the language model you'd like to use："):
        proposed_model = st.radio("", ["gpt-3.5", "gemini"], 
                                index=["gpt-3.5", "gemini"].index(st.session_state['selected_model']))
        if st.button('选择 Select'):
            st.session_state['selected_model'] = proposed_model  # Update the session state only when button is clicked

    st.write("当前选择的模型是 The selected model is：", st.session_state['selected_model'])

    st.divider()
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
        submitted = st.form_submit_button("生成科研经历 Generate")
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
            resume_experience = generate_resume_content(resume_data, st.session_state['selected_model'])
            st.session_state['generated_experience'] = resume_experience
        
    if 'generated_experience' in st.session_state:
        st.markdown("#### 生成结果 Output")
        st.markdown(st.session_state['generated_experience'])
            

with chat_assistant:
    with st.expander("💬 随行聊天小助手 ChatMate AI"):
       
        if "memory" not in st.session_state:
            st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
            st.session_state["messages"] = [{"role": "ai",
                                            "content": "你好，我是你的AI助手，有什么可以帮你的吗？\n Hey there! I'm your AI assistant. What can I help you with today?"}]

        for message in st.session_state["messages"]:
            st.chat_message(message["role"]).write(message["content"])

        prompt = st.chat_input()
        if prompt:
            
            st.session_state["messages"].append({"role": "human", "content": prompt})
            st.chat_message("human").write(prompt)

            with st.spinner("你的AI小助手正在思考嘤，请稍等...Your AI assistant is working..."):
                response = get_chat_response(prompt, st.session_state["memory"],st.session_state['selected_model'])
            msg = {"role": "ai", "content": response}
            st.session_state["messages"].append(msg)
            st.chat_message("ai").write(response)

        if st.button("清空聊天 Clear"):
            # Reset the chat messages
            st.session_state["messages"] = [{"role": "ai", "content": "聊天历史已清空，重新开始对话。Chat history cleared! Let's start a new conversation. "}]
            st.rerun()  