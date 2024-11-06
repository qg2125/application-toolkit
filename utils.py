import streamlit as st
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from prompt_template import system_template_resume_content, system_template_toEnglish, user_template_toEnglish, system_template_toChinese, user_template_toChinese, system_template_rl_first, system_template_email, system_template_emai_reply, system_template_para, system_template_grammar, system_template_interview_tips,system_template_interview_eval


#1 ChatMate AI
def get_chat_response(prompt, memory, model_type):
    openai_model = ChatOpenAI(model=st.secrets["GPT_4OMINI_MODEL"], openai_api_key=st.secrets["4OMONI_API_KEY"], base_url=st.secrets["4OMINI_BASE_URL"])
    gemini_model = ChatGoogleGenerativeAI(model=st.secrets["GEMINI_MODEL"], google_api_key=st.secrets["GEMINI_API_KEY"])
    claude_model = ChatOpenAI(model=st.secrets["CLAUDE_MODEL"], api_key=st.secrets["CLAUDE_API_KEY"], base_url=st.secrets["CLAUDE_BASE_URL"])
    
    if model_type=="chatgpt":
        chain = ConversationChain(llm=openai_model, memory=memory)
    elif model_type=="gemini":
        chain = ConversationChain(llm=gemini_model, memory=memory)
    elif model_type =="claude":
        chain = ConversationChain(llm=claude_model, memory = memory)
    else:
        raise ValueError("Unsupported model type: {}".format(model_type))

    response = chain.invoke({"input": prompt})
    return response["response"]

#2 Translator
def generate_essay_toEnglish(txt, creativity,model_type):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template_toEnglish),
        ("user", user_template_toEnglish)
    ])

    
    if model_type=="chatgpt":
        openai_model = ChatOpenAI(model=st.secrets["GPT_4OMINI_MODEL"], openai_api_key=st.secrets["4OMONI_API_KEY"], base_url=st.secrets["4OMINI_BASE_URL"], temperature=creativity)
        chain = prompt | openai_model
    elif model_type=="gemini":
        gemini_model = ChatGoogleGenerativeAI(model=st.secrets["GEMINI_MODEL"], google_api_key=st.secrets["GEMINI_API_KEY"], temperature=creativity*0.6)
        chain = prompt | gemini_model
    
    else:
        raise ValueError("Unsupported model type: {}".format(model_type))
    result = chain.invoke({"input_chinese": txt}).content

    return result

def generate_essay_toChinese(txt, creativity,model_type):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template_toChinese),
        ("user", user_template_toChinese)
    ])

    openai_model = ChatOpenAI(model=st.secrets["GPT_4OMINI_MODEL"], openai_api_key=st.secrets["4OMONI_API_KEY"], base_url=st.secrets["4OMINI_BASE_URL"], temperature=creativity)
    gemini_model = ChatGoogleGenerativeAI(model=st.secrets["GEMINI_MODEL"], google_api_key=st.secrets["GEMINI_API_KEY"], temperature=creativity*0.6)
    
    if model_type=="chatgpt":
        chain = prompt | openai_model
    elif model_type=="gemini":
        chain = prompt | gemini_model
    
    else:
        raise ValueError("Unsupported model type: {}".format(model_type))
    result = chain.invoke({"input_english": txt}).content

    return result

#3 Resume generator
def generate_date(start, end, format_requirement):
    start_year = start.year
    start_month = start.month
    end_year = end.year
    end_month = end.month
    months = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.", "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."]
    months_full = ["January", "February", "March", "April", "May", "June","July", "August", "September", "October", "November", "December"]


    start_date = months[start_month-1] + " " + str(start_year)
    end_date = months[end_month-1] + " " + str(end_year)
    start_date_full = months_full[start_month-1] + " " + str(start_year)
    end_date_full = months_full[end_month-1] + " " + str(end_year)

    if format_requirement == "缩写Abbrev.":

        return start_date + " - " + end_date
    elif format_requirement == "全拼Full":
        
        return start_date_full + " - " + end_date_full
    

