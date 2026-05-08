from __future__ import annotations

from typing import Literal, Optional

from .._http import AsyncHttpClient, SyncHttpClient
from ..types.models import Application, PaginatedResponse

_STATUS = Literal["pending", "approved", "declined", "withdrawn", "blocked"]
_SOURCE = Literal["browser", "api", "mcp", "invite", "import"]


class ApplicationsResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def list(
        self,
        *,
        program_id: Optional[str] = None,
        search: Optional[str] = None,
        status: Optional[_STATUS] = None,
        source: Optional[_SOURCE] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponse[Application]:
        envelope = self._http.request(
            "GET",
            "/applications",
            params={
                "programId": program_id,
                "search": search,
                "status": status,
                "source": source,
                "cursor": cursor,
                "limit": limit,
                "page": page,
                "pageSize": page_size,
                "offset": offset,
            },
        )
        return PaginatedResponse[Application].model_validate(envelope)

    def get(self, id: str) -> Application:
        envelope = self._http.request("GET", f"/applications/{id}")
        return Application.model_validate(envelope["data"])

    def approve(self, id: str, *, note: Optional[str] = None, idempotency_key: Optional[str] = None) -> Application:
        return self._review(id, "approve", note=note, idempotency_key=idempotency_key)

    def decline(self, id: str, *, note: Optional[str] = None, idempotency_key: Optional[str] = None) -> Application:
        return self._review(id, "decline", note=note, idempotency_key=idempotency_key)

    def block(self, id: str, *, note: Optional[str] = None, idempotency_key: Optional[str] = None) -> Application:
        return self._review(id, "block", note=note, idempotency_key=idempotency_key)

    def _review(
        self,
        id: str,
        action: Literal["approve", "decline", "block"],
        *,
        note: Optional[str],
        idempotency_key: Optional[str],
    ) -> Application:
        envelope = self._http.request(
            "POST",
            f"/applications/{id}/{action}",
            json={"note": note} if note is not None else None,
            idempotency_key=idempotency_key,
        )
        return Application.model_validate(envelope["data"])


class AsyncApplicationsResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        program_id: Optional[str] = None,
        search: Optional[str] = None,
        status: Optional[_STATUS] = None,
        source: Optional[_SOURCE] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponse[Application]:
        envelope = await self._http.request(
            "GET",
            "/applications",
            params={
                "programId": program_id,
                "search": search,
                "status": status,
                "source": source,
                "cursor": cursor,
                "limit": limit,
                "page": page,
                "pageSize": page_size,
                "offset": offset,
            },
        )
        return PaginatedResponse[Application].model_validate(envelope)

    async def get(self, id: str) -> Application:
        envelope = await self._http.request("GET", f"/applications/{id}")
        return Application.model_validate(envelope["data"])

    async def approve(
        self,
        id: str,
        *,
        note: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Application:
        return await self._review(id, "approve", note=note, idempotency_key=idempotency_key)

    async def decline(
        self,
        id: str,
        *,
        note: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Application:
        return await self._review(id, "decline", note=note, idempotency_key=idempotency_key)

    async def block(
        self,
        id: str,
        *,
        note: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Application:
        return await self._review(id, "block", note=note, idempotency_key=idempotency_key)

    async def _review(
        self,
        id: str,
        action: Literal["approve", "decline", "block"],
        *,
        note: Optional[str],
        idempotency_key: Optional[str],
    ) -> Application:
        envelope = await self._http.request(
            "POST",
            f"/applications/{id}/{action}",
            json={"note": note} if note is not None else None,
            idempotency_key=idempotency_key,
        )
        return Application.model_validate(envelope["data"])
