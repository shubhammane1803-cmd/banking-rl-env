# inference.py  — ROOT LEVEL (mandatory for OpenEnv submission)
"""
IFI – Integrated Financial Intelligence
OpenEnv Hackathon submission inference script.

Submission requirements:
  - inference.py must be in the project root
  - use os.getenv() with defaults for API_BASE_URL and MODEL_NAME
  - read HF_TOKEN and raise an error if missing
  - use the OpenAI Python client
  - output [START], [STEP], [END] format exactly
  - [END] must always print, even on exceptions
  - rewards to 2 decimal places
  - booleans as lowercase true/false
"""

import os
import sys
import json
import traceback

# ── Path setup ──────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Environment variable configuration ──────────────────────────────────────
API_BASE_URL = os.getenv("API_BASE_URL", "https://api-inference.huggingface.co/v1")
MODEL_NAME   = os.getenv("MODEL_NAME", "meta-llama/Llama-3.1-8B-Instruct")
HF_TOKEN     = os.getenv("HF_TOKEN")  # REQUIRED — will raise if missing

if not HF_TOKEN:
    raise ValueError(
        "HF_TOKEN environment variable is not set. "
        "Please set it before running inference.py."
    )

# ── Imports (after path setup) ───────────────────────────────────────────────
from openai import OpenAI
from banking_rl_env.server.banking_environment import BankingEnvironment
from banking_rl_env.models import BankingAction

# ── OpenAI client pointing at HuggingFace Inference API ─────────────────────
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN,
)

# ── Env bridge (keeps backward-compatible Env class) ────────────────────────
class Env:
    """OpenEnv mandatory bridge class."""

    def __init__(self):
        self.env = BankingEnvironment()

    def reset(self) -> dict:
        obs = self.env.reset()
        return obs.model_dump()

    def step(self, action_dict: dict) -> dict:
        action = BankingAction(**action_dict)
        obs = self.env.step(action)
        return obs.model_dump()


# ── Helper: format output strictly ──────────────────────────────────────────
def _fmt_reward(r) -> str:
    return f"{float(r):.2f}"


def _fmt_bool(b) -> str:
    return "true" if b else "false"


def _obs_to_str(obs: dict) -> str:
    """
    Format observation for [STEP] output.
    Booleans are lowercase, rewards are 2 decimal places.
    """
    return json.dumps({
        **obs,
        "reward": float(f"{obs.get('reward', 0.0):.2f}"),
        "done": obs.get("done", False),
    }, default=str).replace("true", "true").replace("false", "false").replace("True", "true").replace("False", "false")


# ── LLM action selection ─────────────────────────────────────────────────────
SYSTEM_PROMPT = """
You are an expert banking AI agent. Given the current environment state,
choose exactly ONE action as JSON with keys: domain, action_type, parameters.

Valid domains and actions:
- fraud: UPDATE_RISK_THRESHOLD (threshold: 0.0-1.0), BLOCK_TRANSACTION, ALLOW_TRANSACTION, FLAG_FOR_REVIEW
- collections: CALL_CUSTOMER, SEND_SMS, OFFER_SETTLEMENT, WRITE_OFF
- credit: APPROVE_LOAN (amount: int), REJECT_LOAN, ADJUST_CREDIT_LIMIT
- cash: DISPATCH_REFILL (branch: str, amount: int), HOLD_REFILL, TRANSFER_CASH

Respond ONLY with valid JSON, no explanation.
Example: {"domain": "fraud", "action_type": "UPDATE_RISK_THRESHOLD", "parameters": {"threshold": 0.7}}
""".strip()


def get_llm_action(obs: dict) -> dict:
    """Ask the LLM to pick the next action given the observation."""
    user_msg = f"Current state:\n{json.dumps(obs, indent=2, default=str)}\n\nPick the best action."

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
            max_tokens=200,
            temperature=0.1,
        )
        text = response.choices[0].message.content.strip()
        # Strip markdown code fences if present
        if text.startswith("```"):
            text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
        return json.loads(text)
    except Exception:
        # Fallback: safe default action
        return {
            "domain": "fraud",
            "action_type": "UPDATE_RISK_THRESHOLD",
            "parameters": {"threshold": 0.7}
        }


# ── Main inference loop ───────────────────────────────────────────────────────
def run(max_steps: int = 5):
    """
    Run the LLM-powered agent in the Banking RL environment.
    Output format (required by hackathon):
      [START]
      [STEP] step=N action=... reward=X.XX done=true/false
      [END]
    """
    total_reward = 0.0

    print("[START]")
    sys.stdout.flush()

    try:
        env = Env()
        obs = env.reset()

        for step_num in range(1, max_steps + 1):
            # Get LLM action
            action_dict = get_llm_action(obs)

            # Execute action
            obs = env.step(action_dict)

            reward = float(obs.get("reward", 0.0))
            done = bool(obs.get("done", False))
            total_reward += reward

            # [STEP] output — exact format required
            print(
                f"[STEP] step={step_num} "
                f"action={json.dumps(action_dict)} "
                f"reward={_fmt_reward(reward)} "
                f"done={_fmt_bool(done)} "
                f"day={obs.get('day', 0)} "
                f"capital={obs.get('bank_capital', 0.0):.2f}"
            )
            sys.stdout.flush()

            if done:
                break

    except Exception as e:
        print(f"[STEP] error={str(e)}")
        traceback.print_exc()

    finally:
        # [END] MUST always print — even on exceptions
        print(f"[END] total_reward={_fmt_reward(total_reward)}")
        sys.stdout.flush()


if __name__ == "__main__":
    run()
