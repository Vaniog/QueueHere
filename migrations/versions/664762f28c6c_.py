"""empty message

Revision ID: 664762f28c6c
Revises: 488f7068c40e
Create Date: 2023-04-13 01:19:17.319096

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '664762f28c6c'
down_revision = '488f7068c40e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('queue_task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))
        batch_op.drop_column('id2')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('queue_task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id2', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_column('id')

    # ### end Alembic commands ###
