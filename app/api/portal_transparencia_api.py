
# app/api/portal_transparencia_api.py
import requests
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class PortalTransparenciaClient:
    """
    Cliente para API do Portal da Transparência (CGU)
    https://www.portaltransparencia.gov.br/api-de-dados
    """
    
    def __init__(self):
        self.base_url = os.getenv(
            'PORTAL_TRANSPARENCIA_API_URL',
            'https://api.portaldatransparencia.gov.br/api-de-dados'
        )
        
        # ⭐ IMPORTANTE: Pega a chave do .env
        self.api_key = os.getenv('PORTAL_TRANSPARENCIA_API_KEY')
        
        if not self.api_key:
            print("⚠️ AVISO: Chave da API do Portal da Transparência não configurada")
            print("   Configure PORTAL_TRANSPARENCIA_API_KEY no arquivo .env")
        else:
            print("✅ API do Portal da Transparência configurada")
        
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'chave-api-dados': self.api_key or ''  # ⭐ Header específico da API
        })
    
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
            item_description: Descrição do item/objeto
            start_date: Data inicial (formato: dd/mm/yyyy)
            end_date: Data final (formato: dd/mm/yyyy)
            page: Página de resultados
        
        Returns:
            Lista de contratos encontrados
        """
        
        if not self.api_key:
            print("  ⚠️ API key não configurada, pulando Portal da Transparência")
            return []
        
        print(f"\n--- [DEBUG: PORTAL DA TRANSPARÊNCIA] ---")
        
        # Define datas padrão
        if not end_date:
            end_date = datetime.now().strftime('%d/%m/%Y')
        
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365)).strftime('%d/%m/%Y')
        
        endpoint = f"{self.base_url}/contratos"
        
        params = {
            'dataInicial': start_date,
            'dataFinal': end_date,
            'pagina': page
        }
        
        print(f"- Endpoint: {endpoint}")
        print(f"- Parâmetros: {params}")
        print(f"- API Key: {self.api_key[:10]}... (configurada)")
        
        try:
            response = self.session.get(endpoint, params=params, timeout=30)
            
            print(f"- Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Filtra por descrição
                all_contracts = data if isinstance(data, list) else []
                
                contracts = [
                    c for c in all_contracts 
                    if item_description.lower() in c.get('objeto', '').lower()
                ]
                
                print(f"- Contratos encontrados: {len(contracts)}")
                
                return self._parse_contracts(contracts)
            
            elif response.status_code == 401:
                print(f"- ERRO: Chave de API inválida ou expirada")
                return []
            
            elif response.status_code == 429:
                print(f"- ERRO: Limite de requisições excedido")
                return []
            
            else:
                print(f"- ERRO: Status {response.status_code}")
                print(f"- Resposta: {response.text[:200]}")
                return []
        
        except requests.exceptions.Timeout:
            print(f"- ERRO: Timeout após 30s")
            return []
        except requests.exceptions.RequestException as e:
            print(f"- ERRO: {str(e)[:100]}")
            return []
    
    def _parse_contracts(self, contracts: List[Dict]) -> List[Dict]:
        """Processa contratos do Portal da Transparência"""
        
        items = []
        
        for contract in contracts:
            try:
                # Extrai data
                date_str = contract.get('dataAssinatura')
                if date_str:
                    # Formato: dd/mm/yyyy
                    date_obj = datetime.strptime(date_str, '%d/%m/%Y')
                else:
                    continue
                
                # Valor do contrato
                valor = float(contract.get('valorInicial', 0))
                
                if valor <= 0:
                    continue
                
                items.append({
                    'source': 'Portal da Transparência',
                    'price': valor,
                    'date': date_obj,
                    'supplier': contract.get('fornecedor', {}).get('nome'),
                    'supplier_cnpj': contract.get('fornecedor', {}).get('cnpj'),
                    'entity': contract.get('orgaoVinculado', {}).get('nome'),
                    'contract_number': contract.get('numero'),
                    'object': contract.get('objeto'),
                    'modality': contract.get('modalidade')
                })
            
            except (ValueError, KeyError, TypeError):
                continue
        
        return items
