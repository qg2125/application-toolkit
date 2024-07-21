from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from prompt_template import system_template_resume_content, system_template_toEnglish, user_template_toEnglish, system_template_toChinese, user_template_toChinese, system_template_rl_first
from langchain_anthropic import ChatAnthropic

#1 ChatMate AI
def get_chat_response(prompt, memory, model_type):
    openai_model = ChatOpenAI(model="gpt-4o-mini", openai_api_key="sk-fHzAJXqDYhnJYeexCa4c683e9aBd401bA5Ad398fD52eC126", base_url="https://35.aigcbest.top/v1/")
    gemini_model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key="AIzaSyAS7iBE-CshQOyhlk-PlnDRJhE7JROcXaQ")
    claude_model = ChatOpenAI(model="claude-3-haiku-20240307", api_key="sk-Z5K96AqB3ENn11jUB7853404A0E145D990495363A681041a", base_url="https://api2.aigcbest.top/v1/")
    if model_type=="chatgpt":
        chain = ConversationChain(llm=openai_model, memory=memory)
    elif model_type=="gemini":
        chain = ConversationChain(llm=gemini_model, memory=memory)
    elif model_type == "claude":
        chain = ConversationChain(llm =claude_model, memory=memory)
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
        openai_model = ChatOpenAI(model = "gpt-4o-mini", api_key="sk-fHzAJXqDYhnJYeexCa4c683e9aBd401bA5Ad398fD52eC126", base_url="https://35.aigcbest.top/v1/", temperature=creativity)
        chain = prompt | openai_model
    elif model_type=="gemini":
        gemini_model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key="AIzaSyAS7iBE-CshQOyhlk-PlnDRJhE7JROcXaQ", temperature=creativity*0.6)
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

    openai_model = ChatOpenAI(model = "gpt-4o-mini", api_key="sk-fHzAJXqDYhnJYeexCa4c683e9aBd401bA5Ad398fD52eC126", base_url="https://35.aigcbest.top/v1/", temperature=creativity)
    gemini_model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key="AIzaSyAS7iBE-CshQOyhlk-PlnDRJhE7JROcXaQ", temperature=creativity*0.6)
    
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

    openai_model = ChatOpenAI(model = "gpt-4-all", api_key="sk-fHzAJXqDYhnJYeexCa4c683e9aBd401bA5Ad398fD52eC126", base_url="https://35.aigcbest.top/v1/")
    gemini_model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key="AIzaSyAS7iBE-CshQOyhlk-PlnDRJhE7JROcXaQ")
    claude_model = ChatOpenAI(model="claude-3-5-sonnet-20240620", api_key="sk-Z5K96AqB3ENn11jUB7853404A0E145D990495363A681041a", base_url="https://api2.aigcbest.top/v1/")
    
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

    openai_model = ChatOpenAI(model = "gpt-4-all", api_key="sk-fHzAJXqDYhnJYeexCa4c683e9aBd401bA5Ad398fD52eC126", base_url="https://35.aigcbest.top/v1/")
    gemini_model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key="AIzaSyAS7iBE-CshQOyhlk-PlnDRJhE7JROcXaQ")
    claude_model = ChatOpenAI(model="claude-3-5-sonnet-20240620", api_key="sk-Z5K96AqB3ENn11jUB7853404A0E145D990495363A681041a", base_url="https://api2.aigcbest.top/v1/")
    
    chain_gpt = prompt | openai_model
    chain_gemini = prompt | gemini_model
    chain_claude = prompt | claude_model
    
    result_gpt = chain_gpt.invoke({"input": first_para_input}).content
    result_gemini = chain_gemini.invoke({"input": first_para_input}).content
    result_claude = chain_claude.invoke({"input": first_para_input}).content

    return result_gpt,result_gemini,result_claude
