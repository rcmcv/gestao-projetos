# Arquivo: app/routes/unidades_routes.py
from flask import Blueprint, request
from app.extensions import db
from app.models.models import UnidadeMedida
from app.utils.resposta import resposta_json

# Criação do Blueprint para rotas de Unidade de Medida
bp = Blueprint('unidades', __name__)

# ✅ Listar todas as unidades de medida
@bp.route('/unidades-medida', methods=['GET'])
def listar_unidades():
    unidades = UnidadeMedida.query.all()
    return resposta_json([
        {'id': u.id, 'sigla': u.sigla, 'descricao': u.descricao} for u in unidades
    ])

# ✅ Adicionar nova unidade de medida
@bp.route('/unidades-medida', methods=['POST'])
def adicionar_unidade():
    dados = request.json
    sigla = dados.get('sigla')
    descricao = dados.get('descricao')

    if not sigla or not descricao:
        return resposta_json({'erro': 'Informe a sigla e a descrição.'}, 400)

    unidade = UnidadeMedida(sigla=sigla, descricao=descricao)
    db.session.add(unidade)
    db.session.commit()
    return resposta_json({'mensagem': 'Unidade de medida cadastrada com sucesso!'})

# ✅ Editar unidade de medida
@bp.route('/unidades-medida/<int:id>', methods=['PUT'])
def editar_unidade(id):
    unidade = UnidadeMedida.query.get(id)
    if not unidade:
        return resposta_json({'erro': 'Unidade de medida não encontrada.'}, 404)

    unidade.sigla = request.json.get('sigla', unidade.sigla)
    unidade.descricao = request.json.get('descricao', unidade.descricao)
    db.session.commit()
    return resposta_json({'mensagem': 'Unidade de medida atualizada com sucesso.'})

# ✅ Excluir unidade de medida
@bp.route('/unidades-medida/<int:id>', methods=['DELETE'])
def excluir_unidade(id):
    unidade = UnidadeMedida.query.get(id)
    if not unidade:
        return resposta_json({'erro': 'Unidade de medida não encontrada.'}, 404)

    db.session.delete(unidade)
    db.session.commit()
    return resposta_json({'mensagem': f'Unidade {unidade.sigla} excluída com sucesso.'})
