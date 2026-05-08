# Changelog

## Unreleased

- No unreleased changes.

## 5.1.1

- Aligned Affiliate Link examples with the live API response `code` field.

## 5.1.0

- Added full REST SDK coverage for Applications, Marketing Resources, Onboarding, Tracking, public Invites, Marketplace discovery/application, and the expanded Affiliate Workspace.
- Kept sync and async clients in parity for the new resource namespaces.
- Updated affiliate link creation to use `destination_path` plus optional `custom_slug`.
- Moved application review to `client.applications.approve/decline/block` and removed the stale affiliate approval helper from the active contract.
- Updated marketplace status types from `pending` to `draft` and added `partially_refunded` conversion status support.
- Updated README to document the complete v5.1.0 resource surface.

## 5.0.2

- Switched the default API host to `https://www.agentref.co/api/v1`.
- Removed stale domain-verification expectations and legacy tracking fallback fields from the public SDK contract.
- Updated tests and README to match the active API surface and supported key prefixes.

## 1.0.4

- **Fix:** `payout_info.update()` now sends `PATCH` instead of `PUT` to match the API contract.
- Added optional `include` parameter to `affiliates.get(id, include='stats')` for fetching aggregated stats.

## 1.0.3

- Added `search`, `sort_by`, `sort_order`, `status` parameters to `affiliates.list()`.
- Added `tracking_code`, `skip_onboarding` parameters to `programs.create_invite()`.
- Added `payout_info` resource with `get()` and `update()` methods.
- Added `notifications` resource with `get()` and `update()` methods.
- Added new models: `PayoutInfo`, `UpdatePayoutInfoParams`, `NotificationPreferences`, `UpdateNotificationPreferencesParams`.

## 1.0.2

- Hardened idempotency retry gate: POST retries now require a non-empty idempotency key.
- Added missing merchant API methods for sync+async clients: merchant update/connect_stripe, payouts create, programs marketplace/invites/coupon delete.
- Tightened Pydantic contract models for core resources and payloads.

## 1.0.0

- Initial release.
- Sync + async clients.
- Typed resources for merchant-facing REST API v1 surfaces.
- Retry/idempotency safeguards aligned with API safety model.
