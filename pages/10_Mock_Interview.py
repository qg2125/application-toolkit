import streamlit as st
from utils import get_random_question, interview_tips, interview_evaluation

st.set_page_config(layout="wide")

st.title("模拟面试助手")
st.subheader("哥大工学院面试")

if 'current_question' not in st.session_state:
    st.session_state.current_question = ""
if 'tip' not in st.session_state:
    st.session_state.tip = ""
if 'evaluation' not in st.session_state:
    st.session_state.evaluation = ""

if st.button("随机生成题目 Generate"):
    st.session_state.current_question = get_random_question()
    st.session_state.tip = ""
    st.session_state.evaluation = ""  # 清除上次的评估结果

if st.session_state.current_question:
    st.write("---")
    st.write("### 当前问题:")
    st.write(st.session_state.current_question)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("我没思路"):
            with st.spinner("你的AI小助手正在努力工作嘤...Your AI assistant is working..."):
                st.session_state.tip = interview_tips(st.session_state.current_question)
        
        if st.session_state.tip:
            st.write("提示:")
            st.write(st.session_state.tip)

    with col2:
        user_answer = st.text_area("在此输入你的答案", "")


        # 评估用户答案按钮
        if st.button("评估我的答案"):
            with st.spinner("你的AI小助手正在努力工作嘤...Your AI assistant is working..."):
                if user_answer.strip():  # 如果用户输入不为空
                    st.session_state.evaluation = interview_evaluation(st.session_state.current_question, user_answer)
                else:
                    st.write("请输入答案后再进行评估。")

        if st.session_state.evaluation:
            st.write("评估结果:")
            st.write(st.session_state.evaluation)
