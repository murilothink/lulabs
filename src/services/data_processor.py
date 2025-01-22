from models.models import User, Order, Product

class UserDataProcessor:
    def process(self, lines):
        users_data = []

        for line in lines:
            user_id = int(line[:10].lstrip('0'))
            name = line[10:55].strip()
            order_id = int(line[55:65].lstrip('0'))
            product_id = int(line[65:75].lstrip('0'))

            # Corrige espaços no valor
            value_str = line[75:87].strip()
            try:
                value = float(value_str.replace(' ', ''))
            except ValueError as e:
                print(f"Erro ao processar valor: '{value_str}' na linha: {line}")
                raise e

            date = line[87:95]

            user = next((u for u in users_data if u.user_id == user_id), None)
            if not user:
                user = User(user_id=user_id, name=name, orders=[])
                users_data.append(user)

            order = next((o for o in user.orders if o.id == order_id), None)
            if not order:
                order = Order(id=order_id, date=date, total=0.0) 
                user.orders.append(order)

            product = Product(product_id=product_id, value=value, order_id=order.id)
            order.products.append(product)
            order.total += value

        return users_data
