# Arquivo: app/routes/usuarios_routes.py
# Rotas da interface web relacionadas à usuários: cadastrar, listar, editar e excluir
from flask import render_template, redirect, url_for, request, flash, session
from app.models.models import Usuario
from app.extensions import db
from werkzeug.security import generate_password_hash
from .web_routes import web                     # ✅ Importa o blueprint já criado
from app.forms.usuario_form import UsuarioFormCriar, UsuarioFormEditar  # ✅ Importa o formulário novo

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

    form = UsuarioFormCriar()  # ✅ Instancia o formulário

    if form.validate_on_submit():
        if Usuario.query.filter_by(email=form.email.data).first():
            flash('E-mail já cadastrado.', 'warning')
            return redirect(url_for('web.novo_usuario'))

        novo = Usuario(
            nome=form.nome.data,
            email=form.email.data,
            senha=generate_password_hash(form.senha.data),
            permissao=form.permissao.data
        )
        db.session.add(novo)
        db.session.commit()

        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('web.listar_usuarios'))

    return render_template('usuarios/form_usuario.html', form=form, usuario=None)

# ✅ Edita um usuário existente
@web.route('/usuarios/<int:id>/editar', methods=['GET', 'POST'])
def editar_usuario(id):
    acesso = admin_required()
    if acesso:
        return acesso

    usuario = Usuario.query.get_or_404(id)
    form = UsuarioFormEditar(obj=usuario)  # ✅ Preenche o formulário com dados do banco

    if form.validate_on_submit():
        usuario.nome = form.nome.data
        usuario.email = form.email.data
        usuario.permissao = form.permissao.data

        # Atualiza senha somente se preenchida
        if form.senha.data:
            usuario.senha = generate_password_hash(form.senha.data)

        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('web.listar_usuarios'))

    return render_template('usuarios/form_usuario.html', form=form, usuario=usuario)

# ✅ Exclui um usuário
@web.route('/usuarios/excluir/<int:id>', methods=['POST'])
def excluir_usuario(id):
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para realizar essa ação.', 'danger')
        return redirect(url_for('web.login'))

    if session['usuario_id'] == id:
        flash('Você não pode excluir o seu próprio usuário enquanto estiver logado.', 'warning')
        return redirect(url_for('web.listar_usuarios'))

    usuario = Usuario.query.get(id)
    if not usuario:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('web.listar_usuarios'))

    db.session.delete(usuario)
    db.session.commit()
    flash('Usuário excluído com sucesso.', 'success')
    return redirect(url_for('web.listar_usuarios'))
