
# app/api/comprasnet_api.py
import requests
from typing import List, Dict
from datetime import datetime
import time

class ComprasNetClient:
    """Cliente para API do ComprasNet"""
    
    def __init__(self):
        self.base_url = "http://compras.dados.gov.br/compradores/v1"
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        })
    
    def search_material(self, item_code: str, max_pages: int = 2) -> List[Dict]:
        """Busca materiais no ComprasNet"""
        
        print(f"\n--- [DEBUG: COMPRASNET MATERIAL] ---")
        
        endpoint = f"{self.base_url}/materiais"
        
        all_items = []
        
        for page in range(1, max_pages + 1):
            params = {
                'codigoItemMaterial': item_code,
                'pagina': page
            }
            
            print(f"- Página {page}: {endpoint}")
            print(f"- Parâmetros: {params}")
            
            try:
                response = self.session.get(
                    endpoint, 
                    params=params, 
                    timeout=15
                )
                
                print(f"- Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    items = data.get('_embedded', {}).get('materiais', [])
                    
                    print(f"- Itens na página: {len(items)}")
                    
                    if not items:
                        break
                    
                    all_items.extend(self._parse_items(items))
                    time.sleep(0.5)  # Rate limiting
                else:
                    print(f"- ERRO: Status {response.status_code}")
                    break
                    
            except Exception as e:
                print(f"- ERRO: {str(e)[:100]}")
                break
        
        print(f"- Total de itens coletados: {len(all_items)}")
        return all_items
    
    def search_service(self, item_code: str, max_pages: int = 2) -> List[Dict]:
        """Busca serviços no ComprasNet"""
        
        print(f"\n--- [DEBUG: COMPRASNET SERVICO] ---")
        
        endpoint = f"{self.base_url}/servicos"
        
        all_items = []
        
        for page in range(1, max_pages + 1):
            params = {
                'codigoItemServico': item_code,
                'pagina': page
            }
            
            print(f"- Página {page}: {endpoint}")
            
            try:
                response = self.session.get(endpoint, params=params, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    items = data.get('_embedded', {}).get('servicos', [])
                    
                    if not items:
                        break
                    
                    all_items.extend(self._parse_items(items))
                    time.sleep(0.5)
                    
            except Exception as e:
                print(f"- ERRO: {str(e)[:100]}")
                break
        
        return all_items
    
    def _parse_items(self, items: List[Dict]) -> List[Dict]:
        """Processa itens do ComprasNet"""
        parsed = []
        
        for item in items:
            try:
                valor = item.get('valorUnitario')
                if not valor or float(valor) <= 0:
                    continue
                
                data_str = item.get('dataResultadoCompra', '')
                if data_str:
                    data_obj = datetime.fromisoformat(data_str.split('T')[0])
                else:
                    continue
                
                parsed.append({
                    'source': 'ComprasNet',
                    'price': float(valor),
                    'date': data_obj,
                    'supplier': item.get('fornecedor', 'N/A'),
                    'entity': item.get('orgao', 'N/A'),
                    'region': item.get('uf', 'N/A')
                })
            except (ValueError, KeyError, TypeError):
                continue
        
        return parsed
