import streamlit as st
from utils import generate_rl_first

st.set_page_config(layout="wide")
st.markdown("## 推荐信内容生成 Reference Letter Generator")

first_para_input = st.text_area("请输入被推荐人姓名，推荐人的相关信息，包括姓名、职位、公司或学校名称、和被推荐人的关系（例如科研指导老师，实习指导老师或者某门课程任课老师）、和被推荐人什么时候认识，想强调被推荐人的哪些优点。")
submit_first = st.button("生成开头")

if submit_first:
    with st.spinner("你的AI小助手正在努力工作嘤...Your AI assistant is working..."):
        firstpara_gpt, firstpara_gemini, firstpara_claude  = generate_rl_first(first_para_input)
        gpt_col, gemini_col, claude_col = st.columns([2, 2, 2])
        with gpt_col:
            st.markdown("#### GPT Version:")
            st.write(firstpara_gpt)
        with gemini_col:
            st.markdown("#### Gemini Version:")
            st.write(firstpara_gemini)
        with claude_col:
            st.markdown("#### Claude Version:")
            st.write(firstpara_claude)


