# Arquivo: app/forms/fornecedor_form.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email

# ✅ Formulário de cadastro/edição de fornecedor
class FornecedorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    cnpj = StringField('CNPJ', validators=[DataRequired(), Length(max=20)])
    email = StringField('E-mail', validators=[Length(max=100), Email()])
    telefone = StringField('Telefone', validators=[Length(max=50)])
    contato = StringField('Pessoa de Contato', validators=[Length(max=100)])

    # ✅ Permite selecionar múltiplos tipos de material
    tipos = SelectMultipleField('Tipos de Material', coerce=int, validators=[DataRequired()])

    submit = SubmitField('Salvar')
