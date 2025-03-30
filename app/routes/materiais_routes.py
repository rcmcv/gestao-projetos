# Arquivo: app/routes/materiais_routes.py
from flask import Blueprint, request
from app.extensions import db
from app.models.models import Material, TipoMaterial, UnidadeMedida
from app.utils.resposta import resposta_json
from .web_routes import web

# web = Blueprint('materiais', __name__)

# ✅ Listar materiais com nomes de tipo e unidade
@web.route('/materiais', methods=['GET'])
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
@web.route('/materiais', methods=['POST'])
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
@web.route('/materiais/<int:id>', methods=['PUT'])
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
@web.route('/materiais/<int:id>', methods=['DELETE'])
def excluir_material(id):
    material = Material.query.get(id)
    if not material:
        return resposta_json({'erro': 'Material não encontrado.'}, 404)

    db.session.delete(material)
    db.session.commit()
    return resposta_json({'mensagem': f'Material {material.nome} excluído com sucesso.'})

# ✅ Rota para buscar materiais por tipo de material
@web.route('/materiais/buscar', methods=['GET'])
def buscar_materiais_por_tipo_e_nome():
    tipo_id = request.args.get('tipo_id')
    busca = request.args.get('q', '')  # texto digitado pelo usuário

    if not tipo_id:
        return resposta_json({'erro': 'tipo_id é obrigatório.'}, 400)

    # Filtra materiais pelo tipo e nome que contenha o texto digitado (case insensitive)
    materiais = Material.query.filter(
        Material.tipo_id == tipo_id,
        Material.nome.ilike(f"%{busca}%")
    ).all()

    return resposta_json([
        {'id': m.id, 'nome': m.nome} for m in materiais
    ])
