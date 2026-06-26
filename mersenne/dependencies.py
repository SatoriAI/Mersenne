from typing import Annotated

from fastapi import Depends

from mersenne.settings import Settings, get_settings

SettingsDep = Annotated[Settings, Depends(get_settings)]
