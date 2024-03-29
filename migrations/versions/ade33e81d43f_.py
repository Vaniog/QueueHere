"""empty message

Revision ID: ade33e81d43f
Revises: 3fabc09e03b8
Create Date: 2023-04-11 16:25:41.656088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ade33e81d43f'
down_revision = '3fabc09e03b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('queue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_open', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('queue', schema=None) as batch_op:
        batch_op.drop_column('is_open')

    # ### end Alembic commands ###
