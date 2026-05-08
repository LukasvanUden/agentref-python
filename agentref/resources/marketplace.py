from __future__ import annotations

from typing import Any, Dict, Literal, Optional

from .._http import AsyncHttpClient, SyncHttpClient
from ..types.models import PaginatedResponse

_SORT = Literal["epc", "conversionRate", "commission", "newest"]


class MarketplaceResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def list_programs(
        self,
        *,
        category: Optional[str] = None,
        min_commission: Optional[float] = None,
        min_epc: Optional[float] = None,
        sort: Optional[_SORT] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponse[Dict[str, Any]]:
        envelope = self._http.request(
            "GET",
            "/marketplace/programs",
            params={
                "category": category,
                "minCommission": min_commission,
                "minEpc": min_epc,
                "sort": sort,
                "cursor": cursor,
                "limit": limit,
                "page": page,
                "pageSize": page_size,
                "offset": offset,
            },
        )
        return PaginatedResponse[Dict[str, Any]].model_validate(envelope)

    def apply(self, program_id: str, *, message: Optional[str] = None) -> Dict[str, Any]:
        envelope = self._http.request(
            "POST",
            f"/marketplace/apply/{program_id}",
            json={"message": message} if message is not None else None,
        )
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}


class AsyncMarketplaceResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list_programs(
        self,
        *,
        category: Optional[str] = None,
        min_commission: Optional[float] = None,
        min_epc: Optional[float] = None,
        sort: Optional[_SORT] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponse[Dict[str, Any]]:
        envelope = await self._http.request(
            "GET",
            "/marketplace/programs",
            params={
                "category": category,
                "minCommission": min_commission,
                "minEpc": min_epc,
                "sort": sort,
                "cursor": cursor,
                "limit": limit,
                "page": page,
                "pageSize": page_size,
                "offset": offset,
            },
        )
        return PaginatedResponse[Dict[str, Any]].model_validate(envelope)

    async def apply(self, program_id: str, *, message: Optional[str] = None) -> Dict[str, Any]:
        envelope = await self._http.request(
            "POST",
            f"/marketplace/apply/{program_id}",
            json={"message": message} if message is not None else None,
        )
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}
