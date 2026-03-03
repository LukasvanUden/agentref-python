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
