# FileHelper GPT

通过微信文件传输助手实现的个人 GPT 助理。

## 特性

- 使用 [LangChain](https://github.com/langchain-ai/langchain) 调用 LLM
- 对话上下文存储在本地 SQLite 数据库中
- Playwright 模拟浏览器与文件传输助手交互

## 使用

1. 安装依赖：`pip install -r requirements.txt`
2. 设置 `OPENAI_API_KEY` 环境变量
3. 运行 `python main.py`

输入 `#清除记忆` 可清空会话历史，输入 `#退出对话` 结束程序。
