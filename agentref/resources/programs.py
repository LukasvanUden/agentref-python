from __future__ import annotations

from typing import Any, AsyncGenerator, Dict, Generator, List, Literal, Optional

from .._http import AsyncHttpClient, SyncHttpClient
from ..types.models import (
    Affiliate,
    ConnectProgramStripeParams,
    ConnectProgramStripeResponse,
    Coupon,
    DisconnectProgramStripeResponse,
    Invite,
    PaginatedResponse,
    Program,
    ProgramDetail,
    ProgramDomainVerificationInitResponse,
    ProgramDomainVerificationStatusResponse,
    ProgramStats,
    SuccessResponse,
    UpdateProgramMarketplaceParams,
)


class ProgramsResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def list(
        self,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        offset: Optional[int] = None,
        status: Optional[str] = None,
    ) -> PaginatedResponse[Program]:
        envelope = self._http.request(
            "GET",
            "/programs",
            params={
                "cursor": cursor,
                "limit": limit,
                "page": page,
                "pageSize": page_size,
                "offset": offset,
                "status": status,
            },
        )
        return PaginatedResponse[Program].model_validate(envelope)

    def list_all(self, *, page_size: int = 100) -> Generator[Program, None, None]:
        page = 1
        while True:
            result = self.list(limit=page_size, page=page)
            for item in result.data:
                yield item
            if not result.meta.has_more:
                break
            page += 1

    def get(self, id: str) -> ProgramDetail:
        envelope = self._http.request("GET", f"/programs/{id}")
        return ProgramDetail.model_validate(envelope["data"])

    def create(
        self,
        *,
        name: str,
        commission_type: Literal["one_time", "recurring", "recurring_limited"],
        commission_percent: float,
        website: Optional[str] = None,
        cookie_duration: Optional[int] = None,
        payout_threshold: Optional[int] = None,
        auto_approve_affiliates: Optional[bool] = None,
        description: Optional[str] = None,
        landing_page_url: Optional[str] = None,
        commission_limit_months: Optional[int] = None,
        portal_slug: Optional[str] = None,
        currency: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Program:
        body: Dict[str, Any] = {
            "name": name,
            "commissionType": commission_type,
            "commissionPercent": commission_percent,
            "website": website,
            "cookieDuration": cookie_duration,
            "payoutThreshold": payout_threshold,
            "autoApproveAffiliates": auto_approve_affiliates,
            "description": description,
            "landingPageUrl": landing_page_url,
            "commissionLimitMonths": commission_limit_months,
            "portalSlug": portal_slug,
            "currency": currency,
        }
        envelope = self._http.request(
            "POST",
            "/programs",
            json={k: v for k, v in body.items() if v is not None},
            idempotency_key=idempotency_key,
        )
        return Program.model_validate(envelope["data"])

    def update(
        self,
        id: str,
        *,
        name: Optional[str] = None,
        commission_type: Optional[Literal["one_time", "recurring", "recurring_limited"]] = None,
        commission_percent: Optional[float] = None,
        website: Optional[str] = None,
        cookie_duration: Optional[int] = None,
        payout_threshold: Optional[int] = None,
        auto_approve_affiliates: Optional[bool] = None,
        description: Optional[str] = None,
        landing_page_url: Optional[str] = None,
        status: Optional[Literal["active", "paused", "archived"]] = None,
        commission_limit_months: Optional[int] = None,
        portal_slug: Optional[str] = None,
        currency: Optional[str] = None,
    ) -> Program:
        body: Dict[str, Any] = {
            "name": name,
            "commissionType": commission_type,
            "commissionPercent": commission_percent,
            "website": website,
            "cookieDuration": cookie_duration,
            "payoutThreshold": payout_threshold,
            "autoApproveAffiliates": auto_approve_affiliates,
            "description": description,
            "landingPageUrl": landing_page_url,
            "status": status,
            "commissionLimitMonths": commission_limit_months,
            "portalSlug": portal_slug,
            "currency": currency,
        }
        envelope = self._http.request("PATCH", f"/programs/{id}", json={k: v for k, v in body.items() if v is not None})
        return Program.model_validate(envelope["data"])

    def delete(self, id: str) -> Program:
        envelope = self._http.request("DELETE", f"/programs/{id}")
        return Program.model_validate(envelope["data"])

    def stats(self, id: str, *, period: Optional[str] = None) -> ProgramStats:
        envelope = self._http.request("GET", f"/programs/{id}/stats", params={"period": period})
        data = envelope.get("data", {})
        if not isinstance(data, dict):
            data = {}
        return ProgramStats.model_validate(data)

    def list_affiliates(
        self,
        id: str,
        *,
        include_blocked: Optional[bool] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponse[Affiliate]:
        envelope = self._http.request(
            "GET",
            f"/programs/{id}/affiliates",
            params={
                "includeBlocked": include_blocked,
                "cursor": cursor,
                "limit": limit,
                "page": page,
                "pageSize": page_size,
                "offset": offset,
            },
        )
        return PaginatedResponse[Affiliate].model_validate(envelope)

    def list_coupons(self, id: str) -> List[Coupon]:
        envelope = self._http.request("GET", f"/programs/{id}/coupons")
        raw = envelope.get("data", [])
        if not isinstance(raw, list):
            return []
        return [Coupon.model_validate(item) for item in raw]

    def create_coupon(
        self,
        id: str,
        *,
        affiliate_id: str,
        code: str,
        expires_at: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Coupon:
        body = {"affiliateId": affiliate_id, "code": code, "expiresAt": expires_at}
        envelope = self._http.request(
            "POST",
            f"/programs/{id}/coupons",
            json={k: v for k, v in body.items() if v is not None},
            idempotency_key=idempotency_key,
        )
        return Coupon.model_validate(envelope["data"])

    def create_invite(
        self,
        id: str,
        *,
        email: Optional[str] = None,
        name: Optional[str] = None,
        is_public: Optional[bool] = None,
        usage_limit: Optional[int] = None,
        expires_in_days: Optional[int] = None,
        tracking_code: Optional[str] = None,
        skip_onboarding: Optional[bool] = None,
        idempotency_key: Optional[str] = None,
    ) -> Invite:
        body = {
            "email": email,
            "name": name,
            "isPublic": is_public,
            "usageLimit": usage_limit,
            "expiresInDays": expires_in_days,
            "trackingCode": tracking_code,
            "skipOnboarding": skip_onboarding,
        }
        envelope = self._http.request(
            "POST",
            f"/programs/{id}/invites",
            json={k: v for k, v in body.items() if v is not None},
            idempotency_key=idempotency_key,
        )
        return Invite.model_validate(envelope["data"])

    def list_invites(self, id: str) -> List[Invite]:
        envelope = self._http.request("GET", f"/programs/{id}/invites")
        raw = envelope.get("data", [])
        if not isinstance(raw, list):
            return []
        return [Invite.model_validate(item) for item in raw]

    def delete_coupon(self, coupon_id: str) -> Coupon:
        envelope = self._http.request("DELETE", f"/coupons/{coupon_id}")
        return Coupon.model_validate(envelope["data"])

    def update_marketplace(
        self,
        id: str,
        *,
        status: Optional[Literal["private", "pending", "public"]] = None,
        category: Optional[str] = None,
        description: Optional[str] = None,
        logo_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        body = UpdateProgramMarketplaceParams(
            status=status,
            category=category,
            description=description,
            logo_url=logo_url,
        ).model_dump(by_alias=True, exclude_none=True)
        envelope = self._http.request("PATCH", f"/programs/{id}/marketplace", json=body)
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}

    def connect_stripe(
        self,
        id: str,
        *,
        method: Optional[Literal["oauth_url", "restricted_key"]] = None,
        stripe_account_id: Optional[str] = None,
    ) -> ConnectProgramStripeResponse:
        payload = ConnectProgramStripeParams(
            method=method,
            stripe_account_id=stripe_account_id,
        ).model_dump(by_alias=True, exclude_none=True)
        envelope = self._http.request("POST", f"/programs/{id}/connect-stripe", json=payload or None)
        return ConnectProgramStripeResponse.model_validate(envelope["data"])

    def disconnect_stripe(self, id: str) -> DisconnectProgramStripeResponse:
        envelope = self._http.request("DELETE", f"/programs/{id}/connect-stripe")
        return DisconnectProgramStripeResponse.model_validate(envelope["data"])

    def verify_domain(self, id: str, *, domain: str) -> ProgramDomainVerificationInitResponse:
        envelope = self._http.request("POST", f"/programs/{id}/verify-domain", json={"domain": domain})
        return ProgramDomainVerificationInitResponse.model_validate(envelope["data"])

    def remove_domain_verification(self, id: str) -> SuccessResponse:
        envelope = self._http.request("DELETE", f"/programs/{id}/verify-domain")
        return SuccessResponse.model_validate(envelope["data"])

    def get_domain_status(self, id: str) -> ProgramDomainVerificationStatusResponse:
        envelope = self._http.request("GET", f"/programs/{id}/verify-domain/status")
        return ProgramDomainVerificationStatusResponse.model_validate(envelope["data"])


class AsyncProgramsResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        offset: Optional[int] = None,
        status: Optional[str] = None,
    ) -> PaginatedResponse[Program]:
        envelope = await self._http.request(
            "GET",
            "/programs",
            params={
                "cursor": cursor,
                "limit": limit,
                "page": page,
                "pageSize": page_size,
                "offset": offset,
                "status": status,
            },
        )
        return PaginatedResponse[Program].model_validate(envelope)

    async def list_all(self, *, page_size: int = 100) -> AsyncGenerator[Program, None]:
        page = 1
        while True:
            result = await self.list(limit=page_size, page=page)
            for item in result.data:
                yield item
            if not result.meta.has_more:
                break
            page += 1

    async def get(self, id: str) -> ProgramDetail:
        envelope = await self._http.request("GET", f"/programs/{id}")
        return ProgramDetail.model_validate(envelope["data"])

    async def create(
        self,
        *,
        name: str,
        commission_type: Literal["one_time", "recurring", "recurring_limited"],
        commission_percent: float,
        website: Optional[str] = None,
        cookie_duration: Optional[int] = None,
        payout_threshold: Optional[int] = None,
        auto_approve_affiliates: Optional[bool] = None,
        description: Optional[str] = None,
        landing_page_url: Optional[str] = None,
        commission_limit_months: Optional[int] = None,
        portal_slug: Optional[str] = None,
        currency: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Program:
        body: Dict[str, Any] = {
            "name": name,
            "commissionType": commission_type,
            "commissionPercent": commission_percent,
            "website": website,
            "cookieDuration": cookie_duration,
            "payoutThreshold": payout_threshold,
            "autoApproveAffiliates": auto_approve_affiliates,
            "description": description,
            "landingPageUrl": landing_page_url,
            "commissionLimitMonths": commission_limit_months,
            "portalSlug": portal_slug,
            "currency": currency,
        }
        envelope = await self._http.request(
            "POST",
            "/programs",
            json={k: v for k, v in body.items() if v is not None},
            idempotency_key=idempotency_key,
        )
        return Program.model_validate(envelope["data"])

    async def update(
        self,
        id: str,
        *,
        name: Optional[str] = None,
        commission_type: Optional[Literal["one_time", "recurring", "recurring_limited"]] = None,
        commission_percent: Optional[float] = None,
        website: Optional[str] = None,
        cookie_duration: Optional[int] = None,
        payout_threshold: Optional[int] = None,
        auto_approve_affiliates: Optional[bool] = None,
        description: Optional[str] = None,
        landing_page_url: Optional[str] = None,
        status: Optional[Literal["active", "paused", "archived"]] = None,
        commission_limit_months: Optional[int] = None,
        portal_slug: Optional[str] = None,
        currency: Optional[str] = None,
    ) -> Program:
        body: Dict[str, Any] = {
            "name": name,
            "commissionType": commission_type,
            "commissionPercent": commission_percent,
            "website": website,
            "cookieDuration": cookie_duration,
            "payoutThreshold": payout_threshold,
            "autoApproveAffiliates": auto_approve_affiliates,
            "description": description,
            "landingPageUrl": landing_page_url,
            "status": status,
            "commissionLimitMonths": commission_limit_months,
            "portalSlug": portal_slug,
            "currency": currency,
        }
        envelope = await self._http.request("PATCH", f"/programs/{id}", json={k: v for k, v in body.items() if v is not None})
        return Program.model_validate(envelope["data"])

    async def delete(self, id: str) -> Program:
        envelope = await self._http.request("DELETE", f"/programs/{id}")
        return Program.model_validate(envelope["data"])

    async def stats(self, id: str, *, period: Optional[str] = None) -> ProgramStats:
        envelope = await self._http.request("GET", f"/programs/{id}/stats", params={"period": period})
        data = envelope.get("data", {})
        if not isinstance(data, dict):
            data = {}
        return ProgramStats.model_validate(data)

    async def list_affiliates(
        self,
        id: str,
        *,
        include_blocked: Optional[bool] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponse[Affiliate]:
        envelope = await self._http.request(
            "GET",
            f"/programs/{id}/affiliates",
            params={
                "includeBlocked": include_blocked,
                "cursor": cursor,
                "limit": limit,
                "page": page,
                "pageSize": page_size,
                "offset": offset,
            },
        )
        return PaginatedResponse[Affiliate].model_validate(envelope)

    async def list_coupons(self, id: str) -> List[Coupon]:
        envelope = await self._http.request("GET", f"/programs/{id}/coupons")
        raw = envelope.get("data", [])
        if not isinstance(raw, list):
            return []
        return [Coupon.model_validate(item) for item in raw]

    async def create_coupon(
        self,
        id: str,
        *,
        affiliate_id: str,
        code: str,
        expires_at: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Coupon:
        body = {"affiliateId": affiliate_id, "code": code, "expiresAt": expires_at}
        envelope = await self._http.request(
            "POST",
            f"/programs/{id}/coupons",
            json={k: v for k, v in body.items() if v is not None},
            idempotency_key=idempotency_key,
        )
        return Coupon.model_validate(envelope["data"])

    async def create_invite(
        self,
        id: str,
        *,
        email: Optional[str] = None,
        name: Optional[str] = None,
        is_public: Optional[bool] = None,
        usage_limit: Optional[int] = None,
        expires_in_days: Optional[int] = None,
        tracking_code: Optional[str] = None,
        skip_onboarding: Optional[bool] = None,
        idempotency_key: Optional[str] = None,
    ) -> Invite:
        body = {
            "email": email,
            "name": name,
            "isPublic": is_public,
            "usageLimit": usage_limit,
            "expiresInDays": expires_in_days,
            "trackingCode": tracking_code,
            "skipOnboarding": skip_onboarding,
        }
        envelope = await self._http.request(
            "POST",
            f"/programs/{id}/invites",
            json={k: v for k, v in body.items() if v is not None},
            idempotency_key=idempotency_key,
        )
        return Invite.model_validate(envelope["data"])

    async def list_invites(self, id: str) -> List[Invite]:
        envelope = await self._http.request("GET", f"/programs/{id}/invites")
        raw = envelope.get("data", [])
        if not isinstance(raw, list):
            return []
        return [Invite.model_validate(item) for item in raw]

    async def delete_coupon(self, coupon_id: str) -> Coupon:
        envelope = await self._http.request("DELETE", f"/coupons/{coupon_id}")
        return Coupon.model_validate(envelope["data"])

    async def update_marketplace(
        self,
        id: str,
        *,
        status: Optional[Literal["private", "pending", "public"]] = None,
        category: Optional[str] = None,
        description: Optional[str] = None,
        logo_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        body = UpdateProgramMarketplaceParams(
            status=status,
            category=category,
            description=description,
            logo_url=logo_url,
        ).model_dump(by_alias=True, exclude_none=True)
        envelope = await self._http.request("PATCH", f"/programs/{id}/marketplace", json=body)
        data = envelope.get("data", {})
        return data if isinstance(data, dict) else {}

    async def connect_stripe(
        self,
        id: str,
        *,
        method: Optional[Literal["oauth_url", "restricted_key"]] = None,
        stripe_account_id: Optional[str] = None,
    ) -> ConnectProgramStripeResponse:
        payload = ConnectProgramStripeParams(
            method=method,
            stripe_account_id=stripe_account_id,
        ).model_dump(by_alias=True, exclude_none=True)
        envelope = await self._http.request("POST", f"/programs/{id}/connect-stripe", json=payload or None)
        return ConnectProgramStripeResponse.model_validate(envelope["data"])

    async def disconnect_stripe(self, id: str) -> DisconnectProgramStripeResponse:
        envelope = await self._http.request("DELETE", f"/programs/{id}/connect-stripe")
        return DisconnectProgramStripeResponse.model_validate(envelope["data"])

    async def verify_domain(self, id: str, *, domain: str) -> ProgramDomainVerificationInitResponse:
        envelope = await self._http.request("POST", f"/programs/{id}/verify-domain", json={"domain": domain})
        return ProgramDomainVerificationInitResponse.model_validate(envelope["data"])

    async def remove_domain_verification(self, id: str) -> SuccessResponse:
        envelope = await self._http.request("DELETE", f"/programs/{id}/verify-domain")
        return SuccessResponse.model_validate(envelope["data"])

    async def get_domain_status(self, id: str) -> ProgramDomainVerificationStatusResponse:
        envelope = await self._http.request("GET", f"/programs/{id}/verify-domain/status")
        return ProgramDomainVerificationStatusResponse.model_validate(envelope["data"])
