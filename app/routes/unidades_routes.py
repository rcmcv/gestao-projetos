# Arquivo: app/routes/unidades_routes.py
# Rotas da interface web relacionadas à unidade de medida: cadastrar, listar, editar e excluir
from flask import render_template, request, redirect, url_for, flash
from app.models.models import UnidadeMedida
from app.extensions import db
from .web_routes import web                     # ✅ Importa o blueprint já criado
from app.forms.unidade_form import UnidadeForm  # ✅ Importação do novo formulário

# ✅ Listar todas as unidades de medida
@web.route('/unidades')
def listar_unidades():
    unidades = UnidadeMedida.query.order_by(UnidadeMedida.id).all()
    return render_template('unidades/listar_unidades.html', unidades=unidades)

# ✅ Cadastrar nova unidade de medida
@web.route('/unidades/novo', methods=['GET', 'POST'])
def nova_unidade():
    form = UnidadeForm()

    if form.validate_on_submit():
        nova = UnidadeMedida(
            descricao=form.descricao.data.strip(),
            sigla=form.sigla.data.strip()
        )
        db.session.add(nova)
        db.session.commit()

        flash("Unidade criada com sucesso!", "success")
        return redirect(url_for('web.listar_unidades'))

    return render_template('unidades/form_unidade.html', form=form, unidade=None)

# ✅ Editar unidade existente
@web.route('/unidades/editar/<int:unidade_id>', methods=['GET', 'POST'])
def editar_unidade(unidade_id):
    unidade = UnidadeMedida.query.get_or_404(unidade_id)
    form = UnidadeForm(obj=unidade)

    if form.validate_on_submit():
        unidade.descricao = form.descricao.data.strip()
        unidade.sigla = form.sigla.data.strip()
        db.session.commit()

        flash("Unidade atualizada com sucesso!", "success")
        return redirect(url_for('web.listar_unidades'))

    return render_template('unidades/form_unidade.html', form=form, unidade=unidade)

# ✅ Excluir unidade
@web.route('/unidades/excluir/<int:unidade_id>', methods=['POST'])
def excluir_unidade(unidade_id):
    unidade = UnidadeMedida.query.get_or_404(unidade_id)
    db.session.delete(unidade)
    db.session.commit()

    flash("Unidade excluída com sucesso!", "success")
    return redirect(url_for('web.listar_unidades'))
