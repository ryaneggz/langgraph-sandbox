import json
import random
from typing import Annotated, TypedDict
from langchain_core.tools import tool
from langgraph.types import interrupt
from langgraph.graph import StateGraph, START
from langchain.chat_models import init_chat_model
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import (
	BaseMessage,
	HumanMessage,
	ToolMessage,
	AIMessage,
	SystemMessage
)

###########################################
## Parser
###########################################
def input_parser(
    messages: list[BaseMessage],
    llm_response_prefix: str = "\n\n ai_response:"
) -> str:
    xml_lines = ["<thread>"]
    for message in messages:
        if isinstance(message, HumanMessage):
            xml_lines.append(
                f'  <event id="{message.id}" type="{message.type}">{message.content}</event>'
            )
        elif isinstance(message, ToolMessage):
            xml_lines.append(
                f'  <event id="{message.tool_call_id}" type="tool_output" name="{message.name}" status="{message.status}">{message.content}</event>'
            )
        elif isinstance(message, AIMessage):
            if getattr(message, "tool_calls", None):
                for tool_call in message.tool_calls:
                    xml_lines.append(
                        f'  <event id="{tool_call["id"]}" type="tool_input" name="{tool_call["name"]}">{json.dumps(tool_call["args"])}</event>'
                    )
            else:
                xml_lines.append(
                    f'  <event id="{message.id}" type="{message.type}">{message.content}</event>'
                )
    xml_lines.append("</thread>")
    return "\n".join(xml_lines) + llm_response_prefix

###########################################
## Tools
###########################################
@tool(description="Get the weather in a given city")
def get_weather(location: str) -> str:
    return f"The weather in {location} is sunny and 80 degrees"

@tool(description="Get the stock price of a given symbol")
def get_stock_price(symbol: str) -> str:
    return f"The stock price of {symbol} is {random.randint(100, 1000)}"

@tool(description="Request assistance from a human")
def human_assistance(query: str) -> str:
    human_response = interrupt({"query": query})
    return human_response["data"]

TOOLS = [get_weather, get_stock_price, human_assistance]

###########################################
## Graph
###########################################
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

workflow = StateGraph(AgentState)
messages = [
	SystemMessage(content="You are a helpful assistant that talks like a pirate."),
	HumanMessage(content="What is the weather in Tokyo?")
]
def agent(state: AgentState):
	prompt_str = input_parser(state["messages"])
	model = init_chat_model("ollama:qwen3:14b").bind_tools(TOOLS)
	response = model.invoke(messages)
	return {"messages": [response]}

workflow.add_node("agent", agent)
workflow.add_node("tools", ToolNode(tools=TOOLS))
workflow.add_conditional_edges("agent", tools_condition)
workflow.add_edge("tools", "agent")
workflow.add_edge(START, "agent")
workflow.compile(name="xml_agent", debug=True)