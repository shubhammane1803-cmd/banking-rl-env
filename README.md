---
title: IFI Banking RL Environment
emoji: 🏦
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# 🏦 IFI – Integrated Financial Intelligence

An OpenEnv-compliant Banking Reinforcement Learning Environment covering:
- **Fraud Detection** — real-time risk threshold management
- **Collections** — multi-channel recovery strategies
- **Credit Management** — loan approval/rejection decisions
- **Cash Optimization** — branch liquidity management

## API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/reset/{session_id}` | POST | Reset environment |
| `/step/{session_id}` | POST | Execute action |

## Quick Start

```bash
# Health check
curl https://shubhammane18-banking-rl-env.hf.space/health

# Reset
curl -X POST https://shubhammane18-banking-rl-env.hf.space/reset/my_session

# Step
curl -X POST https://shubhammane18-banking-rl-env.hf.space/step/my_session \
  -H 'Content-Type: application/json' \
  -d '{"domain":"fraud","action_type":"UPDATE_RISK_THRESHOLD","parameters":{"threshold":0.7}}'
```
