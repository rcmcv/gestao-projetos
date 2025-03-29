# Arquivo: app/api/__init__.py
# 📦 Este arquivo registra todos os blueprints da API com prefixo /api/

from flask import Blueprint

# Importação de todas as rotas da API
from .auth_routes import bp as auth_bp
from .usuarios_routes import bp as usuarios_bp
from .clientes_routes import bp as clientes_bp
from .fornecedores_routes import bp as fornecedores_bp
from .materiais_routes import bp as materiais_bp
from .tipos_routes import bp as tipos_bp
from .unidades_routes import bp as unidades_bp
from .status_routes import bp as status_bp
from .projetos_routes import bp as projetos_bp
from .materiais_projeto_routes import bp as materiais_projeto_bp
from .orcamentos_routes import bp as orcamentos_bp

def registrar_rotas_api(app):
    # 🔗 Registro dos blueprints com prefixo '/api'
    app.register_blueprint(auth_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(fornecedores_bp)
    app.register_blueprint(materiais_bp)
    app.register_blueprint(tipos_bp)
    app.register_blueprint(unidades_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(projetos_bp)
    app.register_blueprint(materiais_projeto_bp)
    app.register_blueprint(orcamentos_bp)
