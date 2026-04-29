"""Add Bookings

Revision ID: 7a7ee1356e91
Revises: 3c0cc007fbe4
Create Date: 2026-04-10 06:54:59.892128

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "7a7ee1356e91"
down_revision: Union[str, Sequence[str], None] = "3c0cc007fbe4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "booking",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("date_from", sa.Date(), nullable=False),
        sa.Column("date_to", sa.Date(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )



def downgrade() -> None:
    op.drop_table("booking")

