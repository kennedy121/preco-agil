
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
            allowed_methods=["HEAD", "GET", "OPTIONS"]  # ✅ CORRETO (urllib3 >= 2.0)
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
                # Remove item expirado
                del self._cache[key]
                logger.debug(f"Cache expirado: {key}")
        
        return None
    
    def _set_cache(self, key: str, data: List[Dict]):
        """Armazena item no cache"""
        self._cache[key] = (data, time.time())
        
        # Limpa cache se muito grande (máximo 100 itens)
        if len(self._cache) > 100:
            # Remove os 20 mais antigos
            items = sorted(self._cache.items(), key=lambda x: x[1][1])
            for key, _ in items[:20]:
                del self._cache[key]
            logger.debug(f"Cache limpo: removidos 20 itens antigos")
    
    def search_by_item(
        self, 
        item_code: str, 
        item_type: str,
        region: Optional[str] = None,
        max_days: int = 365,
        max_results: int = 1000
    ) -> List[Dict]:
        """
        Busca preços de um item no Painel de Preços
        
        Args:
            item_code: Código CATMAT ou CATSER
            item_type: 'material' ou 'servico'
            region: Sigla do estado (SP, RJ, etc)
            max_days: Idade máxima dos preços em dias
            max_results: Número máximo de resultados
            
        Returns:
            Lista de dicionários com os preços encontrados
            
        Raises:
            ValueError: Se parâmetros inválidos
            ConnectionError: Se falha de conexão
        """
        
        # ✅ VALIDAÇÃO DE ENTRADA
        if not item_code or not item_code.strip():
            raise ValueError("❌ Código do item é obrigatório")
        
        if item_type not in ['material', 'servico']:
            raise ValueError(f"❌ Tipo inválido: {item_type}. Use 'material' ou 'servico'")
        
        item_code = item_code.strip()
        
        # Verifica cache
        cache_key = f"{item_code}_{item_type}_{region}_{max_days}"
        cached = self._get_cache(cache_key)
        if cached is not None:
            logger.info(f"✅ Retornando {len(cached)} preços do cache")
            return cached
        
        # Faz requisição
        try:
            logger.info(f"🔍 Buscando preços: {item_code} ({item_type})")
            
            results = self._search_with_pagination(
                item_code=item_code,
                item_type=item_type,
                region=region,
                max_days=max_days,
                max_results=max_results
            )
            
            # Armazena no cache
            if results:
                self._set_cache(cache_key, results)
            
            logger.info(f"✅ Encontrados {len(results)} preços no Painel")
            return results
            
        except requests.exceptions.Timeout:
            logger.error(f"⏱️ Timeout ao buscar {item_code} (>{self.timeout}s)")
            raise ConnectionError("Timeout na API do Painel de Preços")
        
        except requests.exceptions.ConnectionError as e:
            logger.error(f"🔌 Erro de conexão: {e}")
            raise ConnectionError("Erro de conexão com Painel de Preços")
        
        except requests.exceptions.HTTPError as e:
            logger.error(f"❌ Erro HTTP: {e}")
            
            if e.response.status_code == 429:
                raise ConnectionError("Rate limit excedido no Painel de Preços")
            elif e.response.status_code == 404:
                logger.info(f"ℹ️ Item {item_code} não encontrado no Painel")
                return []
            else:
                raise ConnectionError(f"Erro HTTP {e.response.status_code}")
        
        except Exception as e:
            logger.error(f"❌ Erro inesperado: {e}", exc_info=True)
            raise
    
    def _search_with_pagination(
        self,
        item_code: str,
        item_type: str,
        region: Optional[str],
        max_days: int,
        max_results: int
    ) -> List[Dict]:
        """Busca com paginação automática"""
        
        all_results = []
        page = 0
        
        while len(all_results) < max_results:
            # Rate limiting
            self._rate_limit()
            
            # Parâmetros da requisição
            params = {
                "codigo_item": item_code,
                "tipo": item_type,
                "offset": page * self.MAX_ITEMS_PER_REQUEST,
                "limit": self.MAX_ITEMS_PER_REQUEST
            }
            
            # Filtro por região
            if region:
                params["uf"] = region.upper()
            
            # Filtro por data
            date_limit = datetime.now() - timedelta(days=max_days)
            params["data_inicio"] = date_limit.strftime("%Y-%m-%d")
            
            logger.debug(f"📄 Página {page + 1}: {params}")
            
            # Requisição
            response = self.session.get(
                f"{self.BASE_URL}/contratacoes",
                params=params,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            
            # Parse JSON
            data = response.json()
            items = data.get("_embedded", {}).get("contracoes", [])
            
            if not items:
                logger.debug(f"ℹ️ Nenhum item na página {page + 1}, finalizando")
                break
            
            # Processa e adiciona
            parsed = self._parse_items(items)
            all_results.extend(parsed)
            
            logger.debug(f"✅ Página {page + 1}: {len(parsed)} itens válidos")
            
            # Se retornou menos que o limite, não há mais páginas
            if len(items) < self.MAX_ITEMS_PER_REQUEST:
                logger.debug("ℹ️ Última página alcançada")
                break
            
            page += 1
            
            # Proteção contra loop infinito
            if page > 50:
                logger.warning("⚠️ Limite de 50 páginas alcançado")
                break
        
        return all_results[:max_results]  # Garante o limite
    
    def _parse_items(self, items: List[Dict]) -> List[Dict]:
        """
        Processa e valida itens retornados pela API
        
        Args:
            items: Lista de itens brutos da API
            
        Returns:
            Lista de itens processados e validados
        """
        parsed = []
        
        for item in items:
            try:
                # Extrai e valida preço
                price = self._extract_price(item)
                if price is None or price <= 0:
                    continue
                
                # Extrai e valida data
                date = self._extract_date(item)
                if date is None:
                    continue
                
                # Monta resultado
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
            # Tenta vários campos possíveis
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
            
            # Remove timezone se houver (ex: "2024-01-01T00:00:00Z")
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
