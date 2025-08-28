import art
from art.langgraph import wrap_rollout, init_chat_model
from art.local import LocalBackend
from langgraph import create_react_agent
from typing import List

def search_inbox(query: str, limit: int = 5) -> str:
    """Search emails with improved functionality."""
    # Simulate email search with realistic results
    results = [
        f"Email {i}: Subject matching '{query}' from user@example.com"
        for i in range(min(limit, 3))
    ]
    return "\n".join(results) if results else "No emails found."

def read_email(email_id: str) -> str:
    """Read email with error handling."""
    if not email_id.isdigit():
        return "Error: Invalid email ID format"
    return f"Email {email_id}: [Email content here...]"

def return_final_answer(answer: str) -> str:
    """Return the final answer to the user."""
    return f"Final Answer: {answer}"

tools = [search_inbox, read_email, return_final_answer]

async def train_advanced_email_agent():
    with LocalBackend() as backend:
        model = art.TrainableModel(
            name="advanced-email-agent",
            project="email-agents",
            base_model="Qwen/Qwen2.5-7B-Instruct",
        )

        await backend.register_model(model)

        @wrap_rollout(model)
        async def run_email_agent(scenario: str) -> art.Trajectory:
            agent = create_react_agent(init_chat_model(), tools)

            result = await agent.ainvoke({
                "messages": [("user", scenario)]
            })

            return art.Trajectory()

        # Diverse training scenarios
        scenarios = [
            "Find the most recent email from the finance team about Q4 budget",
            "Search for emails containing 'meeting' and summarize the key points",
            "Look for urgent emails from management and provide a brief overview",
            "Find emails about project deadlines and list them by priority",
        ]

        # Generate training trajectories
        for scenario in scenarios:
            trajectory = await run_email_agent(scenario)
            print(f"Generated trajectory for: {scenario}")

        # Train with RULER
        await art.train(model, reward_function="ruler")

if __name__ == "__main__":
    import asyncio
    asyncio.run(train_advanced_email_agent())