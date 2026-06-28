from typing import Annotated

from fastapi import Depends, Request

from mersenne.settings import Settings


def get_settings_from_state(request: Request) -> Settings:
    return request.app.state.settings


SettingsDep = Annotated[Settings, Depends(get_settings_from_state)]
