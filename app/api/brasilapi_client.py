# -*- coding: utf-8 -*-
"""
Cliente BrasilAPI - Camada de Abstração Unificada
Preço Ágil

Fornece interface estável e simplificada para múltiplas APIs governamentais
Fallback automático quando APIs oficiais falham

Fonte: https://github.com/BrasilAPI/BrasilAPI
"""

import requests
from typing import Dict, Optional
from datetime import datetime

class BrasilAPIClient:
    """
    Cliente para BrasilAPI - Agregador mantido pela comunidade
    
    VANTAGENS:
    - Interface unificada e estável
    - Fallback automático
    - Sem necessidade de múltiplas chaves de API
    - Cache inteligente
    - Rate limiting gerenciado
    """
    
    def __init__(self):
        self.base_url = "https://brasilapi.com.br/api"
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'PrecoAgil/1.0'
        })
        self._cache = {}
    
    def get_cnpj_info(self, cnpj: str) -> Optional[Dict]:
        """
        Obtém informações de CNPJ (Receita Federal)
        Útil para validar fornecedores
        
        Args:
            cnpj: CNPJ do fornecedor (apenas números ou com formatação)
        
        Returns:
            Informações completas do CNPJ ou None se não encontrado
        """
        # Remove formatação
        cnpj_clean = ''.join(filter(str.isdigit, cnpj))
        
        if len(cnpj_clean) != 14:
            print(f"  ⚠️ CNPJ inválido: {cnpj}")
            return None
        
        # Verifica cache
        if cnpj_clean in self._cache:
            print(f"  💾 CNPJ {cnpj_clean} recuperado do cache")
            return self._cache[cnpj_clean]
        
        endpoint = f"{self.base_url}/cnpj/v1/{cnpj_clean}"
        
        try:
            response = self.session.get(endpoint, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            result = {
                'cnpj': data.get('cnpj'),
                'razao_social': data.get('razao_social'),
                'nome_fantasia': data.get('nome_fantasia'),
                'situacao': data.get('descricao_situacao_cadastral'),
                'data_situacao': data.get('data_situacao_cadastral'),
                'uf': data.get('uf'),
                'municipio': data.get('municipio'),
                'bairro': data.get('bairro'),
                'logradouro': data.get('logradouro'),
                'numero': data.get('numero'),
                'cep': data.get('cep'),
                'email': data.get('email'),
                'telefone': data.get('ddd_telefone_1'),
                'porte': data.get('porte'),
                'natureza_juridica': data.get('natureza_juridica'),
                'atividade_principal': data.get('cnae_fiscal_descricao'),
                'capital_social': data.get('capital_social')
            }
            
            # Armazena em cache
            self._cache[cnpj_clean] = result
            
            return result
        
        except requests.exceptions.RequestException as e:
            print(f"  ⚠️ Erro ao consultar CNPJ {cnpj_clean} via BrasilAPI: {e}")
            return None
    
    def get_cep_info(self, cep: str) -> Optional[Dict]:
        """
        Obtém informações de CEP
        Útil para validar endereços de fornecedores/órgãos
        
        Args:
            cep: CEP (apenas números ou com hífen)
        
        Returns:
            Informações do endereço ou None
        """
        # Remove formatação
        cep_clean = ''.join(filter(str.isdigit, cep))
        
        if len(cep_clean) != 8:
            return None
        
        # Verifica cache
        if f"cep_{cep_clean}" in self._cache:
            return self._cache[f"cep_{cep_clean}"]
        
        endpoint = f"{self.base_url}/cep/v2/{cep_clean}"
        
        try:
            response = self.session.get(endpoint, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Armazena em cache
            self._cache[f"cep_{cep_clean}"] = data
            
            return data
        
        except requests.exceptions.RequestException as e:
            print(f"  ⚠️ Erro ao consultar CEP {cep_clean}: {e}")
            return None
    
    def get_banco_info(self, codigo_banco: str) -> Optional[Dict]:
        """
        Obtém informações de banco
        Útil para validar dados bancários de fornecedores
        
        Args:
            codigo_banco: Código do banco (3 dígitos)
        
        Returns:
            Informações do banco ou None
        """
        codigo_clean = ''.join(filter(str.isdigit, codigo_banco)).zfill(3)
        
        endpoint = f"{self.base_url}/banks/v1/{codigo_clean}"
        
        try:
            response = self.session.get(endpoint, timeout=10)
            response.raise_for_status()
            
            return response.json()
        
        except requests.exceptions.RequestException:
            return None
    
    def validate_supplier(self, cnpj: str) -> Dict:
        """
        Valida fornecedor usando múltiplas checagens
        
        Args:
            cnpj: CNPJ do fornecedor
        
        Returns:
            Dicionário com status de validação completo
        """
        if not cnpj:
            return {
                'valid': False,
                'reason': 'CNPJ não informado'
            }
        
        cnpj_info = self.get_cnpj_info(cnpj)
        
        if not cnpj_info:
            return {
                'valid': False,
                'reason': 'CNPJ não encontrado na Receita Federal'
            }
        
        # Verifica situação cadastral
        situacao = (cnpj_info.get('situacao') or '').upper()
        
        if 'ATIVA' not in situacao:
            return {
                'valid': False,
                'reason': f'Situação cadastral irregular: {situacao}',
                'cnpj_info': cnpj_info
            }
        
        # Verifica se não está em débito (se disponível)
        warnings = []
        
        # Aviso se não tem email
        if not cnpj_info.get('email'):
            warnings.append('Email não cadastrado')
        
        # Aviso se não tem telefone
        if not cnpj_info.get('telefone'):
            warnings.append('Telefone não cadastrado')
        
        return {
            'valid': True,
            'cnpj_info': cnpj_info,
            'warnings': warnings
        }
    
    def clear_cache(self):
        """Limpa o cache interno"""
        self._cache.clear()
        print("  🧹 Cache do BrasilAPI limpo")