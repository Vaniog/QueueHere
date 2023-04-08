"""empty message

Revision ID: e9c980edad3d
Revises: 2acfbf041da7
Create Date: 2023-04-08 20:21:45.748077

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9c980edad3d'
down_revision = '2acfbf041da7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_queue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('arrive_time', sa.DateTime(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_queue', schema=None) as batch_op:
        batch_op.drop_column('arrive_time')

    # ### end Alembic commands ###
