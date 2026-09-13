# 创建一个网址
import streamlit as st          # 负责 UI（页面、输入框、消息气泡）
import requests                 # 负责和 DeepSeek 服务器通信

# Streamlit程序：每次用户任何操作，整个脚本从头到尾重跑一遍

# === 页面配置 ===
st.set_page_config(page_title="我的AI助手", page_icon="🤖")
st.title("🤖 我的AI聊天助手")     # 大标题
st.caption("由 DeepSeek 驱动")   # 小字

# === 侧边栏：配置API密钥 ===
with st.sidebar:
    st.header("⚙️ 配置")
    # type="password" 让输入变成圆点，防止密钥泄露
    api_key = st.text_input("请输入你的 DeepSeek API Key", type="password")
    st.markdown("[获取API密钥](https://platform.deepseek.com/)")

# === 核心：初始化聊天历史 ===
if "messages" not in st.session_state:              # 确保历史容器存在（只初始化一次）
    st.session_state.messages = []

# === 显示历史聊天记录 ===
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# === 核心：处理用户输入和AI回复 ===
if prompt := st.chat_input("有什么我可以帮你的吗？"):                   # st.chat_input 是底部的输入框
    # 1. 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. 调用API并显示AI回复
    if not api_key:
        st.warning("请在侧边栏输入你的 API Key")
        st.stop()

    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                response = requests.post(
                    "https://api.deepseek.com/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "model": "deepseek-chat",                   # deepseek-chat 是对话模型
                        "messages": st.session_state.messages       # session_state：负责"记住"对话历史（关键！）
                        # session_state 是一个跨脚本运行、持久存在的字典，专门用来存这类数据
                    },
                    timeout=60                                      # 防止请求卡死
                )
                if response.status_code == 200:
                    reply = response.json()["choices"][0]["message"]["content"]
                    '''
                    返回的 JSON 结构（OpenAI 兼容格式）：
                    {
                      "choices": [
                        {
                          "message": {
                            "role": "assistant",
                            "content": "你好！有什么可以帮你？"   ← 我们要的就是这个
                          }
                        }
                      ]
                    }
                    '''
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                else:
                    st.error(f"请求失败：{response.status_code}")
            except Exception as e:
                st.error(f"发生错误：{e}")