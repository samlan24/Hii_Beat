from flask import Blueprint

spleeter = Blueprint('spleeter', __name__)

from . import routes