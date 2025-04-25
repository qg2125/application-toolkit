import streamlit as st
import os
import tempfile
from utils import ResumeProcessor
import time
import json
import re
import ast

st.set_page_config(
    page_title="简历分析工具",
    page_icon="📝",
    layout="centered"
)

def parse_complex_structure(text):
    """解析复杂的数据结构字符串，包括嵌套列表和字典"""
    # 尝试多种方式解析文本中的数据结构
    try:
        # 尝试作为JSON解析
        return json.loads(text)
    except:
        pass
    
    try:
        # 尝试作为Python字面量解析
        return ast.literal_eval(text)
    except:
        pass
    
    # 返回原始文本
    return text

def format_list_of_dicts(data_list):
    """格式化字典列表为HTML"""
    html_content = ""
    for item in data_list:
        html_content += '<div style="margin-bottom: 15px; padding: 10px; background-color: rgba(255,255,255,0.5); border-radius: 5px;">'
        for key, value in item.items():
            if key == '公司':
                html_content += f'<strong style="color:#2c7ea5;">{value}</strong><br>'
            elif key == '职位':
                html_content += f'<em>{value}</em><br>'
            elif key == '总结':
                html_content += f'{value}<br>'
            else:
                html_content += f'<strong>{key}:</strong> {value}<br>'
        html_content += '</div>'
    return html_content

def format_experience(experience):
    """处理经历部分的格式化"""
    # 如果是字典类型，转换为格式化文本
    if isinstance(experience, dict):
        formatted_exp = ""
        for key, value in experience.items():
            # 检查值是否是复杂结构
            if isinstance(value, str) and ('[{' in value or '{' in value):
                parsed_value = parse_complex_structure(value)
                if isinstance(parsed_value, list):
                    formatted_exp += f"<strong>{key}:</strong><br>"
                    formatted_exp += format_list_of_dicts(parsed_value)
                else:
                    formatted_exp += f"<strong>{key}:</strong> {value}<br><br>"
            else:
                formatted_exp += f"<strong>{key}:</strong> {value}<br><br>"
        return formatted_exp
    
    # 如果是字符串类型
    experience_text = str(experience)
    
    # 查找并解析包含复杂数据结构的部分
    pattern = r'\*\*([^:]+):\*\*\s*(\[{.*?}\])'
    matches = re.findall(pattern, experience_text, re.DOTALL)
    for title, data_str in matches:
        try:
            data = parse_complex_structure(data_str)
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                formatted_data = format_list_of_dicts(data)
                experience_text = experience_text.replace(
                    f"**{title}:** {data_str}", 
                    f"<strong>{title}:</strong><br>{formatted_data}"
                )
        except:
            pass
    
    # 如果仍是原始格式，尝试不同的解析方式
    if "**实习经历:**" in experience_text and "[{" in experience_text:
        # 尝试解析嵌套的列表和字典
        sections = re.split(r'(\*\*[^:]+:\*\*)', experience_text)
        formatted_sections = []
        
        i = 0
        while i < len(sections):
            if i + 1 < len(sections) and sections[i].startswith("**") and sections[i].endswith(":**"):
                section_title = sections[i]
                section_content = sections[i+1] if i+1 < len(sections) else ""
                
                # 尝试解析复杂的数据结构
                if "[{" in section_content:
                    try:
                        # 提取可能的JSON或Python字面量
                        match = re.search(r'(\[{.*?}\])', section_content, re.DOTALL)
                        if match:
                            data_str = match.group(1)
                            data = parse_complex_structure(data_str)
                            
                            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                                formatted_data = format_list_of_dicts(data)
                                formatted_sections.append(section_title.replace("**", "<strong>").replace(":**", ":</strong><br>"))
                                formatted_sections.append(formatted_data)
                                i += 2
                                continue
                    except:
                        pass
                
                # 默认格式化
                formatted_sections.append(section_title.replace("**", "<strong>").replace(":**", ":</strong>"))
                formatted_sections.append(section_content)
                i += 2
            else:
                formatted_sections.append(sections[i])
                i += 1
                
        experience_text = "".join(formatted_sections)
    
    # 基本文本格式化
    experience_text = experience_text.replace("', '", "'<br>• ")
    experience_text = experience_text.replace("','", "<br>• ")
    experience_text = experience_text.replace("', ", "'<br>• ")
    experience_text = experience_text.replace(", '", "<br>• ")
    
    # 分类显示经历
    experience_text = experience_text.replace("实习经历:", "<strong>实习经历:</strong>")
    experience_text = experience_text.replace("科研项目:", "<strong>科研项目:</strong>")
    experience_text = experience_text.replace("发表论文:", "<strong>发表论文:</strong>")
    experience_text = experience_text.replace("获奖情况:", "<strong>获奖情况:</strong>")
    experience_text = experience_text.replace("社团/领导经历:", "<strong>社团/领导经历:</strong>")
    experience_text = experience_text.replace("掌握的主要技能:", "<strong>掌握的主要技能:</strong>")
    
    return experience_text

