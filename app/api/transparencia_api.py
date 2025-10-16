import requests
import time
import os
from config import RETRY_ATTEMPTS, RETRY_DELAY

# NOTE: This API requires a key, which should be stored as an environment variable.
BASE_URL = "https://api.portaldatransparencia.gov.br/api-de-dados"
API_KEY = os.environ.get("TRANSPARENCIA_API_KEY", "") # Securely get key

def search_expenses(description: str, retries=RETRY_ATTEMPTS):
    """
    Searches for federal expenses related to a description in the Portal da Transparência API.

    Args:
        description (str): The description of the item to search for.
        retries (int): The number of times to retry the request.

    Returns:
        list: A list of dictionaries, where each dictionary represents a price from an expense record.
              Returns an empty list if the API key is missing or the call fails.
    """
    if not API_KEY:
        print("ERROR: TRANSPARENCIA_API_KEY environment variable not set. Skipping search.")
        return []

    # This is a hypothetical endpoint for searching for items in expenses.
    # The actual API may require a different approach (e.g., searching by contract).
    endpoint = f"{BASE_URL}/despesas/documentos"
    headers = {
        "chave-api-dados": API_KEY
    }
    params = {
        "descricao": description, # This parameter might not exist; it's a guess.
        "pagina": 1
    }

    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1}/{retries} to fetch data from Portal da Transparência...")
            response = requests.get(endpoint, headers=headers, params=params, timeout=20)
            response.raise_for_status()
            data = response.json()

            prices = []
            # This data structure is a pure assumption.
            for expense in data:
                prices.append({
                    "data_compra": expense.get("data"),
                    "fornecedor_cnpj": expense.get("cnpjFornecedor"),
                    "fornecedor_nome": expense.get("nomeFornecedor"),
                    "orgao_comprador": expense.get("orgao"),
                    "uf_comprador": None, # May not be available at this level
                    "valor_unitario": expense.get("valor"),
                    "descricao_item": expense.get("descricao"),
                    "quantidade": 1, # Often, expense records don't have quantity
                    "fonte": "Portal da Transparência"
                })
            
            print(f"Successfully fetched {len(prices)} prices from Portal da Transparência.")
            return prices

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for Portal da Transparência API: {e}")
            if attempt < retries - 1:
                wait_time = RETRY_DELAY ** (attempt + 1)
                print(f"Waiting {wait_time} seconds before next retry.")
                time.sleep(wait_time)

    print("All retries failed for Portal da Transparência API.")
    return []
