# Arquivo: run.py

# 📦 Importa a função que cria a aplicação a partir do pacote app
from app import create_app

# 🛠️ Cria a instância da aplicação Flask com todas as configurações e rotas
app = create_app()

# 🚀 Ponto de entrada da aplicação
# Se esse arquivo for executado diretamente (e não importado), roda o servidor Flask
if __name__ == '__main__':
    # debug=True ativa o modo de desenvolvimento com recarregamento automático
    app.run(debug=True)
