# Script para seed do banco Postgres fonte.

import argparse
import json
import os
import random
from datetime import date, datetime, timedelta, timezone
from math import pi, sin

from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import cursor as PostgresCursor
from psycopg2.extras import execute_values

DEFAULT_SEED_DAYS: int = 10
DEFAULT_BATCH_SIZE: int = 1000
DEFAULT_RANDOM_SEED: int = 42
DEFAULT_OUTPUT_PATH: str = "seed_info.json"

SEED_DAYS_ENV_NAME: str = "SEED_DAYS"
SEED_INFO_PATH_ENV_NAME: str = "SEED_INFO_PATH"
SOURCE_DATABASE_URL_ENV_NAME: str = "SOURCE_DATABASE_URL"
DATABASE_URL_ENV_NAME: str = "DATABASE_URL"

POSTGRESQL_PSYCOPG2_PREFIX: str = "postgresql+psycopg2://"
POSTGRESQL_PREFIX: str = "postgresql://"

FREQUENCY_MINUTES: int = 1
HOURS_PER_DAY: int = 24
FULL_CIRCLE_RADIANS: float = 2.0 * pi

ZERO_VALUE: float = 0.0
WIND_SPEED_MEAN: float = 8.0
WIND_SPEED_STANDARD_DEVIATION: float = 2.5
WIND_SPEED_POWER_EXPONENT: int = 3
POWER_COEFFICIENT: float = 0.08
POWER_NOISE_STANDARD_DEVIATION: float = 5.0

AMBIENT_TEMPERATURE_BASE: float = 18.0
AMBIENT_TEMPERATURE_AMPLITUDE: float = 7.0
AMBIENT_TEMPERATURE_NOISE_STANDARD_DEVIATION: float = 1.5

UTC_OFFSET_SUFFIX: str = "+00:00"
UTC_SUFFIX: str = "Z"
UTC_TIMEZONE: timezone = timezone.utc

DataRow = tuple[datetime, float, float, float]


# Normaliza a URL do Postgres para compatibilidade com psycopg2.
def normalize_pg_url(postgres_url: str) -> str:
    has_psycopg2_prefix = postgres_url.startswith(POSTGRESQL_PSYCOPG2_PREFIX)
    if not has_psycopg2_prefix:
        return postgres_url

    normalized_suffix = postgres_url.split(POSTGRESQL_PSYCOPG2_PREFIX, 1)[1]
    return POSTGRESQL_PREFIX + normalized_suffix


# Le argumentos de linha de comando e aplica defaults.
def parse_args() -> argparse.Namespace:
    description = (
        "Seed source Postgres with "
        f"{DEFAULT_SEED_DAYS} days of 1-min data"
    )
    parser = argparse.ArgumentParser(description=description)

    default_seed_days = int(
        os.getenv(SEED_DAYS_ENV_NAME, str(DEFAULT_SEED_DAYS))
    )
    start_date_help = (
        "YYYY-MM-DD (default: today-SEED_DAYS or "
        f"{DEFAULT_SEED_DAYS})"
    )

    parser.add_argument("--start-date", help=start_date_help)
    parser.add_argument("--days", type=int, default=default_seed_days)
    parser.add_argument(
        "--truncate",
        action="store_true",
        help="Truncate table before insert",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
    )
    parser.add_argument("--seed", type=int, default=DEFAULT_RANDOM_SEED)
    parser.add_argument(
        "--output",
        default=os.getenv(SEED_INFO_PATH_ENV_NAME, DEFAULT_OUTPUT_PATH),
    )

    return parser.parse_args()


