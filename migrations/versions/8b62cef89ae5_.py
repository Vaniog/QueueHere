"""empty message

Revision ID: 8b62cef89ae5
Revises: 759d8e547f48
Create Date: 2023-04-04 19:09:19.481968

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b62cef89ae5'
down_revision = '759d8e547f48'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('is_guest', sa.Boolean(), nullable=True),
    sa.Column('ip_address', sa.String(length=30), nullable=True),
    sa.Column('name_to_print', sa.String(length=30), nullable=True),
    sa.Column('is_confirmed', sa.Boolean(), nullable=False),
    sa.Column('confirmed_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('user_queue',
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.Column('queue_id', sa.String(length=10), nullable=False),
    sa.Column('name_printed', sa.String(length=30), nullable=False),
    sa.Column('index_in_queue', sa.Integer(), nullable=False),
    sa.Column('visible', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['member_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['queue_id'], ['queue.id'], ),
    sa.PrimaryKeyConstraint('member_id', 'queue_id')
    )
    with op.batch_alter_table('queue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_index', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('queue', schema=None) as batch_op:
        batch_op.drop_column('last_index')

    op.drop_table('user_queue')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    # ### end Alembic commands ###
