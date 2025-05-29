from pydantic import BaseModel

class MenuItem(BaseModel):
    id: int
    name: str
    price: int

class Order(BaseModel):
    id: int
    item_id: int
    quantity: int 