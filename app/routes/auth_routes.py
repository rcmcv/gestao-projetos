# Arquivo: app/routes/auth_routes.py
# Rotas da interface web relacionadas à autenticação: login, logout e recuperação de senha

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, get_flashed_messages
from app.models.models import Usuario
from app import db
from app.forms.login_form import LoginForm
from app.forms.recuperar_senha_form import RecuperarSenhaForm
from werkzeug.security import check_password_hash, generate_password_hash
from app.utils.email_utils import enviar_nova_senha
from .web_routes import web  # Usamos o blueprint "web" unificado para todas as rotas HTML
#from app.utils.resposta import resposta_json

# ✅ Tela de login – exibe o formulário e processa autenticação
@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # Limpa mensagens antigas *apenas se* não houver mensagens recentes
    if request.method == 'GET' and not get_flashed_messages():
        session.pop('_flashes', None)


    if form.validate_on_submit():
        email = form.email.data.strip()
        senha = form.senha.data.strip()

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.senha, senha):
            # ✅ Login ok → salva dados na sessão
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            session['usuario_email'] = usuario.email
            session['usuario_permissao'] = usuario.permissao

            flash(f'Bem-vindo, {usuario.nome}!', 'success')
            return redirect(url_for('web.pagina_inicial'))
        else:
            flash('E-mail ou Senha inválidos.', 'danger')

    # Renderiza o formulário com o WTForms
    return render_template('login.html', form=form)

# ✅ Logout – limpa a sessão do usuário e redireciona para login
@web.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Logout realizado com sucesso.', 'info')
    return redirect(url_for('web.login'))

# ✅ Rota para recuperação de senha
@web.route('/recuperar-senha', methods=['GET', 'POST'], endpoint='recuperar_senha')
def recuperar_senha():
    form = RecuperarSenhaForm()

    if form.validate_on_submit():
        email = form.email.data.strip()
        usuario = Usuario.query.filter_by(email=email).first()

        # print("🔍 MÉTODO:", request.method)
        # print("✅ FORM VALIDO?", form.validate_on_submit())
        # print("🧩 E-MAIL:", form.email.data)

        # Chama a função de envio de nova senha (já implementada) se usuário existir
        if usuario:
            enviar_nova_senha(email)
            flash('Nova senha enviada para seu e-mail.', 'success')
            return redirect(url_for('web.login'))
        else:
            flash('E-mail não encontrado.', 'danger')  # Mostra erro claro

    return render_template('recuperar_senha.html', form=form)

# ✅ Redireciona rota raiz para a tela de login
@web.route('/')
def root():
    return redirect(url_for('web.login'))

# ✅ Redireciona rota para a tela inicial do sistema
@web.route('/index')
def pagina_inicial():
    if 'usuario_id' not in session:
        return redirect(url_for('web.login'))

    return render_template('index.html')
