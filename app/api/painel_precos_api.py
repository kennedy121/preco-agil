import requests
import time
from config import RETRY_ATTEMPTS, RETRY_DELAY, MAX_PRICE_AGE_DAYS
from datetime import datetime, timedelta

# This is a hypothetical API client. The endpoints and data structures are illustrative.
BASE_URL = "https://paineldeprecos.planejamento.gov.br/api"

def search_prices(description: str, retries=RETRY_ATTEMPTS):
    """
    Searches for prices in the Painel de Preços, which aggregates data from various sources.

    Args:
        description (str): The description of the item to search for.
        retries (int): The number of times to retry the request.

    Returns:
        list: A list of dictionaries, each representing a found price.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=MAX_PRICE_AGE_DAYS)
    
    # The actual API endpoint might be different and require specific filters.
    endpoint = f"{BASE_URL}/analise-precos/v1/precos"
    params = {
        "q": description,
        "periodo_inicio": start_date.strftime('%Y-%m-%d'),
        "periodo_fim": end_date.strftime('%Y-%m-%d'),
        "page": 1,
        "size": 100
    }

    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1}/{retries} to fetch data from Painel de Preços...")
            response = requests.get(endpoint, params=params, timeout=30) # This can be slow
            response.raise_for_status()
            data = response.json().get("results", [])

            prices = []
            for item in data:
                prices.append({
                    "data_compra": item.get("data_compra"),
                    "fornecedor_cnpj": item.get("cnpj_fornecedor"),
                    "fornecedor_nome": item.get("nome_fornecedor"),
                    "orgao_comprador": item.get("nome_orgao"),
                    "uf_comprador": item.get("uf_unidade"),
                    "valor_unitario": item.get("preco_unitario_homologado"),
                    "descricao_item": item.get("descricao_item_licitacao"),
                    "quantidade": item.get("quantidade_item"),
                    "fonte": "Painel de Preços"
                })
            
            print(f"Successfully fetched {len(prices)} prices from Painel de Preços.")
            return prices

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for Painel de Preços API: {e}")
            if attempt < retries - 1:
                wait_time = RETRY_DELAY ** (attempt + 1)
                print(f"Waiting {wait_time} seconds before next retry.")
                time.sleep(wait_time)

    print("All retries failed for Painel de Preços API.")
    return []
