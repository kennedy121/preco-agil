
# app/api/pncp_api.py
import requests
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta

class PNCPClient:
    """Cliente para API do PNCP - Portal Nacional de Contratações Públicas"""
    
    def __init__(self):
        self.base_url = "https://pncp.gov.br/api/consulta/v1"
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        })
        
        # Adiciona a chave da API se estiver disponível no ambiente
        api_key = os.getenv('PNCP_API_KEY')
        if api_key:
            self.session.headers.update({'chave-api-dados': api_key})
            print("🔑 Chave da API do PNCP configurada.")
    
    def search_contracts(
        self,
        item_code: str,
        catalog_type: str,
        max_days: int = 365,
        region: Optional[str] = None
    ) -> List[Dict]:
        """Busca contratos no PNCP"""
        
        # O debug foi removido pois a causa raiz foi encontrada
        
        endpoint = f"{self.base_url}/contratos"
        date_limit = datetime.now() - timedelta(days=max_days)
        
        params = {
            'codigoItem': item_code,
            'dataInicial': date_limit.strftime('%Y-%m-%d'),
            'dataFinal': datetime.now().strftime('%Y-%m-%d'),
            'tamanhoPagina': 50
        }
        
        if region:
            params['uf'] = region
        
        try:
            response = self.session.get(endpoint, params=params, timeout=15)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    contracts = data.get('data', [])
                    return self._parse_contracts(contracts)
                except ValueError:
                    return [] # Falha no JSON
            else:
                return [] # Status de erro
        
        except requests.exceptions.RequestException:
            return [] # Erro de conexão/timeout
    
    def _parse_contracts(self, contracts: List[Dict]) -> List[Dict]:
        """Processa a lista de contratos retornada pela API do PNCP."""
        items = []
        
        for contract in contracts:
            try:
                # Prioriza valor unitário, se não, global
                valor = contract.get('valorUnitarioContratado') or contract.get('valorGlobal')
                
                if not valor or float(valor) <= 0:
                    continue
                
                data_str = contract.get('dataAssinatura')
                data_obj = datetime.fromisoformat(data_str.split('T')[0]) if data_str else datetime.now()
                
                supplier_info = contract.get('fornecedor', {})
                
                items.append({
                    'source': 'PNCP',
                    'price': float(valor),
                    'date': data_obj,
                    'supplier': supplier_info.get('nome', 'N/A'),
                    'supplier_cnpj': supplier_info.get('documento', 'N/A'),
                    'entity': contract.get('orgaoEntidade', {}).get('razaoSocial', 'N/A'),
                    'region': contract.get('municipio', {}).get('uf', {}).get('sigla'),
                    'description': contract.get('objetoContrato', 'N/A'),
                    'url': f"https://pncp.gov.br/app/contrato/{contract.get('id')}"
                })
            except (ValueError, KeyError, TypeError):
                # Pula contrato se algum campo essencial estiver faltando ou mal formatado
                continue
        
        return items
