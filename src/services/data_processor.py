from typing import List
from models.user import User
from models.order import Order
from interfaces.data_processor_interface import DataProcessor

class UserDataProcessor(DataProcessor):
    def process(self, lines: List[str]) -> List[User]:
        users = {}
        for line in lines:
            user_id = int(line[:10].lstrip('0'))
            name = line[10:55].strip()
            order_id = int(line[55:65].lstrip('0'))
            product_id = int(line[65:75].lstrip('0'))
            value = float(line[75:87].strip().replace(" ", ""))  # Remove espaços extras
            date = line[87:95]

            if user_id not in users:
                users[user_id] = User(user_id=user_id, name=name, orders=[])

            # Find or create order
            order = next((o for o in users[user_id].orders if o.order_id == order_id), None)
            if not order:
                order = Order(order_id=order_id, date=date, products=[], total=0.0)
                users[user_id].orders.append(order)

            # Add product to order
            order.products.append({"product_id": product_id, "value": value})
            order.total += value

        return list(users.values())