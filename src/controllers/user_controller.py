from flask import Blueprint, request, jsonify
from typing import List, Dict, Any
from services.file_reader import FixedWidthFileReader
from services.data_processor import UserDataProcessor

user_blueprint = Blueprint('user', __name__)

file_reader = FixedWidthFileReader()
data_processor = UserDataProcessor()

# Variável global para armazenar os usuários processados
processed_users = []

@user_blueprint.route('/upload', methods=['POST'])
def upload_file():
    global processed_users  # Declaração da variável global para armazenar os usuários

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    lines = file.stream.read().decode('utf-8').splitlines()
    users = data_processor.process(lines)

    # Atualiza a variável global com os dados processados
    processed_users = users

    response = [
        {
            "user_id": user.user_id,
            "name": user.name,
            "orders": [
                {
                    "order_id": order.order_id,
                    "total": f"{order.total:.2f}",
                    "date": order.date,
                    "products": order.products
                } for order in user.orders
            ]
        } for user in users
    ]

    return jsonify({"message": "File processed successfully", "data": response})

@user_blueprint.route('/users', methods=['GET'])
def get_users():
    global processed_users  # Declaração da variável global para leitura dos dados

    user_id = request.args.get('user_id', type=int)

    if not processed_users:
        return jsonify({"error": "No data available. Please upload a file first."}), 400

    # Filtra pelo 'user_id'
    if user_id:
        filtered_users = [user for user in processed_users if user.user_id == user_id]
        if not filtered_users:
            return jsonify({"error": "User not found"}), 404

        # Retorna o usuário filtrado
        response = [
            {
                "user_id": user.user_id,
                "name": user.name,
                "orders": [
                    {
                        "order_id": order.order_id,
                        "total": f"{order.total:.2f}",
                        "date": order.date,
                        "products": order.products
                    } for order in user.orders
                ]
            } for user in filtered_users
        ]
    else:
        # Retorna todos os usuários
        response = [
            {
                "user_id": user.user_id,
                "name": user.name,
                "orders": [
                    {
                        "order_id": order.order_id,
                        "total": f"{order.total:.2f}",
                        "date": order.date,
                        "products": order.products
                    } for order in user.orders
                ]
            } for user in processed_users
        ]

    return jsonify(response)
