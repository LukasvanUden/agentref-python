from __future__ import annotations

import json

import httpx
import respx

from agentref import AgentRef


def _mock_program() -> dict:
    return {
        "id": "prog_1",
        "merchantId": "merch_1",
        "name": "Program",
        "description": None,
        "slug": "program",
        "landingPageUrl": None,
        "portalSlug": "program",
        "status": "active",
        "marketplaceStatus": "public",
        "marketplaceCategory": None,
        "marketplaceDescription": None,
        "marketplaceLogoUrl": None,
        "commissionType": "one_time",
        "commissionPercent": 20,
        "commissionLimitMonths": None,
        "commissionHoldDays": 30,
        "cookieDuration": 30,
        "payoutThreshold": 5000,
        "currency": "USD",
        "autoApproveAffiliates": True,
        "termsUrl": None,
        "createdAt": "2026-01-01T00:00:00Z",
        "updatedAt": "2026-01-01T00:00:00Z",
    }


def test_create_uses_real_field_names() -> None:
    client = AgentRef(api_key="ak_live_test")

    with respx.mock:
        route = respx.post("https://www.agentref.dev/api/v1/programs").mock(
            return_value=httpx.Response(201, json={"data": _mock_program(), "meta": {"requestId": "r"}})
        )

        client.programs.create(
            name="Test",
            commission_type="one_time",
            commission_percent=20,
            cookie_duration=30,
            portal_slug="test-program",
            currency="EUR",
        )

        body = json.loads(route.calls[0].request.content)

    assert "commissionType" in body
    assert "commissionPercent" in body
    assert "cookieDuration" in body
    assert body["portalSlug"] == "test-program"
    assert body["currency"] == "EUR"
    assert "commissionRate" not in body
    assert "cookieDays" not in body


def test_list_all_stops_on_has_more_false() -> None:
    client = AgentRef(api_key="ak_live_test")

    with respx.mock:
        respx.get("https://www.agentref.dev/api/v1/programs").mock(
            side_effect=[
                httpx.Response(
                    200,
                    json={
                        "data": [_mock_program()],
                        "meta": {"total": 2, "page": 1, "pageSize": 1, "hasMore": True, "requestId": "r1"},
                    },
                ),
                httpx.Response(
                    200,
                    json={
                        "data": [{**_mock_program(), "id": "prog_2"}],
                        "meta": {"total": 2, "page": 2, "pageSize": 1, "hasMore": False, "requestId": "r2"},
                    },
                ),
            ]
        )

        all_programs = list(client.programs.list_all(page_size=1))

    assert len(all_programs) == 2
    assert all_programs[0].id == "prog_1"
    assert all_programs[1].id == "prog_2"


def test_flags_resolve_sends_block_affiliate_true() -> None:
    client = AgentRef(api_key="ak_live_test")

    with respx.mock:
        route = respx.post("https://www.agentref.dev/api/v1/flags/flag_1/resolve").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": {
                        "id": "flag_1",
                        "affiliateId": "aff_1",
                        "type": "manual_review",
                        "status": "confirmed",
                        "details": {"source": "test"},
                        "note": "confirmed fraud",
                        "createdAt": "2026-01-01T00:00:00Z",
                        "resolvedAt": "2026-01-01T01:00:00Z",
                    },
                    "meta": {"requestId": "r"},
                },
            )
        )

        client.flags.resolve(
            "flag_1",
            status="confirmed",
            note="confirmed fraud",
            block_affiliate=True,
            idempotency_key="idem-flag-1",
        )

        body = json.loads(route.calls[0].request.content)

    assert body["status"] == "confirmed"
    assert body["blockAffiliate"] is True


