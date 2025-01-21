from typing import List, Dict, Any

class Order:
    def __init__(self, order_id: int, date: str, products: List[Dict[str, Any]], total: float):
        self.order_id = order_id
        self.date = date
        self.products = products
        self.total = total