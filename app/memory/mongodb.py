from config.settings import settings

from langgraph.store.mongodb import MongoDBStore
from langgraph.checkpoint.mongodb import MongoDBSaver

async def initialize_saver():
    saver = MongoDBSaver.from_conn_string(
                conn_string=settings.MONGO_DB_NAME,
                db_name=settings.MONGO_DB_NAME,
                checkpoint_collection_name=settings.MONGO_STATE_CHECKPOINT_COLLECTION,
                writes_collection_name=settings.MONGO_STATE_WRITES_COLLECTION,
            )
    return saver


async def initialize_store():     
    store = MongoDBStore.from_conn_string(
            conn_string=settings.MONGO_URI,
            db_name=settings.MONGO_DB_NAME,
            collection_name=settings.MONGO_STATE_STORE_COLLECTION
            )
    return store