def test_list_invites_returns_typed_invites() -> None:
    client = AgentRef(api_key="ak_live_test")

    with respx.mock:
        respx.get("https://www.agentref.dev/api/v1/programs/prog_1/invites").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "token": "tok_1",
                            "email": "affiliate@example.com",
                            "programId": "prog_1",
                            "expiresAt": "2026-12-01T00:00:00Z",
                            "createdAt": "2026-01-01T00:00:00Z",
                        }
                    ],
                    "meta": {"requestId": "r"},
                },
            )
        )
        invites = client.programs.list_invites("prog_1")
    assert invites[0].token == "tok_1"


def test_update_marketplace_uses_camel_case_payload() -> None:
    client = AgentRef(api_key="ak_live_test")

    with respx.mock:
        route = respx.patch("https://www.agentref.dev/api/v1/programs/prog_1/marketplace").mock(
            return_value=httpx.Response(200, json={"data": {"status": "pending"}, "meta": {"requestId": "r"}})
        )
        client.programs.update_marketplace("prog_1", status="pending", logo_url="https://cdn.example.com/logo.png")
        body = json.loads(route.calls[0].request.content)
    assert body["status"] == "pending"
    assert body["logoUrl"] == "https://cdn.example.com/logo.png"


def test_payouts_create_sends_idempotency_and_body() -> None:
    client = AgentRef(api_key="ak_live_test")

    with respx.mock:
        route = respx.post("https://www.agentref.dev/api/v1/payouts").mock(
            return_value=httpx.Response(201, json={"data": {"id": "pay_1"}, "meta": {"requestId": "r"}})
        )
        client.payouts.create(
            affiliate_id="aff_1",
            program_id="prog_1",
            method="paypal",
            idempotency_key="idem-payout-1",
        )
        body = json.loads(route.calls[0].request.content)
        idempotency = route.calls[0].request.headers.get("idempotency-key")
    assert body["affiliateId"] == "aff_1"
    assert body["programId"] == "prog_1"
    assert body["method"] == "paypal"
    assert idempotency == "idem-payout-1"


def test_merchant_update_and_connect_stripe() -> None:
    client = AgentRef(api_key="ak_live_test")

    with respx.mock:
        update_route = respx.patch("https://www.agentref.dev/api/v1/merchant").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": {
                        "id": "merch_1",
                        "userId": "user_1",
                        "companyName": "AgentRef Inc",
                        "website": "https://agentref.dev",
                        "logoUrl": None,
                        "stripeAccountId": None,
                        "stripeConnectedAt": None,
                        "billingTier": "free",
                        "stripeCustomerId": None,
                        "stripeSubscriptionId": None,
                        "paymentStatus": "active",
                        "lastPaymentFailedAt": None,
                        "defaultCookieDuration": 30,
                        "defaultPayoutThreshold": 5000,
                        "timezone": "UTC",
                        "trackingRequiresConsent": True,
                        "trackingParamAliases": ["ref", "partner"],
                        "trackingLegacyMetadataFallbackEnabled": True,
                        "state": "verified",
                        "verifiedDomain": "agentref.dev",
                        "domainVerificationToken": None,
                        "domainVerifiedAt": "2026-01-01T00:00:00Z",
                        "notificationPreferences": {"newAffiliate": True},
                        "onboardingCompleted": True,
                        "onboardingStep": 4,
                        "createdAt": "2026-01-01T00:00:00Z",
                        "updatedAt": "2026-01-02T00:00:00Z",
                    },
                    "meta": {"requestId": "r"},
                },
            )
        )
        connect_route = respx.post("https://www.agentref.dev/api/v1/merchant/connect-stripe").mock(
            return_value=httpx.Response(200, json={"data": {"url": "https://connect.stripe.com/x"}, "meta": {"requestId": "r"}})
        )

        merchant = client.merchant.update(
            company_name="AgentRef Inc",
            tracking_requires_consent=True,
            tracking_param_aliases=["ref", "partner"],
        )
        connect = client.merchant.connect_stripe()
        update_body = json.loads(update_route.calls[0].request.content)
        connect_method = connect_route.calls[0].request.method

    assert merchant.company_name == "AgentRef Inc"
    assert update_body["companyName"] == "AgentRef Inc"
    assert update_body["trackingRequiresConsent"] is True
    assert update_body["trackingParamAliases"] == ["ref", "partner"]
    assert merchant.state == "verified"
    assert merchant.verified_domain == "agentref.dev"
    assert connect.url.startswith("https://connect.stripe.com")
    assert connect_method == "POST"


