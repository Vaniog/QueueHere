"""empty message

Revision ID: cc0d6ec64942
Revises: 8ac110e61a71
Create Date: 2023-04-04 23:35:46.671932

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cc0d6ec64942'
down_revision = '8ac110e61a71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_queue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_visible', sa.Boolean(), nullable=False))
        batch_op.drop_column('visible')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_queue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('visible', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
        batch_op.drop_column('is_visible')

    # ### end Alembic commands ###
