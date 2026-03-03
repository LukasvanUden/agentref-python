from __future__ import annotations

from typing import Literal, Optional

from .._http import AsyncHttpClient, SyncHttpClient
from ..types.models import Flag, FlagStats, PaginatedResponse, ResolveFlagParams


class FlagsResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def list(
        self,
        *,
        status: Optional[str] = None,
        type: Optional[str] = None,
        affiliate_id: Optional[str] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponse[Flag]:
        envelope = self._http.request(
            "GET",
            "/flags",
            params={
                "status": status,
                "type": type,
                "affiliateId": affiliate_id,
                "cursor": cursor,
                "limit": limit,
                "page": page,
                "pageSize": page_size,
                "offset": offset,
            },
        )
        return PaginatedResponse[Flag].model_validate(envelope)

    def stats(self) -> FlagStats:
        envelope = self._http.request("GET", "/flags/stats")
        data = envelope.get("data", {})
        if not isinstance(data, dict):
            data = {}
        return FlagStats.model_validate(data)

    def resolve(
        self,
        id: str,
        *,
        status: Literal["reviewed", "dismissed", "confirmed"],
        note: Optional[str] = None,
        block_affiliate: bool = False,
        idempotency_key: Optional[str] = None,
    ) -> Flag:
        payload = ResolveFlagParams(
            status=status,
            note=note,
            block_affiliate=block_affiliate,
        ).model_dump(by_alias=True, exclude_none=True)

        envelope = self._http.request(
            "POST",
            f"/flags/{id}/resolve",
            json=payload,
            idempotency_key=idempotency_key,
        )
        return Flag.model_validate(envelope["data"])


class AsyncFlagsResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        status: Optional[str] = None,
        type: Optional[str] = None,
        affiliate_id: Optional[str] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponse[Flag]:
        envelope = await self._http.request(
            "GET",
            "/flags",
            params={
                "status": status,
                "type": type,
                "affiliateId": affiliate_id,
                "cursor": cursor,
                "limit": limit,
                "page": page,
                "pageSize": page_size,
                "offset": offset,
            },
        )
        return PaginatedResponse[Flag].model_validate(envelope)

    async def stats(self) -> FlagStats:
        envelope = await self._http.request("GET", "/flags/stats")
        data = envelope.get("data", {})
        if not isinstance(data, dict):
            data = {}
        return FlagStats.model_validate(data)

    async def resolve(
        self,
        id: str,
        *,
        status: Literal["reviewed", "dismissed", "confirmed"],
        note: Optional[str] = None,
        block_affiliate: bool = False,
        idempotency_key: Optional[str] = None,
    ) -> Flag:
        payload = ResolveFlagParams(
            status=status,
            note=note,
            block_affiliate=block_affiliate,
        ).model_dump(by_alias=True, exclude_none=True)

        envelope = await self._http.request(
            "POST",
            f"/flags/{id}/resolve",
            json=payload,
            idempotency_key=idempotency_key,
        )
        return Flag.model_validate(envelope["data"])
