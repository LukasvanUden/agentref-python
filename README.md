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

## Affiliate workspace quickstart

```python
from agentref import AgentRef

client = AgentRef(api_key="ak_aff_...")
overview = client.affiliate_workspace.overview()
programs = client.affiliate_workspace.list_programs()

if programs:
    detail = client.affiliate_workspace.get_program(programs[0].program_id)
    link = client.affiliate_workspace.create_link(
        name="Pricing",
        destination_path="/pricing",
        custom_slug="jane-review",
        program_id=detail.program_id,
        idempotency_key="create-pricing-link",
    )
    print(overview.program_count, detail.program_name, link["refCode"])
```

## Authentication

- Uses `Authorization: Bearer <key>`.
- Supports `ak_onb_*`, `ak_live_*`, `ak_aff_*`.
- Provide `api_key` directly or set `AGENTREF_API_KEY`.

## Resources

- `client.programs`: `list`, `list_all`, `get`, `create`, `update`, `delete`, `stats`, `list_affiliates`, `list_coupons`, `create_coupon`, `delete_coupon`, `list_invites`, `create_invite`, `update_marketplace`, `connect_stripe`, `disconnect_stripe`
- `client.applications`: `list`, `get`, `approve`, `decline`, `block`
- `client.affiliate_workspace`: `overview`, `identity`, `list_programs`, `get_program`, `earnings`, `list_program_earnings`, `list_payouts`, `list_links`, `create_link`, `update_link`, `delete_link`, `click_stats`
- `client.marketing_resources`: `list`, `create_social_post`, `update_social_post`, `create_social_post_media_upload_session`, `complete_social_post_media_upload`, `reorder_social_post_media`, `update_social_post_media`, `remove_social_post_media`, `replace_social_post_media`, `publish`, `unpublish`, `archive`, `notify_affiliates`, `create_download_url`, `list_for_affiliate`, `get_for_affiliate`, `create_affiliate_download_url`, `render_social_post`
- `client.affiliates`: `list`, `get`, `block`, `unblock`
- `client.conversions`: `list`, `stats`, `recent`
- `client.payouts`: `list`, `list_pending`, `stats`, `create`
- `client.flags`: `list`, `stats`, `resolve`
- `client.billing`: `current`, `tiers`, `subscribe`
- `client.merchant`: `get`, `update`
- `client.notifications`: `get`, `update`
- `client.payout_info`: `get`, `update`
- `client.onboarding`: `upsert_merchant_profile`, `complete`
- `client.tracking`: `get_program_status`
- `client.invites`: `get`, `claim`
- `client.marketplace`: `list_programs`, `apply`
- `client.webhooks`: `list`, `create`, `get`, `update`, `delete`, `rotate_secret`

## Applications

Pending affiliate joins are application records. Use `client.applications` to approve,
decline, or block applications before they become approved affiliate memberships.

```python
pending = client.applications.list(program_id="prog-uuid", status="pending")
client.applications.approve(
    pending.data[0].id,
    note="Relevant SaaS audience.",
    idempotency_key="approve-app-1",
)
```

## Marketing Resources

Merchant keys can manage resources. Affiliate keys can list, download, and render
published resources for joined programs.

```python
post = client.marketing_resources.create_social_post(
    "prog-uuid",
    title="Launch copy",
    body="Try AgentRef: {{affiliate_link}}",
    platforms=["linkedin"],
    status="published",
    idempotency_key="mr-social-launch",
)

client.marketing_resources.publish(
    post["id"],
    program_id="prog-uuid",
    notify_affiliates=True,
    idempotency_key="publish-mr-social-launch",
)

rendered = client.marketing_resources.render_social_post(
    post["id"],
    program_id="prog-uuid",
    affiliate_link_id="link-uuid",
)
```

## Marketplace, Invites, Onboarding, and Tracking

```python
client.onboarding.upsert_merchant_profile(company_name="Acme Inc.")
client.onboarding.complete()

tracking = client.tracking.get_program_status("prog-uuid")
invite = client.invites.get("invite-token")
claimed = client.invites.claim(invite["token"])

marketplace = client.marketplace.list_programs(sort="commission")
client.marketplace.apply(
    marketplace.data[0]["programId"],
    message="I manage affiliate agents for SaaS products.",
)
```

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

## Configuration

| Option | Default | Description |
|---|---|---|
| `api_key` | `AGENTREF_API_KEY` | API key |
| `base_url` | `https://www.agentref.co/api/v1` | Base API URL |
| `timeout` | `30.0` | Request timeout in seconds |
| `max_retries` | `2` | Retry count for GET/HEAD and POST+idempotency_key |
