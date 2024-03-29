"""empty message

Revision ID: 488f7068c40e
Revises: 48f35677aad4
Create Date: 2023-04-13 01:18:52.299259

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '488f7068c40e'
down_revision = '48f35677aad4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('queue_task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id2', sa.Integer(), nullable=False))
        batch_op.drop_column('id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('queue_task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_column('id2')

    # ### end Alembic commands ###
