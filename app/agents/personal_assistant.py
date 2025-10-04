import uuid
from datetime import datetime
from typing import Literal

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, merge_message_runs
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore

from agents.prompts import CREATE_INSTRUCTIONS, MODEL_SYSTEM_MESSAGE, TRUSTCALL_INSTRUCTION
from agents.tools import UpdateMemory
from agents.utilities import extract_tool_info, profile_extractor, spy, todo_extractor
from core.llm import model

load_dotenv()


def task_assistant(state: MessagesState, config: RunnableConfig, store: BaseStore) -> dict:
    """Load memories from the store and use them to personalize the chatbot's response."""
    # Get the user ID from the config
    # configurable = configuration.Configuration.from_runnable_config(config)
    # user_id = configurable.user_id
    # todo_category = configurable.todo_category
    # task_maistro_role = configurable.task_maistro_role

    user_id = config.get("configurable", {}).get("user_id")
    if user_id is None:
        raise KeyError("Missing 'user_id' in config['configurable']")

    # Retrieve profile memory from the store
    namespace = ("profile", user_id)
    memories = store.search(namespace)
    user_profile = memories[0].value if memories else None

    # Retrieve people memory from the store
    namespace = ("todo", user_id)
    memories = store.search(namespace)
    todo = "\n".join(f"{mem.value}" for mem in memories)

    # Retrieve custom instructions
    namespace = ("instructions", user_id)
    memories = store.search(namespace)
    instructions = memories[0].value if memories else ""

    system_msg = MODEL_SYSTEM_MESSAGE.format(
        user_profile=user_profile, todo=todo, instructions=instructions
    )

    # Respond using memory as well as the chat history
    response = model.bind_tools([UpdateMemory], parallel_tool_calls=False).invoke(
        [SystemMessage(content=system_msg)] + state["messages"]
    )

    return {"messages": [response]}