def generate_resume_content(resume_data):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template_resume_content),
        ("user", f"""The user will input the following information for you to craft the resume according to the instructions in system template {resume_data['ResearchTitle']} {resume_data['Role']} {resume_data['Institution']} {resume_data['Location']} {resume_data['Date']} {resume_data['Advisor']} {resume_data['Experience']}""")
    ])

    openai_model = ChatOpenAI(model = st.secrets["GPT_4ALL_MODEL"], openai_api_key=st.secrets["4OMONI_API_KEY"], base_url=st.secrets["4OMINI_BASE_URL"])
    gemini_model = ChatGoogleGenerativeAI(model=st.secrets["GEMINI_MODEL"], google_api_key=st.secrets["GEMINI_API_KEY"])
    claude_model = ChatOpenAI(model=st.secrets["CLAUDE_MODEL"], api_key=st.secrets["CLAUDE_API_KEY"], base_url=st.secrets["CLAUDE_BASE_URL"])
    
    chain_gpt = prompt | openai_model
    chain_gemini = prompt | gemini_model
    chain_claude = prompt | claude_model
    
    result_gpt = chain_gpt.invoke(resume_data).content
    result_gemini = chain_gemini.invoke(resume_data).content
    result_claude = chain_claude.invoke(resume_data).content

    return result_gpt,result_gemini,result_claude

#5 Recommendation letter
def generate_rl_first(first_para_input):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template_rl_first),
        ("user", "{input}")
    ])

    openai_model = ChatOpenAI(model = st.secrets["GPT_4ALL_MODEL"], openai_api_key=st.secrets["4OMONI_API_KEY"], base_url=st.secrets["4OMINI_BASE_URL"])
    gemini_model = ChatGoogleGenerativeAI(model=st.secrets["GEMINI_MODEL"], google_api_key=st.secrets["GEMINI_API_KEY"])
    claude_model = ChatOpenAI(model=st.secrets["CLAUDE_MODEL"], api_key=st.secrets["CLAUDE_API_KEY"], base_url=st.secrets["CLAUDE_BASE_URL"])
    
    chain_gpt = prompt | openai_model
    chain_gemini = prompt | gemini_model
    chain_claude = prompt | claude_model
    
    result_gpt = chain_gpt.invoke({"input": first_para_input}).content
    result_gemini = chain_gemini.invoke({"input": first_para_input}).content
    result_claude = chain_claude.invoke({"input": first_para_input}).content

    return result_gpt,result_gemini,result_claude

# 6 Email generator
def generate_email(email_input, email_style):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template_email),
        ("user", "{input}")
    ])

    openai_model = ChatOpenAI(model = st.secrets["GPT_4ALL_MODEL"], openai_api_key=st.secrets["4OMONI_API_KEY"], base_url=st.secrets["4OMINI_BASE_URL"])
    gemini_model = ChatGoogleGenerativeAI(model=st.secrets["GEMINI_MODEL"], google_api_key=st.secrets["GEMINI_API_KEY"])
    
    chain_gpt = prompt | openai_model
    chain_gemini = prompt | gemini_model
    
    result_gpt = chain_gpt.invoke({"input": email_input, "style":email_style}).content
    result_gemini = chain_gemini.invoke({"input": email_input, "style":email_style}).content

    return result_gpt,result_gemini
# 7 reply email
def reply_email(previous_email, email_reply, email_style):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template_emai_reply),
        ("user", "{input}")
    ])

    openai_model = ChatOpenAI(model = st.secrets["GPT_4ALL_MODEL"], openai_api_key=st.secrets["4OMONI_API_KEY"], base_url=st.secrets["4OMINI_BASE_URL"])
    gemini_model = ChatGoogleGenerativeAI(model=st.secrets["GEMINI_MODEL"], google_api_key=st.secrets["GEMINI_API_KEY"])
    
    chain_gpt = prompt | openai_model
    chain_gemini = prompt | gemini_model
    
    result_gpt = chain_gpt.invoke({"input": previous_email, "replyRequirements": email_reply, "style":email_style}).content
    result_gemini = chain_gemini.invoke({"input": previous_email, "replyRequirements": email_reply, "style":email_style}).content

    return result_gpt,result_gemini


