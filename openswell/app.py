"""Openswell service factory wrapper."""
from fastapi import FastAPI
from openswell.api import build_api

def create_app() -> FastAPI:
    return build_api()