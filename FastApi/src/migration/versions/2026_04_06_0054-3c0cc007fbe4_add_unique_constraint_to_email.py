"""Add unique constraint to email

Revision ID: 3c0cc007fbe4
Revises: 103930a102e8
Create Date: 2026-04-06 00:54:44.643272

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "3c0cc007fbe4"
down_revision: Union[str, Sequence[str], None] = "103930a102e8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])



def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