# 8. paragraph editor
def generate_para(para_input, para_requirements,para_major, para_language, length_min, length_max):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template_para),
        ("user", "{input}")
    ])

    openai_model = ChatOpenAI(model = st.secrets["GPT_4ALL_MODEL"], openai_api_key=st.secrets["4OMONI_API_KEY"], base_url=st.secrets["4OMINI_BASE_URL"])
    gemini_model = ChatGoogleGenerativeAI(model=st.secrets["GEMINI_MODEL"], google_api_key=st.secrets["GEMINI_API_KEY"])
    claude_model = ChatOpenAI(model=st.secrets["CLAUDE_MODEL"], api_key=st.secrets["CLAUDE_API_KEY"], base_url=st.secrets["CLAUDE_BASE_URL"])
    
    chain_gpt = prompt | openai_model
    chain_gemini = prompt | gemini_model
    chain_claude = prompt | claude_model
    
    result_gpt = chain_gpt.invoke({"input": para_input, "requirements":para_requirements, "major":para_major, "language":para_language, "min":length_min, "max":length_max}).content
    result_gemini = chain_gemini.invoke({"input": para_input, "requirements":para_requirements, "major":para_major, "language":para_language, "min":length_min, "max":length_max}).content
    result_claude = chain_claude.invoke({"input": para_input, "requirements":para_requirements, "major":para_major, "language":para_language, "min":length_min, "max":length_max}).content

    return result_gpt,result_gemini,result_claude

# 9 Grmmar Checker
def grammar_checker(grammar_input):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template_grammar),
        ("user", "{input}")
    ])

    openai_model = ChatOpenAI(model = st.secrets["GPT_4ALL_MODEL"], openai_api_key=st.secrets["4OMONI_API_KEY"], base_url=st.secrets["4OMINI_BASE_URL"])
    gemini_model = ChatGoogleGenerativeAI(model=st.secrets["GEMINI_MODEL"], google_api_key=st.secrets["GEMINI_API_KEY"])
    claude_model = ChatOpenAI(model=st.secrets["CLAUDE_MODEL"], api_key=st.secrets["CLAUDE_API_KEY"], base_url=st.secrets["CLAUDE_BASE_URL"])
    
    chain_gpt = prompt | openai_model
    chain_gemini = prompt | gemini_model
    chain_claude = prompt | claude_model
    
    result_gpt = chain_gpt.invoke({"input": grammar_input}).content
    result_gemini = chain_gemini.invoke({"input": grammar_input}).content
    result_claude = chain_claude.invoke({"input": grammar_input}).content

    return result_gpt,result_gemini,result_claude

# 10 mock interview
from random import choice
def get_random_question(*args):  # 添加 *args 来接受任何可能的参数
    """
    Returns a random question from a predefined list of questions about Columbia Engineering
    and career goals.
    
    Returns:
        str: A randomly selected question
    """
    questions = [
        "How does the program in Columbia Engineering fulfill your career goal?",
        "Tell us about a course you took in which you learned the most from",
        "How do you feel about New York City?",
        "How does your field align with your career goals?",
        "What is your dream job?"
    ]
    
    return choice(questions)

def interview_tips(question):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template_interview_tips),
        ("user", "{input}")
    ])

    
    claude_model = ChatOpenAI(model=st.secrets["CLAUDE_MODEL"], api_key=st.secrets["CLAUDE_API_KEY"], base_url=st.secrets["CLAUDE_BASE_URL"])
    
    
    chain_claude = prompt | claude_model
    
    
    result_claude = chain_claude.invoke({"input": question}).content

    return result_claude

def interview_evaluation(question, answers):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template_interview_eval),
        ("user", "{input}")
    ])

    
    claude_model = ChatOpenAI(model=st.secrets["CLAUDE_MODEL"], api_key=st.secrets["CLAUDE_API_KEY"], base_url=st.secrets["CLAUDE_BASE_URL"])
    
    
    chain_claude = prompt | claude_model
    
    
    result_claude = chain_claude.invoke({"input": answers, "question": question}).content

    return result_claude