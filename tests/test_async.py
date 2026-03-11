import httpx
import pytest
import respx

from agentref import AsyncAgentRef


@pytest.mark.asyncio
async def test_async_client_programs_list() -> None:
    with respx.mock:
        respx.get("https://www.agentref.dev/api/v1/programs").return_value = httpx.Response(
            200,
            json={
                "data": [],
                "meta": {
                    "total": 0,
                    "page": 1,
                    "pageSize": 20,
                    "hasMore": False,
                    "requestId": "r",
                },
            },
        )

        async with AsyncAgentRef(api_key="ak_live_test") as client:
            result = await client.programs.list()

    assert result.meta.has_more is False
    assert result.meta.request_id == "r"


@pytest.mark.asyncio
async def test_async_list_all_stops_on_has_more_false() -> None:
    with respx.mock:
        respx.get("https://www.agentref.dev/api/v1/programs").mock(
            side_effect=[
                httpx.Response(
                    200,
                    json={
                        "data": [
                            {
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
                        ],
                        "meta": {
                            "total": 2,
                            "page": 1,
                            "pageSize": 1,
                            "hasMore": True,
                            "requestId": "r1",
                        },
                    },
                ),
                httpx.Response(
                    200,
                    json={
                        "data": [
                            {
                                "id": "prog_2",
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
                        ],
                        "meta": {
                            "total": 2,
                            "page": 2,
                            "pageSize": 1,
                            "hasMore": False,
                            "requestId": "r2",
                        },
                    },
                ),
            ]
        )

        async with AsyncAgentRef(api_key="ak_live_test") as client:
            ids = []
            async for program in client.programs.list_all(page_size=1):
                ids.append(program.id)

    assert ids == ["prog_1", "prog_2"]


@pytest.mark.asyncio
async def test_async_webhooks_list_uses_current_contract() -> None:
    with respx.mock:
        respx.get("https://www.agentref.dev/api/v1/webhooks").return_value = httpx.Response(
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

        async with AsyncAgentRef(api_key="ak_live_test") as client:
            result = await client.webhooks.list(program_id="prog_1")

    assert result[0].program_id == "prog_1"
    assert result[0].schema_version == 2
