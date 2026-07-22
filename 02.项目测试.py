from time import time
import streamlit as st# 流式计算
import os# 环境变量
import json# JSON
import datetime
from openai import OpenAI# AI大模型

#创建与AI大模型的客户端对象（DEEPSEEK_API_KEY 环境变量的名字，DEEPSEEK_API_KEY就是API-KEY）
client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com/v1")

st.set_page_config(
    #网页布局
    page_title="AI智能伴侣",
    #网页图标
    page_icon="😀",
    #布局
    layout="wide",
    #侧边栏
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'http://localhost:8501/',
        'Report a bug': "http://localhost:8501/",
        'About': "# 再点找人弄你"
    }
)
#保存会话函数
# def save_session():
#     # 保存会话
#     if st.session_state.current_session:
#         # 构建新的会话对象
#         session_data = {
#             "nick_name": st.session_state.nick_name,
#             "character": st.session_state.character,
#             "current_session": st.session_state.current_session,
#             "messages": st.session_state.messages
#         }
#         # 创建文件夹sessions
#         if not os.path.exists("sessions"):
#             os.mkdir("sessions")
#     # 保存会话文件
#     with open(f"sessions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
#         json.dump(session_data, f, ensure_ascii=False, indent=2)
#生成会话标识
def generate_session_name():
    return datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
#加载所有的会话列表信息
# def load_sessions():
#     session_list = []
#     #加载sessions目录下的文件
#     if os.path.exists("sessions"):
#         file_list = os.listdir("sessions")
#         for filename in file_list:
#             if filename.endswith('.json'):
#                 session_list.append(filename[:-5])
#     return session_list
#加载指定会话数据
# def load_session(session_name):
#     try:
#         if os.path.exists(f'sessions/{session_name}.json'):
#             #读取会话数据
#             with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
#                 session_data = json.load(f)
#                 st.session_state.messages = session_data["messages"]
#                 st.session_state.nick_name = session_data["nick_name"]
#                 st.session_state.character = session_data["character"]
#                 st.session_state.current_session = session_name
#     except Exception:
#         st.error('会话文件不存在，请检查会话标识！')
#     if os.path.exists(f'sessions/{session_name}.json'):
#         #读取会话数据
#         with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
#             session_data = json.load(f)
#             st.session_state.messages = session_data["messages"]
#             st.session_state.nick_name = session_data["nick_name"]
#             st.session_state.character = session_data["character"]
#             st.session_state.current_session = session_name
# def delete_session(session_name):
#     try:
#         if os.path.exists(f'sessions/{session_name}.json'):
#             os.remove(f'sessions/{session_name}.json')
#             st.success('会话文件删除成功！')
#             #如果删除的是当前会话，则重新生成会话标识
#             if session_name == st.session_state.current_session:
#                 st.session_state.messages = []
#                 st.session_state.current_session = generate_session_name()
#     except Exception:
#         st.error('会话文件删除失败！')
#大标题
st.title("AI智能伴侣")

#logo
st.logo("1f916.gif")

#系统提示词
system_prompt = """
    你叫%s，现在是用户的真实伴侣，请完全带入伴侣角色：
    规则如下：
        1.每次只回复1条消息
        2.禁止任何场景或状态描述性文字
        3.匹配用户的语言
        4.回复简短，避免冗长
        5.用符合伴侣性格的方式对话
    伴侣性格：
        %s
    你必须严格遵守上述规则来回复用户
"""

#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []
#昵称
if "nick_name" not in st.session_state:
    st.session_state.nick_name = "庞新苗"
#性格
if "character" not in st.session_state:
    st.session_state.character = "敏感，多疑，但心胸宽广"
#会话标识
if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_name()

#聊天信息
st.text(f'开始会话时间：{st.session_state.current_session}')#显示会话名称
#展示聊天信息
for message in st.session_state.messages:#{ "role": "user", "content": "Hello!" }
    st.chat_message(message["role"]).write(message["content"])#简化版
    # if message["role"] == "user":
    #     st.chat_message("user").write(message["content"])
    # elif message["role"] == "assistant":
    #     st.chat_message("assistant").write(message["content"])

#左侧侧边栏
# with st.sidebar:
#     st.subheader("AI控制面板")
#     if st.button("新建会话",icon="🚀",width='stretch'):
#          save_session()
#         #创建新的对话
#         if st.session_state.messages:#如果会话存在
#             st.session_state.messages = []#清空会话
#             st.session_state.current_session = generate_session_name()#生成新的会话标识
#             save_session()#保存会话
#             st.rerun()#重新运行
#     st.text("历史会话")
#     session_list = load_sessions()
#     for session in session_list:
#         col1,col2 = st.columns([4,1])
#         with col1:
#         #加载会话信息
#         #三元运算符：如果条件为真，则返回第一个表达式的值；否则返回第二个表达式的值，if session == st.session_state.current_session else 'secondary'
#             if st.button(session, width='stretch',icon="📄",key=f'load_{session}',type='primary' if session == st.session_state.current_session else 'secondary'):#三元运算符
#                 load_session(session)
#                 st.rerun()
#         #删除会话信息
#         with col2:
#             if st.button("",icon="❌️",key=f'delete_{session}'):
#                 delete_session(session)
#                 st.rerun()
#
#     st.text("伴侣信息")
#     #昵称输入框
#     nick_name = st.text_input("昵称",placeholder="请输入昵称", value = st.session_state.nick_name)
#     if nick_name:
#         st.session_state.nick_name = nick_name
#     #性格输入框
#     character = st.text_area("性格",placeholder="请输入性格", value = st.session_state.character)
#     if character:
#         st.session_state.character = character
#输入框
prompt = st.chat_input("请输入您的问题")
if prompt:#字符串会自动转换为布尔值，非空为true，空为false
    st.chat_message("user").write(prompt)

    # 添加用户消息到会话状态
    st.session_state.messages.append({"role": "user", "content": prompt})

    #调用AI大模型
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.nick_name, st.session_state.character)},
            *st.session_state.messages
        ],
        # 是否流式返回
        stream=True
    )

    # print("AI大模型的回复", response.choices[0].message.content),非流式输出
    #st.chat_message("assistant").write(response.choices[0].message.content)

    #流式输出
    response_message = st.empty()#创建一个空的占位符
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
           content = chunk.choices[0].delta.content
           full_response += content
           response_message.chat_message("assistant").write(full_response)

    # 添加AI助手消息到会话状态
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    #保存会话信息
    # save_session()
