from datetime import datetime

from fastapi import status
from fastapi.testclient import TestClient

from mersenne.app import create_app
from mersenne.settings import Settings


def test_status_returns_200_and_healthy(
    client: TestClient, test_settings: Settings
) -> None:
    response = client.get("/status")

    assert response.status_code == status.HTTP_200_OK

    body = response.json()
    assert body["status"] == "healthy"

    # Values come from the injected test settings, not hardcoded defaults.
    assert body["service"] == test_settings.app_name
    assert body["environment"] == test_settings.environment

    # timestamp is serialized as a parseable ISO-8601 datetime.
    assert isinstance(datetime.fromisoformat(body["timestamp"]), datetime)


def test_status_reflects_injected_settings() -> None:
    custom = Settings(app_name="OtherApp", environment="production")
    app = create_app(custom)
    response = TestClient(app).get("/status")
    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["service"] == "OtherApp"
    assert body["environment"] == "production"
