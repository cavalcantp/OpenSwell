"""Surf recommender agent executor."""
from langchain_core.runnables import Runnable
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import Runnable
from openswell.agents.prompts import SYSTEM_PROMPT


async def run_surf_recommender_agent(agent: Runnable, user_input: str) -> str:
    """
    Executes one interaction loop:
    - send user message
    - model may call tool
    - tool executes automatically
    - final response returned
    """

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_input),
    ]

    response = await agent.ainvoke(messages)

    return response.content