import streamlit as st
from utils import generate_para


st.set_page_config(layout="wide")
st.markdown("## 文书段落修改 Paragraph Editor")

para_input = st.text_area("请输入你想修改的文书段落")
major = st.text_input("请输入是什么专业的文书内容")
language = st.text_input("输出内容的语言（中文？英文？）")
l_min = st.text_input("请输入段落长度的最小值")
l_max = st.text_input("请输入段落长度的最大值")
submit_first = st.button("修改段落 Revise")

if submit_first:
    with st.spinner("你的AI小助手正在努力工作嘤...Your AI assistant is working..."):
        para_gpt, para_gemini, para_claude  = generate_para(para_input, major,language,l_min,l_max)
        gpt_col, gemini_col, claude_col = st.columns([2, 2, 2])
        with gpt_col:
            st.markdown("#### GPT Version:")
            st.write(para_gpt)
        with gemini_col:
            st.markdown("#### Gemini Version:")
            st.write(para_gemini)
        with claude_col:
            st.markdown("#### Claude Version:")
            st.write(para_claude)
