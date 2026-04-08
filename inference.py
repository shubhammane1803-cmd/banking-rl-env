import sys
from pathlib import Path

# Make sure Python can find your modules
root = Path(__file__).parent
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "banking_rl_env"))

from banking_rl_env.server.banking_environment import BankingEnvironment
from banking_rl_env.models import BankingAction

class Env:
    """This is the required bridge for OpenEnv hackathon"""
    def __init__(self):
        self.env = BankingEnvironment()

    def reset(self):
        """Reset the environment - required by OpenEnv"""
        observation = self.env.reset()
        return observation.model_dump()

    def step(self, action: dict):
        """Take one step in the environment - required by OpenEnv"""
        action_obj = BankingAction(**action)
        observation = self.env.step(action_obj)
        return observation.model_dump()