def test_merchant_domain_status_uses_current_contract() -> None:
    client = AgentRef(api_key="ak_live_test")

    with respx.mock:
        respx.get("https://www.agentref.dev/api/v1/merchant/domain-status").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": {
                        "status": "verified",
                        "domain": "agentref.dev",
                        "txtRecord": None,
                        "verifiedAt": "2026-01-01T00:00:00Z",
                        "trackingMode": "advanced",
                        "advancedTrackingEnabled": True,
                    },
                    "meta": {"requestId": "r"},
                },
            )
        )

        status = client.merchant.domain_status()

    assert status.status == "verified"
    assert status.tracking_mode == "advanced"


def test_program_stats_uses_current_contract() -> None:
    client = AgentRef(api_key="ak_live_test")

    with respx.mock:
        respx.get("https://www.agentref.dev/api/v1/programs/prog_1/stats").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": {
                        "programId": "prog_1",
                        "programName": "Growth Program",
                        "status": "active",
                        "totalRevenue": 25000,
                        "totalConversions": 12,
                        "totalCommissions": 5000,
                        "pendingCommissions": 1200,
                        "activeAffiliates": 3,
                        "conversionsByStatus": {
                            "pending": 1,
                            "approved": 10,
                            "rejected": 1,
                            "refunded": 0,
                        },
                    },
                    "meta": {"requestId": "r"},
                },
            )
        )

        stats = client.programs.stats("prog_1")

    assert stats.program_id == "prog_1"
    assert stats.conversions_by_status["approved"] == 10


def test_payout_info_supports_bank_fields() -> None:
    client = AgentRef(api_key="ak_live_test")

    with respx.mock:
        get_route = respx.get("https://www.agentref.dev/api/v1/me/payout-info").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": {
                        "payoutMethod": "bank_transfer",
                        "paypalEmail": None,
                        "bankAccountHolder": "Jane Doe",
                        "bankIban": "****1234",
                        "bankBic": "COBADEFFXXX",
                        "firstName": "Jane",
                        "lastName": "Doe",
                        "addressLine1": "Main Street 1",
                        "addressLine2": None,
                        "city": "Berlin",
                        "state": None,
                        "postalCode": "10115",
                        "vatId": "DE123",
                    },
                    "meta": {"requestId": "r"},
                },
            )
        )
        update_route = respx.patch("https://www.agentref.dev/api/v1/me/payout-info").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": {
                        "payoutMethod": "bank_transfer",
                        "paypalEmail": None,
                        "bankAccountHolder": "Jane Doe",
                        "bankIban": "****1234",
                        "bankBic": "COBADEFFXXX",
                        "firstName": "Jane",
                        "lastName": "Doe",
                        "addressLine1": "Main Street 1",
                        "addressLine2": None,
                        "city": "Berlin",
                        "state": None,
                        "postalCode": "10115",
                        "vatId": "DE123",
                    },
                    "meta": {"requestId": "r"},
                },
            )
        )

        payout_info = client.payout_info.get()
        client.payout_info.update(
            payout_method="bank_transfer",
            bank_account_holder="Jane Doe",
            bank_iban="DE89370400440532013000",
            bank_bic="COBADEFFXXX",
        )

        update_body = json.loads(update_route.calls[0].request.content)

    assert get_route.called
    assert payout_info.bank_account_holder == "Jane Doe"
    assert payout_info.bank_bic == "COBADEFFXXX"
    assert update_body["bankAccountHolder"] == "Jane Doe"
    assert update_body["bankBic"] == "COBADEFFXXX"
