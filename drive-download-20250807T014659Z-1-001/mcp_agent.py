import os
import json
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.tool import ToolMessage


#openai API key 設置
openai_api_key= os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("請先在環境變數中設定 OPENAI_API_KEY")

os.environ["OPENAI_API_KEY"] = openai_api_key

#字串編碼清理
def clean_input(text):
    return text.encode("utf-8", "ignore").decode("utf-8")

#分析被取用的工具
def extract_invoked_tools(messages):
    tool_names = []
    for msg in messages:
        if isinstance(msg, ToolMessage):
            tool_names.append(msg.name)# msg.name 為工具名稱
    return tool_names

#建立 Client
async def build_agent():
    client = MultiServerMCPClient({
        "multi": {
            "url": "http://localhost:8001/mcp/",
            "transport": "streamable_http",
        },
        # "math": {
        #     "url": "http://localhost:8000/mcp/",
        #     "transport": "streamable_http",
        # },
    })

    tools = await client.get_tools()
    print(tools)

    agent = create_react_agent("openai:gpt-4.1", tools)
    return agent
