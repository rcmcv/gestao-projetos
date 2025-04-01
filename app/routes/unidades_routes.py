# Arquivo: app/routes/unidades_routes.py
# Rotas da interface web relacionadas à unidade de medida: cadastrar, listar, editar e excluir

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models.models import UnidadeMedida
from .web_routes import web


# ✅ Rota: Listar todas as unidades de medida
@web.route('/unidades')
def listar_unidades():
    unidades = UnidadeMedida.query.order_by(UnidadeMedida.id).all()
    return render_template('unidades/listar_unidades.html', unidades=unidades)


# ✅ Rota: Cadastrar nova unidade
@web.route('/unidades/novo', methods=['GET', 'POST'])
def nova_unidade():
    if request.method == 'POST':
        nome = request.form.get('descricao')
        sigla = request.form.get('sigla')

        print("📨 Dados recebidos (nova unidade):", request.form)

        # Validação simples
        if not nome or not sigla:
            flash("Preencha todos os campos obrigatórios.", "error")
            return render_template('unidades/form_unidade.html')

        # Cria nova unidade e salva no banco
        nova = UnidadeMedida(descricao=nome.strip(), sigla=sigla.strip())
        db.session.add(nova)
        db.session.commit()

        flash("Unidade criada com sucesso!", "success")
        return redirect(url_for('web.listar_unidades'))

    # Requisição GET: renderiza o formulário vazio
    return render_template('unidades/form_unidade.html')


# ✅ Rota: Editar unidade existente
@web.route('/unidades/editar/<int:unidade_id>', methods=['GET', 'POST'])
def editar_unidade(unidade_id):
    unidade = UnidadeMedida.query.get_or_404(unidade_id)

    if request.method == 'POST':
        nome = request.form.get('descricao')
        sigla = request.form.get('sigla')

        print("📨 Dados recebidos (editar unidade):", request.form)

        # Validação simples
        if not nome or not sigla:
            flash("Preencha todos os campos obrigatórios.", "error")
            return render_template('unidades/form_unidade.html', unidade=unidade)

        # Atualiza a unidade
        unidade.descricao = nome.strip()
        unidade.sigla = sigla.strip()
        db.session.commit()

        flash("Unidade atualizada com sucesso!", "success")
        return redirect(url_for('web.listar_unidades'))

    # Requisição GET: carrega dados no formulário
    return render_template('unidades/form_unidade.html', unidade=unidade)


# ✅ Rota: Excluir unidade
@web.route('/unidades/excluir/<int:unidade_id>', methods=['POST'])
def excluir_unidade(unidade_id):
    unidade = UnidadeMedida.query.get_or_404(unidade_id)
    db.session.delete(unidade)
    db.session.commit()

    flash("Unidade excluída com sucesso!", "success")
    return redirect(url_for('web.listar_unidades'))
