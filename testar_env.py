from dotenv import load_dotenv
import os
from pathlib import Path

# 🔥 Mostra o caminho completo do .env que está sendo carregado
env_path = Path(__file__).resolve().parent / '.env'
print("🔎 Tentando carregar:", env_path)

# 🔥 Força o carregamento do .env explicitamente
load_dotenv(dotenv_path=env_path, override=True)

env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

print("✔️ Verificando variáveis de ambiente carregadas:")
print("MAIL_USERNAME:", os.getenv("MAIL_USERNAME"))
print("MAIL_PASSWORD:", os.getenv("MAIL_PASSWORD"))
print("MAIL_SERVER:", os.getenv("MAIL_SERVER"))
print("MAIL_PORT:", os.getenv("MAIL_PORT"))
print("MAIL_USE_TLS:", os.getenv("MAIL_USE_TLS"))
