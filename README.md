<div align="center">

  <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Python-Dark.svg" width="30" />
  <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Flask-Dark.svg" width="30" />
  <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Docker.svg" width="30" />

  <h1>SecureForum CTF</h1>
  <p><b>A Deliberately Vulnerable Web Application</b></p>
  <p>A fake community forum packed with four real-world web vulnerabilities. Find the flags, understand the exploits, learn the fixes.</p>

</div>

---

## Overview

**SecureForum** is a deliberately vulnerable web application built with Flask and SQLite. It simulates a community forum with broken authentication, insecure comment rendering, a missing access control guard, and an exploitable profile endpoint.

Every vulnerability was designed to reflect a real mistake developers actually make, not an artificial trap. The app is fully containerized and runs with a single Docker command.

## Vulnerabilities

| # | Vulnerability | OWASP Category | Location |
|---|---|---|---|
| 1 | SQL Injection | A03:2021 - Injection | `/login` |
| 2 | Stored XSS | A03:2021 - Injection | `/comments` |
| 3 | Broken Access Control | A01:2021 - Broken Access Control | `/admin` |
| 4 | IDOR | A01:2021 - Broken Access Control | `/profile?id=N` |

## Getting Started

SecureForum requires **only Docker**. No Python installation, no dependency management.

**1. Clone the repository**
```bash
git clone https://github.com/shndnth/SecureForum-CTF.git
cd SecureForum-CTF
```

**2. Build and run**
```bash
docker-compose up --build
```

**3. Open in your browser**
```
http://localhost:5000
```

To stop the app:
```bash
docker-compose down
```

## Credentials

Three accounts are seeded into the database on first run:

| Username | Password | Role |
|---|---|---|
| player | player123 | user |
| alice | alice456 | user |
| admin | adm1n!pass | admin |

Start with the `player` account.

## Pages

| Route | Description |
|---|---|
| `/` | Home page |
| `/login` | Login form |
| `/comments` | Community forum |
| `/admin` | Admin panel |
| `/profile?id=N` | User profile viewer |
| `/logout` | Clears the session |

## Stack

* **Backend:** Python, Flask, SQLite
* **Frontend:** Jinja2 templates, plain CSS, Google Fonts
* **Runtime:** Docker, Docker Compose

## Disclaimer

This application is intentionally insecure. It was built for educational purposes only. Do not deploy it on a public server or expose it to untrusted networks.

## License

This project is open-source and available under the **MIT License**.
