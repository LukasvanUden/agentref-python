from __future__ import annotations

from typing import Any, Dict, List, Optional

from .._http import AsyncHttpClient, SyncHttpClient
from ..types.models import Conversion, ConversionStats, PaginatedResponse


class ConversionsResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def list(
        self,
        *,
        program_id: Optional[str] = None,
        affiliate_id: Optional[str] = None,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        from_: Optional[str] = None,
        to: Optional[str] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponse[Conversion]:
        envelope = self._http.request(
            "GET",
            "/conversions",
            params={
                "programId": program_id,
                "affiliateId": affiliate_id,
                "status": status,
                "startDate": start_date,
                "endDate": end_date,
                "from": from_,
                "to": to,
                "cursor": cursor,
                "limit": limit,
                "page": page,
                "pageSize": page_size,
                "offset": offset,
            },
        )
        return PaginatedResponse[Conversion].model_validate(envelope)

    def stats(self, *, program_id: Optional[str] = None, period: Optional[str] = None) -> ConversionStats:
        envelope = self._http.request(
            "GET",
            "/conversions/stats",
            params={"programId": program_id, "period": period},
        )
        data = envelope.get("data", {})
        if not isinstance(data, dict):
            data = {}
        return ConversionStats.model_validate(data)

    def recent(self, *, limit: Optional[int] = None) -> List[Conversion]:
        envelope = self._http.request("GET", "/conversions/recent", params={"limit": limit})
        raw = envelope.get("data", [])
        if not isinstance(raw, list):
            return []
        return [Conversion.model_validate(item) for item in raw]


class AsyncConversionsResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        program_id: Optional[str] = None,
        affiliate_id: Optional[str] = None,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        from_: Optional[str] = None,
        to: Optional[str] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponse[Conversion]:
        envelope = await self._http.request(
            "GET",
            "/conversions",
            params={
                "programId": program_id,
                "affiliateId": affiliate_id,
                "status": status,
                "startDate": start_date,
                "endDate": end_date,
                "from": from_,
                "to": to,
                "cursor": cursor,
                "limit": limit,
                "page": page,
                "pageSize": page_size,
                "offset": offset,
            },
        )
        return PaginatedResponse[Conversion].model_validate(envelope)

    async def stats(self, *, program_id: Optional[str] = None, period: Optional[str] = None) -> ConversionStats:
        envelope = await self._http.request(
            "GET",
            "/conversions/stats",
            params={"programId": program_id, "period": period},
        )
        data = envelope.get("data", {})
        if not isinstance(data, dict):
            data = {}
        return ConversionStats.model_validate(data)

    async def recent(self, *, limit: Optional[int] = None) -> List[Conversion]:
        envelope = await self._http.request("GET", "/conversions/recent", params={"limit": limit})
        raw = envelope.get("data", [])
        if not isinstance(raw, list):
            return []
        return [Conversion.model_validate(item) for item in raw]
