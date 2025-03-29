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


# ✅ Rota para exibir o formulário de recuperação de senha e tratar o envio
@bp.route('/recuperar-senha', methods=['GET', 'POST'])
def recuperar_senha():
    mensagem = None  # Variável para exibir feedback ao usuário (erro ou sucesso)

    # Se o formulário for enviado (método POST)
    if request.method == 'POST':
        email = request.form.get('email')  # Captura o e-mail digitado pelo usuário

        # Busca o usuário no banco com base no e-mail informado
        usuario = Usuario.query.filter_by(email=email).first()

        # Se encontrou o usuário no banco
        if usuario:
            # Importa a função de utilitário para envio de nova senha
            from app.utils.email_utils import enviar_nova_senha

            # Gera nova senha, envia por e-mail e atualiza no banco
            nova_senha = enviar_nova_senha(usuario.email)

            # Define mensagem de sucesso
            mensagem = 'Nova senha enviada para o e-mail informado.'
        else:
            # Define mensagem de erro se o e-mail não for encontrado
            mensagem = 'E-mail não encontrado.'

    # Renderiza a página HTML com o formulário e, se houver, exibe a mensagem
    return render_template('recuperar_senha.html', mensagem=mensagem)
