import streamlit as st
from langchain.memory import ConversationBufferMemory
from utils import get_chat_response

st.set_page_config(layout="centered")
st.title("💬 聊天小助手ChatMate AI")
# Initialize or retrieve the selected model from session state
if 'selected_model' not in st.session_state:
    st.session_state['selected_model'] = 'gemini'  # Default model

with st.expander("请选择使用的语言模型 Please choose the language model you'd like to use："):
    proposed_model = st.radio("", ["gpt-3.5", "gemini"], 
                            index=["gpt-3.5", "gemini"].index(st.session_state['selected_model']))
    if st.button('选择 Select'):
        st.session_state['selected_model'] = proposed_model  # Update the session state only when button is clicked

st.write("当前选择的模型是 The selected model is：", st.session_state['selected_model'])

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
    st.session_state["messages"] = [{"role": "ai",
                                     "content": "你好，我是你的AI助手，有什么可以帮你的吗？Hey there! I'm your AI assistant. What can I help you with today?"}]

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()
if prompt:
    
    st.session_state["messages"].append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)

    with st.spinner("AI正在思考中，请稍等...Your AI assistant is working..."):
        response = get_chat_response(prompt, st.session_state["memory"], st.session_state['selected_model'])
    msg = {"role": "ai", "content": response}
    st.session_state["messages"].append(msg)
    st.chat_message("ai").write(response)