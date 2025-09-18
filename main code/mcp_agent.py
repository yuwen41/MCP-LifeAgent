import os
import json
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.tool import ToolMessage


#openai API key setting
openai_api_key= os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("Please set OPENAI_API_KEY in your environment variables first")

os.environ["OPENAI_API_KEY"] = openai_api_key

#String encoding cleanup
def clean_input(text):
    return text.encode("utf-8", "ignore").decode("utf-8")

#Analyze the tools that were invoked
def extract_invoked_tools(messages):
    tool_names = []
    for msg in messages:
        if isinstance(msg, ToolMessage):
            tool_names.append(msg.name)# msg.name is the tool name
    return tool_names

#Build Client
async def build_agent():
    client = MultiServerMCPClient({
        "multi": {
            "url": "http://localhost:8001/mcp",
            "transport": "streamable_http",
        },
    })

    tools = await client.get_tools()
    print(tools)

    agent = create_react_agent("openai:gpt-4.1", tools)
    return agent



