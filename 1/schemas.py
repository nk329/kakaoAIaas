from pydantic import BaseModel

class MenuItemSchema(BaseModel):
    id: int
    name: str
    price: int

class OrderCreateSchema(BaseModel):
    item_id: int
    quantity: int

class OrderSchema(BaseModel):
    id: int
    item_id: int
    quantity: int 