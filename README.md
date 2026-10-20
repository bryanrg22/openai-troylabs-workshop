<p align="center">
  <img src="assets/workshop-header.svg" width="960" alt="Shipping Your First Agent — OpenAI Student Collective × TroyLabs at USC. October 20, 2026.">
  <img src="assets/workshop-brands.svg" width="960" alt="OpenAI Student Collective × TroyLabs × University of Southern California">
</p>

<h1 align="center">LaunchDesk</h1>

<p align="center">Help a startup turn its MVP into a working customer-support app.</p>

LaunchDesk is a fictional startup that helps teams handle order questions, deliveries, returns, and support tickets. It has an MVP dashboard. Your job is to use Codex to bring it to life.

This repository includes:

- The existing LaunchDesk website design.
- Customer, order, and support-ticket records for the fictional company.
- A company handbook with shipping, return, and support policies.
- Five invoice PDFs linked to the included orders.
- Instructions that guide Codex through building the app.

## Quick start

**Download the project — no terminal needed:**

1. Click the green **Code** button near the top of this GitHub page.
2. Choose **Download ZIP**.
3. Extract the ZIP file.
4. Open **Codex** and open the extracted project folder—the one containing this README.
5. Start with the first prompt below.

**Already use Git and the Codex CLI?** Open your terminal and run:

```bash
git clone https://github.com/bryanrg22/openai-troylabs-workshop.git
cd openai-troylabs-workshop
codex
```

## Prompts for Codex

Copy one prompt at a time into Codex. Let it handle the technical setup, implementation, and checks. Follow any sign-in or permission steps it needs, then review the result before moving to the next prompt.

### 1. Frontend

```text
Deploy my LaunchDesk frontend using ChatGPT Sites. Keep the existing design.
```

### 2. Backend + SQL database

```text
Build my backend using ChatGPT Sites and its D1 SQL database. Connect orders, customers, and support tickets so everything saves after refresh.
```

### 3. Invoice storage

```text
Store the included invoice PDFs in Sites' R2 object storage. Keep their metadata in D1 and let users download the correct invoice for each order.
```

### 4. AI Assistant

```text
Create an AI Assistant page where I can chat using my ChatGPT account without an API key. Use Agentic SQL to look up orders and retrieve invoices, answer company-policy questions, and save separate chats so I can continue them after refreshing.
```

---

<p align="center">
  <a href="https://openai.com/student-collective/">OpenAI Student Collective</a> ×
  <a href="https://usctroylabs.com/">TroyLabs</a> ·
  <a href="https://www.usc.edu/">USC</a> ·
  <a href="assets/README.md">Brand asset sources</a><br>
  <sub>Student-led materials. Marks identify the collaboration and campus context, without implying additional institutional endorsement.</sub>
</p>
