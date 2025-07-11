from . import main_bp
from flask import render_template, request, flash, redirect, url_for, jsonify, current_app
from pkg.models import db
from flask_mail import Mail, Message

mail = Mail()

@main_bp.route('/')
def landing():
    return render_template('main/home.html')