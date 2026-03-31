"""Openswell service function definition"""
from fastapi import FastAPI
from openswell.api import build_api_app

def create_app() -> FastAPI:
    return build_api_app()