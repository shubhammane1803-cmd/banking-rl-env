# banking_rl_env/server/banking_environment.py
import random
import sys
import os

sys.path.insert(0, '/content')

from banking_rl_env.models import (
    BankingObservation, FraudState, CollectionsState,
    CreditState, CashState, CustomerHealth, BankingAction
)


class BankingEnvironment:
    """Core Banking RL Environment — covers Fraud, Collections, Credit, Cash."""

    def __init__(self, max_days: int = 365):
        self.max_days = max_days
        self.reset()

    def reset(self) -> BankingObservation:
        self.day = 1
        self.bank_capital = 10_000_000.0
        self.fraud_state = FraudState()
        self.collections_state = CollectionsState()
        self.credit_state = CreditState()
        self.cash_state = CashState()
        self.customer_health = CustomerHealth()
        return self._get_observation(0.0, False)

    def step(self, action: BankingAction) -> BankingObservation:
        reward = 0.0

        if action.domain == 'fraud':
            reward += self._execute_fraud_action(action)
        elif action.domain == 'collections':
            reward += self._execute_collections_action(action)
        elif action.domain == 'credit':
            reward += self._execute_credit_action(action)
        elif action.domain == 'cash':
            reward += self._execute_cash_action(action)

        # Advance environment state every 10 steps
        if self.day % 10 == 0:
            self._advance_day()

        self.day += 1
        done = (
            self.day >= self.max_days or
            self.bank_capital < 0 or
            self.customer_health.satisfaction_score < 1.0
        )
        return self._get_observation(reward, done)

    def _execute_fraud_action(self, action: BankingAction) -> float:
        if action.action_type == 'UPDATE_RISK_THRESHOLD':
            threshold = action.parameters.get('threshold', 0.5)
            self.fraud_state.risk_threshold = float(threshold)
            return 10.0
        elif action.action_type == 'BLOCK_TRANSACTION':
            self.fraud_state.suspicious_count += 1
            return 15.0
        elif action.action_type == 'ALLOW_TRANSACTION':
            return 5.0
        elif action.action_type == 'FLAG_FOR_REVIEW':
            self.fraud_state.alerts.append(f"Day {self.day}: flagged")
            return 8.0
        return 0.0

    def _execute_collections_action(self, action: BankingAction) -> float:
        if action.action_type == 'CALL_CUSTOMER':
            if random.random() < 0.4:
                recovered = random.uniform(500, 2000)
                self.bank_capital += recovered
                self.collections_state.total_overdue -= recovered
                return 50.0
            return -5.0  # call cost, no recovery
        elif action.action_type == 'SEND_SMS':
            return 5.0
        elif action.action_type == 'OFFER_SETTLEMENT':
            self.bank_capital += 1000
            return 30.0
        elif action.action_type == 'WRITE_OFF':
            self.bank_capital -= 5000
            return -20.0
        return 0.0

    def _execute_credit_action(self, action: BankingAction) -> float:
        if action.action_type == 'APPROVE_LOAN':
            amount = float(action.parameters.get('amount', 10000))
            self.bank_capital -= amount
            # Expected return with interest
            self.bank_capital += amount * 0.12  # 12% annual interest placeholder
            return 20.0
        elif action.action_type == 'REJECT_LOAN':
            return -5.0  # Opportunity cost
        elif action.action_type == 'ADJUST_CREDIT_LIMIT':
            return 10.0
        return 0.0

    def _execute_cash_action(self, action: BankingAction) -> float:
        if action.action_type == 'DISPATCH_REFILL':
            branch = action.parameters.get('branch', 'Branch_A')
            amount = float(action.parameters.get('amount', 100000))
            self.bank_capital -= 500  # transport cost
            self.cash_state.refill_costs += 500
            if branch in self.cash_state.branch_balances:
                self.cash_state.branch_balances[branch] += amount
            return -5.0
        elif action.action_type == 'HOLD_REFILL':
            return 2.0
        elif action.action_type == 'TRANSFER_CASH':
            return 5.0
        return 0.0

    def _advance_day(self):
        """Simulate daily cash withdrawals at branches."""
        for branch in list(self.cash_state.branch_balances.keys()):
            withdrawal = random.uniform(10000, 30000)
            self.cash_state.branch_balances[branch] -= withdrawal
            if self.cash_state.branch_balances[branch] < 0:
                self.cash_state.out_of_cash_events += 1
                self.customer_health.satisfaction_score -= 0.5
                self.customer_health.complaints += 1

    def _get_observation(self, reward: float, done: bool) -> BankingObservation:
        return BankingObservation(
            fraud_state=self.fraud_state,
            collections_state=self.collections_state,
            credit_state=self.credit_state,
            cash_state=self.cash_state,
            customer_health=self.customer_health,
            reward=reward,
            done=done,
            day=self.day,
            bank_capital=self.bank_capital
        )
