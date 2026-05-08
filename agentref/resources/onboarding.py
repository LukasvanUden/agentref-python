from __future__ import annotations

from typing import Any, Dict

from .._http import AsyncHttpClient, SyncHttpClient


class OnboardingResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def upsert_merchant_profile(self, *, company_name: str) -> Dict[str, Any]:
        envelope = self._http.request("POST", "/onboarding/merchant", json={"companyName": company_name})
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}

    def complete(self) -> Dict[str, Any]:
        envelope = self._http.request("POST", "/onboarding/complete")
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}


class AsyncOnboardingResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def upsert_merchant_profile(self, *, company_name: str) -> Dict[str, Any]:
        envelope = await self._http.request("POST", "/onboarding/merchant", json={"companyName": company_name})
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}

    async def complete(self) -> Dict[str, Any]:
        envelope = await self._http.request("POST", "/onboarding/complete")
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}
