from typing import List
from models.order import Order

class User:
    def __init__(self, user_id: int, name: str, orders: List[Order]):
        self.user_id = user_id
        self.name = name
        self.orders = orders
