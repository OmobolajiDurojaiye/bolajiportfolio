from flask import Blueprint

main_bp = Blueprint('main', __name__)

from . import routes
from . import contact
from . import about
from . import portfolio
from . import resume
from . import blog