from flask import Blueprint
routes = Blueprint('routes', __name__)

from .dashboard import dashboard
from .script_endpoints import validate_muid, load_pixel

