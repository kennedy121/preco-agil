import requests
import time
from config import RETRY_ATTEMPTS, RETRY_DELAY, MAX_PRICE_AGE_DAYS
from datetime import datetime, timedelta

# This is a hypothetical API client. The endpoints and data structures are illustrative.
BASE_URL = "https://pncp.gov.br/api/pncp/v1"

def search_contracts(description: str, retries=RETRY_ATTEMPTS):
    """
    Searches for recent public contracts based on an item description.

    Args:
        description (str): The description of the item to search for.
        retries (int): The number of times to retry the request.

    Returns:
        list: A list of dictionaries, each representing a priced item from a contract.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=MAX_PRICE_AGE_DAYS)
    
    endpoint = f"{BASE_URL}/contratacoes/publicacao/search"
    params = {
        "q": description,
        "dataInicial": start_date.strftime('%Y-%m-%d'),
        "dataFinal": end_date.strftime('%Y-%m-%d'),
        "pagina": 1
    }

    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1}/{retries} to fetch data from PNCP...")
            response = requests.post(endpoint, json=params, timeout=20)
            response.raise_for_status()
            data = response.json().get("data", [])

            prices = []
            for contract in data:
                for item in contract.get("itens", []):
                    if description.lower() in item.get("descricao", "").lower():
                        prices.append({
                            "data_compra": contract.get("dataAssinatura"),
                            "fornecedor_cnpj": item.get("niFornecedor"),
                            "fornecedor_nome": item.get("nomeFornecedor"),
                            "orgao_comprador": contract.get("orgao"),
                            "uf_comprador": contract.get("uf"),
                            "valor_unitario": item.get("valorUnitario"),
                            "descricao_item": item.get("descricao"),
                            "quantidade": item.get("quantidade"),
                            "fonte": "PNCP"
                        })
            
            print(f"Successfully fetched {len(prices)} prices from PNCP.")
            return prices

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for PNCP API: {e}")
            if attempt < retries - 1:
                wait_time = RETRY_DELAY ** (attempt + 1)
                print(f"Waiting {wait_time} seconds before next retry.")
                time.sleep(wait_time)

    print("All retries failed for PNCP API.")
    return []
