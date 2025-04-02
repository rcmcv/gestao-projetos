# Arquivo: app/forms/unidade_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

# ✅ Formulário de cadastro/edição de unidade de medida
class UnidadeForm(FlaskForm):
    descricao = StringField('Descrição', validators=[DataRequired(), Length(max=100)])
    sigla = StringField('Sigla', validators=[DataRequired(), Length(max=10)])
    submit = SubmitField('Salvar')
