"""Creating Feedback table

Revision ID: 5a69e26804ee
Revises: 752523fb0742
Create Date: 2021-12-18 10:39:46.512742

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a69e26804ee'
down_revision = '752523fb0742'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('feedback',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('frustrations', sa.String(length=2048), nullable=True),
    sa.Column('suggestions', sa.String(length=2048), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('feedback')
    # ### end Alembic commands ###
