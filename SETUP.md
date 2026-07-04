# Employee Leave Management System - Setup & Run Guide

## ✅ Quick Start (SQLite - No Server Needed!)

This project uses **SQLite** making it super easy to run locally with zero configuration!

### Step 1: Install Dependencies
```bash
cd d:\MiniProject\Employee_Leave_Management
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Step 3: Initial Setup Wizard
Open your browser and visit: **http://localhost:5000**
Because the database is fresh, you will automatically be redirected to the **Setup Wizard**.
Fill out the form with your Company Name, Admin Name, Admin Email, and Admin Password to initialize your system.

---

## 🎯 Accounts & Registration

**Admin Login:**
- Use the credentials you just created in the Setup Wizard.

**Employee Login:**
- Register a new account to test employee features. 
- *Note:* Employees must use the company email domain configured during the Setup Wizard.
- *Note:* New employees are placed in a **Pending** status and must be manually approved by the Admin before they can log in.

---

## 📁 Project Structure

```
Employee_Leave_Management/
├── app.py                      # Flask app with SQLAlchemy
├── leave_management.db         # SQLite database (created automatically on run)
├── requirements.txt            # Python dependencies (includes gunicorn for deployment)
├── README.md                   # Repository overview
├── SETUP.md                    # This file
│
├── templates/
│   ├── index.html              # Landing page
│   ├── setup.html              # Database initialization wizard
│   ├── employee_login.html     # Employee login
│   ├── employee_register.html  # Employee registration
│   ├── employee_dashboard.html # Employee dashboard
│   ├── apply_leave.html        # Leave application form
│   ├── leave_history.html      # Leave history
│   ├── employee_profile.html   # Employee profile
│   ├── admin_login.html        # Admin login
│   ├── admin_dashboard.html    # Admin dashboard
│   ├── admin_leave_requests.html # Manage leave requests
│   ├── admin_employees.html    # Manage and approve employees
│   ├── admin_employee_detail.html # Employee details
│   ├── Macros.html             # Reusable UI components (like sidebars)
│   └── base.html               # Base template
│
└── static/
    ├── css/
    │   └── style.css           # Styling
    └── js/
        └── script.js           # JavaScript
```

---

## 🔧 Key Features

✅ **Employee Module**
- Register & Login (Domain restricted & Admin approved)
- Apply for leave (Casual, Sick, Earned)
- View leave history
- Track leave balance
- Manage profile

✅ **Admin Module**
- Initial setup wizard for dynamic configuration
- Approve/Reject new employee registrations
- Review and Approve/Reject leave requests
- Manage employees & View employee details
- Analytics dashboard

✅ **Security**
- Password hashing (Werkzeug)
- Session management
- Login required decorators
- Input validation

---

## 📊 Database Models

**Employees Table:**
- emp_id, name, email, password
- department, designation, phone, join_date
- casual_balance, sick_balance, earned_balance, status (Pending/Active/Rejected)

**Leave Requests Table:**
- employee_id, leave_type, start_date, end_date
- total_days, reason, status, admin_remarks

**Admins Table:**
- name, email, password

**Settings Table:**
- key, value (Stores dynamic company name and email domain)

---

## 🚀 Troubleshooting

**Issue: Port 5000 already in use**
```python
# Edit the last line of app.py:
app.run(debug=True, port=5001)
```

**Issue: Reset Database**
If you want to start completely fresh:
1. Stop the server (`Ctrl+C`).
2. Delete the `leave_management.db` file.
3. Restart the server and visit `http://localhost:5000` to go through the Setup Wizard again.

---

## 📝 Notes

- All dates are in `YYYY-MM-DD` format
- Leave balance defaults: Casual (12), Sick (10), Earned (15)
- Overlapping leave requests are prevented
- Admin approval deducts leave balance automatically

Enjoy! 🎉
