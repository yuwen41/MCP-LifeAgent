import asyncio
from mcp_agent import build_agent, clean_input, extract_invoked_tools
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_core.messages.tool import ToolMessage


#在多輪對話中，保留 AIMessage + ToolMessage 成對的訊息
def clean_history(messages):
    clean = []
    i = 0
    while i < len(messages):
        msg = messages[i]
        #如果這則 AI 訊息呼叫了工具（tool_calls 不為空）
        if isinstance(msg, AIMessage) and getattr(msg, "tool_calls", None):
            #且下一則訊息是對應的工具回傳（ToolMessage）
            if i + 1 < len(messages) and isinstance(messages[i + 1], ToolMessage):
                clean.append(msg)
                clean.append(messages[i + 1])
                i += 2
                continue
        else:
            clean.append(msg)
        i += 1
    return clean

# Prompt 及呼叫 tool
async def main():
    print("🤖 MCP Terminal Chat (type 'exit' to quit)\n")
    agent = await build_agent()
    messages = []

    # ✅ 加入 System Prompt
    system_prompt = (
        "你是一位多工具協作型的 AI 助理，請盡量使用當前可用的工具來回答使用者問題，而不是僅依賴你內建的知識。"
    )
    messages.append(SystemMessage(content=system_prompt))

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        user_msg = HumanMessage(content=clean_input(user_input))
        messages.append(user_msg)

        print("🤖 Thinking...")
        try:
            response = await agent.ainvoke({"messages": clean_history(messages)})

            tools_used = extract_invoked_tools(response["messages"])
            if tools_used:
                print(f"[🛠️ Tools Used: {', '.join(tools_used)}]")

            for msg in response["messages"]:
                if isinstance(msg, ToolMessage):
                    print(f"[Tool Output] {msg.content}")
                elif isinstance(msg, AIMessage):
                    print(f"AI: {msg.content.strip()}")
                    messages.append(msg)

        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
