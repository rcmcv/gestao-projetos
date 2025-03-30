# Arquivo: app/routes/tipos_routes.py
from flask import Blueprint, request
from app.models.models import TipoMaterial
from app.utils.resposta import resposta_json
from app.extensions import db
from .web_routes import web

# Criação do Blueprint para rotas relacionadas a "tipos de material"
# web = Blueprint('tipos', __name__)

# ✅ Rota para listar todos os tipos de material
@web.route('/tipos-material', methods=['GET'])
def listar_tipos():
    tipos = TipoMaterial.query.all()  # Busca todos os registros no banco
    return resposta_json([
        {'id': t.id, 'nome': t.nome} for t in tipos  # Retorna lista de dicionários
    ])

# ✅ Rota para adicionar um novo tipo de material
@web.route('/tipos-material', methods=['POST'])
def adicionar_tipo():
    dados = request.json  # Recebe os dados JSON da requisição
    nome = dados.get('nome')  # Pega o campo 'nome'

    if not nome:
        return resposta_json({'erro': 'Informe o nome do tipo de material.'}, 400)

    tipo = TipoMaterial(nome=nome)  # Cria nova instância do modelo
    db.session.add(tipo)  # Adiciona à sessão
    db.session.commit()  # Salva no banco
    return resposta_json({'mensagem': 'Tipo de material cadastrado com sucesso!'})

# ✅ Rota para editar (atualizar) um tipo de material existente
@web.route('/tipos-material/<int:id>', methods=['PUT'])
def editar_tipo(id):
    tipo = TipoMaterial.query.get(id)  # Busca o tipo pelo ID
    if not tipo:
        return resposta_json({'erro': 'Tipo de material não encontrado.'}, 404)

    tipo.nome = request.json.get('nome', tipo.nome)  # Atualiza o nome, se informado
    db.session.commit()  # Salva no banco
    return resposta_json({'mensagem': 'Tipo de material atualizado com sucesso.'})

# ✅ Rota para excluir um tipo de material
@web.route('/tipos-material/<int:id>', methods=['DELETE'])
def excluir_tipo(id):
    tipo = TipoMaterial.query.get(id)  # Busca pelo ID
    if not tipo:
        return resposta_json({'erro': 'Tipo de material não encontrado.'}, 404)

    db.session.delete(tipo)  # Remove da sessão
    db.session.commit()  # Aplica exclusão no banco
    return resposta_json({'mensagem': f'Tipo {tipo.nome} excluído com sucesso.'})
