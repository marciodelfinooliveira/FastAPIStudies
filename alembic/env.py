import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

# Alembic usará para detectar os modelos e gerar as migrações.
from app.db.base import Base 

# Importa as configurações da aplicação para obter a URL do banco de dados.
from app.core.config import settings

# Este é o objeto de configuração do Alembic, que fornece
# acesso aos valores do arquivo .ini.
config = context.config

# Interpreta o arquivo de configuração para o logging do Python.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Adiciona o metadado do seu modelo ao 'target_metadata'
# para suporte à geração automática de migrações (autogenerate).
# ex: myapp.models.Base.metadata
target_metadata = Base.metadata

# outras opções de configuração podem ser definidas aqui,
# como, por exemplo, a partir de variáveis de ambiente:
# my_important_option = os.environ.get("MY_IMPORTANT_OPTION")
# ... e então passada para o script via context.configure:
# context.configure(my_important_option=my_important_option)

def run_migrations_offline() -> None:
    """Executa as migrações no modo 'offline'.

    Este script configura o contexto apenas com uma URL
    e sem uma Engine, embora uma Engine possa ser usada aqui também.
    Ao pular a criação da Engine, não precisamos nem mesmo de um
    DBAPI disponível.

    As chamadas para context.execute() emitem a string fornecida
    para a saída do script.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Função auxiliar que executa as migrações usando uma conexão de banco de dados.
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Executa as migrações no modo 'online'.

    Neste cenário, precisamos criar uma Engine
    e associar uma conexão com o contexto.

    """
    connectable = create_async_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())