<p align="center">
  <img src="assets/workshop-header.svg" width="960" alt="Shipping Your First Agent — OpenAI Student Collective × TroyLabs at USC. October 20, 2026.">
  <img src="assets/workshop-brands.svg" width="960" alt="OpenAI Student Collective × TroyLabs × University of Southern California">
</p>

<h1 align="center">LaunchDesk</h1>

<p align="center">A fictional customer-support startup. A frontend prototype and mock data. Your starting point.</p>

<p align="center">
  <a href="#quick-start">Quick start</a> ·
  <a href="#mock-data">Mock data</a> ·
  <a href="#how-it-connects">How it connects</a>
</p>

Full numbered copy-paste prompts: [workshop/PROMPTS.md](workshop/PROMPTS.md).

## Quick start

Requires **Git and Python 3.10+**. No extra packages, database signup, or API key needed to preview the frontend.

```bash
git clone https://github.com/bryanrg22/openai-troylabs-workshop.git
cd openai-troylabs-workshop
python3 -m http.server 8000 --bind 127.0.0.1
```

Open **[http://localhost:8000/public/](http://localhost:8000/public/)**. Stop the server with **Ctrl+C**. On Windows, use `py -3` if `python3` is unavailable.

## Mock data

The read-only preview includes **25 customers, 50 orders, and 8 support tickets**. All data is fictional. Ticket creation and chat become functional after a backend is connected.

- [Company policies](data/company-policies.md)
- [Mock records](data/mock-data.json)
- Example order: **LD-1007**

**The application server, SQLite database, and AI agent are not implemented on this branch.** The preview reads JSON files; it does not save changes.

## How it connects

```text
Included now
Browser · frontend prototype
                |
       Mock records · JSON

To build
Browser → Python API → SQLite
                |
          Support agent → OpenAI
```

[Frontend](public/) + [mock data](data/mock-data.json) + [company policies](data/company-policies.md). The preview runs locally with Python's static file server. Build the application backend and database to add persistence, then connect the agent. Keep API keys server-side.

Demo only: the starter has no authentication and is not ready for real customer data.

---

<p align="center">
  <a href="https://openai.com/student-collective/">OpenAI Student Collective</a> ×
  <a href="https://usctroylabs.com/">TroyLabs</a> ·
  <a href="https://www.usc.edu/">USC</a> ·
  <a href="assets/README.md">Brand asset sources</a><br>
  <sub>Student-led materials. Marks identify the collaboration and campus context, without implying additional institutional endorsement.</sub>
</p>
