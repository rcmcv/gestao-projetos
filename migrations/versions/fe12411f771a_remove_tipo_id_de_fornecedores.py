"""Remove tipo_id de fornecedores

Revision ID: fe12411f771a
Revises: 
Create Date: 2025-04-02 19:25:13.243187

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe12411f771a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fornecedores', schema=None) as batch_op:
        batch_op.drop_column('tipo_id')


    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fornecedores', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tipo_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_fornecedores_tipo_id', 'tipos_materiais', ['tipo_id'], ['id'])


    # ### end Alembic commands ###
