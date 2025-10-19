# -*- coding: utf-8 -*-
"""
Blueprint de Autenticação - Preço Ágil
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from app.models import db
from app.models.models import User, AuditLog
from datetime import datetime
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
    """Registra ação no log de auditoria"""
    try:
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
        db.session.rollback()


# ========== ROTAS DE AUTENTICAÇÃO ==========

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
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
    """Registro de novo usuário (auto-registro desabilitado por padrão)"""
    
    if User.query.count() > 0:
        flash('O registro está desabilitado. Contate o administrador.', 'warning')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        full_name = request.form.get('full_name', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        if not all([username, email, full_name, password]):
            flash('Preencha todos os campos.', 'warning')
            return render_template('auth/register.html')
        
        if password != password_confirm:
            flash('As senhas não coincidem.', 'danger')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('A senha deve ter pelo menos 6 caracteres.', 'warning')
            return render_template('auth/register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Nome de usuário já existe.', 'danger')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email já cadastrado.', 'danger')
            return render_template('auth/register.html')
        
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            role='admin'
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        audit_log('user_created', 'user', user.id, {'username': username})
        
        flash('Conta criada com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')


# ========== GERENCIAMENTO DE USUÁRIOS (ADMIN) ==========

@bp.route('/users')
@admin_required
def list_users():
    """Lista todos os usuários (apenas admin)"""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('auth/users.html', users=users)


@bp.route('/users/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    """Cria novo usuário (apenas admin)"""
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            role = request.form.get('role', 'consulta')
            is_active = request.form.get('is_active') == 'on'
            
            if not username or not email or not password:
                flash('Todos os campos obrigatórios devem ser preenchidos.', 'danger')
                return redirect(url_for('auth.create_user'))
            
            if password != confirm_password:
                flash('As senhas não coincidem.', 'danger')
                return redirect(url_for('auth.create_user'))
            
            if len(password) < 6:
                flash('A senha deve ter no mínimo 6 caracteres.', 'danger')
                return redirect(url_for('auth.create_user'))
            
            if User.query.filter_by(username=username).first():
                flash('Nome de usuário já existe.', 'danger')
                return redirect(url_for('auth.create_user'))
            
            if User.query.filter_by(email=email).first():
                flash('E-mail já cadastrado.', 'danger')
                return redirect(url_for('auth.create_user'))
            
            user = User(
                username=username,
                email=email,
                role=role,
                active=is_active
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            flash(f'Usuário {username} criado com sucesso!', 'success')
            return redirect(url_for('auth.list_users'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erro ao criar usuário: {e}")
            flash(f'Erro ao criar usuário: {str(e)}', 'danger')
            return redirect(url_for('auth.create_user'))
    
    return render_template('auth/create_user.html')


@bp.route('/users/<int:id>/toggle', methods=['POST'])
@admin_required
def toggle_user(id):
    """Ativa/Desativa usuário"""
    user = User.query.get_or_404(id)
    
    if user.id == current_user.id:
        flash('Você não pode desativar sua própria conta.', 'warning')
        return redirect(url_for('auth.list_users'))
    
    user.active = not user.active
    db.session.commit()
    
    action = 'ativado' if user.active else 'desativado'
    audit_log(f'user_{action}', 'user', user.id, {'by': current_user.username})
    
    flash(f'Usuário {user.username} {action}.', 'success')
    return redirect(url_for('auth.list_users'))


@bp.route('/users/<int:id>/delete', methods=['POST'])
@admin_required
def delete_user(id):
    """Deleta usuário (apenas admin)"""
    user = User.query.get_or_404(id)
    
    if user.id == current_user.id:
        flash('Você não pode deletar sua própria conta.', 'warning')
        return redirect(url_for('auth.list_users'))
    
    username = user.username
    
    audit_log('user_deleted', 'user', user.id, {
        'username': username,
        'deleted_by': current_user.username
    })
    
    db.session.delete(user)
    db.session.commit()
    
    flash(f'Usuário {username} deletado.', 'success')
    return redirect(url_for('auth.list_users'))


# ========== AUDITORIA (ADMIN/GESTOR) ==========

@bp.route('/audit')
@gestor_required
def audit_logs():
    """Visualiza logs de auditoria"""
    page = request.args.get('page', 1, type=int)
    
    action = request.args.get('action', '').strip()
    user_id = request.args.get('user_id', type=int)
    
    query = AuditLog.query
    
    if action:
        query = query.filter(AuditLog.action == action)
    
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    
    pagination = query.order_by(
        AuditLog.timestamp.desc()
    ).paginate(page=page, per_page=50, error_out=False)
    
    actions = db.session.query(AuditLog.action).distinct().all()
    actions = [a[0] for a in actions]
    
    users = User.query.order_by(User.username).all()
    
    return render_template(
        'auth/audit.html',
        logs=pagination.items,
        pagination=pagination,
        actions=actions,
        users=users,
        filters={'action': action, 'user_id': user_id}
    )


# ========== PERFIL DO USUÁRIO ==========

@bp.route('/profile')
@login_required
def profile():
    """Perfil do usuário logado"""
    return render_template('auth/profile.html')


@bp.route('/profile/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Altera senha do usuário"""
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not current_user.check_password(current_password):
            flash('Senha atual incorreta.', 'danger')
            return render_template('auth/change_password.html')
        
        if new_password != confirm_password:
            flash('As novas senhas não coincidem.', 'danger')
            return render_template('auth/change_password.html')
        
        if len(new_password) < 6:
            flash('A senha deve ter pelo menos 6 caracteres.', 'warning')
            return render_template('auth/change_password.html')
        
        current_user.set_password(new_password)
        db.session.commit()
        
        audit_log('password_changed', 'user', current_user.id)
        
        flash('Senha alterada com sucesso!', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/change_password.html')
