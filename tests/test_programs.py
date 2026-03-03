from __future__ import annotations

import json

import httpx
import respx

from agentref import AgentRef


def _mock_program() -> dict:
    return {
        "id": "prog_1",
        "name": "Program",
        "description": None,
        "landingPageUrl": None,
        "commissionType": "one_time",
        "commissionPercent": 20,
        "commissionLimitMonths": None,
        "cookieDuration": 30,
        "payoutThreshold": 5000,
        "autoApproveAffiliates": True,
        "status": "active",
        "isPublic": True,
        "merchantId": "merch_1",
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
        )

        body = json.loads(route.calls[0].request.content)

    assert "commissionType" in body
    assert "commissionPercent" in body
    assert "cookieDuration" in body
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
            return_value=httpx.Response(200, json={"data": {"status": "public"}, "meta": {"requestId": "r"}})
        )
        client.programs.update_marketplace("prog_1", status="public", logo_url="https://cdn.example.com/logo.png")
        body = json.loads(route.calls[0].request.content)
    assert body["status"] == "public"
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
                        "email": "merchant@example.com",
                        "companyName": "AgentRef Inc",
                        "domain": None,
                        "domainVerified": False,
                        "trustLevel": "standard",
                        "stripeConnected": False,
                        "createdAt": "2026-01-01T00:00:00Z",
                    },
                    "meta": {"requestId": "r"},
                },
            )
        )
        connect_route = respx.post("https://www.agentref.dev/api/v1/merchant/connect-stripe").mock(
            return_value=httpx.Response(200, json={"data": {"url": "https://connect.stripe.com/x"}, "meta": {"requestId": "r"}})
        )

        merchant = client.merchant.update(company_name="AgentRef Inc")
        connect = client.merchant.connect_stripe()
        update_body = json.loads(update_route.calls[0].request.content)
        connect_method = connect_route.calls[0].request.method

    assert merchant.company_name == "AgentRef Inc"
    assert update_body["companyName"] == "AgentRef Inc"
    assert connect.url.startswith("https://connect.stripe.com")
    assert connect_method == "POST"
