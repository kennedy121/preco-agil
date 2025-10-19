
# app/api/comprasnet_api.py
"""
Cliente para ComprasNet
Documentação: https://compras.dados.gov.br/docs/
"""

import logging
from typing import List, Dict
from datetime import datetime
from app.api.base_client import BaseAPIClient

logger = logging.getLogger(__name__)


class ComprasNetClient(BaseAPIClient):
    """Cliente para API do ComprasNet"""
    
    def __init__(self):
        super().__init__(
            base_url='http://compras.dados.gov.br/compradores/v1',
            timeout=15,
            max_retries=2,
            rate_limit_calls=20,  # Mais conservador
            cache_ttl=3600
        )
    
    def search_material(self, item_code: str, max_pages: int = 2) -> List[Dict]:
        """Busca materiais por código CATMAT"""
        logger.info(f"Buscando materiais ComprasNet: {item_code}")
        return self._search_items('/materiais', 'codigoItemMaterial', item_code, max_pages, 'materiais')
    
    def search_service(self, item_code: str, max_pages: int = 2) -> List[Dict]:
        """Busca serviços por código CATSER"""
        logger.info(f"Buscando serviços ComprasNet: {item_code}")
        return self._search_items('/servicos', 'codigoItemServico', item_code, max_pages, 'servicos')
    
    def _search_items(
        self, 
        endpoint: str, 
        param_name: str, 
        item_code: str, 
        max_pages: int,
        data_key: str
    ) -> List[Dict]:
        """Busca itens com paginação"""
        all_items = []
        
        for page in range(1, max_pages + 1):
            params = {
                param_name: item_code,
                'pagina': page
            }
            
            data = self.get(endpoint, params)
            
            if not data:
                break
            
            items = data.get('_embedded', {}).get(data_key, [])
            
            if not items:
                logger.debug(f"Página {page} sem resultados, parando")
                break
            
            all_items.extend(self._parse_items(items))
            logger.debug(f"Página {page}: {len(items)} itens")
        
        logger.info(f"ComprasNet: total de {len(all_items)} itens coletados")
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
                    date_obj = datetime.fromisoformat(data_str.split('T')[0])
                else:
                    continue
                
                parsed.append({
                    'source': 'ComprasNet',
                    'price': float(valor),
                    'date': date_obj,
                    'supplier': item.get('fornecedor', 'N/A'),
                    'entity': item.get('orgao', 'N/A'),
                    'region': item.get('uf', 'N/A')
                })
                
            except (ValueError, KeyError, TypeError) as e:
                logger.debug(f"Item ignorado: {e}")
                continue
        
        return parsed
