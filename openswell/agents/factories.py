"""Surf recommender agent factory."""
from langchain_huggingface import HuggingFaceEndpoint
from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool
from openswell.core.config import Config, LlmProvider

def create_surf_recommender_agent(
    config: Config,
    tools: list[BaseTool],
) -> Runnable:
    """Create surf recommender agent."""
    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct",
        temperature=config.model_api.temperature,
    )

    return llm.bind(tools=tools)

def create_surf_recommender_llm(
    config: Config,
) -> Runnable:
    """Create surf recommender agent."""
    if config.model_api.provider == LlmProvider.OLLAMA:
        llm = ChatOpenAI(
            model=config.model_api.model, # "llama3"
            base_url=str(config.model_api.base_url),
            api_key=config.model_api.api_key,
            temperature=config.model_api.temperature,
            timeout=config.model_api.timeout,
            max_completion_tokens=config.model_api.max_tokens,
        )
    elif config.model_api.provider == LlmProvider.HUGGING_FACE:
        llm = HuggingFaceEndpoint(
            repo_id=config.model_api.model, #"tiiuae/falcon-7b-instruct",
            temperature=config.model_api.temperature,
            huggingfacehub_api_token=config.model_api.api_key,
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {config.model_api.provider}")

    return llm