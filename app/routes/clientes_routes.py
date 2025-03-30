# Arquivo: app/routes/fornecedores_routes.py
# Importações necessárias
from flask import Blueprint, request
from app.extensions import db
from app.models.models import Cliente
from app.utils.resposta import resposta_json
from .web_routes import web

# Blueprint para rotas de clientes
# web = Blueprint('clientes', __name__)

# ✅ Listar clientes
@web.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return resposta_json([
        {
            'id': c.id,
            'nome': c.nome,
            'cpf_cnpj': c.cpf_cnpj,
            'email': c.email,
            'telefone': c.telefone,
            'contato': c.contato
        } for c in clientes
    ])

# ✅ Adicionar cliente
@web.route('/clientes', methods=['POST'])
def adicionar_cliente():
    dados = request.json

    # Verifica campos obrigatórios
    if not dados.get('nome') or not dados.get('cpf_cnpj'):
        return resposta_json({'erro': 'Campos obrigatórios: nome, cpf_cnpj'}, 400)

    cliente = Cliente(
        nome=dados['nome'],
        cpf_cnpj=dados['cpf_cnpj'],
        email=dados.get('email'),
        telefone=dados.get('telefone'),
        contato=dados.get('contato')
    )

    db.session.add(cliente)
    db.session.commit()
    return resposta_json({'mensagem': 'Cliente cadastrado com sucesso!'})

# ✅ Editar cliente
@web.route('/clientes/<int:id>', methods=['PUT'])
def editar_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return resposta_json({'erro': 'Cliente não encontrado.'}, 404)

    dados = request.json
    cliente.nome = dados.get('nome', cliente.nome)
    cliente.cpf_cnpj = dados.get('cpf_cnpj', cliente.cpf_cnpj)
    cliente.email = dados.get('email', cliente.email)
    cliente.telefone = dados.get('telefone', cliente.telefone)
    cliente.contato = dados.get('contato', cliente.contato)

    db.session.commit()
    return resposta_json({'mensagem': 'Cliente atualizado com sucesso.'})

# ✅ Excluir cliente
@web.route('/clientes/<int:id>', methods=['DELETE'])
def excluir_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return resposta_json({'erro': 'Cliente não encontrado.'}, 404)

    db.session.delete(cliente)
    db.session.commit()
    return resposta_json({'mensagem': f'Cliente {cliente.nome} excluído com sucesso.'})
