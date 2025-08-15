import asyncio
import sys
import uvicorn
from config import config


if __name__ == "__main__":
    uvicorn.run("service:app", host=config.HOST, port=config.PORT, reload=config.DEV, log_level="info")
