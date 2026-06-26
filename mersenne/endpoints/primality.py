import logging

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from mersenne.dependencies import SettingsDep
from mersenne.services.lucas_lehmer import LucasLehmer

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/mersenne", tags=["Mersenne"])


class MersennePrimalityRequest(BaseModel):
    p: int = Field(
        # ge=3 is intrinsic (the Lucas-Lehmer domain), so it stays a static
        # constraint. The upper bound is an operational limit and is enforced
        # against settings.max_mersenne_exponent in the handler.
        ge=3,
        description=(
            "Exponent p of the Mersenne number M_p = 2^p - 1. Must be >= 3, "
            "the domain of the Lucas-Lehmer test. An environment-configured "
            "upper bound also applies."
        ),
        examples=[3, 11, 31],
    )


class MersennePrimalityResponse(BaseModel):
    p: int = Field(description="The exponent that was tested.")
    mersenne_number: str = Field(
        description=(
            "The Mersenne number M_p = 2^p - 1, as a decimal string. It is "
            "returned as a string because it can be thousands of digits long, "
            "well beyond the safe integer range of JSON/JavaScript clients."
        ),
    )
    is_prime: bool = Field(
        description="Whether the Mersenne number M_p = 2^p - 1 is prime."
    )


@router.post(
    "/primality",
    status_code=status.HTTP_200_OK,
    summary="Test a Mersenne number for primality",
    description=(
        "Runs the Lucas-Lehmer test to determine whether the Mersenne number "
        "M_p = 2^p - 1 is prime for the given exponent p."
    ),
)
def check_mersenne_primality(
    payload: MersennePrimalityRequest,
    settings: SettingsDep,
) -> MersennePrimalityResponse:
    if payload.p > settings.max_mersenne_exponent:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"p must be <= {settings.max_mersenne_exponent}.",
        )

    logger.info("Testing Mersenne number M_%d for primality.", payload.p)

    # Sync handler: the Lucas-Lehmer test is CPU-bound, so FastAPI runs it in a
    # threadpool instead of blocking the event loop.
    lucas_lehmer = LucasLehmer(payload.p)
    return MersennePrimalityResponse(
        p=payload.p,
        mersenne_number=str(lucas_lehmer.mersenne_number),
        is_prime=lucas_lehmer.test(),
    )
