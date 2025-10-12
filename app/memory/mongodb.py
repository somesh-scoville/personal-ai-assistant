from langgraph.checkpoint.mongodb.aio import AsyncMongoDBSaver
from langgraph.store.mongodb import MongoDBStore

from config.settings import settings


def get_mongodb_saver():
    return AsyncMongoDBSaver.from_conn_string(
        conn_string=settings.MONGO_URI,
        db_name=settings.MONGO_DB_NAME,
        checkpoint_collection_name=settings.MONGO_STATE_CHECKPOINT_COLLECTION,
        writes_collection_name=settings.MONGO_STATE_WRITES_COLLECTION,
    )


def get_mongodb_store():
    return MongoDBStore.from_conn_string(
        conn_string=settings.MONGO_URI,
        db_name=settings.MONGO_DB_NAME,
        collection_name=settings.MONGO_STATE_STORE_COLLECTION,
    )
