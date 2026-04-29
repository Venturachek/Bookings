"""Add Rooms

Revision ID: 09daa42d5665
Revises: a2de1eac5a07
Create Date: 2026-04-02 04:19:02.930952

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "09daa42d5665"
down_revision: Union[str, Sequence[str], None] = "a2de1eac5a07"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hotel_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["hotel_id"],
            ["hotels.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )



def downgrade() -> None:
    op.drop_table("rooms")

