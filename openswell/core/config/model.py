from pydantic import BaseModel, Field, AnyHttpUrl
from enum import StrEnum

class LlmProvider(StrEnum):
    OPEN_AI = "OPEN_AI"
    TOGETHER_AI = "TOGETHER_AI"
    CLAUDE = "CLAUDE"
    HUGGING_FACE = "HUGGING_FACE"
    OLLAMA = "OLLAMA"

class ModelApiConfig(BaseModel):
    provider: LlmProvider = LlmProvider.OLLAMA
    model: str = "llama3"
    api_key: str = Field(
        default="ollama",
        description="Model provider API key."
    )
    base_url: AnyHttpUrl = Field(
        default=AnyHttpUrl("http://localhost:11434/v1"),
        description="URL for the Model API.",
    )
    temperature: float = 0.2
    timeout: int = 60
    max_tokens: int = 512
