from flask import Blueprint

bp = Blueprint('part_creation', __name__, template_folder="templates")

from app.part_creation import routes