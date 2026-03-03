from __future__ import annotations

from typing import List, Optional

from .._http import AsyncHttpClient, SyncHttpClient
from ..types.models import PaginatedResponse, PendingAffiliate, Payout, PayoutStats


class PayoutsResource:
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
    ) -> PaginatedResponse[Payout]:
        envelope = self._http.request(
            "GET",
            "/payouts",
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
        return PaginatedResponse[Payout].model_validate(envelope)

    def list_pending(
        self,
        *,
        program_id: Optional[str] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponse[PendingAffiliate]:
        envelope = self._http.request(
            "GET",
            "/payouts/pending",
            params={
                "programId": program_id,
                "cursor": cursor,
                "limit": limit,
                "page": page,
                "pageSize": page_size,
                "offset": offset,
            },
        )
        return PaginatedResponse[PendingAffiliate].model_validate(envelope)

    def stats(self, *, program_id: Optional[str] = None, period: Optional[str] = None) -> PayoutStats:
        envelope = self._http.request("GET", "/payouts/stats", params={"programId": program_id, "period": period})
        data = envelope.get("data", {})
        if not isinstance(data, dict):
            data = {}
        return PayoutStats.model_validate(data)


class AsyncPayoutsResource:
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
    ) -> PaginatedResponse[Payout]:
        envelope = await self._http.request(
            "GET",
            "/payouts",
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
        return PaginatedResponse[Payout].model_validate(envelope)

    async def list_pending(
        self,
        *,
        program_id: Optional[str] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponse[PendingAffiliate]:
        envelope = await self._http.request(
            "GET",
            "/payouts/pending",
            params={
                "programId": program_id,
                "cursor": cursor,
                "limit": limit,
                "page": page,
                "pageSize": page_size,
                "offset": offset,
            },
        )
        return PaginatedResponse[PendingAffiliate].model_validate(envelope)

    async def stats(self, *, program_id: Optional[str] = None, period: Optional[str] = None) -> PayoutStats:
        envelope = await self._http.request("GET", "/payouts/stats", params={"programId": program_id, "period": period})
        data = envelope.get("data", {})
        if not isinstance(data, dict):
            data = {}
        return PayoutStats.model_validate(data)
