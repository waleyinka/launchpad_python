# MindFuel — Automated Quote Email Delivery Platform

A **production-ready system** that fetches motivational quotes from the [ZenQuotes API](https://zenquotes.io/) and sends them as personalized daily or weekly emails to subscribed users.  

The project was designed for **MindFuel**, a mental wellness startup, and demonstrates the ability to design, build, and orchestrate a modular backend pipeline in Python — integrating APIs, databases, email delivery, and logging systems.

---

## 🧩 Table of Contents

1. [Overview](#overview)
3. [Features](#features)
4. [Tech Stack](#tech-stack)
5. [Setup & Installation](#setup--installation)
6. [Project Structure](#project-structure)
7. [Configuration (.env)](#configuration-env)
8. [Database Schema](#database-schema)
9. [How It Works](#how-it-works)
10. [Scheduling the Job](#scheduling-the-job)
11. [Logging & Monitoring](#logging--monitoring)
12. [Sample Output](#sample-output)
13. [Future Improvements](#future-improvements)
14. [Author & Learning Outcomes](#author--learning-outcomes)

---

## 🧭 Overview

**Goal:**  
Build a system that automatically delivers inspirational quotes to subscribers based on their email frequency (daily or weekly), ensuring reliability, scalability, and clean observability via logs and monitoring.

**Key Responsibilities:**  
- Fetch fresh quotes from ZenQuotes API  
- Manage subscribers (PostgreSQL)  
- Send emails via Mailtrap (SMTP)  
- Handle errors and log all activity  
- Schedule automated daily runs at 7 AM  

This project simulates the backend service layer of a real mental wellness product — built with scalability and modularity in mind.

---

## ✨ Features

✅ Fetches motivational quotes from [ZenQuotes API](https://zenquotes.io)  
✅ Sends **personalized emails** based on subscription frequency  
✅ Handles **both daily and weekly** subscribers  
✅ Logs all activities (fetch, email, errors) to file and DB  
✅ Stores delivery history with timestamps and error messages  
✅ Uses `.env` for environment isolation and security  
✅ Ready for **Docker Compose** or **Cron job scheduling**

---

## ⚙️ Tech Stack

| Category | Technology |
|-----------|-------------|
| Language | Python 3.10+ |
| Database | PostgreSQL |
| Mail Service | Mailtrap (SMTP Testing) |
| API | ZenQuotes |
| Libraries | `psycopg2`, `requests`, `python-dotenv`, `schedule` |
| Logging | Python’s built-in `logging` module |
| Deployment | Docker / Cron Scheduler |

---

## 🛠️ Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/zenquotes-emailer.git
cd zenquotes-emailer
```

---

## 📁 Project Structure

``` bash
zenquotes_emailer/
│
├── app/
│   ├── main.py            
│   ├── db.py             
│   ├── emailer.py         
│   ├── quote_fetcher.py   
│   ├── config.py         
│
├── logs/
│   └── app.log            
│
├── .env                   
├── requirements.txt        
└── README.md               
```

---

## Configuration (.env)

Create a .env file in the root directory:

``` bash
DB_NAME=zenquotes
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

MAIL_HOST=smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USER=your-mailtrap-username
MAIL_PASSWORD=your-mailtrap-password
```

## 🧮 Database Schema

users

| **Column**     | **Type**         | **Description**         |
| ---------- | ------------ | ------------------- |
| id         | SERIAL       | Primary key         |
| email      | VARCHAR(255) | Unique email        |
| name       | VARCHAR(100) | Full name           |
| is_active  | BOOLEAN      | Active subscription |
| frequency  | VARCHAR(10)  | 'daily' or 'weekly' |
| created_at | TIMESTAMP    | Auto timestamp      |

email_sends

| **Column**        | **Type**        | **Description**              |
| ------------- | ----------- | ------------------------ |
| id            | SERIAL      | Primary key              |
| user_id       | INT         | FK → users(id)           |
| send_date     | DATE        | Defaults to current date |
| status        | VARCHAR(20) | ‘sent’ or ‘failed’       |
| error_message | TEXT        | Failure reason           |
| sent_at       | TIMESTAMP   | Auto timestamp           |

---

## ⚙️ How It Works

1. main.py runs the orchestrator.

2. It calls quote_fetcher.py to pull a fresh quote from ZenQuotes.

3. The system retrieves active users from PostgreSQL using db.py.

4. For each user:

 - Builds a personalized message (first name only).

 - Sends via SMTP using emailer.py.

 - Logs status (sent/failed) into the email_sends table.

5. Logs all operations in logs/app.log with timestamps.

---

## ⏰ Scheduling the Job

**Option 1 — Linux Cron**

Run the emailer every day at 7 AM:

``` bash
crontab -e
```

Add:

``` bash
0 7 * * * /path/to/venv/bin/python /path/to/app/main.py >> /path/to/logs/cron.log 2>&1
```

**Option 2 — Python Scheduler**

You can add this to `main.py`:

``` bash
import schedule, time
schedule.every().day.at("07:00").do(main)

while True:
    schedule.run_pending()
    time.sleep(60)
```

--

## 🪵 Logging & Monitoring

Every operation is logged both to the console and to logs/app.log.
Logs are grouped by section (Daily/Weekly) for readability.

Example log:

``` sql
================================================================================
=== DAILY QUOTES (2025-11-05) ==================================================
2025-11-05 07:00:02 - INFO - Quote fetched: "Change is hard..." - Robin Sharma
2025-11-05 07:00:03 - INFO - Found 2 active users.
2025-11-05 07:00:04 - INFO - Email sent successfully to user1@example.com
2025-11-05 07:00:05 - ERROR - Failed to send email to user2@example.com
================================================================================
```

---

## 🧩 Sample Output

**📩 Email Preview (HTML)**

 Hi first_name,

 “Change is hard at first, messy in the middle and gorgeous at the end.”
 — Robin Sharma

 Stay inspired,
 MindFuel Team

---

## 🚀 Future Enhancements

- Add REST API endpoints for user management (Flask/FastAPI)

- Add daily admin summary report (email stats)

- Implement retry mechanism for failed sends

- Add caching for quotes (Redis)

- Support timezones per user

- Integrate Celery for distributed scheduling

---

## 👨🏽‍💻 Author & Learning Outcomes

**Author:** Ganiu Odeyinka
LinkedIn

---

## Key Learnings

- Designing modular, maintainable Python systems

- Integrating APIs, databases, and email delivery pipelines

- Building fault-tolerant data workflows

- Managing logs, observability, and idempotent DB writes

- Transitioning from conceptual design thinking → engineering execution