<p align="center">
  <img src="assets/workshop-header.svg" width="960" alt="Shipping Your First Agent — OpenAI Student Collective × TroyLabs at USC. October 20, 2026. A hands-on LaunchDesk workshop.">
  <img src="assets/workshop-brands.svg" width="960" alt="OpenAI Student Collective × TroyLabs × University of Southern California">
</p>

<h1 align="center">LaunchDesk · Shipping Your First Agent</h1>

<p align="center">
  Take a working startup MVP and build a customer support agent with Codex.<br>
  <strong>October 20, 2026 · USC · 90 minutes · Python + SQLite</strong>
</p>

<p align="center">
  <a href="#quick-start">Quick start</a> ·
  <a href="workshop/README.md">Workshop guide</a> ·
  <a href="#build-with-codex">Codex prompts</a> ·
  <a href="#test-your-work">Test your work</a>
</p>

---

## Welcome to the team

You’re joining the tech team at **LaunchDesk**, a fictional customer-support startup. The founder has an MVP: a dashboard, customers, orders, and a ticket inbox. Your brief is to add an AI support agent that can answer policy questions, look up real records in the demo database, and create a ticket after the customer confirms.

You’ll use **Codex to inspect, plan, implement, and test**. You don’t need to write the code by hand; bring questions and be ready to review what you build. Every customer, order, and ticket is synthetic.

**By the end, you’ll know how to:**

- Explain how a frontend, Python API, AI agent, and relational database connect.
- Ground agent answers in company policies and database records.
- Give an agent useful tools, with explicit confirmation before creating a ticket.
- Test both successful requests and failure cases, and explain what a real deployment still needs.

## Quick start

**You’ll need:** Git and **Python 3.10+**. To join the building exercises, have Codex ready to open this folder. The starter itself needs no extra Python packages, cloud database account, or API key.

```bash
git clone https://github.com/bryanrg22/openai-troylabs-workshop.git
cd openai-troylabs-workshop
python3 server.py
```

Open **[http://localhost:8000](http://localhost:8000)**. Leave the terminal running while you explore. Stop the server with **Ctrl+C**.

The local `launchdesk.db` file is created and seeded automatically on the first run. Your changes persist between restarts.

> [!TIP]
> Explore the dashboard before building. Try order **LD-1007**, browse the ticket inbox, and read the company policies. You already have a working app to build on.

<details>
<summary><strong>Setup help and resetting the demo</strong></summary>

- **Windows:** If `python3` is unavailable, use `py -3 server.py` with Python 3.10 or newer. Use `py -3` in place of `python3` in the test command, too.
- **Python version:** Run `python3 --version` (or `py -3 --version`) to check.
- **Port already in use:** Stop any earlier LaunchDesk server before starting another on port 8000.
- **Fresh demo:** Stop the server, then delete `launchdesk.db` from this folder. This removes your local demo changes; the original sample data returns at the next start. Never commit database files.

</details>

## What you inherit

The MVP includes a support dashboard, **25 fictional customers**, **50 fictional orders**, **8 seeded tickets**, manual ticket creation, a persistent SQLite database, and a chat interface. Its [company handbook](data/company-policies.md) supplies the support policies.

> [!IMPORTANT]
> **The AI agent is the workshop exercise.** The starter’s `/api/chat` endpoint intentionally returns **501 Not Implemented**. OpenAI API access and server-side credentials are needed when you connect the live agent; they are not required to explore the starter. Any packages added during that exercise must be installed then.

## Build with Codex

Open this repository folder in Codex. Start with the [project instructions](AGENTS.md), then follow the **[90-minute workshop guide](workshop/README.md)** for the full sequence.

### 1. Understand the system

Copy this prompt into Codex before changing code:

```text
Read AGENTS.md and workshop/README.md, then inspect this existing LaunchDesk
MVP. Explain the frontend, Python backend, and SQLite database. Propose the
simplest architecture for a customer support AI agent. Do not edit code yet.
```

Discuss where each part runs, what data the agent needs, and which actions should require confirmation.

### 2. Connect the support agent

```text
Implement the customer support agent using the OpenAI API in the Python
backend. Keep the API key server-side in an environment variable. Ground
policy answers in data/company-policies.md and connect the existing chat UI.
Preserve the dashboard, order lookup, and manual ticket creation. Add clear
setup instructions, friendly errors, and tests. Never commit credentials.
```

### 3. Add tools and verify behavior

```text
Add agent tools to look up an order by ID and create a support ticket only
after the user explicitly confirms. Use the existing SQLite database and
API. Never invent order details or policy. Test valid and missing orders,
unconfirmed and confirmed tickets, and API failures. Run the existing tests
and verify the original dashboard and manual ticket flow still work.
```

For the demo, ask about **LD-1007**, then request a support ticket. Check that the agent asks for confirmation, creates only the intended ticket, and reports the result accurately.

## How it connects

```text
Your browser · LaunchDesk dashboard + chat
                    |
          Local Python HTTP API
          |                   |
     SQLite database     Support agent ← build this
     customers           |          |
     orders              |     OpenAI API
     tickets             |     (server-side key)
                         |
              Company policies + database tools
```

The **frontend, Python backend, and SQLite database run locally** for this workshop. The live agent adds calls from the backend to the OpenAI API. Read [server.py](server.py), [database.py](database.py), and the [schema](data/schema.sql) to trace the existing path.

For a deployed service, discuss a hosted backend and a managed relational database such as PostgreSQL. A frontend published through ChatGPT Sites needs a reachable backend API; a public page cannot directly reach this local-only server. The workshop starter remains a local app.

## Test your work

Run the existing regression suite from the repository folder:

```bash
python3 -m unittest discover -s tests -v
```

As you build the agent, use these demo checks alongside its new tests:

- **Known order:** LD-1007 returns the details stored in SQLite.
- **Missing order:** An unknown ID gets a clear “not found” response.
- **Policy question:** The answer follows the company handbook.
- **Ticket request:** No agent-created ticket until explicit confirmation; the confirmed ticket appears in the inbox.
- **Failure path:** Missing credentials or an API failure produces a helpful error.
- **Existing MVP:** Customers, orders, and manual ticket creation still work.

## From workshop to production

This is a learning starter with fake data, localhost binding, and no authentication. Before using real customer data, you would need authentication, authorization, per-user isolation, request and spending limits, secure secrets, monitoring, hosted compute, and persistent storage.

**Keep OpenAI API keys on the server. Never put them in frontend JavaScript, chat messages, logs, or GitHub.**

---

<p align="center">
  Built for the <strong>OpenAI Student Collective × TroyLabs</strong> workshop at USC.<br>
  <a href="https://openai.com/student-collective/">Student Collective</a> ·
  <a href="https://usctroylabs.com/">TroyLabs</a> ·
  <a href="https://www.usc.edu/">USC</a> ·
  <a href="assets/README.md">Brand asset sources</a>
</p>

<p align="center"><sub>Student-led workshop materials. Marks identify the workshop collaboration and campus context; they do not imply additional institutional endorsement.</sub></p>
