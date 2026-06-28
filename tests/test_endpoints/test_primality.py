import pytest
from fastapi import status
from fastapi.testclient import TestClient

from mersenne.app import create_app
from mersenne.settings import Settings


def test_returns_true_for_mersenne_prime(client: TestClient) -> None:
    # M_3 = 7 is prime.
    response = client.post("/mersenne/primality", json={"p": 3})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"p": 3, "mersenne_number": "7", "is_prime": True}


def test_returns_false_for_composite_mersenne_number(client: TestClient) -> None:
    # M_11 = 2047 = 23 x 89 is composite.
    response = client.post("/mersenne/primality", json={"p": 11})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"p": 11, "mersenne_number": "2047", "is_prime": False}


def test_large_mersenne_number_is_exact_string(client: TestClient) -> None:
    # M_61 exceeds the JS/JSON safe integer range; it must come back as an
    # exact decimal string with no precision loss.
    response = client.post("/mersenne/primality", json={"p": 61})

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["mersenne_number"] == str(2**61 - 1)
    assert isinstance(body["mersenne_number"], str)


@pytest.mark.parametrize("p", [2, 1, 0, -5])
def test_rejects_exponent_below_domain(client: TestClient, p: int) -> None:
    response = client.post("/mersenne/primality", json={"p": p})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_rejects_exponent_above_max(
    client: TestClient, test_settings: Settings
) -> None:
    response = client.post(
        "/mersenne/primality",
        json={"p": test_settings.max_mersenne_exponent + 1},
    )

    # Operational limit -> 400 (distinct from schema-validation 422).
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_max_exponent_is_configurable() -> None:
    # The ceiling is an operational setting, so a lower configured value must
    # reject an exponent that would otherwise be accepted.
    low_max = Settings(app_name="Mersenne-Test", max_mersenne_exponent=5)
    app = create_app(low_max)

    response = TestClient(app).post("/mersenne/primality", json={"p": 7})

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_rejects_malformed_body(client: TestClient) -> None:
    response = client.post("/mersenne/primality", json={})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
