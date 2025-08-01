from fastapi import Body, FastAPI
app=FastAPI()

@app.get("/health")
async def health():
    return {"status":"ok"}
@app.get("/")
async def root():
    return {"message":"Hello World"}


@app.post("/items")
async def create_items(payload:dict=Body(...)):
    print(payload)
    return {"message": f"title:{payload['title']}"}