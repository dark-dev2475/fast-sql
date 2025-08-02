from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
app=FastAPI()
class Item(BaseModel):
    title: str
    published: bool = True # default value optional field for postg request
    description:Optional[str]=None
my_items = [{"title": "Phone"}, {"title": "Tablet"}   ]  # creaeting a temporarry variabel ewhic will acta smy database for as of now latwe we will be using a postgres sql o rrsome other sort of sql data bases

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

@app.post("/items")
async def create_items(new_item:Item):
    print(new_item.description)
    print(new_item.dict()) #new_item.dict() methis to create a dictionary from the pydantic model
    return {"message": f"title:{new_item.title}"}