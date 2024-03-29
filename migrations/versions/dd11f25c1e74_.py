"""empty message

Revision ID: dd11f25c1e74
Revises: 33deb8b015e9
Create Date: 2023-04-04 23:50:53.882382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd11f25c1e74'
down_revision = '33deb8b015e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_queue', schema=None) as batch_op:
        batch_op.drop_constraint('user_queue_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('user_queue_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['member_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'queue', ['queue_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_queue', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('user_queue_ibfk_2', 'queue', ['queue_id'], ['id'])
        batch_op.create_foreign_key('user_queue_ibfk_1', 'user', ['member_id'], ['id'])

    # ### end Alembic commands ###
