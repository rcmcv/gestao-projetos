# Arquivo: app/forms/usuario_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional

# ✅ Formulário de cadastro/edição de usuário
class UsuarioFormCriar(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=100)])
    permissao = SelectField('Permissão', choices=[('admin', 'Administrador'), ('comum', 'Comum')], validators=[DataRequired()])
    submit = SubmitField('Salvar')

class UsuarioFormEditar(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha (preencher apenas para alterar)', validators=[Optional(), Length(min=6, max=100)])
    permissao = SelectField('Permissão', choices=[('admin', 'Administrador'), ('comum', 'Comum')], validators=[DataRequired()])
    submit = SubmitField('Salvar')

