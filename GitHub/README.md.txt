# 🤖 AI 聊天助手 & 知识库

基于 Streamlit 和 DeepSeek 大模型构建的智能对话与文档问答系统。

## ✨ 功能
- 智能对话：与DeepSeek模型多轮聊天
- 文档问答：上传PDF/Word/TXT，基于文档内容回答问题

## 🛠️ 技术栈
- 前端：Streamlit
- 大模型：DeepSeek API
- RAG框架：LlamaIndex
- 嵌入模型：HuggingFace Embedding

## 🚀 快速开始
1. 安装依赖：`pip install -r requirements.txt`
2. 配置API Key：在 `.streamlit/secrets.toml` 中写入 `DEEPSEEK_API_KEY = "你的密钥"`
3. 运行聊天助手：`streamlit run app.py`
4. 运行知识库：`streamlit run rag_app.py`

## 👤 作者
你的名字 - 软件工程大二学生