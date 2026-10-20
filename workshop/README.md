# 90-minute workshop

## 8:00–8:15 — Act like the TroyLabs tech team
The fictional founder gives you LaunchDesk, an MVP, and asks for an AI customer support agent. Sketch the frontend, backend/API, agent execution, and relational database. Discuss why SQLite is fine locally and where production might use PostgreSQL.

## 8:15–8:25 — Onboard with Codex
Open this project in Codex. Ask it to inspect AGENTS.md and the repo before changing files. Run `python3 server.py` and open http://localhost:8000.

## 8:25–8:50 — Build agent
Have Codex connect an OpenAI agent to the existing support interface. Supply API credentials only through environment variables, never the website.

## 8:50–9:10 — Give agent tools
Use Codex to add safe order-lookup and ticket-creation function tools. Ticket creation must require customer confirmation. Test an existing order and a nonexistent order.

## 9:10–9:25 — Test and ship
Use Codex to add tests and error handling. Show the difference between a local working prototype and a deployed service. Do not assume a public Sites page can reach localhost.

## 9:25–9:30 — Showcase
Demo an order inquiry and ticket, then discuss what production still requires: authentication, authorization, monitoring, request limits, hosted compute, and persistent storage.

## Copy/paste prompt 1
Read AGENTS.md and inspect this existing LaunchDesk MVP. Explain what the frontend, Python backend, and SQLite database do, then propose the simplest architecture to add a customer support AI agent. Do not edit code yet.

## Copy/paste prompt 2
Implement the customer support agent using the OpenAI API in the Python backend. Keep the API key server-side. Ground policy responses in data/company-policies.md and make the existing chat UI functional. Add friendly error handling and tests.

## Copy/paste prompt 3
Create agent tools to look up a fictional order by order ID and to create a support ticket only after the user explicitly confirms. Use the existing SQLite database and API. Test valid and invalid orders.
