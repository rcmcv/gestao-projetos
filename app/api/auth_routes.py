# app/api/auth_routes.py
from flask import Blueprint, request, session
from app.models.models import Usuario
from app.extensions import db
from app.utils.resposta import resposta_json
from werkzeug.security import check_password_hash, generate_password_hash

# ✅ Blueprint da API de autenticação com prefixo '/api'
bp = Blueprint('auth_api', __name__, url_prefix='/api')

# 🔐 Login de usuário (API)
@bp.route('/login', methods=['POST'])
def login_api():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')

    if not email or not senha:
        return resposta_json({'erro': 'Informe e-mail e senha.'}, 400)

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not check_password_hash(usuario.senha, senha):
        return resposta_json({'erro': 'Credenciais inválidas.'}, 401)

    # Armazena dados da sessão (caso queira reaproveitar)
    session['usuario_id'] = usuario.id
    session['usuario_nome'] = usuario.nome
    session['permissao'] = usuario.permissao

    return resposta_json({
        'mensagem': 'Login realizado com sucesso.',
        'usuario': {
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'permissao': usuario.permissao
        }
    })

# 🚪 Logout do usuário (API)
@bp.route('/logout', methods=['POST'])
def logout_api():
    session.clear()
    return resposta_json({'mensagem': 'Logout realizado com sucesso.'})

# 🔁 Redefinir senha via API (requer e-mail e nova senha)
@bp.route('/recuperar-senha', methods=['POST'])
def recuperar_senha_api():
    dados = request.json
    email = dados.get('email')
    nova_senha = dados.get('nova_senha')

    if not email or not nova_senha:
        return resposta_json({'erro': 'Informe o e-mail e a nova senha.'}, 400)

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        return resposta_json({'erro': 'E-mail não encontrado.'}, 404)

    usuario.senha = generate_password_hash(nova_senha)
    db.session.commit()

    return resposta_json({'mensagem': 'Senha redefinida com sucesso!'})


# ✅ Rota protegida para administradores (área restrita via API)
@bp.route('/admin-area', methods=['GET'])
def admin_area():
    if 'usuario_id' not in session:
        return resposta_json({'erro': 'Acesso não autorizado. Faça login primeiro.'}), 401

    if session.get('permissao') != 'admin':
        return resposta_json({'erro': 'Acesso restrito para administradores.'}), 403

    return resposta_json({
        'mensagem': f'Acesso liberado para administrador {session.get("usuario_nome")}'
    })
