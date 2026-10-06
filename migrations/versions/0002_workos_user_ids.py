"""Use WorkOS string IDs and enforce task ownership.

Deletes disposable development tasks and users: old integer identities have no
mapping to WorkOS IDs. Do not apply to a database with data to preserve.
"""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('DELETE FROM task')
    op.execute('DELETE FROM "user"')
    op.alter_column("user", "id", existing_type=sa.Integer(), server_default=None)
    op.alter_column("user", "id", existing_type=sa.Integer(), type_=sa.String(),
                    existing_nullable=False, postgresql_using="id::text")
    op.execute('DROP SEQUENCE IF EXISTS user_id_seq')
    op.create_foreign_key("fk_task_user_id_user", "task", "user", ["user_id"], ["id"])


def downgrade() -> None:
    raise RuntimeError("Cannot map WorkOS IDs back to integer IDs; downgrade is unsupported")
