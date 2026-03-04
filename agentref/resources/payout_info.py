from __future__ import annotations

from typing import Optional

from .._http import AsyncHttpClient, SyncHttpClient
from ..types.models import PayoutInfo, UpdatePayoutInfoParams


class PayoutInfoResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def get(self) -> PayoutInfo:
        envelope = self._http.request("GET", "/me/payout-info")
        return PayoutInfo.model_validate(envelope["data"])

    def update(
        self,
        *,
        payout_method: Optional[str] = None,
        paypal_email: Optional[str] = None,
        bank_iban: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        address_line1: Optional[str] = None,
        address_line2: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        postal_code: Optional[str] = None,
        vat_id: Optional[str] = None,
    ) -> PayoutInfo:
        payload = UpdatePayoutInfoParams(
            payout_method=payout_method,
            paypal_email=paypal_email,
            bank_iban=bank_iban,
            first_name=first_name,
            last_name=last_name,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            postal_code=postal_code,
            vat_id=vat_id,
        ).model_dump(by_alias=True, exclude_none=True)
        envelope = self._http.request("PATCH", "/me/payout-info", json=payload)
        return PayoutInfo.model_validate(envelope["data"])


class AsyncPayoutInfoResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get(self) -> PayoutInfo:
        envelope = await self._http.request("GET", "/me/payout-info")
        return PayoutInfo.model_validate(envelope["data"])

    async def update(
        self,
        *,
        payout_method: Optional[str] = None,
        paypal_email: Optional[str] = None,
        bank_iban: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        address_line1: Optional[str] = None,
        address_line2: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        postal_code: Optional[str] = None,
        vat_id: Optional[str] = None,
    ) -> PayoutInfo:
        payload = UpdatePayoutInfoParams(
            payout_method=payout_method,
            paypal_email=paypal_email,
            bank_iban=bank_iban,
            first_name=first_name,
            last_name=last_name,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            postal_code=postal_code,
            vat_id=vat_id,
        ).model_dump(by_alias=True, exclude_none=True)
        envelope = await self._http.request("PATCH", "/me/payout-info", json=payload)
        return PayoutInfo.model_validate(envelope["data"])
