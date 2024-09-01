import streamlit as st
from utils import generate_essay_toEnglish, generate_essay_toChinese

st.set_page_config(layout="wide")
st.title("文书翻译 Translation AI")
# Initialize session state if not already set
if 'selected_model' not in st.session_state:
    st.session_state['selected_model'] = 'gemini'  # Default model

if 'trans_1_input' not in st.session_state:
    st.session_state['trans_1_input'] = ''

if 'trans_1_result' not in st.session_state:
    st.session_state['trans_1_result'] = ''

if 'trans_2_input' not in st.session_state:
    st.session_state['trans_2_input'] = ''

if 'trans_2_result' not in st.session_state:
    st.session_state['trans_2_result'] = ''

# Model selection radio button
with st.expander("请选择使用的语言模型 Please choose the language model you'd like to use："):
    proposed_model = st.radio("", ["chatgpt", "gemini"], 
                            index=["chatgpt", "gemini"].index(st.session_state['selected_model']))
    if st.button('选择 Select'):
        st.session_state['selected_model'] = proposed_model  # Update the session state only when button is clicked

st.write("当前选择的模型是 The selected model is：", st.session_state['selected_model'])
st.divider()

tab1, tab2 = st.tabs(["中译英 Chinese to English","英译中 English to Chinese"])

with tab1:
    
    st.session_state['trans_1_input'] = st.text_area("复制或者输入需要翻译的文本（中文夹杂英文没关系，语言支离破碎也没关系），拉拽文本框的右下角增加文本框长度。Go ahead and paste or type out the text you want to translate — it's totally fine if it's a mix of English and Chinese. Drag the bottom right corner of the text box to expand it as needed!")
    st.session_state['trans_1_creativity'] = st.slider("请输入翻译后英文文本的创造力（数字小说明更严谨，数字大说明更多样更有创造性，默认值为1。Please enter a creativity value for the translated English text. A lower number means it's more precise, while a higher number indicates it's more diverse and creative. The default value is 1.）", min_value=0.5,
                       max_value=1.5, value=1.0, step=0.1)
    submit1 = st.button("翻译 To English")

    if submit1:
        with st.spinner("你的AI小助手正在努力工作嘤...Your AI translator is working..."):
            st.session_state['trans_1_result'] = generate_essay_toEnglish(st.session_state['trans_1_input'],st.session_state['trans_1_creativity'],st.session_state['selected_model'])
    if st.session_state['trans_1_input']:
        st.divider()
        left,right = st.columns(2)
        with left:
            st.markdown("#### 原文 Original Text")
            st.write(st.session_state['trans_1_input'])
        with right:
            st.markdown("#### 翻译后的文本 Translated text")
            st.write(st.session_state['trans_1_result'])
            st.download_button(label="一键下载生成内容 Download", data=st.session_state['trans_1_result'], file_name="my_results.txt")

with tab2:
    
    st.session_state['trans_2_input'] = st.text_area("复制或者输入需要翻译的文本（英文夹杂中文没关系，语言支离破碎也没关系），拉拽文本框的右下角增加文本框长度。Go ahead and paste or type out the text you want to translate — it's totally fine if it's a mix of English and Chinese. Drag the bottom right corner of the text box to expand it as needed!")
    st.session_state['trans_2_creativity'] = st.slider("请输入翻译后中文文本的创造力（数字小说明更严谨，数字大说明更多样更有创造性，默认值为1。Please enter a creativity value for the translated English text. A lower number means it's more precise, while a higher number indicates it's more diverse and creative. The default value is 1.）", min_value=0.5,
                       max_value=1.5, value=1.0, step=0.1)
    submit2 = st.button("翻译 To Chinese")

    if submit2:
        with st.spinner("你的AI小助手正在努力工作嘤...Your AI translator is working..."):
            st.session_state['trans_2_result'] = generate_essay_toChinese(st.session_state['trans_2_input'],st.session_state['trans_2_creativity'],st.session_state['selected_model'])
    if st.session_state['trans_2_input']:
        st.divider()
        left,right = st.columns(2)
        with left:
            st.markdown("#### 原文 Original text")
            st.write(st.session_state['trans_2_input'])
        with right:
            st.markdown("#### 翻译后的文本 Translated text")
            st.write(st.session_state['trans_2_result'])
            st.download_button(label="一键下载生成内容 Download", data=st.session_state['trans_2_result'], file_name="my_results.txt")