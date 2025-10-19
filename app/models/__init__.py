# -*- coding: utf-8 -*-
"""
Preço Ágil - Inicialização da Aplicação Flask
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
import os

# Instancia as extensões
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

# Configura o LoginManager
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'warning'


def create_app(config_class=Config):
    """Factory para criar a aplicação Flask"""

    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

    app = Flask(__name__,
                template_folder=template_dir,
                static_folder=static_dir)

    app.config.from_object(config_class)

    # ✅ Inicializa as extensões com a app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # ✅ CRÍTICO: Importa modelos ANTES de criar tabelas
    from app.models.models import User, Pesquisa, AuditLog

    # ✅ Função para carregar o usuário logado
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        # Cria diretórios, se não existirem
        os.makedirs(app.config['DATA_DIR'], exist_ok=True)
        os.makedirs(app.config['REPORTS_DIR'], exist_ok=True)
        
        # ✅ AGORA cria todas as tabelas
        db.create_all()
        print("✅ Banco de dados inicializado")

    # ✅ Registra Blueprints
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # ✅ Registra processadores de contexto e error handlers
    from app.context_processors import inject_global_vars
    app.context_processor(inject_global_vars)

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
