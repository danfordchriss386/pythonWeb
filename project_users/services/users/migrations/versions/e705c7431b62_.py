"""empty message

Revision ID: e705c7431b62
Revises: 
Create Date: 2023-08-28 08:45:16.256622

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e705c7431b62'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=128), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
