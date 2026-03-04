# Changelog

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
