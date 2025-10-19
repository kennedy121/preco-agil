# -*- coding: utf-8 -*-
"""
Cliente PNCP - Portal Nacional de Contratações Públicas
"""

import requests
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta


class PNCPClient:
    """Cliente para API do PNCP (pública, sem necessidade de chave)"""
    
    def __init__(self):
        self.base_url = 'https://pncp.gov.br/api/consulta/v1'
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'PrecoAgil/1.0'
        })
    
    def search_contracts(
        self,
        item_code: str,
        catalog_type: str,
        max_days: int = 730,
        region: Optional[str] = None
    ) -> List[Dict]:
        """Busca contratos no PNCP"""
        
        endpoint = f"{self.base_url}/contratos"
        date_limit = datetime.now() - timedelta(days=max_days)
        
        params = {
            'dataInicial': date_limit.strftime('%Y%m%d'),
            'dataFinal': datetime.now().strftime('%Y%m%d'),
            'pagina': 1,
            'tamanhoPagina': 100
        }
        
        print(f"  🔗 GET {endpoint}")
        
        try:
            response = self.session.get(endpoint, params=params, timeout=20)
            print(f"  📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    contratos = data.get('data', [])
                    print(f"  ✅ {len(contratos)} contratos")
                    return self._parse_contracts(contratos)
                except Exception as e:
                    print(f"  ❌ Erro JSON: {e}")
                    return []
            else:
                print(f"  ⚠️ Erro HTTP {response.status_code}")
                return []
        
        except requests.exceptions.Timeout:
            print(f"  ⏱️ Timeout")
            return []
        except Exception as e:
            print(f"  ❌ Erro: {str(e)[:80]}")
            return []
    
    def _parse_contracts(self, contracts: List[Dict]) -> List[Dict]:
        """Processa contratos do PNCP"""
        items = []
        
        for contract in contracts:
            try:
                valor = (
                    contract.get('valorTotal') or
                    contract.get('valorGlobal') or
                    contract.get('valorInicial')
                )
                
                if not valor or float(valor) <= 0:
                    continue
                
                data_str = contract.get('dataAssinatura') or contract.get('dataPublicacao')
                if data_str:
                    try:
                        date_obj = datetime.strptime(data_str.split('T')[0], '%Y-%m-%d')
                    except:
                        continue
                else:
                    continue
                
                items.append({
                    'source': 'PNCP',
                    'price': float(valor),
                    'date': date_obj,
                    'supplier': contract.get('nomeRazaoSocialFornecedor', 'N/A'),
                    'supplier_cnpj': contract.get('niFornecedor'),
                    'entity': contract.get('orgaoEntidade', {}).get('razaoSocial', 'N/A'),
                    'region': contract.get('ufOrgao'),
                    'contract_number': contract.get('numeroControlePNCP')
                })
            
            except (ValueError, KeyError, TypeError):
                continue
        
        return items
