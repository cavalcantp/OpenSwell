from pydantic import BaseModel, Field, AnyHttpUrl

class WeatherApiConfig(BaseModel):
    api_key: str = Field(
        default="default_key",
        description="Open Weather API key."
    )
    base_url: AnyHttpUrl = Field(
        default=AnyHttpUrl("http://localhost:8080"),
        description="URL for the Weather API.",
    )