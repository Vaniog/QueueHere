"""empty message

Revision ID: e7d431d6b47e
Revises: 28e6c0fa6e20
Create Date: 2023-04-14 10:41:17.180090

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7d431d6b47e'
down_revision = '28e6c0fa6e20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('queue_task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('queue_id', sa.String(length=10), nullable=False),
    sa.Column('action', sa.Enum('clear', 'close', 'open', name='taskenum'), nullable=False),
    sa.Column('execute_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['queue_id'], ['queue.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('queue_task', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_queue_task_execute_time'), ['execute_time'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('queue_task', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_queue_task_execute_time'))

    op.drop_table('queue_task')
    # ### end Alembic commands ###