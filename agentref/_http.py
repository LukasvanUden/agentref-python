from __future__ import annotations

import asyncio
import importlib.metadata
import os
import time
from email.utils import parsedate_to_datetime
from typing import Any, Dict, Mapping, Optional, Set, cast

import httpx

from .errors import (
    AgentRefError,
    AuthError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)

_SAFE_METHODS: Set[str] = {"GET", "HEAD"}
_DEFAULT_BASE_URL = "https://www.agentref.dev/api/v1"
_DEFAULT_TIMEOUT = 30.0
_DEFAULT_MAX_RETRIES = 2


def _sdk_version() -> str:
    try:
        return importlib.metadata.version("agentref")
    except importlib.metadata.PackageNotFoundError:
        return "unknown"


def _parse_retry_after_seconds(value: Optional[str]) -> int:
    if not value:
        return 60

    try:
        parsed = float(value)
        if parsed >= 0:
            return int(parsed) if parsed.is_integer() else int(parsed) + 1
    except ValueError:
        pass

    try:
        parsed_date = parsedate_to_datetime(value)
        delta = parsed_date.timestamp() - time.time()
        if delta <= 0:
            return 0
        return int(delta) if float(delta).is_integer() else int(delta) + 1
    except (TypeError, ValueError, OverflowError):
        return 60


def _can_retry(method: str, idempotency_key: Optional[str]) -> bool:
    upper = method.upper()
    return upper in _SAFE_METHODS or (upper == "POST" and _has_usable_idempotency_key(idempotency_key))


def _has_usable_idempotency_key(idempotency_key: Optional[str]) -> bool:
    return isinstance(idempotency_key, str) and idempotency_key.strip() != ""


def _json_object(response: httpx.Response) -> Dict[str, Any]:
    try:
        payload = response.json()
    except ValueError:
        return {}

    if isinstance(payload, dict):
        return cast(Dict[str, Any], payload)

    return {}


class _BaseHttpClient:
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = _DEFAULT_TIMEOUT,
        max_retries: int = _DEFAULT_MAX_RETRIES,
    ) -> None:
        resolved_key = api_key or os.environ.get("AGENTREF_API_KEY")
        if not resolved_key:
            raise ValueError(
                "[AgentRef] API key is required. Pass it as api_key or set AGENTREF_API_KEY environment variable."
            )

        self._api_key = resolved_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._user_agent = f"agentref-python/{_sdk_version()}"

    def _headers(self, method: str, idempotency_key: Optional[str]) -> Dict[str, str]:
        headers: Dict[str, str] = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "User-Agent": self._user_agent,
        }

        if method.upper() == "POST" and _has_usable_idempotency_key(idempotency_key):
            assert idempotency_key is not None
            headers["Idempotency-Key"] = idempotency_key.strip()

        return headers

    def _parse_error(self, response: httpx.Response) -> AgentRefError:
        payload = _json_object(response)
        raw_error = payload.get("error")
        raw_meta = payload.get("meta")

        error = raw_error if isinstance(raw_error, dict) else {}
        meta = raw_meta if isinstance(raw_meta, dict) else {}

        code = cast(str, error.get("code", "UNKNOWN_ERROR"))
        message = cast(str, error.get("message", response.reason_phrase))
        request_id = cast(str, meta.get("requestId", ""))
        details = error.get("details")

        if response.status_code == 400:
            return ValidationError(message, code, request_id, details)
        if response.status_code == 401:
            return AuthError(message, code, request_id)
        if response.status_code == 403:
            return ForbiddenError(message, code, request_id)
        if response.status_code == 404:
            return NotFoundError(message, code, request_id)
        if response.status_code == 409:
            return ConflictError(message, code, request_id)
        if response.status_code == 429:
            retry_after = _parse_retry_after_seconds(response.headers.get("Retry-After"))
            return RateLimitError(message, code, request_id, retry_after)

        return ServerError(message, code, response.status_code, request_id)

    @staticmethod
    def _is_retryable(status: int) -> bool:
        return status == 429 or status >= 500

    @staticmethod
    def _backoff_seconds(attempt: int) -> float:
        return float(0.5 * (2 ** attempt))


class SyncHttpClient(_BaseHttpClient):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._client = httpx.Client(base_url=self._base_url, timeout=self._timeout)

    def close(self) -> None:
        self._client.close()

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        can_retry = _can_retry(method, idempotency_key)
        attempts = self._max_retries + 1 if can_retry else 1

        for attempt in range(attempts):
            try:
                response = self._client.request(
                    method,
                    path,
                    params={k: v for k, v in (params or {}).items() if v is not None},
                    json=json,
                    headers=self._headers(method, idempotency_key),
                )
            except httpx.HTTPError:
                if can_retry and attempt < attempts - 1:
                    time.sleep(self._backoff_seconds(attempt))
                    continue
                raise

            if response.is_error:
                parsed = self._parse_error(response)
                if can_retry and self._is_retryable(response.status_code) and attempt < attempts - 1:
                    delay = (
                        float(_parse_retry_after_seconds(response.headers.get("Retry-After")))
                        if response.status_code == 429
                        else self._backoff_seconds(attempt)
                    )
                    time.sleep(delay)
                    continue
                raise parsed

            return _json_object(response)

        raise ServerError("Request failed after retries", "REQUEST_RETRY_EXHAUSTED", 500, "")


class AsyncHttpClient(_BaseHttpClient):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._client = httpx.AsyncClient(base_url=self._base_url, timeout=self._timeout)

    async def __aenter__(self) -> "AsyncHttpClient":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self._client.aclose()

    async def aclose(self) -> None:
        await self._client.aclose()

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        can_retry = _can_retry(method, idempotency_key)
        attempts = self._max_retries + 1 if can_retry else 1

        for attempt in range(attempts):
            try:
                response = await self._client.request(
                    method,
                    path,
                    params={k: v for k, v in (params or {}).items() if v is not None},
                    json=json,
                    headers=self._headers(method, idempotency_key),
                )
            except httpx.HTTPError:
                if can_retry and attempt < attempts - 1:
                    await asyncio.sleep(self._backoff_seconds(attempt))
                    continue
                raise

            if response.is_error:
                parsed = self._parse_error(response)
                if can_retry and self._is_retryable(response.status_code) and attempt < attempts - 1:
                    delay = (
                        float(_parse_retry_after_seconds(response.headers.get("Retry-After")))
                        if response.status_code == 429
                        else self._backoff_seconds(attempt)
                    )
                    await asyncio.sleep(delay)
                    continue
                raise parsed

            return _json_object(response)

        raise ServerError("Request failed after retries", "REQUEST_RETRY_EXHAUSTED", 500, "")