def prepare_download_content(summary):
    """准备下载内容，移除HTML标签"""
    def remove_html_tags(text):
        if isinstance(text, dict):
            return "\n".join([f"{k}: {v}" for k, v in text.items()])
        
        text = str(text)
        text = text.replace('<br>', '\n')
        text = text.replace('<strong>', '**')
        text = text.replace('</strong>', '**')
        text = text.replace('<div style="margin-bottom: 15px; padding: 10px; background-color: rgba(255,255,255,0.5); border-radius: 5px;">', '')
        text = text.replace('</div>', '\n')
        text = text.replace('<em>', '_')
        text = text.replace('</em>', '_')
        text = text.replace('• ', '- ')
        return text
    
    return "\n\n".join([
        "# 简历分析摘要",
        f"## 教育背景\n{remove_html_tags(summary['背景'])}",
        f"## 学术表现\n{remove_html_tags(summary['学术'])}",
        f"## 主要经历\n{remove_html_tags(summary['经历'])}"
    ])

def main():
    # 页面标题和介绍
    st.title("📝 智能简历分析工具")
    st.markdown("""
    上传简历PDF文件，获取AI分析摘要。该工具会自动识别关键信息并提供结构化反馈。
    """)
    
    # 创建处理器实例
    try:
        # 创建处理器实例
        api_key = st.secrets.get("CLAUDE_API_KEY", "")  # 使用 get 方法防止键不存在时出错
        base_url = st.secrets.get("4O_BASE_URL", "")
        
        if not api_key or not base_url:
            st.error("API设置错误：请检查secrets配置")
            return
            
        processor = ResumeProcessor(api_key=api_key, base_url=base_url)
    except Exception as e:
        st.error(f"初始化错误: {str(e)}")
    
    # 创建上传文件组件
    uploaded_file = st.file_uploader("上传简历 (PDF格式)", type=["pdf"])
    
    if uploaded_file:
        # 显示上传的文件名
        st.write(f"已上传: {uploaded_file.name}")
        
        # 处理按钮
        if st.button("🔍 分析简历"):
            # 显示处理状态
            with st.spinner("正在分析简历..."):
                try:
                    # 验证API密钥
                    if not processor.validate_api_key():
                        st.error("API密钥验证失败，请联系管理员")
                        return
                    
                    # 处理简历
                    summary = processor.process_resume(uploaded_file)
                    
                    # 显示处理结果
                    st.success("简历分析完成！")
                    
                    # 使用垂直布局显示结果
                    st.markdown("## 📊 简历分析结果")
                    
                    # 教育背景部分
                    st.markdown(f"""
                    <div style="border:1px solid #8bc9e0; border-radius:10px; padding:20px; margin-bottom:20px; background-color:#f0f8fb;">
                        <h3 style="color:#2c7ea5;">🎓 教育背景</h3>
                        <p>{summary["背景"]}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 学术表现部分
                    st.markdown(f"""
                    <div style="border:1px solid #a3d1a2; border-radius:10px; padding:20px; margin-bottom:20px; background-color:#f0fbf0;">
                        <h3 style="color:#3c9e3b;">📊 学术表现</h3>
                        <p>{summary["学术"]}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 主要经历部分 - 处理格式化问题
                    formatted_experience = format_experience(summary["经历"])
                    
                    st.markdown(f"""
                    <div style="border:1px solid #e0c88b; border-radius:10px; padding:20px; margin-bottom:20px; background-color:#fbf8f0;">
                        <h3 style="color:#a57c2c;">💼 主要经历</h3>
                        <div>{formatted_experience}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 提供下载选项
                    st_download = prepare_download_content(summary)
                    
                    st.download_button(
                        label="📥 下载分析结果",
                        data=st_download,
                        file_name=f"{uploaded_file.name.split('.')[0]}_分析结果.md",
                        mime="text/markdown"
                    )
                    
                except Exception as e:
                    st.error(f"处理失败: {str(e)}")
                    import traceback
                    st.error(traceback.format_exc())  # 显示详细错误信息，帮助调试
    
    # 添加页脚
    st.markdown("---")
    st.markdown("© 2025 简历分析工具 | 基于AI技术")

if __name__ == "__main__":
    main()