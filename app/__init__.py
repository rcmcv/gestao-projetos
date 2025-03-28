# Arquivo: app/__init__.py
from flask import Flask
from app.extensions import db
from app.routes import tipos_routes
from app.routes import unidades_routes
from app.routes import materiais_routes
from app.routes import fornecedores_routes
from app.routes import clientes_routes
from app.routes import status_routes
from app.routes import projetos_routes
from app.routes import materiais_projeto_routes
from app.routes import orcamentos_routes

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Carregar configurações padrão
    app.config.from_object('config')

    # Carregar configurações específicas da instância (como caminho do banco)
    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)

    # Importar e registrar rotas
    from app.routes import auth_routes, main_routes
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

    return app
