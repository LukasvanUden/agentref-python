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
    is_public: Optional[bool] = None
    merchant_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class Affiliate(BaseModel):
    model_config = _API_CONFIG

    id: str
    user_id: Optional[str] = None
    program_id: Optional[str] = None
    code: Optional[str] = None
    status: Optional[str] = None
    total_clicks: Optional[int] = None
    total_conversions: Optional[int] = None
    total_earnings: Optional[float] = None
    created_at: Optional[str] = None


class Conversion(BaseModel):
    model_config = _API_CONFIG

    id: str
    affiliate_id: Optional[str] = None
    program_id: Optional[str] = None
    amount: Optional[float] = None
    commission: Optional[float] = None
    status: Optional[str] = None
    method: Optional[str] = None
    stripe_session_id: Optional[str] = None
    created_at: Optional[str] = None


class ConversionStats(BaseModel):
    model_config = _API_CONFIG

    total: int = 0
    pending: int = 0
    approved: int = 0
    total_revenue: float = 0
    total_commissions: float = 0


class Payout(BaseModel):
    model_config = _API_CONFIG

    id: str
    affiliate_id: Optional[str] = None
    amount: Optional[float] = None
    status: Optional[str] = None
    method: Optional[str] = None
    created_at: Optional[str] = None
    completed_at: Optional[str] = None


class PendingAffiliate(BaseModel):
    model_config = _API_CONFIG

    affiliate_id: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    code: Optional[str] = None
    program_id: Optional[str] = None
    program_name: Optional[str] = None
    payout_method: Optional[str] = None
    paypal_email: Optional[str] = None
    bank_iban: Optional[str] = None
    pending_amount: Optional[float] = None
    currency: Optional[str] = None
    threshold: Optional[float] = None
    meets_threshold: Optional[bool] = None
    commission_count: Optional[int] = None
    has_payout_method: Optional[bool] = None


class PayoutStats(BaseModel):
    model_config = _API_CONFIG

    total_paid: float = 0
    total_pending: float = 0
    count: int = 0


class Flag(BaseModel):
    model_config = _API_CONFIG

    id: str
    affiliate_id: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    note: Optional[str] = None
    created_at: Optional[str] = None
    resolved_at: Optional[str] = None


class FlagStats(BaseModel):
    model_config = _API_CONFIG

    open: int = 0
    reviewed: int = 0
    dismissed: int = 0
    confirmed: int = 0
    total: int = 0


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
    max_revenue: Optional[float] = None
    features: Optional[List[str]] = None
    bookable: Optional[bool] = None


class BillingStatus(BaseModel):
    model_config = _API_CONFIG

    tier: Optional[str] = None
    monthly_revenue: Optional[float] = None
    next_tier: Optional[str] = None
    stripe_subscription_id: Optional[str] = None


class Merchant(BaseModel):
    model_config = _API_CONFIG

    id: str
    email: str
    company_name: Optional[str] = None
    domain: Optional[str] = None
    domain_verified: Optional[bool] = None
    trust_level: Optional[str] = None
    stripe_connected: Optional[bool] = None
    created_at: Optional[str] = None


class Coupon(BaseModel):
    model_config = _API_CONFIG

    id: str
    code: str
    affiliate_id: Optional[str] = None
    program_id: Optional[str] = None
    created_at: Optional[str] = None


class Invite(BaseModel):
    model_config = _API_CONFIG

    token: Optional[str] = None
    email: Optional[str] = None
    program_id: Optional[str] = None
    expires_at: Optional[str] = None
    created_at: Optional[str] = None
