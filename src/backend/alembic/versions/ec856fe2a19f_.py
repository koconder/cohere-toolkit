"""empty message

Revision ID: ec856fe2a19f
Revises: ed17f144f4bf
Create Date: 2024-07-17 21:53:31.643685

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "ec856fe2a19f"
down_revision: Union[str, None] = "ed17f144f4bf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "conversations",
        sa.Column("file_ids", postgresql.ARRAY(sa.String()), nullable=True),
    )
    op.drop_index("file_conversation_id", table_name="files")
    op.drop_index("file_conversation_id_user_id", table_name="files")
    op.drop_index("file_message_id", table_name="files")
    op.drop_index("file_user_id", table_name="files")
    op.drop_constraint("files_message_id_fkey", "files", type_="foreignkey")
    op.drop_constraint("file_conversation_id_user_id_fkey", "files", type_="foreignkey")
    op.drop_column("files", "message_id")
    op.drop_column("files", "conversation_id")
    op.add_column(
        "messages", sa.Column("file_ids", postgresql.ARRAY(sa.String()), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("messages", "file_ids")
    op.add_column(
        "files",
        sa.Column("conversation_id", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "files",
        sa.Column("message_id", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "file_conversation_id_user_id_fkey",
        "files",
        "conversations",
        ["conversation_id", "user_id"],
        ["id", "user_id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "files_message_id_fkey",
        "files",
        "messages",
        ["message_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_index("file_user_id", "files", ["user_id"], unique=False)
    op.create_index("file_message_id", "files", ["message_id"], unique=False)
    op.create_index(
        "file_conversation_id_user_id",
        "files",
        ["conversation_id", "user_id"],
        unique=False,
    )
    op.create_index("file_conversation_id", "files", ["conversation_id"], unique=False)
    op.drop_column("conversations", "file_ids")
    # ### end Alembic commands ###
