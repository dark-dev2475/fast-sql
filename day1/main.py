from typing import Optional
from fastapi import Body, FastAPI,Response,status,HTTPException
from pydantic import BaseModel

from random import randrange
app=FastAPI()
class Item(BaseModel):
    title: str
    published: bool = True # default value optional field for postg request
    description:Optional[str]=None
my_items = [{"title": "Phone","id":3}, {"title": "Tablet","id":2}   ]  # creaeting a temporarry variabel ewhic will acta smy database for as of now latwe we will be using a postgres sql o rrsome other sort of sql data bases

@app.get("/health")
async def health():
    return {"status":"ok"}
@app.get("/")
async def root():
    return {"data": my_items}
#ptdantic model takes careof what is being iven in the post rrequest unlikely in  express where we need to do it manually whetehr it is a string or number
# python -m  venv new\ ->cmd to create a virtual environment
# source new/bin/activate -> to activate the virtual environment in mac
# new\Scripts\activate -> to activate the virtual environment in windows
@app.post("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}

@app.post("/items",status_code=status.HTTP_201_CREATED)  # status code 201 is for created
async def create_items(new_item:Item):
    item_dict=new_item.dict()
    item_dict['id']=randrange(0,10000)

    print(new_item.dict()) #new_item.dict() methis to create a dictionary from the pydantic model
    my_items.append(item_dict)

    return my_items

def find_item(id):
    for i in my_items:
        if i["id"]==id:
            return i

@app.get("/items/latest")
def get_latest_item():
    if len(my_items) == 0:
        return {"message": "No items found"}
    latest_item = my_items[len(my_items)-1]  # Get the last item in the list
    return {"latest_item": latest_item}

@app.get("/items/{item_id}")
def get_item(item_id: int, response: Response):  # :int is a validator which checks if item_id is an integer nd also it also chnges to an integer
    item=find_item(item_id)  
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        # Alternatively, you can use the following line to return a custom response
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "Item not found"}
        # Uncomment the following lines if you want to return a custom response instead of raising an exception
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "Item not found"}
    print(item_id)
    return {"item": item}

def find_index(id):
    for i,p in enumerate(my_items):
        if p["id"]==id:
            return i

@app.delete("/items/{item_id}",status_code=status.HTTP_204_NO_CONTENT)  # status code 204 is for no content
def delete_item(item_id: int):
    index=find_index(item_id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        # Alternatively, you can use the following line to return a custom response
        # return Response(status_code=status.HTTP_404_NOT_FOUND, content="Item not found")
    my_items.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)  # Return a response with no content (204 status code)




@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    index=find_index(item_id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    item_dict = item.dict()
    item_dict['id'] = item_id  # Ensure the ID is set to the item_id
    my_items[index] = item_dict
    return {"item": my_items[index]}
    