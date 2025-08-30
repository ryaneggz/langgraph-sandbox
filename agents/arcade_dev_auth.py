import os
 
# Import necessary classes and modules
from langchain_arcade import ArcadeToolManager
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode
 
arcade_api_key = os.environ["ARCADE_API_KEY"]
 
# Initialize the tool manager and fetch tools compatible with langgraph
tool_manager = ArcadeToolManager(api_key=arcade_api_key)
tools = tool_manager.get_tools(toolkits=["Gmail"])
tool_node = ToolNode(tools)
 
# Create a language model instance and bind it with the tools
model = init_chat_model(model="openai:gpt-5-nano", temperature=0.7, timeout=30)
model_with_tools = model.bind_tools(tools)

# Function to invoke the model and get a response
def call_agent(state: MessagesState):
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    # Return the updated message history
    return {"messages": [response]}
 
 
# Function to determine the next step in the workflow based on the last message
def should_continue(state: MessagesState):
    if state["messages"][-1].tool_calls:
        for tool_call in state["messages"][-1].tool_calls:
            if tool_manager.requires_auth(tool_call["name"]):
                return "authorization"
        return "tools"  # Proceed to tool execution if no authorization is needed
    return END  # End the workflow if no tool calls are present
 
 
# Function to handle authorization for tools that require it
def authorize(state: MessagesState, config: dict):
    user_id = config["configurable"].get("user_id")
    for tool_call in state["messages"][-1].tool_calls:
        tool_name = tool_call["name"]
        if not tool_manager.requires_auth(tool_name):
            continue
        auth_response = tool_manager.authorize(tool_name, user_id)
        if auth_response.status != "completed":
            # Prompt the user to visit the authorization URL
            print(f"Visit the following URL to authorize: {auth_response.url}")
 
            # Wait for the user to complete the authorization
            # and then check the authorization status again
            tool_manager.wait_for_auth(auth_response.id)
            if not tool_manager.is_authorized(auth_response.id):
                # This stops execution if authorization fails
                raise ValueError("Authorization failed")
 
    return {"messages": []}

# Build the workflow graph using StateGraph
workflow = StateGraph(MessagesState)

# Add nodes (steps) to the graph
workflow.add_node("agent", call_agent)
workflow.add_node("tools", tool_node)
workflow.add_node("authorization", authorize)

# Define the edges and control flow between nodes
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, ["authorization", "tools", END])
workflow.add_edge("authorization", "tools")
workflow.add_edge("tools", "agent")

# Set up memory for checkpointing the state
memory = MemorySaver()

# Compile the graph with the checkpointer
workflow.compile(checkpointer=memory)