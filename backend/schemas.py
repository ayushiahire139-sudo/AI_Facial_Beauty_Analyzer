from pydantic import BaseModel

class UserCreate(BaseModel):
    fullname: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class ImageResponse(BaseModel):
    id: int
    filename: str
    filepath: str

    class Config:
        from_attributes = True