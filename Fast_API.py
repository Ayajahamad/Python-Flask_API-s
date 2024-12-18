from fastapi import FastAPI
from pydantic import BaseModel

# Create an instance of FastAPI app
app = FastAPI()

# Pydantic model for the request data (used in POST endpoint)
class Item(BaseModel):
    id:int
    name: str
    price: float

# In-memory storage (simulated database)
items_db = []

@app.get("/")
def get_items():
    return {"message": "Hello World"}


# GET endpoint: Returns a list of stored items
@app.get("/items/")
def get_items():
    return items_db

# POST endpoint: Accepts JSON data, stores it in memory, and returns a response
@app.post("/items/")
def create_item(item: Item):
    items_db.append(item)  # Store the posted data in the list
    return {"message": f"Item {item.name} with price {item.price} has been created."}

# Update item endpoint (PUT)
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    bd_item = next((i for i in items_db if i.id == item_id),None)
    
    bd_item.name = item.name
    bd_item.price = item.price
    print(bd_item)
    return {"message": f"Item {item_id} has been updated.", "item": bd_item}
            
# Delete item endpoint (DELETE)
@app.delete("/items/{item_id}")
def delete_item(item_id: int, item: Item):
    bd_item = next((i for i in items_db if i.id == item_id),None)
    
    items_db.remove(bd_item)
    return {"message": f"Item {item_id} has been deleted.", "item": items_db}