import sys
import os
from typing import Dict, Any

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), "banking_rl_env"))

from banking_rl_env.server.banking_environment import BankingEnvironment
from banking_rl_env.models import BankingAction

class Env:
    """OpenEnv Required Bridge Class"""
    def __init__(self):
        self.env = BankingEnvironment()

    def reset(self) -> Dict[str, Any]:
        obs = self.env.reset()
        return obs.model_dump()

    def step(self, action_dict: Dict[str, Any]) -> Dict[str, Any]:
        action = BankingAction(**action_dict)
        obs = self.env.step(action)
        return obs.model_dump()
