# Arquivo: app/forms/fornecedor_form.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp

# ✅ Formulário de cadastro/edição de fornecedor
class FornecedorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])

    cnpj = StringField('CNPJ', validators=[
        DataRequired(),
        Length(min=14, max=20),
        Regexp(r'^\d{14}$', message="CNPJ deve conter exatamente 14 números")
    ])

    email = StringField('E-mail', validators=[Length(max=100), Email()])

    telefone = StringField('Telefone', validators=[
        Length(max=50),
        Regexp(r'^\d{10,11}$', message="Telefone deve conter 10 ou 11 números")
    ])

    contato = StringField('Pessoa de Contato', validators=[Length(max=100)])

    submit = SubmitField('Salvar')
