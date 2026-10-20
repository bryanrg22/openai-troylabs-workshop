# Workshop prompts

Open this repository in your coding agent. Use these prompts in order, one at a time. The implementation details and verification checks are in [AGENTS.md](../AGENTS.md).

## 1. Frontend

```text
Deploy my LaunchDesk frontend using ChatGPT Sites. Keep the existing design.
```

## 2. Backend + SQL database

```text
Build my backend using ChatGPT Sites and its D1 SQL database. Connect orders, customers, and support tickets so everything saves after refresh.
```

## 3. Invoice storage

```text
Store the included invoice PDFs in Sites' R2 object storage. Keep their metadata in D1 and let users download the correct invoice for each order.
```

## 4. AI Assistant

```text
Create an AI Assistant page where I can chat using my ChatGPT account without an API key. Use Agentic SQL to look up orders and retrieve invoices, answer company-policy questions, and save separate chats so I can continue them after refreshing.
```

The starter is intentionally incomplete. These prompts describe what to build; they do not mean the backend, storage, or AI already works. Follow AGENTS.md for this Sites workflow; the README also includes a local frontend preview.
