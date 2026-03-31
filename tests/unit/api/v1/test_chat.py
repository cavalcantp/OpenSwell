"""Unit tests for chat endpoint."""
from http import HTTPStatus
from pytest import fixture
from unittest.mock import patch
from fastapi.testclient import TestClient
from openswell.api.schemas import ChatRequest, ChatResponse
from openswell.api.routes.v1.endpoints import chat as chat_module
from langchain_core.runnables import Runnable
from openswell.services import GeocodeService, SurfRecommenderService

@fixture
def chat_request():
    return ChatRequest(
        message="I am an intermediate surfer trying to practice carves around Lisbon. What is the best spot for that today ?"
    )

@fixture
def workflow_response():
    return {"explanation":{"overall_summary": "The best spot based on your surfing level and current conditions is Ribeira D'Ilhas."}}

@fixture
def chat_response(
    workflow_response: dict[str, dict[str, str]],
):
    return ChatResponse(
        message=workflow_response["explanation"]["overall_summary"],
    )

def test_chat_endpoint_triggers_workflow_execution(
    client: TestClient,
    surf_recommender_llm: Runnable,
    geocoding_service: GeocodeService,
    surf_recommender_service: SurfRecommenderService,
    chat_request: ChatRequest,
    workflow_response: dict[str, dict[str, str]],
    chat_response: ChatResponse,
):
    with patch.object(
        target=chat_module,
        attribute="execute_workflow",
        return_value=workflow_response,
    ) as mock_execute_workflow:
        response = client.post(
            url="/api/v1/chat",
            content=chat_request.model_dump_json(),
        )

    mock_execute_workflow.assert_awaited_once_with(
        llm=surf_recommender_llm,
        surf_recommender_service=surf_recommender_service,
        geocoding_service=geocoding_service,
        user_input=chat_request.message,
    )

    assert response.status_code == HTTPStatus.OK
    assert ChatResponse.model_validate(response.json()) == chat_response 