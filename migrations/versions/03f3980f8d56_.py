"""empty message

Revision ID: 03f3980f8d56
Revises: ef1344a97136
Create Date: 2023-04-08 20:23:07.664983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03f3980f8d56'
down_revision = 'ef1344a97136'
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
