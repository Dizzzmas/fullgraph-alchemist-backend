"""User model

Revision ID: a5bd99eb0195
Revises: b64b2dcb690f
Create Date: 2020-07-29 12:21:14.850171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a5bd99eb0195"
down_revision = "b64b2dcb690f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id_", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column("updated", sa.DateTime(), nullable=True),
        sa.Column("full_name", sa.Text(), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("_password", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id_"),
        sa.UniqueConstraint("email"),
    )
    op.add_column("item", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        None, "item", "user", ["user_id"], ["id_"], ondelete="CASCADE"
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "item", type_="foreignkey")
    op.drop_column("item", "user_id")
    op.drop_table("user")
    # ### end Alembic commands ###