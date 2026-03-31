"""Openswell intent extractor agent executor."""
from langchain_core.runnables import Runnable
from langchain_core.messages import HumanMessage, SystemMessage
from openswell.agents.prompts import INTENT_PROMPT
from openswell.domain.models import SurfIntent
from openswell.agents.utils import extract_json

async def extract_intent(llm: Runnable, user_input: str) -> SurfIntent:
    response = await llm.ainvoke([
        SystemMessage(content=INTENT_PROMPT),
        HumanMessage(content=user_input),
    ])

    data = extract_json(text=response.content)

    return SurfIntent(**data)