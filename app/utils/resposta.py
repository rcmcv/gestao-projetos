# Arquivo: app/utils/resposta.py
import json
from flask import Response

def resposta_json(dados, status=200):
    """
    Retorna uma resposta JSON com acentuação correta.
    """
    return Response(
        json.dumps(dados, ensure_ascii=False),
        status=status,
        mimetype='application/json'
    )
