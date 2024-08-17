import streamlit as st
from utils import grammar_checker


st.set_page_config(layout="wide")
st.markdown("## 语法检查 Grammar Checker")

grammar_input = st.text_area("请输入你想修改的段落")
submit_first = st.button("开始修改 Revise")

if submit_first:
    with st.spinner("你的AI小助手正在努力工作嘤...Your AI assistant is working..."):
        grammar_gpt, grammar_gemini, grammar_claude  = grammar_checker(grammar_input)
        gpt_col, gemini_col, claude_col = st.tabs(["GPT version","Gemini version", "Claude version"])
        with gpt_col:
            st.markdown("#### GPT Version:")
            st.markdown(grammar_gpt)
        with gemini_col:
            st.markdown("#### Gemini Version:")
            st.markdown(grammar_gemini)
        with claude_col:
            st.markdown("#### Claude Version:")
            st.markdown(grammar_claude)
