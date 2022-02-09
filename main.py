from os import stat
from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
            {"title": "favorite foods", "content": "I like pizza", "id": 2}]



def find_post (id):
    for p in my_posts:
        if p['id']==id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    return {"message": "Hello World"}


#Get all the posts
@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts():
    return {"data" : my_posts}


#Get a single post
@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int):
    post = find_post(id) #post to be deleted
    if not post:         #if post is not present
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_detail": post}


#Create a post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post): #Taking post as a Pydantic schema of type Post
    post_dict = post.dict() #take data from front end and convert it to dictionary
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


#Delete a post
@app.delete ("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post (id: int):
    index = find_index_post(id) #finding index of the post to be deleted
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" Post with id {id} does not exists")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) #Returning this after successfull deletion


#Update a post
@app.put ("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id        #update the id
    my_posts[index] = post_dict #update the post
    return {"data": post_dict}