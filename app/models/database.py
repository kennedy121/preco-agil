# -*- coding: utf-8 -*-
"""
Modelos do Banco de Dados (SQLAlchemy)
Preço Ágil - Sistema de Pesquisa de Preços
"""

from app import db
from sqlalchemy.sql import func

class PriceResearch(db.Model):
    """Representa uma pesquisa de preços armazenada no banco"""
    
    # Chave primária
    id = db.Column(db.Integer, primary_key=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    # Dados do item pesquisado
    item_code = db.Column(db.String(50), nullable=False, index=True)
    item_description = db.Column(db.String(1000), nullable=False)
    item_type = db.Column(db.String(20), nullable=False)  # 'material' ou 'servico'
    
    # Dados da pesquisa
    search_parameters = db.Column(db.JSON, nullable=True) # Parâmetros usados
    collected_prices = db.Column(db.JSON, nullable=False)  # Lista de preços coletados
    
    # Resultados da Análise Estatística
    statistical_analysis = db.Column(db.JSON, nullable=True)
    final_price = db.Column(db.Float, nullable=True) # Preço final adotado (mediana, média, etc)
    
    # Metadados
    user_id = db.Column(db.Integer, nullable=True) # Futuro: link para usuário
    report_file = db.Column(db.String(255), nullable=True) # Caminho para o PDF gerado
    status = db.Column(db.String(50), default='Completed') # Ex: Completed, In Progress, Failed

    def __repr__(self):
        return f'<PriceResearch {self.id}: {self.item_description[:50]}>'

    def to_dict(self):
        """Converte o objeto para um dicionário serializável"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'item_code': self.item_code,
            'item_description': self.item_description,
            'item_type': self.item_type,
            'search_parameters': self.search_parameters,
            'collected_prices': self.collected_prices,
            'statistical_analysis': self.statistical_analysis,
            'final_price': self.final_price,
            'status': self.status
        }
