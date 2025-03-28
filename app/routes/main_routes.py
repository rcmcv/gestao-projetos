# Arquivo: app/routes/main_routes.py
from flask import Blueprint

bp = Blueprint('main', __name__)

@bp.route('/inicio')
def home():
    return '🚀 Sistema de Gestão de Projetos Online!'
