"""Baseline of the schema previously created by create_all."""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("remaining_units", sa.Integer(), nullable=False),
    )
    op.create_table(
        "task",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("status", sa.Enum("PENDING", "PROCESSING", "COMPLETED", "FAILED",
                                    name="taskstatus"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    for column in ("due_date", "user_id", "status"):
        op.create_index(f"ix_task_{column}", "task", [column])


def downgrade() -> None:
    op.drop_table("task")
    op.drop_table("user")
    sa.Enum(name="taskstatus").drop(op.get_bind(), checkfirst=True)
