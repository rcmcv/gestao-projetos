# Arquivo: app/api/orcamentos_routes.py
# Descrição: CRUD de orçamentos e relatório de balizamento
# Autor: Projeto Gestão de Projetos
# Versão: API estruturada com prefixo /api

from flask import Blueprint, request
from app.extensions import db
from app.models.models import Orcamento, MaterialProjeto
from app.utils.resposta import resposta_json
from datetime import datetime

bp = Blueprint('orcamentos_api', __name__, url_prefix='/api')

# 📌 1. Criar novo orçamento (sem PDF por enquanto)
@bp.route('/orcamentos', methods=['POST'])
def cadastrar_orcamento():
    try:
        dados = request.json

        orcamento = Orcamento(
            material_projeto_id=dados['material_projeto_id'],
            fornecedor_id=dados['fornecedor_id'],
            valor_unitario=dados['valor_unitario'],
            numero_orcamento=dados.get('numero_orcamento'),
            data_orcamento=datetime.strptime(dados['data_orcamento'], '%Y-%m-%d') if dados.get('data_orcamento') else None,
            arquivo_pdf=None  # Ainda será implementado no frontend
        )

        db.session.add(orcamento)
        db.session.commit()
        return resposta_json({'mensagem': 'Orçamento cadastrado com sucesso.'})

    except Exception as e:
        return resposta_json({'erro': str(e)}, 400)

# 📌 2. Listar orçamentos de um projeto
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

# 📌 3. Atualizar orçamento
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

# 📌 4. Excluir orçamento
@bp.route('/orcamentos/<int:id>', methods=['DELETE'])
def excluir_orcamento(id):
    orcamento = Orcamento.query.get(id)
    if not orcamento:
        return resposta_json({'erro': 'Orçamento não encontrado.'}, 404)

    db.session.delete(orcamento)
    db.session.commit()
    return resposta_json({'mensagem': 'Orçamento excluído com sucesso.'})

# 📌 5. Relatório de balizamento por projeto
@bp.route('/projetos/<int:projeto_id>/relatorio-balizamento', methods=['GET'])
def relatorio_balizamento(projeto_id):
    relatorio = []

    materiais = MaterialProjeto.query.filter_by(projeto_id=projeto_id).all()

    for m in materiais:
        orcamentos = m.orcamentos

        if not orcamentos:
            continue  # Pula materiais sem orçamentos

        menor_valor = min(o.valor_unitario for o in orcamentos)

        relatorio.append({
            "material": m.material.nome,
            "quantidade": m.quantidade,
            "orcamentos": [
                {
                    "fornecedor": o.fornecedor.nome,
                    "valor_unitario": o.valor_unitario,
                    "menor_preco": o.valor_unitario == menor_valor
                } for o in orcamentos
            ]
        })

    return resposta_json(relatorio)
