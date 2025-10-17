# -*- coding: utf-8 -*-
"""
Preço Ágil - Inicialização da Aplicação Flask
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

db = SQLAlchemy()

def create_app(config_class=Config):
    """Factory para criar a aplicação Flask"""
    
    # Aponta para as pastas 'templates' e 'static' no diretório 'app'
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir)
    
    app.config.from_object(config_class)
    
    # Inicializa extensões
    db.init_app(app)
    
    # Cria diretórios
    os.makedirs(app.config['DATA_DIR'], exist_ok=True)
    os.makedirs(app.config['REPORTS_DIR'], exist_ok=True)
    
    # Cria tabelas do banco
    with app.app_context():
        # Correção: Importação relativa para evitar dependência circular
        from .models import Pesquisa
        db.create_all()
        print("✅ Banco de dados inicializado")
    
    # Registra blueprints
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Registra o processador de contexto
    from app.context_processors import inject_global_vars
    app.context_processor(inject_global_vars)
    
    # Erros
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        db.session.rollback()
        return render_template('500.html'), 500
    
    print("✅ Preço Ágil inicializado")
    
    return app
