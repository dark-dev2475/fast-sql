from typing import Optional
from fastapi import Body, FastAPI,Response,status,HTTPException
from pydantic import BaseModel

from random import randrange
app=FastAPI()
class Post(BaseModel):
    title: str
    published: bool = True # default value optional field for postg request
    description:Optional[str]=None
my_posts = [{"title": "Phone","id":3}, {"title": "Tablet","id":2}   ]  # creaeting a temporarry variabel ewhic will acta smy database for as of now latwe we will be using a postgres sql o rrsome other sort of sql data bases


@app.get("/health")
async def health():
    return {"status":"ok"}

@app.get("/")
async def root():
    return {"data": my_posts}
#ptdantic model takes careof what is being iven in the post rrequest unlikely in  express where we need to do it manually whetehr it is a string or number
# python -m  venv new\ ->cmd to create a virtual environment
# source new/bin/activate -> to activate the virtual environment in mac
# new\Scripts\activate -> to activate the virtual environment in windows

@app.post("/posts/{post_id}")
async def create_post(post_id: int, post: Post):
    return {"post_id": post_id, "post": post}

@app.post("/posts",status_code=status.HTTP_201_CREATED)  # status code 201 is for created
async def create_posts(new_post:Post):
    post_dict=new_post.dict()
    post_dict['id']=randrange(0,10000)

    print(new_post.dict()) #new_post.dict() methis to create a dictionary from the pydantic model
    my_posts.append(post_dict)

    return my_posts

def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p

@app.get("/posts/latest")
def get_latest_post():
    if len(my_posts) == 0:
        return {"message": "No posts found"}
    latest_post = my_posts[len(my_posts)-1]  # Get the last post in the list
    return {"latest_post": latest_post}

@app.get("/posts/{post_id}")
def get_post(post_id: int, response: Response):  # :int is a validator which checks if post_id is an integer nd also it also chnges to an integer
    post=find_post(post_id)  
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        # Alternatively, you can use the following line to return a custom response
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "Post not found"}
        # Uncomment the following lines if you want to return a custom response instead of raising an exception
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "Post not found"}
    print(post_id)
    return {"post": post}

def find_index(id):
    for i,p in enumerate(my_posts):
        if p["id"]==id:
            return i

@app.delete("/posts/{post_id}",status_code=status.HTTP_204_NO_CONTENT)  # status code 204 is for no content
def delete_post(post_id: int):
    index=find_index(post_id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        # Alternatively, you can use the following line to return a custom response
        # return Response(status_code=status.HTTP_404_NOT_FOUND, content="Post not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)  # Return a response with no content (204 status code)




@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    index=find_index(post_id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    post_dict = post.dict()
    post_dict['id'] = post_id  # Ensure the ID is set to the post_id
    my_posts[index] = post_dict
    return {"post": my_posts[index]}
    