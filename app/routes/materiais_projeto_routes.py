# Arquivo: app/routes/materiais_projeto_routes.py
# Importações necessárias
from flask import Blueprint, request
from app.extensions import db
from app.models.models import MaterialProjeto, Projeto, Material
from app.utils.resposta import resposta_json

bp = Blueprint('materiais_projeto', __name__)

# ✅ Listar materiais de um projeto específico
@bp.route('/projetos/<int:projeto_id>/materiais', methods=['GET'])
def listar_materiais_do_projeto(projeto_id):
    materiais = MaterialProjeto.query.filter_by(projeto_id=projeto_id).all()
    return resposta_json([
        {
            'id': m.id,
            'material_id': m.material_id,
            'material_nome': m.material.nome,
            'quantidade': m.quantidade
        } for m in materiais
    ])

# ✅ Adicionar material a um projeto
@bp.route('/projetos/<int:projeto_id>/materiais', methods=['POST'])
def adicionar_material_ao_projeto(projeto_id):
    dados = request.json
    material_id = dados.get('material_id')
    quantidade = dados.get('quantidade')

    if not material_id or not quantidade:
        return resposta_json({'erro': 'Informe material_id e quantidade.'}, 400)

    associacao = MaterialProjeto(
        projeto_id=projeto_id,
        material_id=material_id,
        quantidade=quantidade
    )

    db.session.add(associacao)
    db.session.commit()
    return resposta_json({'mensagem': 'Material adicionado ao projeto com sucesso.'})

# ✅ Editar quantidade de material em projeto
@bp.route('/materiais-projeto/<int:id>', methods=['PUT'])
def editar_material_projeto(id):
    item = MaterialProjeto.query.get(id)
    if not item:
        return resposta_json({'erro': 'Item não encontrado.'}, 404)

    item.quantidade = request.json.get('quantidade', item.quantidade)
    db.session.commit()
    return resposta_json({'mensagem': 'Quantidade atualizada com sucesso.'})

# ✅ Excluir material do projeto
@bp.route('/materiais-projeto/<int:id>', methods=['DELETE'])
def excluir_material_projeto(id):
    item = MaterialProjeto.query.get(id)
    if not item:
        return resposta_json({'erro': 'Item não encontrado.'}, 404)

    db.session.delete(item)
    db.session.commit()
    return resposta_json({'mensagem': 'Material removido do projeto com sucesso.'})
