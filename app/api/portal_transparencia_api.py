# app/api/portal_transparencia_api.py
import requests
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class PortalTransparenciaClient:
    """Cliente para API do Portal da Transparência (CGU)"""
    
    def __init__(self):
        self.base_url = "https://api.portaldatransparencia.gov.br/api-de-dados"
        
        self.api_key = os.getenv('PORTAL_TRANSPARENCIA_API_KEY', '')
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; PrecoAgil/1.0)',
            'Accept': 'application/json',
            'chave-api-dados': self.api_key
        })
    
    def search_by_item(self, item_code: str, catalog_type: str = 'material', **kwargs) -> List[Dict]:
        """
        Busca despesas relacionadas ao item
        """
        try:
            if not self.api_key:
                print("  ⚠️ Portal Transparência: API Key não configurada")
                print("  ℹ️ Configure PORTAL_TRANSPARENCIA_API_KEY no .env")
                return self._generate_mock_data(item_code)
            
            from datetime import datetime, timedelta
            
            data_fim = datetime.now()
            data_inicio = data_fim - timedelta(days=365)
            
            endpoint = f"{self.base_url}/despesas/documentos"
            
            params = {
                'dataInicio': data_inicio.strftime('%d/%m/%Y'),
                'dataFim': data_fim.strftime('%d/%m/%Y'),
                'pagina': 1
            }
            
            print(f"  🔗 GET {endpoint}")
            print(f"  📋 Params: {params}")
            
            response = self.session.get(
                endpoint,
                params=params,
                timeout=30
            )
            
            print(f"  📊 Status: {response.status_code}")
            
            if response.status_code == 400:
                print("  ⚠️ Erro 400 - Verificando resposta...")
                try:
                    error_detail = response.json()
                    print(f"  📄 Detalhe do erro: {error_detail}")
                except:
                    print(f"  📄 Resposta: {response.text[:500]}")
                
                print("  ℹ️ Usando dados mockados")
                return self._generate_mock_data(item_code)
            
            if response.status_code == 403:
                print("  ⚠️ Erro 403 - API Key inválida ou não autorizada")
                return self._generate_mock_data(item_code)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    return self._parse_results(data, item_code)
                except Exception as e:
                    print(f"  ⚠️ Erro ao parsear JSON: {e}")
                    return []
            
            return []
            
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Erro de conexão: {e}")
            return self._generate_mock_data(item_code)
        except Exception as e:
            print(f"  ❌ Erro inesperado: {e}")
            import traceback
            traceback.print_exc()
            return self._generate_mock_data(item_code)
    
    def _parse_results(self, data: Dict, item_code: str) -> List[Dict]:
        """Parse dos resultados da API"""
        results = []
        
        try:
            items = data if isinstance(data, list) else data.get('dados', [])
            
            for item in items:
                try:
                    descricao = item.get('descricao', '').upper()
                    if item_code not in descricao:
                        continue
                    
                    result = {
                        'source': 'Portal da Transparência',
                        'price': float(item.get('valor', item.get('valorPago', 0))),
                        'date': item.get('data', item.get('dataEmissao', '')),
                        'supplier': item.get('favorecido', {}).get('nome', 'N/A') if isinstance(item.get('favorecido'), dict) else 'N/A',
                        'cnpj': item.get('favorecido', {}).get('cnpj', '') if isinstance(item.get('favorecido'), dict) else '',
                        'description': descricao,
                        'unit': 'UN',
                        'orgao': item.get('orgao', {}).get('nome', 'N/A') if isinstance(item.get('orgao'), dict) else 'N/A'
                    }
                    
                    if result['price'] > 0:
                        results.append(result)
                        
                except (KeyError, ValueError, TypeError):
                    continue
                    
        except Exception as e:
            print(f"  ⚠️ Erro ao parsear: {e}")
        
        return results
    
    def _generate_mock_data(self, item_code: str, count: int = 20) -> List[Dict]:
        """Gera dados mockados quando API não disponível"""
        import random
        from datetime import datetime, timedelta
        
        print(f"  📦 Gerando {count} preços mockados para Portal Transparência")
        
        results = []
        base_price = random.uniform(150, 6000)
        
        for i in range(count):
            date = datetime.now() - timedelta(days=random.randint(1, 365))
            price = base_price * random.uniform(0.85, 1.15)
            
            results.append({
                'source': 'Portal da Transparência',
                'price': round(price, 2),
                'date': date.strftime('%Y-%m-%d'),
                'supplier': f'Órgão Público {i+1}',
                'cnpj': f'{random.randint(10000000, 99999999):08d}000{random.randint(100, 199)}',
                'description': f'Item {item_code}',
                'unit': 'UN',
                'orgao': f'Ministério/Órgão {i+1}',
                'is_mock': True
            })
        
        return results