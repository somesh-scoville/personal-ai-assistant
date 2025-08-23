from config.settings import settings

from langgraph.store.mongodb import MongoDBStore
from langgraph.checkpoint.mongodb.aio import AsyncMongoDBSaver


async def initialize_saver():
    print("initializing mongo saver")
    async with AsyncMongoDBSaver.from_conn_string(
                conn_string=settings.MONGO_URI,
                db_name=settings.MONGO_DB_NAME,
                checkpoint_collection_name=settings.MONGO_STATE_CHECKPOINT_COLLECTION,
                writes_collection_name=settings.MONGO_STATE_WRITES_COLLECTION,
            ) as saver:
        return saver


async def initialize_store():
    print("initializing mongo store")  
    async with MongoDBStore.from_conn_string(
            conn_string=settings.MONGO_URI,
            db_name=settings.MONGO_DB_NAME,
            collection_name=settings.MONGO_STATE_STORE_COLLECTION
            ) as store:
        return store
