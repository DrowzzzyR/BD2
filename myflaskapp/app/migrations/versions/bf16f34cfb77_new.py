"""New

Revision ID: bf16f34cfb77
Revises: 53bd602517c3
Create Date: 2024-01-13 18:55:23.887891

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bf16f34cfb77'
down_revision = '53bd602517c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('login', sa.String(length=100), nullable=False))
        batch_op.drop_index('uq_users_username')
        batch_op.create_unique_constraint(batch_op.f('uq_users_login'), ['login'])
        batch_op.drop_column('username')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', mysql.VARCHAR(length=100), nullable=False))
        batch_op.drop_constraint(batch_op.f('uq_users_login'), type_='unique')
        batch_op.create_index('uq_users_username', ['username'], unique=False)
        batch_op.drop_column('login')

    # ### end Alembic commands ###
