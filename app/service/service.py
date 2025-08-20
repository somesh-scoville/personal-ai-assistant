from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from langchain_core.messages import AIMessage, HumanMessage


import json
import asyncio

from agents.personal_assistant import create_agent_graph

from service.schemas import UserInput, ResponseModel

app = FastAPI()
# Initialize the agent graph
graph = create_agent_graph(checkpointer=None,store=None)

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
        for chunk in graph.stream({"messages":input_message}, config=config, stream_mode="values"):
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
    



