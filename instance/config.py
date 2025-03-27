# Arquivo: instance/config.py
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, 'gestao.db')

SECRET_KEY = 'minha_chave_secreta'  # depois podemos melhorar com .env
SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
