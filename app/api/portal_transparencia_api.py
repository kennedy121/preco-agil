
# app/api/portal_transparencia_api.py
"""
Cliente para Portal da Transparência (CGU)
Documentação: https://portaldatransparencia.gov.br/api-de-dados
"""

import os
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from app.api.base_client import BaseAPIClient

logger = logging.getLogger(__name__)


class PortalTransparenciaClient(BaseAPIClient):
    """Cliente para API do Portal da Transparência"""
    
    def __init__(self):
        api_key = os.getenv('PORTAL_TRANSPARENCIA_API_KEY')
        
        super().__init__(
            base_url='https://api.portaldatransparencia.gov.br/api-de-dados',
            timeout=30,
            max_retries=3,
            rate_limit_calls=10,  # API tem limite rigoroso
            cache_ttl=3600
        )
        
        if not api_key:
            logger.warning("⚠️ PORTAL_TRANSPARENCIA_API_KEY não configurada")
            self.api_key = None
        else:
            self.api_key = api_key
            self.session.headers.update({'chave-api-dados': api_key})
            logger.info("✅ API do Portal da Transparência configurada")
    
    def search_contracts(
        self,
        item_description: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        page: int = 1
    ) -> List[Dict]:
        """
        Busca contratos por descrição
        
        Args:
            item_description: Termos de busca
            start_date: Data inicial (dd/mm/yyyy)
            end_date: Data final (dd/mm/yyyy)
            page: Página
        
        Returns:
            Lista de contratos
        """
        if not self.api_key:
            logger.warning("API key não configurada, pulando Portal Transparência")
            return []
        
        # Datas padrão
        if not end_date:
            end_date = datetime.now().strftime('%d/%m/%Y')
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365)).strftime('%d/%m/%Y')
        
        endpoint = '/contratos'
        params = {
            'dataInicial': start_date,
            'dataFinal': end_date,
            'pagina': page
        }
        
        logger.info(f"Buscando contratos Portal Transparência: {item_description[:30]}...")
        
        data = self.get(endpoint, params)
        
        if not data:
            return []
        
        # Filtra por descrição
        all_contracts = data if isinstance(data, list) else []
        
        contracts = [
            c for c in all_contracts 
            if item_description.lower() in c.get('objeto', '').lower()
        ]
        
        logger.info(f"Portal Transparência: {len(contracts)} contratos filtrados")
        
        return self._parse_contracts(contracts)
    
    def _parse_contracts(self, contracts: List[Dict]) -> List[Dict]:
        """Processa contratos"""
        items = []
        
        for contract in contracts:
            try:
                # Data
                date_str = contract.get('dataAssinatura')
                if date_str:
                    date_obj = datetime.strptime(date_str, '%d/%m/%Y')
                else:
                    continue
                
                # Valor
                valor = float(contract.get('valorInicial', 0))
                if valor <= 0:
                    continue
                
                fornecedor_info = contract.get('fornecedor', {})
                orgao_info = contract.get('orgaoVinculado', {})
                
                items.append({
                    'source': 'Portal da Transparência',
                    'price': valor,
                    'date': date_obj,
                    'supplier': fornecedor_info.get('nome'),
                    'supplier_cnpj': fornecedor_info.get('cnpj'),
                    'entity': orgao_info.get('nome'),
                    'contract_number': contract.get('numero'),
                    'object': contract.get('objeto'),
                    'modality': contract.get('modalidade')
                })
                
            except (ValueError, KeyError, TypeError) as e:
                logger.debug(f"Contrato ignorado: {e}")
                continue
        
        return items
