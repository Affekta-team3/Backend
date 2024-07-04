"""Added example table

Revision ID: b8e1dbc40642
Revises: 
Create Date: 2024-07-03 15:27:43.174324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8e1dbc40642'
down_revision = None
branch_labels = None
depends_on = None


from alembic import op
import sqlalchemy as sa

def upgrade():
    # Create the 'example' table
    op.create_table(
        'example',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('problem_id', sa.String(length=36), nullable=False),
        sa.Column('input', sa.String(length=500), nullable=False),
        sa.Column('output', sa.String(length=500), nullable=False),
        sa.Column('explanation', sa.String(length=500), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['problem_id'], ['problem.id'], ondelete='CASCADE')
    )


    # ### end Alembic commands ###


def downgrade():
    pass

    # ### end Alembic commands ###
