# Arquivo: app/api/tipos_routes.py
from flask import Blueprint, request
from app import db
from app.models.models import TipoMaterial
from app.utils.resposta import resposta_json

bp = Blueprint('api_tipos', __name__, url_prefix='/api/tipos')


# ✅ Listar todos os tipos
@bp.route('/', methods=['GET'])
def listar_tipos():
    tipos = TipoMaterial.query.all()
    lista = [{'id': t.id, 'nome': t.nome} for t in tipos]
    return resposta_json(lista)


# ✅ Criar novo tipo
@bp.route('/', methods=['POST'])
def criar_tipo():
    dados = request.json
    tipo = TipoMaterial(nome=dados.get('nome'))
    db.session.add(tipo)
    db.session.commit()
    return resposta_json({'mensagem': 'Tipo criado com sucesso.'}, 201)


# ✅ Atualizar tipo
@bp.route('/<int:id>', methods=['PUT'])
def atualizar_tipo(id):
    tipo = TipoMaterial.query.get(id)
    if not tipo:
        return resposta_json({'erro': 'Tipo não encontrado.'}, 404)

    tipo.nome = request.json.get('nome')
    db.session.commit()
    return resposta_json({'mensagem': 'Tipo atualizado com sucesso.'})


# ✅ Excluir tipo
@bp.route('/<int:id>', methods=['DELETE'])
def excluir_tipo(id):
    tipo = TipoMaterial.query.get(id)
    if not tipo:
        return resposta_json({'erro': 'Tipo não encontrado.'}, 404)

    db.session.delete(tipo)
    db.session.commit()
    return resposta_json({'mensagem': 'Tipo excluído com sucesso.'})
