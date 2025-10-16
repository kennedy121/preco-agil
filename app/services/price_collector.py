from app.api import painel_precos_api, pncp_api, comprasnet_api, transparencia_api

def collect_prices(description: str) -> list:
    """
    Collects prices from all available data sources, in order of priority.

    Args:
        description (str): The description of the item to search for.

    Returns:
        list: A list of all unique prices found across all sources.
    """
    all_prices = []

    # 1. Painel de Preços (Priority 1)
    print("\n--- Starting search on Painel de Preços ---")
    prices_painel = painel_precos_api.search_prices(description)
    all_prices.extend(prices_painel)
    print(f"--- Found {len(prices_painel)} prices ---")

    # 2. PNCP (Priority 2)
    print("\n--- Starting search on PNCP ---")
    prices_pncp = pncp_api.search_contracts(description)
    all_prices.extend(prices_pncp)
    print(f"--- Found {len(prices_pncp)} prices ---")

    # 3. ComprasNet (Priority 3)
    print("\n--- Starting search on ComprasNet ---")
    prices_comprasnet = comprasnet_api.search_historical_prices(description)
    all_prices.extend(prices_comprasnet)
    print(f"--- Found {len(prices_comprasnet)} prices ---")

    # 4. Portal da Transparência (Priority 4)
    print("\n--- Starting search on Portal da Transparência ---")
    prices_transparencia = transparencia_api.search_expenses(description)
    all_prices.extend(prices_transparencia)
    print(f"--- Found {len(prices_transparencia)} prices ---")
    
    print(f"\nTotal prices collected before deduplication: {len(all_prices)}")

    # --- Deduplication --- #
    # A simple deduplication based on a few key fields.
    # More sophisticated methods may be needed for production.
    unique_prices = []
    seen_keys = set()
    for price in all_prices:
        # Create a unique key for each price entry
        key = (price.get('valor_unitario'), price.get('fornecedor_cnpj'), price.get('data_compra'))
        if key not in seen_keys:
            unique_prices.append(price)
            seen_keys.add(key)
            
    print(f"Total prices after deduplication: {len(unique_prices)}")

    return unique_prices
