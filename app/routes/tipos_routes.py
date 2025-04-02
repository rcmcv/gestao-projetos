# Arquivo: app/routes/tipos_routes.py
# Rotas da interface web relacionadas à tipos de material: cadastrar, listar, editar e excluir
from flask import render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models.models import TipoMaterial
from .web_routes import web
from app.forms.tipo_material_form import TipoMaterialForm  # ✅ Novo formulário

# ✅ Listar todos os tipos de material
@web.route('/tipos-material')
def listar_tipos_material():
    tipos = TipoMaterial.query.order_by(TipoMaterial.id).all()
    return render_template('tipos/listar_tipos_material.html', tipos=tipos)

# ✅ Criar novo tipo de material
@web.route('/tipos-material/novo', methods=['GET', 'POST'])
def adicionar_tipo_material():
    form = TipoMaterialForm()

    if form.validate_on_submit():
        tipo = TipoMaterial(nome=form.nome.data.strip())
        db.session.add(tipo)
        db.session.commit()

        flash("Tipo de material criado com sucesso!", "success")
        return redirect(url_for('web.listar_tipos_material'))

    return render_template('tipos/form_tipo_material.html', form=form, tipo=None)

# ✅ Editar tipo de material
@web.route('/tipos-material/<int:id>/editar', methods=['GET', 'POST'])
def editar_tipo_material(id):
    tipo = TipoMaterial.query.get_or_404(id)
    form = TipoMaterialForm(obj=tipo)

    if form.validate_on_submit():
        tipo.nome = form.nome.data.strip()
        db.session.commit()

        flash("Tipo de material atualizado com sucesso!", "success")
        return redirect(url_for('web.listar_tipos_material'))

    return render_template('tipos/form_tipo_material.html', form=form, tipo=tipo)

# ✅ Excluir tipo de material
@web.route('/tipos-material/<int:id>/excluir', methods=['POST'])
def excluir_tipo_material(id):
    tipo = TipoMaterial.query.get_or_404(id)
    db.session.delete(tipo)
    db.session.commit()

    flash("Tipo de material excluído com sucesso!", "success")
    return redirect(url_for('web.listar_tipos_material'))

