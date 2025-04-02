# Arquivo: app/routes/fornecedores_routes.py
# Rotas da interface web relacionadas à fornecedores: cadastrar, listar, editar, excluir e busca dinâmica
from flask import render_template, request, redirect, url_for, flash, jsonify
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
    form.tipos.choices = [(t.id, t.nome) for t in TipoMaterial.query.order_by('nome')]

    if form.validate_on_submit():
        fornecedor = Fornecedor(
            nome=form.nome.data.strip(),
            cnpj=form.cnpj.data.strip(),
            email=form.email.data.strip(),
            telefone=form.telefone.data.strip(),
            contato=form.contato.data.strip(),
            tipos=TipoMaterial.query.filter(TipoMaterial.id.in_(form.tipos.data)).all()
        )
        db.session.add(fornecedor)
        db.session.commit()
        flash("Fornecedor cadastrado com sucesso!", "success")
        return redirect(url_for('web.listar_fornecedores'))

    return render_template('fornecedores/form_fornecedor.html', form=form, fornecedor=None)

# ✅ Editar fornecedor
@web.route('/fornecedores/<int:id>/editar', methods=['GET', 'POST'])
def editar_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    form = FornecedorForm(obj=fornecedor)
    form.tipos.choices = [(t.id, t.nome) for t in TipoMaterial.query.order_by('nome')]
    form.tipos.data = [t.id for t in fornecedor.tipos]

    if form.validate_on_submit():
        fornecedor.nome = form.nome.data.strip()
        fornecedor.cnpj = form.cnpj.data.strip()
        fornecedor.email = form.email.data.strip()
        fornecedor.telefone = form.telefone.data.strip()
        fornecedor.contato = form.contato.data.strip()
        fornecedor.tipos = TipoMaterial.query.filter(TipoMaterial.id.in_(form.tipos.data)).all()

        db.session.commit()
        flash("Fornecedor atualizado com sucesso!", "success")
        return redirect(url_for('web.listar_fornecedores'))

    return render_template('fornecedores/form_fornecedor.html', form=form, fornecedor=fornecedor)

# ✅ Excluir fornecedor
@web.route('/fornecedores/<int:id>/excluir', methods=['POST'])
def excluir_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    db.session.delete(fornecedor)
    db.session.commit()
    flash("Fornecedor excluído com sucesso!", "success")
    return redirect(url_for('web.listar_fornecedores'))

# ✅ Buscar fornecedores por tipo (AJAX)
@web.route('/fornecedores/buscar', methods=['GET'])
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
