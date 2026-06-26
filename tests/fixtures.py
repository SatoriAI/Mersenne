import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from mersenne.app import create_app
from mersenne.settings import Settings, get_settings


@pytest.fixture
def test_settings() -> Settings:
    return Settings(
        app_name="Mersenne-Test",
        environment="local",
    )


@pytest.fixture
def app(test_settings: Settings) -> FastAPI:
    # Build the app from the test settings so construction-time config (docs,
    # title, CORS) is hermetic, and override the request-time dependency too.
    application = create_app(test_settings)
    application.dependency_overrides[get_settings] = lambda: test_settings
    return application


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
