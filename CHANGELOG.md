# Changelog

## Unreleased

- Removed obsolete merchant-scoped integration methods from the active SDK surface.
- Aligned `merchant.get()` / `merchant.update()` models with the final merchant profile contract.
- Added program-scoped integration methods on `programs`: Stripe connect/disconnect and domain verification/status/removal.
- Added `webhooks` resource for sync and async clients.

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
