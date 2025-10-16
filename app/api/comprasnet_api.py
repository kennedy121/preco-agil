import requests
import time
from config import RETRY_ATTEMPTS, RETRY_DELAY, MAX_PRICE_AGE_DAYS

# This is a hypothetical API client. The endpoints and data structures are illustrative.
BASE_URL = "http://compras.dados.gov.br/pregoes/v1"

def search_historical_prices(description: str, retries=RETRY_ATTEMPTS):
    """
    Searches for historical prices of items in recent government procurement events.

    Args:
        description (str): The description of the item to search for.
        retries (int): The number of times to retry the request.

    Returns:
        list: A list of dictionaries, each representing a price found.
    """
    endpoint = f"{BASE_URL}/pregoes"
    params = {
        "item_descricao": description,
        "data_final": "", # Ideally, we would set a date range based on MAX_PRICE_AGE_DAYS
        "pagina": 1
    }

    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1}/{retries} to fetch data from ComprasNet...")
            response = requests.get(endpoint, params=params, timeout=15)
            response.raise_for_status()
            data = response.json().get("_embedded", {}).get("pregoes", [])

            prices = []
            for pregao in data:
                # This data structure is a pure assumption.
                prices.append({
                    "data_compra": pregao.get("data_publicacao"),
                    "fornecedor_cnpj": None, # May require another API call to get winner
                    "fornecedor_nome": None,
                    "orgao_comprador": pregao.get("uasg_nome"),
                    "uf_comprador": pregao.get("uasg_uf"),
                    "valor_unitario": pregao.get("valor_unitario_estimado"),
                    "descricao_item": pregao.get("objeto"),
                    "quantidade": pregao.get("quantidade_itens"),
                    "fonte": "ComprasNet"
                })
            
            print(f"Successfully fetched {len(prices)} prices from ComprasNet.")
            return prices

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for ComprasNet API: {e}")
            if attempt < retries - 1:
                wait_time = RETRY_DELAY ** (attempt + 1)
                print(f"Waiting {wait_time} seconds before next retry.")
                time.sleep(wait_time)

    print("All retries failed for ComprasNet API.")
    return []
