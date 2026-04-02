"""Openswell settings class."""
import os
from importlib_metadata import version as package_version
from typing import ClassVar, Self
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from openswell.core.config.model import ModelApiConfig
from openswell.core.config.weather import WeatherApiConfig
from openswell.core.config.swell import SwellApiConfig
from openswell.core.config.spot import SpotStoreConfig
from openswell.core.config.geocode import GeocodeApiConfig

ENV_ENVIRONMENT = "OPENSWELL_ENV"

class Config(BaseSettings):
    DEFAULT_ENVIRONMENT: ClassVar[str] = "local"
    DEFAULT_SERVICE_NAME: ClassVar[str] = "openswell"

    model_api: ModelApiConfig = Field(
        default_factory=ModelApiConfig.model_construct,
        title="Model API config",
        description="Underlying foundation model API config."
    )

    weather_api: WeatherApiConfig = Field(
        default_factory=WeatherApiConfig.model_construct,
        title="Weather API config",
        description="Configuration to access weather API."
    )

    swell_api: SwellApiConfig = Field(
        default_factory=SwellApiConfig.model_construct,
        title="Swell API config",
        description="Configuration to access surf forecast API."
    )

    geocode_api: GeocodeApiConfig = Field(
        default_factory=GeocodeApiConfig.model_construct,
        title="Geocode API config",
        description="Configuration to access geocode API."
    )

    spot_store: SpotStoreConfig = Field(
        default_factory=SpotStoreConfig.model_construct,
        description="Configuration of the store of surfing spot descriptions."
    )

    model_config = SettingsConfigDict(
        env=os.environ.get(ENV_ENVIRONMENT, DEFAULT_ENVIRONMENT),
        env_prefix="openswell__",
        env_nested_delimiter="__",
        env_parse_none_str="null",
        nested_model_default_partial_update=True,
        extra="ignore",
    )

    @property
    def environment(self: Self) -> str:
        return self.model_config.get("env")
    
    @property
    def service_version(self: Self):
        """Get version of service package."""
        package_name = __name__.split(".")[0]
        return package_version(package_name)