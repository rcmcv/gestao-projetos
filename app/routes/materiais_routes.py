# Arquivo: app/routes/materiais_routes.py
# Rotas da interface web relacionadas à materiais: cadastrar, listar, editar, excluir e busca dinâmica
from flask import render_template, request, redirect, url_for, flash, jsonify
from app.extensions import db
from app.models.models import Material, TipoMaterial, UnidadeMedida
from .web_routes import web
from app.forms.material_form import MaterialForm

# ✅ Lista todos os materiais
@web.route('/materiais')
def listar_materiais_web():
    materiais = Material.query.order_by(Material.id).all()
    return render_template('materiais/listar_materiais.html', materiais=materiais)

# ✅ Adiciona novo material
@web.route('/materiais/novo', methods=['GET', 'POST'])
def novo_material():
    form = MaterialForm()
    form.tipo_id.choices = [(t.id, t.nome) for t in TipoMaterial.query.order_by('nome')]
    form.unidade_id.choices = [(u.id, u.sigla) for u in UnidadeMedida.query.order_by('sigla')]

    if form.validate_on_submit():
        novo = Material(
            nome=form.nome.data.strip(),
            tipo_id=form.tipo_id.data,
            unidade_id=form.unidade_id.data
        )
        db.session.add(novo)
        db.session.commit()
        flash("Material cadastrado com sucesso!", "success")
        return redirect(url_for('web.listar_materiais_web'))

    return render_template('materiais/form_material.html', form=form, material=None)

# ✅ Edita material
@web.route('/materiais/<int:id>/editar', methods=['GET', 'POST'])
def editar_material(id):
    material = Material.query.get_or_404(id)
    form = MaterialForm(obj=material)
    form.tipo_id.choices = [(t.id, t.nome) for t in TipoMaterial.query.order_by('nome')]
    form.unidade_id.choices = [(u.id, u.sigla) for u in UnidadeMedida.query.order_by('sigla')]

    if form.validate_on_submit():
        material.nome = form.nome.data.strip()
        material.tipo_id = form.tipo_id.data
        material.unidade_id = form.unidade_id.data
        db.session.commit()
        flash("Material atualizado com sucesso!", "success")
        return redirect(url_for('web.listar_materiais_web'))

    return render_template('materiais/form_material.html', form=form, material=material)

# ✅ Exclui material
@web.route('/materiais/<int:id>/excluir', methods=['POST'])
def excluir_material(id):
    material = Material.query.get_or_404(id)
    db.session.delete(material)
    db.session.commit()
    flash("Material excluído com sucesso!", "success")
    return redirect(url_for('web.listar_materiais_web'))

# ✅ Busca dinâmica por tipo e nome
@web.route('/materiais/buscar', methods=['GET'])
def buscar_materiais_web():
    tipo_id = request.args.get('tipo_id')
    busca = request.args.get('q', '')

    if not tipo_id:
        return jsonify({'erro': 'tipo_id é obrigatório.'}), 400

    materiais = Material.query.filter(
        Material.tipo_id == tipo_id,
        Material.nome.ilike(f"%{busca}%")
    ).all()

    return jsonify([{'id': m.id, 'nome': m.nome} for m in materiais])

@web.route('/materiais/buscar-ui')
def buscar_materiais_ui():
    tipos = TipoMaterial.query.order_by('nome').all()
    return render_template('materiais/buscar_materiais.html', tipos=tipos)
