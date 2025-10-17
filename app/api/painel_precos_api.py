# -*- coding: utf-8 -*-
"""Cliente para a API do Painel de Preços"""

import requests
from typing import List, Dict, Optional
from datetime import datetime
import logging
import json

# Configura o logger
logger = logging.getLogger(__name__)

class PainelPrecosClient:
    """
    Cliente para consumir a API do Painel de Preços do Governo Federal.
    URL Base: https://paineldeprecos.planejamento.gov.br/api/
    """
    
    BASE_URL = "https://paineldeprecos.planejamento.gov.br/api/v1"

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json"
        }

    def search_by_item(self, 
                         item_code: str, 
                         item_type: str,
                         region: Optional[str] = None,
                         max_days: int = 365) -> List[Dict]:
        """
        Busca preços de um item no Painel de Preços.
        """
        
        endpoint = f"{self.BASE_URL}/contratacoes"
        
        params = {
            "codigo_item": item_code,
            "offset": 0,
            "limit": 500 # Aumentar o limite para capturar mais dados
        }

        try:
            response = requests.get(endpoint, headers=self.headers, params=params, timeout=self.timeout)
            response.raise_for_status() # Levanta um erro para respostas HTTP 4xx/5xx
            
            try:
                data = response.json()
            except json.JSONDecodeError:
                # Loga o erro caso a resposta não seja um JSON válido
                logger.warning(f"A resposta da API do Painel de Preços não foi um JSON válido. Status: {response.status_code}")
                return []

            contratacoes = data.get('_embedded', {}).get('contratacoes', [])
            
            if not contratacoes:
                return []

            return self._format_data(contratacoes)

        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição ao Painel de Preços: {e}")
            return []
        except Exception as e:
            logger.error(f"Erro inesperado ao processar dados do Painel de Preços: {e}")
            return []

    def _format_data(self, contratacoes: List[Dict]) -> List[Dict]:
        """
        Formata os dados brutos da API para o formato esperado pelo sistema.
        """
        prices = []
        for item in contratacoes:
            try:
                price = {
                    "source": "Painel de Preços",
                    "date": datetime.strptime(item.get("data_assinatura_contrato"), '%Y-%m-%d').date() if item.get("data_assinatura_contrato") else None,
                    "price": float(item.get("valor_unitario_homologado")),
                    "quantity": int(item.get("quantidade_item")),
                    "supplier": item.get("fornecedor_contratado"),
                    "supplier_cnpj": item.get("cnpj_fornecedor_contratado"),
                    "entity": item.get("orgao_contratante"),
                    "region": item.get("uf_orgao_contratante"),
                    "details_url": item.get('_links', {}).get('self', {}).get('href')
                }
                if price["price"] and price["price"] > 0:
                    prices.append(price)
            except (ValueError, TypeError, KeyError) as e:
                logger.warning(f"Item do Painel de Preços ignorado por erro de formatação: {e} | Item: {item}")
                continue
        return prices
