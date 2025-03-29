# Arquivo: app/__init__.py

from flask import Flask
from app.extensions import db
from app.utils.email_utils import mail

# Rotas da interface web (HTML)
from app.routes import (
    web_routes,
    auth_routes,
    main_routes,
    tipos_routes,
    unidades_routes,
    materiais_routes,
    fornecedores_routes,
    clientes_routes,
    status_routes,
    projetos_routes,
    materiais_projeto_routes,
    orcamentos_routes
)

# Função que registra TODAS as rotas da API automaticamente
from app.api import registrar_rotas_api

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # 🔧 Configurações da instância (pasta instance/config.py)
    app.config.from_pyfile('config.py')

    # 🔌 Inicializar extensões
    db.init_app(app)
    mail.init_app(app)

    # 🌐 Registrar rotas da interface web (HTML)
    app.register_blueprint(web_routes.bp)
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(main_routes.bp)
    app.register_blueprint(tipos_routes.bp)
    app.register_blueprint(unidades_routes.bp)
    app.register_blueprint(materiais_routes.bp)
    app.register_blueprint(fornecedores_routes.bp)
    app.register_blueprint(clientes_routes.bp)
    app.register_blueprint(status_routes.bp)
    app.register_blueprint(projetos_routes.bp)
    app.register_blueprint(materiais_projeto_routes.bp)
    app.register_blueprint(orcamentos_routes.bp)

    # 📡 Registrar rotas da API
    registrar_rotas_api(app)

    return app
