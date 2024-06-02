from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Importe seus modelos SQLAlchemy
from wallpaper.models import Base
from category.models import Base
from user.models import Base

# Configure os loggers
if context.config.config_file_name:
    fileConfig(context.config.config_file_name)

# Atribua o objeto metadata aos seus modelos
target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=context.config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    configuration = context.config.get_section(context.config.config_ini_section)
    configuration['sqlalchemy.url'] = context.config.get_main_option("sqlalchemy.url")
    connectable = engine_from_config(
        configuration,
        prefix='sqlalchemy.',
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
