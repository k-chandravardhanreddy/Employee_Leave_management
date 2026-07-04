# Employee Leave Management System
## Project Documentation

---

## Table of Contents

1. [Abstract](#1-abstract)
2. [Introduction](#2-introduction)
3. [Literature Survey](#3-literature-survey)
4. [System Requirements](#4-system-requirements)
5. [System Design](#5-system-design)
6. [Implementation](#6-implementation)
7. [Testing](#7-testing)
8. [Screenshots](#8-screenshots)
9. [Future Enhancements](#9-future-enhancements)
10. [Conclusion](#10-conclusion)
11. [References](#11-references)

---

## 1. Abstract

The **Employee Leave Management System** is a full-stack web application developed using the Flask framework in Python. It automates the process of applying for, tracking, and managing employee leaves within an organization. The system provides two distinct interfaces — one for **employees** to submit and monitor their leave requests, and another for **administrators (HR)** to review, approve, or reject those requests.

Key highlights include domain-restricted email registration, an HR-driven employee approval workflow, real-time leave balance tracking, and a modern, responsive user interface. The application uses SQLite as its database backend (auto-generated, requiring zero configuration) and has been deployed on Render.com using Gunicorn as the production WSGI server.

**Keywords:** Flask, Python, Leave Management, SQLAlchemy, SQLite, Web Application, HR Automation

---

## 2. Introduction

### 2.1 Background

In most organizations, tracking employee leave is done through manual registers, spreadsheets, or email chains. This approach is:
- **Error-prone** — manual tracking leads to miscalculations in leave balances.
- **Time-consuming** — HR managers spend excessive time on repetitive administrative tasks.
- **Lack of transparency** — employees often don't have real-time visibility into their remaining leave balances or the status of their pending requests.

### 2.2 Problem Statement

To design and develop a web-based Employee Leave Management System that automates the entire lifecycle of leave requests — from application to approval — while enforcing organizational policies such as domain-restricted registration and HR-verified employee accounts.

### 2.3 Objectives

| # | Objective |
|---|-----------|
| 1 | Automate the leave application and approval workflow |
| 2 | Provide real-time leave balance tracking for employees |
| 3 | Enable HR administrators to manage employee registrations with an approval/rejection mechanism |
| 4 | Enforce company domain-restricted email registration for security |
| 5 | Deliver a responsive, modern, and visually appealing web interface |
| 6 | Deploy the application on a cloud platform for remote accessibility |

### 2.4 Scope

The system covers:
- Employee self-registration with company email validation
- HR-driven employee verification (Pending → Active / Rejected)
- Leave application for three categories: Casual, Sick, and Earned
- Leave balance management with automatic deduction upon approval
- Admin dashboard with analytics and employee management
- Cloud deployment on Render.com

---

## 3. Literature Survey

| # | Title / Technology | Description | Relevance |
|---|---|---|---|
| 1 | **Flask Web Framework** | A lightweight Python micro-framework for building web applications. It follows the WSGI standard and provides routing, templating (Jinja2), and session management. | Core backend framework used in this project. |
| 2 | **Flask-SQLAlchemy** | An ORM (Object Relational Mapper) that integrates SQLAlchemy with Flask, providing Pythonic database interactions without writing raw SQL. | Used for all database operations, model definitions, and relationships. |
| 3 | **SQLite** | A serverless, zero-configuration, self-contained SQL database engine. | Chosen as the database for its simplicity and zero-setup requirements. |
| 4 | **Werkzeug Security** | Provides password hashing functions using PBKDF2 algorithm with salt, ensuring passwords are never stored in plaintext. | Used for secure password storage and verification. |
| 5 | **Jinja2 Templating** | A modern templating engine for Python, used by Flask to render dynamic HTML content. | Used for all 15 HTML templates with template inheritance and macros. |
| 6 | **Gunicorn** | A production-grade Python WSGI HTTP server for Unix/Linux. | Used as the production server on Render.com deployment. |

---

## 4. System Requirements

### 4.1 Hardware Requirements

| Component | Minimum Requirement |
|---|---|
| Processor | Intel i3 or equivalent |
| RAM | 4 GB |
| Storage | 500 MB free space |
| Network | Internet connection (for deployment) |

### 4.2 Software Requirements

| Component | Specification |
|---|---|
| Operating System | Windows 10+ / macOS / Linux |
| Programming Language | Python 3.8+ |
| Web Framework | Flask 3.0.3 |
| ORM | Flask-SQLAlchemy 3.1.1 |
| Security Library | Werkzeug 3.0.3 |
| Database | SQLite 3 (built into Python) |
| Production Server | Gunicorn 22.0.0 |
| Browser | Chrome, Firefox, Edge (modern) |
| Deployment Platform | Render.com |

### 4.3 Python Dependencies

```
Flask==3.0.3
Flask-SQLAlchemy==3.1.1
Werkzeug==3.0.3
gunicorn==22.0.0
```

---

## 5. System Design

### 5.1 System Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     CLIENT BROWSER                       │
│              (HTML5 / CSS3 / JavaScript)                 │
└────────────────────────┬─────────────────────────────────┘
                         │  HTTP Requests
                         ▼
┌──────────────────────────────────────────────────────────┐
│                  FLASK APPLICATION                       │
│                     (app.py)                             │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │   Routes     │  │  Decorators  │  │   Helpers     │  │
│  │  /employee/* │  │ @employee_   │  │ business_days │  │
│  │  /admin/*    │  │   required   │  │ generate_emp_ │  │
│  │  /setup      │  │ @admin_      │  │   id          │  │
│  │  /api/*      │  │   required   │  │ get_setting   │  │
│  └──────────────┘  └──────────────┘  └───────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │           Jinja2 Template Engine                  │    │
│  │   15 Templates + Macros + Template Inheritance   │    │
│  └──────────────────────────────────────────────────┘    │
└───────────┬──────────────────────────────┬───────────────┘
            │                              │
            ▼                              ▼
┌───────────────────────┐    ┌─────────────────────────────┐
│   SQLite Database     │    │    Static Assets            │
│  leave_management.db  │    │  /static/css/style.css      │
│                       │    │  /static/js/script.js       │
│  Tables:              │    │                             │
│  - settings           │    │                             │
│  - admins             │    │                             │
│  - employees          │    │                             │
│  - leave_requests     │    │                             │
└───────────────────────┘    └─────────────────────────────┘
```

### 5.2 Database Design (ER Diagram)

```
┌─────────────────┐          ┌─────────────────────────────┐
│     SETTINGS    │          │           ADMINS             │
├─────────────────┤          ├─────────────────────────────┤
│ id       (PK)  │          │ id            (PK)          │
│ key      (UQ)  │          │ name                        │
│ value           │          │ email         (UQ)          │
└─────────────────┘          │ password      (hashed)      │
                             │ created_at                  │
                             └─────────────────────────────┘

┌─────────────────────────────┐      ┌──────────────────────────────┐
│         EMPLOYEES           │      │       LEAVE_REQUESTS         │
├─────────────────────────────┤      ├──────────────────────────────┤
│ id            (PK)          │──1:N─│ id              (PK)         │
│ emp_id        (UQ)          │      │ employee_id     (FK)         │
│ name                        │      │ leave_type                   │
│ email         (UQ)          │      │ start_date                   │
│ password      (hashed)      │      │ end_date                     │
│ department                  │      │ total_days                   │
│ designation                 │      │ reason                       │
│ phone                       │      │ status                       │
│ join_date                   │      │ admin_remarks                │
│ casual_balance (def: 12)    │      │ applied_on                   │
│ sick_balance   (def: 10)    │      │ updated_on                   │
│ earned_balance (def: 15)    │      └──────────────────────────────┘
│ status (Pending/Active/     │
│         Rejected)           │
│ created_at                  │
└─────────────────────────────┘
```

### 5.3 Application Workflow

```
┌──────────────┐     ┌───────────────┐     ┌──────────────────┐
│  First Run   │────▶│ Setup Wizard  │────▶│ Admin Account    │
│  (No Admin)  │     │ /setup        │     │ Created          │
└──────────────┘     └───────────────┘     └────────┬─────────┘
                                                     │
                          ┌──────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    EMPLOYEE FLOW                            │
│                                                             │
│  Register ──▶ Pending ──▶ Admin Approves ──▶ Active Login  │
│  (company       │                               │           │
│   email only)   │                               ▼           │
│                 ▼                         Apply Leave        │
│           Admin Rejects                      │              │
│                 │                            ▼              │
│                 ▼                     Admin Reviews          │
│           Cannot Login               ┌──────┴──────┐       │
│                                      ▼             ▼        │
│                                  Approved      Rejected     │
│                                  (balance       (no         │
│                                   deducted)     change)     │
└─────────────────────────────────────────────────────────────┘
```

### 5.4 Module Design

#### Module 1: Setup Wizard
- First-time initialization of the application
- Configures company name and email domain
- Creates the primary admin account
- Auto-generates the SQLite database schema

#### Module 2: Employee Module
| Feature | Route | Method |
|---------|-------|--------|
| Register | `/employee/register` | GET, POST |
| Login | `/employee/login` | GET, POST |
| Logout | `/employee/logout` | GET |
| Dashboard | `/employee/dashboard` | GET |
| Apply Leave | `/employee/apply_leave` | GET, POST |
| Leave History | `/employee/leave_history` | GET |
| Profile | `/employee/profile` | GET |
| Update Profile | `/employee/profile/update` | POST |

#### Module 3: Admin Module
| Feature | Route | Method |
|---------|-------|--------|
| Login | `/admin/login` | GET, POST |
| Logout | `/admin/logout` | GET |
| Dashboard | `/admin/dashboard` | GET |
| Leave Requests | `/admin/leave_requests` | GET |
| Approve/Reject Leave | `/admin/action/<id>` | POST |
| Employee List | `/admin/employees` | GET |
| Approve/Reject Employee | `/admin/employee/action/<id>` | POST |
| Employee Detail | `/admin/employee/<id>` | GET |

#### Module 4: API Module
| Feature | Route | Method |
|---------|-------|--------|
| Leave Stats (AJAX) | `/api/leave_stats` | GET |

---

## 6. Implementation

### 6.1 Project Structure

```
Employee_Leave_Management/
├── app.py                          # Main Flask application (632 lines)
├── leave_management.db             # SQLite database (auto-generated)
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git exclusion rules
├── README.md                       # Repository overview
├── SETUP.md                        # Detailed setup guide
│
├── templates/                      # Jinja2 HTML Templates (15 files)
│   ├── base.html                   # Base layout with flash messages
│   ├── Macros.html                 # Reusable sidebar components
│   ├── index.html                  # Landing page
│   ├── setup.html                  # Setup wizard
│   ├── employee_login.html         # Employee login
│   ├── employee_register.html      # Employee registration
│   ├── employee_dashboard.html     # Employee dashboard
│   ├── apply_leave.html            # Leave application form
│   ├── leave_history.html          # Leave history with filters
│   ├── employee_profile.html       # Employee profile
│   ├── admin_login.html            # Admin login
│   ├── admin_dashboard.html        # Admin dashboard
│   ├── admin_leave_requests.html   # Leave request management
│   ├── admin_employees.html        # Employee management
│   └── admin_employee_detail.html  # Individual employee detail
│
└── static/
    ├── css/
    │   └── style.css               # Custom CSS design system
    └── js/
        └── script.js               # Client-side JavaScript
```

### 6.2 Key Implementation Details

#### 6.2.1 Database Models (SQLAlchemy ORM)

Four models are defined in `app.py`:

```python
class Setting(db.Model):       # Dynamic configuration storage
class Admin(db.Model):          # Administrator accounts
class Employee(db.Model):       # Employee accounts with leave balances
class LeaveRequest(db.Model):   # Leave applications
```

The `Employee` model has a one-to-many relationship with `LeaveRequest` using `db.relationship()` with cascade delete.

#### 6.2.2 Authentication & Authorization

Two Python decorators enforce role-based access:
- `@employee_required` — Restricts routes to logged-in employees; also validates that the employee still exists in the database.
- `@admin_required` — Restricts routes to logged-in admins; also validates that the admin still exists in the database.

Both decorators clear the session and redirect to the login page if the user no longer exists (e.g., after a database reset), preventing 500 Internal Server Errors.

#### 6.2.3 Domain Restriction

During registration, the system extracts the company domain from the database settings and validates the employee's email:

```python
comp_domain = get_setting('company_domain', 'company.com')
if not email.endswith('@' + comp_domain):
    flash('Registration is restricted to company email addresses...')
```

#### 6.2.4 Employee Approval Workflow

1. Employee registers → `status = 'Pending'`
2. Employee tries to login → Blocked with message if not `Active`
3. Admin visits Employees page → Sees Pending employees with Approve/Reject buttons
4. Admin clicks Approve → `status = 'Active'` → Employee can now login

#### 6.2.5 Leave Balance Management

Default balances assigned on registration:
- Casual Leave: 12 days
- Sick Leave: 10 days
- Earned Leave: 15 days

On approval, balances are automatically deducted:
```python
if action == 'Approved':
    emp = leave.employee
    if leave.leave_type == 'Casual':
        emp.casual_balance -= leave.total_days
```

#### 6.2.6 Setup Wizard

The `@app.before_request` hook checks if an admin exists. If not, all requests are redirected to `/setup`, ensuring the system is properly initialized before use.

### 6.3 Security Implementation

| Feature | Implementation |
|---|---|
| Password Storage | `generate_password_hash()` using PBKDF2 with salt |
| Password Verification | `check_password_hash()` |
| Session Management | Flask server-side sessions with `session` object |
| Input Validation | Regex for email, length checks for passwords |
| SQL Injection Prevention | SQLAlchemy ORM parameterized queries |
| XSS Prevention | Jinja2 auto-escaping enabled by default |
| Access Control | Custom decorators with DB existence validation |

---

## 7. Testing

### 7.1 Test Cases

| # | Test Case | Input | Expected Output | Status |
|---|---|---|---|---|
| 1 | Setup Wizard - Valid Input | Company name, admin email, password | System initialized, redirect to admin login | ✅ Pass |
| 2 | Setup Wizard - Duplicate Access | Visit /setup after admin exists | Redirected with error message | ✅ Pass |
| 3 | Employee Registration - Valid | Company email, valid details | Account created in Pending status | ✅ Pass |
| 4 | Employee Registration - Wrong Domain | Non-company email | Error: "Registration is restricted to company email" | ✅ Pass |
| 5 | Employee Login - Pending Account | Valid credentials, Pending status | Blocked: "Your account is currently pending" | ✅ Pass |
| 6 | Employee Login - Active Account | Valid credentials, Active status | Dashboard loaded successfully | ✅ Pass |
| 7 | Employee Login - Invalid Credentials | Wrong password | Error: "Invalid email or password" | ✅ Pass |
| 8 | Admin Approve Employee | Click Approve on pending employee | Status changed to Active | ✅ Pass |
| 9 | Admin Reject Employee | Click Reject on pending employee | Status changed to Rejected | ✅ Pass |
| 10 | Apply Leave - Valid | Valid dates, sufficient balance | Leave request submitted | ✅ Pass |
| 11 | Apply Leave - Insufficient Balance | Days > available balance | Error: "Insufficient leave balance" | ✅ Pass |
| 12 | Apply Leave - Overlapping Dates | Dates overlap existing request | Error: "Overlapping dates" | ✅ Pass |
| 13 | Admin Approve Leave | Approve leave request | Status = Approved, balance deducted | ✅ Pass |
| 14 | Admin Reject Leave | Reject leave request | Status = Rejected, no balance change | ✅ Pass |
| 15 | Session After DB Reset | Access dashboard after DB wipe | Auto-logout, redirect to login | ✅ Pass |
| 16 | Case-Sensitive Template (Linux) | Deploy on Render (Linux) | Templates load correctly | ✅ Pass |

### 7.2 Deployment Testing

| # | Test | Result |
|---|---|---|
| 1 | Push to GitHub | ✅ Successful |
| 2 | Render auto-build | ✅ Dependencies installed |
| 3 | Gunicorn starts successfully | ✅ Application running |
| 4 | Setup Wizard on fresh deploy | ✅ Redirected correctly |
| 5 | Full workflow on production | ✅ All features working |

---

## 8. Screenshots

> **Note:** Screenshots can be captured from the live deployment at:
> `https://employee-leave-management-22kt.onrender.com`

The following pages are available for screenshots:

| # | Page | URL Path |
|---|---|---|
| 1 | Landing Page | `/` |
| 2 | Setup Wizard | `/setup` |
| 3 | Employee Registration | `/employee/register` |
| 4 | Employee Login | `/employee/login` |
| 5 | Employee Dashboard | `/employee/dashboard` |
| 6 | Apply Leave Form | `/employee/apply_leave` |
| 7 | Leave History | `/employee/leave_history` |
| 8 | Employee Profile | `/employee/profile` |
| 9 | Admin Login | `/admin/login` |
| 10 | Admin Dashboard | `/admin/dashboard` |
| 11 | Leave Request Management | `/admin/leave_requests` |
| 12 | Employee Management | `/admin/employees` |
| 13 | Employee Detail View | `/admin/employee/<id>` |

---

## 9. Future Enhancements

1. **Email Notifications** — Send automated emails when leave is approved/rejected or when a new employee registers.
2. **PostgreSQL Migration** — Upgrade from SQLite to PostgreSQL for persistent data on cloud deployments.
3. **Leave Calendar View** — Visual calendar showing approved leaves and team availability.
4. **Report Generation** — Export leave reports to PDF or Excel formats.
5. **Multi-Admin Support** — Role hierarchy with Super Admin, HR Manager, and Department Head roles.
6. **Mobile PWA** — Progressive Web App for mobile-first access.
7. **Holiday Calendar** — Integrate public holidays into leave calculations.
8. **Audit Trail** — Log all admin actions for compliance and accountability.

---

## 10. Conclusion

The Employee Leave Management System successfully addresses the challenges of manual leave tracking by providing a fully digital, automated solution. The application demonstrates:

- **Full-stack development** using Python Flask with SQLAlchemy ORM
- **Real-world security practices** including password hashing, session management, and domain-restricted access
- **Professional HR workflows** with employee verification and leave approval processes
- **Cloud deployment** on Render.com with Gunicorn for production-grade serving
- **Modern UI/UX** with a responsive design system built using custom CSS

The system is currently deployed and accessible online, proving its readiness for real-world use in small to medium-sized organizations.

---

## 11. References

1. Flask Documentation — https://flask.palletsprojects.com/
2. Flask-SQLAlchemy Documentation — https://flask-sqlalchemy.palletsprojects.com/
3. SQLite Documentation — https://www.sqlite.org/docs.html
4. Werkzeug Security — https://werkzeug.palletsprojects.com/en/stable/utils/#module-werkzeug.security
5. Jinja2 Template Engine — https://jinja.palletsprojects.com/
6. Gunicorn Documentation — https://docs.gunicorn.org/
7. Render Deployment Guide — https://render.com/docs
8. Python Official Documentation — https://docs.python.org/3/

---

*Document prepared for: Mini Project Submission — June 2026*
