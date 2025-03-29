# Arquivo: app/api/clientes_routes.py
from flask import Blueprint, request
from app import db
from app.models.models import Cliente
from app.utils.resposta import resposta_json

bp = Blueprint('api_clientes', __name__, url_prefix='/api/clientes')


# ✅ Listar todos os clientes
@bp.route('/', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    lista = [{'id': c.id, 'nome': c.nome, 'email': c.email, 'telefone': c.telefone} for c in clientes]
    return resposta_json(lista)


# ✅ Criar novo cliente
@bp.route('/', methods=['POST'])
def criar_cliente():
    dados = request.json
    cliente = Cliente(
        nome=dados.get('nome'),
        email=dados.get('email'),
        telefone=dados.get('telefone')
    )
    db.session.add(cliente)
    db.session.commit()
    return resposta_json({'mensagem': 'Cliente criado com sucesso.'}, 201)


# ✅ Atualizar cliente existente
@bp.route('/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return resposta_json({'erro': 'Cliente não encontrado.'}, 404)

    dados = request.json
    cliente.nome = dados.get('nome')
    cliente.email = dados.get('email')
    cliente.telefone = dados.get('telefone')

    db.session.commit()
    return resposta_json({'mensagem': 'Cliente atualizado com sucesso.'})


# ✅ Excluir cliente
@bp.route('/<int:id>', methods=['DELETE'])
def excluir_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return resposta_json({'erro': 'Cliente não encontrado.'}, 404)

    db.session.delete(cliente)
    db.session.commit()
    return resposta_json({'mensagem': 'Cliente excluído com sucesso.'})
