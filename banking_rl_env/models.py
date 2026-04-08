# banking_rl_env/models.py
from enum import Enum
from typing import List, Dict, Literal
from pydantic import BaseModel, Field


class FraudActionType(str, Enum):
    BLOCK_TRANSACTION = "BLOCK_TRANSACTION"
    ALLOW_TRANSACTION = "ALLOW_TRANSACTION"
    FLAG_FOR_REVIEW = "FLAG_FOR_REVIEW"
    UPDATE_RISK_THRESHOLD = "UPDATE_RISK_THRESHOLD"


class CollectionsActionType(str, Enum):
    CALL_CUSTOMER = "CALL_CUSTOMER"
    SEND_SMS = "SEND_SMS"
    SEND_WHATSAPP = "SEND_WHATSAPP"
    OFFER_SETTLEMENT = "OFFER_SETTLEMENT"
    ESCALATE_TO_AGENT = "ESCALATE_TO_AGENT"
    WRITE_OFF = "WRITE_OFF"


class CreditActionType(str, Enum):
    APPROVE_LOAN = "APPROVE_LOAN"
    REJECT_LOAN = "REJECT_LOAN"
    OFFER_LOWER_AMOUNT = "OFFER_LOWER_AMOUNT"
    ADJUST_CREDIT_LIMIT = "ADJUST_CREDIT_LIMIT"


class CashActionType(str, Enum):
    DISPATCH_REFILL = "DISPATCH_REFILL"
    HOLD_REFILL = "HOLD_REFILL"
    TRANSFER_CASH = "TRANSFER_CASH"


class BankingAction(BaseModel):
    domain: Literal["fraud", "collections", "credit", "cash"]
    action_type: str
    parameters: Dict = Field(default_factory=dict)


class FraudState(BaseModel):
    suspicious_count: int = 0
    false_positives: int = 0
    risk_threshold: float = 0.5
    alerts: List[str] = Field(default_factory=list)


class CollectionsState(BaseModel):
    buckets: Dict[str, int] = Field(default_factory=lambda: {'0-30': 100, '31-60': 50, '61-90': 20, '90+': 10})
    total_overdue: float = 500000.0
    recovery_rate: float = 0.0


class CreditState(BaseModel):
    pending_applications: int = 15
    approval_rate: float = 0.7
    default_rate: float = 0.02


class CashState(BaseModel):
    branch_balances: Dict[str, float] = Field(
        default_factory=lambda: {'Branch_A': 200000.0, 'Branch_B': 150000.0}
    )
    out_of_cash_events: int = 0
    refill_costs: float = 0.0


class CustomerHealth(BaseModel):
    satisfaction_score: float = 5.0
    complaints: int = 0


class BankingObservation(BaseModel):
    fraud_state: FraudState
    collections_state: CollectionsState
    credit_state: CreditState
    cash_state: CashState
    customer_health: CustomerHealth
    reward: float
    done: bool
    day: int
    bank_capital: float
