# Arquivo: app/routes/materiais_routes.py
from flask import Blueprint, request
from app.extensions import db
from app.models.models import Material, TipoMaterial, UnidadeMedida
from app.utils.resposta import resposta_json

bp = Blueprint('materiais', __name__)

# ✅ Listar materiais com nomes de tipo e unidade
@bp.route('/materiais', methods=['GET'])
def listar_materiais():
    materiais = Material.query.all()
    return resposta_json([
        {
            'id': m.id,
            'nome': m.nome,
            'tipo': m.tipo.nome,
            'unidade': m.unidade.sigla
        } for m in materiais
    ])

# ✅ Adicionar novo material
@bp.route('/materiais', methods=['POST'])
def adicionar_material():
    dados = request.json
    nome = dados.get('nome')
    tipo_id = dados.get('tipo_id')
    unidade_id = dados.get('unidade_id')

    if not nome or not tipo_id or not unidade_id:
        return resposta_json({'erro': 'Informe nome, tipo_id e unidade_id.'}, 400)

    material = Material(nome=nome, tipo_id=tipo_id, unidade_id=unidade_id)
    db.session.add(material)
    db.session.commit()
    return resposta_json({'mensagem': 'Material cadastrado com sucesso!'})

# ✅ Editar material
@bp.route('/materiais/<int:id>', methods=['PUT'])
def editar_material(id):
    material = Material.query.get(id)
    if not material:
        return resposta_json({'erro': 'Material não encontrado.'}, 404)

    dados = request.json
    material.nome = dados.get('nome', material.nome)
    material.tipo_id = dados.get('tipo_id', material.tipo_id)
    material.unidade_id = dados.get('unidade_id', material.unidade_id)

    db.session.commit()
    return resposta_json({'mensagem': 'Material atualizado com sucesso.'})

# ✅ Excluir material
@bp.route('/materiais/<int:id>', methods=['DELETE'])
def excluir_material(id):
    material = Material.query.get(id)
    if not material:
        return resposta_json({'erro': 'Material não encontrado.'}, 404)

    db.session.delete(material)
    db.session.commit()
    return resposta_json({'mensagem': f'Material {material.nome} excluído com sucesso.'})
