from __future__ import annotations

from typing import Any, Dict, Optional

from .._http import AsyncHttpClient, SyncHttpClient
from ..types.models import (
    AffiliateWorkspaceOverview,
    AffiliateWorkspaceProgram,
    AffiliateWorkspaceProgramDetail,
    PaginatedResponse,
)


class AffiliateWorkspaceResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def overview(self) -> AffiliateWorkspaceOverview:
        envelope = self._http.request("GET", "/me/overview")
        return AffiliateWorkspaceOverview.model_validate(envelope["data"])

    def identity(self) -> Dict[str, Any]:
        envelope = self._http.request("GET", "/me")
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}

    def list_programs(self) -> list[AffiliateWorkspaceProgram]:
        envelope = self._http.request("GET", "/me/programs")
        return [AffiliateWorkspaceProgram.model_validate(item) for item in envelope["data"]]

    def get_program(self, program_id: str) -> AffiliateWorkspaceProgramDetail:
        envelope = self._http.request("GET", f"/me/programs/{program_id}")
        return AffiliateWorkspaceProgramDetail.model_validate(envelope["data"])

    def earnings(self) -> Dict[str, Any]:
        envelope = self._http.request("GET", "/me/earnings")
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}

    def list_program_earnings(
        self,
        program_id: str,
        *,
        period: Optional[str] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponse[Dict[str, Any]]:
        envelope = self._http.request(
            "GET",
            f"/me/earnings/{program_id}",
            params={
                "period": period,
                "cursor": cursor,
                "limit": limit,
                "page": page,
                "pageSize": page_size,
                "offset": offset,
            },
        )
        return PaginatedResponse[Dict[str, Any]].model_validate(envelope)

    def list_payouts(
        self,
        *,
        program_id: Optional[str] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponse[Dict[str, Any]]:
        envelope = self._http.request(
            "GET",
            "/me/payouts",
            params={
                "program_id": program_id,
                "cursor": cursor,
                "limit": limit,
                "page": page,
                "pageSize": page_size,
                "offset": offset,
            },
        )
        return PaginatedResponse[Dict[str, Any]].model_validate(envelope)

    def list_links(self, *, program_id: Optional[str] = None) -> list[Dict[str, Any]]:
        envelope = self._http.request("GET", "/me/links", params={"program_id": program_id})
        data = envelope.get("data", [])
        return [item for item in data if isinstance(item, dict)] if isinstance(data, list) else []

    def create_link(
        self,
        *,
        name: str,
        destination_path: Optional[str] = None,
        custom_slug: Optional[str] = None,
        program_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {
            "name": name,
            "destination_path": destination_path,
            "custom_slug": custom_slug,
        }
        envelope = self._http.request(
            "POST",
            "/me/links",
            params={"program_id": program_id},
            json={k: v for k, v in payload.items() if v is not None},
            idempotency_key=idempotency_key,
        )
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}

    def update_link(
        self,
        id: str,
        *,
        name: Optional[str] = None,
        target_url: Optional[str] = None,
        is_active: Optional[bool] = None,
        program_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {"name": name, "targetUrl": target_url, "isActive": is_active}
        envelope = self._http.request(
            "PATCH",
            f"/me/links/{id}",
            params={"program_id": program_id},
            json={k: v for k, v in payload.items() if v is not None},
        )
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}

    def delete_link(self, id: str, *, program_id: Optional[str] = None) -> Dict[str, Any]:
        envelope = self._http.request("DELETE", f"/me/links/{id}", params={"program_id": program_id})
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}

    def click_stats(
        self,
        *,
        program_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        envelope = self._http.request(
            "GET",
            "/me/clicks",
            params={"program_id": program_id, "startDate": start_date, "endDate": end_date},
        )
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}


class AsyncAffiliateWorkspaceResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def overview(self) -> AffiliateWorkspaceOverview:
        envelope = await self._http.request("GET", "/me/overview")
        return AffiliateWorkspaceOverview.model_validate(envelope["data"])

    async def identity(self) -> Dict[str, Any]:
        envelope = await self._http.request("GET", "/me")
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}

    async def list_programs(self) -> list[AffiliateWorkspaceProgram]:
        envelope = await self._http.request("GET", "/me/programs")
        return [AffiliateWorkspaceProgram.model_validate(item) for item in envelope["data"]]

    async def get_program(self, program_id: str) -> AffiliateWorkspaceProgramDetail:
        envelope = await self._http.request("GET", f"/me/programs/{program_id}")
        return AffiliateWorkspaceProgramDetail.model_validate(envelope["data"])

    async def earnings(self) -> Dict[str, Any]:
        envelope = await self._http.request("GET", "/me/earnings")
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}

    async def list_program_earnings(
        self,
        program_id: str,
        *,
        period: Optional[str] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponse[Dict[str, Any]]:
        envelope = await self._http.request(
            "GET",
            f"/me/earnings/{program_id}",
            params={
                "period": period,
                "cursor": cursor,
                "limit": limit,
                "page": page,
                "pageSize": page_size,
                "offset": offset,
            },
        )
        return PaginatedResponse[Dict[str, Any]].model_validate(envelope)

    async def list_payouts(
        self,
        *,
        program_id: Optional[str] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponse[Dict[str, Any]]:
        envelope = await self._http.request(
            "GET",
            "/me/payouts",
            params={
                "program_id": program_id,
                "cursor": cursor,
                "limit": limit,
                "page": page,
                "pageSize": page_size,
                "offset": offset,
            },
        )
        return PaginatedResponse[Dict[str, Any]].model_validate(envelope)

    async def list_links(self, *, program_id: Optional[str] = None) -> list[Dict[str, Any]]:
        envelope = await self._http.request("GET", "/me/links", params={"program_id": program_id})
        data = envelope.get("data", [])
        return [item for item in data if isinstance(item, dict)] if isinstance(data, list) else []

    async def create_link(
        self,
        *,
        name: str,
        destination_path: Optional[str] = None,
        custom_slug: Optional[str] = None,
        program_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {
            "name": name,
            "destination_path": destination_path,
            "custom_slug": custom_slug,
        }
        envelope = await self._http.request(
            "POST",
            "/me/links",
            params={"program_id": program_id},
            json={k: v for k, v in payload.items() if v is not None},
            idempotency_key=idempotency_key,
        )
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}

    async def update_link(
        self,
        id: str,
        *,
        name: Optional[str] = None,
        target_url: Optional[str] = None,
        is_active: Optional[bool] = None,
        program_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {"name": name, "targetUrl": target_url, "isActive": is_active}
        envelope = await self._http.request(
            "PATCH",
            f"/me/links/{id}",
            params={"program_id": program_id},
            json={k: v for k, v in payload.items() if v is not None},
        )
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}

    async def delete_link(self, id: str, *, program_id: Optional[str] = None) -> Dict[str, Any]:
        envelope = await self._http.request("DELETE", f"/me/links/{id}", params={"program_id": program_id})
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}

    async def click_stats(
        self,
        *,
        program_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        envelope = await self._http.request(
            "GET",
            "/me/clicks",
            params={"program_id": program_id, "startDate": start_date, "endDate": end_date},
        )
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}
