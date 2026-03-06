from sqlmodel import SQLModel
from pydantic import EmailStr


class SignUpRequest(SQLModel):
    username:str
    email:EmailStr
    password:str

class LoginRequest(SQLModel):
    email:EmailStr
    password:str