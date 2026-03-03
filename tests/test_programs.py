from __future__ import annotations

import json

import httpx
import respx

from agentref import AgentRef


def _mock_program() -> dict:
    return {
        "id": "prog_1",
        "name": "Program",
        "commissionType": "one_time",
        "commissionPercent": 20,
        "commissionLimitMonths": None,
        "cookieDuration": 30,
        "payoutThreshold": 5000,
        "autoApproveAffiliates": True,
        "status": "active",
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
            return_value=httpx.Response(200, json={"data": {"id": "flag_1"}, "meta": {"requestId": "r"}})
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
