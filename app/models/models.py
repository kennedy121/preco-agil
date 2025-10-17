from . import db
import datetime

class Pesquisa(db.Model):
    """Modelo para armazenar os resultados de uma pesquisa de preços."""
    id = db.Column(db.Integer, primary_key=True)
    
    # Informações do Item
    item_code = db.Column(db.String(50), nullable=False, index=True)
    item_description = db.Column(db.Text, nullable=False)
    catalog_type = db.Column(db.String(20), nullable=False) # 'material' ou 'servico'
    
    # Metadados da Pesquisa
    research_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow, index=True)
    responsible_agent = db.Column(db.String(100), nullable=False)
    
    # Dados da Coleta e Estatísticas (armazenados como JSON)
    stats = db.Column(db.JSON, nullable=False)
    prices_collected = db.Column(db.JSON, nullable=False)
    sources_consulted = db.Column(db.JSON, nullable=True)
    
    # Artefatos Gerados
    pdf_filename = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Pesquisa {self.id} - {self.item_code}>'

    @property
    def estimated_value(self):
        """Propriedade para acessar facilmente o valor estimado de dentro do JSON de estatísticas."""
        return self.stats.get('estimated_value', 0)

    @property
    def sample_size(self):
        """Propriedade para acessar o tamanho da amostra."""
        return self.stats.get('sample_size', 0)
