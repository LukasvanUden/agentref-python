from __future__ import annotations

from typing import Any, Dict

from .._http import AsyncHttpClient, SyncHttpClient
from ..types.models import Merchant


class MerchantResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def get(self) -> Merchant:
        envelope = self._http.request("GET", "/merchant")
        return Merchant.model_validate(envelope["data"])

    def domain_status(self) -> Dict[str, Any]:
        envelope = self._http.request("GET", "/merchant/domain-status")
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}


class AsyncMerchantResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get(self) -> Merchant:
        envelope = await self._http.request("GET", "/merchant")
        return Merchant.model_validate(envelope["data"])

    async def domain_status(self) -> Dict[str, Any]:
        envelope = await self._http.request("GET", "/merchant/domain-status")
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}
