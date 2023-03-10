"""fix ingredient model

Revision ID: 1bbb51519622
Revises: a36ea391bf8f
Create Date: 2023-02-02 19:41:53.539420

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1bbb51519622'
down_revision = 'a36ea391bf8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ingredient', 'unit')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ingredient', sa.Column('unit', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
