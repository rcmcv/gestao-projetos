# Arquivo: app/routes/web_routes.py
# Importações necessárias
from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.models import Usuario
from werkzeug.security import check_password_hash

bp = Blueprint('web', __name__)

# ✅ Rota para login
@bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            session['permissao'] = usuario.permissao
            return redirect(url_for('web.dashboard'))
        else:
            return render_template('login.html', erro='Credenciais inválidas.')

    return render_template('login.html')  # ← aqui ele exibe o HTML

# ✅ Dashboard após login
@bp.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect(url_for('web.login'))
    return render_template('dashboard.html', nome=session['usuario_nome'])

# ✅ Logout
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('web.login'))
