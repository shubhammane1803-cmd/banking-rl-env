from fastapi import FastAPI
from banking_rl_env.server.banking_environment import BankingEnvironment
from banking_rl_env.models import BankingAction

app = FastAPI(title="IFI Banking RL Environment")

environments = {}

@app.get("/health")
@app.get("/")
def health():
    return {"status": "healthy", "message": "IFI Banking RL Environment is running"}

@app.post("/reset/{session_id}")
def reset(session_id: str):
    env = BankingEnvironment()
    environments[session_id] = env
    return env.reset().model_dump()

@app.post("/step/{session_id}")
def step(session_id: str, action: BankingAction):
    env = environments.get(session_id)
    if not env:
        return {"error": "Session not found"}
    obs = env.step(action)
    return obs.model_dump()

# REQUIRED by OpenEnv validator
def main():
    """Main entry point - DO NOT call uvicorn.run here"""
    return app
