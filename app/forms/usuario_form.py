# Arquivo: app/forms/usuario_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length

# ✅ Formulário de cadastro/edição de usuário
class UsuarioForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    email = StringField('E-mail', validators=[DataRequired(), Email(), Length(max=120)])
    senha = PasswordField('Senha (preencher apenas para alterar)', validators=[Length(min=6, max=100)])
    permissao = SelectField('Permissão', choices=[('admin', 'Admin'), ('usuario', 'Usuário')], validators=[DataRequired()])
    submit = SubmitField('Salvar')
