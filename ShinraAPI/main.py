import pandas as pd
from fastapi import FastAPI
from api_models import Post, User
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import sessionmaker
from data_model import Base, DBPost, DBUser

SQLALCHEMY_DATABASE_URL = "sqlite:///./social_media.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

app = FastAPI()
post_df = pd.read_sql_table("posts", engine)
user_df = pd.read_sql_table("users", engine)


async def get_user_by_name(name: str):
    user_row = user_df[user_df["username"] == name].iloc[0].to_dict()

    return User(id=user_row["id"],
                username=user_row["username"],
                image_url=user_row["image_url"],
                is_admin=user_row["is_admin"])


@app.get("/users/")
async def get_users(name: str | None = None):
    return_list = []
    if name:
        return_list.append(await get_user_by_name(name))
        return return_list
    else:
        for each in user_df["username"]:
            return_list.append(await get_user_by_name(str(each)))
        return return_list
    
@app.get("/users/{user_Id}")
async def get_user_by_id(user_Id: int):
    user = user_df[user_df["id"] == user_Id].iloc[0].to_dict()
    return User(id=user["id"],
                username=user["username"],
                image_url=user["image_url"],
                is_admin=user["is_admin"])

@app.get("/posts/user/{user_Id}")
async def get_posts_by_user(user_Id: int):
    return_list = []
    x = 0
    for _ in post_df[post_df["user_id"] == user_Id]:
        each = post_df[post_df["user_id"] == user_Id].iloc[x].to_dict()
        post = Post(id = each["id"],
                    user_id=each["user_id"],
                    title = each["title"],
                    post_text = each["post_text"],
                    likes = each["likes"])
        return_list.append(post)
        x += 1
    x = 0
    return return_list

@app.get("/posts/")
async def get_posts(title: str | None = None):
    post_df = pd.read_sql_table("posts", engine)
    return_list = []
    x = 0
    if title:
        for _ in post_df[post_df["title"] == title].iterrows():
            each = post_df[post_df["title"] == title].iloc[x].to_dict()
            post = Post(id = each["id"],
                    user_id=each["user_id"],
                    title = each["title"],
                    post_text = each["post_text"],
                    likes = each["likes"])
            return_list.append(post)
            x += 1
        return return_list
    for _ in post_df.iterrows():
        x += 1
    x -= 1
    for _ in post_df.iterrows():
        each = post_df.iloc[x].to_dict()
        post = Post(id = each["id"],
                    user_id=each["user_id"],
                    title = each["title"],
                    post_text = each["post_text"],
                    likes = each["likes"])
        return_list.append(post)
        x -= 1
    x = 0
    return return_list

@app.get("/posts/{post_id}")
async def get_post_by_id(post_id: int):
    post_df = pd.read_sql_table("posts", engine)
    row = post_df[post_df["id"] == post_id].iloc[0].to_dict()
    post = Post(id=row["id"],
                title=row["title"],
                user_id=row["user_id"],
                post_text=row["post_text"],
                likes=row["likes"])
    return post
@app.post("/posts/")
async def create_post(post: Post):
    post_df = pd.read_sql_table("posts", engine)
    x = 0
    for _ in post_df.iterrows():
        x += 1
    x -= 1
    last_post = post_df.iloc[x].to_dict()
    new_post = DBPost(id=last_post["id"] + 1,
           user_id=post.user_id,
           title=post.title,
           post_text=post.post_text,
           likes=post.likes)
    session.add(new_post)
    session.commit()

@app.put("/posts/{post_id}")
async def update_post(post_id, post: Post):
    statement = update(DBPost).where(DBPost.id == post_id).values(title=post.title, post_text=post.post_text)
    session.execute(statement)
    session.commit()