# Arquivo: app/routes/orcamentos_routes.py
# Importações necessárias
from flask import Blueprint, request
from app.extensions import db
from app.models.models import Orcamento
from app.utils.resposta import resposta_json
import os
from datetime import datetime
from werkzeug.utils import secure_filename

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
