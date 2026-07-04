"""
Employee Leave Management System
Flask Backend - app.py with SQLAlchemy
"""

from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash, jsonify)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
from functools import wraps
import re
import os

app = Flask(__name__)
app.secret_key = 'lms_super_secret_key_2024'

# ─────────────────────────────────────────────
#  SQLite Configuration & Company Settings
# ─────────────────────────────────────────────
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "leave_management.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ─────────────────────────────────────────────
#  Database Models
# ─────────────────────────────────────────────
class Setting(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(255), nullable=False)
class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    join_date = db.Column(db.Date, nullable=False)
    casual_balance = db.Column(db.Integer, default=12)
    sick_balance = db.Column(db.Integer, default=10)
    earned_balance = db.Column(db.Integer, default=15)
    status = db.Column(db.String(20), default='Pending')  # 'Pending', 'Active', 'Rejected'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    leaves = db.relationship('LeaveRequest', backref='employee', lazy=True, cascade='all, delete-orphan')

class LeaveRequest(db.Model):
    __tablename__ = 'leave_requests'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    leave_type = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_days = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    admin_remarks = db.Column(db.Text)
    applied_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ──────────────────────────────
#  Decorators
# ──────────────────────────────
def employee_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'employee_id' not in session:
            flash('Please login to continue.', 'error')
            return redirect(url_for('employee_login'))
        
        # Verify employee still exists in database
        emp = db.session.get(Employee, session['employee_id'])
        if not emp:
            session.clear()
            flash('Session expired or invalid. Please login again.', 'error')
            return redirect(url_for('employee_login'))
            
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Admin login required.', 'error')
            return redirect(url_for('admin_login'))
            
        # Verify admin still exists in database
        admin = db.session.get(Admin, session['admin_id'])
        if not admin:
            session.clear()
            flash('Session expired or invalid. Please login again.', 'error')
            return redirect(url_for('admin_login'))
            
        return f(*args, **kwargs)
    return decorated


# ──────────────────────────────
#  Helpers
# ──────────────────────────────
def business_days(start: date, end: date) -> int:
    """Return calendar days inclusive (weekends counted for simplicity)."""
    delta = (end - start).days + 1
    return max(delta, 1)


def generate_emp_id() -> str:
    """Generate next employee ID."""
    last_emp = Employee.query.order_by(Employee.id.desc()).first()
    next_id = (last_emp.id if last_emp else 0) + 1
    return f"EMP{next_id:04d}"




# ──────────────────────────────
#  Helpers & Settings
# ──────────────────────────────
def get_setting(key: str, default: str = "") -> str:
    """Helper to fetch a setting value from database."""
    try:
        setting = Setting.query.filter_by(key=key).first()
        if setting:
            return setting.value
    except Exception:
        pass
    return default


@app.context_processor
def inject_company_settings():
    """Inject company settings dynamically into all templates."""
    company_name = get_setting('company_name', 'LeaveSync')
    company_domain = get_setting('company_domain', 'company.com')
    return dict(company_name=company_name, company_domain=company_domain)


@app.before_request
def check_setup():
    """Enforce registration setup before allowing app access."""
    # Allow assets and setup wizard endpoints
    if request.path.startswith('/static/') or request.endpoint in ('setup_wizard', 'static'):
        return None

    # Check if there are any admins configured
    try:
        if Admin.query.first() is None:
            return redirect(url_for('setup_wizard'))
    except Exception:
        # Table might not exist yet, trigger setup
        db.create_all()
        return redirect(url_for('setup_wizard'))


