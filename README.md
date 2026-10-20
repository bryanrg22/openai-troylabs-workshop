<p align="center">
  <img src="assets/workshop-header.svg" width="960" alt="Shipping Your First Agent — OpenAI Student Collective × TroyLabs at USC. October 20, 2026.">
  <img src="assets/workshop-brands.svg" width="960" alt="OpenAI Student Collective × TroyLabs × University of Southern California">
</p>

<h1 align="center">LaunchDesk</h1>

<p align="center">A fictional customer-support startup. A working MVP. Your starting point.</p>

<p align="center">
  <a href="#quick-start">Quick start</a> ·
  <a href="#mock-data">Mock data</a> ·
  <a href="#how-it-connects">How it connects</a> ·
  <a href="#test-your-work">Test your work</a>
</p>

## Quick start

Requires **Git and Python 3.10+**. No extra packages, database signup, or API key needed to run the starter.

```bash
git clone https://github.com/bryanrg22/openai-troylabs-workshop.git
cd openai-troylabs-workshop
python3 server.py
```

Open **[http://localhost:8000](http://localhost:8000)**. Stop the server with **Ctrl+C**. On Windows, use `py -3` if `python3` is unavailable.

## Mock data

The dashboard comes with **25 customers, 50 orders, and 8 support tickets**, plus order lookup and manual ticket creation. All data is fictional.

- [Company policies](data/company-policies.md)
- [Database schema](data/schema.sql)
- Example order: **LD-1007**

SQLite creates and seeds `launchdesk.db` automatically. Changes persist between restarts. To reset the demo, stop the server and delete that file; the next start restores the sample data. Keep database files out of Git.

**AI chat is a placeholder:** `/api/chat` returns **501 Not Implemented** until an agent is connected.

## How it connects

```text
Browser · dashboard + chat UI
                |
       Python HTTP API
                |
    SQLite · launchdesk.db
    ├── customers
    ├── orders
    └── tickets

Company knowledge · data/company-policies.md
```

[Frontend](public/) → [Python server](server.py) → [SQLite](database.py). Everything runs locally. A future support agent can connect through the backend, using company policies and database records. Keep API keys server-side.

## Test your work

```bash
python3 -m unittest discover -s tests -v
```

The tests cover seeded data, valid and missing order lookups, ticket persistence, and unique customer emails.

Demo only: the starter has no authentication and is not ready for real customer data.

---

<p align="center">
  <a href="https://openai.com/student-collective/">OpenAI Student Collective</a> ×
  <a href="https://usctroylabs.com/">TroyLabs</a> ·
  <a href="https://www.usc.edu/">USC</a> ·
  <a href="assets/README.md">Brand asset sources</a><br>
  <sub>Student-led materials. Marks identify the collaboration and campus context, without implying additional institutional endorsement.</sub>
</p>
