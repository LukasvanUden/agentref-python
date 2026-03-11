from agentref.errors import (
    AgentRefError,
    AuthError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
)


def test_auth_error_is_agentref_error() -> None:
    error = AuthError("Unauthorized", "INVALID_AUTH", "req_1")
    assert isinstance(error, AgentRefError)
    assert error.status == 401


def test_forbidden_error_is_403_not_server_error() -> None:
    error = ForbiddenError("Forbidden", "FORBIDDEN", "req_2")
    assert error.status == 403
    assert isinstance(error, AgentRefError)
    assert not isinstance(error, ServerError)


def test_not_found_error_status() -> None:
    error = NotFoundError("Not found", "NOT_FOUND", "req_3")
    assert error.status == 404


def test_rate_limit_error_has_retry_after() -> None:
    error = RateLimitError("Too many", "RATE_LIMITED", "req_4", 30)
    assert error.retry_after == 30
    assert error.status == 429


def test_pydantic_models_parse_camel_case() -> None:
    from agentref.types.models import Program

    program = Program.model_validate(
        {
            "id": "p1",
            "merchantId": "m1",
            "name": "Test",
            "description": None,
            "slug": "test",
            "website": "https://agentref.dev",
            "landingPageUrl": None,
            "portalSlug": "test",
            "status": "active",
            "marketplaceStatus": "public",
            "marketplaceCategory": None,
            "marketplaceDescription": None,
            "marketplaceLogoUrl": None,
            "commissionType": "one_time",
            "commissionPercent": 20.0,
            "commissionLimitMonths": None,
            "commissionHoldDays": 30,
            "cookieDuration": 30,
            "trackingRequiresConsent": False,
            "trackingParamAliases": ["ref"],
            "trackingLegacyMetadataFallbackEnabled": True,
            "payoutThreshold": 5000,
            "currency": "USD",
            "autoApproveAffiliates": True,
            "termsUrl": None,
            "stripeAccountId": None,
            "stripeConnectedAt": None,
            "verifiedDomain": None,
            "domainVerificationToken": None,
            "domainVerifiedAt": None,
            "createdAt": "2026-01-01T00:00:00Z",
            "updatedAt": "2026-01-01T00:00:00Z",
        }
    )

    assert program.commission_type == "one_time"
    assert program.commission_percent == 20.0
    assert program.cookie_duration == 30
    assert program.auto_approve_affiliates is True


def test_merchant_model_parses_current_rest_shape() -> None:
    from agentref.types.models import Merchant

    merchant = Merchant.model_validate(
        {
            "id": "merch_1",
            "userId": "user_1",
            "companyName": "AgentRef Inc",
            "logoUrl": None,
            "billingTier": "free",
            "billingRequirementStatus": "not_required",
            "paymentStatus": "active",
            "lastPaymentFailedAt": None,
            "defaultCookieDuration": 30,
            "defaultPayoutThreshold": 5000,
            "timezone": "UTC",
            "trackingRequiresConsent": True,
            "trackingParamAliases": ["ref"],
            "trackingLegacyMetadataFallbackEnabled": True,
            "notificationPreferences": {"newAffiliate": True},
            "onboardingCompleted": True,
            "onboardingStep": 4,
            "createdAt": "2026-01-01T00:00:00Z",
            "updatedAt": "2026-01-02T00:00:00Z",
        }
    )

    assert merchant.billing_requirement_status == "not_required"
    assert merchant.notification_preferences == {"newAffiliate": True}


def test_pagination_meta_parses_camel_case() -> None:
    from agentref.types.models import PaginationMeta

    meta = PaginationMeta.model_validate(
        {
            "total": 100,
            "page": 1,
            "pageSize": 20,
            "hasMore": True,
            "nextCursor": "abc123",
            "requestId": "req_x",
        }
    )

    assert meta.has_more is True
    assert meta.next_cursor == "abc123"
    assert meta.request_id == "req_x"
    assert meta.page_size == 20
