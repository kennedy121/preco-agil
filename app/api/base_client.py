
# app/api/base_client.py
"""
Cliente base para todas as APIs governamentais
Implementa retry, rate limiting, cache e logging
"""

import requests
import time
import logging
from typing import Optional, Dict, Any, Callable
from functools import wraps
from datetime import datetime, timedelta
from collections import defaultdict
import threading

logger = logging.getLogger(__name__)


class CacheManager:
    """Gerenciador de cache com expiração automática"""
    
    def __init__(self, ttl_seconds: int = 3600, max_size: int = 1000):
        self._cache: Dict[str, Any] = {}
        self._timestamps: Dict[str, datetime] = {}
        self.ttl = timedelta(seconds=ttl_seconds)
        self.max_size = max_size
        self._lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """Recupera item do cache se não expirado"""
        with self._lock:
            if key not in self._cache:
                return None
            
            # Verifica expiração
            if datetime.now() - self._timestamps[key] > self.ttl:
                self._remove(key)
                return None
            
            return self._cache[key]
    
    def set(self, key: str, value: Any) -> None:
        """Armazena item no cache"""
        with self._lock:
            # Limpa cache se muito grande
            if len(self._cache) >= self.max_size:
                self._cleanup()
            
            self._cache[key] = value
            self._timestamps[key] = datetime.now()
    
    def _remove(self, key: str) -> None:
        """Remove item do cache"""
        if key in self._cache:
            del self._cache[key]
        if key in self._timestamps:
            del self._timestamps[key]
    
    def _cleanup(self) -> None:
        """Remove 20% dos itens mais antigos"""
        remove_count = int(self.max_size * 0.2)
        sorted_items = sorted(self._timestamps.items(), key=lambda x: x[1])
        
        for key, _ in sorted_items[:remove_count]:
            self._remove(key)
        
        logger.info(f"Cache cleanup: removidos {remove_count} itens")
    
    def clear(self) -> None:
        """Limpa todo o cache"""
        with self._lock:
            self._cache.clear()
            self._timestamps.clear()


class RateLimiter:
    """Rate limiter thread-safe"""
    
    def __init__(self):
        self._calls: Dict[str, list] = defaultdict(list)
        self._lock = threading.Lock()
    
    def is_allowed(self, key: str, max_calls: int, period_seconds: int) -> bool:
        """Verifica se chamada é permitida"""
        with self._lock:
            now = datetime.now()
            cutoff = now - timedelta(seconds=period_seconds)
            
            # Remove chamadas antigas
            self._calls[key] = [
                call_time for call_time in self._calls[key]
                if call_time > cutoff
            ]
            
            # Verifica limite
            if len(self._calls[key]) < max_calls:
                self._calls[key].append(now)
                return True
            
            return False
    
    def wait_if_needed(self, key: str, max_calls: int, period_seconds: int) -> None:
        """Aguarda se necessário para respeitar rate limit"""
        while not self.is_allowed(key, max_calls, period_seconds):
            wait_time = 1.0
            logger.warning(f"Rate limit atingido para {key}, aguardando {wait_time}s")
            time.sleep(wait_time)


class BaseAPIClient:
    """Cliente base com funcionalidades comuns"""
    
    def __init__(
        self, 
        base_url: str,
        timeout: int = 30,
        max_retries: int = 3,
        rate_limit_calls: int = 30,
        rate_limit_period: int = 60,
        cache_ttl: int = 3600
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        
        # Session reutilizável
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'PrecoAgil/1.0'
        })
        
        # Gerenciadores
        self.cache = CacheManager(ttl_seconds=cache_ttl)
        self.rate_limiter = RateLimiter()
        self.rate_limit_calls = rate_limit_calls
        self.rate_limit_period = rate_limit_period
    
    def _get_cache_key(self, endpoint: str, params: Dict) -> str:
        """Gera chave única para cache"""
        import hashlib
        import json
        
        data = f"{endpoint}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def _request_with_retry(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        use_cache: bool = True,
        **kwargs
    ) -> Optional[Dict]:
        """Faz requisição com retry, rate limiting e cache"""
        
        # Verifica cache
        if use_cache and method.upper() == 'GET':
            cache_key = self._get_cache_key(endpoint, params or {})
            cached = self.cache.get(cache_key)
            if cached is not None:
                logger.debug(f"Cache hit para {endpoint}")
                return cached
        
        # Rate limiting
        rate_key = f"{self.__class__.__name__}:{endpoint}"
        self.rate_limiter.wait_if_needed(
            rate_key, 
            self.rate_limit_calls, 
            self.rate_limit_period
        )
        
        # Retry com backoff exponencial
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                response = self.session.request(
                    method=method,
                    url=f"{self.base_url}{endpoint}",
                    params=params,
                    timeout=self.timeout,
                    **kwargs
                )
                
                response.raise_for_status()
                data = response.json()
                
                # Armazena em cache
                if use_cache and method.upper() == 'GET':
                    self.cache.set(cache_key, data)
                
                logger.debug(f"Sucesso: {method} {endpoint}")
                return data
                
            except requests.exceptions.Timeout as e:
                last_exception = e
                logger.warning(f"Timeout na tentativa {attempt + 1}/{self.max_retries}: {endpoint}")
                
            except requests.exceptions.HTTPError as e:
                status = e.response.status_code
                
                # Não retenta em alguns casos
                if status in [400, 401, 403, 404]:
                    logger.error(f"Erro HTTP {status} (não retentável): {endpoint}")
                    return None
                
                last_exception = e
                logger.warning(f"Erro HTTP {status} na tentativa {attempt + 1}/{self.max_retries}")
                
            except requests.exceptions.RequestException as e:
                last_exception = e
                logger.warning(f"Erro na tentativa {attempt + 1}/{self.max_retries}: {e}")
            
            # Backoff exponencial
            if attempt < self.max_retries - 1:
                wait_time = 2 ** attempt  # 1s, 2s, 4s
                logger.info(f"Aguardando {wait_time}s antes de retentar...")
                time.sleep(wait_time)
        
        # Todas as tentativas falharam
        logger.error(f"Todas as {self.max_retries} tentativas falharam para {endpoint}: {last_exception}")
        return None
    
    def get(self, endpoint: str, params: Optional[Dict] = None, use_cache: bool = True) -> Optional[Dict]:
        """GET request"""
        return self._request_with_retry('GET', endpoint, params, use_cache)
    
    def post(self, endpoint: str, data: Optional[Dict] = None, use_cache: bool = False) -> Optional[Dict]:
        """POST request"""
        return self._request_with_retry('POST', endpoint, json=data, use_cache=use_cache)
