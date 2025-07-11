from . import main_bp
from flask import render_template, request, flash, redirect, url_for, jsonify, current_app
from pkg.models import db

@main_bp.route('/about')
def about():
    return render_template('main/about.html')