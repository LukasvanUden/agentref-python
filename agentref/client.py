from __future__ import annotations

from typing import Any, Optional

from ._http import AsyncHttpClient, SyncHttpClient
from .resources import (
    AffiliatesResource,
    AsyncAffiliatesResource,
    AsyncBillingResource,
    AsyncConversionsResource,
    AsyncFlagsResource,
    AsyncMerchantResource,
    AsyncNotificationsResource,
    AsyncPayoutInfoResource,
    AsyncPayoutsResource,
    AsyncProgramsResource,
    AsyncWebhooksResource,
    BillingResource,
    ConversionsResource,
    FlagsResource,
    MerchantResource,
    NotificationsResource,
    PayoutInfoResource,
    PayoutsResource,
    ProgramsResource,
    WebhooksResource,
)


class AgentRef:
    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: str = "https://www.agentref.dev/api/v1",
        timeout: float = 30.0,
        max_retries: int = 2,
    ) -> None:
        self._http = SyncHttpClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )

        self.programs = ProgramsResource(self._http)
        self.affiliates = AffiliatesResource(self._http)
        self.conversions = ConversionsResource(self._http)
        self.payouts = PayoutsResource(self._http)
        self.flags = FlagsResource(self._http)
        self.billing = BillingResource(self._http)
        self.merchant = MerchantResource(self._http)
        self.notifications = NotificationsResource(self._http)
        self.payout_info = PayoutInfoResource(self._http)
        self.webhooks = WebhooksResource(self._http)

    def close(self) -> None:
        self._http.close()


class AsyncAgentRef:
    """Async variant -- use as async context manager for connection pooling."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: str = "https://www.agentref.dev/api/v1",
        timeout: float = 30.0,
        max_retries: int = 2,
    ) -> None:
        self._http = AsyncHttpClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )

        self.programs = AsyncProgramsResource(self._http)
        self.affiliates = AsyncAffiliatesResource(self._http)
        self.conversions = AsyncConversionsResource(self._http)
        self.payouts = AsyncPayoutsResource(self._http)
        self.flags = AsyncFlagsResource(self._http)
        self.billing = AsyncBillingResource(self._http)
        self.merchant = AsyncMerchantResource(self._http)
        self.notifications = AsyncNotificationsResource(self._http)
        self.payout_info = AsyncPayoutInfoResource(self._http)
        self.webhooks = AsyncWebhooksResource(self._http)

    async def __aenter__(self) -> "AsyncAgentRef":
        await self._http.__aenter__()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self._http.__aexit__(*args)
