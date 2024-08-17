import streamlit as st
from utils import reply_email


st.set_page_config(layout="wide")
st.markdown("## 邮件内容生成 Email Writer")

previous_email = st.text_area("请把之前的往来的邮件内容复制到这里")
email_reply = st.text_area("请输入你想回复的内容是什么")
email_style = st.text_input("请描述希望生成的邮件风格，比如希望写得正式一些，更口语化一些，更简洁一些")
submit_first = st.button("生成邮件 Generate")

if submit_first:
    with st.spinner("你的AI小助手正在努力工作嘤...Your AI assistant is working..."):
        email_gpt, email_gemini  = reply_email(previous_email, email_reply, email_style)
        gpt_col, blank, gemini_col = st.columns([1,0.2,1])
        with gpt_col:
            st.markdown("#### GPT Version:")
            st.write(email_gpt)
        with gemini_col:
            st.markdown("#### Gemini Version:")
            st.write(email_gemini)
        
