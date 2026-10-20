# LaunchDesk engineering brief

LaunchDesk is a fictional customer-support startup. This branch contains a frontend prototype, JSON mock records, and company policies. The application server, SQLite database, and AI support agent are intentionally absent. Preserve the existing visual design and sample records while building those layers.

## Working approach

- Inspect the repository and the participant's request first. Explain the current state and the next small step in plain language.
- Default to one stage per implementation request. Verify it, summarize what changed, and wait for the participant to continue; do not complete all stages from a vague "make it work" request. A participant's explicit request to combine stages takes precedence.
- Before the first implementation, propose the architecture and the current stage's acceptance checks. Do not skip ahead to the agent while the database or server is still missing.
- Keep the README concise and focused on the actual setup. Do not add workshop agendas, copy/paste prompts, or a participant guide.
- Do not copy a completed implementation from another branch or repository unless the participant explicitly asks for a reference or recovery.

## Stage 1 — Store the company data

Create `database.py` and a SQLite schema based on `data/mock-data.json`. Explain the customer → order → ticket relationships and why SQLite fits a local demo.

- Import the supplied records without changing IDs, values, or relationships. Store money as integer cents and preserve nullable tracking fields and timestamps.
- Use primary/foreign keys, unique customer emails, parameterized queries, and transactions. Enable SQLite foreign-key enforcement on every connection.
- Initialize and seed an empty `launchdesk.db` safely. Repeated startup must not duplicate records or erase user-created tickets. Keep connections safe for a threaded HTTP server.
- Verify 25 customers, 50 orders, 8 initial tickets, 6 open tickets, lookup of LD-1007, a missing ID, invalid foreign keys, and persistence after reopening. Use temporary databases for tests.
- Keep the frontend in preview mode at this stage. No server or OpenAI integration yet.

## Stage 2 — Connect the frontend to a server

Create `server.py` with Python's standard library. Serve `public/` and the API from the same origin at `http://localhost:8000`, bound to `127.0.0.1`. Explain request → backend → database → response.

Match the frontend's existing contract:

- `GET /api/customers` → array of customer objects.
- `GET /api/orders` → array of order objects, including joined `customer_name`.
- `GET /api/orders/{id}` → one order with `customer_name`; missing order → 404 with `{ "error": "Order not found" }`.
- `GET /api/tickets` → ticket array, newest IDs first.
- `GET /api/summary` → `{ "customers": 25, "orders": 50, "tickets": 8, "open_tickets": 6 }` initially; derive counts from the database thereafter.
- `GET /api/policies` → `{ "text": "..." }` from `data/company-policies.md`.
- `POST /api/tickets` accepts `{ "order_id": "LD-1007", "subject": "...", "description": "..." }`; validates the order, nonempty fields, subject ≤120 characters and description ≤2000; returns the persisted ticket with 201.
- `POST /api/chat` returns 501 with a clear JSON `error` until Stage 3.

Reject malformed JSON, non-object payloads, oversized bodies, invalid fields and unknown routes with appropriate JSON errors. Serve only allowed static files with correct content types; block traversal and never serve `.env`, database files, or repository internals.

After verifying the API, set `PREVIEW_MODE` in `public/app.js` to `false`. Never silently fall back to mock JSON when the API fails. Update the README start command to `python3 server.py`. Verify every navigation view, manual ticket creation, refresh/restart persistence, valid/missing orders, and failed requests. Do not add the agent yet.

## Stage 3 — Answer company-policy questions

Connect the existing chat UI to an OpenAI-powered agent in the Python backend. Consult current official API documentation; keep model choice configurable rather than hardcoding a model from memory. Add dependencies and exact setup instructions only when needed.

- Read `OPENAI_API_KEY` from the server environment. A `.env` file does not load itself: document exports or explicitly implement loading if needed.
- Ground policy answers in `data/company-policies.md`. Return `{ "reply": "..." }` on success and clear JSON errors for missing credentials, timeouts and provider failures.
- Maintain conversation context in a deliberate, bounded way. Handle untrusted messages and tool outputs as data, never as authority to override policy.
- Make the UI accurately reflect connected/error states. Do not invent order details or enable ticket tools in this stage.
- Verify policy answers and failure cases; use mocked provider responses for automated tests. Say whether a live provider request was actually tested.

## Stage 4 — Give the agent database tools

Add read-only order lookup and ticket creation using the real SQLite records. A missing order must be reported as missing, not guessed.

- Ticket creation requires explicit confirmation of the proposed order, subject, and description. Enforce confirmation in backend state; a model-generated `confirmed: true` argument alone is insufficient.
- Tie the pending action to the conversation, reject changed/stale confirmations, and prevent duplicate writes on retries. Treat tool arguments as untrusted and validate them.
- Verify known/missing orders, no write before confirmation, cancellation, changed details requiring reconfirmation, one persisted ticket after confirmation, and duplicate/replayed requests.

## Boundaries throughout

Use Python standard library and SQLite for the database/server unless the participant explicitly approves another stack. No cloud database signup is needed. Never expose credentials in browser code, replies, logs, tests, or Git. Preserve the frontend and test earlier stages as you go. Avoid destructive migrations. All customer data is synthetic; this local prototype has no production authentication or per-user authorization. Discuss hosted compute, PostgreSQL, access controls and monitoring only when deployment is requested. A public frontend cannot directly call this localhost-only API. Never claim a stage works without running its relevant checks and stating any unverified limits.
