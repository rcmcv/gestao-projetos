# Arquivo: app/routes/web_routes.py
# Descrição: Rotas da interface web (HTML), incluindo login, dashboard, logout e recuperação de senha.

from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.models import Usuario
from werkzeug.security import check_password_hash
from app.utils.email_utils import enviar_nova_senha  # Utilitário para envio de nova senha

# 🔹 Cria o blueprint para as rotas web
web = Blueprint('web', __name__)

# ✅ Rota do Dashboard (página principal após login)
@web.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect(url_for('web.login'))  # Redireciona para login se não estiver logado
    return render_template('dashboard.html', nome=session.get('usuario_nome'))
