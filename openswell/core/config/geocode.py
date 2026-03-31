from pydantic import BaseModel, Field, AnyHttpUrl

class GeocodeApiConfig(BaseModel):
    base_url: AnyHttpUrl = AnyHttpUrl("https://nominatim.openstreetmap.org/search")