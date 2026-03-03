from __future__ import annotations

from typing import Optional

from .._http import AsyncHttpClient, SyncHttpClient
from ..types.models import Affiliate, PaginatedResponse


class AffiliatesResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def list(
        self,
        *,
        program_id: Optional[str] = None,
        include_blocked: Optional[bool] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponse[Affiliate]:
        envelope = self._http.request(
            "GET",
            "/affiliates",
            params={
                "programId": program_id,
                "includeBlocked": include_blocked,
                "cursor": cursor,
                "limit": limit,
                "page": page,
                "pageSize": page_size,
                "offset": offset,
            },
        )
        return PaginatedResponse[Affiliate].model_validate(envelope)

    def get(self, id: str) -> Affiliate:
        envelope = self._http.request("GET", f"/affiliates/{id}")
        return Affiliate.model_validate(envelope["data"])

    def approve(self, id: str, *, idempotency_key: Optional[str] = None) -> Affiliate:
        envelope = self._http.request("POST", f"/affiliates/{id}/approve", idempotency_key=idempotency_key)
        return Affiliate.model_validate(envelope["data"])

    def block(
        self,
        id: str,
        *,
        reason: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Affiliate:
        envelope = self._http.request(
            "POST",
            f"/affiliates/{id}/block",
            json={"reason": reason} if reason is not None else None,
            idempotency_key=idempotency_key,
        )
        return Affiliate.model_validate(envelope["data"])

    def unblock(self, id: str, *, idempotency_key: Optional[str] = None) -> Affiliate:
        envelope = self._http.request("POST", f"/affiliates/{id}/unblock", idempotency_key=idempotency_key)
        return Affiliate.model_validate(envelope["data"])


class AsyncAffiliatesResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        program_id: Optional[str] = None,
        include_blocked: Optional[bool] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponse[Affiliate]:
        envelope = await self._http.request(
            "GET",
            "/affiliates",
            params={
                "programId": program_id,
                "includeBlocked": include_blocked,
                "cursor": cursor,
                "limit": limit,
                "page": page,
                "pageSize": page_size,
                "offset": offset,
            },
        )
        return PaginatedResponse[Affiliate].model_validate(envelope)

    async def get(self, id: str) -> Affiliate:
        envelope = await self._http.request("GET", f"/affiliates/{id}")
        return Affiliate.model_validate(envelope["data"])

    async def approve(self, id: str, *, idempotency_key: Optional[str] = None) -> Affiliate:
        envelope = await self._http.request("POST", f"/affiliates/{id}/approve", idempotency_key=idempotency_key)
        return Affiliate.model_validate(envelope["data"])

    async def block(
        self,
        id: str,
        *,
        reason: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Affiliate:
        envelope = await self._http.request(
            "POST",
            f"/affiliates/{id}/block",
            json={"reason": reason} if reason is not None else None,
            idempotency_key=idempotency_key,
        )
        return Affiliate.model_validate(envelope["data"])

    async def unblock(self, id: str, *, idempotency_key: Optional[str] = None) -> Affiliate:
        envelope = await self._http.request("POST", f"/affiliates/{id}/unblock", idempotency_key=idempotency_key)
        return Affiliate.model_validate(envelope["data"])
