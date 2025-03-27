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
