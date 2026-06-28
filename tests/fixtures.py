import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from mersenne.app import create_app
from mersenne.settings import Settings


@pytest.fixture
def test_settings() -> Settings:
    return Settings(
        app_name="Mersenne-Test",
        environment="local",
    )


@pytest.fixture
def app(test_settings: Settings) -> FastAPI:
    return create_app(test_settings)


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