# ──────────────────────────────
#  Setup Wizard
# ──────────────────────────────
@app.route('/setup', methods=['GET', 'POST'])
def setup_wizard():
    # If admin already exists, block access
    try:
        if Admin.query.first() is not None:
            flash('System is already initialized.', 'error')
            return redirect(url_for('admin_login'))
    except Exception:
        # Tables don't exist yet, we will create them below
        pass

    if request.method == 'POST':
        company_name = request.form.get('company_name', '').strip()
        admin_name = request.form.get('admin_name', '').strip()
        admin_email = request.form.get('admin_email', '').strip().lower()
        admin_password = request.form.get('admin_password', '')

        errors = []
        if not all([company_name, admin_name, admin_email, admin_password]):
            errors.append('All fields are required.')
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', admin_email):
            errors.append('Invalid email address.')
        if len(admin_password) < 6:
            errors.append('Admin password must be at least 6 characters.')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('setup.html')

        # Initialize schema
        db.create_all()

        # Parse company domain from email (e.g. admin@acme.com -> acme.com)
        domain = admin_email.split('@')[-1]

        # Reset settings
        db.session.query(Setting).filter(Setting.key.in_(['company_name', 'company_domain'])).delete(synchronize_session=False)
        db.session.add(Setting(key='company_name', value=company_name))
        db.session.add(Setting(key='company_domain', value=domain))

        # Create Admin
        hashed = generate_password_hash(admin_password)
        admin = Admin(
            name=admin_name,
            email=admin_email,
            password=hashed
        )
        db.session.add(admin)
        db.session.commit()

        flash('Setup completed successfully! Please login with your admin account.', 'success')
        return redirect(url_for('admin_login'))

    return render_template('setup.html')


# ──────────────────────────────
#  Root
# ──────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')


# ══════════════════════════════════════════════════════
#  EMPLOYEE ROUTES
# ══════════════════════════════════════════════════════

@app.route('/employee/register', methods=['GET', 'POST'])
def employee_register():
    if request.method == 'POST':
        name        = request.form.get('name', '').strip()
        email       = request.form.get('email', '').strip().lower()
        password    = request.form.get('password', '')
        department  = request.form.get('department', '').strip()
        designation = request.form.get('designation', '').strip()
        phone       = request.form.get('phone', '').strip()
        join_date   = request.form.get('join_date', '')

        errors = []
        if not all([name, email, password, department, designation, join_date]):
            errors.append('All required fields must be filled.')
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            errors.append('Invalid email address.')
        else:
            comp_domain = get_setting('company_domain', 'company.com')
            if not email.endswith('@' + comp_domain):
                errors.append(f'Registration is restricted to company email addresses ending with @{comp_domain}.')
        if len(password) < 6:
            errors.append('Password must be at least 6 characters.')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('employee_register.html')

        if Employee.query.filter_by(email=email).first() or Admin.query.filter_by(email=email).first():
            flash('Email already in use.', 'error')
            return render_template('employee_register.html')

        # Create the new employee account in Pending status
        emp_id = generate_emp_id()
        hashed = generate_password_hash(password)
        emp = Employee(
            emp_id=emp_id,
            name=name,
            email=email,
            password=hashed,
            department=department,
            designation=designation,
            phone=phone,
            join_date=datetime.strptime(join_date, '%Y-%m-%d').date(),
            status='Pending'
        )
        db.session.add(emp)
        db.session.commit()

        flash('Registration successful! Your account is pending HR approval. You will be able to log in once activated.', 'success')
        return redirect(url_for('employee_login'))

    return render_template('employee_register.html')


