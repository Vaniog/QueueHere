"""empty message

Revision ID: 786c5bac1fa9
Revises: aa1d9b3706af
Create Date: 2023-04-08 20:17:26.274105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '786c5bac1fa9'
down_revision = 'aa1d9b3706af'
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