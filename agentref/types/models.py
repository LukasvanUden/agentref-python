from __future__ import annotations

from typing import Any, Dict, Generic, List, Literal, Optional, TypeVar

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

T = TypeVar("T")

_API_CONFIG = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class PaginationMeta(BaseModel):
    model_config = _API_CONFIG

    total: int
    page: int
    page_size: int
    has_more: bool
    next_cursor: Optional[str] = None
    request_id: str


class PaginatedResponse(BaseModel, Generic[T]):
    model_config = _API_CONFIG

    data: List[T]
    meta: PaginationMeta


class Program(BaseModel):
    model_config = _API_CONFIG

    id: str
    merchant_id: str
    name: str
    description: Optional[str] = None
    slug: str
    landing_page_url: Optional[str] = None
    portal_slug: Optional[str] = None
    status: str
    marketplace_status: str
    marketplace_category: Optional[str] = None
    marketplace_description: Optional[str] = None
    marketplace_logo_url: Optional[str] = None
    commission_type: str
    commission_percent: float
    commission_limit_months: Optional[int] = None
    commission_hold_days: int
    cookie_duration: int
    payout_threshold: int
    currency: str
    auto_approve_affiliates: bool
    terms_url: Optional[str] = None
    created_at: str
    updated_at: str


class ProgramStats(BaseModel):
    model_config = _API_CONFIG

    program_id: str
    program_name: str
    status: str
    total_revenue: float
    total_conversions: int
    total_commissions: float
    pending_commissions: float
    active_affiliates: int
    conversions_by_status: Dict[str, int]


class UpdateProgramMarketplaceParams(BaseModel):
    model_config = _API_CONFIG

    status: Optional[Literal["private", "pending", "public"]] = None
    category: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None


class Affiliate(BaseModel):
    model_config = _API_CONFIG

    id: str
    user_id: str
    program_id: str
    code: str
    status: str
    total_clicks: int
    total_conversions: int
    total_earnings: float
    created_at: str


class Conversion(BaseModel):
    model_config = _API_CONFIG

    id: str
    affiliate_id: str
    program_id: str
    amount: float
    commission: float
    status: str
    method: str
    stripe_session_id: Optional[str] = None
    created_at: str


class ConversionStats(BaseModel):
    model_config = _API_CONFIG

    total: int
    pending: int
    approved: int
    total_revenue: float
    total_commissions: float


class Payout(BaseModel):
    model_config = _API_CONFIG

    id: str
    affiliate_id: str
    amount: float
    status: str
    method: Optional[str] = None
    created_at: str
    completed_at: Optional[str] = None


class CreatePayoutParams(BaseModel):
    model_config = _API_CONFIG

    affiliate_id: str
    program_id: str
    method: Literal["paypal", "bank_transfer"]
    notes: Optional[str] = None


class PendingAffiliate(BaseModel):
    model_config = _API_CONFIG

    affiliate_id: str
    email: str
    name: Optional[str] = None
    code: str
    program_id: str
    program_name: str
    payout_method: Optional[str] = None
    paypal_email: Optional[str] = None
    bank_iban: Optional[str] = None
    pending_amount: float
    currency: str
    threshold: float
    meets_threshold: bool
    commission_count: int
    has_payout_method: bool


class PayoutStats(BaseModel):
    model_config = _API_CONFIG

    total_paid: float
    total_pending: float
    count: int


class Flag(BaseModel):
    model_config = _API_CONFIG

    id: str
    affiliate_id: str
    type: str
    status: str
    details: Optional[Dict[str, Any]] = None
    note: Optional[str] = None
    created_at: str
    resolved_at: Optional[str] = None


class FlagStats(BaseModel):
    model_config = _API_CONFIG

    open: int
    reviewed: int
    dismissed: int
    confirmed: int
    total: int


class ResolveFlagParams(BaseModel):
    model_config = _API_CONFIG

    status: Literal["reviewed", "dismissed", "confirmed"]
    note: Optional[str] = None
    block_affiliate: bool = False


class BillingTier(BaseModel):
    model_config = _API_CONFIG

    id: str
    name: str
    price: float
    max_revenue: float
    features: List[str]
    bookable: bool


class BillingStatus(BaseModel):
    model_config = _API_CONFIG

    tier: str
    monthly_revenue: float
    next_tier: Optional[str] = None
    stripe_subscription_id: Optional[str] = None


class Merchant(BaseModel):
    model_config = _API_CONFIG

    id: str
    user_id: str
    company_name: str
    website: Optional[str] = None
    logo_url: Optional[str] = None
    stripe_account_id: Optional[str] = None
    stripe_connected_at: Optional[str] = None
    billing_tier: str
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None
    payment_status: str
    last_payment_failed_at: Optional[str] = None
    default_cookie_duration: int
    default_payout_threshold: int
    timezone: str
    tracking_requires_consent: bool
    tracking_param_aliases: List[str]
    tracking_legacy_metadata_fallback_enabled: bool
    state: str
    verified_domain: Optional[str] = None
    domain_verification_token: Optional[str] = None
    domain_verified_at: Optional[str] = None
    notification_preferences: Optional[Dict[str, bool]] = None
    onboarding_completed: bool
    onboarding_step: int
    created_at: str
    updated_at: str


class UpdateMerchantParams(BaseModel):
    model_config = _API_CONFIG

    company_name: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    timezone: Optional[str] = None
    default_cookie_duration: Optional[int] = None
    default_payout_threshold: Optional[int] = None
    tracking_requires_consent: Optional[bool] = None
    tracking_param_aliases: Optional[List[str]] = None
    tracking_legacy_metadata_fallback_enabled: Optional[bool] = None


class MerchantDomainStatus(BaseModel):
    model_config = _API_CONFIG

    status: str
    domain: Optional[str] = None
    txt_record: Optional[str] = None
    verified_at: Optional[str] = None
    tracking_mode: str
    advanced_tracking_enabled: bool


class StripeConnectSession(BaseModel):
    model_config = _API_CONFIG

    url: str


class Coupon(BaseModel):
    model_config = _API_CONFIG

    id: str
    code: str
    affiliate_id: str
    program_id: str
    created_at: str


class Invite(BaseModel):
    model_config = _API_CONFIG

    token: str
    email: str
    program_id: str
    expires_at: str
    created_at: str


class PayoutInfo(BaseModel):
    model_config = _API_CONFIG

    payout_method: Optional[str] = None
    paypal_email: Optional[str] = None
    bank_account_holder: Optional[str] = None
    bank_iban: Optional[str] = None
    bank_bic: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    vat_id: Optional[str] = None


class UpdatePayoutInfoParams(BaseModel):
    model_config = _API_CONFIG

    payout_method: Optional[str] = None
    paypal_email: Optional[str] = None
    bank_account_holder: Optional[str] = None
    bank_iban: Optional[str] = None
    bank_bic: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    vat_id: Optional[str] = None


class NotificationPreferences(BaseModel):
    model_config = _API_CONFIG

    new_affiliate: bool = True
    new_conversion: bool = True
    commission_approved: bool = True
    payout_processed: bool = True
    weekly_digest: bool = False


class UpdateNotificationPreferencesParams(BaseModel):
    model_config = _API_CONFIG

    new_affiliate: Optional[bool] = None
    new_conversion: Optional[bool] = None
    commission_approved: Optional[bool] = None
    payout_processed: Optional[bool] = None
    weekly_digest: Optional[bool] = None
