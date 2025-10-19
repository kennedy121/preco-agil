
# app/api/brasilapi_client.py
"""
Cliente para BrasilAPI - Validação de CNPJ, CEP, Bancos
Documentação: https://brasilapi.com.br/docs
"""

import logging
from typing import Dict, Optional
from app.api.base_client import BaseAPIClient

logger = logging.getLogger(__name__)


class BrasilAPIClient(BaseAPIClient):
    """Cliente para BrasilAPI com cache e retry automáticos"""
    
    def __init__(self):
        super().__init__(
            base_url='https://brasilapi.com.br/api',
            timeout=10,
            cache_ttl=86400  # 24 horas para dados que mudam pouco
        )
    
    def get_cnpj_info(self, cnpj: str) -> Optional[Dict]:
        """
        Obtém informações de CNPJ da Receita Federal
        
        Args:
            cnpj: CNPJ com ou sem formatação
        
        Returns:
            Dados do CNPJ ou None se não encontrado
        """
        # Remove formatação
        cnpj_clean = ''.join(filter(str.isdigit, cnpj))
        
        if len(cnpj_clean) != 14:
            logger.warning(f"CNPJ inválido (tamanho incorreto): {cnpj}")
            return None
        
        endpoint = f'/cnpj/v1/{cnpj_clean}'
        data = self.get(endpoint)
        
        if not data:
            return None
        
        # Formata resposta padronizada
        return {
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
    
    def get_cep_info(self, cep: str) -> Optional[Dict]:
        """Obtém informações de CEP"""
        cep_clean = ''.join(filter(str.isdigit, cep))
        
        if len(cep_clean) != 8:
            logger.warning(f"CEP inválido: {cep}")
            return None
        
        endpoint = f'/cep/v2/{cep_clean}'
        return self.get(endpoint)
    
    def get_banco_info(self, codigo_banco: str) -> Optional[Dict]:
        """Obtém informações de banco"""
        codigo_clean = ''.join(filter(str.isdigit, codigo_banco)).zfill(3)
        endpoint = f'/banks/v1/{codigo_clean}'
        return self.get(endpoint)
    
    def validate_supplier(self, cnpj: str) -> Dict:
        """
        Valida fornecedor com checagens completas
        
        Returns:
            {
                'valid': bool,
                'reason': str (se inválido),
                'cnpj_info': dict (se válido),
                'warnings': list
            }
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
        
        # Coleta warnings (não impedem, mas alertam)
        warnings = []
        if not cnpj_info.get('email'):
            warnings.append('Email não cadastrado')
        if not cnpj_info.get('telefone'):
            warnings.append('Telefone não cadastrado')
        
        return {
            'valid': True,
            'cnpj_info': cnpj_info,
            'warnings': warnings
        }
