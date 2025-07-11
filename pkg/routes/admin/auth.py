from flask import render_template, request, flash, redirect, url_for, session, current_app, g
from . import admin_bp
from pkg.models import db, User
from pkg import mail
from flask_mail import Message
import random
from functools import wraps

# --- 1. THE ROBUST CUSTOM LOGIN DECORATOR (Unchanged) ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            session.clear()
            flash('Please log in to access this page.', 'info')
            return redirect(url_for('admin.auth_page'))
        return f(*args, **kwargs)
    return decorated_function

# --- 2. THE NEW UNIFIED AUTH ROUTE ---
@admin_bp.route('/auth', methods=['GET', 'POST'])
def auth_page():
    # If user is already logged in, redirect them to the dashboard
    if 'user_id' in session and g.user is not None:
        return redirect(url_for('admin.dashboard'))
    
    # Check if an admin account already exists to control signup visibility
    admin_exists = User.query.first() is not None

    # Handle the LOGIN form submission
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session.permanent = True # Keep user logged in
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    # For a GET request, show the page, passing the admin_exists flag
    return render_template('admin/auth.html', admin_exists=admin_exists)

# --- 3. SECURE SIGNUP ROUTE (POST ONLY) ---
@admin_bp.route('/signup', methods=['POST'])
def signup():
    # CRITICAL: Prevent more than one user from ever signing up
    if User.query.first():
        flash('An admin account already exists. Signup is disabled.', 'error')
        return redirect(url_for('admin.auth_page'))

    username = request.form.get('username')
    email = request.form.get('email') # This is the user's proposed email
    password = request.form.get('password')

    # Basic validation
    if not all([username, email, password]):
        flash('All fields are required for signup.', 'error')
        return redirect(url_for('admin.auth_page'))
    if len(password) < 8:
        flash('Password must be at least 8 characters long.', 'error')
        return redirect(url_for('admin.auth_page'))

    verification_code = random.randint(100000, 999999)
    session['signup_data'] = {
        'username': username,
        'email': email,
        'password': password,
        'code': verification_code
    }
    
    # CRITICAL: Send verification to the site owner's email, not the user's
    admin_email = current_app.config['MAIL_DEFAULT_SENDER'][1]

    msg = Message("Admin Account Creation Request", recipients=[admin_email])
    msg.body = f"""
    An attempt was made to create an admin account for your portfolio.
    
    Details provided:
    Username: {username}
    Email: {email}
    
    To approve this account creation, use the following verification code:
    
    {verification_code}
    
    If you did not request this, you can safely ignore this email.
    """
    
    try:
        mail.send(msg)
        flash('A verification code has been sent to the site administrator for approval.', 'info')
        return redirect(url_for('admin.verify'))
    except Exception as e:
        current_app.logger.error(f"Mail sending failed: {e}")
        flash('Could not send verification email. Please contact the site owner.', 'error')
        return redirect(url_for('admin.auth_page'))

# --- 4. VERIFY AND LOGOUT ROUTES ---
@admin_bp.route('/verify', methods=['GET', 'POST'])
def verify():
    if 'signup_data' not in session:
        flash('No signup process in progress. Please start again.', 'warning')
        return redirect(url_for('admin.auth_page'))

    if request.method == 'POST':
        user_code = request.form.get('code')
        signup_data = session.get('signup_data')

        if user_code and user_code.isdigit() and int(user_code) == signup_data['code']:
            new_user = User(username=signup_data['username'], email=signup_data['email'])
            new_user.set_password(signup_data['password'])
            db.session.add(new_user)
            db.session.commit()

            session.pop('signup_data', None)
            flash('Account created successfully! You may now log in.', 'success')
            return redirect(url_for('admin.auth_page'))
        else:
            flash('Invalid verification code. Please try again.', 'error')

    return render_template('admin/verify.html')

@admin_bp.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You have been successfully logged out.', 'success')
    return redirect(url_for('admin.auth_page'))