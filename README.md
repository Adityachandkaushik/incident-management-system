# incident-management-system
Open-source incident management system for logging, tracking, assigning, and resolving infrastructure and application incidents with role-based access and DevOps automation.

# 🚨 Open-Source Incident Management System

A lightweight Incident Management System designed to help teams log, track, assign, and resolve infrastructure and application incidents through a centralized portal.

The project is being developed as a hands-on DevOps project, gradually moving from a local Flask application to a containerized, CI/CD-driven deployment on AWS.

---

## 🎯 Project Objective

The goal of this project is to build a centralized incident management portal that allows teams to:

- 🚨 Create and track incidents
- 👨‍💻 Assign incidents to engineers
- 🔄 Track incident status
- ⚡ Manage priority and severity
- ✅ Resolve and close incidents
- 🔐 Implement role-based access control
- 📧 Send email notifications
- 🐳 Containerize the application
- 🔄 Implement CI/CD
- ☁️ Deploy the application on AWS

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| Flask | Web framework & REST APIs |
| SQLite | Database |
| HTML / Jinja2 | Frontend |
| Bootstrap | UI |
| Git | Version control |
| GitHub | Source code management |
| Docker | Containerization |
| SMTP | Email notifications |
| GitHub Actions | CI/CD |
| AWS EC2 | Cloud deployment |

---

## 👥 User Roles

### 👑 Admin
- Manage users
- View all incidents
- Assign incidents
- Manage incident lifecycle

### 👨‍💻 Engineer
- View assigned incidents
- Update incidents
- Change status
- Resolve incidents

### 👤 User
- Create incidents
- View submitted incidents
- Track incident status

---

## 🔄 Incident Lifecycle

```text
OPEN
  ↓
ASSIGNED
  ↓
IN_PROGRESS
  ↓
RESOLVED
  ↓
CLOSED
