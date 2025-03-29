# Arquivo: app/api/projetos_routes.py
from flask import Blueprint, request
from app.extensions import db
from app.models.models import Projeto
from app.utils.resposta import resposta_json
from datetime import datetime

# ✅ Blueprint da API de projetos com prefixo '/api/projetos'
bp = Blueprint('projetos_api', __name__, url_prefix='/api/projetos')

# 🔍 Listar todos os projetos
@bp.route('/', methods=['GET'])
def listar_projetos():
    projetos = Projeto.query.all()

    return resposta_json([
        {
            'id': p.id,
            'nome': p.nome,
            'descricao': p.descricao,
            'cliente': p.cliente.nome if p.cliente else None,
            'responsavel': p.responsavel.nome if p.responsavel else None,
            'status': p.status.nome if p.status else None,
            'data_solicitacao': p.data_solicitacao.strftime('%Y-%m-%d'),
            'data_inicio': p.data_inicio.strftime('%Y-%m-%d') if p.data_inicio else None,
            'data_fim': p.data_fim.strftime('%Y-%m-%d') if p.data_fim else None
        } for p in projetos
    ])

# ➕ Cadastrar novo projeto
@bp.route('/', methods=['POST'])
def adicionar_projeto():
    dados = request.json
    try:
        # Cria um novo projeto com os dados obrigatórios
        projeto = Projeto(
            nome=dados['nome'],
            descricao=dados.get('descricao'),
            cliente_id=dados['cliente_id'],
            responsavel_id=dados['responsavel_id'],
            status_id=dados['status_id'],
            data_solicitacao=datetime.strptime(dados['data_solicitacao'], '%Y-%m-%d'),
            data_inicio=None,
            data_fim=None
        )
        db.session.add(projeto)
        db.session.commit()
        return resposta_json({'mensagem': 'Projeto cadastrado com sucesso!'}, 201)
    except Exception as e:
        return resposta_json({'erro': str(e)}, 400)

# ✏️ Atualizar projeto existente (inclui atualização de datas, status, etc.)
@bp.route('/<int:id>', methods=['PUT'])
def editar_projeto(id):
    projeto = Projeto.query.get(id)
    if not projeto:
        return resposta_json({'erro': 'Projeto não encontrado.'}, 404)

    dados = request.json

    # Atualiza campos básicos
    projeto.nome = dados.get('nome', projeto.nome)
    projeto.descricao = dados.get('descricao', projeto.descricao)
    projeto.cliente_id = dados.get('cliente_id', projeto.cliente_id)
    projeto.responsavel_id = dados.get('responsavel_id', projeto.responsavel_id)
    projeto.status_id = dados.get('status_id', projeto.status_id)

    # Permite atualizar a data de solicitação
    if dados.get('data_solicitacao'):
        projeto.data_solicitacao = datetime.strptime(dados['data_solicitacao'], '%Y-%m-%d')

    # Se o status for 'aprovado', libera datas de execução
    if dados.get('status_nome') == 'aprovado' or (projeto.status and projeto.status.nome.lower() == 'aprovado'):
        if dados.get('data_inicio'):
            projeto.data_inicio = datetime.strptime(dados['data_inicio'], '%Y-%m-%d')
        if dados.get('data_fim'):
            projeto.data_fim = datetime.strptime(dados['data_fim'], '%Y-%m-%d')

    db.session.commit()
    return resposta_json({'mensagem': 'Projeto atualizado com sucesso.'})

# ❌ Excluir projeto
@bp.route('/<int:id>', methods=['DELETE'])
def excluir_projeto(id):
    projeto = Projeto.query.get(id)
    if not projeto:
        return resposta_json({'erro': 'Projeto não encontrado.'}, 404)

    db.session.delete(projeto)
    db.session.commit()
    return resposta_json({'mensagem': f'Projeto {projeto.nome} excluído com sucesso.'})
