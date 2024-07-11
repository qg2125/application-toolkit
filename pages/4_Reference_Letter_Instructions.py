import streamlit as st

st.markdown("## 常见推荐信问题 Reference Letter FAQ")
with st.expander("🖊️ 合适的推荐人数量和搭配"):
    st.write("""
    通常情况下，申请人需要准备2-3封推荐信，整体而言，最好至少联系3-4位老师，因为部分老师不愿意为同一位学生撰写过多封推荐信。

    在推荐人选择方面，建议参考以下几种组合：

    * 授课老师2位 + 科研/实习导师1位
    * 授课老师1位 + 科研导师1位 + 实习导师1位
    * 授课老师1位 + 科研/实习导师2位
"""
    )
with st.expander("🖊️ 推荐人筛选原则"):
    st.write("""
    以下影响因素排名有先后，对同学的了解程度、认可度、专业的相关度和推荐人的靠谱程度相对更重要。
    1. **熟悉程度**: 优先选择与学生交集多，对其经历了解深入的人选，例如主修课程任课教师、科研导师、实习/工作主管、课外活动/竞赛指导教师/负责人等。
    2. **专业相关性**: 推荐人最好与申请专业直接相关。例如，核心专业课程教师的推荐优先级高于非专业课程教师；申请计算机科学方向的学生应尽量避免选择写作课教师作为推荐人。
    3. **互动与表现**: 选择在与学生互动中，学生表现突出的推荐人，例如成绩优异、科研投入且成果显著、实习努力且成果丰硕、沟通交流频繁等。这类推荐人更有可能撰写强有力的推荐信。
    4. **可靠度与声誉**: 优先选择历年学生口碑良好，有耐心且乐于提供帮助的推荐人。 尽量避免选择不靠谱的人选，例如邮件沟通不畅、无法按时提交推荐信、同意推荐后反悔、承诺推荐数量后临时变卦等。
    5. **推荐人头衔不是最重要的，但是也需要考虑**: 避免所有推荐人身份单一，例如全部为讲师。 但也不应单纯追求推荐人头衔，而忽视其他因素。
    6. **海外联系和业内的名气**: 推荐人是否与申请目标国家或项目有联系也是一项考量因素，例如是某学校的校友，曾经在目标学校任教等。
    
    可以使用下表记录自己的推荐人信息，以便筛选。
"""
    )
    st.image("images/select_1.jpg")
    

with st.expander("🖊️ 推荐信提交流程"):
    st.write(" 1️⃣ 学生需自行在每个项目的网申系统中填写推荐人信息，包括姓名、职称、职位、关系以及电子邮件地址（推荐使用官方邮箱，例如以“.edu”或公司域名结尾的邮箱）。请注意，建议选择“I waive my right to access this report.”的选项，以提高推荐信的可信度。")
    st.image("images/upload_1.jpg", width=600)
    st.write("2️⃣ 填写完成后，申请系统自动发邮件到推荐人的邮箱。")
    st.image("images/upload_2.jpg", width=600)
    st.write(
        """
        3️⃣ 当候选人通过推荐链接提交申请时，推荐系统通常包含以下部分：

        * 推荐人信息确认： 首先核对推荐人的基本身份信息。
        * 推荐信上传： 推荐人上传已撰写好的推荐信文件，或根据系统提供的模板填写。
        * 能力打分（可选）： 部分系统会要求推荐人对候选人的各项能力进行打分。
        * 额外问题（可选）： 部分系统可能会要求推荐人回答一些关于候选人的额外问题，以更全面地了解候选人。
"""
    )
    st.image("images/upload_3.jpg", width=600)
    st.write("""
        4️⃣ 推荐人提交推荐信后，学生通常会收到申请邮箱的邮件通知，告知该推荐人的推荐信已提交。如果未收到邮件，则可直接在申请系统中查看提交状态。
    """
    )
    st.image("images/upload_4.jpg")

with st.expander("🖊️ 什么时候可以向老师要推荐信"):
    st.write("""
        建议尽早联系已经可以提供推荐信的老师，最晚要在项目截止日期前**至少一个月**通知推荐人。
        * 授课老师: 课程结束后即可联系，并在取得成绩后索要推荐信，课程初期不宜直接索要。
        * 实习导师: 已结束实习的导师可以直接联系，刚开始做的实习则暂不索要。
        * 科研导师: 已经完成或结束科研项目的导师可以直接联系，正在进行中、尤其是开始时间很短（例如几周或一个月内）的项目导师暂不索要。
    """
    )

with st.expander("🖊️ 如何用正确的方式和老师沟通推荐信"):
    st.write(
        f"""
        对于比较熟识的老师可以通过常用的方式沟通，比如office hour、组会、短信等。对于不太熟悉的老师，建议使用邮件沟通。如果是海外推荐人，在首次联系老师索要推荐信时，建议仅询问老师是否愿意提供推荐信，而不要涉及推荐信数量或提交方式等细节问题。如果事先未与老师沟通过，切勿直接将推荐信草稿发送给老师。首次与老师沟通的邮件可以参考：

        
        Dear Professor XX,

        I hope you are doing well!
        
        I’m XXX, who is taking your course - EECS442 XX this semester and earned an A in this course. I’m writing to kindly inquire the possibility of you providing a reference for me as I am working on my graduate application for Fall 2024. 
        
        Your instruction in this course has greatly inspired me to further pursue the subject of computer science at a graduate school. You’ve also encouraged me enormously in class discussion and graduate school pursuit. Therefore, I believe that you would be the ideal person to provide a letter of recommendation for my graduate school application.

        I completely understand that you might be extremely busy. Please let me know if would be comfortable endorsing my candidacy. I would be more than happy to send you additional information about my background and motivation. I have attached my resume and transcript to this email for your reference. Thank you very much in advance for your consideration.

        Best regards,
        
        

    """
    )