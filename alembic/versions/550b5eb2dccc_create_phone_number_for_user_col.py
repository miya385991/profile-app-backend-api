"""create phone number for user col

Revision ID: 550b5eb2dccc
Revises: 52f3de4fa3b7
Create Date: 2022-07-23 15:28:22.549990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '550b5eb2dccc'
down_revision = '52f3de4fa3b7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users',sa.Column("phone_number",sa.String(), nullable=True))


def downgrade() -> None:
    pass
