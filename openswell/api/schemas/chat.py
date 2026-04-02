"""Schemas for Openswell API chat endpoint."""
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    message: str