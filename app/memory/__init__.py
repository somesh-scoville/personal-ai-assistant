from config.settings import DatabaseType, settings
from memory.mongodb import get_mongodb_saver, get_mongodb_store
from memory.postgres import get_postgres_saver, get_postgres_store


def initialize_database():
    """Initialize appropriate database checkpointer"""
    if settings.DATABASE_TYPE == DatabaseType.POSTGRES:
        return get_postgres_saver()
    elif settings.DATABASE_TYPE == DatabaseType.MONGO:
        return get_mongodb_saver()
    else:
        raise ValueError("Unsupported database type")


def initialize_store():
    """Initialize appropriate database checkpointer"""
    if settings.DATABASE_TYPE == DatabaseType.MONGO:
        return get_mongodb_store()
    elif settings.DATABASE_TYPE == DatabaseType.POSTGRES:
        return get_postgres_store()
    else:
        raise ValueError("Unsupported database type")


__all__ = ["initialize_database", "initialize_store"]
