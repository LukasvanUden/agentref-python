from __future__ import annotations

from typing import Any, Dict

from .._http import AsyncHttpClient, SyncHttpClient


class InvitesResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def get(self, token: str) -> Dict[str, Any]:
        envelope = self._http.request("GET", f"/invites/{token}")
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}

    def claim(self, token: str) -> Dict[str, Any]:
        envelope = self._http.request("POST", f"/invites/{token}/claim")
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}


class AsyncInvitesResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get(self, token: str) -> Dict[str, Any]:
        envelope = await self._http.request("GET", f"/invites/{token}")
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}

    async def claim(self, token: str) -> Dict[str, Any]:
        envelope = await self._http.request("POST", f"/invites/{token}/claim")
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}
