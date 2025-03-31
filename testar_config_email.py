# Arquivo: testar_config_email.py
from instance.config import Config

print("\n🔍 Verificando variáveis carregadas da classe Config:\n")

# Cria uma instância da configuração
config = Config()

print("✅ MAIL_USERNAME:", config.MAIL_USERNAME)
print("✅ MAIL_PASSWORD:", config.MAIL_PASSWORD)
print("✅ MAIL_SERVER:", config.MAIL_SERVER)
print("✅ MAIL_PORT:", config.MAIL_PORT)
print("✅ MAIL_USE_TLS:", config.MAIL_USE_TLS)
print("✅ MAIL_DEFAULT_SENDER:", config.MAIL_DEFAULT_SENDER)

print("✅ DATABASE_URI:", config.SQLALCHEMY_DATABASE_URI)
print("✅ SECRET_KEY:", config.SECRET_KEY)
