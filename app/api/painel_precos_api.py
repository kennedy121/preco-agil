
# app/api/painel_precos_api.py

import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging
from functools import lru_cache
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

class PainelPrecosClient:
    """
    Cliente para API do Painel de Preços (Gov Federal)
    
    Funcionalidades:
    - ✅ Retry automático com backoff
    - ✅ Cache inteligente
    - ✅ Rate limiting
    - ✅ Paginação automática
    - ✅ Validação de dados
    """
    
    BASE_URL = "https://paineldeprecos.planejamento.gov.br/api/v1"
    
    # Configurações
    MAX_RETRIES = 3
    BACKOFF_FACTOR = 0.5
    TIMEOUT = 30
    MAX_ITEMS_PER_REQUEST = 100  # API limita a 500, mas 100 é mais seguro
    
    def __init__(self, timeout: int = None):
        """
        Inicializa cliente do Painel de Preços
        
        Args:
            timeout: Timeout para requisições (default: 30s)
        """
        self.timeout = timeout or self.TIMEOUT
        self.session = self._create_session()
        
        # Cache simples (pode ser substituído por Redis)
        self._cache: Dict[str, tuple] = {}  # {key: (data, timestamp)}
        self._cache_ttl = 3600  # 1 hora
        
        # Rate limiting
        self._last_request_time = 0
        self._min_interval = 0.5  # Mínimo 0.5s entre requisições
    

    def _create_session(self) -> requests.Session:
        """Cria sessão com retry automático"""
        session = requests.Session()
        
        # Configurar retry strategy
        retry_strategy = Retry(
            total=self.MAX_RETRIES,
            backoff_factor=self.BACKOFF_FACTOR,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Headers
        session.headers.update({
            "User-Agent": "PrecoAgil/1.0 (Pesquisa de Precos)",
            "Accept": "application/json"
        })
        
        return session

    
    def _rate_limit(self):
        """Implementa rate limiting simples"""
        elapsed = time.time() - self._last_request_time
        if elapsed < self._min_interval:
            sleep_time = self._min_interval - elapsed
            logger.debug(f"Rate limiting: aguardando {sleep_time:.2f}s")
            time.sleep(sleep_time)
        self._last_request_time = time.time()
    
    def _get_cache(self, key: str) -> Optional[List[Dict]]:
        """Recupera item do cache se válido"""
        if key in self._cache:
            data, timestamp = self._cache[key]
            age = time.time() - timestamp
            
            if age < self._cache_ttl:
                logger.debug(f"Cache hit: {key} (idade: {age:.0f}s)")
                return data
            else:
                del self._cache[key]
                logger.debug(f"Cache expirado: {key}")
        
        return None
    
    def _set_cache(self, key: str, data: List[Dict]):
        """Armazena item no cache"""
        self._cache[key] = (data, time.time())
        
        if len(self._cache) > 100:
            items = sorted(self._cache.items(), key=lambda x: x[1][1])
            for key, _ in items[:20]:
                del self._cache[key]
            logger.debug(f"Cache limpo: removidos 20 itens antigos")
    

    def search_by_item(self, item_code: str, catalog_type: str = 'material', **kwargs) -> List[Dict]:
        """
        Busca preços de um item no Painel de Preços
        
        Args:
            item_code: Código do item
            catalog_type: Tipo do catálogo ('material' ou 'servico')
            **kwargs: Aceita parâmetros adicionais (region, max_days, etc) para compatibilidade
        """
        if 'item_type' in kwargs:
            catalog_type = kwargs['item_type']
        
        region = kwargs.get('region', None)
        max_results = kwargs.get('max_results', 1000)
        
        try:
            params = {
                'codigoItem': item_code,
                'tipo': 'material' if catalog_type == 'material' else 'servico'
            }
            
            if region:
                params['regiao'] = region
            
            results = self._search_with_pagination(
                params=params,
                max_results=max_results
            )
            
            return results
            
        except Exception as e:
            print(f"   ⚠️ Erro: {e}")
            return []
    
    
    def _search_with_pagination(self, params: Dict, max_results: int = 1000) -> List[Dict]:
        """Busca com paginação automática"""
        all_results = []
        page = 1
        
        while len(all_results) < max_results:
            params['page'] = page
            
            try:
                response = self.session.get(
                    f"{self.BASE_URL}/compras",
                    params=params,
                    timeout=30
                )
                
                if response.status_code != 200:
                    print(f"   ⚠️ Status {response.status_code}: {response.text[:200]}")
                    break
                
                if not response.text or 'application/json' not in response.headers.get('Content-Type', ''):
                    print(f"   ⚠️ Resposta inesperada da API: {response.text[:500]}")
                    break
                
                data = response.json()
                items = data.get('_embedded', {}).get('compras', [])

                if not items:
                    break

                all_results.extend(self._parse_items(items))
                page += 1

            except requests.exceptions.JSONDecodeError as e:
                print(f"   ⚠️ Erro ao decodificar JSON: {e}")
                print(f"   📄 Resposta recebida: {response.text[:500]}")
                break
            except Exception as e:
                print(f"   ❌ Erro inesperado: {e}")
                break
        
        return all_results

    
    def _parse_items(self, items: List[Dict]) -> List[Dict]:
        """
        Processa e valida itens retornados pela API
        """
        parsed = []
        
        for item in items:
            try:
                price = self._extract_price(item)
                if price is None or price <= 0:
                    continue
                
                date = self._extract_date(item)
                if date is None:
                    continue
                
                result = {
                    "source": "Painel de Preços",
                    "price": price,
                    "date": date,
                    "quantity": self._extract_quantity(item),
                    "supplier": item.get("fornecedor_nome", "N/A"),
                    "supplier_cnpj": item.get("fornecedor_cpnj", None),
                    "entity": item.get("orgao_nome", "N/A"),
                    "region": item.get("uf", None),
                    "contract_number": item.get("numero_contrato", None),
                    "details_url": item.get("_links", {}).get("self", {}).get("href", None)
                }
                
                parsed.append(result)
                
            except Exception as e:
                logger.debug(f"⚠️ Item ignorado por erro: {e}")
                continue
        
        return parsed
    
    def _extract_price(self, item: Dict) -> Optional[float]:
        """Extrai preço unitário"""
        try:
            price = (
                item.get("valor_unitario") or
                item.get("valor_unitario_homologado") or
                item.get("preco_unitario") or
                item.get("preco")
            )
            
            if price is None:
                return None
            
            return float(price)
        
        except (ValueError, TypeError):
            return None
    
    def _extract_date(self, item: Dict) -> Optional[datetime]:
        """Extrai data de forma robusta"""
        try:
            date_str = (
                item.get("data_assinatura") or
                item.get("data_contrato") or
                item.get("data_compra")
            )
            
            if not date_str:
                return None
            
            date_str = date_str.split("T")[0]
            
            return datetime.strptime(date_str, "%Y-%m-%d")
        
        except (ValueError, AttributeError):
            return None
    
    def _extract_quantity(self, item: Dict) -> int:
        """Extrai quantidade (com fallback para 1)"""
        try:
            qty = item.get("quantidade") or item.get("quantidade_item")
            return int(qty) if qty else 1
        except (ValueError, TypeError):
            return 1
    
    def clear_cache(self):
        """Limpa o cache manualmente"""
        self._cache.clear()
        logger.info("🧹 Cache limpo manualmente")
    
    def get_cache_stats(self) -> Dict:
        """Retorna estatísticas do cache"""
        total_items = len(self._cache)
        
        if total_items == 0:
            return {"total_items": 0, "avg_age": 0, "oldest": 0}
        
        now = time.time()
        ages = [now - timestamp for _, (_, timestamp) in self._cache.items()]
        
        return {
            "total_items": total_items,
            "avg_age": sum(ages) / len(ages),
            "oldest": max(ages) if ages else 0,
            "newest": min(ages) if ages else 0
        }
