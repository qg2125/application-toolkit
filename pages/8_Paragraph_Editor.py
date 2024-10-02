import streamlit as st
from utils import generate_para

st.set_page_config(layout="wide")
st.markdown("## 文书段落修改 Paragraph Editor")

# Initialize session state variables
state_variables = ['para_input', 'requirements', 'major', 'language', 'l_min', 'l_max', 'para_gpt', 'para_gemini', 'para_claude', 'downloads']
for var in state_variables:
    if var not in st.session_state:
        st.session_state[var] = ''

# Input fields
st.session_state['para_input'] = st.text_area("请输入你想修改的文书段落")
st.session_state['requirements'] = st.text_input("请输入具体的修改要求")
st.session_state['major'] = st.text_input("请输入是什么专业的文书内容")
st.session_state['language'] = st.text_input("输出内容的语言（中文？英文？）")
st.session_state['l_min'] = st.text_input("请输入段落长度的最小值")
st.session_state['l_max'] = st.text_input("请输入段落长度的最大值")
submit_first = st.button("修改段落 Revise")

if submit_first:
    with st.spinner("你的AI小助手正在努力工作嘤...Your AI assistant is working..."):
        # Generate the content
        gpt_para, gemini_para, claude_para = generate_para(
            st.session_state['para_input'],
            st.session_state['requirements'],
            st.session_state['major'],
            st.session_state['language'],
            st.session_state['l_min'],
            st.session_state['l_max']
        )

        # Update session state with generated content
        st.session_state['para_gpt'] = gpt_para
        st.session_state['para_gemini'] = gemini_para
        st.session_state['para_claude'] = claude_para
        
        # Concatenate and update downloads content
        st.session_state['downloads'] = (
            "-----------chatgpt version-----------\n" + st.session_state['para_gpt'] + "\n\n\n\n\n"
            "-----------gemini version-----------\n" + st.session_state['para_gemini'] + "\n\n\n\n\n"
            "-----------claude version-----------\n" + st.session_state['para_claude']
        )

if st.session_state['downloads']:
    st.download_button(label="一键下载生成内容 Download", data=st.session_state['downloads'], file_name="my_results.txt")

# Display the generated content
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

# Download button for the concatenated content

