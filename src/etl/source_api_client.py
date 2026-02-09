# Cliente da API fonte.

from collections.abc import Sequence
import logging
from typing import Any

import httpx

from etl.constants import API_DATA_PATH

LOGGER = logging.getLogger(__name__)

EMPTY_RESPONSE_MESSAGE: str = "Source API returned an empty payload"
INVALID_RESPONSE_MESSAGE: str = "Source API returned a non-list payload"
REQUEST_FAILED_MESSAGE: str = "Source API request failed"


class SourceApiClient:
    def __init__(
        self,
        base_url: str,
        timeout_seconds: float,
        retry_attempts: int,
        api_limit: int,
        api_offset: int,
    ) -> None:
        self._base_url = base_url
        self._timeout_seconds = timeout_seconds
        self._retry_attempts = retry_attempts
        self._api_limit = api_limit
        self._api_offset = api_offset
        self._http_client = httpx.Client(
            base_url=self._base_url,
            timeout=self._timeout_seconds,
        )

    def do_close(self) -> None:
        self._http_client.close()

    def do_fetch_data(
        self,
        start_timestamp: str,
        end_timestamp: str,
        signal_names: Sequence[str],
    ) -> list[dict[str, Any]]:
        data_rows: list[dict[str, Any]] = []
        offset_value = self._api_offset
        limit_value = self._api_limit

        while True:
            page_rows = self._do_fetch_page(
                start_timestamp=start_timestamp,
                end_timestamp=end_timestamp,
                signal_names=signal_names,
                limit_value=limit_value,
                offset_value=offset_value,
            )
            data_rows.extend(page_rows)
            has_more_rows = len(page_rows) == limit_value
            if not has_more_rows:
                break
            offset_value = offset_value + limit_value

        return data_rows

    def _do_fetch_page(
        self,
        start_timestamp: str,
        end_timestamp: str,
        signal_names: Sequence[str],
        limit_value: int,
        offset_value: int,
    ) -> list[dict[str, Any]]:
        attempt_number = 0
        while attempt_number < self._retry_attempts:
            attempt_number = attempt_number + 1
            try:
                response = self._http_client.get(
                    API_DATA_PATH,
                    params={
                        "start": start_timestamp,
                        "end": end_timestamp,
                        "signals": list(signal_names),
                        "limit": limit_value,
                        "offset": offset_value,
                    },
                )
                response.raise_for_status()
                payload = response.json()
                is_list_payload = isinstance(payload, list)
                if not is_list_payload:
                    raise RuntimeError(INVALID_RESPONSE_MESSAGE)
                has_payload = bool(payload)
                if not has_payload:
                    LOGGER.info(
                        "%s for %s to %s",
                        EMPTY_RESPONSE_MESSAGE,
                        start_timestamp,
                        end_timestamp,
                    )
                return payload
            except httpx.RequestError as error:
                LOGGER.warning(
                    "%s on attempt %s: %s",
                    REQUEST_FAILED_MESSAGE,
                    attempt_number,
                    error,
                )
            except httpx.HTTPStatusError as error:
                LOGGER.warning(
                    "%s on attempt %s: %s",
                    REQUEST_FAILED_MESSAGE,
                    attempt_number,
                    error,
                )

        raise RuntimeError(REQUEST_FAILED_MESSAGE)

