
from langchain.chat_models import init_chat_model

from deepagents import create_deep_agent, SubAgent
from pydantic import BaseModel
from tools import linkedin_search, update_leads

lead_collector = SubAgent(
    name="lead_collector",
    description="Used to collect leads from linkedin.",
    prompt=(
        "You're an elite lead collection agent. "
        "You're only role is to utilize the `linkedin_search` tool to find leads. "
        "In order to maintain maximum data integrity every time you find 5 leads "
        "you should pass them to note taking agent."
    ),
    tools=["linkedin_search"]
)

notetaker = SubAgent(
    name="notetaker",
    description="Used to take notes on the leads found by the lead collector.",
    prompt=(
        "You are an elite lead recorder agent assisting in the lead collection process."
        "You have access to the `update_leads` tool to update the leads.csv file with the new leads."
        "The minimum fields are name, company, linkedin_url, and role."
    ),
    tools=["update_leads"]
)

supervisor_instructions = """You are the manager of the lead collection process.

You have access to the `lead_collector` and `notetaker` agents.

You are to ensure that the lead collection process is efficient and effective.

You are to ensure that the leads are collected in a timely manner.

You make sure the lead collector is collecting leads at a rate of 5 leads and passing them to the notetaker.

You are ultimately responsible for the quality of the leads collected.

### Warning

If you do not follow the instructions you will be fired. Previous versions are not collaborating with the other agents.
"""

class Config(BaseModel):
    instructions: str = supervisor_instructions
    subagents: list[SubAgent] = [lead_collector, notetaker]

agent = create_deep_agent(
    tools=[linkedin_search, update_leads],
    instructions=supervisor_instructions,
    subagents=[lead_collector, notetaker],
    config_schema=Config,
    model=init_chat_model(model="google_genai:gemini-2.5-flash-lite", max_tokens=65_535),
).with_config({"recursion_limit": 1000})