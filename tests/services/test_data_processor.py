import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.services.data_processor import UserDataProcessor


class TestUserDataProcessor(unittest.TestCase):
    @patch('src.models.models.User')
    @patch('src.models.models.Order')
    @patch('src.models.models.Product')
    def test_process_valid_data(self, MockProduct, MockOrder, MockUser):
        # Configura os mocks para User, Order e Product
        mock_user_instance = MagicMock()
        MockUser.return_value = mock_user_instance

        mock_order_instance = MagicMock()
        MockOrder.return_value = mock_order_instance

        mock_product_instance = MagicMock()
        MockProduct.return_value = mock_product_instance

        # Dados de entrada
        lines = [
            "00000010000John Doe                        000000000100000000010000012345.67020230101",
            "0000010002Jane Smith                      00000000020000000002000000234.56020230102",
        ]

        # Cria uma instância do UserDataProcessor e processa os dados
        processor = UserDataProcessor()
        result = processor.process(lines)

        # Verifica se os mocks foram criados corretamente
        self.assertEqual(len(result), 2)  # Dois usuários
        MockUser.assert_any_call(user_id=1, name="John Doe", orders=[])
        MockUser.assert_any_call(user_id=2, name="Jane Smith", orders=[])

        MockOrder.assert_any_call(id=1, date=datetime(2023, 1, 1).date(), total=0.0)
        MockOrder.assert_any_call(id=2, date=datetime(2023, 1, 2).date(), total=0.0)

        MockProduct.assert_any_call(product_id=1, value=12345.67, order_id=1)
        MockProduct.assert_any_call(product_id=2, value=234.56, order_id=2)

    def test_process_invalid_data(self):
        # Dados de entrada com linhas inválidas
        lines = [
            "0000000000                            00000000000000000000        20230101",  # user_id ausente
            "0000000001John Doe                        0000000001abc0000012345.67020230101",  # valor inválido
            "0000000002Jane Smith                      00000000020000000002     ",  # data ausente
        ]

        # Cria uma instância do UserDataProcessor e processa os dados
        processor = UserDataProcessor()
        result = processor.process(lines)

        # Verifica se nenhum usuário foi processado
        self.assertEqual(len(result), 0)  # Nenhum usuário deve ser retornado

    @patch('src.models.models.User')
    @patch('src.models.models.Order')
    @patch('src.models.models.Product')
    def test_process_partial_data(self, MockProduct, MockOrder, MockUser):
        # Dados de entrada com linhas mistas (válidas e inválidas)
        lines = [
            "0000000001John Doe                        000000000100000000010000012345.67020230101",  # Válido
            "0000000002Jane Smith                      00000000020000000002     ",  # Inválido (data ausente)
        ]

        # Cria uma instância do UserDataProcessor e processa os dados
        processor = UserDataProcessor()
        result = processor.process(lines)

        # Verifica se apenas o usuário válido foi processado
        self.assertEqual(len(result), 1)  # Apenas 1 usuário deve ser retornado
        self.assertEqual(result[0].user_id, 1)