from flask import Flask
from dotenv import load_dotenv
from .extensions import db, mail
from app.routes import web_routes
from app.api import registrar_rotas_api
from pathlib import Path
import os

load_dotenv()

def create_app():
    # 🔹 Cria a aplicação e define que ela pode carregar configs da pasta 'instance'
    app = Flask(__name__, instance_relative_config=True)

    # 🔹 Lê o caminho do banco da variável de ambiente
    raw_db_uri = os.getenv("DATABASE_URI", "sqlite:///instance/gestao.db")

    # 🔹 Se o caminho for relativo (começa com "sqlite:///instance"), torna-o absoluto
    if raw_db_uri.startswith("sqlite:///instance"):
        db_path = os.path.join(app.instance_path, 'gestao.db')
        db_uri = f"sqlite:///{db_path}"
    else:
        db_uri = raw_db_uri

    # 🔹 Aplica a configuração no app
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-padrao-insegura')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 🔹 Inicializa as extensões
    db.init_app(app)
    mail.init_app(app)

    # 🔹 (Opcional) Exibe o caminho real do banco no terminal
    print("📁 Caminho final do banco:", db_uri)

    # 🔹 Registra rotas web
    app.register_blueprint(web_routes)

    # 📡 Registra rotas da API REST com prefixo /api
    registrar_rotas_api(app)

    # Retorna a instância da aplicação já configurada
    return app
