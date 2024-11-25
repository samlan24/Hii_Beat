from flask import Blueprint

bpm_change = Blueprint('bpm_change', __name__)

from . import routes
from . import utils