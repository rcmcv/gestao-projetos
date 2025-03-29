# Arquivo: app/api/materiais_routes.py
from flask import Blueprint, request
from app import db
from app.models.models import Material
from app.utils.resposta import resposta_json

bp = Blueprint('api_materiais', __name__, url_prefix='/api/materiais')


# ✅ Listar todos os materiais
@bp.route('/', methods=['GET'])
def listar_materiais():
    materiais = Material.query.all()
    lista = [{
        'id': m.id,
        'nome': m.nome,
        'descricao': m.descricao,
        'tipo_material_id': m.tipo_material_id,
        'unidade_id': m.unidade_id
    } for m in materiais]
    return resposta_json(lista)


# ✅ Criar novo material
@bp.route('/', methods=['POST'])
def criar_material():
    dados = request.json
    material = Material(
        nome=dados.get('nome'),
        descricao=dados.get('descricao'),
        tipo_material_id=dados.get('tipo_material_id'),
        unidade_id=dados.get('unidade_id')
    )
    db.session.add(material)
    db.session.commit()
    return resposta_json({'mensagem': 'Material criado com sucesso.'}, 201)


# ✅ Atualizar material
@bp.route('/<int:id>', methods=['PUT'])
def atualizar_material(id):
    material = Material.query.get(id)
    if not material:
        return resposta_json({'erro': 'Material não encontrado.'}, 404)

    dados = request.json
    material.nome = dados.get('nome')
    material.descricao = dados.get('descricao')
    material.tipo_material_id = dados.get('tipo_material_id')
    material.unidade_id = dados.get('unidade_id')

    db.session.commit()
    return resposta_json({'mensagem': 'Material atualizado com sucesso.'})


# ✅ Excluir material
@bp.route('/<int:id>', methods=['DELETE'])
def excluir_material(id):
    material = Material.query.get(id)
    if not material:
        return resposta_json({'erro': 'Material não encontrado.'}, 404)

    db.session.delete(material)
    db.session.commit()
    return resposta_json({'mensagem': 'Material excluído com sucesso.'})
