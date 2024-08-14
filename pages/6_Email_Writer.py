import streamlit as st
from utils import generate_email


st.set_page_config(layout="wide")
st.markdown("## 邮件内容生成 Email Writer")

email_input = st.text_area("请输入你想把邮件发给谁，想写的邮件大概内容是什么")
email_style = st.text_input("请描述希望生成的邮件风格，比如希望写得正式一些，更口语化一些，更简洁一些")
submit_first = st.button("生成邮件 Generate")

if submit_first:
    with st.spinner("你的AI小助手正在努力工作嘤...Your AI assistant is working..."):
        email_gpt, email_gemini, email_claude  = generate_email(email_input, email_style)
        gpt_col, gemini_col, claude_col = st.columns([2, 2, 2])
        with gpt_col:
            st.markdown("#### GPT Version:")
            st.write(email_gpt)
        with gemini_col:
            st.markdown("#### Gemini Version:")
            st.write(email_gemini)
        with claude_col:
            st.markdown("#### Claude Version:")
            st.write(email_claude)
