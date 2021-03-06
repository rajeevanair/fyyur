"""empty message

Revision ID: 33afa5eb7374
Revises: 27279fc8b980
Create Date: 2020-10-14 21:56:20.604159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33afa5eb7374'
down_revision = '27279fc8b980'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.add_column('Artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'seeking_venue')
    op.drop_column('Artist', 'seeking_description')
    # ### end Alembic commands ###
