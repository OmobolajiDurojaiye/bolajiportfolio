from . import main_bp
from flask import render_template, request, flash, redirect, url_for, jsonify, current_app
from pkg.models import db, Project  # Import the new Project model
import click
from datetime import date

@main_bp.route('/portfolio')
def portfolio():
    """Renders the portfolio page, displaying all projects from the DB."""
    projects = Project.query.order_by(Project.date.desc()).all()
    return render_template('main/portfolio.html', projects=projects)
