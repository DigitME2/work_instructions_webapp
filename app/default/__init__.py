from flask import Blueprint

bp = Blueprint('default', __name__, template_folder="templates")

from app.default import routes