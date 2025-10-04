from contextlib import asynccontextmanager

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres import AsyncPostgresStore
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

from config.settings import settings


def get_postgres_connection_string() -> str:
    """Build and return the PostgreSQL connection string from settings."""
    if settings.POSTGRES_PASSWORD is None:
        raise ValueError("POSTGRES_PASSWORD is not set")
    return (
        f"postgresql://{settings.POSTGRES_USER}:"
        f"{settings.POSTGRES_PASSWORD.get_secret_value()}@"
        f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/"
        f"{settings.POSTGRES_DB}"
    )


@asynccontextmanager
async def get_postgres_saver():
    "Initializes and return a postgreSQL saver instance using connection pool for resilent connection"

    application_name = settings.POSTGRES_APPLICATION_NAME + "-" + "saver"

    async with AsyncConnectionPool(
        get_postgres_connection_string(),
        min_size=settings.POSTGRES_MIN_CONNECTIONS_PER_POOL,
        max_size=settings.POSTGRES_MAX_CONNECTIONS_PER_POOL,
        kwargs={"autocommit": True, "row_factory": dict_row, "application_name": application_name},
        check=AsyncConnectionPool.check_connection,
    ) as pool:
        try:
            async with pool.connection() as conn:
                checkpointer = AsyncPostgresSaver(conn)
                await checkpointer.setup()
                yield checkpointer

        finally:
            await pool.close()


@asynccontextmanager
async def get_postgres_store():
    "Initializes and return a postgreSQL store instance using connection pool for resilent connection"

    application_name = settings.POSTGRES_APPLICATION_NAME + "-" + "store"

    async with AsyncConnectionPool(
        get_postgres_connection_string(),
        min_size=settings.POSTGRES_MIN_CONNECTIONS_PER_POOL,
        max_size=settings.POSTGRES_MAX_CONNECTIONS_PER_POOL,
        kwargs={"autocommit": True, "row_factory": dict_row, "application_name": application_name},
        check=AsyncConnectionPool.check_connection,
    ) as pool:
        try:
            async with pool.connection() as conn:
                store = AsyncPostgresStore(conn)
                await store.setup()
                yield store

        finally:
            await pool.close()
