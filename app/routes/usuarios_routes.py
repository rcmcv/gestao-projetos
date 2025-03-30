# app/routes/usuarios_routes.py

from flask import render_template, redirect, url_for, request, flash, session
from app.models.models import Usuario
from app import db
from werkzeug.security import generate_password_hash
from .web_routes import web  # ✅ Importa o blueprint já criado

# ✅ Middleware de acesso restrito
def admin_required():
    if 'usuario_id' not in session or session.get('usuario_permissao') != 'admin':
        flash('Acesso restrito a administradores.', 'danger')
        return redirect(url_for('web.login'))
    return None

# ✅ Lista todos os usuários cadastrados
@web.route('/usuarios')
def listar_usuarios():
    acesso = admin_required()
    if acesso:
        return acesso

    usuarios = Usuario.query.all()
    return render_template('usuarios/listar_usuarios.html', usuarios=usuarios)

# ✅ Exibe formulário de novo usuário
@web.route('/usuarios/novo', methods=['GET', 'POST'])
def novo_usuario():
    acesso = admin_required()
    if acesso:
        return acesso

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        permissao = request.form.get('permissao')

        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.', 'warning')
            return redirect(url_for('web.novo_usuario'))

        novo = Usuario(
            nome=nome,
            email=email,
            senha=generate_password_hash(senha),
            permissao=permissao
        )
        db.session.add(novo)
        db.session.commit()

        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('web.listar_usuarios'))

    return render_template('usuarios/form_usuario.html', usuario=None)

# ✅ Edita um usuário existente
@web.route('/usuarios/<int:id>/editar', methods=['GET', 'POST'])
def editar_usuario(id):
    acesso = admin_required()
    if acesso:
        return acesso

    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        usuario.nome = request.form.get('nome')
        usuario.email = request.form.get('email')
        usuario.permissao = request.form.get('permissao')

        # Atualiza senha se foi preenchida
        nova_senha = request.form.get('senha')
        if nova_senha:
            usuario.senha = generate_password_hash(nova_senha)

        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('web.listar_usuarios'))

    return render_template('usuarios/form_usuario.html', usuario=usuario)
