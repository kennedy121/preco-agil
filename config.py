import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações do Preço Ágil"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'preco-agil-secret-key-2024')
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    
    # Branding
    APP_NAME = "Preço Ágil"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "Sistema de Pesquisa de Preços para Licitações"
    
    # APIs Governamentais
    PNCP_API_URL = os.getenv('PNCP_API_URL', 'https://pncp.gov.br/api')
    COMPRASNET_API_URL = os.getenv('COMPRASNET_API_URL', 'https://compras.dados.gov.br/api')
    PAINEL_PRECOS_URL = 'https://paineldeprecos.planejamento.gov.br/api/v1'
    
    # Banco de dados
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///preco_agil.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de pesquisa (Portaria TCU 121/2023)
    MAX_PRICE_AGE_DAYS = int(os.getenv('MAX_PRICE_AGE_DAYS', 365))
    MIN_SAMPLES = int(os.getenv('MIN_SAMPLES', 3))
    
    # Configurações estatísticas
    OUTLIER_THRESHOLD = float(os.getenv('OUTLIER_THRESHOLD', 1.5))
    CV_THRESHOLD = float(os.getenv('CV_THRESHOLD', 0.30))
    
    # Diretórios
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
    
    # ⭐ CATÁLOGOS EM CSV
    CATMAT_FILE = os.path.join(DATA_DIR, 'catmat.csv')
    CATSER_FILE = os.path.join(DATA_DIR, 'catser.csv')
    
    # Servidor
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8000))