# -*- coding: utf-8 -*-
"""
Modelos do Banco de Dados - Preço Ágil
"""

from app.models import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    """Modelo de Usuário com controle de acesso"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    
    # Controle de Acesso
    role = db.Column(db.String(20), nullable=False, default='consulta')  # admin, gestor, consulta
    active = db.Column(db.Boolean, default=True)
    
    # Metadados
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    login_count = db.Column(db.Integer, default=0)
    
    # Relacionamentos
    pesquisas = db.relationship('Pesquisa', backref='user', lazy='dynamic')
    auditorias = db.relationship('AuditLog', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        """Gera hash da senha"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica se a senha está correta"""
        return check_password_hash(self.password_hash, password)
    
    @property
    def is_admin(self):
        """Verifica se é admin"""
        return self.role == 'admin'
    
    @property
    def is_gestor(self):
        """Verifica se é gestor ou admin"""
        return self.role in ['admin', 'gestor']
    
    @property
    def is_consulta(self):
        """Verifica se tem pelo menos permissão de consulta"""
        return self.role in ['admin', 'gestor', 'consulta']
    
    def __repr__(self):
        return f'<User {self.username}>'


class Pesquisa(db.Model):
    """Modelo para armazenar os resultados de uma pesquisa de preços"""
    __tablename__ = 'pesquisas'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Chave estrangeira para o usuário
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Informações do Item
    item_code = db.Column(db.String(50), nullable=False, index=True)
    item_description = db.Column(db.Text, nullable=False)
    catalog_type = db.Column(db.String(20), nullable=False)  # material ou servico
    
    # Metadados da Pesquisa
    research_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    responsible_agent = db.Column(db.String(100), nullable=False)
    
    # Dados da Coleta e Estatísticas (armazenados como JSON)
    stats = db.Column(db.JSON, nullable=False)
    prices_collected = db.Column(db.JSON, nullable=False)
    sources_consulted = db.Column(db.JSON, nullable=True)
    
    # Artefatos Gerados
    pdf_filename = db.Column(db.String(255), nullable=True)

    @property
    def estimated_value(self):
        """Retorna valor estimado da pesquisa"""
        return self.stats.get('estimated_value', 0)

    @property
    def sample_size(self):
        """Retorna tamanho da amostra"""
        return self.stats.get('sample_size', 0)

    def __repr__(self):
        return f'<Pesquisa {self.id} - {self.item_code}>'


class AuditLog(db.Model):
    """Log de auditoria de ações no sistema"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Ação realizada
    action = db.Column(db.String(50), nullable=False)
    resource = db.Column(db.String(50))
    resource_id = db.Column(db.Integer)
    
    # Detalhes
    details = db.Column(db.JSON)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    
    # Timestamp
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<AuditLog {self.action} by User {self.user_id}>'
