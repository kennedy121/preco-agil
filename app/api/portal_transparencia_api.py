# -*- coding: utf-8 -*-
"""
Cliente API Portal da Transparência
"""

import requests
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


class PortalTransparenciaClient:
    """Cliente para API do Portal da Transparência (CGU)"""
    
    def __init__(self):
        self.base_url = os.getenv(
            'PORTAL_TRANSPARENCIA_API_URL',
            'https://api.portaldatransparencia.gov.br/api-de-dados'
        )
        
        self.api_key = os.getenv('PORTAL_TRANSPARENCIA_API_KEY')
        
        if not self.api_key:
            print("⚠️ PORTAL_TRANSPARENCIA_API_KEY não configurada")
        else:
            print("✅ API Portal da Transparência OK")
        
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'chave-api-dados': self.api_key or ''
        })
    
    def search_contracts(
        self,
        item_description: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        max_results: int = 100
    ) -> List[Dict]:
        """Busca contratos por descrição"""
        
        if not self.api_key:
            print("  ⚠️ API key não configurada")
            return []
        
        if not end_date:
            end_date = datetime.now().strftime('%d/%m/%Y')
        
        if not start_date:
            start_date = (datetime.now() - timedelta(days=730)).strftime('%d/%m/%Y')
        
        endpoint = f"{self.base_url}/despesas/documentos"
        
        params = {
            'dataInicial': start_date,
            'dataFinal': end_date,
            'pagina': 1
        }
        
        print(f"  🔗 GET {endpoint}")
        
        try:
            response = self.session.get(endpoint, params=params, timeout=15)
            print(f"  📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    if isinstance(data, list):
                        filtered = [
                            item for item in data 
                            if item_description.lower() in str(item.get('descricao', '')).lower()
                        ]
                        
                        print(f"  ✅ {len(filtered)} contratos")
                        return self._parse_contracts(filtered[:max_results])
                    else:
                        return []
                
                except Exception as e:
                    print(f"  ❌ Erro JSON: {e}")
                    return []
            
            elif response.status_code == 401:
                print(f"  ❌ API Key inválida")
                return []
            else:
                print(f"  ⚠️ Erro HTTP {response.status_code}")
                return []
        
        except requests.exceptions.Timeout:
            print(f"  ⏱️ Timeout")
            return []
        except Exception as e:
            print(f"  ❌ Erro: {str(e)[:100]}")
            return []
    
    def _parse_contracts(self, contracts: List[Dict]) -> List[Dict]:
        """Processa contratos do Portal"""
        items = []
        
        for contract in contracts:
            try:
                valor = float(contract.get('valor', 0))
                
                if valor <= 0:
                    continue
                
                data_str = contract.get('data')
                if data_str:
                    try:
                        date_obj = datetime.strptime(data_str, '%d/%m/%Y')
                    except:
                        try:
                            date_obj = datetime.strptime(data_str.split('T')[0], '%Y-%m-%d')
                        except:
                            continue
                else:
                    continue
                
                items.append({
                    'source': 'Portal da Transparência',
                    'price': valor,
                    'date': date_obj,
                    'supplier': contract.get('fornecedor', {}).get('nome', 'N/A'),
                    'supplier_cnpj': contract.get('fornecedor', {}).get('cnpjFormatado'),
                    'entity': contract.get('orgao', {}).get('nome', 'N/A'),
                    'region': contract.get('uf'),
                    'contract_number': contract.get('numeroDocumento')
                })
            
            except (ValueError, KeyError, TypeError):
                continue
        
        return items
