from __future__ import annotations

from typing import Optional

from .._http import AsyncHttpClient, SyncHttpClient
from ..types.models import Merchant, UpdateMerchantParams


class MerchantResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def get(self) -> Merchant:
        envelope = self._http.request("GET", "/merchant")
        return Merchant.model_validate(envelope["data"])

    def update(
        self,
        *,
        company_name: Optional[str] = None,
        logo_url: Optional[str] = None,
        timezone: Optional[str] = None,
        default_cookie_duration: Optional[int] = None,
        default_payout_threshold: Optional[int] = None,
        tracking_requires_consent: Optional[bool] = None,
        tracking_param_aliases: Optional[list[str]] = None,
        tracking_legacy_metadata_fallback_enabled: Optional[bool] = None,
    ) -> Merchant:
        payload = UpdateMerchantParams(
            company_name=company_name,
            logo_url=logo_url,
            timezone=timezone,
            default_cookie_duration=default_cookie_duration,
            default_payout_threshold=default_payout_threshold,
            tracking_requires_consent=tracking_requires_consent,
            tracking_param_aliases=tracking_param_aliases,
            tracking_legacy_metadata_fallback_enabled=tracking_legacy_metadata_fallback_enabled,
        ).model_dump(by_alias=True, exclude_none=True)
        envelope = self._http.request("PATCH", "/merchant", json=payload)
        return Merchant.model_validate(envelope["data"])


class AsyncMerchantResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get(self) -> Merchant:
        envelope = await self._http.request("GET", "/merchant")
        return Merchant.model_validate(envelope["data"])

    async def update(
        self,
        *,
        company_name: Optional[str] = None,
        logo_url: Optional[str] = None,
        timezone: Optional[str] = None,
        default_cookie_duration: Optional[int] = None,
        default_payout_threshold: Optional[int] = None,
        tracking_requires_consent: Optional[bool] = None,
        tracking_param_aliases: Optional[list[str]] = None,
        tracking_legacy_metadata_fallback_enabled: Optional[bool] = None,
    ) -> Merchant:
        payload = UpdateMerchantParams(
            company_name=company_name,
            logo_url=logo_url,
            timezone=timezone,
            default_cookie_duration=default_cookie_duration,
            default_payout_threshold=default_payout_threshold,
            tracking_requires_consent=tracking_requires_consent,
            tracking_param_aliases=tracking_param_aliases,
            tracking_legacy_metadata_fallback_enabled=tracking_legacy_metadata_fallback_enabled,
        ).model_dump(by_alias=True, exclude_none=True)
        envelope = await self._http.request("PATCH", "/merchant", json=payload)
        return Merchant.model_validate(envelope["data"])
