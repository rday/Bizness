"""Create database

Revision ID: 515bce8890b7
Revises: 
Create Date: 2015-03-30 20:33:02.743569

"""

# revision identifiers, used by Alembic.
revision = '515bce8890b7'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'items',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(64)),
        sa.Column('description', sa.Text),
        sa.Column('handled', sa.Boolean, default=False),
        sa.Column('due_date', sa.TIMESTAMP),
        sa.Column('handled_date', sa.TIMESTAMP)
    )

    op.create_index('items_duedate_idx', 'items', ['due_date'])


def downgrade():
    op.drop_index('items_duedate_idx', 'items')
    op.drop_table('items')
