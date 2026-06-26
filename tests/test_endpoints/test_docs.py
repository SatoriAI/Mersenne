from fastapi import status
from fastapi.testclient import TestClient

from mersenne.app import create_app
from mersenne.settings import Settings


def test_swagger_enabled_by_default(client: TestClient) -> None:
    assert client.get("/docs").status_code == status.HTTP_200_OK


def test_swagger_disabled_hides_only_swagger() -> None:
    app = create_app(Settings(app_name="Mersenne-Test", swagger_enabled=False))
    client = TestClient(app)

    # Swagger UI is gone...
    assert client.get("/docs").status_code == status.HTTP_404_NOT_FOUND

    # ...but ReDoc and the OpenAPI schema remain available.
    assert client.get("/redoc").status_code == status.HTTP_200_OK
    assert client.get("/openapi.json").status_code == status.HTTP_200_OK
