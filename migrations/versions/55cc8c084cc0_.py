"""empty message

Revision ID: 55cc8c084cc0
Revises: 22343b63da28
Create Date: 2022-05-24 16:46:29.318289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55cc8c084cc0'
down_revision = '22343b63da28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    
    op.add_column('games', sa.Column('name', sa.String(length=100), nullable=False))
    
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
   
    op.drop_column('games', 'name')
    
    # ### end Alembic commands ###
