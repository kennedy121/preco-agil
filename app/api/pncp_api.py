
# app/api/pncp_api.py
"""
Cliente para PNCP - Portal Nacional de Contratações Públicas
Documentação: https://pncp.gov.br/api/swagger-ui/index.html
"""

import os
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from app.api.base_client import BaseAPIClient

logger = logging.getLogger(__name__)


class PNCPClient(BaseAPIClient):
    """Cliente para API do PNCP"""
    
    def __init__(self):
        super().__init__(
            base_url='https://pncp.gov.br/api/consulta/v1',
            timeout=30,
            max_retries=3,
            cache_ttl=3600  # 1 hora
        )
        
        # Chave de API (se necessário)
        api_key = os.getenv('PNCP_API_KEY')
        if api_key:
            self.session.headers.update({'chave-api-dados': api_key})
            logger.info("✅ Chave da API do PNCP configurada")
    
    def search_contracts(
        self,
        item_code: str,
        catalog_type: str,
        max_days: int = 365,
        region: Optional[str] = None
    ) -> List[Dict]:
        """
        Busca contratos por código de item
        
        Args:
            item_code: Código CATMAT/CATSER
            catalog_type: 'material' ou 'servico'
            max_days: Período máximo em dias
            region: UF (opcional)
        
        Returns:
            Lista de contratos formatados
        """
        endpoint = '/contratos'
        date_limit = datetime.now() - timedelta(days=max_days)
        
        params = {
            'codigoItem': item_code,
            'dataInicial': date_limit.strftime('%Y-%m-%d'),
            'dataFinal': datetime.now().strftime('%Y-%m-%d'),
            'tamanhoPagina': 50
        }
        
        if region:
            params['uf'] = region
        
        logger.info(f"Buscando contratos PNCP: item={item_code}, tipo={catalog_type}")
        
        data = self.get(endpoint, params)
        
        if not data:
            logger.warning("Nenhum dado retornado do PNCP")
            return []
        
        contracts = data.get('data', [])
        logger.info(f"PNCP retornou {len(contracts)} contratos brutos")
        
        parsed = self._parse_contracts(contracts)
        logger.info(f"PNCP: {len(parsed)} contratos válidos após parsing")
        
        return parsed
    
    def _parse_contracts(self, contracts: List[Dict]) -> List[Dict]:
        """Processa contratos retornados"""
        items = []
        
        for contract in contracts:
            try:
                # Valor (prioriza unitário)
                valor = contract.get('valorUnitarioContratado') or contract.get('valorGlobal')
                if not valor or float(valor) <= 0:
                    continue
                
                # Data
                data_str = contract.get('dataAssinatura')
                if data_str:
                    date_obj = datetime.fromisoformat(data_str.split('T')[0])
                else:
                    continue
                
                supplier_info = contract.get('fornecedor', {})
                entity_info = contract.get('orgaoEntidade', {})
                municipio_info = contract.get('municipio', {})
                
                items.append({
                    'source': 'PNCP',
                    'price': float(valor),
                    'date': date_obj,
                    'supplier': supplier_info.get('nome', 'N/A'),
                    'supplier_cnpj': supplier_info.get('documento', 'N/A'),
                    'entity': entity_info.get('razaoSocial', 'N/A'),
                    'region': municipio_info.get('uf', {}).get('sigla'),
                    'description': contract.get('objetoContrato', 'N/A'),
                    'url': f"https://pncp.gov.br/app/contrato/{contract.get('id')}"
                })
                
            except (ValueError, KeyError, TypeError) as e:
                logger.debug(f"Contrato ignorado (erro no parse): {e}")
                continue
        
        return items
