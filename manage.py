# manage.py
from flask.cli import FlaskGroup
from app import create_app
from app.extensions import db, migrate
from flask_migrate import init as db_init, migrate as db_migrate, upgrade as db_upgrade

# Cria a aplicação normalmente
app = create_app()

# Cria o grupo de comandos
cli = FlaskGroup(app)

# ✅ Registra manualmente os comandos 'db init', 'db migrate', 'db upgrade'
@cli.command("db-init")
def init():
    """Inicializa as migrações"""
    db_init()

@cli.command("db-migrate")
def do_migrate():
    """Cria o script de migração"""
    db_migrate(message="migração automática")

@cli.command("db-upgrade")
def do_upgrade():
    """Aplica a migração no banco"""
    db_upgrade()

if __name__ == '__main__':
    cli()
