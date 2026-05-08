from __future__ import annotations

import json

import httpx
import respx

from agentref import AgentRef


def test_applications_list_and_review_use_applications_lifecycle() -> None:
    client = AgentRef(api_key="ak_live_test")

    with respx.mock:
        list_route = respx.get("https://www.agentref.co/api/v1/applications").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [{"id": "app_1", "status": "pending"}],
                    "meta": {"total": 1, "page": 1, "pageSize": 20, "hasMore": False, "requestId": "r"},
                },
            )
        )
        approve_route = respx.post("https://www.agentref.co/api/v1/applications/app_1/approve").mock(
            return_value=httpx.Response(
                200,
                json={"data": {"id": "app_1", "status": "approved"}, "meta": {"requestId": "r"}},
            )
        )

        applications = client.applications.list(status="pending")
        approved = client.applications.approve("app_1", note="looks good", idempotency_key="idem-app-1")

    assert list_route.calls[0].request.url.params["status"] == "pending"
    assert applications.data[0].id == "app_1"
    assert json.loads(approve_route.calls[0].request.content)["note"] == "looks good"
    assert approve_route.calls[0].request.headers["idempotency-key"] == "idem-app-1"
    assert approved.status == "approved"


def test_affiliate_workspace_exposes_links_earnings_payouts_clicks_and_identity() -> None:
    client = AgentRef(api_key="ak_live_test")

    with respx.mock:
        respx.get("https://www.agentref.co/api/v1/me").mock(
            return_value=httpx.Response(
                200,
                json={"data": {"key": {"ownerType": "affiliate"}, "owner": {"affiliateId": "aff_1"}}, "meta": {}},
            )
        )
        respx.get("https://www.agentref.co/api/v1/me/earnings").mock(
            return_value=httpx.Response(200, json={"data": {"total": 100}, "meta": {}})
        )
        respx.get("https://www.agentref.co/api/v1/me/earnings/prog_1").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [{"id": "earn_1", "amount": 100}],
                    "meta": {"total": 1, "page": 1, "pageSize": 20, "hasMore": False, "requestId": "r"},
                },
            )
        )
        respx.get("https://www.agentref.co/api/v1/me/payouts").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [{"id": "pay_1"}],
                    "meta": {"total": 1, "page": 1, "pageSize": 20, "hasMore": False, "requestId": "r"},
                },
            )
        )
        clicks_route = respx.get("https://www.agentref.co/api/v1/me/clicks").mock(
            return_value=httpx.Response(200, json={"data": {"totalClicks": 4}, "meta": {}})
        )
        link_route = respx.post("https://www.agentref.co/api/v1/me/links").mock(
            return_value=httpx.Response(
                201,
                json={"data": {"id": "link_1", "refCode": "jane-review"}, "meta": {}},
            )
        )

        identity = client.affiliate_workspace.identity()
        earnings = client.affiliate_workspace.earnings()
        program_earnings = client.affiliate_workspace.list_program_earnings("prog_1")
        payouts = client.affiliate_workspace.list_payouts()
        clicks = client.affiliate_workspace.click_stats(program_id="prog_1")
        link = client.affiliate_workspace.create_link(
            name="Pricing",
            destination_path="/pricing",
            custom_slug="jane-review",
            program_id="prog_1",
            idempotency_key="idem-link-1",
        )

    assert identity["key"]["ownerType"] == "affiliate"
    assert earnings["total"] == 100
    assert program_earnings.data[0]["id"] == "earn_1"
    assert payouts.data[0]["id"] == "pay_1"
    assert clicks["totalClicks"] == 4
    assert clicks_route.calls[0].request.url.params["program_id"] == "prog_1"
    link_body = json.loads(link_route.calls[0].request.content)
    assert link_body == {
        "name": "Pricing",
        "destination_path": "/pricing",
        "custom_slug": "jane-review",
    }
    assert link_route.calls[0].request.url.params["program_id"] == "prog_1"
    assert link["refCode"] == "jane-review"


