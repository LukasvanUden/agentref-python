from __future__ import annotations

from typing import Optional

from .._http import AsyncHttpClient, SyncHttpClient
from ..types.models import NotificationPreferences, UpdateNotificationPreferencesParams


class NotificationsResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def get(self) -> NotificationPreferences:
        envelope = self._http.request("GET", "/merchant/notifications")
        return NotificationPreferences.model_validate(envelope["data"])

    def update(
        self,
        *,
        new_affiliate: Optional[bool] = None,
        new_conversion: Optional[bool] = None,
        commission_approved: Optional[bool] = None,
        payout_processed: Optional[bool] = None,
        weekly_digest: Optional[bool] = None,
    ) -> NotificationPreferences:
        payload = UpdateNotificationPreferencesParams(
            new_affiliate=new_affiliate,
            new_conversion=new_conversion,
            commission_approved=commission_approved,
            payout_processed=payout_processed,
            weekly_digest=weekly_digest,
        ).model_dump(by_alias=True, exclude_none=True)
        envelope = self._http.request("PUT", "/merchant/notifications", json=payload)
        return NotificationPreferences.model_validate(envelope["data"])


class AsyncNotificationsResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get(self) -> NotificationPreferences:
        envelope = await self._http.request("GET", "/merchant/notifications")
        return NotificationPreferences.model_validate(envelope["data"])

    async def update(
        self,
        *,
        new_affiliate: Optional[bool] = None,
        new_conversion: Optional[bool] = None,
        commission_approved: Optional[bool] = None,
        payout_processed: Optional[bool] = None,
        weekly_digest: Optional[bool] = None,
    ) -> NotificationPreferences:
        payload = UpdateNotificationPreferencesParams(
            new_affiliate=new_affiliate,
            new_conversion=new_conversion,
            commission_approved=commission_approved,
            payout_processed=payout_processed,
            weekly_digest=weekly_digest,
        ).model_dump(by_alias=True, exclude_none=True)
        envelope = await self._http.request("PUT", "/merchant/notifications", json=payload)
        return NotificationPreferences.model_validate(envelope["data"])
