"""Update table

Revision ID: 993610c5fca0
Revises: 3025af974662
Create Date: 2024-01-14 17:01:27.497763

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '993610c5fca0'
down_revision = '3025af974662'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('supplies', sa.Column('description', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('supplies', 'description')
    # ### end Alembic commands ###
