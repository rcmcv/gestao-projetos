# Arquivo: app/forms/tipo_material_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

# ✅ Formulário de cadastro/edição de tipo de material
class TipoMaterialForm(FlaskForm):
    nome = StringField('Nome do Tipo de Material', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Salvar')
