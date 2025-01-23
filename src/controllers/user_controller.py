from flask import Blueprint, request, jsonify
from models.models import db, User, Order, Product
from services.data_processor import UserDataProcessor
from sqlalchemy.exc import IntegrityError
import traceback
from datetime import datetime

user_blueprint = Blueprint('user', __name__)
data_processor = UserDataProcessor()



@user_blueprint.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    lines = file.stream.read().decode('utf-8').splitlines()

    try:
        users_data = data_processor.process(lines)
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
        traceback.print_exc()  # Adiciona detalhes do traceback no log
        return jsonify({"error": f"Error processing file: {str(e)}"}), 400

    try:
        for user_data in users_data:
            with db.session.no_autoflush:
                user = User.query.filter_by(user_id=user_data.user_id).first()
                if not user:
                    user = User(user_id=user_data.user_id, name=user_data.name)
                    db.session.add(user)

                for order_data in user_data.orders:
                    existing_order = Order.query.filter_by(id=order_data.id).first()
                    if not existing_order:
                        order = Order(
                            id=order_data.id,
                            user_id=user.user_id,
                            date=order_data.date,
                            total=order_data.total
                        )
                        db.session.add(order)
                    else:
                        # Atualiza os valores do pedido, se necessário
                        existing_order.date = order_data.date
                        existing_order.total = order_data.total

                    for product_data in order_data.products:
                        existing_product = Product.query.filter_by(
                            order_id=order_data.id, product_id=product_data.product_id
                        ).first()
                        if not existing_product:
                            product = Product(
                                order_id=order_data.id,
                                product_id=product_data.product_id,
                                value=product_data.value
                            )
                            db.session.add(product)

        db.session.commit()
        return jsonify({"message": "File processed and data saved successfully"}), 201
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")
        db.session.rollback()
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@user_blueprint.route('/users', methods=['GET'])
def get_users():
    user_id = request.args.get('user_id', type=int)
    date_filter = request.args.get('date')

    # Validação da data, se fornecida
    if date_filter:
        try:
            date_filter = datetime.strptime(date_filter, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    if user_id:
        # Busca o usuário pelo ID
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Filtra os pedidos por data, se necessário
        orders = [
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
            if not date_filter or order.date == date_filter
        ]

        response = {
            "user_id": user.user_id, 
            "name": user.name,
            "orders": orders,
        }
    else:
        # Busca todos os usuários
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
                    if not date_filter or order.date == date_filter
                ],
            }
            for user in users
        ]

    return jsonify(response)

