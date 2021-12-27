"""Creating Domain

Revision ID: 7b7689f19569
Revises: 0f28f7ae2a74
Create Date: 2021-12-24 16:31:37.810754

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7b7689f19569'
down_revision = '0f28f7ae2a74'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('domain',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('deployed_on', sa.DateTime(), nullable=True),
    sa.Column('description', sa.String(length=2048), nullable=True),
    sa.Column('support_email', sa.String(length=255), nullable=True),
    sa.Column('version_name', sa.String(length=255), nullable=True),
    sa.Column('repository', sa.String(length=255), nullable=True),
    sa.Column('branch', sa.String(length=255), nullable=True),
    sa.Column('commit_hash', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('domain_user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user', postgresql.UUID(), nullable=True),
    sa.Column('domain', postgresql.UUID(), nullable=True),
    sa.Column('role', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['domain'], ['domain.id'], ),
    sa.ForeignKeyConstraint(['role'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('domain_user')
    op.drop_table('domain')
    # ### end Alembic commands ###
