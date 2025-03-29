# Arquivo: app/api/materiais_projetos_routes.py
from flask import Blueprint, request
from app.extensions import db
from app.models.models import MaterialProjeto, Material
from app.utils.resposta import resposta_json

# ✅ Blueprint da API com prefixo '/api'
bp = Blueprint('materiais_projeto_api', __name__, url_prefix='/api')

# ✅ Listar todos os materiais de um projeto
@bp.route('/projetos/<int:projeto_id>/materiais', methods=['GET'])
def listar_materiais_do_projeto(projeto_id):
    materiais = MaterialProjeto.query.filter_by(projeto_id=projeto_id).all()

    return resposta_json([
        {
            'id': m.id,
            'material_id': m.material_id,
            'material_nome': m.material.nome,
            'tipo_material': m.tipo.nome if m.tipo else None,
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

    # Busca o material para verificar se existe
    material = Material.query.get(material_id)
    if not material:
        return resposta_json({'erro': 'Material não encontrado.'}, 404)

    # Cria associação do material com o projeto, incluindo tipo_id
    associacao = MaterialProjeto(
        projeto_id=projeto_id,
        material_id=material_id,
        tipo_id=material.tipo_id,
        quantidade=quantidade
    )

    db.session.add(associacao)
    db.session.commit()
    return resposta_json({'mensagem': 'Material adicionado ao projeto com sucesso.'})

# ✅ Editar a quantidade de um material em um projeto
@bp.route('/materiais-projeto/<int:id>', methods=['PUT'])
def editar_material_projeto(id):
    item = MaterialProjeto.query.get(id)
    if not item:
        return resposta_json({'erro': 'Item não encontrado.'}, 404)

    nova_qtd = request.json.get('quantidade')
    if not nova_qtd:
        return resposta_json({'erro': 'Informe a nova quantidade.'}, 400)

    item.quantidade = nova_qtd
    db.session.commit()
    return resposta_json({'mensagem': 'Quantidade atualizada com sucesso.'})

# ✅ Remover material do projeto (com verificação de vínculos com orçamentos)
@bp.route('/materiais-projeto/<int:id>', methods=['DELETE'])
def excluir_material_projeto(id):
    # Busca o item pelo ID
    item = MaterialProjeto.query.get(id)

    if not item:
        return resposta_json({'erro': 'Item não encontrado.'}, 404)

    # Verifica se existem orçamentos vinculados a este material
    if item.orcamentos:  # Lista de orçamentos relacionados
        return resposta_json({
            'erro': 'Este material possui orçamentos vinculados e não pode ser excluído.'
        }, 400)

    # Se não houver vínculos, permite a exclusão
    db.session.delete(item)
    db.session.commit()

    return resposta_json({'mensagem': 'Material removido do projeto com sucesso.'})
