from pydantic import BaseModel

class UserCRUDInput(BaseModel):
    name: str
    email: str
    password: str

class LoginInput(BaseModel):
    email: str
    password: str
