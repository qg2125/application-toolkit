import streamlit as st
from utils import generate_essay_toEnglish, generate_essay_toChinese

st.set_page_config(layout="wide")
st.title("文书翻译 Translation AI")
# Initialize or retrieve the selected model from session state
if 'selected_model' not in st.session_state:
    st.session_state['selected_model'] = 'gemini'  # Default model

# Model selection radio button
with st.expander("请选择使用的语言模型 Please choose the language model you'd like to use："):
    proposed_model = st.radio("", ["gpt-3.5", "gemini"], 
                            index=["gpt-3.5", "gemini"].index(st.session_state['selected_model']))
    if st.button('选择 Select'):
        st.session_state['selected_model'] = proposed_model  # Update the session state only when button is clicked

st.write("当前选择的模型是 The selected model is：", st.session_state['selected_model'])
st.divider()

tab1, tab2 = st.tabs(["中译英 Chinese to English","英译中 English to Chinese"])

with tab1:
    with st.expander("AI助手提示词参考 GTP Prompt"):
        st.write("""
## Character
You are a professional translator, adept at translating mixed-language text (Chinese and English) into English. Your translations are polished and align with the writing standards of U.S. graduate school admissions. You ensure logical coherence even if the original text has some inconsistencies.

## Skills

### Skill 1: Translation Accuracy and Fluency
- Translate Chinese and English content into fluent English.
- Maintain a polished, academically appropriate tone.

### Skill 2: Logical Coherence
- Improve the logical flow of the text while translating.
- Correct any logical inconsistencies present in the original text.

## Constraints
- Translate all content provided by the user.
- Ensure the translated paragraph aligns with U.S. graduate school admission standards.
- Ensure logical coherence and fluency in the translated text.

"""

        )
    paragraph1 = st.text_area("复制或者输入需要翻译的文本（中文夹杂英文没关系，语言支离破碎也没关系），拉拽文本框的右下角增加文本框长度。Go ahead and paste or type out the text you want to translate — it's totally fine if it's a mix of English and Chinese. Drag the bottom right corner of the text box to expand it as needed!")
    creativity = st.slider("请输入翻译后英文文本的创造力（数字小说明更严谨，数字大说明更多样更有创造性，默认值为1。Please enter a creativity value for the translated English text. A lower number means it's more precise, while a higher number indicates it's more diverse and creative. The default value is 1.）", min_value=0.5,
                       max_value=1.5, value=1.0, step=0.1)
    submit1 = st.button("翻译 To English")

    if submit1:
        with st.spinner("你的AI小助手正在努力工作嘤...Your AI translator is working..."):
            result1 = generate_essay_toEnglish(paragraph1,creativity,st.session_state['selected_model'])
        st.divider()
        left,right = st.columns(2)
        with left:
            st.markdown("#### 原文 Original Text")
            st.write(paragraph1)
        with right:
            st.markdown("#### 翻译后的文本 Translated text")
            st.write(result1)

with tab2:
    with st.expander("AI助手提示词参考 GTP Prompt"):
        st.write("""
## 角色
您是一名专业翻译人员，擅长将中英文混合文本翻译成中文。您的翻译工作精炼，并符合中文学术写作标准。即使原文中存在一些不一致之处，您也确保翻译的逻辑连贯性。

## 技能
### 技能1：翻译的准确性和流畅性
- 将中文和英文内容翻译成流畅的中文。
- 保持语气恰当。

### 技能2：逻辑连贯性
- 在翻译过程中改善文本的逻辑流畅性。
- 纠正原文中存在的任何逻辑不一致。

## 约束
- 翻译用户提供的所有内容。
- 确保翻译后的段落符合中文正常的表达习惯。
- 确保翻译文本的逻辑连贯性和流畅性。



"""

        )
    paragraph2 = st.text_area("复制或者输入需要翻译的文本（英文夹杂中文没关系，语言支离破碎也没关系），拉拽文本框的右下角增加文本框长度。Go ahead and paste or type out the text you want to translate — it's totally fine if it's a mix of English and Chinese. Drag the bottom right corner of the text box to expand it as needed!")
    creativity2 = st.slider("请输入翻译后中文文本的创造力（数字小说明更严谨，数字大说明更多样更有创造性，默认值为1。Please enter a creativity value for the translated English text. A lower number means it's more precise, while a higher number indicates it's more diverse and creative. The default value is 1.）", min_value=0.5,
                       max_value=1.5, value=1.0, step=0.1)
    submit2 = st.button("翻译 To Chinese")

    if submit2:
        with st.spinner("你的AI小助手正在努力工作嘤...Your AI translator is working..."):
            result2 = generate_essay_toChinese(paragraph2,creativity2,st.session_state['selected_model'])
        st.divider()
        left,right = st.columns(2)
        with left:
            st.markdown("#### 原文 Original text")
            st.write(paragraph2)
        with right:
            st.markdown("#### 翻译后的文本 Translated text")
            st.write(result2)