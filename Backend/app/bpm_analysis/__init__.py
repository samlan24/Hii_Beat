from flask import Blueprint

bpm = Blueprint('bpm', __name__)

from . import routes