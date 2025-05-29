from fastapi import FastAPI, HTTPException
from models import MenuItem, Order
from schemas import MenuItemSchema, OrderCreateSchema, OrderSchema
from database import menu_db, order_db

app = FastAPI(title="카페 주문 관리 API")

@app.get("/menu", response_model=list[MenuItemSchema])
def get_menu():
    """전체 메뉴 조회"""
    return menu_db

@app.get("/menu/{item_id}", response_model=MenuItemSchema)
def get_menu_item(item_id: int):
    """특정 메뉴 아이템 조회"""
    for item in menu_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="메뉴를 찾을 수 없습니다.")

@app.post("/orders", response_model=OrderSchema)
def create_order(order: OrderCreateSchema):
    """새 주문 생성"""
    new_order = Order(id=len(order_db)+1, **order.dict())
    order_db.append(new_order)
    return new_order

@app.get("/orders/{order_id}", response_model=OrderSchema)
def get_order(order_id: int):
    """주문 상세 조회"""
    for order in order_db:
        if order.id == order_id:
            return order
    raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다.") 