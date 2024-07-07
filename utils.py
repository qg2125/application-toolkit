from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from prompt_template import system_template_resume_content, system_template_toEnglish, user_template_toEnglish, system_template_toChinese, user_template_toChinese


#1 ChatMate AI
def get_chat_response(prompt, memory, model_type):
    openai_model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key="sk-Z5K96AqB3ENn11jUB7853404A0E145D990495363A681041a", base_url="https://api2.aigcbest.top/v1")
    gemini_model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key="AIzaSyAS7iBE-CshQOyhlk-PlnDRJhE7JROcXaQ")
    if model_type=="gpt-3.5":
        chain = ConversationChain(llm=openai_model, memory=memory)
    elif model_type=="gemini":
        chain = ConversationChain(llm=gemini_model, memory=memory)
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

    openai_model = ChatOpenAI(model = "gpt-3.5-turbo", api_key="sk-Z5K96AqB3ENn11jUB7853404A0E145D990495363A681041a", base_url="https://api2.aigcbest.top/v1")
    gemini_model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key="AIzaSyAS7iBE-CshQOyhlk-PlnDRJhE7JROcXaQ")
    if model_type=="gpt-3.5":
        chain = prompt | openai_model
    elif model_type=="gemini":
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

    openai_model = ChatOpenAI(model = "gpt-3.5-turbo", api_key="sk-Z5K96AqB3ENn11jUB7853404A0E145D990495363A681041a", base_url="https://api2.aigcbest.top/v1")
    gemini_model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key="AIzaSyAS7iBE-CshQOyhlk-PlnDRJhE7JROcXaQ")
    if model_type=="gpt-3.5":
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
    

def generate_resume_content(resume_data, model_type):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template_resume_content),
        ("user", f"""The user will input the following information for you to craft the resume according to the instructions {resume_data['ResearchTitle']} {resume_data['Role']} {resume_data['Institution']} {resume_data['Location']} {resume_data['Date']} {resume_data['Advisor']} {resume_data['Experience']}""")
    ])

    openai_model = ChatOpenAI(model = "gpt-3.5-turbo", api_key="sk-Z5K96AqB3ENn11jUB7853404A0E145D990495363A681041a", base_url="https://api2.aigcbest.top/v1")
    gemini_model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key="AIzaSyAS7iBE-CshQOyhlk-PlnDRJhE7JROcXaQ")
    if model_type=="gpt-3.5":
        chain = prompt | openai_model
    elif model_type=="gemini":
        chain = prompt | gemini_model
    else:
        raise ValueError("Unsupported model type: {}".format(model_type))
    
    result = chain.invoke(resume_data).content

    return result

