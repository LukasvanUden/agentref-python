from __future__ import annotations

from typing import Any, Dict

from .._http import AsyncHttpClient, SyncHttpClient


class TrackingResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def get_program_status(self, program_id: str) -> Dict[str, Any]:
        envelope = self._http.request("GET", f"/programs/{program_id}/tracking/status")
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}


class AsyncTrackingResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get_program_status(self, program_id: str) -> Dict[str, Any]:
        envelope = await self._http.request("GET", f"/programs/{program_id}/tracking/status")
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}
