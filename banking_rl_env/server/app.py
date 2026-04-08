import sys
from pathlib import Path

root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from server.banking_environment import BankingEnvironment
from models import BankingAction

# Create the FastAPI app
app = FastAPI(
    title="IFI Banking RL Environment",
    description="Integrated Financial Intelligence - Banking RL Environment for OpenEnv"
)

environments = {}

@app.get("/")
@app.get("/health")
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

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    env = BankingEnvironment()
    environments[session_id] = env
    try:
        while True:
            data = await websocket.receive_json()
            action = BankingAction(**data)
            obs = env.step(action)
            await websocket.send_json(obs.model_dump())
    except WebSocketDisconnect:
        if session_id in environments:
            del environments[session_id]

# ←←← ADD THIS FUNCTION AT THE VERY BOTTOM ←←←
def main():
    """Main entry point required by OpenEnv hackathon validator"""
    return app
