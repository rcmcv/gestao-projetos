# Arquivo: app/api/status_routes.py
from flask import Blueprint, request
from app import db
from app.models.models import Status
from app.utils.resposta import resposta_json

bp = Blueprint('api_status', __name__, url_prefix='/api/status')


# ✅ Listar todos os status
@bp.route('/', methods=['GET'])
def listar_status():
    status = Status.query.all()
    lista = [{'id': s.id, 'nome': s.nome} for s in status]
    return resposta_json(lista)


# ✅ Criar novo status
@bp.route('/', methods=['POST'])
def criar_status():
    dados = request.json
    novo_status = Status(nome=dados.get('nome'))
    db.session.add(novo_status)
    db.session.commit()
    return resposta_json({'mensagem': 'Status criado com sucesso.'}, 201)


# ✅ Atualizar status
@bp.route('/<int:id>', methods=['PUT'])
def atualizar_status(id):
    status = Status.query.get(id)
    if not status:
        return resposta_json({'erro': 'Status não encontrado.'}, 404)

    status.nome = request.json.get('nome')
    db.session.commit()
    return resposta_json({'mensagem': 'Status atualizado com sucesso.'})


# ✅ Excluir status
@bp.route('/<int:id>', methods=['DELETE'])
def excluir_status(id):
    status = Status.query.get(id)
    if not status:
        return resposta_json({'erro': 'Status não encontrado.'}, 404)

    db.session.delete(status)
    db.session.commit()
    return resposta_json({'mensagem': 'Status excluído com sucesso.'})
