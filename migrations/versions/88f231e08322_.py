"""empty message

Revision ID: 88f231e08322
Revises: ade33e81d43f
Create Date: 2023-04-13 01:15:21.258376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88f231e08322'
down_revision = 'ade33e81d43f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('queue_task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id2', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('queue_task', schema=None) as batch_op:
        batch_op.drop_column('id2')

    # ### end Alembic commands ###
