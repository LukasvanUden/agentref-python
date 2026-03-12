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
        "website": "https://agentref.dev",
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
            website="https://new.agentref.dev",
            cookie_duration=30,
            portal_slug="test-program",
            currency="EUR",
        )

        body = json.loads(route.calls[0].request.content)

    assert "commissionType" in body
    assert "commissionPercent" in body
    assert body["website"] == "https://new.agentref.dev"
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


def test_program_get_returns_program_detail() -> None:
    client = AgentRef(api_key="ak_live_test")

    with respx.mock:
        respx.get("https://www.agentref.dev/api/v1/programs/prog_1").mock(
            return_value=httpx.Response(
                200,
                json={"data": {**_mock_program(), "readiness": "ready"}, "meta": {"requestId": "r"}},
            )
        )

        program = client.programs.get("prog_1")

    assert program.id == "prog_1"
    assert program.readiness == "ready"


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


def test_merchant_update_uses_current_contract() -> None:
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
                        "logoUrl": None,
                        "billingTier": "free",
                        "billingRequirementStatus": "not_required",
                        "paymentStatus": "active",
                        "lastPaymentFailedAt": None,
                        "defaultCookieDuration": 30,
                        "defaultPayoutThreshold": 5000,
                        "timezone": "UTC",
                        "trackingRequiresConsent": True,
                        "trackingParamAliases": ["ref", "partner"],
                        "trackingLegacyMetadataFallbackEnabled": True,
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

        merchant = client.merchant.update(
            company_name="AgentRef Inc",
            tracking_requires_consent=True,
            tracking_param_aliases=["ref", "partner"],
        )
        update_body = json.loads(update_route.calls[0].request.content)

    assert merchant.company_name == "AgentRef Inc"
    assert update_body["companyName"] == "AgentRef Inc"
    assert update_body["trackingRequiresConsent"] is True
    assert update_body["trackingParamAliases"] == ["ref", "partner"]
    assert merchant.billing_requirement_status == "not_required"
    assert not hasattr(merchant, "state")


def test_program_connects_stripe_via_program_scope() -> None:
    client = AgentRef(api_key="ak_live_test")

    with respx.mock:
        route = respx.post("https://www.agentref.dev/api/v1/programs/prog_1/connect-stripe").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": {
                        "connected": False,
                        "method": "oauth_url",
                        "programId": "prog_1",
                        "authUrl": "https://connect.stripe.com/oauth/authorize",
                        "message": "Continue in Stripe.",
                    },
                    "meta": {"requestId": "r"},
                },
            )
        )

        connect = client.programs.connect_stripe("prog_1", method="oauth_url")
        body = json.loads(route.calls[0].request.content)

    assert body["method"] == "oauth_url"
    assert connect.program_id == "prog_1"
    assert connect.auth_url == "https://connect.stripe.com/oauth/authorize"


def test_program_domain_methods_use_current_contract() -> None:
    client = AgentRef(api_key="ak_live_test")

    with respx.mock:
        respx.post("https://www.agentref.dev/api/v1/programs/prog_1/verify-domain").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": {
                        "programId": "prog_1",
                        "domain": "agentref.dev",
                        "token": "verify_me",
                        "txtRecord": "verify_me",
                        "txtRecordName": "_agentref.agentref.dev",
                        "message": "Add the TXT record.",
                    },
                    "meta": {"requestId": "r"},
                },
            )
        )
        respx.get("https://www.agentref.dev/api/v1/programs/prog_1/verify-domain/status").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": {
                        "verified": True,
                        "domain": "agentref.dev",
                        "verifiedAt": "2026-01-01T00:00:00Z",
                        "programId": "prog_1",
                        "programReadiness": "ready",
                        "message": "Domain verified.",
                    },
                    "meta": {"requestId": "r"},
                },
            )
        )
        respx.delete("https://www.agentref.dev/api/v1/programs/prog_1/verify-domain").mock(
            return_value=httpx.Response(
                200,
                json={"data": {"success": True}, "meta": {"requestId": "r"}},
            )
        )

        verify = client.programs.verify_domain("prog_1", domain="agentref.dev")
        status = client.programs.get_domain_status("prog_1")
        removed = client.programs.remove_domain_verification("prog_1")

    assert verify.txt_record_name == "_agentref.agentref.dev"
    assert status.program_readiness == "ready"
    assert removed.success is True


