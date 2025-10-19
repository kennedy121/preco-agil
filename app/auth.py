# -*- coding: utf-8 -*-
"""
Blueprint de Autenticação - Preço Ágil
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from functools import wraps

bp = Blueprint('auth', __name__)


# ========== DECORATORS DE PERMISSÃO ==========

def admin_required(f):
    """Decorator para rotas que exigem permissão de Admin"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Você não tem permissão para acessar esta página.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


def gestor_required(f):
    """Decorator para rotas que exigem permissão de Gestor ou Admin"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_gestor:
            flash('Você não tem permissão para acessar esta página.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


# ========== FUNÇÃO DE AUDITORIA ==========

def audit_log(action, resource=None, resource_id=None, details=None):
    """
    Registra ação no log de auditoria
    
    Args:
        action: Ação realizada (ex: 'login', 'pesquisa_criada')
        resource: Tipo de recurso (ex: 'user', 'pesquisa')
        resource_id: ID do recurso
        details: Detalhes adicionais (dict)
    """
    try:
        from app.models import db
        from app.models.models import AuditLog
        
        log = AuditLog(
            user_id=current_user.id if current_user.is_authenticated else None,
            action=action,
            resource=resource,
            resource_id=resource_id,
            details=details,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')[:500]
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f'Erro ao registrar auditoria: {e}')
        # Não interrompe a execução se auditoria falhar
        pass


# ========== ROTAS DE AUTENTICAÇÃO ==========

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        from app.models import db
        from app.models.models import User
        from datetime import datetime
        
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        if not username or not password:
            flash('Por favor, preencha todos os campos.', 'warning')
            return render_template('auth/login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            audit_log('login_failed', details={'username': username})
            flash('Usuário ou senha inválidos.', 'danger')
            return render_template('auth/login.html')
        
        if not user.active:
            flash('Sua conta está desativada. Contate o administrador.', 'warning')
            return render_template('auth/login.html')
        
        # Login bem-sucedido
        login_user(user, remember=remember)
        
        # Atualiza metadados do usuário
        user.last_login = datetime.utcnow()
        user.login_count += 1
        db.session.commit()
        
        # Auditoria
        audit_log('login', 'user', user.id, {'username': username})
        
        flash(f'Bem-vindo, {user.full_name}!', 'success')
        
        # Redireciona para página solicitada ou index
        next_page = request.args.get('next')
        if next_page and next_page.startswith('/'):
            return redirect(next_page)
        
        return redirect(url_for('main.index'))
    
    return render_template('auth/login.html')


@bp.route('/logout')
@login_required
def logout():
    """Logout do usuário"""
    audit_log('logout', 'user', current_user.id)
    logout_user()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de novo usuário (apenas primeiro usuário)"""
    from app.models import db
    from app.models.models import User
    
    # Verifica se há usuários no sistema
    if User.query.count() > 0:
        flash('O registro está desabilitado. Contate o administrador.', 'warning')
        return redirect(url_for('auth.login'))
    
    # Permite criar o primeiro usuário (será admin)
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        full_name = request.form.get('full_name', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        # Validações
        if not all([username, email, full_name, password]):
            flash('Preencha todos os campos.', 'warning')
            return render_template('auth/register.html')
        
        if password != password_confirm:
            flash('As senhas não coincidem.', 'danger')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('A senha deve ter pelo menos 6 caracteres.', 'warning')
            return render_template('auth/register.html')
        
        # Verifica se usuário já existe
        if User.query.filter_by(username=username).first():
            flash('Nome de usuário já existe.', 'danger')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email já cadastrado.', 'danger')
            return render_template('auth/register.html')
        
        # Cria usuário (primeiro é admin)
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            role='admin'  # Primeiro usuário é admin
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        audit_log('user_created', 'user', user.id, {'username': username})
        
        flash('Conta criada com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')


@bp.route('/profile')
@login_required
def profile():
    """Perfil do usuário logado"""
    return render_template('auth/profile.html')

