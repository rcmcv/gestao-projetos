# Arquivo: app/__init__.py

from flask import Flask
from app.extensions import db
from app.utils.email_utils import mail

# ✅ Importa todos os blueprints da interface web (rotas HTML)
from app.routes import (web_routes)

# ✅ Função centralizada para registrar todas as rotas da API REST
from app.api import registrar_rotas_api

# 🔧 Função que cria e configura a aplicação Flask
def create_app():
    # Cria a aplicação com suporte a pasta 'instance/' para configs
    app = Flask(__name__, instance_relative_config=True)

    # 🔒 Carrega configurações da instância (como o banco e chave secreta)
    app.config.from_pyfile('config.py')

    # 🔌 Inicializa as extensões do sistema (DB e Mail)
    db.init_app(app)
    mail.init_app(app)

    # 🌐 Registra todos os blueprints da interface web
    app.register_blueprint(web_routes)

    # 📡 Registra rotas da API REST com prefixo /api
    registrar_rotas_api(app)

    # Retorna a instância da aplicação já configurada
    return app
