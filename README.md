---
title: IFI Banking RL Environment - OpenEnv Hackathon Submission
emoji: 🚀
colorFrom: indigo
colorTo: blue
sdk: docker
app_port: 7860
---

**🚀 Elevating Financial Intelligence: Our OpenEnv Hackathon Journey**

- **Project Presentation:** [Presentation Deck](https://drive.google.com/file/d/1362ZvLDTv0njw2iGlsrOPmELSPwzNJjO/view?usp=sharing)
- **GitHub Repository:** [shubhammane1803-cmd/banking-rl-env](https://github.com/shubhammane1803-cmd/banking-rl-env)
- **Live Deployment:** [Hugging Face Space](https://huggingface.co/spaces/Shubhammane18/banking-rl-env)

# 🏦 IFI – Integrated Financial Intelligence: Revolutionizing Banking with RL

**Unleash the Future of Financial Decision-Making**

This is not just another environment; it's a paradigm shift in how financial institutions tackle complex challenges. Our Integrated Financial Intelligence (IFI) platform, built on cutting-edge Reinforcement Learning principles, offers a dynamic, real-time simulation for strategic banking operations. Fully compliant with OpenEnv standards, IFI empowers agents to learn, adapt, and optimize across critical domains, transforming reactive measures into proactive intelligence.

**Key Pillars of Innovation:**

-   **Fraud Detection** — Master real-time risk mitigation and threshold management to outsmart evolving threats.
-   **Collections Optimization** — Implement multi-channel recovery strategies that maximize efficiency and customer retention.
-   **Credit Management** — Drive smarter lending decisions with adaptive loan approval and limit adjustment mechanisms.
-   **Cash Optimization** — Ensure unparalleled liquidity across branches, minimizing costs and maximizing customer satisfaction.

## ⚡️ The IFI Advantage: Why We Stand Out

Our environment isn't just comprehensive; it's designed for **impact**. We combine a robust, modular architecture with a clear, actionable observation space, enabling agents to develop highly sophisticated strategies that directly translate to tangible improvements in bank capital, customer health, and operational efficiency.

## API Endpoints: Your Gateway to Intelligent Banking

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | `GET` | Verify the operational status of the IFI environment. |
| `/reset/{session_id}` | `POST` | Initialize a new session or reset an existing one. |
| `/step/{session_id}` | `POST` | Execute a strategic banking action and observe consequences. |

## Quick Start: Engage with IFI Now!

Experience the power of IFI with these simple `curl` commands using our live endpoint:

```bash
# Health check
curl https://shubhammane18-banking-rl-env.hf.space/health

# Reset a session
curl -X POST https://shubhammane18-banking-rl-env.hf.space/reset/my_session

# Execute a strategic step
curl -X POST https://shubhammane18-banking-rl-env.hf.space/step/my_session \
  -H 'Content-Type: application/json' \
  -d '{"domain":"fraud","action_type":"UPDATE_RISK_THRESHOLD","parameters":{"threshold":0.7}}'
```

---

**Built with passion for the OpenEnv Hackathon by Team [Your Team Name Here].**