# Gera linhas sinteticas para o intervalo solicitado.
def build_rows(
    start_timestamp: datetime,
    end_timestamp: datetime,
    seed: int,
) -> list[DataRow]:
    random.seed(seed)
    data_rows: list[DataRow] = []
    current_timestamp = start_timestamp

    while current_timestamp < end_timestamp:
        wind_speed = max(
            ZERO_VALUE,
            random.gauss(WIND_SPEED_MEAN, WIND_SPEED_STANDARD_DEVIATION),
        )
        wind_speed_power = wind_speed ** WIND_SPEED_POWER_EXPONENT
        power_value = max(
            ZERO_VALUE,
            wind_speed_power * POWER_COEFFICIENT
            + random.gauss(ZERO_VALUE, POWER_NOISE_STANDARD_DEVIATION),
        )

        day_fraction = current_timestamp.hour / HOURS_PER_DAY
        ambient_temperature = (
            AMBIENT_TEMPERATURE_BASE
            + AMBIENT_TEMPERATURE_AMPLITUDE
            * sin(FULL_CIRCLE_RADIANS * day_fraction)
            + random.gauss(
                ZERO_VALUE,
                AMBIENT_TEMPERATURE_NOISE_STANDARD_DEVIATION,
            )
        )

        data_rows.append(
            (current_timestamp, wind_speed, power_value, ambient_temperature)
        )
        current_timestamp += timedelta(minutes=FREQUENCY_MINUTES)

    return data_rows


# Garante que a tabela e o indice existam no banco fonte.
def ensure_table(cursor: PostgresCursor) -> None:
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS data (
          timestamp TIMESTAMP NOT NULL,
          wind_speed DOUBLE PRECISION,
          power DOUBLE PRECISION,
          ambient_temperature DOUBLE PRECISION
        );
        """
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_data_timestamp ON data (timestamp);"
    )


# Salva metadados do seed para rastreio em JSON.
def write_seed_info(
    path: str,
    start_timestamp: datetime,
    end_timestamp: datetime,
    rows: int,
) -> None:
    generated_at = datetime.now(UTC_TIMEZONE).isoformat()
    generated_at = generated_at.replace(UTC_OFFSET_SUFFIX, UTC_SUFFIX)
    payload = {
        "start_ts": start_timestamp.isoformat(),
        "end_ts": end_timestamp.isoformat(),
        "rows": rows,
        "frequency_minutes": FREQUENCY_MINUTES,
        "generated_at": generated_at,
    }
    with open(path, "w", encoding="utf-8") as file_handle:
        json.dump(payload, file_handle, indent=2)


# Fluxo principal: carrega env, gera dados e grava no Postgres.
def main() -> None:
    load_dotenv()
    arguments = parse_args()

    start_date_value = arguments.start_date
    if start_date_value:
        start_date = datetime.strptime(start_date_value, "%Y-%m-%d").date()
    else:
        current_date = date.today()
        start_date = current_date - timedelta(days=arguments.days)

    start_timestamp = datetime.combine(start_date, datetime.min.time())
    end_timestamp = start_timestamp + timedelta(days=arguments.days)

    database_url = os.getenv(SOURCE_DATABASE_URL_ENV_NAME)
    if not database_url:
        database_url = os.getenv(DATABASE_URL_ENV_NAME)
    if not database_url:
        raise SystemExit("SOURCE_DATABASE_URL is not set")

    normalized_url = normalize_pg_url(database_url)
    data_rows = build_rows(start_timestamp, end_timestamp, arguments.seed)

    with psycopg2.connect(normalized_url) as connection:
        with connection.cursor() as cursor:
            ensure_table(cursor)
            if arguments.truncate:
                cursor.execute("TRUNCATE TABLE data;")
        with connection.cursor() as cursor:
            execute_values(
                cursor,
                "INSERT INTO data "
                "(timestamp, wind_speed, power, ambient_temperature) "
                "VALUES %s",
                data_rows,
                page_size=arguments.batch_size,
            )

    write_seed_info(
        arguments.output,
        start_timestamp,
        end_timestamp,
        len(data_rows),
    )

    seed_message = (
        f"Seeded {len(data_rows)} rows from "
        f"{start_timestamp} to {end_timestamp}."
    )
    print(seed_message)

    info_message = f"Seed info written to {arguments.output}."
    print(info_message)


if __name__ == "__main__":
    main()
