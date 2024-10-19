from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    image_url: str
    is_admin: bool

class Post(BaseModel):
    id: int
    user_id: int
    title: str
    post_text: str
    likes: int