import asyncio
from mcp_agent import build_agent, clean_input, extract_invoked_tools
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_core.messages.tool import ToolMessage


#In multi-turn conversations, retain paired messages consisting of AIMessage and ToolMessage
def clean_history(messages):
    clean = []
    i = 0
    while i < len(messages):
        msg = messages[i]
        #If an AI message includes a tool call（tool_calls is not empty）
        if isinstance(msg, AIMessage) and getattr(msg, "tool_calls", None):
            #and the next message is the corresponding tool response（ToolMessage）
            if i + 1 < len(messages) and isinstance(messages[i + 1], ToolMessage):
                clean.append(msg)
                clean.append(messages[i + 1])
                i += 2
                continue
        else:
            clean.append(msg)
        i += 1
    return clean

# Prompt and tool call be preserved
async def main():
    print("🤖 MCP Terminal Chat (type 'exit' to quit)\n")
    agent = await build_agent()
    messages = []

    # ✅ Add System Prompt
    system_prompt = (
        "You are a multi-tool collaborative AI assistant. Please make use of the currently available tools as much as possible to answer user questions, rather than relying solely on your built-in knowledge."
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


