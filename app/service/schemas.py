from pydantic import BaseModel


class UserInput(BaseModel):
    message:str
    user_id: str
    thread_id: str

class ResponseModel(BaseModel):
    response: str
    thread_id: str
    user_id: str
    status: str