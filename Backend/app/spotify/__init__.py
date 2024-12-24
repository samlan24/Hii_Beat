from flask import Blueprint

spoti = Blueprint('spoti', __name__)

from . import routes
