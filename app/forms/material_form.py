# Arquivo: app/forms/material_form.py

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

# ✅ Formulário para cadastro e edição de materiais
class MaterialForm(FlaskForm):
    nome = StringField('Nome do Material', validators=[DataRequired(), Length(max=100)])
    tipo_id = SelectField('Tipo de Material', coerce=int, validators=[DataRequired()])
    unidade_id = SelectField('Unidade de Medida', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Salvar')
