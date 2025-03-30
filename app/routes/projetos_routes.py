# Arquivo: app/routes/projetos_routes.py
from flask import Blueprint, request
from app.extensions import db
from app.models.models import Projeto
from app.utils.resposta import resposta_json
from datetime import datetime
from .web_routes import web

# web = Blueprint('projetos', __name__)

# ✅ Listar todos os projetos
@web.route('/projetos', methods=['GET'])
def listar_projetos():
    projetos = Projeto.query.all()
    return resposta_json([
        {
            'id': p.id,
            'nome': p.nome,
            'descricao': p.descricao,
            'cliente': p.cliente.nome,
            'responsavel': p.responsavel.nome,
            'status': p.status.nome,
            'data_solicitacao': p.data_solicitacao.strftime('%Y-%m-%d'),
            'data_inicio': p.data_inicio.strftime('%Y-%m-%d') if p.data_inicio else None,
            'data_fim': p.data_fim.strftime('%Y-%m-%d') if p.data_fim else None
        } for p in projetos
    ])

# ✅ Cadastrar novo projeto
@web.route('/projetos', methods=['POST'])
def adicionar_projeto():
    dados = request.json
    try:
        projeto = Projeto(
            nome=dados['nome'],
            descricao=dados.get('descricao'),
            cliente_id=dados['cliente_id'],
            responsavel_id=dados['responsavel_id'],
            status_id=dados['status_id'],
            data_solicitacao=datetime.strptime(dados['data_solicitacao'], '%Y-%m-%d'),  # obrigatório
            data_inicio=None,
            data_fim=None
        )
        db.session.add(projeto)
        db.session.commit()
        return resposta_json({'mensagem': 'Projeto cadastrado com sucesso!'})
    except Exception as e:
        return resposta_json({'erro': str(e)}, 400)

# ✅ Atualizar projeto (inclui aprovação e datas de execução)
@web.route('/projetos/<int:id>', methods=['PUT'])
def editar_projeto(id):
    projeto = Projeto.query.get(id)
    if not projeto:
        return resposta_json({'erro': 'Projeto não encontrado.'}, 404)

    dados = request.json
    projeto.nome = dados.get('nome', projeto.nome)
    projeto.descricao = dados.get('descricao', projeto.descricao)
    projeto.cliente_id = dados.get('cliente_id', projeto.cliente_id)
    projeto.responsavel_id = dados.get('responsavel_id', projeto.responsavel_id)
    projeto.status_id = dados.get('status_id', projeto.status_id)

    # Atualiza data de solicitação (se quiser permitir isso)
    if dados.get('data_solicitacao'):
        projeto.data_solicitacao = datetime.strptime(dados['data_solicitacao'], '%Y-%m-%d')

    # Permite preencher data de início/fim somente se status for "aprovado"
    if dados.get('status_nome') == 'aprovado' or projeto.status.nome.lower() == 'aprovado':
        if dados.get('data_inicio'):
            projeto.data_inicio = datetime.strptime(dados['data_inicio'], '%Y-%m-%d')
        if dados.get('data_fim'):
            projeto.data_fim = datetime.strptime(dados['data_fim'], '%Y-%m-%d')

    db.session.commit()
    return resposta_json({'mensagem': 'Projeto atualizado com sucesso.'})

# ✅ Excluir projeto
@web.route('/projetos/<int:id>', methods=['DELETE'])
def excluir_projeto(id):
    projeto = Projeto.query.get(id)
    if not projeto:
        return resposta_json({'erro': 'Projeto não encontrado.'}, 404)

    db.session.delete(projeto)
    db.session.commit()
    return resposta_json({'mensagem': f'Projeto {projeto.nome} excluído com sucesso.'})
