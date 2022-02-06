"""Missing fields

Revision ID: e02b37af896a
Revises: fc4dc8a50b5c
Create Date: 2022-02-06 15:23:38.099009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e02b37af896a'
down_revision = 'fc4dc8a50b5c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('data_request', sa.Column('budget', sa.Float(), nullable=True))
    op.add_column('role', sa.Column('domain_name', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('role', 'domain_name')
    op.drop_column('data_request', 'budget')
    # ### end Alembic commands ###