from sqlmodel import  Session, select
from typing import List
from fastapi import  APIRouter, Depends, HTTPException
from models import *
from database import get_session
from pydantic import BaseModel

router = APIRouter()

# schema for item creation
class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float


# Create item endpoint
@router.post("/items/", response_model=Item)
async def create_item(viewModel: ItemCreate, session:Session=  Depends(get_session)):
    db_item = Item(name=viewModel.name, description=viewModel.description , price=viewModel.price)
    # db_item = Item()
    # db_item.name = viewModel.name
    # db_item.description = viewModel.description
    # db_item.price = viewModel.price
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

# Read all items endpoint
@router.get("/items/", response_model=List[Item])
def read_items(session: Session = Depends(get_session)):
    items = session.exec(select(Item)).all()
    return items

# Read single item by ID endpoint
@router.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Update item endpoint
@router.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: ItemCreate, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.name = updated_item.name
    item.description = updated_item.description
    item.price = updated_item.price
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

# Delete item endpoint
@router.delete("/items/{item_id}")
def delete_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
    return {"ok": True}