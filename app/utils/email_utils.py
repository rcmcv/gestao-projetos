# Arquivo: app/utils/email_utils.py
import string
import random
from flask_mail import Mail, Message
from flask import current_app
from app.models.models import Usuario
from app.extensions import db
from werkzeug.security import generate_password_hash

mail = Mail()  # Instância do Flask-Mail

# ✅ Função para gerar uma senha aleatória simples
def gerar_nova_senha(tamanho=8):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

# ✅ Enviar e-mail com nova senha e atualizar no banco
def enviar_nova_senha(email):
    # Gera nova senha aleatória
    nova_senha = gerar_nova_senha()

    # Busca o usuário pelo e-mail
    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        return None

    # Atualiza a senha no banco (com hash)
    usuario.senha = generate_password_hash(nova_senha)
    db.session.commit()

    # Cria a mensagem de e-mail
    assunto = "Recuperação de Senha - Gestão de Projetos"
    corpo = f"""
Olá {usuario.nome},

Conforme solicitado, sua nova senha de acesso é: {nova_senha}

Recomendamos que você faça login e troque sua senha em seguida.

Atenciosamente,
Sistema de Gestão de Projetos
"""

    # Envia o e-mail
    with current_app.app_context():
        msg = Message(subject=assunto, recipients=[email], body=corpo)
        mail.send(msg)

    return nova_senha  # Pode ser útil para testes
