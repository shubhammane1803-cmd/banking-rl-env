# banking_rl_env/server/app.py
import sys
import uvicorn
from typing import Dict
from fastapi import FastAPI, HTTPException

sys.path.insert(0, '/content')

from banking_rl_env.server.banking_environment import BankingEnvironment
from banking_rl_env.models import BankingAction

app = FastAPI(
    title="IFI Banking RL Environment",
    description="Integrated Financial Intelligence — OpenEnv compliant Banking RL Environment",
    version="1.0.0"
)

# Session store: session_id -> BankingEnvironment instance
environments: Dict[str, BankingEnvironment] = {}


@app.get("/")
@app.get("/health")
def health():
    return {"status": "healthy", "service": "IFI Banking RL Environment"}


@app.post("/reset/{session_id}")
def reset(session_id: str):
    """Initialize or reset a banking environment session."""
    env = BankingEnvironment()
    environments[session_id] = env
    obs = env.reset()
    return obs.model_dump()


@app.post("/step/{session_id}")
def step(session_id: str, action: BankingAction):
    """Execute one step in the environment."""
    env = environments.get(session_id)
    if not env:
        raise HTTPException(
            status_code=404,
            detail=f"Session '{session_id}' not found. Call /reset first."
        )
    obs = env.step(action)
    return obs.model_dump()


def main():
    uvicorn.run("banking_rl_env.server.app:app", host="0.0.0.0", port=7860, reload=False)


if __name__ == "__main__":
    main()
