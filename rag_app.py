import streamlit as st
import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.deepseek import DeepSeek

st.set_page_config(page_title="我的知识库", page_icon="📚")
st.title("📚 我的个人知识库助手")
st.caption("上传你的文档，问任何问题")

# === 侧边栏：配置 ===
with st.sidebar:
    st.header("⚙️ 配置")
    api_key = st.text_input("DeepSeek API Key", type="password")
    st.markdown("[获取密钥](https://platform.deepseek.com/)")

    st.header("📤 上传文档")
    uploaded_files = st.file_uploader(
        "支持 PDF、Word、TXT",
        accept_multiple_files=True,
        type=["pdf", "docx", "txt"]
    )

    if st.button("🚀 构建知识库") and api_key and uploaded_files:
        with st.spinner("正在读取和索引文档..."):
            # 保存上传的文件到临时目录
            os.makedirs("./temp_data", exist_ok=True)
            for file in uploaded_files:
                with open(f"./temp_data/{file.name}", "wb") as f:
                    f.write(file.getbuffer())

            # 设置模型
            Settings.llm = DeepSeek(
                model="deepseek-chat",
                api_key=api_key,
                api_base="https://api.deepseek.com/v1"
            )
            Settings.embed_model = HuggingFaceEmbedding(
                model_name="BAAI/bge-small-en-v1.5"
            )

            # 构建索引
            documents = SimpleDirectoryReader("./temp_data").load_data()
            index = VectorStoreIndex.from_documents(documents)
            st.session_state.index = index
            st.success(f"✅ 成功索引 {len(documents)} 个文档！")

# === 主界面：问答 ===
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("基于你的文档提问..."):
    if "index" not in st.session_state:
        st.warning("请先在左侧上传文档并构建知识库！")
        st.stop()

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("检索中..."):
            query_engine = st.session_state.index.as_query_engine()
            response = query_engine.query(prompt)
            st.markdown(str(response))
            st.session_state.messages.append({"role": "assistant", "content": str(response)})