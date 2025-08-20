from typing import List, Optional, Literal, TypedDict
from pydantic import BaseModel, Field



# Update memory tool
class UpdateMemory(TypedDict):
    """ Decision on what memory type to update."""
    update_type: Literal['user', 'todo', 'instructions']

class Profile(BaseModel):
    """This is a profile of the user you are interacting with."""

    name: Optional[str] = Field(description="The user's name", default=None)
    age: Optional[int] = Field(description="The user's age",default=None)
    location: Optional[str] = Field( description="The user's location", default=None)
    job: Optional[str] = Field(description="The user's job", default=None)
    connections: List[str] = Field(default_factory=list, description="Peronal connection of the user, such as family members, friends, or coworkers")
    interests: List[str] = Field(default_factory=list, description="The user's interests or hobbies")

# ToDo schema
class ToDo(BaseModel):
    """ToDo item for the user to complete."""
    task: str = Field(description="The task to be completed.")
    time_to_complete: Optional[str] = Field(description="Estimated time to complete the task (minutes).")
    deadline: Optional[str] = Field(
        description="When the task needs to be completed by (if applicable)",
        default=None
    )
    solutions: list[str] = Field(
        description="List of specific, actionable solutions (e.g., specific ideas, service providers, or concrete options relevant to completing the task)",
        min_items=1,
        default_factory=list
    )
    status: Literal["not started", "in progress", "done", "archived"] = Field(
        description="Current status of the task",
        default="not started"
    )

