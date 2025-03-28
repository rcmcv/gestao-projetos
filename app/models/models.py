# Arquivo: app/models/models.py
from app.extensions import db

# ✅ Cria a classe Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    permissao = db.Column(db.String(20), nullable=False)  # ex: 'admin', 'usuario'

    def __repr__(self):
        return f'<Usuario {self.nome}>'


# ✅ Cria a classe Tipo de Material
class TipoMaterial(db.Model):
    __tablename__ = 'tipos_materiais'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f'<TipoMaterial {self.nome}>'


# ✅ Cria a classe Unidade de Medida
class UnidadeMedida(db.Model):
    __tablename__ = 'unidades_medida'

    id = db.Column(db.Integer, primary_key=True)
    sigla = db.Column(db.String(10), nullable=False, unique=True)   # Ex: kg, m, un
    descricao = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<UnidadeMedida {self.sigla}>'


# ✅ Cria a classe Material
class Material(db.Model):
    __tablename__ = 'materiais'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipos_materiais.id'), nullable=False)
    unidade_id = db.Column(db.Integer, db.ForeignKey('unidades_medida.id'), nullable=False)

    tipo = db.relationship('TipoMaterial', backref='materiais')
    unidade = db.relationship('UnidadeMedida', backref='materiais')

    def __repr__(self):
        return f'<Material {self.nome}>'


# ✅ Cria a classe Fornecedores
class Fornecedor(db.Model):
    __tablename__ = 'fornecedores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(50))
    contato = db.Column(db.String(100))

    tipo_id = db.Column(db.Integer, db.ForeignKey('tipos_materiais.id'), nullable=False)
    tipo = db.relationship('TipoMaterial', backref='fornecedores')

    def __repr__(self):
        return f'<Fornecedor {self.nome}>'


# ✅ Cria a classe Clientes
class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf_cnpj = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(50))
    contato = db.Column(db.String(100))

    def __repr__(self):
        return f'<Cliente {self.nome}>'


# ✅ Cria a classe Status
class Status(db.Model):
    __tablename__ = 'status'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)
    ativo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Status {self.nome}>'


# ✅ Cria a classe Projeto
class Projeto(db.Model):
    __tablename__ = 'projetos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)

    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    cliente = db.relationship('Cliente', backref='projetos')

    responsavel_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    responsavel = db.relationship('Usuario', backref='projetos')

    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    status = db.relationship('Status', backref='projetos')

    data_solicitacao = db.Column(db.Date, nullable=False)  # NOVO campo obrigatório
    data_inicio = db.Column(db.Date, nullable=True)        # só preenchido se aprovado
    data_fim = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f'<Projeto {self.nome}>'


# ✅ Cria a classe MaterialProjeto
class MaterialProjeto(db.Model):
    __tablename__ = 'materiais_projeto'

    id = db.Column(db.Integer, primary_key=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projetos.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materiais.id'), nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipos_materiais.id'), nullable=False)  # <- novo campo
    quantidade = db.Column(db.Float, nullable=False)

    projeto = db.relationship('Projeto', backref='materiais_projeto')
    material = db.relationship('Material', backref='projetos_usando')
    tipo = db.relationship('TipoMaterial')

    def __repr__(self):
        return f'<MaterialProjeto Projeto={self.projeto_id} Material={self.material_id} Qtd={self.quantidade}>'


# ✅ Cria a classe Orçamento
class Orcamento(db.Model):
    __tablename__ = 'orcamentos'

    id = db.Column(db.Integer, primary_key=True)
    material_projeto_id = db.Column(db.Integer, db.ForeignKey('materiais_projeto.id'), nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'), nullable=False)
    valor_unitario = db.Column(db.Float, nullable=False)
    numero_orcamento = db.Column(db.String(50))
    arquivo_pdf = db.Column(db.String(200))
    data_orcamento = db.Column(db.Date)

    material_projeto = db.relationship('MaterialProjeto', backref='orcamentos')
    fornecedor = db.relationship('Fornecedor', backref='orcamentos')

    def __repr__(self):
        return f'<Orcamento R$ {self.valor_unitario}>'
