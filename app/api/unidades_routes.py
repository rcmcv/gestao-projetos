# Arquivo: app/api/unidades_routes.py
from flask import Blueprint, request
from app import db
from app.models.models import UnidadeMedida
from app.utils.resposta import resposta_json

bp = Blueprint('api_unidades', __name__, url_prefix='/api/unidades')


# ✅ Listar todas as unidades
@bp.route('/', methods=['GET'])
def listar_unidades():
    unidades = UnidadeMedida.query.all()
    lista = [{'id': u.id, 'nome': u.nome, 'sigla': u.sigla} for u in unidades]
    return resposta_json(lista)


# ✅ Criar nova unidade
@bp.route('/', methods=['POST'])
def criar_unidade():
    dados = request.json
    unidade = UnidadeMedida(
        nome=dados.get('nome'),
        sigla=dados.get('sigla')
    )
    db.session.add(unidade)
    db.session.commit()
    return resposta_json({'mensagem': 'Unidade criada com sucesso.'}, 201)


# ✅ Atualizar unidade
@bp.route('/<int:id>', methods=['PUT'])
def atualizar_unidade(id):
    unidade = UnidadeMedida.query.get(id)
    if not unidade:
        return resposta_json({'erro': 'Unidade não encontrada.'}, 404)

    unidade.nome = request.json.get('nome')
    unidade.sigla = request.json.get('sigla')

    db.session.commit()
    return resposta_json({'mensagem': 'Unidade atualizada com sucesso.'})


# ✅ Excluir unidade
@bp.route('/<int:id>', methods=['DELETE'])
def excluir_unidade(id):
    unidade = UnidadeMedida.query.get(id)
    if not unidade:
        return resposta_json({'erro': 'Unidade não encontrada.'}, 404)

    db.session.delete(unidade)
    db.session.commit()
    return resposta_json({'mensagem': 'Unidade excluída com sucesso.'})
