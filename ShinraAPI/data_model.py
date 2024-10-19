from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class DBPost(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    title = Column(String)
    post_text = Column(String)
    likes = Column(Integer)

    #def __repr__(self):
        #return f"{self.id} | User Id: {self.user_id}, Title: {self.title}, Text: {self.post_text}, Likes: {self.likes}"

class DBUser(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    image_url = Column(String)
    is_admin = Column(Boolean)

