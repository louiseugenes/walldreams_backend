"""Change old_field type to Text

Revision ID: f31cccc13f6b
Revises: 05cfc7b537b0
Create Date: 2024-06-01 21:23:59.731969

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f31cccc13f6b'
down_revision: Union[str, None] = '05cfc7b537b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('category', 'count')
    # ### end Alembic commands ###
