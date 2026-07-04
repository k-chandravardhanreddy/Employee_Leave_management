# 🏢 Employee Leave Management System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)

A modern, secure, and fully responsive **Flask-based web application** designed to streamline employee leave requests and HR approvals. Built with a focus on clean UI/UX, the system allows companies to enforce domain-specific email registrations and manage employee access with a manual HR approval workflow.

---

## ✨ Key Features

### 👨‍💼 For Employees
* **Domain-Restricted Registration:** Employees can only register using verified company email domains.
* **Leave Applications:** Seamlessly apply for Casual, Sick, or Earned leave.
* **Real-time Dashboard:** Track current leave balances, view recent applications, and check approval statuses.
* **Profile Management:** Easily update contact details and personal information.

### 🛡️ For Administrators (HR)
* **Dynamic Setup Wizard:** First-time launch automatically triggers a UI setup wizard to configure the company domain and admin credentials.
* **Employee Verification Flow:** New employee registrations are placed in a **Pending** queue for manual admin review, preventing unauthorized access.
* **Leave Management:** Approve or reject leave requests with optional remarks. Leave balances are automatically deducted upon approval.
* **Analytics Dashboard:** Get a bird's-eye view of total employees, pending requests, and system activity.

---

## 🛠️ Technology Stack

* **Backend:** Python, Flask, Flask-SQLAlchemy
* **Database:** SQLite (Auto-generated)
* **Frontend:** HTML5, Vanilla CSS (Custom Design System), JavaScript
* **Security:** Werkzeug Password Hashing, Secure Session Management

---

## 🚀 Getting Started

Follow these steps to run the application locally.

### 1. Clone & Navigate
```bash
# Navigate to the project directory
cd d:\MiniProject\Employee_Leave_Management
```

### 2. Install Dependencies
It is recommended to use a virtual environment.
```bash
# Install required Python packages
pip install -r requirements.txt
```

### 3. Run the Application
Start the Flask development server:
```bash
python app.py
```

### 4. Initial Setup
1. Open your browser and navigate to `http://localhost:5000`.
2. On your very first run, you will be redirected to the **Setup Wizard**.
3. Enter your Company Name, Company Domain, and establish your Admin credentials.
4. The SQLite database is automatically configured and you're ready to go!

---

## 🌐 Deployment Ready

This application is configured for easy deployment on platforms like **Render** or **Heroku**.
* `gunicorn` is included in the `requirements.txt`.
* A `.gitignore` is provided to ensure local databases and caches are not pushed to production.
* The application is fully stateless aside from the database, making it perfect for containerized environments.

*For detailed deployment instructions, refer to the Deployment Guide.*

---
*Designed & Developed for seamless HR operations.*
