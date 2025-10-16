# -*- coding: utf-8 -*-
"""
Preço Ágil - Sistema de Pesquisa de Preços para Licitações
Conforme Lei 14.133/2021 e Portarias TCU 121, 122 e 123/2023
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

# Inicializa SQLAlchemy
db = SQLAlchemy()

def create_app(config_class=Config):
    """Factory para criar a aplicação Flask"""
    
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Carrega configurações
    app.config.from_object(config_class)
    
    # Inicializa extensões
    db.init_app(app)
    
    # Cria diretórios necessários
    os.makedirs(app.config['DATA_DIR'], exist_ok=True)
    os.makedirs(app.config['REPORTS_DIR'], exist_ok=True)
    
    # Cria tabelas do banco de dados
    with app.app_context():
        from app.models.database import PriceResearch
        db.create_all()
        print("✅ Banco de dados inicializado")
    
    # Registra blueprints (rotas)
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    # Manipuladores de erro
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        db.session.rollback()
        return render_template('500.html'), 500
    
    # Contexto do template
    @app.context_processor
    def inject_config():
        return {
            'app_name': Config.APP_NAME,
            'app_version': Config.APP_VERSION,
            'app_description': Config.APP_DESCRIPTION
        }
    
    print("=" * 70)
    print(f"✅ {Config.APP_NAME} v{Config.APP_VERSION}")
    print("=" * 70)
    
    return app