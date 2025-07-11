from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

from . import routes
from . import auth
from . import manage_projects
from . import manage_resume
from . import manage_messages