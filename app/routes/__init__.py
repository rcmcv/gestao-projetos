# Arquivo: app/routes/__init__.py
# 🔹 Importa todos os blueprints das rotas web
from .auth_routes import web as auth_routes
from .clientes_routes import web as clientes_routes
from .fornecedores_routes import web as fornecedores_routes
from .main_routes import web as main_routes
from .materiais_routes import web as materiais_routes
from .materiais_projeto_routes import web as materiais_projeto_routes
from .orcamentos_routes import web as orcamentos_routes
from .projetos_routes import web as projetos_routes
from .status_routes import web as status_routes
from .tipos_routes import web as tipos_routes
from .unidades_routes import web as unidades_routes
from .web_routes import web as web_routes  # 👈 Aqui está o blueprint "web"
from .usuarios_routes import web as usuarios_routes


# 🔹 Opcional: podemos expor esses blueprints num dicionário se quisermos
# usar isso de forma mais dinâmica futuramente.
