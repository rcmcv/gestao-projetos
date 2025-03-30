# ✅ Arquivo: criar_banco.py
import os
from app import create_app, db
from app.models import models

# 🔹 Garante que a pasta instance exista
os.makedirs("instance", exist_ok=True)

# 🔹 Cria a app e contexto
app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Banco de dados criado com sucesso!")
