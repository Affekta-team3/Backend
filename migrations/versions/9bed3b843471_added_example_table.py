"""Added example table!

Revision ID: 9bed3b843471
Revises: b8e1dbc40642
Create Date: 2024-07-03 15:32:41.998493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bed3b843471'
down_revision = 'b8e1dbc40642'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('submission', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.String(length=36), nullable=False))
        batch_op.add_column(sa.Column('problem_id', sa.String(length=36), nullable=False))
        batch_op.drop_constraint('FK__submissio__probl__59904A2C', type_='foreignkey')
        batch_op.create_foreign_key(None, 'problem', ['problem_id'], ['id'])
        batch_op.drop_column('Id')
        batch_op.drop_column('problemId')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('submission', schema=None) as batch_op:
        batch_op.add_column(sa.Column('problemId', sa.NVARCHAR(length=36, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('Id', sa.NVARCHAR(length=36, collation='SQL_Latin1_General_CP1_CI_AS'), server_default=sa.text('(newid())'), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('FK__submissio__probl__59904A2C', 'problem', ['problemId'], ['id'])
        batch_op.drop_column('problem_id')
        batch_op.drop_column('id')

    # ### end Alembic commands ###