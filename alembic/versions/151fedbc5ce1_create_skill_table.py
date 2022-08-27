"""create skills.py table

Revision ID: 151fedbc5ce1
Revises: 550b5eb2dccc
Create Date: 2022-07-23 15:54:16.309342

"""
from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision = '151fedbc5ce1'
down_revision = '550b5eb2dccc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('skills.py',
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('skill_name', sa.String(), nullable=False,),
                    sa.Column('created', sa.DateTime(timezone=True),
                              default=datetime.datetime.utcnow),
                    )


def downgrade() -> None:
    op.drop_table('skills.py')
