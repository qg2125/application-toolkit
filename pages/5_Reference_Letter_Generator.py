import streamlit as st
from utils import generate_rl_first

st.set_page_config(layout="wide")
st.markdown("## 推荐信内容生成 Reference Letter Generator")

state_variables = ['first_para_input', 'firstpara_gpt', 'firstpara_gemini', 'firstpara_claude', 'downloads']
for var in state_variables:
    if var not in st.session_state:
        st.session_state[var] = ''

# Input fields
st.session_state['first_para_input'] = st.text_area(
    "请输入被推荐人姓名，推荐人的相关信息，包括姓名、职位、公司或学校名称、和被推荐人的关系（例如科研指导老师，实习指导老师或者某门课程任课老师）、和被推荐人什么时候认识，想强调被推荐人的哪些优点和具体例子。",
    st.session_state['first_para_input']
)
submit_first = st.button("生成推荐信 Generate")

if submit_first:
    with st.spinner("你的AI小助手正在努力工作嘤...Your AI assistant is working..."):
        firstpara_gpt, firstpara_gemini, firstpara_claude = generate_rl_first(st.session_state['first_para_input'])
        st.session_state['firstpara_gpt'] = firstpara_gpt
        st.session_state['firstpara_gemini'] = firstpara_gemini
        st.session_state['firstpara_claude'] = firstpara_claude

        # Generate the download content
        st.session_state['downloads'] = (
            "-----------chatgpt version-----------\n" + firstpara_gpt + "\n\n\n\n\n"
            "-----------gemini version-----------\n" + firstpara_gemini + "\n\n\n\n\n"
            "-----------claude version-----------\n" + firstpara_claude
        )

        # Add a download button directly below the generation button
if 'downloads' in st.session_state and st.session_state['downloads']:
    st.download_button(
        label="下载推荐信 Download Letters",
        data=st.session_state['downloads'],
        file_name='recommendation_letters.txt',
        mime='text/plain'
    )

# Display the generated letters if they exist in the session state
if st.session_state['firstpara_gpt'] or st.session_state['firstpara_gemini'] or st.session_state['firstpara_claude']:
    gpt_col, gemini_col, claude_col = st.columns([2, 2, 2])
    with gpt_col:
        st.markdown("#### GPT Version:")
        st.write(st.session_state['firstpara_gpt'])
    with gemini_col:
        st.markdown("#### Gemini Version:")
        st.write(st.session_state['firstpara_gemini'])
    with claude_col:
        st.markdown("#### Claude Version:")
        st.write(st.session_state['firstpara_claude'])
