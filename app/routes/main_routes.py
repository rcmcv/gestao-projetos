# Arquivo: app/routes/main_routes.py
from flask import Blueprint

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return '🚀 Sistema de Gestão de Projetos Online!'
