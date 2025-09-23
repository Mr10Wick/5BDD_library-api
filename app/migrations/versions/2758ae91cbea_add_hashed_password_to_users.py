"""add hashed_password to users"""

from alembic import op
import sqlalchemy as sa
from app.core.security import hash_password

# Révisions Alembic
revision = "2758ae91cbea"
down_revision = "3a211b4a512b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. ajouter la colonne nullable
    op.add_column("users", sa.Column("hashed_password", sa.String(255), nullable=True))

    # 2. remplir les anciennes lignes avec un mot de passe par défaut
    conn = op.get_bind()
    default_pwd = hash_password("changeme")
    conn.execute(sa.text("UPDATE users SET hashed_password = :pwd"), {"pwd": default_pwd})

    # 3. rendre la colonne NOT NULL
    op.alter_column("users", "hashed_password", nullable=False)


def downgrade() -> None:
    op.drop_column("users", "hashed_password")
