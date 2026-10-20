# LaunchDesk · Shipping Your First Agent

**OpenAI Student Collective × TroyLabs** · Hands-on workshop · October 20, 2026

LaunchDesk is a **fictional customer-support startup**. You inherit a working MVP and use **Codex** to plan, build, and test an OpenAI-powered support agent. No hand-written code is required, no database signup is needed, and all customers, orders, and tickets are synthetic.

## What works already

- Polished support operations dashboard
- Customer directory (**25 fictional customers**)
- Order management (**50 fictional orders**)
- Ticket inbox (**8 seeded tickets**) and manual ticket creation
- Persistent local **SQLite** database
- Company policy handbook and an AI chat UI

The AI chat endpoint intentionally returns **501 Not Implemented**. That is your exercise: let Codex implement the agent, safe order-lookup tools, and ticket creation requiring confirmation.

## Start in 30 seconds

**Requirement:** Python 3.10+.

```bash
git clone https://github.com/bryanrg22/openai-troylabs-workshop.git
cd openai-troylabs-workshop
python3 server.py
```

Open **http://localhost:8000** in a browser. The database seeds itself the first time you start the server. You do **not** need to install packages, create an account, or configure an API key to explore the MVP.

To start clean, stop the server and remove the local `launchdesk.db` file; it will be recreated on next run. Never commit the `.db` file.

## Workshop instructions

1. Open the folder in **Codex**.
2. Tell Codex: **"Read AGENTS.md and workshop/README.md, inspect the repo, and propose the architecture. Do not edit yet."**
3. Discuss where the website, backend, AI agent, and relational database live.
4. Follow the prompts in **[workshop/README.md](workshop/README.md)** and let Codex implement, test, and iterate.
5. Try order **LD-1007**, then ask for a support ticket.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## Architecture

```text
Browser / LaunchDesk Dashboard
              |
       Python HTTP API  <-- Codex integrates OpenAI agent here
              |
    SQLite (launchdesk.db)
    ├── customers
    ├── orders
    └── tickets

data/company-policies.md (company knowledge)
```

For the workshop, the backend and SQLite run **locally** to avoid signing up for cloud services. In a real deployment, a hosted backend and managed relational database such as PostgreSQL may be appropriate. A ChatGPT Sites-hosted frontend **cannot directly call a local-only backend** without a public API endpoint or other supported deployment setup.

## Security note

The starter uses **fake data only**, localhost binding, and no authentication. It is **not production-ready**: authentication, authorization, isolation, usage limits, secure secrets, monitoring, and deployment need separate review. Never insert OpenAI API keys into frontend JavaScript or GitHub.

Built for the **OpenAI Student Collective × TroyLabs — Shipping Your First Agent** workshop.
