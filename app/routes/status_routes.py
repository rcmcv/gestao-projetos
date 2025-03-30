# Arquivo: app/routes/status_routes.py
# Importações necessárias
from flask import Blueprint, request
from app.extensions import db
from app.models.models import Status
from app.utils.resposta import resposta_json
from .web_routes import web

# Blueprint para rotas de status
# web = Blueprint('status', __name__)

# ✅ Listar todos os status
@web.route('/status', methods=['GET'])
def listar_status():
    status = Status.query.all()
    return resposta_json([
        {'id': s.id, 'nome': s.nome, 'ativo': s.ativo} for s in status
    ])

# ✅ Adicionar novo status
@web.route('/status', methods=['POST'])
def adicionar_status():
    dados = request.json
    nome = dados.get('nome')
    if not nome:
        return resposta_json({'erro': 'Informe o nome do status.'}, 400)

    status = Status(nome=nome)
    db.session.add(status)
    db.session.commit()
    return resposta_json({'mensagem': 'Status cadastrado com sucesso!'})

# ✅ Editar status
@web.route('/status/<int:id>', methods=['PUT'])
def editar_status(id):
    status = Status.query.get(id)
    if not status:
        return resposta_json({'erro': 'Status não encontrado.'}, 404)

    dados = request.json
    status.nome = dados.get('nome', status.nome)
    status.ativo = dados.get('ativo', status.ativo)
    db.session.commit()
    return resposta_json({'mensagem': 'Status atualizado com sucesso.'})

# ✅ Excluir status
@web.route('/status/<int:id>', methods=['DELETE'])
def excluir_status(id):
    status = Status.query.get(id)
    if not status:
        return resposta_json({'erro': 'Status não encontrado.'}, 404)

    db.session.delete(status)
    db.session.commit()
    return resposta_json({'mensagem': f'Status {status.nome} excluído com sucesso.'})
