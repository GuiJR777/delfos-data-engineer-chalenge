# Constantes do banco alvo.

TARGET_DATABASE_URL_ENV_NAME: str = "TARGET_DATABASE_URL"
DATABASE_URL_ENV_NAME: str = "DATABASE_URL"

MISSING_TARGET_DATABASE_URL_MESSAGE: str = (
    "TARGET_DATABASE_URL is not set"
)

SIGNAL_TABLE_NAME: str = "signal"
DATA_TABLE_NAME: str = "data"

SIGNAL_NAME_MAX_LENGTH: int = 128

DATA_UNIQUE_CONSTRAINT_NAME: str = "uq_data_timestamp_signal"

DEFAULT_SIGNAL_NAMES: tuple[str, ...] = (
    "wind_speed_mean",
    "wind_speed_min",
    "wind_speed_max",
    "wind_speed_std",
    "power_mean",
    "power_min",
    "power_max",
    "power_std",
)

