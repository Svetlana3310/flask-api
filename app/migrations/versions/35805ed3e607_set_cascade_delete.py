"""set cascade delete

Revision ID: 35805ed3e607
Revises: 8de1b07fc6b0
Create Date: 2024-12-16 21:41:06.130058

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35805ed3e607'
down_revision = '8de1b07fc6b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)

    # ### end Alembic commands ###
