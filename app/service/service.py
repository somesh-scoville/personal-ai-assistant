from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import AIMessage, HumanMessage

from agents.personal_assistant import create_agent_graph
from memory import initialize_database, initialize_store
from service.schemas import ResponseModel, UserInput


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Initializes database checkpointer and store based on settings."""
    try:
        async with initialize_database() as saver, initialize_store() as store:  # type: ignore
            if hasattr(saver, "setup"):
                await saver.setup()  # type: ignore
            if hasattr(store, "setup"):
                await store.setup()

            agent = create_agent_graph(checkpointer=saver, store=store)
            # need to store the agent in the app state for access in routes
            app.state.agent = agent

            yield

    except Exception as e:
        print(f"Error during database or store initialization: {e}")

    finally:
        # The code here runs on shutdown.
        print("Log:--> Application shutting down...")


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
async def chat(request: UserInput) -> ResponseModel:
    # seperating threads with user id and thread id
    thread_id = request.user_id + "_" + request.thread_id

    config = {"configurable": {"thread_id": thread_id, "user_id": request.user_id}}
    input_message = HumanMessage(content=request.message)

    try:
        # now lets access agent from app lifespan

        agent = app.state.agent

        response = await agent.ainvoke({"messages": input_message}, config=config)

        last_message = response["messages"][-1]
        if isinstance(last_message, AIMessage):
            # Process the AI message as needed
            response_message = str(last_message.content)
            status = "success"

        else:
            response_message = "Unexpected message type received."
            status = "error"

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return ResponseModel(
        response=response_message,
        thread_id=request.thread_id,
        user_id=request.user_id,
        status=status,
    )


@app.post("/chat_stream")
async def chat_stream(request: UserInput) -> ResponseModel:
    # separating threads with user id and thread id
    thread_id = request.user_id + "_" + request.thread_id

    config = {"configurable": {"thread_id": thread_id, "user_id": request.user_id}}
    input_message = HumanMessage(content=request.message)

    try:
        agent = app.state.agent
        response_message = ""
        status = ""

        async for chunk in agent.astream(
            {"messages": input_message}, config=config, stream_mode="values"
        ):
            last_message = chunk["messages"][-1]
            if isinstance(last_message, AIMessage):
                # Process the AI message as needed
                response_message = str(last_message.content)
                status = "success"

            else:
                response_message = "Unexpected message type received."
                status = "error"

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return ResponseModel(
        response=response_message,
        thread_id=request.thread_id,
        user_id=request.user_id,
        status=status,
    )


@app.get("/health_check")
def health_check():
    return {"status": "ok"}
