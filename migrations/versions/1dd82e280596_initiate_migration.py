"""Initiate Migration

Revision ID: 1dd82e280596
Revises: 
Create Date: 2020-04-21 17:59:23.611083

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1dd82e280596'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('jobs', sa.Column('job_location', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('jobs', 'job_location')
    # ### end Alembic commands ###
