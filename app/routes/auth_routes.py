# Arquivo: app/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from flask import session
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from app import db
from app.models.models import Usuario
from app.utils.resposta import resposta_json

bp = Blueprint('auth', __name__)

# ✅ Listar todos os usuários
@bp.route('/usuarios')
def listar_usuarios():
    usuarios = Usuario.query.all()
    lista = []
    for u in usuarios:
        lista.append({
            'id': u.id,
            'nome': u.nome,
            'email': u.email,
            'senha': u.senha,
            'permissao': u.permissao
        })
    return jsonify(lista)


# ✅ Adicionar novo usuário
@bp.route('/usuarios/novo', methods=['POST'])
def adicionar_usuario():
    dados = request.json
    senha_criptografada = generate_password_hash(dados['senha'])

    novo = Usuario(
        nome=dados['nome'],
        email=dados['email'],
        senha=senha_criptografada,  # Salva a senha criptografada em hash!
        permissao=dados['permissao']
    )
    db.session.add(novo)
    db.session.commit()
    return resposta_json({'mensagem': 'Usuário cadastrado com sucesso!'})


# ✅ Login de usuários
@bp.route('/login', methods=['POST'])
def realizar_login():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')

    usuario = Usuario.query.filter_by(email=email).first()

    if usuario and check_password_hash(usuario.senha, senha):
        session['usuario_id'] = usuario.id
        session['usuario_nome'] = usuario.nome
        session['usuario_permissao'] = usuario.permissao
        return resposta_json({'mensagem': f'Bem-vindo(a), {usuario.nome}!', 'permissao': usuario.permissao})
    else:
        return resposta_json({'erro': 'Email ou senha inválidos'}), 401


#✅ Logout de usuários
@bp.route('/api/logout')
def logout():
    session.clear()
    return resposta_json({'mensagem': 'Logout realizado com sucesso.'})


# ✅ Área restrita
@bp.route('/admin-area')
def admin_area():
    if 'usuario_id' not in session:
        return resposta_json({'erro': 'Acesso não autorizado. Faça login primeiro.'}), 401

    if session.get('usuario_permissao') != 'admin':
        return resposta_json({'erro': 'Acesso restrito para administradores.'}), 403

    return resposta_json({'mensagem': f'Acesso liberado para administrador {session.get("usuario_nome")}'})


# 🔁 Atualizar um usuário existente
@bp.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return resposta_json({'erro': 'Usuário não encontrado.'}, 404)

    dados = request.json
    usuario.nome = dados.get('nome', usuario.nome)
    usuario.email = dados.get('email', usuario.email)
    usuario.permissao = dados.get('permissao', usuario.permissao)

    if 'senha' in dados:
        from werkzeug.security import generate_password_hash
        usuario.senha = generate_password_hash(dados['senha'])

    db.session.commit()
    return resposta_json({'mensagem': 'Usuário atualizado com sucesso.'})


# ❌ Excluir um usuário
@bp.route('/usuarios/<int:id>', methods=['DELETE'])
def excluir_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return resposta_json({'erro': 'Usuário não encontrado.'}, 404)

    db.session.delete(usuario)
    db.session.commit()
    return resposta_json({'mensagem': f'Usuário {usuario.nome} excluído com sucesso.'})


# 🔍 Buscar usuário individual
@bp.route('/usuarios/<int:id>')
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


# 🔁 Recuperar senha de usuário existente
@bp.route('/api/recuperar-senha', methods=['POST'])
def recuperar_senha():
    dados = request.json
    email = dados.get('email')
    nova_senha = dados.get('nova_senha')

    if not email or not nova_senha:
        return resposta_json({'erro': 'Informe o e-mail e a nova senha.'}, 400)

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return resposta_json({'erro': 'E-mail não encontrado.'}, 404)

    from werkzeug.security import generate_password_hash
    usuario.senha = generate_password_hash(nova_senha)
    db.session.commit()

    return resposta_json({'mensagem': 'Senha redefinida com sucesso!'})
