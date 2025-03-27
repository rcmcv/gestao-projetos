# Arquivo: app/routes/fornecedores_routes.py
# Importações necessárias
from flask import Blueprint, request
from app.extensions import db
from app.models.models import Fornecedor, TipoMaterial
from app.utils.resposta import resposta_json

# Criação do Blueprint para rotas do módulo "fornecedores"
bp = Blueprint('fornecedores', __name__)

# ✅ Rota para listar todos os fornecedores
@bp.route('/fornecedores', methods=['GET'])
def listar_fornecedores():
    fornecedores = Fornecedor.query.all()  # Consulta todos os fornecedores no banco
    return resposta_json([
        {
            'id': f.id,
            'nome': f.nome,
            'cnpj': f.cnpj,
            'email': f.email,
            'telefone': f.telefone,
            'contato': f.contato,
            'tipo_material': f.tipo.nome  # Acesso ao nome do tipo de material relacionado
        } for f in fornecedores
    ])

# ✅ Rota para adicionar novo fornecedor
@bp.route('/fornecedores', methods=['POST'])
def adicionar_fornecedor():
    dados = request.json  # Recebe os dados em JSON enviados na requisição

    # Valida campos obrigatórios
    campos_obrigatorios = ['nome', 'cnpj', 'tipo_id']
    if not all(dados.get(c) for c in campos_obrigatorios):
        return resposta_json({'erro': 'Campos obrigatórios: nome, cnpj, tipo_id'}, 400)

    # Cria nova instância de Fornecedor
    fornecedor = Fornecedor(
        nome=dados['nome'],
        cnpj=dados['cnpj'],
        email=dados.get('email'),
        telefone=dados.get('telefone'),
        contato=dados.get('contato'),
        tipo_id=dados['tipo_id']
    )

    db.session.add(fornecedor)  # Adiciona à sessão
    db.session.commit()         # Salva no banco
    return resposta_json({'mensagem': 'Fornecedor cadastrado com sucesso!'})

# ✅ Rota para editar fornecedor existente
@bp.route('/fornecedores/<int:id>', methods=['PUT'])
def editar_fornecedor(id):
    fornecedor = Fornecedor.query.get(id)  # Busca fornecedor pelo ID
    if not fornecedor:
        return resposta_json({'erro': 'Fornecedor não encontrado.'}, 404)

    # Atualiza campos se enviados na requisição
    dados = request.json
    fornecedor.nome = dados.get('nome', fornecedor.nome)
    fornecedor.cnpj = dados.get('cnpj', fornecedor.cnpj)
    fornecedor.email = dados.get('email', fornecedor.email)
    fornecedor.telefone = dados.get('telefone', fornecedor.telefone)
    fornecedor.contato = dados.get('contato', fornecedor.contato)
    fornecedor.tipo_id = dados.get('tipo_id', fornecedor.tipo_id)

    db.session.commit()
    return resposta_json({'mensagem': 'Fornecedor atualizado com sucesso.'})

# ✅ Rota para excluir fornecedor
@bp.route('/fornecedores/<int:id>', methods=['DELETE'])
def excluir_fornecedor(id):
    fornecedor = Fornecedor.query.get(id)  # Busca fornecedor pelo ID
    if not fornecedor:
        return resposta_json({'erro': 'Fornecedor não encontrado.'}, 404)

    db.session.delete(fornecedor)  # Remove da sessão
    db.session.commit()            # Aplica exclusão no banco
    return resposta_json({'mensagem': f'Fornecedor {fornecedor.nome} excluído com sucesso.'})