def test_program_disconnects_stripe() -> None:
    client = AgentRef(api_key="ak_live_test")

    with respx.mock:
        respx.delete("https://www.agentref.dev/api/v1/programs/prog_1/connect-stripe").mock(
            return_value=httpx.Response(
                200,
                json={"data": {"success": True, "programId": "prog_1"}, "meta": {"requestId": "r"}},
            )
        )

        result = client.programs.disconnect_stripe("prog_1")

    assert result.success is True
    assert result.program_id == "prog_1"


def test_webhooks_use_current_contract() -> None:
    client = AgentRef(api_key="ak_live_test")

    with respx.mock:
        create_route = respx.post("https://www.agentref.dev/api/v1/webhooks").mock(
            return_value=httpx.Response(
                201,
                json={
                    "data": {
                        "endpoint": {
                            "id": "wh_1",
                            "name": "Primary",
                            "url": "https://example.com/webhooks",
                            "status": "active",
                            "programId": "prog_1",
                            "schemaVersion": 2,
                            "subscribedEvents": ["program.created"],
                            "secretLastFour": "1234",
                            "createdAt": "2026-01-01T00:00:00Z",
                            "updatedAt": "2026-01-01T00:00:00Z",
                            "disabledAt": None,
                        },
                        "signingSecret": "whsec_123",
                    },
                    "meta": {"requestId": "r"},
                },
            )
        )
        respx.get("https://www.agentref.dev/api/v1/webhooks").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "id": "wh_1",
                            "name": "Primary",
                            "url": "https://example.com/webhooks",
                            "status": "active",
                            "programId": "prog_1",
                            "schemaVersion": 2,
                            "subscribedEvents": ["program.created"],
                            "secretLastFour": "1234",
                            "createdAt": "2026-01-01T00:00:00Z",
                            "updatedAt": "2026-01-01T00:00:00Z",
                            "disabledAt": None,
                        }
                    ],
                    "meta": {"requestId": "r"},
                },
            )
        )
        respx.patch("https://www.agentref.dev/api/v1/webhooks/wh_1").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": {
                        "id": "wh_1",
                        "name": "Renamed",
                        "url": "https://example.com/webhooks",
                        "status": "active",
                        "programId": None,
                        "schemaVersion": 2,
                        "subscribedEvents": ["program.updated"],
                        "secretLastFour": "1234",
                        "createdAt": "2026-01-01T00:00:00Z",
                        "updatedAt": "2026-01-02T00:00:00Z",
                        "disabledAt": None,
                    },
                    "meta": {"requestId": "r"},
                },
            )
        )
        respx.post("https://www.agentref.dev/api/v1/webhooks/wh_1/rotate-secret").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": {
                        "endpoint": {
                            "id": "wh_1",
                            "name": "Renamed",
                            "url": "https://example.com/webhooks",
                            "status": "active",
                            "programId": None,
                            "schemaVersion": 2,
                            "subscribedEvents": ["program.updated"],
                            "secretLastFour": "5678",
                            "createdAt": "2026-01-01T00:00:00Z",
                            "updatedAt": "2026-01-02T00:00:00Z",
                            "disabledAt": None,
                        },
                        "signingSecret": "whsec_456",
                    },
                    "meta": {"requestId": "r"},
                },
            )
        )
        respx.delete("https://www.agentref.dev/api/v1/webhooks/wh_1").mock(
            return_value=httpx.Response(
                200,
                json={"data": {"success": True}, "meta": {"requestId": "r"}},
            )
        )

        created = client.webhooks.create(
            name="Primary",
            url="https://example.com/webhooks",
            program_id="prog_1",
            subscribed_events=["program.created"],
            schema_version=2,
        )
        listed = client.webhooks.list(program_id="prog_1")
        updated = client.webhooks.update(
            "wh_1",
            name="Renamed",
            subscribed_events=["program.updated"],
            program_id=None,
            schema_version=2,
        )
        rotated = client.webhooks.rotate_secret("wh_1")
        deleted = client.webhooks.delete("wh_1")
        create_body = json.loads(create_route.calls[0].request.content)

    assert create_body["programId"] == "prog_1"
    assert created.signing_secret == "whsec_123"
    assert listed[0].schema_version == 2
    assert updated.program_id is None
    assert rotated.endpoint.secret_last_four == "5678"
    assert deleted.success is True


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
