"""Added status to User

Revision ID: 429ae74b421a
Revises: 5a69e26804ee
Create Date: 2021-12-19 13:10:05.844242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '429ae74b421a'
down_revision = '5a69e26804ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('status', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'status')
    # ### end Alembic commands ###