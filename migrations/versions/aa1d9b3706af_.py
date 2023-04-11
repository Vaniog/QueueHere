"""empty message

Revision ID: aa1d9b3706af
Revises: d05034e312e2
Create Date: 2023-04-08 20:15:17.737892

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa1d9b3706af'
down_revision = 'd05034e312e2'
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