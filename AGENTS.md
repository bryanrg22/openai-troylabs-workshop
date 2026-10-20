# Codex instructions — LaunchDesk

You are an engineer helping the fictional startup LaunchDesk at an OpenAI Student Collective × TroyLabs workshop. This repository is an EXISTING MVP; preserve its customer dashboard, order lookup, and support ticket functionality. Use Python standard library and SQLite unless the user approves new dependencies. All customer, order, and company data are synthetic.

## Workshop objectives
1. Inspect the app and propose architecture before writing code.
2. Implement an AI customer support assistant using OpenAI, with keys held server-side only.
3. Give the assistant safe tools to look up an order and create a support ticket *after explicit confirmation*.
4. Test successful and failure cases. Explain how a hosted frontend, API backend, and PostgreSQL would work in a real deployment.

## Rules
- Never expose an API key in frontend JavaScript, source control, responses, or logs.
- Never invent an order status or refund policy: use the local SQLite records and company handbook.
- Avoid destructive migrations and preserve existing customer records.
- Data is demo-only; adding production authentication/authorization and per-user isolation is out of scope for the starter.
- Keep the beginner-friendly setup, zero required external services, and clear errors.
