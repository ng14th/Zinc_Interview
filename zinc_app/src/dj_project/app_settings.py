import os
import sys
from pathlib import Path
from typing import Optional

try:
    import core
except ModuleNotFoundError:
    current_path = Path(os.getcwd())
    sys.path.append(str(current_path.parents[0]))
    import core  # noqa

from core import constants
from .init_logger import create_console_logger


from core.settings import (
    DjangoSetting,
    DatabaseSettings,
    GunicornSetting
)


class AppSettings(
    DjangoSetting,
    DatabaseSettings,
    GunicornSetting
):
    APP_NAME: Optional[str] = 'Zinc'


__env_file_path = AppSettings.get_env_file_path(AppSettings.get_selected_env())
app_settings: AppSettings = AppSettings(_env_file=__env_file_path)
app_settings.setup(__env_file_path)

logger = create_console_logger(constants.CONSOLE_LOGGER)
