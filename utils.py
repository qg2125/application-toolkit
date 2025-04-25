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
    "Tell us about a course you took in which you learned the most from.",
    "How do you feel about New York City?",
    "How does your field align with your career goals?",
    "What is your dream job?",
    "Where do you see yourself in ten years?",
    "Are you interested in a career in industry or academia? And why?",
    "What do you know about our department and the faculty?",
    "Why pursue an advanced degree?",
    "Do you have any internship or work experience? If so, what role did it play in your decision to pursue an MS degree?",
    "Of the 8 standard tracks in the MS program, which are you most interested in and why?",
    "What have you done thus far to prepare for your application?",
    "We are very proud of our curriculum; what courses or topics are you excited about?",
    "If you were to enter an academic/career path entirely unrelated to science and engineering, what would it be and why?"
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


# 11. pdf处理

import os
import re
import PyPDF2
import json
import requests

class ResumeProcessor:
    def __init__(self, api_key="", base_url=""):
        # 初始化OpenAI API配置
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 识别和过滤个人信息的正则表达式
        self.email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        self.phone_pattern = r"(?:\+?\d{1,3}[- ]?)?\(?(?:\d{3})?\)?[- ]?\d{3}[- ]?\d{4,}"
        self.address_pattern = r"(?:Address|Location|City|State|Country)[\s:]*([^\n]+)"
    
    def extract_text_from_pdf(self, pdf_file):
        """从PDF文件中提取文本"""
        try:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception(f"PDF文件读取失败: {e}")
    
    def anonymize_text(self, text):
        """移除个人身份信息"""
        # 移除电子邮件
        text = re.sub(self.email_pattern, "[EMAIL REMOVED]", text)
        # 移除电话号码
        text = re.sub(self.phone_pattern, "[PHONE REMOVED]", text)
        # 移除地址
        text = re.sub(self.address_pattern, "[ADDRESS REMOVED]", text)
        
        # 使用OpenAI识别和移除姓名
        prompt = """
        This is a resume text. Please identify any personal names that likely represent the resume owner's name 
        (usually appears at the top or in a header section). Return only the name without any explanation.
        If you can't find a name, return "None". Resume text:
        
        """
        try:
            response = self.call_openai_api(prompt + text[:500])  # 只检查前500个字符，姓名通常在开头
            potential_name = response.strip()
            if potential_name != "None":
                text = text.replace(potential_name, "[NAME REMOVED]")
        except Exception as e:
            print(f"Warning: Name anonymization failed: {e}")
        
        return text
    
    def call_openai_api(self, prompt, model="Qwen/Qwen2.5-72B-Instruct-128K"):
        """调用OpenAI API"""
        endpoint = f"{self.base_url}/v1/chat/completions"
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.5,
            "max_tokens": 3000,  # 设置合适的最大输出长度
            
        }
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()  # 检查HTTP错误
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                raise Exception(f"API调用失败: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"API请求失败: {str(e)}")
    
    def process_resume_with_ai(self, anonymized_text):
        """使用OpenAI API处理简历内容并提取结构化信息"""
        prompt = """
        分析以下英文简历内容，提取关键信息并按指定格式输出。
        
        请识别以下信息：
        1. 教育背景：
           - 学校类型：如果是中国985高校，标记为"985"；如果是211高校，标记为"211"；如果是其他中国高校，标记为"双非"；
             如果是国外学校，标记为"海本"或"海硕"或"海博"；美国高校标记为"美本"
           - 专业名称
        
        2. 学术表现：
           - GPA（如有）
           - 语言成绩（托福/雅思/GRE等，如有）
        
        3. 主要经历：
           - 实习经历，注明有几段实习经历，如果在知名企业可以特别注明，并且对于每段实习经历进行2-3句话的总结。
           - 科研项目，注明有几段科研经历，说明级别：国家级/省级/校级等，并且对于每段科研经历进行2-3句话的总结。
           - 发表论文情况（数量和级别）
           - 竞赛获奖情况
           - 课外活动/社团经历
           - 掌握的主要技能
        
        以JSON格式输出，格式如下：
        {
            "背景": "学校类型+专业",
            "学术": "GPA和语言成绩",
            "经历": "主要经历概述"
        }
        
        只返回JSON数据，不要有其他说明。如果某项信息不存在，填写"未提及"。
        
        简历内容：
        """
        
        try:
            response_text = self.call_openai_api(prompt + anonymized_text)
            
            # 提取JSON部分
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(0))
                return result
            else:
                print("Warning: Could not extract JSON from AI response")
                # 创建一个默认结果
                return {
                    "背景": "未能识别",
                    "学术": "未能识别",
                    "经历": "未能识别"
                }
        except Exception as e:
            print(f"Error processing resume with AI: {e}")
            return {
                "背景": "AI处理出错",
                "学术": "AI处理出错",
                "经历": "AI处理出错"
            }
    
    def process_resume(self, pdf_file):
        """处理简历并生成摘要"""
        # 提取文本
        text = self.extract_text_from_pdf(pdf_file)
        
        # 匿名化处理
        anonymized_text = self.anonymize_text(text)
        
        # 使用AI提取信息
        summary = self.process_resume_with_ai(anonymized_text)
        
        return summary
    
    def validate_api_key(self):
        """验证API密钥是否有效"""
        try:
            self.call_openai_api("Hello")
            return True
        except Exception as e:
            print(f"API密钥验证失败: {e}")
            return False
