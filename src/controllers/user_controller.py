from flask import Blueprint, request, jsonify
from models.models import db, User, Order, Product
from services.data_processor import UserDataProcessor

user_blueprint = Blueprint('user', __name__)
data_processor = UserDataProcessor()

@user_blueprint.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    lines = file.stream.read().decode('utf-8').splitlines()

    users_data = data_processor.process(lines)

    # Salvar no banco de dados
    for user_data in users_data:
        # Busca o usuário
        user = User.query.filter_by(user_id=user_data.user_id).first()
        if not user:
            user = User(user_id=user_data.user_id, name=user_data.name)
            db.session.add(user)

        # Processar os pedidos associados ao usuário
        for order_data in user_data.orders:
            # Busca ou cria o pedido
            order = Order.query.filter_by(id=order_data.id, user_id=user.user_id).first()
            if not order:
                order = Order(id=order_data.id, user_id=user.user_id, date=order_data.date, total=order_data.total)
                db.session.add(order)

            # Processar os produtos associados ao pedido
            for product_data in order_data.products:
                if isinstance(product_data, dict):  
                    product = Product.query.filter_by(order_id=order.id, product_id=product_data['product_id']).first()
                    if not product:
                        product = Product(order_id=order.id, product_id=product_data['product_id'], value=product_data['value'])
                        db.session.add(product)
                else:
                    print(f"Unexpected product_data type: {type(product_data)}")

    db.session.commit()

    return jsonify({"message": "File processed and data saved successfully"}), 201

@user_blueprint.route('/users', methods=['GET'])
def get_users():
    user_id = request.args.get('user_id', type=int)

    if user_id:
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        response = {
            "user_id": user.user_id, 
            "name": user.name,
            "orders": [
                {
                    "order_id": order.id,
                    "total": f"{order.total:.2f}",
                    "date": order.date,
                    "products": [
                        {"product_id": product.product_id, "value": product.value}
                        for product in order.products
                    ],
                }
                for order in user.orders
            ],
        }
    else:
        users = User.query.all()
        response = [
            {
                "user_id": user.user_id,
                "name": user.name,
                "orders": [
                    {
                        "order_id": order.id,
                        "total": f"{order.total:.2f}",
                        "date": order.date,
                        "products": [
                            {"product_id": product.product_id, "value": product.value}
                            for product in order.products
                        ],
                    }
                    for order in user.orders
                ],
            }
            for user in users
        ]


    return jsonify(response)
