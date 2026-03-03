from __future__ import annotations

from typing import List, Literal, Optional

from .._http import AsyncHttpClient, SyncHttpClient
from ..types.models import BillingStatus, BillingTier


class BillingResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def current(self) -> BillingStatus:
        envelope = self._http.request("GET", "/billing")
        return BillingStatus.model_validate(envelope["data"])

    def tiers(self) -> List[BillingTier]:
        envelope = self._http.request("GET", "/billing/tiers")
        raw = envelope.get("data", [])
        if not isinstance(raw, list):
            return []
        return [BillingTier.model_validate(item) for item in raw]

    def subscribe(
        self,
        *,
        tier: Literal["starter", "growth", "pro", "scale"],
        idempotency_key: Optional[str] = None,
    ) -> BillingStatus:
        envelope = self._http.request(
            "POST",
            "/billing/subscribe",
            json={"tier": tier},
            idempotency_key=idempotency_key,
        )
        return BillingStatus.model_validate(envelope["data"])


class AsyncBillingResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def current(self) -> BillingStatus:
        envelope = await self._http.request("GET", "/billing")
        return BillingStatus.model_validate(envelope["data"])

    async def tiers(self) -> List[BillingTier]:
        envelope = await self._http.request("GET", "/billing/tiers")
        raw = envelope.get("data", [])
        if not isinstance(raw, list):
            return []
        return [BillingTier.model_validate(item) for item in raw]

    async def subscribe(
        self,
        *,
        tier: Literal["starter", "growth", "pro", "scale"],
        idempotency_key: Optional[str] = None,
    ) -> BillingStatus:
        envelope = await self._http.request(
            "POST",
            "/billing/subscribe",
            json={"tier": tier},
            idempotency_key=idempotency_key,
        )
        return BillingStatus.model_validate(envelope["data"])