def update_profile(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """Reflect on the chat history and update the memory collection."""
    # Get the user ID from the config
    user_id = config.get("configurable", {}).get("user_id")
    if user_id is None:
        raise KeyError("Missing 'user_id' in config['configurable']")

    # Define the namespace for the memories
    namespace = ("profile", user_id)

    # Retrieve the most recent memories for context
    existing_items = store.search(namespace)

    # Format the existing memories for the Trustcall extractor
    tool_name = "Profile"
    existing_memories = (
        [(existing_item.key, tool_name, existing_item.value) for existing_item in existing_items]
        if existing_items
        else None
    )

    # Merge the chat history and the instruction
    trustcall_instruction_formatted = TRUSTCALL_INSTRUCTION.format(time=datetime.now().isoformat())
    updated_messages = list(
        merge_message_runs(
            messages=[
                SystemMessage(content=trustcall_instruction_formatted),
                *state["messages"][:-1],
            ]
        )
    )

    # Invoke the extractor
    result = profile_extractor.invoke({"messages": updated_messages, "existing": existing_memories})

    # Save save the memories from Trustcall to the store
    for r, rmeta in zip(result["responses"], result["response_metadata"], strict=False):
        store.put(namespace, rmeta.get("json_doc_id", str(uuid.uuid4())), r.model_dump(mode="json"))
    tool_calls = state["messages"][-1].tool_calls  # type: ignore
    # Return tool message with update verification
    return {
        "messages": [
            {"role": "tool", "content": "updated profile", "tool_call_id": tool_calls[0]["id"]}
        ]
    }


def update_todos(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """Reflect on the chat history and update the memory collection."""
    # Get the user ID from the config
    user_id = config.get("configurable", {}).get("user_id")
    if user_id is None:
        raise KeyError("Missing 'user_id' in config['configurable']")

    # Define the namespace for the memories
    namespace = ("todo", user_id)

    # Retrieve the most recent memories for context
    existing_items = store.search(namespace)

    # Format the existing memories for the Trustcall extractor
    tool_name = "ToDo"
    existing_memories = (
        [(existing_item.key, tool_name, existing_item.value) for existing_item in existing_items]
        if existing_items
        else None
    )

    # Merge the chat history and the instruction
    trustcall_instruction_formatted = TRUSTCALL_INSTRUCTION.format(time=datetime.now().isoformat())
    updated_messages = list(
        merge_message_runs(
            messages=[
                SystemMessage(content=trustcall_instruction_formatted),
                *state["messages"][:-1],
            ]
        )
    )

    # Invoke the extractor
    result = todo_extractor.invoke({"messages": updated_messages, "existing": existing_memories})

    # Save save the memories from Trustcall to the store
    for r, rmeta in zip(result["responses"], result["response_metadata"], strict=False):
        store.put(namespace, rmeta.get("json_doc_id", str(uuid.uuid4())), r.model_dump(mode="json"))

    # Respond to the tool call made in task_mAIstro, confirming the update
    tool_calls = state["messages"][-1].tool_calls  # type: ignore

    # Extract the changes made by Trustcall and add the the ToolMessage returned to task_mAIstro
    todo_update_msg = extract_tool_info(spy.called_tools, tool_name)
    return {
        "messages": [
            {"role": "tool", "content": todo_update_msg, "tool_call_id": tool_calls[0]["id"]}
        ]
    }


def update_instructions(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """Reflect on the chat history and update the memory collection."""
    # Get the user ID from the config
    user_id = config.get("configurable", {}).get("user_id")
    if user_id is None:
        raise KeyError("Missing 'user_id' in config['configurable']")

    namespace = ("instructions", user_id)

    existing_memory = store.get(namespace, "user_instructions")

    # Format the memory in the system prompt
    system_msg = CREATE_INSTRUCTIONS.format(
        current_instructions=existing_memory.value if existing_memory else None
    )
    new_memory = model.invoke(
        [
            SystemMessage(content=system_msg),
            *state["messages"][:-1],
            HumanMessage(content="Please update the instructions based on the conversation"),
        ]
    )

    # Overwrite the existing memory in the store
    key = "user_instructions"
    store.put(namespace, key, {"memory": new_memory.content})
    tool_calls = state["messages"][-1].tool_calls  # type: ignore
    # Return tool message with update verification
    return {
        "messages": [
            {"role": "tool", "content": "updated instructions", "tool_call_id": tool_calls[0]["id"]}
        ]
    }


def route_message(
    state: MessagesState, config: RunnableConfig, store: BaseStore
) -> Literal[END, "update_todos", "update_instructions", "update_profile"]:  # type: ignore
    """Reflect on the memories and chat history to decide whether to update the memory collection."""
    message = state["messages"][-1]
    if len(message.tool_calls) == 0:  # type: ignore
        return END
    else:
        tool_call = message.tool_calls[0]  # type: ignore
        if tool_call["args"]["update_type"] == "user":
            return "update_profile"
        elif tool_call["args"]["update_type"] == "todo":
            return "update_todos"
        elif tool_call["args"]["update_type"] == "instructions":
            return "update_instructions"
        else:
            raise ValueError


def create_agent_graph(checkpointer, store) -> StateGraph:
    """Create the agent graph for the personal assistant."""
    # Create the graph + all nodes
    builder = StateGraph(MessagesState)

    # Define the flow of the memory extraction process
    builder.add_node(task_assistant)
    builder.add_node(update_todos)
    builder.add_node(update_profile)
    builder.add_node(update_instructions)

    # Define the flow
    builder.add_edge(START, "task_assistant")
    builder.add_conditional_edges("task_assistant", route_message)
    builder.add_edge("update_todos", "task_assistant")
    builder.add_edge("update_profile", "task_assistant")
    builder.add_edge("update_instructions", "task_assistant")

    if checkpointer is None:
        checkpointer = MemorySaver()
    if store is None:
        store = InMemoryStore()
    # Compile the graph with the checkpointer and store
    graph = builder.compile(checkpointer=checkpointer, store=store)
    return graph  # type: ignore
