from pydantic import BaseModel, Field, AnyHttpUrl

class SwellApiConfig(BaseModel):
    api_key: str = Field(
        default="default_key",
        description="StormGlass API key."
    )
    base_url: AnyHttpUrl = Field(
        default=AnyHttpUrl("http://localhost:8082"),
        description="URL for the Swell API.",
    )