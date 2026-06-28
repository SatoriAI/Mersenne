import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mersenne.settings import Settings, get_settings
from mersenne.logging_config import configure_logging
from mersenne.endpoints.status import router as status_router
from mersenne.endpoints.primality import router as primality_router

logger = logging.getLogger(__name__)


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()

    configure_logging(settings.log_level)

    # Toggle only the Swagger UI; ReDoc and the OpenAPI schema stay enabled.
    application = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        docs_url=settings.swagger_endpoint if settings.swagger_enabled else None,
    )
    # Single source of truth for request-time settings (see SettingsDep). Set
    # before routers/middleware so any later wiring can rely on it.
    application.state.settings = settings

    # allow_credentials=True is incompatible with allow_origins=["*"]; list explicit origins in env.
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )

    application.include_router(status_router)
    application.include_router(primality_router)

    logger.info(
        "Application configured successfully.",
        extra={"environment": settings.environment},
    )

    return application


app = create_app()
