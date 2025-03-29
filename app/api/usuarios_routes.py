# app/api/usuarios_routes.py
from flask import Blueprint, request
from app.models.models import Usuario
from app.extensions import db
from app.utils.resposta import resposta_json
from werkzeug.security import generate_password_hash

# ✅ Blueprint da API de usuários com prefixo '/api/usuarios'
bp = Blueprint('usuarios_api', __name__, url_prefix='/api/usuarios')

# 🔍 Listar todos os usuários
@bp.route('/', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return resposta_json([{
        'id': u.id,
        'nome': u.nome,
        'email': u.email,
        'permissao': u.permissao
    } for u in usuarios])

# ➕ Criar novo usuário
@bp.route('/novo', methods=['POST'])
def criar_usuario():
    dados = request.json
    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')
    permissao = dados.get('permissao')

    if not nome or not email or not senha:
        return resposta_json({'erro': 'Preencha nome, e-mail e senha.'}, 400)

    senha_hash = generate_password_hash(senha)

    novo = Usuario(nome=nome, email=email, senha=senha_hash, permissao=permissao)
    db.session.add(novo)
    db.session.commit()

    return resposta_json({'mensagem': 'Usuário criado com sucesso.'}, 201)

# 🔄 Atualizar usuário existente
@bp.route('/<int:id>', methods=['PUT'])
def editar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return resposta_json({'erro': 'Usuário não encontrado.'}, 404)

    dados = request.json
    usuario.nome = dados.get('nome', usuario.nome)
    usuario.email = dados.get('email', usuario.email)
    usuario.permissao = dados.get('permissao', usuario.permissao)

    db.session.commit()
    return resposta_json({'mensagem': 'Usuário atualizado com sucesso.'})

# ❌ Excluir usuário
@bp.route('/<int:id>', methods=['DELETE'])
def excluir_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return resposta_json({'erro': 'Usuário não encontrado.'}, 404)

    db.session.delete(usuario)
    db.session.commit()
    return resposta_json({'mensagem': 'Usuário excluído com sucesso.'})

# 🔍 Buscar um usuário individual
@bp.route('/<int:id>', methods=['GET'])
def buscar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return resposta_json({'erro': 'Usuário não encontrado.'}, 404)

    return resposta_json({
        'id': usuario.id,
        'nome': usuario.nome,
        'email': usuario.email,
        'permissao': usuario.permissao
    })
