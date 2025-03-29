# Arquivo: app/api/fornecedores_routes.py
from flask import Blueprint, request
from app import db
from app.models.models import Fornecedor
from app.utils.resposta import resposta_json

bp = Blueprint('api_fornecedores', __name__, url_prefix='/api/fornecedores')


# ✅ Listar todos os fornecedores
@bp.route('/', methods=['GET'])
def listar_fornecedores():
    fornecedores = Fornecedor.query.all()
    lista = [{
        'id': f.id,
        'nome': f.nome,
        'cnpj': f.cnpj,
        'email': f.email,
        'telefone': f.telefone,
        'contato': f.contato,
        'tipo_material_id': f.tipo_material_id
    } for f in fornecedores]
    return resposta_json(lista)


# ✅ Criar novo fornecedor
@bp.route('/', methods=['POST'])
def criar_fornecedor():
    dados = request.json
    fornecedor = Fornecedor(
        nome=dados.get('nome'),
        cnpj=dados.get('cnpj'),
        email=dados.get('email'),
        telefone=dados.get('telefone'),
        contato=dados.get('contato'),
        tipo_material_id=dados.get('tipo_material_id')
    )
    db.session.add(fornecedor)
    db.session.commit()
    return resposta_json({'mensagem': 'Fornecedor criado com sucesso.'}, 201)


# ✅ Atualizar fornecedor
@bp.route('/<int:id>', methods=['PUT'])
def atualizar_fornecedor(id):
    fornecedor = Fornecedor.query.get(id)
    if not fornecedor:
        return resposta_json({'erro': 'Fornecedor não encontrado.'}, 404)

    dados = request.json
    fornecedor.nome = dados.get('nome')
    fornecedor.cnpj = dados.get('cnpj')
    fornecedor.email = dados.get('email')
    fornecedor.telefone = dados.get('telefone')
    fornecedor.contato = dados.get('contato')
    fornecedor.tipo_material_id = dados.get('tipo_material_id')

    db.session.commit()
    return resposta_json({'mensagem': 'Fornecedor atualizado com sucesso.'})


# ✅ Excluir fornecedor
@bp.route('/<int:id>', methods=['DELETE'])
def excluir_fornecedor(id):
    fornecedor = Fornecedor.query.get(id)
    if not fornecedor:
        return resposta_json({'erro': 'Fornecedor não encontrado.'}, 404)

    db.session.delete(fornecedor)
    db.session.commit()
    return resposta_json({'mensagem': 'Fornecedor excluído com sucesso.'})
