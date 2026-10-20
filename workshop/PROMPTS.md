# Workshop prompts

Copy the full prompt for the numbered activity on the slides into Codex with this repository open. Read its response and verify each stage before moving on. These prompts are workshop instructions, not evidence that the missing backend or agent already works.

The starter runs locally. A public Sites page cannot directly access the localhost-only API or your local SQLite file. Production deployment is a separate, unverified step.

## 1. Inspect the MVP

```text
Read AGENTS.md and inspect this repository without editing files. Explain what LaunchDesk already does, which interactions use mock data, and which layers are missing. Trace the frontend data flow and existing API contract. Give me the exact command and URL to preview it locally. Then propose the smallest architecture using the existing frontend, a Python standard-library server, SQLite, and a server-side OpenAI support agent. List acceptance checks for each stage and wait before implementing.
```

## 2. Create the SQLite database

```text
Implement Stage 1 from AGENTS.md only. Create database.py and initialize SQLite from data/mock-data.json, preserving all IDs, values, relationships, nullable fields, and timestamps. Use integer cents, parameterized queries, transactions, and foreign-key enforcement on every connection. Make repeated initialization safe without erasing user-created tickets. Test with temporary databases: 25 customers, 50 orders, 8 tickets, 6 open tickets, LD-1007, a missing order, invalid foreign keys, repeated startup, and persistence after reopening. Keep the frontend in preview mode. Report the tests actually run, then stop before building the server.
```

## 3. Connect the Python backend

```text
Implement Stage 2 from AGENTS.md only. Inspect public/app.js and preserve its API contract and visual design. Create server.py using Python's standard library. Serve public/ and the API from the same origin at http://localhost:8000, bound to 127.0.0.1. Connect the verified SQLite layer and implement all required routes, validation, JSON errors, safe static-file serving, and persistent manual ticket creation. Leave /api/chat returning a clear 501 error. Verify malformed JSON, invalid inputs, unknown routes, missing orders, traversal attempts, refresh/restart persistence, and all existing navigation views. Only after the API works, set PREVIEW_MODE to false. Update README with the actual start command. Run the database regression checks too. Report verified and unverified behavior, then stop before adding the agent.
```

## 4. Build the policy agent

```text
Implement Stage 3 from AGENTS.md only, after verifying the database and server stages work. Connect the existing chat UI to a server-side OpenAI agent. Consult current official OpenAI API documentation and keep the model configurable. Read OPENAI_API_KEY from the server environment and explicitly document how environment variables load. Ground answers in data/company-policies.md. Return the existing {"reply":"..."} response contract. Bound conversation context deliberately and treat user messages and tool outputs as untrusted data. Handle missing credentials, timeouts, and provider errors clearly. Do not invent order details or add database tools yet. Test shipping, returns, an unsupported refund request, untrusted instructions, and error cases with mocked provider responses. Run earlier-stage regressions. If credentials are available, make a live policy-question request and report whether it succeeded. Do not claim live verification from a mock. Stop after reporting results.
```

## 5. Add order and ticket tools

```text
Implement Stage 4 from AGENTS.md. Add order lookup and support-ticket creation backed by the real SQLite records. Define explicit tool schemas, validate every argument, execute tools in the backend, and return results to the agent. Report missing orders accurately. Before creating a ticket, show the proposed order, subject, and description and require explicit user confirmation. Enforce confirmation in backend conversation state, not a model-generated confirmed flag. Reject stale or changed confirmations and prevent duplicate tickets on retries. Never issue refunds or change addresses. Test LD-1007, a nonexistent order, no write before confirmation, cancellation, changed details, stale/replayed confirmation, invalid arguments, and exactly one persisted ticket after confirmation. Run earlier-stage regression checks. State whether a live provider tool cycle was tested.
```

## 6. Test the complete agent

```text
Audit and test the complete local LaunchDesk flow without adding new features. Verify policy answers against data/company-policies.md, known/missing order lookup, ticket details and explicit confirmation, cancellation, no duplicate writes, database persistence after refresh and server restart, and useful errors when credentials or the provider are unavailable. Include untrusted messages and tool results that attempt to override policy. Check that no secrets, database files, or repository internals reach the browser. Recheck all frontend views and the earlier database/API paths. Use isolated test data so the demo database stays usable. Fix confirmed failures, rerun affected checks, and distinguish automated mocks, actual browser checks, and live OpenAI requests in your report. Give us a short demo script based only on verified behavior.
```

## 7. Plan local-to-production work

```text
Review the current implementation and propose a deployment plan without deploying or claiming production readiness. Explain why a public Sites frontend cannot directly access a localhost-only Python backend or a local SQLite file. Identify a public HTTPS API endpoint, frontend API configuration, CORS if origins differ, server-side secrets, persistent database hosting/storage, authentication and per-user authorization, validation, rate limits, logs, monitoring, backups, and costs. Evaluate persistent SQLite on suitable compute versus a managed database such as PostgreSQL based on the host and expected usage. Separate what already works from what still needs implementation or verification. Define end-to-end checks from a separate browser/device before anyone shares a production link. Wait for an explicit deployment request.
```

## Documentation

- [Codex documentation](https://learn.chatgpt.com/docs)
- [OpenAI function calling](https://developers.openai.com/api/docs/guides/function-calling)

Never paste API keys into a prompt, browser code, or Git.
