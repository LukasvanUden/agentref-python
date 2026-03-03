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
    name: str
    commission_type: str
    commission_percent: float
    commission_limit_months: Optional[int] = None
    cookie_duration: int
    payout_threshold: int
    auto_approve_affiliates: bool
    description: Optional[str] = None
    landing_page_url: Optional[str] = None
    status: str
    is_public: bool
    merchant_id: str
    created_at: str
    updated_at: str


class ProgramStats(BaseModel):
    model_config = _API_CONFIG

    clicks: int
    conversions: int
    revenue: float
    commissions: float
    period: str


class UpdateProgramMarketplaceParams(BaseModel):
    model_config = _API_CONFIG

    status: Optional[Literal["private", "public"]] = None
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
    email: str
    company_name: Optional[str] = None
    domain: Optional[str] = None
    domain_verified: bool
    trust_level: str
    stripe_connected: bool
    created_at: str


class UpdateMerchantParams(BaseModel):
    model_config = _API_CONFIG

    company_name: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    timezone: Optional[str] = None
    default_cookie_duration: Optional[int] = None
    default_payout_threshold: Optional[int] = None


class MerchantDomainStatus(BaseModel):
    model_config = _API_CONFIG

    domain: Optional[str] = None
    verified: bool
    txt_record: Optional[str] = None


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
