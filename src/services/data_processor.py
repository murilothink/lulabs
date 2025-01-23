from models.models import User, Order, Product
from datetime import datetime



class UserDataProcessor:
    def process(self, lines):
        users_data = []

        for line in lines:
            try:
                # Extração dos campos
                user_id = int(line[:10].strip().lstrip('0') or -1)
                name = line[10:55].strip()
                order_id = int(line[55:65].strip().lstrip('0') or -1)
                product_id = int(line[65:75].strip().lstrip('0') or 0)  # Permitir product_id = 0
                value_str = line[75:87].strip()
                date_str = line[87:95].strip()

                # Conversão dos campos válidos
                value = float(value_str)
                date = datetime.strptime(date_str, '%Y%m%d').date()

            except Exception as e:
                # Registro do erro e continuação
                print(f"Erro ao processar linha: {line}. Detalhes: {e}")
                continue

            # Verifica se o usuário já existe
            user = next((u for u in users_data if u.user_id == user_id), None)
            if not user:
                user = User(user_id=user_id, name=name, orders=[])
                users_data.append(user)

            # Verifica se o pedido já existe
            order = next((o for o in user.orders if o.id == order_id), None)
            if not order:
                order = Order(id=order_id, date=date, total=0.0)
                user.orders.append(order)

            # Adiciona o produto ao pedido (mesmo se product_id = 0)
            product = Product(product_id=product_id, value=value, order_id=order.id)
            order.products.append(product)
            order.total += value

        return users_data


