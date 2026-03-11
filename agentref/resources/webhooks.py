from __future__ import annotations

from typing import List, Literal, Optional

from .._http import AsyncHttpClient, SyncHttpClient
from ..types.models import (
    CreateWebhookEndpointParams,
    SuccessResponse,
    WebhookEndpoint,
    WebhookSecretResponse,
)

_UNSET = object()
WebhookEventType = Literal[
    "program.created",
    "program.updated",
    "affiliate.joined",
    "affiliate.approved",
    "affiliate.blocked",
    "affiliate.unblocked",
    "conversion.created",
    "conversion.refunded",
    "payout.created",
    "payout.processing",
    "payout.completed",
    "payout.failed",
    "flag.resolved",
]


class WebhooksResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def list(self, *, program_id: Optional[str] = None) -> List[WebhookEndpoint]:
        envelope = self._http.request("GET", "/webhooks", params={"programId": program_id})
        data = envelope.get("data", [])
        if not isinstance(data, list):
            return []
        return [WebhookEndpoint.model_validate(item) for item in data]

    def create(
        self,
        *,
        name: str,
        url: str,
        subscribed_events: List[WebhookEventType],
        program_id: Optional[str] = None,
        schema_version: Optional[Literal[2]] = None,
    ) -> WebhookSecretResponse:
        payload = CreateWebhookEndpointParams(
            name=name,
            url=url,
            subscribed_events=subscribed_events,
            program_id=program_id,
            schema_version=schema_version,
        ).model_dump(by_alias=True, exclude_none=True)
        envelope = self._http.request("POST", "/webhooks", json=payload)
        return WebhookSecretResponse.model_validate(envelope["data"])

    def get(self, id: str) -> WebhookEndpoint:
        envelope = self._http.request("GET", f"/webhooks/{id}")
        return WebhookEndpoint.model_validate(envelope["data"])

    def update(
        self,
        id: str,
        *,
        name: Optional[str] = None,
        url: Optional[str] = None,
        subscribed_events: Optional[List[WebhookEventType]] = None,
        program_id: object = _UNSET,
        schema_version: Optional[Literal[2]] = None,
    ) -> WebhookEndpoint:
        payload: dict[str, object] = {}
        if name is not None:
            payload["name"] = name
        if url is not None:
            payload["url"] = url
        if subscribed_events is not None:
            payload["subscribedEvents"] = subscribed_events
        if program_id is not _UNSET:
            payload["programId"] = program_id
        if schema_version is not None:
            payload["schemaVersion"] = schema_version
        envelope = self._http.request("PATCH", f"/webhooks/{id}", json=payload)
        return WebhookEndpoint.model_validate(envelope["data"])

    def delete(self, id: str) -> SuccessResponse:
        envelope = self._http.request("DELETE", f"/webhooks/{id}")
        return SuccessResponse.model_validate(envelope["data"])

    def rotate_secret(self, id: str) -> WebhookSecretResponse:
        envelope = self._http.request("POST", f"/webhooks/{id}/rotate-secret")
        return WebhookSecretResponse.model_validate(envelope["data"])


class AsyncWebhooksResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(self, *, program_id: Optional[str] = None) -> List[WebhookEndpoint]:
        envelope = await self._http.request("GET", "/webhooks", params={"programId": program_id})
        data = envelope.get("data", [])
        if not isinstance(data, list):
            return []
        return [WebhookEndpoint.model_validate(item) for item in data]

    async def create(
        self,
        *,
        name: str,
        url: str,
        subscribed_events: List[WebhookEventType],
        program_id: Optional[str] = None,
        schema_version: Optional[Literal[2]] = None,
    ) -> WebhookSecretResponse:
        payload = CreateWebhookEndpointParams(
            name=name,
            url=url,
            subscribed_events=subscribed_events,
            program_id=program_id,
            schema_version=schema_version,
        ).model_dump(by_alias=True, exclude_none=True)
        envelope = await self._http.request("POST", "/webhooks", json=payload)
        return WebhookSecretResponse.model_validate(envelope["data"])

    async def get(self, id: str) -> WebhookEndpoint:
        envelope = await self._http.request("GET", f"/webhooks/{id}")
        return WebhookEndpoint.model_validate(envelope["data"])

    async def update(
        self,
        id: str,
        *,
        name: Optional[str] = None,
        url: Optional[str] = None,
        subscribed_events: Optional[List[WebhookEventType]] = None,
        program_id: object = _UNSET,
        schema_version: Optional[Literal[2]] = None,
    ) -> WebhookEndpoint:
        payload: dict[str, object] = {}
        if name is not None:
            payload["name"] = name
        if url is not None:
            payload["url"] = url
        if subscribed_events is not None:
            payload["subscribedEvents"] = subscribed_events
        if program_id is not _UNSET:
            payload["programId"] = program_id
        if schema_version is not None:
            payload["schemaVersion"] = schema_version
        envelope = await self._http.request("PATCH", f"/webhooks/{id}", json=payload)
        return WebhookEndpoint.model_validate(envelope["data"])

    async def delete(self, id: str) -> SuccessResponse:
        envelope = await self._http.request("DELETE", f"/webhooks/{id}")
        return SuccessResponse.model_validate(envelope["data"])

    async def rotate_secret(self, id: str) -> WebhookSecretResponse:
        envelope = await self._http.request("POST", f"/webhooks/{id}/rotate-secret")
        return WebhookSecretResponse.model_validate(envelope["data"])
