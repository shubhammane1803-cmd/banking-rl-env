# main.py — ROOT LEVEL entry point (required by OpenEnv validator)
# OpenEnv expects: "main:app" as the server entry point
import sys
sys.path.insert(0, '/app')
sys.path.insert(0, '/content')

from banking_rl_env.server.app import app  # re-export app at root level

# This allows uvicorn to be started as: uvicorn main:app
