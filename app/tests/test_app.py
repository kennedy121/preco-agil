import unittest
from unittest.mock import patch
from app import create_app

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        # Disable CSRF protection for testing forms
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()

    def test_index_page(self):
        """Test that the index page loads correctly and has the correct title."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Correctly check for the title in the response
        self.assertIn('Busca de Preços de Referência', response.data.decode('utf-8'))

    # Patch the price_collector to avoid real API calls
    @patch('app.services.price_collector.collect_prices')
    def test_search_with_query_and_results(self, mock_collect_prices):
        """Test that the search works with a valid query and returns results."""
        # Configure the mock to return some sample data
        mock_collect_prices.return_value = [
            {'fonte': 'TestAPI', 'valor_unitario': 10.5, 'descricao_item': 'caneta azul', 'data_compra': '2023-01-01'},
            {'fonte': 'TestAPI', 'valor_unitario': 11.0, 'descricao_item': 'caneta azul', 'data_compra': '2023-01-02'},
            {'fonte': 'TestAPI', 'valor_unitario': 10.0, 'descricao_item': 'caneta azul', 'data_compra': '2023-01-03'},
        ]

        response = self.client.get('/search?query=caneta')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')

        # Check that the main sections appear
        self.assertIn('Relatório de Pesquisa de Preços', response_text)
        self.assertIn('Análise Estatística', response_text)
        self.assertIn('Itens Coletados', response_text)

        # Check that the analysis shows a recommended value (the exact value depends on the data_analyzer logic)
        self.assertIn('Valor Recomendado', response_text)
        self.assertIn('10.50', response_text) # Median of [10.0, 10.5, 11.0] is 10.5

    @patch('app.services.price_collector.collect_prices')
    def test_search_with_no_results(self, mock_collect_prices):
        """Test the search page when no prices are found."""
        # Configure the mock to return an empty list
        mock_collect_prices.return_value = []

        response = self.client.get('/search?query=produto_inexistente')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')

        # Check that an appropriate message is shown
        self.assertIn('Nenhum preço foi encontrado', response_text)
        self.assertIn('Análise não realizada', response_text) # Check for the error message from the analyzer

    def test_search_without_query(self):
        """Test that the search page handles missing queries gracefully."""
        response = self.client.get('/search')
        self.assertEqual(response.status_code, 200)
        # Check for the specific error message for no query
        self.assertIn('Nenhum termo de pesquisa foi fornecido', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
