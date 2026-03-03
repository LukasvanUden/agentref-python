from __future__ import annotations

import httpx
import pytest
import respx

from agentref._http import AsyncHttpClient, SyncHttpClient
from agentref.errors import ForbiddenError, ServerError


def test_get_retries_on_500() -> None:
    client = SyncHttpClient(api_key="ak_live_test", max_retries=2)
    call_count = {"count": 0}

    with respx.mock:
        def handler(request: httpx.Request) -> httpx.Response:
            call_count["count"] += 1
            if call_count["count"] < 3:
                return httpx.Response(
                    500,
                    json={"error": {"code": "INTERNAL_ERROR"}, "meta": {"requestId": "r"}},
                )
            return httpx.Response(200, json={"data": [], "meta": {"total": 0, "page": 1, "pageSize": 20, "hasMore": False, "requestId": "r"}})

        respx.get("https://www.agentref.dev/api/v1/programs").mock(side_effect=handler)
        payload = client.request("GET", "/programs")

    assert call_count["count"] == 3
    assert payload["meta"]["requestId"] == "r"
    client.close()


def test_post_no_retry_without_idempotency_key() -> None:
    client = SyncHttpClient(api_key="ak_live_test", max_retries=2)
    call_count = {"count": 0}

    with respx.mock:
        def handler(request: httpx.Request) -> httpx.Response:
            call_count["count"] += 1
            return httpx.Response(
                500,
                json={"error": {"code": "INTERNAL_ERROR"}, "meta": {"requestId": "r"}},
            )

        respx.post("https://www.agentref.dev/api/v1/programs").mock(side_effect=handler)

        with pytest.raises(ServerError):
            client.request("POST", "/programs", json={})

    assert call_count["count"] == 1
    client.close()


def test_post_retries_with_idempotency_key() -> None:
    client = SyncHttpClient(api_key="ak_live_test", max_retries=2)
    call_count = {"count": 0}

    with respx.mock:
        def handler(request: httpx.Request) -> httpx.Response:
            call_count["count"] += 1
            if call_count["count"] < 3:
                return httpx.Response(
                    500,
                    json={"error": {"code": "INTERNAL_ERROR"}, "meta": {"requestId": "r"}},
                )
            return httpx.Response(201, json={"data": {"id": "prog_1"}, "meta": {"requestId": "r"}})

        respx.post("https://www.agentref.dev/api/v1/programs").mock(side_effect=handler)

        payload = client.request("POST", "/programs", json={}, idempotency_key="key-123")

    assert call_count["count"] == 3
    assert payload["data"]["id"] == "prog_1"
    client.close()


def test_post_does_not_retry_with_empty_idempotency_key() -> None:
    client = SyncHttpClient(api_key="ak_live_test", max_retries=2)
    call_count = {"count": 0}

    with respx.mock:
        def handler(request: httpx.Request) -> httpx.Response:
            call_count["count"] += 1
            return httpx.Response(
                500,
                json={"error": {"code": "INTERNAL_ERROR"}, "meta": {"requestId": "r"}},
            )

        respx.post("https://www.agentref.dev/api/v1/programs").mock(side_effect=handler)

        with pytest.raises(ServerError):
            client.request("POST", "/programs", json={}, idempotency_key="")

    assert call_count["count"] == 1
    client.close()


def test_patch_no_retry_even_with_idempotency_key() -> None:
    client = SyncHttpClient(api_key="ak_live_test", max_retries=2)
    call_count = {"count": 0}

    with respx.mock:
        def handler(request: httpx.Request) -> httpx.Response:
            call_count["count"] += 1
            return httpx.Response(
                500,
                json={"error": {"code": "INTERNAL_ERROR"}, "meta": {"requestId": "r"}},
            )

        respx.patch("https://www.agentref.dev/api/v1/programs/p1").mock(side_effect=handler)

        with pytest.raises(ServerError):
            client.request("PATCH", "/programs/p1", json={"name": "x"}, idempotency_key="ignored")

    assert call_count["count"] == 1
    client.close()


def test_delete_no_retry() -> None:
    client = SyncHttpClient(api_key="ak_live_test", max_retries=2)
    call_count = {"count": 0}

    with respx.mock:
        def handler(request: httpx.Request) -> httpx.Response:
            call_count["count"] += 1
            return httpx.Response(
                500,
                json={"error": {"code": "INTERNAL_ERROR"}, "meta": {"requestId": "r"}},
            )

        respx.delete("https://www.agentref.dev/api/v1/programs/p1").mock(side_effect=handler)

        with pytest.raises(ServerError):
            client.request("DELETE", "/programs/p1")

    assert call_count["count"] == 1
    client.close()


def test_forbidden_error_on_403() -> None:
    client = SyncHttpClient(api_key="ak_live_test", max_retries=0)

    with respx.mock:
        respx.get("https://www.agentref.dev/api/v1/programs").return_value = httpx.Response(
            403,
            json={"error": {"code": "FORBIDDEN", "message": "Forbidden"}, "meta": {"requestId": "r"}},
        )

        with pytest.raises(ForbiddenError) as exc_info:
            client.request("GET", "/programs")

    assert exc_info.value.status == 403
    assert not isinstance(exc_info.value, ServerError)
    client.close()


def test_idempotency_key_sent_as_header() -> None:
    client = SyncHttpClient(api_key="ak_live_test")

    with respx.mock:
        route = respx.post("https://www.agentref.dev/api/v1/programs").mock(
            return_value=httpx.Response(201, json={"data": {}, "meta": {"requestId": "r"}})
        )

        client.request("POST", "/programs", json={}, idempotency_key="key-123")

    assert route.calls[0].request.headers["idempotency-key"] == "key-123"
    client.close()


@pytest.mark.asyncio
async def test_async_get_smoke() -> None:
    client = AsyncHttpClient(api_key="ak_live_test")

    with respx.mock:
        respx.get("https://www.agentref.dev/api/v1/programs").return_value = httpx.Response(
            200,
            json={"data": [], "meta": {"total": 0, "page": 1, "pageSize": 20, "hasMore": False, "requestId": "r"}},
        )

        payload = await client.request("GET", "/programs")

    assert payload["meta"]["requestId"] == "r"
    await client.__aexit__()
