"""livestreams table added

Revision ID: e7ecbe67690b
Revises: 94f9d56d70c8
Create Date: 2020-01-16 06:11:04.978251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7ecbe67690b'
down_revision = '94f9d56d70c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('livestream',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('internal_ip', sa.String(length=20), nullable=True),
    sa.Column('configuration_type', sa.String(length=10), nullable=True),
    sa.Column('configuration_name', sa.String(length=100), nullable=True),
    sa.Column('id_user', sa.Integer(), nullable=True),
    sa.Column('id_configuration', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_configuration'], ['configuration.id'], ),
    sa.ForeignKeyConstraint(['id_user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('livestream')
    # ### end Alembic commands ###
