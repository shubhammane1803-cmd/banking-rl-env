import sys
from pathlib import Path

# Add paths so modules can be found
root = Path(__file__).parent
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "banking_rl_env"))

from banking_rl_env.server.banking_environment import BankingEnvironment
from banking_rl_env.models import BankingAction

class Env:
    def __init__(self):
        self.env = BankingEnvironment()

    def reset(self):
        """Required by OpenEnv: reset the environment"""
        obs = self.env.reset()
        return obs.model_dump()

    def step(self, action: dict):
        """Required by OpenEnv: take one step"""
        action_obj = BankingAction(**action)
        obs = self.env.step(action_obj)
        return obs.model_dump()
