import asyncio
import sys
import uvicorn
from config.settings import settings


if __name__ == "__main__":
    uvicorn.run("service:app", host=settings.SERVICE_HOST, port=settings.SERVICE_PORT, reload=settings.DEV, log_level="info")
