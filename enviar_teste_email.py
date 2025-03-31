# Arquivo: enviar_teste_email.py

from flask import Flask
from flask_mail import Mail, Message
from dotenv import load_dotenv
from pathlib import Path
import os

# 🔹 Carrega .env corretamente
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

# 🔹 Cria a aplicação Flask
app = Flask(__name__)

# 🔹 Configurações do e-mail via os.getenv
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', os.getenv('MAIL_USERNAME'))

# 🔹 Inicializa o Flask-Mail
mail = Mail(app)

# 🔹 Teste de envio
with app.app_context():
    print(f"📬 MAIL_USERNAME: {app.config['MAIL_USERNAME']}")
    msg = Message(
        subject='✅ Teste de envio de e-mail',
        recipients=[app.config['MAIL_USERNAME']],  # Envia para si mesmo
        body='Este é um teste de envio de e-mail via Flask-Mail com .env funcionando corretamente!'
    )
    mail.send(msg)
    print("✅ E-mail enviado com sucesso!")
