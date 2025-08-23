from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from langchain_core.messages import AIMessage, HumanMessage

from agents.personal_assistant import create_agent_graph

from service.schemas import UserInput, ResponseModel

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

# from memory.mongodb import initialize_store, initialize_saver

## Settings ##
from config.settings import settings

from langgraph.store.mongodb import MongoDBStore
from langgraph.checkpoint.mongodb.aio import AsyncMongoDBSaver

@asynccontextmanager
async def lifespan(app:FastAPI) -> AsyncGenerator:
    """
    initializes mongodb database checkpointer and store
    """

    try:
        print("initializing mongo saver")
        async with AsyncMongoDBSaver.from_conn_string(
                    conn_string=settings.MONGO_URI,
                    db_name=settings.MONGO_DB_NAME,
                    checkpoint_collection_name=settings.MONGO_STATE_CHECKPOINT_COLLECTION,
                    writes_collection_name=settings.MONGO_STATE_WRITES_COLLECTION,
                ) as saver:
            
            
            agent = create_agent_graph(checkpointer=saver,store=None)
            #need to store the agent in the app state for access in routes
            app.state.agent = agent

            yield

    except Exception as e:
        raise e
    
    finally:
        # The code here runs on shutdown.
        print("Log: Application shutting down...")

app = FastAPI(lifespan=lifespan)


# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity; adjust as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.post("/chat")
async def chat(request:UserInput) -> ResponseModel:

    config = {"configurable":{"thread_id": request.thread_id, "user_id": request.user_id}}
    input_message = HumanMessage(content=request.message)

    try:
        #now lets access agent from app lifespan

        agent = app.state.agent

        response = await agent.ainvoke({"messages": input_message}, config=config)
        

        last_message = response['messages'][-1]
        if isinstance(last_message, AIMessage):
            # Process the AI message as needed
            response_message = last_message.content
            status = "success"

        else:
            response_message="Unexpected message type received."
            status = "error"


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return ResponseModel(
        response=response_message,
        thread_id=request.thread_id,
        user_id=request.user_id,
        status=status
    )



@app.post("/chat_stream")
async def chat(request:UserInput) -> ResponseModel:

    config = {"configurable":{"thread_id": request.thread_id, "user_id": request.user_id}}
    input_message = HumanMessage(content=request.message)

    try:

        agent = app.state.agent

        for chunk in agent.stream({"messages":input_message}, config=config, stream_mode="values"):
            last_message = chunk['messages'][-1]
            if isinstance(last_message, AIMessage):
                # Process the AI message as needed
                response_message = last_message.content
                status = "success"

            else:
                response_message="Unexpected message type received."
                status = "error"


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return ResponseModel(
        response=response_message,
        thread_id=request.thread_id,
        user_id=request.user_id,
        status=status
    )
    



