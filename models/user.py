from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name:str = ''
    email:str = ''
    password:str = ''

class UserLog(BaseModel):
    email:str = ''
    password:str = ''

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None