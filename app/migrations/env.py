import os
import sys
from sqlalchemy import create_engine, pool
from alembic import context

sys.path.append("/app")
from app.core.config import settings
from app.db.base import Base
from app import models  # noqa

config = context.config
DB_URL = (
    f"oracle+oracledb://{settings.ORACLE_USER}:{settings.ORACLE_PASSWORD}"
    f"@{settings.ORACLE_HOST}:{settings.ORACLE_PORT}/?service_name={settings.ORACLE_SERVICE}"
)
config.set_main_option("sqlalchemy.url", DB_URL)
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        include_schemas=False,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(DB_URL, poolclass=pool.NullPool, future=True)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            include_schemas=False,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
