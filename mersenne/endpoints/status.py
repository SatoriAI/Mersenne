from datetime import UTC, datetime

from fastapi import APIRouter, status
from pydantic import BaseModel

from mersenne.dependencies import SettingsDep

router = APIRouter(tags=["Status"])


class HealthCheckResponse(BaseModel):
    status: str
    service: str
    environment: str
    timestamp: datetime


@router.get(
    "/status",
    status_code=status.HTTP_200_OK,
    summary="Application health status",
    description="Returns the current operational status of the application.",
)
async def get_status(settings: SettingsDep) -> HealthCheckResponse:
    return HealthCheckResponse(
        status="healthy",
        service=settings.app_name,
        environment=settings.environment,
        timestamp=datetime.now(UTC),
    )
