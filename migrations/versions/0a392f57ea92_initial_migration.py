"""Initial migration

Revision ID: 0a392f57ea92
Revises: 
Create Date: 2024-06-24 18:33:55.084227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a392f57ea92'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('submission', schema=None) as batch_op:
        batch_op.add_column(sa.Column('problem_id', sa.String(length=36), nullable=False))
        batch_op.drop_constraint('FK__submissio__probl__59904A2C', type_='foreignkey')
        batch_op.create_foreign_key(None, 'problem', ['problem_id'], ['id'])
        batch_op.drop_column('problemId')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('submission', schema=None) as batch_op:
        batch_op.add_column(sa.Column('problemId', sa.NVARCHAR(length=36, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('FK__submissio__probl__59904A2C', 'problem', ['problemId'], ['id'])
        batch_op.drop_column('problem_id')

    # ### end Alembic commands ###
