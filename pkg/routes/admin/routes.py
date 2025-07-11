from . import admin_bp
from flask import render_template, redirect, url_for, session, g
from pkg.models import User, ContactSubmission
from .auth import login_required

# Redirect base /admin to the auth page or dashboard
@admin_bp.route('/')
def index():
    if 'user_id' in session and g.user is not None:
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('admin.auth_page'))

# This will run before every request within this blueprint
@admin_bp.before_request
def before_request():
    """Load user from session and get unread message count."""
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
        g.unread_count = 0
    else:
        g.user = User.query.get(user_id)
        # Calculate unread messages count and add to global `g`
        g.unread_count = ContactSubmission.query.filter_by(is_read=False).count()

# Your protected admin dashboard
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    # The login_required decorator guarantees g.user is a valid user here
    return render_template("admin/dashboard.html")