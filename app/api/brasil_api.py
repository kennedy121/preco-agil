import requests
import time
from config import RETRY_ATTEMPTS, RETRY_DELAY

# This is a community-driven, free API. Good for supplementary data.
BASE_URL = "https://brasilapi.com.br/api"

def get_cnpj_details(cnpj: str, retries=RETRY_ATTEMPTS):
    """
    Fetches company details from the BrasilAPI based on a CNPJ.

    Args:
        cnpj (str): The CNPJ of the company to look up.
        retries (int): The number of times to retry the request.

    Returns:
        dict: A dictionary containing details about the company, or an empty dict on failure.
    """
    if not cnpj:
        return {}

    endpoint = f"{BASE_URL}/cnpj/v1/{cnpj}"
    
    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1}/{retries} to fetch CNPJ {cnpj} from BrasilAPI...")
            response = requests.get(endpoint, timeout=10)
            response.raise_for_status()
            print(f"Successfully fetched details for CNPJ {cnpj}.")
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for BrasilAPI (CNPJ {cnpj}): {e}")
            if attempt < retries - 1:
                wait_time = RETRY_DELAY ** (attempt + 1)
                print(f"Waiting {wait_time} seconds before next retry.")
                time.sleep(wait_time)
    
    print(f"All retries failed for CNPJ {cnpj}.")
    return {}
