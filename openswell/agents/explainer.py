"""Openswell explainer agent executor."""
import json
from langchain_core.runnables import Runnable
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import Runnable
from openswell.agents.prompts import EXPLANATION_PROMPT
from openswell.domain.models import Recommendation
from openswell.domain.models import ExplanationResponse
from openswell.agents.utils import extract_json


# def serialize_recommendations(results: list[Recommendation]) -> list[dict]:
#     return [
#         {
#             "spot_name": r.spot.name,
#             "score": r.score,
#             "swell_size": r.swell_size,
#             "swell_direction": r.swell_direction,
#             "wind_speed": r.wind_speed,
#             "wind_direction": r.wind_direction,
#         }
#         for r in results
#     ]


async def explain_recommendations(
    llm: Runnable,
    user_input: str,
    results: list[Recommendation],
) -> ExplanationResponse:

    # structured_results = serialize_recommendations(results)

    response = await llm.ainvoke([
        SystemMessage(content=EXPLANATION_PROMPT),
        HumanMessage(
            content=f"""
                User request: {user_input}
                Recommendations: {[r.model_dump_json() for r in results]}
                """ #json.dumps(structured_results, indent=2)}
        ),
        ]
    )

    data = extract_json(text=response.content)

    return ExplanationResponse(**data)