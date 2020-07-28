from flask import Blueprint

bp = Blueprint('prod_recording', __name__, template_folder="templates")

from app.prod_recording import routes