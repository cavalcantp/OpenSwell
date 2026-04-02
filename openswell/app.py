"""Openswell service factory wrapper."""
from fastapi import FastAPI
from openswell.api import build_api

def create_service() -> FastAPI:
    return build_api()