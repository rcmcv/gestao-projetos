# Arquivo: app/__init__.py
from flask import Flask
from dotenv import load_dotenv
from .extensions import db, mail
from app.routes import web_routes
from app.api import registrar_rotas_api
from pathlib import Path
import os

# 🔹 Importa a classe Config com as variáveis da aplicação
from instance.config import Config

# 🔹 Cria a aplicação e define que ela pode carregar configs da pasta 'instance'
app = Flask(__name__, instance_relative_config=True)

# 🔹 Carrega todas as configurações da classe Config
app.config.from_object(Config)

# 🔹 Carrega o .env (caso ainda não tenha sido carregado)
load_dotenv()

def create_app():
    # 🔹 Corrige o caminho do banco se for relativo
    raw_db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "sqlite:///instance/gestao.db")
    if raw_db_uri.startswith("sqlite:///instance"):
        db_path = os.path.join(app.instance_path, 'gestao.db')
        db_uri = f"sqlite:///{db_path}"
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    else:
        db_uri = raw_db_uri

    # 🔹 Inicializa as extensões
    db.init_app(app)
    mail.init_app(app)

    # 🔹 Exibe o caminho real do banco para debug
    print("📁 Caminho final do banco:", db_uri)
    print("📧 Servidor de e-mail:", app.config.get("MAIL_SERVER"))

    # 🔹 Registra rotas web
    app.register_blueprint(web_routes)

    # 🔹 Registra rotas da API REST com prefixo /api
    registrar_rotas_api(app)

    return app
