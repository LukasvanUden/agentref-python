# AgentRef Python SDK

Official Python SDK for the AgentRef REST API v1.

## Install

```bash
pip install agentref
```

## Quickstart

```python
from agentref import AgentRef

client = AgentRef(api_key="ak_live_...")
programs = client.programs.list()
print(programs.meta.request_id)
```

## Async quickstart

```python
from agentref import AsyncAgentRef

async with AsyncAgentRef(api_key="ak_live_...") as client:
    programs = await client.programs.list()
```

## Authentication

- Uses `Authorization: Bearer <key>`.
- Supports `ak_live_*`, `ak_aff_*`.
- Provide `api_key` directly or set `AGENTREF_API_KEY`.

## Resources

- `client.programs`: `list`, `list_all`, `get`, `create`, `update`, `delete`, `stats`, `list_affiliates`, `list_coupons`, `create_coupon`, `delete_coupon`, `list_invites`, `create_invite`, `update_marketplace`, `connect_stripe`, `disconnect_stripe`, `verify_domain`, `remove_domain_verification`, `get_domain_status`
- `client.affiliates`: `list`, `get`, `approve`, `block`, `unblock`
- `client.conversions`: `list`, `stats`, `recent`
- `client.payouts`: `list`, `list_pending`, `stats`, `create`
- `client.flags`: `list`, `stats`, `resolve`
- `client.billing`: `current`, `tiers`, `subscribe`
- `client.merchant`: `get`, `update`
- `client.notifications`: `get`, `update`
- `client.payout_info`: `get`, `update`
- `client.webhooks`: `list`, `create`, `get`, `update`, `delete`, `rotate_secret`

## Pagination

List endpoints return `PaginatedResponse[T]` with:

- `meta.total`
- `meta.page`
- `meta.page_size`
- `meta.has_more`
- `meta.next_cursor`
- `meta.request_id`

Auto-pagination (`list_all`) stops on `has_more is False`.

## Idempotency and retry behavior

- GET/HEAD: auto-retry on 429/5xx.
- POST: auto-retry only when `idempotency_key` is provided.
- PATCH/DELETE: never auto-retry.
- `Idempotency-Key` header is sent only for POST requests.

## Error handling

```python
from agentref import AgentRef
from agentref.errors import ForbiddenError, NotFoundError, RateLimitError, AgentRefError

client = AgentRef(api_key="ak_live_...")

try:
    client.programs.get("missing-id")
except ForbiddenError as e:
    print(e.code, e.request_id)
except NotFoundError as e:
    print(e.request_id)
except RateLimitError as e:
    print(e.retry_after)
except AgentRefError as e:
    print(e.status)
```