def test_marketing_resources_supports_merchant_and_affiliate_workflows() -> None:
    client = AgentRef(api_key="ak_live_test")

    with respx.mock:
        list_route = respx.get("https://www.agentref.co/api/v1/programs/prog_1/marketing-resources").mock(
            return_value=httpx.Response(200, json={"data": [{"id": "res_1", "kind": "social_post"}], "meta": {}})
        )
        create_route = respx.post(
            "https://www.agentref.co/api/v1/programs/prog_1/marketing-resources/social-posts"
        ).mock(
            return_value=httpx.Response(
                201,
                json={"data": {"id": "res_1", "title": "Launch"}, "meta": {}},
            )
        )
        respx.post("https://www.agentref.co/api/v1/marketing-resources/res_1/publish").mock(
            return_value=httpx.Response(
                200,
                json={"data": {"resource": {"id": "res_1"}, "notification": {"requested": True}}, "meta": {}},
            )
        )
        respx.get("https://www.agentref.co/api/v1/me/programs/prog_1/marketing-resources").mock(
            return_value=httpx.Response(200, json={"data": [{"id": "res_1", "title": "Launch"}], "meta": {}})
        )
        render_route = respx.post(
            "https://www.agentref.co/api/v1/me/marketing-resources/social-posts/res_1/render"
        ).mock(
            return_value=httpx.Response(
                200,
                json={"data": {"body": "Post https://ref.example/link", "disclosure": "#ad"}, "meta": {}},
            )
        )

        resources = client.marketing_resources.list("prog_1", kind="social_posts")
        created = client.marketing_resources.create_social_post(
            "prog_1",
            title="Launch",
            body="Try {{affiliate_link}}",
            platforms=["linkedin"],
            status="published",
            idempotency_key="idem-mr-1",
        )
        published = client.marketing_resources.publish(
            "res_1",
            program_id="prog_1",
            notify_affiliates=True,
            idempotency_key="idem-publish-1",
        )
        affiliate_resources = client.marketing_resources.list_for_affiliate("prog_1")
        rendered = client.marketing_resources.render_social_post(
            "res_1",
            program_id="prog_1",
            affiliate_link_id="link_1",
        )

    assert list_route.calls[0].request.url.params["kind"] == "social_posts"
    assert resources[0]["id"] == "res_1"
    assert json.loads(create_route.calls[0].request.content)["status"] == "published"
    assert created["title"] == "Launch"
    assert published["notification"]["requested"] is True
    assert affiliate_resources[0]["id"] == "res_1"
    assert json.loads(render_route.calls[0].request.content) == {
        "program_id": "prog_1",
        "affiliate_link_id": "link_1",
    }
    assert rendered["disclosure"] == "#ad"


def test_onboarding_tracking_invites_marketplace_notifications_and_payout_info_are_top_level_resources() -> None:
    client = AgentRef(api_key="ak_live_test")

    with respx.mock:
        respx.post("https://www.agentref.co/api/v1/onboarding/merchant").mock(
            return_value=httpx.Response(
                200,
                json={"data": {"merchantId": "merch_1", "companyName": "AgentRef"}, "meta": {}},
            )
        )
        respx.post("https://www.agentref.co/api/v1/onboarding/complete").mock(
            return_value=httpx.Response(
                200,
                json={"data": {"onboardingCompleted": True, "onboardingStep": 4}, "meta": {}},
            )
        )
        respx.get("https://www.agentref.co/api/v1/programs/prog_1/tracking/status").mock(
            return_value=httpx.Response(
                200,
                json={"data": {"programId": "prog_1", "health": {"scriptInstalled": {"complete": True}}}, "meta": {}},
            )
        )
        respx.get("https://www.agentref.co/api/v1/invites/invite_token").mock(
            return_value=httpx.Response(200, json={"data": {"token": "invite_token", "programId": "prog_1"}, "meta": {}})
        )
        respx.post("https://www.agentref.co/api/v1/invites/invite_token/claim").mock(
            return_value=httpx.Response(
                201,
                json={"data": {"affiliateId": "aff_1", "programId": "prog_1"}, "meta": {}},
            )
        )
        respx.get("https://www.agentref.co/api/v1/marketplace/programs").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [{"programId": "prog_1", "commissionPercent": 30}],
                    "meta": {"total": 1, "page": 1, "pageSize": 20, "hasMore": False, "requestId": "r"},
                },
            )
        )
        respx.post("https://www.agentref.co/api/v1/marketplace/apply/prog_1").mock(
            return_value=httpx.Response(
                201,
                json={"data": {"programId": "prog_1", "message": "I build AI agents."}, "meta": {}},
            )
        )
        respx.get("https://www.agentref.co/api/v1/merchant/notifications").mock(
            return_value=httpx.Response(200, json={"data": {"newAffiliate": True, "weeklyDigest": False}, "meta": {}})
        )
        respx.get("https://www.agentref.co/api/v1/me/payout-info").mock(
            return_value=httpx.Response(
                200,
                json={"data": {"payoutMethod": "paypal", "paypalEmail": "pay@example.com"}, "meta": {}},
            )
        )

        merchant = client.onboarding.upsert_merchant_profile(company_name="AgentRef")
        completed = client.onboarding.complete()
        tracking = client.tracking.get_program_status("prog_1")
        invite = client.invites.get("invite_token")
        claimed = client.invites.claim("invite_token")
        programs = client.marketplace.list_programs(sort="commission")
        application = client.marketplace.apply("prog_1", message="I build AI agents.")
        notifications = client.notifications.get()
        payout_info = client.payout_info.get()

    assert merchant["companyName"] == "AgentRef"
    assert completed["onboardingCompleted"] is True
    assert tracking["programId"] == "prog_1"
    assert invite["token"] == "invite_token"
    assert claimed["affiliateId"] == "aff_1"
    assert programs.data[0]["programId"] == "prog_1"
    assert application["message"] == "I build AI agents."
    assert notifications.new_affiliate is True
    assert payout_info.paypal_email == "pay@example.com"
