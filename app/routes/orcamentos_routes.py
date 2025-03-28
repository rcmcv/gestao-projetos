# Arquivo: app/routes/orcamentos_routes.py
# Importações necessárias
from flask import Blueprint, request
from app.extensions import db
from app.models.models import Orcamento
from app.utils.resposta import resposta_json
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from app.models.models import MaterialProjeto, Material, Fornecedor

bp = Blueprint('orcamentos', __name__)

UPLOAD_DIR = 'app/uploads/orcamentos'

# ✅ Cadastrar orçamento sem upload de PDF
@bp.route('/orcamentos', methods=['POST'])
def cadastrar_orcamento():
    try:
        dados = request.json  # <- usa JSON ao invés de request.form

        orcamento = Orcamento(
            material_projeto_id=dados['material_projeto_id'],
            fornecedor_id=dados['fornecedor_id'],
            valor_unitario=dados['valor_unitario'],
            numero_orcamento=dados.get('numero_orcamento'),
            data_orcamento=datetime.strptime(dados['data_orcamento'], '%Y-%m-%d') if dados.get('data_orcamento') else None,
            arquivo_pdf=None  # ainda não usado nesse formato
        )

        db.session.add(orcamento)
        db.session.commit()
        return resposta_json({'mensagem': 'Orçamento cadastrado com sucesso.'})
    except Exception as e:
        return resposta_json({'erro': str(e)}, 400)


# ✅ Listar orçamentos de um projeto
@bp.route('/projetos/<int:projeto_id>/orcamentos', methods=['GET'])
def listar_orcamentos_por_projeto(projeto_id):
    orcamentos = (
        db.session.query(Orcamento)
        .join(MaterialProjeto)
        .filter(MaterialProjeto.projeto_id == projeto_id)
        .all()
    )

    return resposta_json([
        {
            'id': o.id,
            'material': o.material_projeto.material.nome,
            'fornecedor': o.fornecedor.nome,
            'valor_unitario': o.valor_unitario,
            'numero_orcamento': o.numero_orcamento,
            'data_orcamento': o.data_orcamento.strftime('%Y-%m-%d') if o.data_orcamento else None
        } for o in orcamentos
    ])


# ✅ Atualizar um orçamento
@bp.route('/orcamentos/<int:id>', methods=['PUT'])
def editar_orcamento(id):
    orcamento = Orcamento.query.get(id)
    if not orcamento:
        return resposta_json({'erro': 'Orçamento não encontrado.'}, 404)

    dados = request.json
    orcamento.fornecedor_id = dados.get('fornecedor_id', orcamento.fornecedor_id)
    orcamento.valor_unitario = dados.get('valor_unitario', orcamento.valor_unitario)
    orcamento.numero_orcamento = dados.get('numero_orcamento', orcamento.numero_orcamento)

    if dados.get('data_orcamento'):
        orcamento.data_orcamento = datetime.strptime(dados['data_orcamento'], '%Y-%m-%d')

    db.session.commit()
    return resposta_json({'mensagem': 'Orçamento atualizado com sucesso.'})


# ✅ Excluir um orçamento
@bp.route('/orcamentos/<int:id>', methods=['DELETE'])
def excluir_orcamento(id):
    orcamento = Orcamento.query.get(id)
    if not orcamento:
        return resposta_json({'erro': 'Orçamento não encontrado.'}, 404)

    db.session.delete(orcamento)
    db.session.commit()
    return resposta_json({'mensagem': 'Orçamento excluído com sucesso.'})
