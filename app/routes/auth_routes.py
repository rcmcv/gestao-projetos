# Arquivo: app/routes/auth_routes.py
# Rotas da interface web relacionadas à autenticação: login, logout e recuperação de senha

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.models import Usuario
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from app.utils.email_utils import enviar_nova_senha
from app.utils.resposta import resposta_json
from .web_routes import web  # Usamos o blueprint "web" unificado para todas as rotas HTML

# ✅ Tela de login – exibe o formulário e processa autenticação
@web.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtém os dados do formulário
        email = request.form.get('email')
        senha = request.form.get('senha')

        # Busca o usuário pelo email
        usuario = Usuario.query.filter_by(email=email).first()

        # Verifica se o usuário existe e se a senha está correta
        if usuario and check_password_hash(usuario.senha, senha):
            # Login OK → salva os dados do usuário na sessão
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            session['usuario_email'] = usuario.email
            session['usuario_permissao'] = usuario.permissao

            # Exibe mensagem de boas-vindas
            # flash(f'Bem-vindo, {usuario.nome}!', 'success')

            # Redireciona para a página inicial do sistema
            return redirect(url_for('web.pagina_inicial'))
        else:
            # Email ou senha incorretos → exibe mensagem de erro
            erro = 'Email ou senha inválidos.'
            return render_template('login.html', erro=erro)

    # Requisição GET → limpa mensagens antigas (ex: logout) da sessão
    session.pop('_flashes', None)

    # Renderiza o formulário de login
    return render_template('login.html')

# ✅ Logout – limpa a sessão do usuário e redireciona para login
@web.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Logout realizado com sucesso.', 'info')
    return redirect(url_for('web.login'))

# ✅ Rota para recuperação de senha
@web.route('/recuperar-senha', methods=['GET', 'POST'], endpoint='recuperar_senha')
def recuperar_senha_form():
    if request.method == 'POST':
        email = request.form.get('email')

        if not email:
            flash('Por favor, informe um e-mail válido.', 'warning')
            return redirect(url_for('web.recuperar_senha'))

        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario:
            flash('E-mail não encontrado no sistema.', 'danger')
            return redirect(url_for('web.recuperar_senha'))

        try:
            enviar_nova_senha(email)
            flash('Nova senha enviada para seu e-mail.', 'success')
        except Exception as e:
            flash('Erro ao enviar o e-mail. Tente novamente mais tarde.', 'danger')
            print(f"[ERRO] Falha no envio do e-mail: {e}")  # Para log em terminal

        return redirect(url_for('web.login'))

    return render_template('recuperar_senha.html')

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
