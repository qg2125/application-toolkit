import streamlit as st
from utils import generate_para


st.set_page_config(layout="wide")
st.markdown("## 文书段落修改 Paragraph Editor")

if 'para_input' not in st.session_state:
    st.session_state['para_input'] = ''
if 'requirements' not in st.session_state:
    st.session_state['requirements'] = ''
if 'major' not in st.session_state:
    st.session_state['major'] = ''
if 'language' not in st.session_state:
    st.session_state['language'] = ''
if 'l_min' not in st.session_state:
    st.session_state['l_min'] = ''
if 'l_max' not in st.session_state:
    st.session_state['l_max'] = ''
if 'para_gpt' not in st.session_state:
    st.session_state['para_gpt'] = ''
if 'para_gemini' not in st.session_state:
    st.session_state['para_gemini'] = ''
if 'para_claude' not in st.session_state:
    st.session_state['para_claude'] = ''
if 'downloads' not in st.session_state:
    st.session_state['downloads'] = ''


st.session_state['para_input'] = st.text_area("请输入你想修改的文书段落")
st.session_state['requirements'] = st.text_input("请输入具体的修改要求")
st.session_state['major'] = st.text_input("请输入是什么专业的文书内容")
st.session_state['language'] = st.text_input("输出内容的语言（中文？英文？）")
st.session_state['l_min'] = st.text_input("请输入段落长度的最小值")
st.session_state['l_max'] = st.text_input("请输入段落长度的最大值")
submit_first = st.button("修改段落 Revise")

st.download_button(label="一键下载生成内容 Download", data=st.session_state['downloads'], file_name="my_results.txt")
st.session_state['downloads'] = "-----------chatgpt version-----------\n"+st.session_state['para_gpt'] + "\n\n\n\n\n-----------gemini version-----------\n"+st.session_state['para_gemini'] + "\n\n\n\n\n-----------claude version-----------\n"+st.session_state['para_claude']
if submit_first:
    with st.spinner("你的AI小助手正在努力工作嘤...Your AI assistant is working..."):
        st.session_state['para_gpt'], st.session_state['para_gemini'], st.session_state['para_claude']  = generate_para(st.session_state['para_input'], st.session_state['requirements'], st.session_state['major'],st.session_state['language'],st.session_state['l_min'],st.session_state['l_max'])

gpt_col, gemini_col, claude_col = st.columns([2, 2, 2])
if st.session_state['para_gpt']:
    with gpt_col:
        st.markdown("#### GPT Version:")
        st.write(st.session_state['para_gpt'])
if st.session_state['para_gemini']:
    with gemini_col:
        st.markdown("#### Gemini Version:")
        st.write(st.session_state['para_gemini'])
if st.session_state['para_claude']:
    with claude_col:
        st.markdown("#### Claude Version:")
        st.write(st.session_state['para_claude'])
