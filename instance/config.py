# Arquivo: instance/config.py
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, 'gestao.db')

SECRET_KEY = 'chave-secreta-supersegura'  # Trocar por algo mais forte depois
SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
