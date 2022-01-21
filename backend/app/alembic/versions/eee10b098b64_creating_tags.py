"""Creating Tags

Revision ID: eee10b098b64
Revises: 7b7689f19569
Create Date: 2022-01-21 10:04:34.949560

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'eee10b098b64'
down_revision = '7b7689f19569'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('domain', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['domain'], ['domain.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tags')
    # ### end Alembic commands ###