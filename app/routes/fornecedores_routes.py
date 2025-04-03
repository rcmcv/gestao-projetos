# Arquivo: app/routes/fornecedores_routes.py
# Rotas da interface web relacionadas à fornecedores: cadastrar, listar, editar, excluir e busca dinâmica
from flask import render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models.models import Fornecedor, TipoMaterial
from .web_routes import web
from app.forms.fornecedor_form import FornecedorForm

# ✅ Listar fornecedores
@web.route('/fornecedores')
def listar_fornecedores():
    fornecedores = Fornecedor.query.all()
    return render_template('fornecedores/listar_fornecedores.html', fornecedores=fornecedores)

# ✅ Cadastrar novo fornecedor
@web.route('/fornecedores/novo', methods=['GET', 'POST'])
def novo_fornecedor():
    form = FornecedorForm()
    tipos = TipoMaterial.query.order_by('nome').all()

    if form.validate_on_submit():
        tipos_ids = request.form.get('tipos', '')
        ids = [int(i) for i in tipos_ids.split(',') if i.isdigit()]

        if not ids:
            flash("Selecione pelo menos um tipo de material.", "danger")
            return render_template('fornecedores/form_fornecedor.html', form=form, titulo="Cadastrar Fornecedor", tipos=tipos, tipos_iniciais=ids)

        fornecedor = Fornecedor(
            nome=form.nome.data.strip(),
            cnpj=form.cnpj.data.strip(),
            email=form.email.data.strip(),
            telefone=form.telefone.data.strip(),
            contato=form.contato.data.strip(),
            tipos=TipoMaterial.query.filter(TipoMaterial.id.in_(ids)).all()
        )

        try:
            db.session.add(fornecedor)
            db.session.commit()
            flash("Fornecedor cadastrado com sucesso!", "success")
            return redirect(url_for('web.listar_fornecedores'))
        except IntegrityError:
            db.session.rollback()
            flash("Já existe um fornecedor com esse CNPJ.", "danger")

    return render_template('fornecedores/form_fornecedor.html', form=form, titulo="Cadastrar Fornecedor", tipos=tipos)

# ✅ Editar fornecedor
@web.route('/fornecedores/<int:id>/editar', methods=['GET', 'POST'])
def editar_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    form = FornecedorForm(obj=fornecedor)
    tipos = TipoMaterial.query.order_by('nome').all()

    if form.validate_on_submit():
        tipos_ids = request.form.get('tipos', '')
        ids = [int(i) for i in tipos_ids.split(',') if i.isdigit()]

        if not ids:
            flash("Selecione pelo menos um tipo de material.", "danger")
            return render_template('fornecedores/form_fornecedor.html', form=form, fornecedor=fornecedor, titulo="Editar Fornecedor", tipos=tipos, tipos_iniciais=ids)

        fornecedor.nome = form.nome.data.strip()
        fornecedor.cnpj = form.cnpj.data.strip()
        fornecedor.email = form.email.data.strip()
        fornecedor.telefone = form.telefone.data.strip()
        fornecedor.contato = form.contato.data.strip()
        fornecedor.tipos = TipoMaterial.query.filter(TipoMaterial.id.in_(ids)).all()

        try:
            db.session.commit()
            flash("Fornecedor atualizado com sucesso!", "success")
            return redirect(url_for('web.listar_fornecedores'))
        except IntegrityError:
            db.session.rollback()
            flash("Erro ao atualizar fornecedor. CNPJ duplicado?", "danger")

    return render_template('fornecedores/form_fornecedor.html', form=form, fornecedor=fornecedor, titulo="Editar Fornecedor", tipos=tipos)

# ✅ Excluir fornecedor
@web.route('/fornecedores/<int:id>/excluir', methods=['POST'])
def excluir_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    db.session.delete(fornecedor)
    db.session.commit()
    flash("Fornecedor excluído com sucesso!", "success")
    return redirect(url_for('web.listar_fornecedores'))

# ✅ Página de busca com select
@web.route('/fornecedores/buscar')
def buscar_fornecedores():
    tipos = TipoMaterial.query.order_by('nome').all()
    return render_template('fornecedores/buscar_fornecedores.html', tipos=tipos)

# ✅ Rota AJAX
@web.route('/fornecedores/buscar_ajax')
def buscar_fornecedores_ajax():
    tipo_id = request.args.get('tipo_id')

    if not tipo_id:
        return jsonify({'erro': 'tipo_id é obrigatório'}), 400

    fornecedores = Fornecedor.query.filter(
        Fornecedor.tipos.any(TipoMaterial.id == tipo_id)
    ).all()

    return jsonify([
        {'id': f.id, 'nome': f.nome, 'cnpj': f.cnpj} for f in fornecedores
    ])

