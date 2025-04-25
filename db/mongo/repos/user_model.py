from pydantic import BaseModel, Field


class UserModel(BaseModel):
    id: int = Field(alias="_id")
    login: str
    password: str
    hash: str