
# -*- coding: utf-8 -*-
"""
Dados Mockados Realistas - Preço Ágil
Usado como fallback quando APIs não retornam dados
"""

from datetime import datetime, timedelta
import random
from typing import List, Dict

def generate_mock_prices(item_code: str, count: int = 35) -> List[Dict]:
    """
    Gera preços mockados realistas para testes
    
    Args:
        item_code: Código do item
        count: Quantidade de preços a gerar
    
    Returns:
        Lista de preços simulados
    """
    
    # Usa código do item como seed para gerar preços consistentes
    seed_value = int(''.join(filter(str.isdigit, str(item_code)[:6])) or '123456')
    random.seed(seed_value)
    
    # Preço base varia conforme o código
    base_price = random.uniform(50, 8000)
    
    prices = []
    
    fornecedores = [
        "Fornecedor Alpha Ltda",
        "Beta Comércio e Serviços S/A",
        "Gamma Distribuidora ME",
        "Delta Suprimentos Ltda",
        "Epsilon Materials EIRELI",
        "Zeta Produtos e Serviços",
        "Eta Supply Chain S/A",
        "Theta Comércio Atacadista",
        "Iota Indústria e Comércio",
        "Kappa Fornecimentos Ltda",
        "Lambda Distribuidora",
        "Omega Suprimentos S/A"
    ]
    
    orgaos = [
        "Ministério da Economia",
        "Ministério da Educação",
        "Ministério da Saúde",
        "Tribunal de Contas da União",
        "Polícia Federal - Departamento Regional",
        "Receita Federal do Brasil",
        "INSS - Instituto Nacional do Seguro Social",
        "Universidade Federal de São Paulo",
        "Prefeitura Municipal de Brasília",
        "Governo do Estado de Minas Gerais",
        "IBAMA - Instituto Brasileiro do Meio Ambiente",
        "Câmara dos Deputados"
    ]
    
    fontes = [
        "PNCP",
        "ComprasNet",
        "Painel de Preços",
        "Portal da Transparência"
    ]
    
    ufs = ['SP', 'RJ', 'MG', 'DF', 'BA', 'RS', 'PR', 'SC', 'PE', 'CE', 'GO', 'ES']
    
    for i in range(count):
        # Variação de preço (60% a 140% do base, criando dispersão realista)
        variation = random.uniform(0.6, 1.4)
        price = base_price * variation
        
        # Adiciona alguns outliers ocasionais (10% de chance)
        if random.random() < 0.1:
            price *= random.choice([0.5, 1.8])  # Outlier
        
        # Data aleatória no último ano
        days_ago = random.randint(1, 365)
        date = datetime.now() - timedelta(days=days_ago)
        
        # CNPJ fictício mas válido em formato
        cnpj = f"{random.randint(10, 99)}.{random.randint(100, 999)}.{random.randint(100, 999)}/0001-{random.randint(10, 99)}"
        
        prices.append({
            'source': random.choice(fontes),
            'price': round(price, 2),
            'date': date,
            'supplier': random.choice(fornecedores),
            'supplier_cnpj': cnpj,
            'entity': random.choice(orgaos),
            'region': random.choice(ufs),
            'contract_number': f"CT-{random.randint(1000, 9999)}/{date.year}",
            'supplier_validated': None  # Mock não valida
        })
    
    # Embaralha para parecer mais real
    random.shuffle(prices)
    
    return prices