@app.route('/employee/login', methods=['GET', 'POST'])
def employee_login():
    if 'employee_id' in session:
        return redirect(url_for('employee_dashboard'))

    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        emp = Employee.query.filter_by(email=email).first()

        if emp and check_password_hash(emp.password, password):
            if emp.status != 'Active':
                flash(f'Your account is currently {emp.status.lower()}. Please wait for HR approval.', 'error')
                return redirect(url_for('employee_login'))
            session['employee_id']   = emp.id
            session['employee_name'] = emp.name
            session['employee_emp_id'] = emp.emp_id
            flash(f'Welcome back, {emp.name}!', 'success')
            return redirect(url_for('employee_dashboard'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('employee_login.html')


@app.route('/employee/logout')
def employee_logout():
    session.pop('employee_id', None)
    session.pop('employee_name', None)
    session.pop('employee_emp_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('employee_login'))


@app.route('/employee/dashboard')
@employee_required
def employee_dashboard():
    emp = db.session.get(Employee, session['employee_id'])
    
    stats = {
        'total': LeaveRequest.query.filter_by(employee_id=emp.id).count(),
        'pending': LeaveRequest.query.filter_by(employee_id=emp.id, status='Pending').count(),
        'approved': LeaveRequest.query.filter_by(employee_id=emp.id, status='Approved').count(),
        'rejected': LeaveRequest.query.filter_by(employee_id=emp.id, status='Rejected').count(),
    }
    
    recent = LeaveRequest.query.filter_by(employee_id=emp.id).order_by(LeaveRequest.applied_on.desc()).limit(5).all()
    
    return render_template('employee_dashboard.html', emp=emp, stats=stats, recent=recent)


@app.route('/employee/apply_leave', methods=['GET', 'POST'])
@employee_required
def apply_leave():
    emp = db.session.get(Employee, session['employee_id'])

    if request.method == 'POST':
        leave_type = request.form.get('leave_type')
        start_date = request.form.get('start_date')
        end_date   = request.form.get('end_date')
        reason     = request.form.get('reason', '').strip()

        if not all([leave_type, start_date, end_date, reason]):
            flash('All fields are required.', 'error')
            return render_template('apply_leave.html', emp=emp)

        s = datetime.strptime(start_date, '%Y-%m-%d').date()
        e = datetime.strptime(end_date,   '%Y-%m-%d').date()

        if e < s:
            flash('End date cannot be before start date.', 'error')
            return render_template('apply_leave.html', emp=emp)

        total_days = business_days(s, e)

        balance_col = {'Casual': emp.casual_balance,
                       'Sick': emp.sick_balance,
                       'Earned': emp.earned_balance}.get(leave_type)
        if balance_col and balance_col < total_days:
            flash(f'Insufficient {leave_type} leave balance. Available: {balance_col} days.', 'error')
            return render_template('apply_leave.html', emp=emp)

        overlap = LeaveRequest.query.filter(
            LeaveRequest.employee_id == emp.id,
            LeaveRequest.status != 'Rejected',
            LeaveRequest.start_date <= e,
            LeaveRequest.end_date >= s
        ).first()
        
        if overlap:
            flash('You already have a leave request overlapping these dates.', 'error')
            return render_template('apply_leave.html', emp=emp)

        leave = LeaveRequest(
            employee_id=emp.id,
            leave_type=leave_type,
            start_date=s,
            end_date=e,
            total_days=total_days,
            reason=reason
        )
        db.session.add(leave)
        db.session.commit()
        flash(f'Leave application submitted successfully for {total_days} day(s).', 'success')
        return redirect(url_for('leave_history'))

    return render_template('apply_leave.html', emp=emp)


@app.route('/employee/leave_history')
@employee_required
def leave_history():
    status_filter = request.args.get('status', 'All')
    search        = request.args.get('search', '').strip()

    query = LeaveRequest.query.filter_by(employee_id=session['employee_id'])

    if status_filter != 'All':
        query = query.filter_by(status=status_filter)
    if search:
        query = query.filter(
            (LeaveRequest.leave_type.ilike(f'%{search}%')) |
            (LeaveRequest.reason.ilike(f'%{search}%'))
        )

    leaves = query.order_by(LeaveRequest.applied_on.desc()).all()
    return render_template('leave_history.html', leaves=leaves,
                           status_filter=status_filter, search=search)


@app.route('/employee/profile')
@employee_required
def employee_profile():
    emp = db.session.get(Employee, session['employee_id'])
    return render_template('employee_profile.html', emp=emp)


@app.route('/employee/profile/update', methods=['POST'])
@employee_required
def employee_profile_update():
    emp = db.session.get(Employee, session['employee_id'])
    emp.phone = request.form.get('phone', '').strip()
    db.session.commit()
    flash('Profile updated successfully.', 'success')
    return redirect(url_for('employee_profile'))


# ══════════════════════════════════════════════════════
#  ADMIN ROUTES
# ══════════════════════════════════════════════════════

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if 'admin_id' in session:
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        admin = Admin.query.filter_by(email=email).first()

        if admin and check_password_hash(admin.password, password):
            session['admin_id']   = admin.id
            session['admin_name'] = admin.name
            flash(f'Welcome, {admin.name}!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials.', 'error')

    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    session.pop('admin_name', None)
    flash('Admin logged out.', 'info')
    return redirect(url_for('admin_login'))


@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    total_emp = Employee.query.count()
    
    stats = {
        'total': LeaveRequest.query.count(),
        'pending': LeaveRequest.query.filter_by(status='Pending').count(),
        'approved': LeaveRequest.query.filter_by(status='Approved').count(),
        'rejected': LeaveRequest.query.filter_by(status='Rejected').count(),
    }
    
    pending = LeaveRequest.query.filter_by(status='Pending').order_by(LeaveRequest.applied_on.desc()).limit(5).all()
    
    return render_template('admin_dashboard.html',
                           total_emp=total_emp, stats=stats, pending=pending)


@app.route('/admin/leave_requests')
@admin_required
def admin_leave_requests():
    status_filter = request.args.get('status', 'All')
    
    query = LeaveRequest.query
    if status_filter != 'All':
        query = query.filter_by(status=status_filter)
    
    leaves = query.order_by(LeaveRequest.applied_on.desc()).all()
    
    for leave in leaves:
        leave.employee_name = leave.employee.name
    
    return render_template('admin_leave_requests.html', leaves=leaves, status_filter=status_filter)


@app.route('/admin/action/<int:leave_id>', methods=['POST'])
@admin_required
def admin_action(leave_id):
    action  = request.form.get('action')
    remarks = request.form.get('remarks', '').strip()

    if action not in ('Approved', 'Rejected'):
        flash('Invalid action.', 'error')
        return redirect(url_for('admin_leave_requests'))

    leave = db.session.get(LeaveRequest, leave_id)

    if not leave:
        flash('Leave request not found.', 'error')
        return redirect(url_for('admin_leave_requests'))

    if leave.status != 'Pending':
        flash('This request has already been processed.', 'error')
        return redirect(url_for('admin_leave_requests'))

    leave.status = action
    leave.admin_remarks = remarks
    
    if action == 'Approved':
        emp = leave.employee
        if leave.leave_type == 'Casual':
            emp.casual_balance -= leave.total_days
        elif leave.leave_type == 'Sick':
            emp.sick_balance -= leave.total_days
        elif leave.leave_type == 'Earned':
            emp.earned_balance -= leave.total_days

    db.session.commit()
    flash(f'Leave request {action.lower()} successfully.', 'success')
    return redirect(url_for('admin_leave_requests'))


@app.route('/admin/employee/action/<int:emp_id>', methods=['POST'])
@admin_required
def admin_employee_action(emp_id):
    action = request.form.get('action')
    if action not in ('Active', 'Rejected'):
        flash('Invalid action.', 'error')
        return redirect(url_for('admin_employees'))

    emp = db.session.get(Employee, emp_id)
    if not emp:
        flash('Employee not found.', 'error')
        return redirect(url_for('admin_employees'))

    if emp.status != 'Pending':
        flash('Employee is already processed.', 'error')
        return redirect(url_for('admin_employees'))

    emp.status = action
    db.session.commit()
    flash(f'Employee account {action.lower()} successfully.', 'success')
    return redirect(url_for('admin_employees'))


@app.route('/admin/employees')
@admin_required
def admin_employees():
    search = request.args.get('search', '').strip()
    dept   = request.args.get('dept', 'All')

    query = Employee.query
    
    if search:
        query = query.filter(
            (Employee.name.ilike(f'%{search}%')) |
            (Employee.emp_id.ilike(f'%{search}%')) |
            (Employee.email.ilike(f'%{search}%'))
        )
    if dept != 'All':
        query = query.filter_by(department=dept)

    employees = query.order_by(Employee.created_at.desc()).all()
    
    depts = db.session.query(Employee.department).distinct().order_by(Employee.department).all()
    depts = [d[0] for d in depts]
    
    return render_template('admin_employees.html', employees=employees,
                           search=search, dept=dept, depts=depts)


@app.route('/admin/employee/<int:emp_id>')
@admin_required
def admin_employee_detail(emp_id):
    emp = db.session.get(Employee, emp_id)
    if not emp:
        flash('Employee not found.', 'error')
        return redirect(url_for('admin_employees'))

    leaves = LeaveRequest.query.filter_by(employee_id=emp_id).order_by(LeaveRequest.applied_on.desc()).all()
    return render_template('admin_employee_detail.html', emp=emp, leaves=leaves)


# ──────────────────────────────
#  API – leave stats (AJAX)
# ──────────────────────────────
@app.route('/api/leave_stats')
@employee_required
def api_leave_stats():
    emp = db.session.get(Employee, session['employee_id'])
    return jsonify({
        'casual_balance': emp.casual_balance,
        'sick_balance': emp.sick_balance,
        'earned_balance': emp.earned_balance
    })


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
