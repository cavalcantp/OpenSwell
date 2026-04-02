"""Examplar unit tests for openswell API. 
Low coverage as this is a toy example"""
from http import HTTPStatus
from fastapi.testclient import TestClient

def test_api_health_check_endpoint_returns_ok(client: TestClient):
    response = client.get(url="/health")

    assert response.status_code == HTTPStatus.OK