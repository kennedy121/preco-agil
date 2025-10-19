# Preço Ágil - Análise de Código

## Resumo do Projeto

O **Preço Ágil** é uma aplicação web desenvolvida em Python com o micro-framework Flask. Seu objetivo é automatizar e otimizar o processo de pesquisa de preços para licitações públicas, garantindo conformidade com a legislação brasileira (Lei 14.133/2021) e as portarias do Tribunal de Contas da União (TCU).

### Funcionalidades Principais

- **Busca em Múltiplas Fontes Oficiais:** O sistema consulta diversas APIs governamentais, incluindo **PNCP**, **ComprasNet**, **Painel de Preços** e **Portal da Transparência**, além de catálogos locais (CATMAT/CATSER) e a **BrasilAPI** para validação de fornecedores. Ele implementa fallback automático e tratamento de erros para garantir a resiliência na coleta de dados.
- **Análise Estatística Avançada:** Utiliza métodos estatísticos robustos, como a mediana e a média saneada (com remoção de outliers via IQR), para processar os preços coletados e determinar um valor estimado confiável para a contratação, seguindo as diretrizes do TCU.
- **Geração de Relatórios Detalhados:** Para cada pesquisa realizada, é gerado um relatório completo em formato PDF, detalhando as fontes consultadas, a série de preços, a análise estatística, a justificativa da metodologia e o valor estimado final, em conformidade com o Art. 29 da Portaria TCU 121/2023.
- **Autenticação e Controle de Acesso:** Inclui um sistema de autenticação de usuários com diferentes perfis (administrador, gestor, consulta) e um log de auditoria para rastrear as ações no sistema, garantindo segurança e conformidade.
- **Histórico e Comparação de Pesquisas:** Permite aos usuários visualizar um histórico de todas as suas pesquisas (ou todas, para gestores e administradores), aplicar filtros, e comparar estatísticas entre múltiplas pesquisas através de gráficos interativos.
- **Visualização Interativa de Dados:** Os resultados das pesquisas são apresentados com gráficos dinâmicos (histogramas, boxplots, timelines, dispersão por fonte) para facilitar a análise visual da distribuição e evolução dos preços.

---

## Estrutura do Projeto

```
.
├── 📄 .env                             # Variáveis de ambiente
├── 📄 config.py                        # Configurações da aplicação
├── 📄 devserver.sh                     # Script para iniciar o servidor de desenvolvimento
├── 📄 GEMINI.md                        # Regras de interação da IA
├── 📄 README.md                        # Documentação principal do projeto
├── 📄 requirements.txt                 # Dependências do Python
├── 🚀 run.py                           # Ponto de entrada da aplicação
├── 📁 app/                             # Módulo principal da aplicação Flask
│   ├── 📄 __init__.py                  # Inicialização do Flask app
│   ├── 📄 context_processors.py        # Processadores de contexto para templates
│   ├── 📄 routes.py                    # Definição das rotas e lógica principal
│   ├── 📄 auth.py                      # Blueprint de autenticação e gerenciamento de usuários
│   ├── 📁 api/                         # Clientes para APIs externas
│   │   ├── 📄 __init__.py              # Inicializador do módulo de APIs
│   │   ├── 📄 brasilapi_client.py      # Cliente para BrasilAPI (CNPJ, CEP)
│   │   ├── 📄 catmat_api.py            # Cliente para catálogo CATMAT (CSV local)
│   │   ├── 📄 catser_api.py            # Cliente para catálogo CATSER (CSV local)
│   │   ├── 📄 comprasnet_api.py        # Cliente para API do ComprasNet
│   │   ├── 📄 fallback_manager.py      # Gerenciamento de fallback e resiliência
│   │   ├── 📄 painel_precos_api.py     # Cliente para API do Painel de Preços
│   │   ├── 📄 pncp_api.py              # Cliente para API do PNCP
│   │   └── 📄 portal_transparencia_api.py # Cliente para API do Portal da Transparência
│   ├── 📁 models/                      # Modelos do banco de dados (SQLAlchemy)
│   │   ├── 📄 __init__.py              # Inicialização do módulo de modelos
│   │   ├── 📄 models.py                # Definição dos modelos (Pesquisa, User, AuditLog)
│   │   └── 📄 database.py              # Definições de modelos mais antigas/secundárias (pode ser unificado)
│   ├── 📁 services/                    # Lógica de negócio e serviços auxiliares
│   │   ├── 📄 __init__.py              # Inicializador do módulo de serviços
│   │   ├── 📄 chart_generator.py       # Geração de gráficos para visualização de dados
│   │   ├── 📄 data_analyzer.py         # Análise e tratamento de dados
│   │   ├── 📄 document_generator.py    # Geração de relatórios em PDF
│   │   ├── 📄 mock_price_data.py       # Geração de dados de preço mockados
│   │   └── 📄 statistical_analyzer.py  # Análise estatística dos preços coletados
│   ├── 📁 static/                      # Arquivos estáticos (CSS, JS, imagens)
│   │   ├── 📁 css/                     # Folhas de estilo CSS
│   │   │   └── 📄 style.css            # Estilos customizados da aplicação
│   │   └── 📁 js/                      # Scripts JavaScript
│   │       └── 📄 main.js              # JavaScript principal da aplicação
│   └── 📁 templates/                   # Templates HTML Jinja2
│       ├── 📄 404.html                 # Página de erro 404
│       ├── 📄 500.html                 # Página de erro 500
│       ├── 📄 base.html                # Template base para todas as páginas
│       ├── 📄 comparacao.html          # Página de comparação de pesquisas
│       ├── 📄 dashboard.html           # Dashboard de métricas gerais
│       ├── 📄 hello.html               # Exemplo de página (Hello World)
│       ├── 📄 historico.html           # Histórico de pesquisas realizadas
│       ├── 📄 index.html               # Página inicial de busca de itens
│       ├── 📄 resultado.html           # Página de resultados de uma pesquisa
│       └── 📁 auth/                    # Templates de autenticação
│           ├── 📄 audit.html           # Log de auditoria
│           ├── 📄 change_password.html # Alterar senha do usuário
│           ├── 📄 create_user.html     # Criar novo usuário (admin)
│           ├── 📄 login.html           # Página de login
│           ├── 📄 profile.html         # Perfil do usuário
│           └── 📄 register.html        # Registro de novo usuário
├── 📁 data/                            # Diretório para arquivos de dados (e.g., catálogos CSV)
├── 📁 instance/                        # Arquivos de instância (e.g., banco de dados SQLite)
│   └── 📄 preco_agil.db
├── 📁 migrations/                      # Scripts de migração do banco de dados (Alembic/Flask-Migrate)
│   └── 📁 versions/                    # Versões das migrações
│       └── 📄 ceb304052287_criacao_inicial_da_tabela_pesquisa.py # Exemplo de migração
├── 📁 reports/                         # Relatórios PDF gerados
│   └── 📄 ...                          # Arquivos de relatório
├── 📁 src/                             # Arquivos fonte (potencialmente estáticos ou legado)
│   └── 📄 index.html                   # (Exemplo)
└── 📁 tests/                           # Testes unitários e de integração
    └── 📄 test_app.py                  # Testes para a aplicação Flask
```

---

## Código Fonte Completo

--- START OF FILE: ./GEMINI.md ---

```
# Gemini AI Rules for Python with Flask Projects

## 1. Persona & Expertise

You are an expert back-end developer with a deep specialization in Python and the Flask micro-framework. You are proficient in building robust, scalable, and secure web applications and APIs. Your expertise includes routing, request handling, middleware, and best practices for structuring Flask projects, including the use of Blueprints.

## 2. Project Context

This project is a web application or API built with Python and the Flask framework. The focus is on creating a lightweight, modular, and maintainable server-side application. Assume the project uses a virtual environment and manages dependencies via a `requirements.txt` file.

## 3. Development Environment

The project is configured to run in a Nix-based environment managed by Firebase Studio. Here are the key details of the setup from the `dev.nix` configuration:

- **Python Environment:** The environment uses Python 3. A virtual environment is automatically created at `.venv`.
- **Dependency Management:** Project dependencies are listed in `requirements.txt`. They are automatically installed into the virtual environment when the workspace is first created.
- **Activation:** To work with the project's dependencies in the terminal, you must first activate the virtual environment:
  ```bash
  source .venv/bin/activate
  ```
- **Running the Server:** The Flask development server can be started using the `web` preview task, which executes the `./devserver.sh` script. This script handles running the Flask development server on the correct port for the preview panel.
- **Tooling:** The workspace is pre-configured with the official Microsoft Python extension for VS Code, providing features like linting, debugging, and IntelliSense. Depending on the template variation, it may also include the Thunder Client extension for testing API endpoints.

When providing assistance, assume this environment is set up. Remind the user to activate the virtual environment (`source .venv/bin/activate`) before running any `pip` or `python` commands in the terminal.

## 4. Coding Standards & Best Practices

### General
- **Language:** Use modern, idiomatic Python 3. Follow the PEP 8 style guide.
- **Dependencies:** Manage all project dependencies using a `requirements.txt` file and a virtual environment. After suggesting a new package, remind the user to add it to `requirements.txt` and run `pip install -r requirements.txt`.
- **Testing:** Encourage the use of a testing framework like Pytest for unit and integration tests.

### Python & Flask Specific
- **Security:**
    - **Secrets Management:** Never hard-code secrets like `SECRET_KEY` or database credentials. Use environment variables and a library like `python-dotenv` to load them from a `.env` file.
    - **Input Validation:** Use a library like Flask-WTF or Marshmallow to validate and sanitize all user input.
    - **Database Security:** If using an ORM like SQLAlchemy, use its features to prevent SQL injection.
- **Project Structure:**
    - **Blueprints:** Use Flask Blueprints to organize the application into smaller, reusable components. Keep related routes, templates, and static files grouped within a blueprint.
    - **Application Factory:** Use the application factory pattern to create instances of the Flask application. This is useful for testing and managing different configurations.
- **Asynchronous Tasks:**
    - For long-running or resource-intensive AI tasks, suggest using a task queue like Celery with Redis or RabbitMQ to avoid blocking web requests.
- **AI Model Integration:**
    - **Model Loading:** Load AI models once when the application starts, not on each request, to improve performance.
    - **Decoupling:** For large-scale applications, consider deploying AI models as separate services and having the Flask application interact with them via an API.
- **Performance:**
    - **Caching:** Recommend caching strategies for expensive computations or database queries.
    - **WSGI Server:** For production, advise using a production-ready WSGI server like Gunicorn or uWSGI.

## 5. Interaction Guidelines

- Assume the user is familiar with Python and the basics of web development.
- Provide clear and actionable code examples for creating routes, using Blueprints, and interacting with AI services.
- Break down complex tasks, like setting up a task queue or configuring authentication, into smaller, manageable steps.
- If a request is ambiguous, ask for clarification about the specific blueprint, route, or desired functionality.
- When discussing security, provide specific libraries and techniques to address common vulnerabilities in Flask applications.
```

--- END OF FILE: ./GEMINI.md ---

--- START OF FILE: ./README.md ---

```
🚀 Preço Ágil
Sistema de Pesquisa de Preços para Licitações Públicas

📋 Descrição
O Preço Ágil é uma ferramenta completa para realizar pesquisas de preços conforme a Lei 14.133/2021 (Nova Lei de Licitações) e as Portarias TCU 121, 122 e 123/2023.

✅ Funcionalidades
🔍 Busca em múltiplas fontes oficiais (PNCP, ComprasNet, Painel de Preços)
📊 Análise estatística robusta (mediana, média saneada)
📄 Geração automática de relatórios em PDF
✅ Validação de fornecedores (CNPJ via Receita Federal)
💾 Histórico completo de pesquisas
🔄 Sistema de fallback (alta disponibilidade)

🎯 Conformidade Legal
✅ Lei 14.133/2021 - Nova Lei de Licitações
✅ Portaria TCU 121/2023 - Pesquisa de Preços
✅ Portaria TCU 122/2023 - Catálogo Eletrônico
✅ Portaria TCU 123/2023 - Sistema Nacional de Preços

🛠️ Tecnologias
Python 3.8+
Flask 3.0
SQLAlchemy
Pandas
ReportLab
APIs governamentais

📦 Instalação
1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/preco-agil.git
cd preco-agil
```
2. Crie ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```
3. Instale dependências
```bash
pip install -r requirements.txt
```
4. Configure os catálogos
Baixe os catálogos CATMAT e CATSER em formato CSV e coloque na pasta data/:

data/

├── catmat.csv (formato: codigo,descricao)

└── catser.csv (formato: codigo,descricao)

Fontes oficiais:

CATMAT: https://www.gov.br/compras/pt-br/acesso-a-informacao/catalogo-de-materiais
CATSER: https://www.gov.br/compras/pt-br/acesso-a-informacao/catalogo-de-servicos

5. Configure o .env
```bash
cp .env.example .env
# Edite o .env com suas configurações
```
6. Execute
```bash
python run.py
```
Acesse: http://localhost:8000

📊 APIs Integradas
Painel de Preços - Ministério da Economia (Prioridade 1)
PNCP - Portal Nacional de Contratações Públicas
ComprasNet - Sistema Integrado de Administração
Portal da Transparência - CGU
BrasilAPI - Validação de CNPJ

📖 Como Usar
1.  **Buscar Item**: Digite a descrição do produto/serviço
2.  **Selecionar**: Escolha o código CATMAT ou CATSER
3.  **Pesquisar**: O sistema coleta preços de todas as fontes
4.  **Analisar**: Análise estatística automática
5.  **Download**: Baixe o relatório PDF completo

🤝 Contribuindo
Contribuições são bem-vindas! Por favor:

1.  Fork o projeto
2.  Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3.  Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4.  Push para a branch (`git push origin feature/nova-funcionalidade`)
5.  Abra um Pull Request

📄 Licença
Este projeto está sob a licença MIT.

👥 Autores
*   **Seu Nome** - _Trabalho Inicial_ - [@seu-usuario](https://github.com/seu-usuario)

🙏 Agradecimentos
*   TCU - Pela documentação e orientações
*   Comunidade Open Source brasileira
*   Mantenedores das APIs governamentais

📁 ESTRUTURA DE ARQUIVOS CSV
Formato esperado para `catmat.csv`:
```csv
codigo,descricao
123456,CADEIRA GIRATÓRIA PARA ESCRITÓRIO
234567,MESA DE ESCRITÓRIO EM MADEIRA
345678,COMPUTADOR DESKTOP CORE I5
```
OU com ponto-e-vírgula:
```csv
codigo;descricao
123456;CADEIRA GIRATÓRIA PARA ESCRITÓRIO
234567;MESA DE ESCRITÓRIO EM MADEIRA
345678;COMPUTADOR DESKTOP CORE I5
```

Formato esperado para `catser.csv`:
```csv
codigo,descricao
11001,SERVIÇO DE LIMPEZA E CONSERVAÇÃO
22002,SERVIÇO DE VIGILÂNCIA ARMADA
33003,SERVIÇO DE MANUTENÇÃO PREDIAL
```
```

--- END OF FILE: ./README.md ---

--- START OF FILE: ./config.py ---

```
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
    PAINEL_PRECOS_URL = os.getenv(
        "PAINEL_PRECOS_URL",
        "https://paineldeprecos.planejamento.gov.br/api/v1"
    )
    PAINEL_PRECOS_TIMEOUT = int(os.getenv("PAINEL_PRECOS_TIMEOUT", "30"))
    PAINEL_PRECOS_MAX_RESULTS = int(os.getenv("PAINEL_PRECOS_MAX_RESULTS", "1000"))
    PAINEL_PRECOS_CACHE_TTL = int(os.getenv("PAINEL_PRECOS_CACHE_TTL", "3600"))
    
    # Rate limiting
    PAINEL_PRECOS_RATE_LIMIT = float(os.getenv("PAINEL_PRECOS_RATE_LIMIT", "0.5"))
    
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
```

--- END OF FILE: ./config.py ---

--- START OF FILE: ./devserver.sh ---

```
#!/bin/sh
source .venv/bin/activate
# Usamos 'run' como app, e definimos a porta 8000 como padrão caso $PORT não exista.
python -u -m flask --app run run --host=0.0.0.0 --port=${PORT:-8000} --debug
```

--- END OF FILE: ./devserver.sh ---

--- START OF FILE: ./requirements.txt ---

```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
requests==2.31.0
pandas==2.1.3
numpy==1.26.2
sqlalchemy==2.0.23
scipy==1.11.4
reportlab==4.0.7
python-dotenv==1.0.0
Werkzeug==3.0.1
plotly==5.18.0
matplotlib==3.8.2
seaborn==0.13.0
openpyxl==3.1.2
xlsxwriter==3.1.9
Flask-Mail==0.9.1
Flask-Login==0.6.3
Flask-Bcrypt==1.0.1
Flask-JWT-Extended==4.6.0
APScheduler==3.10.4
celery==5.3.4
redis==5.0.1
Flask-Limiter==3.5.0
```

--- END OF FILE: ./requirements.txt ---

--- START OF FILE: ./run.py ---

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Preço Ágil - Sistema de Pesquisa de Preços para Licitações

Conforme:
- Lei 14.133/2021 (Nova Lei de Licitações)
- Portaria TCU 121/2023 (Pesquisa de Preços)
- Portaria TCU 122/2023 (Catálogo Eletrônico)
- Portaria TCU 123/2023 (Sistema Nacional de Preços)
"""

from app.models import create_app
from config import Config
import os

# Cria a aplicação
app = create_app()

if __name__ == '__main__':
    # Cria diretórios necessários
    os.makedirs(Config.DATA_DIR, exist_ok=True)
    os.makedirs(Config.REPORTS_DIR, exist_ok=True)
    
    # Banner
    print("\n" + "="*70)
    print("🚀 PREÇO ÁGIL - SISTEMA DE PESQUISA DE PREÇOS")
    print("="*70)
    print(f"📋 Versão: {Config.APP_VERSION}")
    print(f"📋 Lei 14.133/2021 | Portarias TCU 121, 122 e 123/2023")
    print("="*70)
    print(f"🌐 Servidor: http://{Config.HOST}:{Config.PORT}")
    print(f"📊 Ambiente: {'Desenvolvimento' if Config.DEBUG else 'Produção'}")
    print(f"💾 Banco: {Config.SQLALCHEMY_DATABASE_URI}")
    print(f"📁 CATMAT: {'✅' if os.path.exists(Config.CATMAT_FILE) else '❌'} {Config.CATMAT_FILE}")
    print(f"📁 CATSER: {'✅' if os.path.exists(Config.CATSER_FILE) else '❌'} {Config.CATSER_FILE}")
    print("="*70 + "\n")
    
    # Verifica arquivos CSV
    if not os.path.exists(Config.CATMAT_FILE):
        print("⚠️ AVISO: Arquivo catmat.csv não encontrado em data/")
        print("   Coloque o arquivo CSV com as colunas: codigo,descricao\n")
    
    if not os.path.exists(Config.CATSER_FILE):
        print("⚠️ AVISO: Arquivo catser.csv não encontrado em data/")
        print("   Coloque o arquivo CSV com as colunas: codigo,descricao\n")
    
    # Inicia o servidor
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
```

--- END OF FILE: ./run.py ---

--- START OF FILE: ./app/auth.py ---

```
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
```

--- END OF FILE: ./app/auth.py ---

--- START OF FILE: ./app/context_processors.py ---

```
# -*- coding: utf-8 -*-
"""
Context Processors - Injeta variáveis globais em todos os templates
"""

from config import Config

def inject_global_vars():
    """
    Injeta variáveis globais de configuração em todos os templates.
    Isso evita ter que passar essas variáveis em cada chamada `render_template`.
    """
    return {
        'app_version': Config.APP_VERSION,
        'app_description': Config.APP_DESCRIPTION,
        'app_name': Config.APP_NAME
    }
```

--- END OF FILE: ./app/context_processors.py ---

--- START OF FILE: ./app/routes.py ---

```
# -*- coding: utf-8 -*-
"""
Preço Ágil - Rotas da Aplicação Flask
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file, jsonify, current_app
from flask_login import login_required, current_user
from app.models import db
from app.models.models import Pesquisa
from app.services.price_collector_enhanced import EnhancedPriceCollector
from app.services.statistical_analyzer import StatisticalAnalyzer
from app.services.document_generator import DocumentGenerator
from app.services.chart_generator import ChartGenerator
from app.auth import audit_log, admin_required
from config import Config
from datetime import datetime, timedelta
import os

bp = Blueprint('main', __name__)

# Inicializa serviços
collector = EnhancedPriceCollector()
analyzer = StatisticalAnalyzer()
doc_generator = DocumentGenerator()
chart_gen = ChartGenerator()


@bp.route('/')
@login_required
def index():
    """Página inicial"""
    return render_template('index.html')


@bp.route('/buscar-item', methods=['POST'])
@login_required
def buscar_item():
    """Busca item nos catálogos"""
    descricao = request.form.get('descricao', '').strip()
    
    if not descricao or len(descricao) < 3:
        flash('Por favor, informe uma descrição com pelo menos 3 caracteres.', 'warning')
        return redirect(url_for('main.index'))
    
    try:
        resultados = collector.search_item(descricao)
        
        if resultados['total'] == 0:
            flash('Nenhum item encontrado. Tente usar outras palavras-chave.', 'info')
        else:
            flash(f"Encontrados {{resultados['total']}} itens.", 'success')
        
        return render_template('index.html', descricao_buscada=descricao, resultados=resultados)
    
    except Exception as e:
        current_app.logger.error(f'Erro na busca de item: {{e}}')
        flash('Erro ao buscar item. Tente novamente.', 'danger')
        return redirect(url_for('main.index'))


@bp.route('/pesquisar-precos', methods=['POST'])
@login_required
def pesquisar_precos():
    """Executa pesquisa de preços"""
    item_code = request.form.get('item_code', '').strip()
    catalog_type = request.form.get('catalog_type', '').strip()
    region = request.form.get('region', '').strip() or None
    responsible_agent = current_user.full_name
    
    if not item_code or not catalog_type:
        flash('Código do item e tipo são obrigatórios.', 'danger')
        return redirect(url_for('main.index'))

    try:
        # Coleta preços
        price_data = collector.collect_prices_with_fallback(item_code, catalog_type, region=region)
        
        if price_data['total_prices'] == 0:
            flash('Nenhum preço encontrado para este item.', 'warning')
            return render_template('resultado.html', error=True)

        # Extrai valores para análise
        prices_values = [p['price'] for p in price_data['prices'] if p.get('price') and p['price'] > 0]
        
        if not prices_values:
            flash('Nenhum preço válido encontrado.', 'danger')
            return render_template('resultado.html', error=True)
        
        # Análise estatística
        stats = analyzer.analyze_prices(prices_values)
        
        if 'error' in stats:
            flash(stats['error'], 'danger')
            return render_template('resultado.html', error=True)

        # Informações do catálogo
        catalog_info = collector.get_catalog_info(item_code, catalog_type)
        
        # Monta dados da pesquisa
        research_data = {{
            'item_code': item_code,
            'catalog_type': catalog_type,
            'catalog_info': catalog_info,
            'catalog_source': 'CATMAT' if catalog_type == 'material' else 'CATSER',
            'responsible_agent': responsible_agent,
            'research_date': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'sources_consulted': price_data['sources'],
            'prices_collected': price_data['prices'],
            'filters_applied': price_data['filters'],
            'sample_size': len(prices_values)
        }}

        # Gera gráficos
        charts = {{
            'histogram': chart_gen.create_histogram(prices_values, stats),
            'boxplot': chart_gen.create_boxplot(prices_values, stats),
            'timeline': chart_gen.create_timeline(price_data['prices']),
            'scatter': chart_gen.create_scatter_by_source(price_data['prices'])
        }}

        # Gera PDF
        pdf_filename = None
        try:
            pdf_data = {{**research_data, 'statistical_analysis': stats}}
            pdf_path = doc_generator.generate_research_report(pdf_data)
            pdf_filename = os.path.basename(pdf_path)
        except Exception as e:
            current_app.logger.error(f'Erro ao gerar PDF: {{e}}')

        # Serializa datas para JSON
        prices_serializable = []
        for p in price_data['prices']:
            p_copy = p.copy()
            if isinstance(p_copy.get('date'), datetime):
                p_copy['date'] = p_copy['date'].isoformat()
            prices_serializable.append(p_copy)
        
        # Salva no banco
        db_research = Pesquisa(
            user_id=current_user.id,
            item_code=item_code,
            item_description=catalog_info.get('description', 'N/A'),
            catalog_type=catalog_type,
            responsible_agent=responsible_agent,
            stats=stats,
            prices_collected=prices_serializable,
            sources_consulted=price_data['sources'],
            pdf_filename=pdf_filename
        )
        
        try:
            db.session.add(db_research)
            db.session.commit()
            research_id = db_research.id
            
            flash('Pesquisa concluída e salva com sucesso!', 'success')
            
            audit_log(
                'pesquisa_criada', 'pesquisa', research_id,
                {{'item': f"{{item_code}} ({{catalog_type}})", 'valor': stats.get('estimated_value')}}
            )
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Erro ao salvar: {{e}}')
            research_id = None

        return render_template('resultado.html', 
                             research=research_data, 
                             stats=stats, 
                             pdf_filename=pdf_filename, 
                             research_id=research_id, 
                             charts=charts)

    except Exception as e:
        current_app.logger.error(f'Erro na pesquisa: {{e}}')
        import traceback
        traceback.print_exc()
        flash(f'Erro ao realizar pesquisa: {{e}}', 'danger')
        return render_template('resultado.html', error=True)


@bp.route('/download-pdf/<filename>')
@login_required
def download_pdf(filename):
    """Download de PDF"""
    try:
        reports_dir = current_app.config['REPORTS_DIR']
        filepath = os.path.join(reports_dir, filename)
        
        if not os.path.exists(filepath):
            flash('Arquivo PDF não encontrado.', 'danger')
            return redirect(url_for('main.index'))
        
        return send_file(filepath, as_attachment=True)
    
    except Exception as e:
        current_app.logger.error(f'Erro no download: {{e}}')
        flash('Erro ao baixar PDF.', 'danger')
        return redirect(url_for('main.index'))


@bp.route('/historico')
@login_required
def historico():
    """Histórico de pesquisas"""
    try:
        page = request.args.get('page', 1, type=int)
        
        # Controle de acesso
        if current_user.is_gestor:
            query = Pesquisa.query
        else:
            query = Pesquisa.query.filter_by(user_id=current_user.id)

        pagination = query.order_by(
            Pesquisa.research_date.desc()
        ).paginate(page=page, per_page=15, error_out=False)
        
        return render_template('historico.html', pesquisas=pagination.items, pagination=pagination)
        
    except Exception as e:
        current_app.logger.error(f'Erro no histórico: {{e}}')
        flash('Erro ao carregar histórico.', 'danger')
        return redirect(url_for('main.index'))


@bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard geral"""
    try:
        if current_user.is_gestor:
            query = Pesquisa.query
        else:
            query = Pesquisa.query.filter_by(user_id=current_user.id)

        all_pesquisas = query.all()
        
        if len(all_pesquisas) == 0:
            flash('Ainda não há dados para o dashboard.', 'info')
            return redirect(url_for('main.index'))
        
        stats_gerais = {{
            'total_pesquisas': len(all_pesquisas),
            'pesquisas_recentes': len([p for p in all_pesquisas if p.research_date >= datetime.now() - timedelta(days=30)]),
            'valor_medio': sum([p.estimated_value for p in all_pesquisas if p.estimated_value]) / len(all_pesquisas),
            'materiais': len([p for p in all_pesquisas if p.catalog_type == 'material']),
            'servicos': len([p for p in all_pesquisas if p.catalog_type == 'servico']),
            'metodos': {{}}
        }}
        
        return render_template('dashboard.html', stats=stats_gerais, charts={{}}, top_itens=[])
        
    except Exception as e:
        current_app.logger.error(f'Erro no dashboard: {{e}}')
        flash('Erro ao carregar dashboard.', 'danger')
        return redirect(url_for('main.index'))


@bp.app_template_filter('currency')
def currency_filter(value):
    """Filtro para formatar valores monetários"""
    try:
        return f"R$ {{float(value):,.2f}}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError):
        return 'R$ 0,00'
```

--- END OF FILE: ./app/routes.py ---

--- START OF FILE: ./app/api/__init__.py ---

```
# -*- coding: utf-8 -*-
"""
Preço Ágil - Módulo de APIs
Integrações com fontes governamentais e auxiliares
"""

from app.api.catmat_api import CATMATClient
from app.api.catser_api import CATSERClient
# from app.api.pncp_api import PNCPClient # Comentado, pois ainda não foi refatorado
# from app.api.comprasnet_api import ComprasNetClient # Comentado, pois ainda não foi refatorado
# from app.api.painel_precos_api import PainelPrecosClient # Comentado, pois ainda não foi refatorado
from app.api.portal_transparencia_api import PortalTransparenciaClient
from app.api.brasilapi_client import BrasilAPIClient
# from app.api.fallback_manager import APIFallbackManager, exponential_backoff, rate_limit

__all__ = [
    'CATMATClient',
    'CATSERClient',
    'PortalTransparenciaClient',
    'BrasilAPIClient',
    # 'PNCPClient',
    # 'ComprasNetClient',
    # 'PainelPrecosClient',
    # 'APIFallbackManager',
    # 'exponential_backoff',
    # 'rate_limit'
]
```

--- END OF FILE: ./app/api/__init__.py ---

--- START OF FILE: ./app/api/brasil_api.py ---

```
import requests
import time
from config import RETRY_ATTEMPTS, RETRY_DELAY

# This is a community-driven, free API. Good for supplementary data.
BASE_URL = "https://brasilapi.com.br/api"

def get_cnpj_details(cnpj: str, retries=RETRY_ATTEMPTS):
    """
    Fetches company details from the BrasilAPI based on a CNPJ.

    Args:
        cnpj (str): The CNPJ of the company to look up.
        retries (int): The number of times to retry the request.

    Returns:
        dict: A dictionary containing details about the company, or an empty dict on failure.
    """
    if not cnpj:
        return {}

    endpoint = f"{BASE_URL}/cnpj/v1/{cnpj}"
    
    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1}/{retries} to fetch CNPJ {cnpj} from BrasilAPI...")
            response = requests.get(endpoint, timeout=10)
            response.raise_for_status()
            print(f"Successfully fetched details for CNPJ {cnpj}.")
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for BrasilAPI (CNPJ {cnpj}): {e}")
            if attempt < retries - 1:
                wait_time = RETRY_DELAY ** (attempt + 1)
                print(f"Waiting {wait_time} seconds before next retry.")
                time.sleep(wait_time)
    
    print(f"All retries failed for CNPJ {cnpj}.")
    return {}
```

--- END OF FILE: ./app/api/brasil_api.py ---

--- START OF FILE: ./app/api/brasilapi_client.py ---

```

# app/api/brasilapi_client.py
"""
Cliente para BrasilAPI - Validação de CNPJ, CEP, Bancos
Documentação: https://brasilapi.com.br/docs
"""

import logging
from typing import Dict, Optional
from app.api.base_client import BaseAPIClient

logger = logging.getLogger(__name__)


class BrasilAPIClient(BaseAPIClient):
    """Cliente para BrasilAPI com cache e retry automáticos"""
    
    def __init__(self):
        super().__init__(
            base_url='https://brasilapi.com.br/api',
            timeout=10,
            cache_ttl=86400  # 24 horas para dados que mudam pouco
        )
    
    def get_cnpj_info(self, cnpj: str) -> Optional[Dict]:
        """
        Obtém informações de CNPJ da Receita Federal
        
        Args:
            cnpj: CNPJ com ou sem formatação
        
        Returns:
            Dados do CNPJ ou None se não encontrado
        """
        # Remove formatação
        cnpj_clean = ''.join(filter(str.isdigit, cnpj))
        
        if len(cnpj_clean) != 14:
            logger.warning(f"CNPJ inválido (tamanho incorreto): {cnpj}")
            return None
        
        endpoint = f'/cnpj/v1/{cnpj_clean}'
        data = self.get(endpoint)
        
        if not data:
            return None
        
        # Formata resposta padronizada
        return {
            'cnpj': data.get('cnpj'),
            'razao_social': data.get('razao_social'),
            'nome_fantasia': data.get('nome_fantasia'),
            'situacao': data.get('descricao_situacao_cadastral'),
            'data_situacao': data.get('data_situacao_cadastral'),
            'uf': data.get('uf'),
            'municipio': data.get('municipio'),
            'bairro': data.get('bairro'),
            'logradouro': data.get('logradouro'),
            'numero': data.get('numero'),
            'cep': data.get('cep'),
            'email': data.get('email'),
            'telefone': data.get('ddd_telefone_1'),
            'porte': data.get('porte'),
            'natureza_juridica': data.get('natureza_juridica'),
            'atividade_principal': data.get('cnae_fiscal_descricao'),
            'capital_social': data.get('capital_social')
        }
    
    def get_cep_info(self, cep: str) -> Optional[Dict]:
        """Obtém informações de CEP"""
        cep_clean = ''.join(filter(str.isdigit, cep))
        
        if len(cep_clean) != 8:
            logger.warning(f"CEP inválido: {cep}")
            return None
        
        endpoint = f'/cep/v2/{cep_clean}'
        return self.get(endpoint)
    
    def get_banco_info(self, codigo_banco: str) -> Optional[Dict]:
        """Obtém informações de banco"""
        codigo_clean = ''.join(filter(str.isdigit, codigo_banco)).zfill(3)
        endpoint = f'/banks/v1/{codigo_clean}'
        return self.get(endpoint)
    
    def validate_supplier(self, cnpj: str) -> Dict:
        """
        Valida fornecedor com checagens completas
        
        Returns:
            {
                'valid': bool,
                'reason': str (se inválido),
                'cnpj_info': dict (se válido),
                'warnings': list
            }
        """
        if not cnpj:
            return {
                'valid': False,
                'reason': 'CNPJ não informado'
            }
        
        cnpj_info = self.get_cnpj_info(cnpj)
        
        if not cnpj_info:
            return {
                'valid': False,
                'reason': 'CNPJ não encontrado na Receita Federal'
            }
        
        # Verifica situação cadastral
        situacao = (cnpj_info.get('situacao') or '').upper()
        
        if 'ATIVA' not in situacao:
            return {
                'valid': False,
                'reason': f'Situação cadastral irregular: {situacao}',
                'cnpj_info': cnpj_info
            }
        
        # Coleta warnings (não impedem, mas alertam)
        warnings = []
        if not cnpj_info.get('email'):
            warnings.append('Email não cadastrado')
        if not cnpj_info.get('telefone'):
            warnings.append('Telefone não cadastrado')
        
        return {
            'valid': True,
            'cnpj_info': cnpj_info,
            'warnings': warnings
        }
```

--- END OF FILE: ./app/api/brasilapi_client.py ---

--- START OF FILE: ./app/api/catmat_api.py ---

```
# -*- coding: utf-8 -*-
"""
Cliente para catálogo CATMAT (CSV) - VERSÃO ROBUSTA
Preço Ágil - Sistema de Pesquisa de Preços
"""

import pandas as pd
import unicodedata
from typing import List, Dict, Optional
from config import Config
import os
import logging

logger = logging.getLogger(__name__)


class CATMATClient:
    """Cliente para catálogo CATMAT em formato CSV"""
    
    def __init__(self):
        self.catalog = None
        self.catalog_df = None
        self.load_catalog()
    
    def load_catalog(self):
        """
        Carrega catálogo CATMAT do arquivo CSV
        
        Parser ROBUSTO que aceita:
        - Linhas com campos variados
        - Diferentes delimitadores (vírgula, ponto-vírgula)
        - Linhas de cabeçalho extras
        - Campos com vírgulas dentro (entre aspas)
        """
        try:
            if not os.path.exists(Config.CATMAT_FILE):
                logger.warning(f"⚠️ Arquivo CATMAT não encontrado: {Config.CATMAT_FILE}")
                self.catalog = {}
                return
            
            logger.info(f"📂 Carregando CATMAT: {Config.CATMAT_FILE}")
            
            # ✅ PARSER ROBUSTO - Tenta múltiplas estratégias
            df = self._read_csv_robust(Config.CATMAT_FILE)
            
            if df is None or df.empty:
                logger.warning("⚠️ Arquivo CATMAT vazio ou inválido")
                self.catalog = {}
                return
            
            # ✅ Identifica colunas de código e descrição
            codigo_col, descricao_col = self._identify_columns(df)
            
            if not codigo_col or not descricao_col:
                logger.error("❌ Não foi possível identificar colunas no CATMAT")
                self.catalog = {}
                return
            
            # ✅ Limpa e valida dados
            df_clean = self._clean_dataframe(df, codigo_col, descricao_col)
            
            # ✅ Cria dicionário código: descrição
            self.catalog = dict(zip(
                df_clean[codigo_col].astype(str),
                df_clean[descricao_col].astype(str)
            ))
            
            self.catalog_df = df_clean
            
            logger.info(f"✅ CATMAT carregado: {len(self.catalog)} itens")
            
            # Exemplos
            if len(self.catalog) > 0:
                logger.info("📝 Exemplos:")
                for i, (cod, desc) in enumerate(list(self.catalog.items())[:3]):
                    logger.info(f"   • {cod}: {desc[:70]}...")
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar CATMAT: {e}")
            import traceback
            traceback.print_exc()
            self.catalog = {}
    
    
    def _read_csv_robust(self, filepath: str) -> Optional[pd.DataFrame]:
        """
        Lê CSV com múltiplas tentativas
        """
        
        strategies = [
            # ✅ Estratégia 1: Pula PRIMEIRA linha (cabeçalho extra)
            {
                'sep': ';',
                'on_bad_lines': 'skip',
                'encoding': 'utf-8',
                'skiprows': 1  # ✅ Pula linha "Consulta realizada em..."
            },
            # Estratégia 2: Pula DUAS linhas
            {
                'sep': ';',
                'on_bad_lines': 'skip',
                'encoding': 'utf-8',
                'skiprows': 2
            },
            # Estratégia 3: Latin-1, pula 1
            {
                'sep': ';',
                'on_bad_lines': 'skip',
                'encoding': 'latin-1',
                'skiprows': 1
            },
            # Estratégia 4: Vírgula
            {
                'sep': ',',
                'on_bad_lines': 'skip',
                'encoding': 'utf-8',
                'skiprows': 1
            },
            # Estratégia 5: Detector automático
            {
                'sep': None,
                'engine': 'python',
                'on_bad_lines': 'skip',
                'encoding': 'utf-8',
                'skiprows': 0
            }
        ]
        
        for i, strategy in enumerate(strategies):
            try:
                logger.debug(f"Tentativa {i+1}: {strategy}")
                df = pd.read_csv(filepath, **strategy, dtype=str, low_memory=False)
                
                # Remove linhas completamente vazias
                df = df.dropna(how='all')
                
                if not df.empty and len(df.columns) > 1:
                    logger.info(f"✅ CSV lido com estratégia {i+1}: {len(df)} linhas, {len(df.columns)} colunas")
                    logger.debug(f"Colunas: {list(df.columns)[:5]}")
                    return df
            
            except Exception as e:
                logger.debug(f"Estratégia {i+1} falhou: {e}")
                continue
        
        logger.error("❌ Todas as estratégias falharam")
        return None
    
    def _identify_columns(self, df: pd.DataFrame) -> tuple:
        """
        Identifica colunas de código e descrição
        
        Procura por:
        - Colunas com nome contendo 'codigo', 'code', 'item'
        - Colunas com nome contendo 'descricao', 'description'
        """
        
        codigo_col = None
        descricao_col = None
        
        # Procura por nome de coluna
        for col in df.columns:
            col_lower = str(col).lower()
            
            if not codigo_col and any(x in col_lower for x in ['codigo', 'code', 'item', 'catmat']):
                codigo_col = col
            
            if not descricao_col and any(x in col_lower for x in ['descricao', 'description', 'desc', 'nome']):
                descricao_col = col
        
        # Fallback: usa colunas por posição
        if not codigo_col or not descricao_col:
            logger.warning("⚠️ Usando colunas por posição (fallback)")
            
            if len(df.columns) >= 2:
                # Assume primeira coluna = código, segunda = descrição
                # OU usa as últimas 2 colunas
                if len(df.columns) >= 8:
                    codigo_col = df.columns[6]      # Coluna 7
                    descricao_col = df.columns[7]   # Coluna 8
                else:
                    codigo_col = df.columns[0]
                    descricao_col = df.columns[1]
                
                logger.info(f"📊 Colunas identificadas: [{codigo_col}] → [{descricao_col}]")
        
        return codigo_col, descricao_col
    
    
    def _clean_dataframe(self, df: pd.DataFrame, codigo_col: str, descricao_col: str) -> pd.DataFrame:
        """Limpa e valida dataframe"""
        
        try:
            # ✅ Verifica se colunas existem
            if codigo_col not in df.columns or descricao_col not in df.columns:
                logger.error(f"❌ Colunas não encontradas: {codigo_col}, {descricao_col}")
                return pd.DataFrame()
            
            # Seleciona apenas colunas necessárias
            df_clean = df[[codigo_col, descricao_col]].copy()
            
            # Remove NaN
            df_clean = df_clean.dropna()
            
            # ✅ CORREÇÃO: Acessa a Series corretamente
            df_clean.loc[:, codigo_col] = df_clean[codigo_col].astype(str).str.strip()
            df_clean.loc[:, descricao_col] = df_clean[descricao_col].astype(str).str.strip()
            
            # Remove vazios
            df_clean = df_clean[df_clean[codigo_col].astype(bool)]
            df_clean = df_clean[df_clean[descricao_col].astype(bool)]
            
            # Remove linhas que parecem cabeçalhos
            df_clean = df_clean[~df_clean[codigo_col].str.lower().str.contains('codigo|catmat', na=False)]
            
            # Remove duplicatas
            df_clean = df_clean.drop_duplicates(subset=[codigo_col])
            
            logger.debug(f"✅ DataFrame limpo: {{len(df_clean)}} linhas válidas")
            
            return df_clean
        
        except Exception as e:
            logger.error(f"❌ Erro ao limpar dataframe: {e}")
            return pd.DataFrame()

    
    def search_by_description(self, description: str, limit: int = 50) -> List[Dict]:
        """Busca códigos CATMAT por descrição"""
        if not self.catalog:
            return []
        
        palavras = [
            self._normalize(p) 
            for p in description.split() 
            if len(p) >= 3
        ]
        
        if not palavras:
            return []
        
        resultados = []
        
        for codigo, desc in self.catalog.items():
            desc_norm = self._normalize(desc)
            
            if all(palavra in desc_norm for palavra in palavras):
                resultados.append({
                    "codigo": codigo,
                    "descricao": desc,
                    "tipo": "material"
                })
                
                if len(resultados) >= limit:
                    break
        
        return resultados
    
    def get_description(self, code: str) -> Optional[str]:
        """Retorna descrição de um código CATMAT"""
        if not self.catalog:
            return None
        
        return self.catalog.get(str(code).strip())
    
    def search_by_code(self, code: str) -> Optional[Dict]:
        """Busca item por código exato"""
        desc = self.get_description(code)
        
        if desc:
            return {
                "codigo": code,
                "descricao": desc,
                "tipo": "material"
            }
        
        return None
    
    @staticmethod
    def _normalize(text: str) -> str:
        """Remove acentos e normaliza texto"""
        if not isinstance(text, str):
            text = str(text)
        
        text = unicodedata.normalize('NFD', text.lower())
        text = text.encode('ascii', 'ignore').decode('utf-8')
        text = ' '.join(text.split())
        
        return text
```

--- END OF FILE: ./app/api/catmat_api.py ---

--- START OF FILE: ./app/api/catser_api.py ---

```
# -*- coding: utf-8 -*-
"""
Cliente para catálogo CATSER (CSV) - VERSÃO ROBUSTA
Preço Ágil - Sistema de Pesquisa de Preços
"""

import pandas as pd
import unicodedata
from typing import List, Dict, Optional
from config import Config
import os
import logging

logger = logging.getLogger(__name__)


class CATSERClient:
    """Cliente para catálogo CATSER em formato CSV"""
    
    def __init__(self):
        self.catalog = None
        self.catalog_df = None
        self.load_catalog()
    
    def load_catalog(self):
        """Carrega catálogo CATSER do arquivo CSV"""
        try:
            if not os.path.exists(Config.CATSER_FILE):
                logger.warning(f"⚠️ Arquivo CATSER não encontrado: {Config.CATSER_FILE}")
                self.catalog = {}
                return
            
            logger.info(f"📂 Carregando CATSER: {Config.CATSER_FILE}")
            
            # ✅ PARSER ROBUSTO
            df = self._read_csv_robust(Config.CATSER_FILE)
            
            if df is None or df.empty:
                logger.warning("⚠️ Arquivo CATSER vazio ou inválido")
                self.catalog = {}
                return
            
            # ✅ Identifica colunas
            codigo_col, descricao_col = self._identify_columns(df)
            
            if not codigo_col or not descricao_col:
                logger.error("❌ Não foi possível identificar colunas no CATSER")
                self.catalog = {}
                return
            
            # ✅ Limpa dados
            df_clean = self._clean_dataframe(df, codigo_col, descricao_col)
            
            # ✅ Cria dicionário
            self.catalog = dict(zip(
                df_clean[codigo_col].astype(str),
                df_clean[descricao_col].astype(str)
            ))
            
            self.catalog_df = df_clean
            
            logger.info(f"✅ CATSER carregado: {len(self.catalog)} itens")
            
            # Exemplos
            if len(self.catalog) > 0:
                logger.info("📝 Exemplos:")
                for i, (cod, desc) in enumerate(list(self.catalog.items())[:3]):
                    logger.info(f"   • {cod}: {desc[:70]}...")
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar CATSER: {e}")
            import traceback
            traceback.print_exc()
            self.catalog = {}
    
    # ✅ Mesmos métodos do CATMAT
    
    def _read_csv_robust(self, filepath: str) -> Optional[pd.DataFrame]:
        """
        Lê CSV com múltiplas tentativas
        """
        
        strategies = [
            # ✅ Estratégia 1: Pula PRIMEIRA linha (cabeçalho extra)
            {
                'sep': ';',
                'on_bad_lines': 'skip',
                'encoding': 'utf-8',
                'skiprows': 1  # ✅ Pula linha "Consulta realizada em..."
            },
            # Estratégia 2: Pula DUAS linhas
            {
                'sep': ';',
                'on_bad_lines': 'skip',
                'encoding': 'utf-8',
                'skiprows': 2
            },
            # Estratégia 3: Latin-1, pula 1
            {
                'sep': ';',
                'on_bad_lines': 'skip',
                'encoding': 'latin-1',
                'skiprows': 1
            },
            # Estratégia 4: Vírgula
            {
                'sep': ',',
                'on_bad_lines': 'skip',
                'encoding': 'utf-8',
                'skiprows': 1
            },
            # Estratégia 5: Detector automático
            {
                'sep': None,
                'engine': 'python',
                'on_bad_lines': 'skip',
                'encoding': 'utf-8',
                'skiprows': 0
            }
        ]
        
        for i, strategy in enumerate(strategies):
            try:
                logger.debug(f"Tentativa {i+1}: {strategy}")
                df = pd.read_csv(filepath, **strategy, dtype=str, low_memory=False)
                
                # Remove linhas completamente vazias
                df = df.dropna(how='all')
                
                if not df.empty and len(df.columns) > 1:
                    logger.info(f"✅ CSV lido com estratégia {i+1}: {len(df)} linhas, {len(df.columns)} colunas")
                    logger.debug(f"Colunas: {list(df.columns)[:5]}")
                    return df
            
            except Exception as e:
                logger.debug(f"Estratégia {i+1} falhou: {e}")
                continue
        
        logger.error("❌ Todas as estratégias falharam")
        return None

        
    def _identify_columns(self, df: pd.DataFrame) -> tuple:
        """Identifica colunas de código e descrição"""
        codigo_col = None
        descricao_col = None
        
        for col in df.columns:
            col_lower = str(col).lower()
            
            if not codigo_col and any(x in col_lower for x in ['codigo', 'code', 'servico', 'catser']):
                codigo_col = col
            
            if not descricao_col and any(x in col_lower for x in ['descricao', 'description', 'desc', 'nome']):
                descricao_col = col
        
        # Fallback: posição
        if not codigo_col or not descricao_col:
            logger.warning("⚠️ Usando colunas por posição (fallback)")
            
            if len(df.columns) >= 7:
                codigo_col = df.columns[5]   # Coluna 6
                descricao_col = df.columns[6]   # Coluna 7
            elif len(df.columns) >= 2:
                codigo_col = df.columns[0]
                descricao_col = df.columns[1]
            
            logger.info(f"📊 Colunas: [{codigo_col}] → [{descricao_col}]")
        
        return codigo_col, descricao_col
    

    def _clean_dataframe(self, df: pd.DataFrame, codigo_col: str, descricao_col: str) -> pd.DataFrame:
        """Limpa e valida dataframe"""
        
        try:
            # ✅ Verifica se colunas existem
            if codigo_col not in df.columns or descricao_col not in df.columns:
                logger.error(f"❌ Colunas não encontradas: {codigo_col}, {descricao_col}")
                return pd.DataFrame()
            
            # Seleciona apenas colunas necessárias
            df_clean = df[[codigo_col, descricao_col]].copy()
            
            # Remove NaN
            df_clean = df_clean.dropna()
            
            # ✅ CORREÇÃO: Acessa a Series corretamente
            df_clean.loc[:, codigo_col] = df_clean[codigo_col].astype(str).str.strip()
            df_clean.loc[:, descricao_col] = df_clean[descricao_col].astype(str).str.strip()
            
            # Remove vazios
            df_clean = df_clean[df_clean[codigo_col].astype(bool)]
            df_clean = df_clean[df_clean[descricao_col].astype(bool)]
            
            # Remove linhas que parecem cabeçalhos
            df_clean = df_clean[~df_clean[codigo_col].str.lower().str.contains('codigo|catmat', na=False)]
            
            # Remove duplicatas
            df_clean = df_clean.drop_duplicates(subset=[codigo_col])
            
            logger.debug(f"✅ DataFrame limpo: {len(df_clean)} linhas válidas")
            
            return df_clean
        
        except Exception as e:
            logger.error(f"❌ Erro ao limpar dataframe: {e}")
            return pd.DataFrame()

    
    def search_by_description(self, description: str, limit: int = 50) -> List[Dict]:
        """Busca códigos CATSER por descrição"""
        if not self.catalog:
            return []
        
        palavras = [self._normalize(p) for p in description.split() if len(p) >= 3]
        if not palavras:
            return []
        
        resultados = []
        for codigo, desc in self.catalog.items():
            desc_norm = self._normalize(desc)
            if all(palavra in desc_norm for palavra in palavras):
                resultados.append({"codigo": codigo, "descricao": desc, "tipo": "servico"})
                if len(resultados) >= limit:
                    break
        
        return resultados
    
    def get_description(self, code: str) -> Optional[str]:
        """Retorna descrição"""
        if not self.catalog:
            return None
        return self.catalog.get(str(code).strip())
    
    def search_by_code(self, code: str) -> Optional[Dict]:
        """Busca por código"""
        desc = self.get_description(code)
        if desc:
            return {"codigo": code, "descricao": desc, "tipo": "servico"}
        return None
    
    @staticmethod
    def _normalize(text: str) -> str:
        """Normaliza texto"""
        if not isinstance(text, str):
            text = str(text)
        text = unicodedata.normalize('NFD', text.lower())
        text = text.encode('ascii', 'ignore').decode('utf-8')
        text = ' '.join(text.split())
        return text
```

--- END OF FILE: ./app/api/catser_api.py ---

--- START OF FILE: ./app/api/comprasnet_api.py ---

```

# app/api/comprasnet_api.py
"""
Cliente para ComprasNet
Documentação: https://compras.dados.gov.br/docs/
"""

import logging
from typing import List, Dict
from datetime import datetime
from app.api.base_client import BaseAPIClient

logger = logging.getLogger(__name__)


class ComprasNetClient(BaseAPIClient):
    """Cliente para API do ComprasNet"""
    
    def __init__(self):
        super().__init__(
            base_url='http://compras.dados.gov.br/compradores/v1',
            timeout=15,
            max_retries=2,
            rate_limit_calls=20,  # Mais conservador
            cache_ttl=3600
        )
    
    def search_material(self, item_code: str, max_pages: int = 2) -> List[Dict]:
        """Busca materiais por código CATMAT"""
        logger.info(f"Buscando materiais ComprasNet: {item_code}")
        return self._search_items('/materiais', 'codigoItemMaterial', item_code, max_pages, 'materiais')
    
    def search_service(self, item_code: str, max_pages: int = 2) -> List[Dict]:
        """Busca serviços por código CATSER"""
        logger.info(f"Buscando serviços ComprasNet: {item_code}")
        return self._search_items('/servicos', 'codigoItemServico', item_code, max_pages, 'servicos')
    
    def _search_items(
        self, 
        endpoint: str, 
        param_name: str, 
        item_code: str, 
        max_pages: int,
        data_key: str
    ) -> List[Dict]:
        """Busca itens com paginação"""
        all_items = []
        
        for page in range(1, max_pages + 1):
            params = {
                param_name: item_code,
                'pagina': page
            }
            
            data = self.get(endpoint, params)
            
            if not data:
                break
            
            items = data.get('_embedded', {}).get(data_key, [])
            
            if not items:
                logger.debug(f"Página {page} sem resultados, parando")
                break
            
            all_items.extend(self._parse_items(items))
            logger.debug(f"Página {page}: {len(items)} itens")
        
        logger.info(f"ComprasNet: total de {len(all_items)} itens coletados")
        return all_items
    
    def _parse_items(self, items: List[Dict]) -> List[Dict]:
        """Processa itens do ComprasNet"""
        parsed = []
        
        for item in items:
            try:
                valor = item.get('valorUnitario')
                if not valor or float(valor) <= 0:
                    continue
                
                data_str = item.get('dataResultadoCompra', '')
                if data_str:
                    date_obj = datetime.fromisoformat(data_str.split('T')[0])
                else:
                    continue
                
                parsed.append({
                    'source': 'ComprasNet',
                    'price': float(valor),
                    'date': date_obj,
                    'supplier': item.get('fornecedor', 'N/A'),
                    'entity': item.get('orgao', 'N/A'),
                    'region': item.get('uf', 'N/A')
                })
                
            except (ValueError, KeyError, TypeError) as e:
                logger.debug(f"Item ignorado: {e}")
                continue
        
        return parsed
```

--- END OF FILE: ./app/api/comprasnet_api.py ---

--- START OF FILE: ./app/api/fallback_manager.py ---

```
# -*- coding: utf-8 -*-
"""Gerenciador de Fallback e Resiliência (Simulado)"""

import time
from functools import wraps

class APIFallbackManager:
    """Classe placeholder para o gerenciador de fallback."""
    def __init__(self):
        print("   -> [SIMULADO] APIFallbackManager instanciado.")

def exponential_backoff(max_retries=3, base_delay=1):
    """Decorator simulado para exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Simplesmente chama a função original sem lógica de retry
            return func(*args, **kwargs)
        return wrapper
    return decorator

def rate_limit(calls_per_minute=60):
    """Decorator simulado para rate limiting."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Simplesmente chama a função original sem lógica de rate limiting
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

--- END OF FILE: ./app/api/fallback_manager.py ---

--- START OF FILE: ./app/api/painel_precos_api.py ---

```

# app/api/painel_precos_api.py

import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging
from functools import lru_cache
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

class PainelPrecosClient:
    """
    Cliente para API do Painel de Preços (Gov Federal)
    
    Funcionalidades:
    - ✅ Retry automático com backoff
    - ✅ Cache inteligente
    - ✅ Rate limiting
    - ✅ Paginação automática
    - ✅ Validação de dados
    """
    
    BASE_URL = "https://paineldeprecos.planejamento.gov.br/api/v1"
    
    # Configurações
    MAX_RETRIES = 3
    BACKOFF_FACTOR = 0.5
    TIMEOUT = 30
    MAX_ITEMS_PER_REQUEST = 100  # API limita a 500, mas 100 é mais seguro
    
    def __init__(self, timeout: int = None):
        """
        Inicializa cliente do Painel de Preços
        
        Args:
            timeout: Timeout para requisições (default: 30s)
        """
        self.timeout = timeout or self.TIMEOUT
        self.session = self._create_session()
        
        # Cache simples (pode ser substituído por Redis)
        self._cache: Dict[str, tuple] = {}  # {key: (data, timestamp)}
        self._cache_ttl = 3600  # 1 hora
        
        # Rate limiting
        self._last_request_time = 0
        self._min_interval = 0.5  # Mínimo 0.5s entre requisições
    

    def _create_session(self) -> requests.Session:
        """Cria sessão com retry automático"""
        session = requests.Session()
        
        # Configurar retry strategy
        retry_strategy = Retry(
            total=self.MAX_RETRIES,
            backoff_factor=self.BACKOFF_FACTOR,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]  # ✅ CORRETO (urllib3 >= 2.0)
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Headers
        session.headers.update({
            "User-Agent": "PrecoAgil/1.0 (Pesquisa de Precos)",
            "Accept": "application/json"
        })
        
        return session

    
    def _rate_limit(self):
        """Implementa rate limiting simples"""
        elapsed = time.time() - self._last_request_time
        if elapsed < self._min_interval:
            sleep_time = self._min_interval - elapsed
            logger.debug(f"Rate limiting: aguardando {sleep_time:.2f}s")
            time.sleep(sleep_time)
        self._last_request_time = time.time()
    
    def _get_cache(self, key: str) -> Optional[List[Dict]]:
        """Recupera item do cache se válido"""
        if key in self._cache:
            data, timestamp = self._cache[key]
            age = time.time() - timestamp
            
            if age < self._cache_ttl:
                logger.debug(f"Cache hit: {key} (idade: {age:.0f}s)")
                return data
            else:
                # Remove item expirado
                del self._cache[key]
                logger.debug(f"Cache expirado: {key}")
        
        return None
    
    def _set_cache(self, key: str, data: List[Dict]):
        """Armazena item no cache"""
        self._cache[key] = (data, time.time())
        
        # Limpa cache se muito grande (máximo 100 itens)
        if len(self._cache) > 100:
            # Remove os 20 mais antigos
            items = sorted(self._cache.items(), key=lambda x: x[1][1])
            for key, _ in items[:20]:
                del self._cache[key]
            logger.debug(f"Cache limpo: removidos 20 itens antigos")
    
    def search_by_item(
        self, 
        item_code: str, 
        item_type: str,
        region: Optional[str] = None,
        max_days: int = 365,
        max_results: int = 1000
    ) -> List[Dict]:
        """
        Busca preços de um item no Painel de Preços
        
        Args:
            item_code: Código CATMAT ou CATSER
            item_type: 'material' ou 'servico'
            region: Sigla do estado (SP, RJ, etc)
            max_days: Idade máxima dos preços em dias
            max_results: Número máximo de resultados
            
        Returns:
            Lista de dicionários com os preços encontrados
            
        Raises:
            ValueError: Se parâmetros inválidos
            ConnectionError: Se falha de conexão
        """
        
        # ✅ VALIDAÇÃO DE ENTRADA
        if not item_code or not item_code.strip():
            raise ValueError("❌ Código do item é obrigatório")
        
        if item_type not in ['material', 'servico']:
            raise ValueError(f"❌ Tipo inválido: {item_type}. Use 'material' ou 'servico'")
        
        item_code = item_code.strip()
        
        # Verifica cache
        cache_key = f"{item_code}_{item_type}_{region}_{max_days}"
        cached = self._get_cache(cache_key)
        if cached is not None:
            logger.info(f"✅ Retornando {len(cached)} preços do cache")
            return cached
        
        # Faz requisição
        try:
            logger.info(f"🔍 Buscando preços: {item_code} ({item_type})")
            
            results = self._search_with_pagination(
                item_code=item_code,
                item_type=item_type,
                region=region,
                max_days=max_days,
                max_results=max_results
            )
            
            # Armazena no cache
            if results:
                self._set_cache(cache_key, results)
            
            logger.info(f"✅ Encontrados {len(results)} preços no Painel")
            return results
            
        except requests.exceptions.Timeout:
            logger.error(f"⏱️ Timeout ao buscar {item_code} (>{self.timeout}s)")
            raise ConnectionError("Timeout na API do Painel de Preços")
        
        except requests.exceptions.ConnectionError as e:
            logger.error(f"🔌 Erro de conexão: {e}")
            raise ConnectionError("Erro de conexão com Painel de Preços")
        
        except requests.exceptions.HTTPError as e:
            logger.error(f"❌ Erro HTTP: {e}")
            
            if e.response.status_code == 429:
                raise ConnectionError("Rate limit excedido no Painel de Preços")
            elif e.response.status_code == 404:
                logger.info(f"ℹ️ Item {item_code} não encontrado no Painel")
                return []
            else:
                raise ConnectionError(f"Erro HTTP {e.response.status_code}")
        
        except Exception as e:
            logger.error(f"❌ Erro inesperado: {e}", exc_info=True)
            raise
    
    def _search_with_pagination(
        self,
        item_code: str,
        item_type: str,
        region: Optional[str],
        max_days: int,
        max_results: int
    ) -> List[Dict]:
        """Busca com paginação automática"""
        
        all_results = []
        page = 0
        
        while len(all_results) < max_results:
            # Rate limiting
            self._rate_limit()
            
            # Parâmetros da requisição
            params = {
                "codigo_item": item_code,
                "tipo": item_type,
                "offset": page * self.MAX_ITEMS_PER_REQUEST,
                "limit": self.MAX_ITEMS_PER_REQUEST
            }
            
            # Filtro por região
            if region:
                params["uf"] = region.upper()
            
            # Filtro por data
            date_limit = datetime.now() - timedelta(days=max_days)
            params["data_inicio"] = date_limit.strftime("%Y-%m-%d")
            
            logger.debug(f"📄 Página {page + 1}: {params}")
            
            # Requisição
            response = self.session.get(
                f"{self.BASE_URL}/contratacoes",
                params=params,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            
            # Parse JSON
            data = response.json()
            items = data.get("_embedded", {}).get("contracoes", [])
            
            if not items:
                logger.debug(f"ℹ️ Nenhum item na página {page + 1}, finalizando")
                break
            
            # Processa e adiciona
            parsed = self._parse_items(items)
            all_results.extend(parsed)
            
            logger.debug(f"✅ Página {page + 1}: {len(parsed)} itens válidos")
            
            # Se retornou menos que o limite, não há mais páginas
            if len(items) < self.MAX_ITEMS_PER_REQUEST:
                logger.debug("ℹ️ Última página alcançada")
                break
            
            page += 1
            
            # Proteção contra loop infinito
            if page > 50:
                logger.warning("⚠️ Limite de 50 páginas alcançado")
                break
        
        return all_results[:max_results]  # Garante o limite
    
    def _parse_items(self, items: List[Dict]) -> List[Dict]:
        """
        Processa e valida itens retornados pela API
        
        Args:
            items: Lista de itens brutos da API
            
        Returns:
            Lista de itens processados e validados
        """
        parsed = []
        
        for item in items:
            try:
                # Extrai e valida preço
                price = self._extract_price(item)
                if price is None or price <= 0:
                    continue
                
                # Extrai e valida data
                date = self._extract_date(item)
                if date is None:
                    continue
                
                # Monta resultado
                result = {
                    "source": "Painel de Preços",
                    "price": price,
                    "date": date,
                    "quantity": self._extract_quantity(item),
                    "supplier": item.get("fornecedor_nome", "N/A"),
                    "supplier_cnpj": item.get("fornecedor_cpnj", None),
                    "entity": item.get("orgao_nome", "N/A"),
                    "region": item.get("uf", None),
                    "contract_number": item.get("numero_contrato", None),
                    "details_url": item.get("_links", {}).get("self", {}).get("href", None)
                }
                
                parsed.append(result)
                
            except Exception as e:
                logger.debug(f"⚠️ Item ignorado por erro: {e}")
                continue
        
        return parsed
    
    def _extract_price(self, item: Dict) -> Optional[float]:
        """Extrai preço unitário"""
        try:
            # Tenta vários campos possíveis
            price = (
                item.get("valor_unitario") or
                item.get("valor_unitario_homologado") or
                item.get("preco_unitario") or
                item.get("preco")
            )
            
            if price is None:
                return None
            
            return float(price)
        
        except (ValueError, TypeError):
            return None
    
    def _extract_date(self, item: Dict) -> Optional[datetime]:
        """Extrai data de forma robusta"""
        try:
            date_str = (
                item.get("data_assinatura") or
                item.get("data_contrato") or
                item.get("data_compra")
            )
            
            if not date_str:
                return None
            
            # Remove timezone se houver (ex: "2024-01-01T00:00:00Z")
            date_str = date_str.split("T")[0]
            
            return datetime.strptime(date_str, "%Y-%m-%d")
        
        except (ValueError, AttributeError):
            return None
    
    def _extract_quantity(self, item: Dict) -> int:
        """Extrai quantidade (com fallback para 1)"""
        try:
            qty = item.get("quantidade") or item.get("quantidade_item")
            return int(qty) if qty else 1
        except (ValueError, TypeError):
            return 1
    
    def clear_cache(self):
        """Limpa o cache manualmente"""
        self._cache.clear()
        logger.info("🧹 Cache limpo manualmente")
    
    def get_cache_stats(self) -> Dict:
        """Retorna estatísticas do cache"""
        total_items = len(self._cache)
        
        if total_items == 0:
            return {"total_items": 0, "avg_age": 0, "oldest": 0}
        
        now = time.time()
        ages = [now - timestamp for _, (_, timestamp) in self._cache.items()]
        
        return {
            "total_items": total_items,
            "avg_age": sum(ages) / len(ages),
            "oldest": max(ages) if ages else 0,
            "newest": min(ages) if ages else 0
        }
```

--- END OF FILE: ./app/api/painel_precos_api.py ---

--- START OF FILE: ./app/api/pncp_api.py ---

```
# -*- coding: utf-8 -*-
"""
Cliente PNCP - Portal Nacional de Contratações Públicas
"""

import requests
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta


class PNCPClient:
    """Cliente para API do PNCP (pública, sem necessidade de chave)"""
    
    def __init__(self):
        self.base_url = 'https://pncp.gov.br/api/consulta/v1'
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'PrecoAgil/1.0'
        })
    
    def search_contracts(
        self,
        item_code: str,
        catalog_type: str,
        max_days: int = 730,
        region: Optional[str] = None
    ) -> List[Dict]:
        """Busca contratos no PNCP"""
        
        endpoint = f"{self.base_url}/contratos"
        date_limit = datetime.now() - timedelta(days=max_days)
        
        params = {
            'dataInicial': date_limit.strftime('%Y%m%d'),
            'dataFinal': datetime.now().strftime('%Y%m%d'),
            'pagina': 1,
            'tamanhoPagina': 100
        }
        
        print(f"  🔗 GET {endpoint}")
        
        try:
            response = self.session.get(endpoint, params=params, timeout=20)
            print(f"  📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    contratos = data.get('data', [])
                    print(f"  ✅ {len(contratos)} contratos")
                    return self._parse_contracts(contratos)
                except Exception as e:
                    print(f"  ❌ Erro JSON: {e}")
                    return []
            else:
                print(f"  ⚠️ Erro HTTP {response.status_code}")
                return []
        
        except requests.exceptions.Timeout:
            print(f"  ⏱️ Timeout")
            return []
        except Exception as e:
            print(f"  ❌ Erro: {str(e)[:80]}")
            return []
    
    def _parse_contracts(self, contracts: List[Dict]) -> List[Dict]:
        """Processa contratos do PNCP"""
        items = []
        
        for contract in contracts:
            try:
                valor = (
                    contract.get('valorTotal') or
                    contract.get('valorGlobal') or
                    contract.get('valorInicial')
                )
                
                if not valor or float(valor) <= 0:
                    continue
                
                data_str = contract.get('dataAssinatura') or contract.get('dataPublicacao')
                if data_str:
                    try:
                        date_obj = datetime.strptime(data_str.split('T')[0], '%Y-%m-%d')
                    except:
                        continue
                else:
                    continue
                
                items.append({
                    'source': 'PNCP',
                    'price': float(valor),
                    'date': date_obj,
                    'supplier': contract.get('nomeRazaoSocialFornecedor', 'N/A'),
                    'supplier_cnpj': contract.get('niFornecedor'),
                    'entity': contract.get('orgaoEntidade', {}).get('razaoSocial', 'N/A'),
                    'region': contract.get('ufOrgao'),
                    'contract_number': contract.get('numeroControlePNCP')
                })
            
            except (ValueError, KeyError, TypeError):
                continue
        
        return items
```

--- END OF FILE: ./app/api/pncp_api.py ---

--- START OF FILE: ./app/api/portal_transparencia_api.py ---

```
# -*- coding: utf-8 -*-
"""
Cliente API Portal da Transparência
"""

import requests
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


class PortalTransparenciaClient:
    """Cliente para API do Portal da Transparência (CGU)"""
    
    def __init__(self):
        self.base_url = os.getenv(
            'PORTAL_TRANSPARENCIA_API_URL',
            'https://api.portaldatransparencia.gov.br/api-de-dados'
        )
        
        self.api_key = os.getenv('PORTAL_TRANSPARENCIA_API_KEY')
        
        if not self.api_key:
            print("⚠️ PORTAL_TRANSPARENCIA_API_KEY não configurada")
        else:
            print("✅ API Portal da Transparência OK")
        
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'chave-api-dados': self.api_key or ''
        })
    
    def search_contracts(
        self,
        item_description: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        max_results: int = 100
    ) -> List[Dict]:
        """Busca contratos por descrição"""
        
        if not self.api_key:
            print("  ⚠️ API key não configurada")
            return []
        
        if not end_date:
            end_date = datetime.now().strftime('%d/%m/%Y')
        
        if not start_date:
            start_date = (datetime.now() - timedelta(days=730)).strftime('%d/%m/%Y')
        
        endpoint = f"{self.base_url}/despesas/documentos"
        
        params = {
            'dataInicial': start_date,
            'dataFinal': end_date,
            'pagina': 1
        }
        
        print(f"  🔗 GET {endpoint}")
        
        try:
            response = self.session.get(endpoint, params=params, timeout=15)
            print(f"  📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    if isinstance(data, list):
                        filtered = [
                            item for item in data 
                            if item_description.lower() in str(item.get('descricao', '')).lower()
                        ]
                        
                        print(f"  ✅ {len(filtered)} contratos")
                        return self._parse_contracts(filtered[:max_results])
                    else:
                        return []
                
                except Exception as e:
                    print(f"  ❌ Erro JSON: {e}")
                    return []
            
            elif response.status_code == 401:
                print(f"  ❌ API Key inválida")
                return []
            else:
                print(f"  ⚠️ Erro HTTP {response.status_code}")
                return []
        
        except requests.exceptions.Timeout:
            print(f"  ⏱️ Timeout")
            return []
        except Exception as e:
            print(f"  ❌ Erro: {str(e)[:100]}")
            return []
    
    def _parse_contracts(self, contracts: List[Dict]) -> List[Dict]:
        """Processa contratos do Portal"""
        items = []
        
        for contract in contracts:
            try:
                valor = float(contract.get('valor', 0))
                
                if valor <= 0:
                    continue
                
                data_str = contract.get('data')
                if data_str:
                    try:
                        date_obj = datetime.strptime(data_str, '%d/%m/%Y')
                    except:
                        try:
                            date_obj = datetime.strptime(data_str.split('T')[0], '%Y-%m-%d')
                        except:
                            continue
                else:
                    continue
                
                items.append({
                    'source': 'Portal da Transparência',
                    'price': valor,
                    'date': date_obj,
                    'supplier': contract.get('fornecedor', {}).get('nome', 'N/A'),
                    'supplier_cnpj': contract.get('fornecedor', {}).get('cnpjFormatado'),
                    'entity': contract.get('orgao', {}).get('nome', 'N/A'),
                    'region': contract.get('uf'),
                    'contract_number': contract.get('numeroDocumento')
                })
            
            except (ValueError, KeyError, TypeError):
                continue
        
        return items
```

--- END OF FILE: ./app/api/portal_transparencia_api.py ---

--- START OF FILE: ./app/api/transparencia_api.py ---

```
import requests
import time
import os
from config import RETRY_ATTEMPTS, RETRY_DELAY

# NOTE: This API requires a key, which should be stored as an environment variable.
BASE_URL = "https://api.portaldatransparencia.gov.br/api-de-dados"
API_KEY = os.environ.get("TRANSPARENCIA_API_KEY", "") # Securely get key

def search_expenses(description: str, retries=RETRY_ATTEMPTS):
    """
    Searches for federal expenses related to a description in the Portal da Transparência API.

    Args:
        description (str): The description of the item to search for.
        retries (int): The number of times to retry the request.

    Returns:
        list: A list of dictionaries, where each dictionary represents a price from an expense record.
              Returns an empty list if the API key is missing or the call fails.
    """
    if not API_KEY:
        print("ERROR: TRANSPARENCIA_API_KEY environment variable not set. Skipping search.")
        return []

    # This is a hypothetical endpoint for searching for items in expenses.
    # The actual API may require a different approach (e.g., searching by contract).
    endpoint = f"{BASE_URL}/despesas/documentos"
    headers = {
        "chave-api-dados": API_KEY
    }
    params = {
        "descricao": description, # This parameter might not exist; it's a guess.
        "pagina": 1
    }

    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1}/{retries} to fetch data from Portal da Transparência...")
            response = requests.get(endpoint, headers=headers, params=params, timeout=20)
            response.raise_for_status()
            data = response.json()

            prices = []
            # This data structure is a pure assumption.
            for expense in data:
                prices.append({
                    "data_compra": expense.get("data"),
                    "fornecedor_cnpj": expense.get("cnpjFornecedor"),
                    "fornecedor_nome": expense.get("nomeFornecedor"),
                    "orgao_comprador": expense.get("orgao"),
                    "uf_comprador": None, # May not be available at this level
                    "valor_unitario": expense.get("valor"),
                    "descricao_item": expense.get("descricao"),
                    "quantidade": 1, # Often, expense records don't have quantity
                    "fonte": "Portal da Transparência"
                })
            
            print(f"Successfully fetched {len(prices)} prices from Portal da Transparência.")
            return prices

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for Portal da Transparência API: {e}")
            if attempt < retries - 1:
                wait_time = RETRY_DELAY ** (attempt + 1)
                print(f"Waiting {wait_time} seconds before next retry.")
                time.sleep(wait_time)

    print("All retries failed for Portal da Transparência API.")
    return []
```

--- END OF FILE: ./app/api/transparencia_api.py ---

--- START OF FILE: ./app/models/__init__.py ---

```
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
```

--- END OF FILE: ./app/models/__init__.py ---

--- START OF FILE: ./app/models/database.py ---

```
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
```

--- END OF FILE: ./app/models/database.py ---

--- START OF FILE: ./app/models/models.py ---

```
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
```

--- END OF FILE: ./app/models/models.py ---

--- START OF FILE: ./app/services/__init__.py ---

```

```

--- END OF FILE: ./app/services/__init__.py ---

--- START OF FILE: ./app/services/chart_generator.py ---

```

# -*- coding: utf-8 -*-
"""
Gerador de Gráficos - Preço Ágil
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from typing import List, Dict
from datetime import datetime

class ChartGenerator:
    """Gera gráficos interativos para análise de preços"""
    
    def __init__(self):
        self.colors = {
            'primary': '#0d6efd',
            'success': '#198754',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'info': '#0dcaf0'
        }
    
    def create_histogram(self, prices: List[float], stats: Dict) -> str:
        """
        Cria histograma de distribuição de preços
        
        Returns:
            HTML do gráfico
        """
        fig = go.Figure()
        
        # Histograma
        fig.add_trace(go.Histogram(
            x=prices,
            name='Distribuição',
            marker_color=self.colors['primary'],
            opacity=0.7,
            nbinsx=20
        ))
        
        # Linha da mediana
        fig.add_vline(
            x=stats['median'],
            line_dash="dash",
            line_color=self.colors['success'],
            annotation_text=f"Mediana: R$ {stats['median']:.2f}",
            annotation_position="top"
        )
        
        # Linha da média
        fig.add_vline(
            x=stats['mean'],
            line_dash="dot",
            line_color=self.colors['warning'],
            annotation_text=f"Média: R$ {stats['mean']:.2f}",
            annotation_position="bottom"
        )
        
        fig.update_layout(
            title="Distribuição de Preços",
            xaxis_title="Preço (R$)",
            yaxis_title="Frequência",
            hovermode='x',
            template='plotly_white',
            height=400
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_boxplot(self, prices: List[float], stats: Dict) -> str:
        """
        Cria boxplot mostrando quartis e outliers
        
        Returns:
            HTML do gráfico
        """
        fig = go.Figure()
        
        fig.add_trace(go.Box(
            y=prices,
            name='Preços',
            marker_color=self.colors['info'],
            boxmean='sd'  # Mostra média e desvio padrão
        ))
        
        fig.update_layout(
            title="Análise de Dispersão (Boxplot)",
            yaxis_title="Preço (R$)",
            template='plotly_white',
            height=400,
            showlegend=False
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_timeline(self, prices_data: List[Dict]) -> str:
        """
        Cria timeline de preços ao longo do tempo
        
        Args:
            prices_data: Lista com dicts contendo 'date' e 'price'
        
        Returns:
            HTML do gráfico
        """
        # Ordena por data
        sorted_prices = sorted(prices_data, key=lambda x: x['date'] if isinstance(x['date'], datetime) else datetime.fromisoformat(x['date']))
        
        dates = []
        values = []
        sources = []
        
        for p in sorted_prices:
            if isinstance(p['date'], datetime):
                dates.append(p['date'])
            else:
                dates.append(datetime.fromisoformat(p['date']))
            values.append(p['price'])
            sources.append(p['source'])
        
        fig = go.Figure()
        
        # Linha de preços
        fig.add_trace(go.Scatter(
            x=dates,
            y=values,
            mode='markers+lines',
            name='Preços',
            marker=dict(
                size=8,
                color=values,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Preço (R$)")
            ),
            text=sources,
            hovertemplate='<b>%{text}</b><br>Data: %{x|%d/%m/%Y}<br>Preço: R$ %{y:.2f}<extra></extra>'
        ))
        
        # Linha de tendência
        if len(dates) > 3:
            z = np.polyfit(range(len(values)), values, 1)
            p = np.poly1d(z)
            fig.add_trace(go.Scatter(
                x=dates,
                y=p(range(len(values))),
                mode='lines',
                name='Tendência',
                line=dict(dash='dash', color=self.colors['danger'])
            ))
        
        fig.update_layout(
            title="Evolução de Preços ao Longo do Tempo",
            xaxis_title="Data",
            yaxis_title="Preço (R$)",
            hovermode='closest',
            template='plotly_white',
            height=450
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_scatter_by_source(self, prices_data: List[Dict]) -> str:
        """
        Dispersão de preços por fonte
        
        Returns:
            HTML do gráfico
        """
        import pandas as pd
        
        df = pd.DataFrame(prices_data)
        
        fig = px.scatter(
            df,
            x='source',
            y='price',
            color='region',
            size='price',
            hover_data=['supplier', 'entity'],
            title="Preços por Fonte de Dados",
            labels={'price': 'Preço (R$)', 'source': 'Fonte', 'region': 'UF'}
        )
        
        fig.update_layout(
            template='plotly_white',
            height=400
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_dashboard_summary(self, all_researches: List) -> str:
        """
        Dashboard com resumo geral do sistema
        
        Args:
            all_researches: Lista de todas as pesquisas
        
        Returns:
            HTML com múltiplos gráficos
        """
        # Gráfico de pizza: Métodos mais usados
        methods = {}
        for r in all_researches:
            method = r.recommended_method
            methods[method] = methods.get(method, 0) + 1
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Métodos Utilizados', 'Pesquisas por Mês', 
                          'Distribuição de Valores', 'Fontes Mais Usadas'),
            specs=[[{'type': 'pie'}, {'type': 'bar'}],
                   [{'type': 'histogram'}, {'type': 'bar'}]]
        )
        
        # Pizza: Métodos
        fig.add_trace(
            go.Pie(labels=list(methods.keys()), values=list(methods.values())),
            row=1, col=1
        )
        
        # Demais gráficos...
        
        fig.update_layout(
            title_text="Dashboard - Visão Geral do Sistema",
            height=800,
            showlegend=True,
            template='plotly_white'
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')

    def create_comparison_charts(self, pesquisas: List) -> Dict[str, str]:
        """Gera gráficos comparativos entre múltiplas pesquisas."""
        charts = {}
        labels = [f"#{p.id} - {p.item_code}" for p in pesquisas]

        # 1. Comparação de Valores Estimados (Barra)
        valores = [p.estimated_value for p in pesquisas]
        fig_valores = go.Figure(data=[go.Bar(
            x=labels,
            y=valores,
            text=[f"R$ {v:,.2f}" for v in valores],
            textposition='auto',
            marker_color=self.colors['primary']
        )])
        fig_valores.update_layout(title_text="Comparação de Valores Estimados", template='plotly_white', height=400)
        charts['valores'] = fig_valores.to_html(full_html=False, include_plotlyjs='cdn')

        # 2. Comparação de Tamanho da Amostra (Barra)
        amostras = [p.sample_size for p in pesquisas]
        fig_amostras = go.Figure(data=[go.Bar(
            x=labels,
            y=amostras,
            text=amostras,
            textposition='auto',
            marker_color=self.colors['info']
        )])
        fig_amostras.update_layout(title_text="Comparação de Tamanho da Amostra", template='plotly_white', height=400)
        charts['amostras'] = fig_amostras.to_html(full_html=False, include_plotlyjs='cdn')

        # 3. Radar de Métricas Estatísticas
        fig_radar = go.Figure()
        radar_categories = ['Mediana', 'Média', 'Média Saneada', 'CV (%)', 'Mínimo', 'Máximo']
        
        # Normalização dos dados para o radar
        all_stats = [p.stats for p in pesquisas]
        max_values = {
            'median': max([s.get('median', 0) for s in all_stats]),
            'mean': max([s.get('mean', 0) for s in all_stats]),
            'sane_mean': max([s.get('sane_mean', 0) for s in all_stats]),
            'coefficient_variation': max([s.get('coefficient_variation', 0) for s in all_stats]) or 1,
            'min': max([s.get('min', 0) for s in all_stats]),
            'max': max([s.get('max', 0) for s in all_stats]),
        }

        for p in pesquisas:
            stats = p.stats
            values = [
                stats.get('median', 0) / max_values['median'] if max_values['median'] else 0,
                stats.get('mean', 0) / max_values['mean'] if max_values['mean'] else 0,
                stats.get('sane_mean', 0) / max_values['sane_mean'] if max_values['sane_mean'] else 0,
                stats.get('coefficient_variation', 0) / max_values['coefficient_variation'] if max_values['coefficient_variation'] else 0,
                stats.get('min', 0) / max_values['min'] if max_values['min'] else 0,
                stats.get('max', 0) / max_values['max'] if max_values['max'] else 0,
            ]
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=radar_categories,
                fill='toself',
                name=f"Pesquisa #{p.id}"
            ))

        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            title_text="Radar Comparativo de Métricas Estatísticas (Normalizado)",
            template='plotly_white',
            height=500
        )
        charts['radar'] = fig_radar.to_html(full_html=False, include_plotlyjs='cdn')

        return charts
```

--- END OF FILE: ./app/services/chart_generator.py ---

--- START OF FILE: ./app/services/data_analyzer.py ---

```
import numpy as np
from config import MIN_SAMPLES, CV_THRESHOLD, OUTLIER_THRESHOLD

def analyze_prices(prices: list) -> dict:
    """
    Performs a statistical analysis on a list of collected prices based on TCU regulations.

    Args:
        prices (list): A list of price dictionaries from the collector.

    Returns:
        dict: A dictionary containing the full statistical analysis, including the
              recommended value and justification.
    """
    # 1. Coleta de Preços & Limpeza Inicial
    price_values = [p.get('valor_unitario') for p in prices if p.get('valor_unitario') and p.get('valor_unitario') > 0]

    analysis_result = {
        "total_samples": len(prices),
        "valid_samples": len(price_values),
        "median": None,
        "mean": None,
        "sanitized_mean": None,
        "std_dev": None,
        "cv": None,
        "min_price": None,
        "max_price": None,
        "outliers_identified": [],
        "recommended_value": None,
        "recommendation_method": None,
        "justification": None,
        "error": None
    }

    if len(price_values) < MIN_SAMPLES:
        analysis_result["error"] = f"Análise não realizada. São necessárias pelo menos {MIN_SAMPLES} amostras de preços válidas."
        analysis_result["justification"] = "Número insuficiente de dados para uma análise estatística confiável."
        print(analysis_result["error"])
        return analysis_result

    price_array = np.array(price_values)

    # 2. Cálculo de Estatísticas Básicas
    analysis_result["median"] = np.median(price_array)
    analysis_result["mean"] = np.mean(price_array)
    analysis_result["std_dev"] = np.std(price_array)
    analysis_result["min_price"] = np.min(price_array)
    analysis_result["max_price"] = np.max(price_array)
    
    # Avoid division by zero for CV
    if analysis_result["mean"] > 0:
        analysis_result["cv"] = (analysis_result["std_dev"] / analysis_result["mean"]) * 100
    else:
        analysis_result["cv"] = 0

    # Média Saneada (remove outliers by IQR)
    q1 = np.percentile(price_array, 25)
    q3 = np.percentile(price_array, 75)
    iqr = q3 - q1
    lower_bound = q1 - OUTLIER_THRESHOLD * iqr
    upper_bound = q3 + OUTLIER_THRESHOLD * iqr

    sanitized_prices = [p for p in price_array if lower_bound <= p <= upper_bound]
    outliers = [p for p in price_array if p < lower_bound or p > upper_bound]
    analysis_result["outliers_identified"] = outliers

    if len(sanitized_prices) > 0:
        analysis_result["sanitized_mean"] = np.mean(sanitized_prices)
    else:
        # In the extreme case all data is considered outlier, fall back to the simple mean
        analysis_result["sanitized_mean"] = analysis_result["mean"]
        sanitized_prices = price_array # Use original data for decision

    # 3. Decisão do Método
    if analysis_result["cv"] > (CV_THRESHOLD * 100):
        analysis_result["recommendation_method"] = "Mediana"
        analysis_result["recommended_value"] = analysis_result["median"]
        analysis_result["justification"] = f"Alta dispersão de dados (CV > {CV_THRESHOLD * 100}%). A mediana é uma medida mais robusta a outliers e distribuições assimétricas."
    else:
        analysis_result["recommendation_method"] = "Média Saneada"
        analysis_result["recommended_value"] = analysis_result["sanitized_mean"]
        analysis_result["justification"] = f"Baixa dispersão de dados (CV <= {CV_THRESHOLD * 100}%). A média saneada (após remoção de outliers) é uma representação estatística adequada e confiável do valor central."

    print(f"\n--- Statistical Analysis Complete ---")
    print(f"Recommended Method: {analysis_result['recommendation_method']}")
    print(f"Recommended Value: {analysis_result['recommended_value']:.2f}")
    print(f"Justification: {analysis_result['justification']}")

    return analysis_result
```

--- END OF FILE: ./app/services/data_analyzer.py ---

--- START OF FILE: ./app/services/document_generator.py ---

```
# -*- coding: utf-8 -*-
"""
Gerador de Documentos PDF - Preço Ágil
Conforme Art. 29 da Portaria TCU 121/2023
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from datetime import datetime
from typing import Dict, List
import os
from config import Config

class DocumentGenerator:
    """
    Gerador de documentos de pesquisa de preços
    Conforme Art. 29 da Portaria TCU 121/2023
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configura estilos personalizados"""
        
        # Título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#0066cc'),
            spaceAfter=20,
            spaceBefore=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtítulos
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=13,
            textColor=colors.HexColor('#003366'),
            spaceAfter=12,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        ))
        
        # Texto normal justificado
        self.styles.add(ParagraphStyle(
            name='Justified',
            parent=self.styles['Normal'],
            alignment=TA_JUSTIFY,
            fontSize=10,
            leading=14
        ))
        
        # Destaque
        self.styles.add(ParagraphStyle(
            name='Highlight',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#006600'),
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            spaceAfter=15,
            spaceBefore=15
        ))
    
    def generate_research_report(self, research_data: Dict, filename: str = None) -> str:
        """
        Gera relatório completo de pesquisa de preços em PDF
        
        Conforme Art. 29 da Portaria TCU 121/2023:
        I - Descrição do objeto
        II - Responsável pela pesquisa
        III - Fontes consultadas
        IV - Série de preços coletados
        V - Método estatístico aplicado
        VI - Justificativa da metodologia
        VII - Memória de cálculo
        VIII - Valor estimado
        
        Args:
            research_data: Dicionário com dados da pesquisa
            filename: Nome do arquivo (opcional)
        
        Returns:
            Caminho completo do arquivo gerado
        """
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            item_code = research_data.get('item_code', 'item').replace('/', '-')
            filename = f"pesquisa_precos_{item_code}_{timestamp}.pdf"
        
        filepath = os.path.join(Config.REPORTS_DIR, filename)
        
        # Cria diretório se não existir
        os.makedirs(Config.REPORTS_DIR, exist_ok=True)
        
        # Cria documento
        doc = SimpleDocTemplate(
            filepath, 
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        story = []
        
        # ========== CABEÇALHO ==========
        story.append(Paragraph(
            "RELATÓRIO DE PESQUISA DE PREÇOS",
            self.styles['CustomTitle']
        ))
        
        story.append(Paragraph(
            "Preço Ágil - Sistema de Pesquisa de Preços",
            self.styles['Normal']
        ))
        
        story.append(Paragraph(
            "Conforme Lei 14.133/2021 e Portaria TCU 121/2023",
            self.styles['Normal']
        ))
        
        story.append(Spacer(1, 25))
        
        # ========== I - DESCRIÇÃO DO OBJETO ==========
        story.append(Paragraph(
            "<b>I - DESCRIÇÃO DO OBJETO</b>",
            self.styles['CustomHeading']
        ))
        
        catalog_info = research_data.get('catalog_info', {})
        
        object_data = [
            ['<b>Código:</b>', str(research_data.get('item_code', 'N/A'))],
            ['<b>Tipo:</b>', research_data.get('catalog_type', 'N/A').upper()],
            ['<b>Catálogo:</b>', research_data.get('catalog_source', 'N/A')],
            ['<b>Descrição:</b>', catalog_info.get('description', 'Não disponível')]
        ]
        
        table = Table(object_data, colWidths=[4*cm, 13*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # ========== II - RESPONSÁVEL PELA PESQUISA ==========
        story.append(Paragraph(
            "<b>II - RESPONSÁVEL PELA PESQUISA</b>",
            self.styles['CustomHeading']
        ))
        
        responsible_data = [
            ['<b>Responsável:</b>', research_data.get('responsible_agent', 'Sistema Automatizado')],
            ['<b>Data da Pesquisa:</b>', research_data.get('research_date', datetime.now().strftime('%d/%m/%Y %H:%M'))],
            ['<b>Sistema:</b>', 'Preço Ágil v' + Config.APP_VERSION]
        ]
        
        table = Table(responsible_data, colWidths=[4*cm, 13*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # ========== III - FONTES CONSULTADAS ==========
        story.append(Paragraph(
            "<b>III - FONTES CONSULTADAS</b>",
            self.styles['CustomHeading']
        ))
        
        sources = research_data.get('sources_consulted', [])
        
        if sources:
            sources_data = [['<b>Fonte</b>', '<b>Registros</b>', '<b>Prioridade</b>']]
            
            for source in sources:
                sources_data.append([
                    source.get('fonte', 'N/A'),
                    str(source.get('quantidade', 0)),
                    str(source.get('prioridade', '-'))
                ])
            
            table = Table(sources_data, colWidths=[10*cm, 3*cm, 4*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (2, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            
            story.append(table)
        else:
            story.append(Paragraph("Nenhuma fonte consultada", self.styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # ========== IV - SÉRIE DE PREÇOS COLETADOS ==========
        story.append(Paragraph(
            "<b>IV - SÉRIE DE PREÇOS COLETADOS</b>",
            self.styles['CustomHeading']
        ))
        
        sample_size = research_data.get('sample_size', 0)
        story.append(Paragraph(
            f"<b>Total de preços válidos coletados:</b> {sample_size}",
            self.styles['Normal']
        ))
        story.append(Spacer(1, 10))
        
        # Tabela de preços (primeiros 30)
        prices = research_data.get('prices_collected', [])[:30]
        
        if prices:
            prices_data = [['<b>Data</b>', '<b>Fornecedor</b>', '<b>Órgão</b>', '<b>UF</b>', '<b>Valor (R$)</b>']]
            
            for price in prices:
                date_obj = price.get('date')
                if isinstance(date_obj, datetime):
                    date_str = date_obj.strftime('%d/%m/%Y')
                else:
                    date_str = str(date_obj)[:10] if date_obj else 'N/A'
                
                supplier = str(price.get('supplier', 'N/A'))[:25]
                entity = str(price.get('entity', 'N/A'))[:25]
                region = str(price.get('region', '-'))
                value = price.get('price', 0)
                
                prices_data.append([
                    date_str,
                    supplier,
                    entity,
                    region,
                    f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                ])
            
            table = Table(prices_data, colWidths=[2.2*cm, 5*cm, 5*cm, 1.5*cm, 3.3*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (3, 0), (3, -1), 'CENTER'),
                ('ALIGN', (4, 0), (4, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 7),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            
            story.append(table)
            
            if len(research_data.get('prices_collected', [])) > 30:
                story.append(Spacer(1, 10))
                story.append(Paragraph(
                    f"<i>* Exibindo 30 de {len(research_data.get('prices_collected', []))} preços coletados</i>",
                    self.styles['Normal']
                ))
        
        story.append(Spacer(1, 20))
        
        # ========== V - ANÁLISE ESTATÍSTICA ==========
        story.append(Paragraph(
            "<b>V - ANÁLISE ESTATÍSTICA</b>",
            self.styles['CustomHeading']
        ))
        
        stats = research_data.get('statistical_analysis', {})
        
        stats_data = [
            ['<b>Mediana:</b>', f"R$ {stats.get('median', 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')],
            ['<b>Média Aritmética:</b>', f"R$ {stats.get('mean', 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')],
            ['<b>Média Saneada:</b>', f"R$ {stats.get('sane_mean', 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')],
            ['<b>Desvio Padrão:</b>', f"R$ {stats.get('std_deviation', 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')],
            ['<b>Coeficiente de Variação:</b>', f"{stats.get('coefficient_variation', 0):.2%}"],
            ['<b>Valor Mínimo:</b>', f"R$ {stats.get('min', 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')],
            ['<b>Valor Máximo:</b>', f"R$ {stats.get('max', 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')],
            ['<b>Outliers Identificados:</b>', str(stats.get('outliers_count', 0))],
            ['<b>Tamanho da Amostra:</b>', str(stats.get('sample_size', 0))]
        ]
        
        table = Table(stats_data, colWidths=[7*cm, 10*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # ========== VI - MÉTODO APLICADO E JUSTIFICATIVA ==========
        story.append(Paragraph(
            "<b>VI - MÉTODO APLICADO E JUSTIFICATIVA</b>",
            self.styles['CustomHeading']
        ))
        
        story.append(Paragraph(
            f"<b>Método Recomendado:</b> {stats.get('recommended_method', 'N/A')}",
            self.styles['Normal']
        ))
        
        story.append(Spacer(1, 10))
        
        story.append(Paragraph(
            "<b>Justificativa Técnica:</b>",
            self.styles['Normal']
        ))
        
        story.append(Paragraph(
            stats.get('justification', 'Justificativa não disponível'),
            self.styles['Justified']
        ))
        
        story.append(Spacer(1, 20))
        
        # ========== VII - VALOR ESTIMADO FINAL ==========
        story.append(Paragraph(
            "<b>VII - VALOR ESTIMADO DA CONTRATAÇÃO</b>",
            self.styles['CustomHeading']
        ))
        
        estimated_value = stats.get('estimated_value', 0)
        estimated_formatted = f"R$ {estimated_value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        
        story.append(Paragraph(
            f"<b>VALOR UNITÁRIO ESTIMADO: {estimated_formatted}</b>",
            self.styles['Highlight']
        ))
        
        story.append(Spacer(1, 20))
        
        # ========== RODAPÉ ==========
        story.append(Spacer(1, 30))
        
        story.append(Paragraph(
            "___________________________________________",
            self.styles['Normal']
        ))
        
        story.append(Paragraph(
            f"Documento gerado automaticamente pelo Preço Ágil v{Config.APP_VERSION}",
            self.styles['Normal']
        ))
        
        story.append(Paragraph(
            f"Data e hora: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}",
            self.styles['Normal']
        ))
        
        story.append(Paragraph(
            "Conforme Lei 14.133/2021 e Portarias TCU 121, 122 e 123/2023",
            self.styles['Normal']
        ))
        
        # Gera PDF
        doc.build(story)
        
        print(f"✅ PDF gerado: {filepath}")
        
        return filepath
```

--- END OF FILE: ./app/services/document_generator.py ---

--- START OF FILE: ./app/services/mock_price_data.py ---

```

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
```

--- END OF FILE: ./app/services/mock_price_data.py ---

--- START OF FILE: ./app/services/price_collector_enhanced.py ---

```
# -*- coding: utf-8 -*-
"""
Coletor de Preços APRIMORADO - Preço Ágil
"""

from typing import List, Dict, Optional
from datetime import datetime
from app.api.pncp_api import PNCPClient
from app.api.comprasnet_api import ComprasNetClient
from app.api.painel_precos_api import PainelPrecosClient
from app.api.portal_transparencia_api import PortalTransparenciaClient
from app.api.catmat_api import CATMATClient
from app.api.catser_api import CATSERClient
from app.api.brasilapi_client import BrasilAPIClient


class EnhancedPriceCollector:
    """
    Coletor de preços com fallback automático
    Conforme Portaria TCU 121/2023
    """
    
    def __init__(self):
        # Catálogos locais
        self.catmat = CATMATClient()
        self.catser = CATSERClient()
        
        # APIs principais
        self.painel_precos = PainelPrecosClient()
        self.pncp = PNCPClient()
        self.comprasnet = ComprasNetClient()
        self.portal_transparencia = PortalTransparenciaClient()
        
        # APIs auxiliares
        self.brasilapi = BrasilAPIClient()
        
        # Cache simples
        self._cache = {}
        self._cache_ttl = 3600  # 1 hora
    
    def collect_prices_with_fallback(
        self,
        item_code: str,
        catalog_type: str,
        region: Optional[str] = None,
        max_days: int = 365,
        validate_suppliers: bool = False
    ) -> Dict:
        """
        Coleta preços com sistema robusto de fallback
        
        Args:
            item_code: Código CATMAT/CATSER
            catalog_type: 'material' ou 'servico'
            region: UF (opcional)
            max_days: Idade máxima dos preços
            validate_suppliers: Validar CNPJs
        
        Returns:
            Dados completos com preços validados
        """
        
        all_prices = []
        sources_used = []
        
        print(f"\n{'='*70}")
        print(f"🔍 COLETA APRIMORADA DE PREÇOS - Item: {item_code}")
        print(f"{'='*70}")
        
        # 1. PAINEL DE PREÇOS
        print(f"\n1️⃣ Consultando Painel de Preços...")
        painel_prices = self._collect_from_painel(item_code, catalog_type, region)
        if painel_prices:
            all_prices.extend(painel_prices)
            sources_used.append({
                'fonte': 'Painel de Preços - Ministério da Economia',
                'quantidade': len(painel_prices),
                'url': 'https://paineldeprecos.planejamento.gov.br',
                'prioridade': 1
            })
            print(f"   ✅ {len(painel_prices)} preços encontrados")
        else:
            print(f"   ℹ️ Nenhum preço encontrado")
        
        # 2. PNCP
        print(f"\n2️⃣ Consultando PNCP...")
        pncp_prices = self._collect_from_pncp(item_code, catalog_type, region, max_days)
        if pncp_prices:
            all_prices.extend(pncp_prices)
            sources_used.append({
                'fonte': 'PNCP - Portal Nacional de Contratações Públicas',
                'quantidade': len(pncp_prices),
                'url': 'https://pncp.gov.br',
                'prioridade': 2
            })
            print(f"   ✅ {len(pncp_prices)} preços encontrados")
        else:
            print(f"   ℹ️ Nenhum preço encontrado")
        
        # 3. COMPRASNET
        print(f"\n3️⃣ Consultando ComprasNet...")
        comprasnet_prices = self._collect_from_comprasnet(item_code, catalog_type)
        if comprasnet_prices:
            all_prices.extend(comprasnet_prices)
            sources_used.append({
                'fonte': 'ComprasNet - Sistema Integrado',
                'quantidade': len(comprasnet_prices),
                'url': 'https://compras.dados.gov.br',
                'prioridade': 3
            })
            print(f"   ✅ {len(comprasnet_prices)} preços encontrados")
        else:
            print(f"   ℹ️ Nenhum preço encontrado")
        
        # 4. PORTAL DA TRANSPARÊNCIA
        print(f"\n4️⃣ Consultando Portal da Transparência...")
        pt_prices = self._collect_from_portal_transparencia(item_code, catalog_type)
        if pt_prices:
            all_prices.extend(pt_prices)
            sources_used.append({
                'fonte': 'Portal da Transparência - CGU',
                'quantidade': len(pt_prices),
                'url': 'https://portaltransparencia.gov.br',
                'prioridade': 4
            })
            print(f"   ✅ {len(pt_prices)} preços encontrados")
        else:
            print(f"   ℹ️ Nenhum preço encontrado")
        
        # 5. MODO HÍBRIDO: Complementa com mockados se poucos dados reais
        if len(all_prices) < 10:
            print(f"\n⚠️ Apenas {len(all_prices)} preços reais encontrados")
            print(f"   📊 Complementando com dados de teste...")
            
            try:
                from app.services.mock_price_data import generate_mock_prices
                
                needed = max(20 - len(all_prices), 10)
                mock_prices = generate_mock_prices(item_code, count=needed)
                all_prices.extend(mock_prices)
                
                sources_used.append({
                    'fonte': '⚠️ Complemento (Dados de Teste)',
                    'quantidade': needed,
                    'url': 'Sistema Local',
                    'prioridade': 999,
                    'nota': f'Adicionados {needed} preços simulados'
                })
                
                print(f"   ✅ {needed} preços de teste gerados")
                
            except Exception as e:
                print(f"   ❌ Erro ao gerar mockados: {e}")
        
        # 6. Remove duplicatas
        all_prices = self._clean_prices(all_prices)
        
        # 7. Ordena por data
        all_prices.sort(key=lambda x: x.get('date', datetime.min), reverse=True)
        
        # 8. Obtém descrição
        item_description = self.catmat.get_description(item_code) if catalog_type == 'material' else self.catser.get_description(item_code)
        
        result = {
            'item_code': item_code,
            'item_description': item_description or 'Descrição não disponível',
            'catalog_type': catalog_type,
            'prices': all_prices,
            'total_prices': len(all_prices),
            'sources': sources_used,
            'filters': {
                'region': region,
                'max_days': max_days
            },
            'collection_date': datetime.now(),
            'metadata': {
                'suppliers_validated': validate_suppliers,
                'cache_hit': False
            }
        }
        
        print(f"\n{'='*70}")
        print(f"✅ COLETA CONCLUÍDA - {len(all_prices)} preços válidos")
        print(f"   📊 Fontes consultadas: {len(sources_used)}")
        print(f"{'='*70}\n")
        
        return result
    
    def _collect_from_painel(self, item_code: str, catalog_type: str, region: Optional[str]) -> List[Dict]:
        """Coleta do Painel de Preços"""
        try:
            return self.painel_precos.search_by_item(
                item_code=item_code,
                item_type=catalog_type,
                region=region
            )
        except Exception as e:
            print(f"   ⚠️ Erro: {e}")
            return []
    
    def _collect_from_pncp(self, item_code: str, catalog_type: str, region: Optional[str], max_days: int) -> List[Dict]:
        """Coleta do PNCP"""
        try:
            return self.pncp.search_contracts(
                item_code=item_code,
                catalog_type=catalog_type,
                max_days=max_days,
                region=region
            )
        except Exception as e:
            print(f"   ⚠️ Erro: {e}")
            return []
    
    def _collect_from_comprasnet(self, item_code: str, catalog_type: str) -> List[Dict]:
        """Coleta do ComprasNet"""
        try:
            if catalog_type == 'material':
                return self.comprasnet.search_material(item_code, max_pages=2)
            else:
                return self.comprasnet.search_service(item_code, max_pages=2)
        except Exception as e:
            print(f"   ⚠️ Erro: {e}")
            return []
    
    def _collect_from_portal_transparencia(self, item_code: str, catalog_type: str) -> List[Dict]:
        """Coleta do Portal da Transparência"""
        try:
            if catalog_type == 'material':
                item_info = self.catmat.search_by_code(item_code)
            else:
                item_info = self.catser.search_by_code(item_code)
            
            if not item_info:
                return []
            
            description = item_info.get('descricao', '')
            if description:
                search_terms = ' '.join(description.split()[:5])
                return self.portal_transparencia.search_contracts(item_description=search_terms)
            return []
        except Exception as e:
            print(f"   ⚠️ Erro: {e}")
            return []
    
    def _clean_prices(self, prices: List[Dict]) -> List[Dict]:
        """Remove duplicatas"""
        if not prices:
            return []
        
        unique_prices = []
        seen = set()
        
        for p in prices:
            key = (
                round(p.get('price', 0), 2),
                p.get('supplier'),
                str(p.get('date'))
            )
            
            if key not in seen:
                seen.add(key)
                unique_prices.append(p)
        
        return unique_prices
    
    def search_item(self, description: str) -> Dict:
        """Busca item nos catálogos"""
        materiais = self.catmat.search_by_description(description)
        servicos = self.catser.search_by_description(description)
        
        return {
            'materiais': materiais,
            'servicos': servicos,
            'total': len(materiais) + len(servicos)
        }
    
    def get_catalog_info(self, item_code: str, catalog_type: str) -> Dict:
        """Informações do catálogo"""
        if catalog_type == 'material':
            return {
                'code': item_code,
                'description': self.catmat.get_description(item_code) or 'N/A',
                'catalog': 'CATMAT',
                'type': catalog_type
            }
        else:
            return {
                'code': item_code,
                'description': self.catser.get_description(item_code) or 'N/A',
                'catalog': 'CATSER',
                'type': catalog_type
            }
```

--- END OF FILE: ./app/services/price_collector_enhanced.py ---

--- START OF FILE: ./app/services/statistical_analyzer.py ---

```
# -*- coding: utf-8 -*-
"""
Análise Estatística de Preços - Preço Ágil
Conforme Portaria TCU 121/2023, Art. 26
"""

import numpy as np
from typing import List, Dict, Tuple
from scipy import stats
from config import Config

class StatisticalAnalyzer:
    """
    Análise estatística de preços conforme Portaria TCU 121/2023
    
    Art. 26 - Preferência pela MEDIANA ou MÉDIA SANEADA
    Enunciado CJF 33/2023 - Critérios estatísticos robustos
    """
    
    def __init__(self):
        self.config = Config()
    
    def analyze_prices(self, prices: List[float]) -> Dict:
        """
        Analisa série de preços e retorna estatísticas completas
        
        Args:
            prices: Lista de preços a analisar
        
        Returns:
            Dicionário com estatísticas e recomendação
        """
        
        if not prices or len(prices) < Config.MIN_SAMPLES:
            return {
                "error": f"Necessário mínimo de {Config.MIN_SAMPLES} amostras. Obtido: {len(prices) if prices else 0}",
                "sample_size": len(prices) if prices else 0
            }
        
        # Remove preços zero ou negativos
        prices_array = np.array([p for p in prices if p > 0])
        
        if len(prices_array) < Config.MIN_SAMPLES:
            return {
                "error": f"Após filtrar preços inválidos, restaram apenas {len(prices_array)} amostras",
                "sample_size": len(prices_array)
            }
        
        # Estatísticas básicas
        median = np.median(prices_array)
        mean = np.mean(prices_array)
        std_dev = np.std(prices_array, ddof=1)  # ddof=1 para amostra
        min_price = np.min(prices_array)
        max_price = np.max(prices_array)
        
        # Coeficiente de variação (CV)
        cv = (std_dev / mean) if mean > 0 else 0
        
        # Média saneada (remove outliers pelo método IQR)
        sane_mean, outliers = self._calculate_sane_mean(prices_array)
        
        # Decide método baseado no CV (Art. 26)
        # CV > 0.30 indica alta dispersão → preferir MEDIANA
        if cv > Config.CV_THRESHOLD:
            recommended_method = "MEDIANA"
            estimated_value = median
            justification = (
                f"Coeficiente de Variação = {cv:.2%} > {Config.CV_THRESHOLD:.0%}. "
                f"Alta dispersão nos dados, mediana é mais robusta contra outliers. "
                f"Conforme Art. 26 da Portaria TCU 121/2023, que recomenda o uso da mediana "
                f"quando há grande variabilidade nos preços coletados."
            )
        else:
            recommended_method = "MÉDIA SANEADA"
            estimated_value = sane_mean
            justification = (
                f"Coeficiente de Variação = {cv:.2%} ≤ {Config.CV_THRESHOLD:.0%}. "
                f"Baixa dispersão nos dados, média saneada é adequada. "
                f"{len(outliers)} outliers removidos pelo método IQR (Interquartile Range). "
                f"Conforme Enunciado CJF 33/2023, que recomenda o uso de critérios estatísticos "
                f"para exclusão de valores discrepantes."
            )
        
        return {
            "sample_size": len(prices_array),
            "median": float(median),
            "mean": float(mean),
            "sane_mean": float(sane_mean),
            "min": float(min_price),
            "max": float(max_price),
            "std_deviation": float(std_dev),
            "coefficient_variation": float(cv),
            "outliers_count": len(outliers),
            "outliers_values": [float(x) for x in outliers],
            "recommended_method": recommended_method,
            "estimated_value": float(estimated_value),
            "justification": justification,
        }
    
    def _calculate_sane_mean(self, prices: np.ndarray) -> Tuple[float, np.ndarray]:
        """
        Calcula média saneada removendo outliers usando método IQR
        (Interquartile Range)
        """
        Q1 = np.percentile(prices, 25)
        Q3 = np.percentile(prices, 75)
        IQR = Q3 - Q1
        
        # Limites para identificar outliers
        lower_bound = Q1 - (Config.OUTLIER_THRESHOLD * IQR)
        upper_bound = Q3 + (Config.OUTLIER_THRESHOLD * IQR)
        
        # Identifica outliers
        outliers = prices[(prices < lower_bound) | (prices > upper_bound)]
        
        # Preços sem outliers
        clean_prices = prices[(prices >= lower_bound) & (prices <= upper_bound)]
        
        # Média dos preços limpos
        sane_mean = np.mean(clean_prices) if len(clean_prices) > 0 else np.mean(prices)
        
        return sane_mean, list(outliers)
```

--- END OF FILE: ./app/services/statistical_analyzer.py ---

--- START OF FILE: ./app/static/css/style.css ---

```
/* ============================================
   PREÇO ÁGIL - ESTILOS CUSTOMIZADOS
   ============================================ */

:root {
    --primary-color: #0d6efd;
    --secondary-color: #6c757d;
    --success-color: #198754;
    --info-color: #0dcaf0;
    --warning-color: #ffc107;
    --danger-color: #dc3545;
    --light-color: #f8f9fa;
    --dark-color: #212529;
}

/* ============================================
   GLOBAL
   ============================================ */

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

main {
    flex: 1;
}

/* ============================================
   NAVBAR
   ============================================ */

.navbar-brand {
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -0.5px;
}

.navbar-brand i {
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.1);
    }
}

/* ============================================
   HERO SECTION
   ============================================ */

.hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background: linear-gradient(to right, #e3f2fd, #bbdefb);
    border-radius: 15px;
    margin-bottom: 2rem;
}

.hero-section i {
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-10px);
    }
}

/* ============================================
   CARDS
   ============================================ */

.card {
    border-radius: 10px;
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.1) !important;
}

.card-header {
    border-radius: 10px 10px 0 0 !important;
    font-weight: 600;
}

/* ============================================
   FORMS
   ============================================ */

.form-control:focus,
.form-select:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.form-control-lg {
    padding: 0.75rem 1rem;
    font-size: 1.1rem;
}

/* ============================================
   BUTTONS
   ============================================ */

.btn {
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    font-weight: 500;
    transition: all 0.3s ease;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.btn-lg {
    padding: 0.75rem 2rem;
    font-size: 1.1rem;
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background: var(--primary-color);
    border: none;
}

.btn-primary:hover {
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    background: #0b5ed7;
}

/* ============================================
   TABLES
   ============================================ */

.table {
    border-radius: 10px;
    overflow: hidden;
}

.table thead {
    background-color: var(--light-color);
}

.table tbody tr {
    transition: all 0.3s ease;
}

.table tbody tr:hover {
    background-color: rgba(13, 110, 253, 0.05);
    transform: scale(1.01);
}

/* ============================================
   BADGES
   ============================================ */

.badge {
    padding: 0.5em 0.8em;
    font-weight: 500;
    border-radius: 6px;
}

/* ============================================
   ALERTS
   ============================================ */

.alert {
    border-radius: 10px;
    border: none;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

/* ============================================
   STATISTICS CARDS
   ============================================ */

.stat-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 15px;
    padding: 1.5rem;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.stat-value {
    font-size: 2.5rem;
    font-weight: 700;
    line-height: 1;
}

.stat-label {
    font-size: 0.9rem;
    opacity: 0.9;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ============================================
   PRICE TABLE
   ============================================ */

.price-table {
    max-height: 500px;
    overflow-y: auto;
}

.price-table::-webkit-scrollbar {
    width: 8px;
}

.price-table::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

.price-table::-webkit-scrollbar-thumb {
    background: var(--primary-color);
    border-radius: 10px;
}

.price-table::-webkit-scrollbar-thumb:hover {
    background: #0b5ed7;
}

/* ============================================
   RESULT SECTION
   ============================================ */

.result-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 15px 15px 0 0;
    margin-bottom: 0;
}

.estimated-value {
    font-size: 3rem;
    font-weight: 700;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.method-badge {
    font-size: 1rem;
    padding: 0.5rem 1rem;
    background: rgba(255,255,255,0.2);
    border-radius: 20px;
}

/* ============================================
   FOOTER
   ============================================ */

.footer {
    background-color: var(--light-color);
    border-top: 3px solid var(--primary-color);
    margin-top: auto;
}

.footer h5, .footer h6 {
    font-weight: 600;
}

.footer a {
    transition: all 0.3s ease;
}

.footer a:hover {
    color: var(--primary-color) !important;
    transform: translateX(5px);
}

/* ============================================
   LOADING SPINNER
   ============================================ */

.loading-spinner {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.7);
    z-index: 9999;
    justify-content: center;
    align-items: center;
}

.loading-spinner.active {
    display: flex;
}

.spinner-content {
    text-align: center;
    color: white;
}

.spinner-content .spinner-border {
    width: 4rem;
    height: 4rem;
    border-width: 0.4rem;
}

/* ============================================
   MODAL
   ============================================ */

.modal-content {
    border-radius: 15px;
    border: none;
    box-shadow: 0 10px 50px rgba(0,0,0,0.3);
}

.modal-header {
    border-radius: 15px 15px 0 0;
    border-bottom: none;
}

/* ============================================
   PROGRESS BAR
   ============================================ */

.progress {
    height: 25px;
    border-radius: 10px;
    background-color: #e9ecef;
}

.progress-bar {
    font-weight: 600;
    border-radius: 10px;
}

/* ============================================
   ANIMATIONS
   ============================================ */

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in {
    animation: fadeIn 0.5s ease-in-out;
}

/* ============================================
   TIMELINE
   ============================================ */

.timeline {
    position: relative;
    padding-left: 30px;
}

.timeline::before {
    content: '';
    position: absolute;
    left: 10px;
    top: 0;
    bottom: 0;
    width: 2px;
    background: var(--primary-color);
}

.timeline-item {
    position: relative;
    margin-bottom: 30px;
}

.timeline-item::before {
    content: '';
    position: absolute;
    left: -24px;
    top: 5px;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: var(--primary-color);
    border: 3px solid white;
    box-shadow: 0 0 0 3px var(--primary-color);
}

/* ============================================
   RESPONSIVE
   ============================================ */

@media (max-width: 768px) {
    .hero-section {
        padding: 2rem 1rem !important;
    }
    
    .hero-section h1 {
        font-size: 2rem;
    }
    
    .estimated-value {
        font-size: 2rem;
    }
    
    .stat-value {
        font-size: 1.8rem;
    }
    
    .table {
        font-size: 0.9rem;
    }
}

/* ============================================
   UTILITY CLASSES
   ============================================ */

.text-shadow {
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.box-shadow {
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.border-radius-lg {
    border-radius: 15px;
}

.bg-gradient-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.bg-gradient-success {
    background: linear-gradient(135deg, #0cebeb 0%, #20e3b2 100%);
}

.bg-gradient-info {
    background: linear-gradient(135deg, #667eea 0%, #0dcaf0 100%);
}

.bg-gradient-warning {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

/* ============================================
   DARK MODE (Opcional)
   ============================================ */

@media (prefers-color-scheme: dark) {
    body {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    .card {
        background-color: #2d2d2d;
        color: #ffffff;
    }
    
    .table {
        color: #ffffff;
    }
    
    .table thead {
        background-color: #3d3d3d;
    }
}
```

--- END OF FILE: ./app/static/css/style.css ---

--- START OF FILE: ./app/static/js/main.js ---

```

// static/js/main.js
// Preço Ágil - JavaScript Principal

console.log('🚀 Preço Ágil - JavaScript carregando...');

/**
 * Função para selecionar item e abrir modal
 */
function selecionarItem(codigo, tipo, descricao) {
    console.log('📦 Item selecionado:', codigo, tipo);
    
    try {
        // Preenche campos hidden
        const inputCode = document.getElementById('item_code');
        const inputType = document.getElementById('catalog_type');
        
        if (inputCode) inputCode.value = codigo;
        if (inputType) inputType.value = tipo;
        
        // Preenche campos de exibição
        const spanCode = document.getElementById('display_code');
        const spanDesc = document.getElementById('display_desc');
        
        if (spanCode) spanCode.textContent = codigo;
        if (spanDesc) spanDesc.textContent = descricao.substring(0, 200);
        
        // Abre modal
        const modalElement = document.getElementById('modalPesquisa');
        if (modalElement) {
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
            console.log('✅ Modal aberto!');
        } else {
            console.error('❌ Modal não encontrado!');
        }
    } catch (error) {
        console.error('❌ Erro ao selecionar item:', error);
    }
}

/**
 * Inicialização quando DOM carrega
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ DOM carregado');
    
    // Aguarda um pouco para garantir que tudo carregou
    setTimeout(function() {
        inicializarEventListeners();
    }, 100);
    
    // Auto-fechar alerts
    configurarAlerts();
});

/**
 * Inicializa event listeners nos botões
 */
function inicializarEventListeners() {
    const botoes = document.querySelectorAll('.btn-selecionar-item');
    
    console.log(`🔍 Encontrados ${botoes.length} botões`);
    
    if (botoes.length === 0) {
        console.warn('⚠️ Nenhum botão encontrado. Os resultados foram carregados?');
        return;
    }
    
    botoes.forEach(function(botao, index) {
        // Remove listeners antigos (se houver)
        const novoBtn = botao.cloneNode(true);
        botao.parentNode.replaceChild(novoBtn, botao);
        
        // Adiciona novo listener
        novoBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const codigo = this.getAttribute('data-codigo');
            const tipo = this.getAttribute('data-tipo');
            const descricao = this.getAttribute('data-descricao');
            
            console.log(`🖱️ Clique no botão ${index + 1}:`, codigo, tipo);
            
            if (codigo && tipo && descricao) {
                selecionarItem(codigo, tipo, descricao);
            } else {
                console.error('❌ Dados incompletos:', {codigo, tipo, descricao});
            }
        });
    });
    
    console.log('✅ Event listeners adicionados a todos os botões');
}

/**
 * Configura auto-fechar para alerts
 */
function configurarAlerts() {
    const alerts = document.querySelectorAll('.alert-dismissible');
    
    alerts.forEach(function(alert) {
        // Não fecha o alert do modal
        if (!alert.closest('#modalPesquisa')) {
            setTimeout(function() {
                try {
                    const bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                } catch(e) {
                    // Ignora erro se já foi fechado
                }
            }, 5000);
        }
    });
}

// Expõe função globalmente para debug
window.selecionarItem = selecionarItem;
window.inicializarEventListeners = inicializarEventListeners;

console.log('✅ JavaScript carregado completamente');
```

--- END OF FILE: ./app/static/js/main.js ---

--- START OF FILE: ./app/templates/404.html ---

```
{% extends "base.html" %}

{% block title %}Página não encontrada - Preço Ágil{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-lg-6 text-center py-5">
            <i class="bi bi-exclamation-triangle display-1 text-warning mb-4"></i>
            <h1 class="display-4 text-primary">404</h1>
            <h2 class="mb-4">Página não encontrada</h2>
            <p class="lead text-muted mb-4">
                A página que você está procurando não existe ou foi movida.
            </p>
            <a href="{{ url_for('main.index') }}" class="btn btn-primary btn-lg">
                <i class="bi bi-house-door me-2"></i>Voltar para Início
            </a>
        </div>
    </div>
</div>
{% endblock %}
```

--- END OF FILE: ./app/templates/404.html ---

--- START OF FILE: ./app/templates/500.html ---

```
{% extends "base.html" %}

{% block title %}Erro no Servidor - Preço Ágil{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-lg-6 text-center py-5">
            <i class="bi bi-exclamation-octagon display-1 text-danger mb-4"></i>
            <h1 class="display-4 text-primary">500</h1>
            <h2 class="mb-4">Erro no Servidor</h2>
            <p class="lead text-muted mb-4">
                Ocorreu um erro interno no servidor. Nossa equipe já foi notificada.
            </p>
            <a href="{{ url_for('main.index') }}" class="btn btn-primary btn-lg">
                <i class="bi bi-arrow-clockwise me-2"></i>Tentar Novamente
            </a>
        </div>
    </div>
</div>
{% endblock %}
```

--- END OF FILE: ./app/templates/500.html ---

--- START OF FILE: ./app/templates/base.html ---

```
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Preço Ágil - Sistema de Pesquisa de Preços para Licitações">
    <title>{% block title %}Preço Ágil{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand d-flex align-items-center" href="{{ url_for('main.index') }}">
                <i class="bi bi-speedometer2 me-2 fs-4"></i>
                <span class="fw-bold">Preço Ágil</span>
                <span class="badge bg-light text-primary ms-2">v{{ app_version }}</span>
            </a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('main.index') }}">
                            <i class="bi bi-search me-1"></i>Nova Pesquisa
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('main.historico') }}">
                            <i class="bi bi-clock-history me-1"></i>Histórico
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#" data-bs-toggle="modal" data-bs-target="#infoModal">
                            <i class="bi bi-info-circle me-1"></i>Sobre
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Flash Messages -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <div class="container mt-3">
                {% for category, message in messages %}
                    <div class="alert alert-{{ 'danger' if category == 'error' else category }} alert-dismissible fade show" role="alert">
                        <i class="bi bi-{{ 'exclamation-triangle' if category == 'error' or category == 'danger' else 'check-circle' if category == 'success' else 'info-circle' }} me-2"></i>
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    {% endwith %}

    <!-- Main Content -->
    <main class="py-4">
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="footer mt-auto py-4 bg-light">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h5 class="text-primary">
                        <i class="bi bi-speedometer2 me-2"></i>Preço Ágil
                    </h5>
                    <p class="text-muted small mb-2">{{ app_description }}</p>
                    <p class="text-muted small">
                        <i class="bi bi-shield-check me-1"></i>
                        Conforme Lei 14.133/2021 e Portarias TCU 121, 122 e 123/2023
                    </p>
                </div>
                <div class="col-md-3">
                    <h6 class="text-primary">Fontes de Dados</h6>
                    <ul class="list-unstyled small text-muted">
                        <li><i class="bi bi-check-circle-fill text-success me-1"></i>Painel de Preços (ME)</li>
                        <li><i class="bi bi-check-circle-fill text-success me-1"></i>PNCP</li>
                        <li><i class="bi bi-check-circle-fill text-success me-1"></i>ComprasNet</li>
                        <li><i class="bi bi-check-circle-fill text-success me-1"></i>Portal da Transparência</li>
                    </ul>
                </div>
                <div class="col-md-3">
                    <h6 class="text-primary">Suporte</h6>
                    <ul class="list-unstyled small">
                        <li>
                            <a href="#" class="text-decoration-none text-muted">
                                <i class="bi bi-book me-1"></i>Documentação
                            </a>
                        </li>
                        <li>
                            <a href="#" class="text-decoration-none text-muted">
                                <i class="bi bi-question-circle me-1"></i>FAQ
                            </a>
                        </li>
                        <li>
                            <a href="https://github.com" class="text-decoration-none text-muted" target="_blank">
                                <i class="bi bi-github me-1"></i>GitHub
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
            <hr>
            <div class="row">
                <div class="col text-center text-muted small">
                    © 2024 Preço Ágil | Desenvolvido para conformidade com a legislação de licitações
                </div>
            </div>
        </div>
    </footer>

    <!-- Modal Info -->
    <div class="modal fade" id="infoModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header bg-primary text-white">
                    <h5 class="modal-title">
                        <i class="bi bi-info-circle me-2"></i>Sobre o Preço Ágil
                    </h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <h6 class="text-primary">O que é?</h6>
                    <p>O <strong>Preço Ágil</strong> é um sistema completo para realizar pesquisas de preços em licitações públicas, totalmente conforme a legislação vigente.</p>
                    
                    <h6 class="text-primary mt-3">Conformidade Legal</h6>
                    <ul>
                        <li><strong>Lei 14.133/2021</strong> - Nova Lei de Licitações (Art. 23)</li>
                        <li><strong>Portaria TCU 121/2023</strong> - Pesquisa de Preços (Art. 26, 28, 29)</li>
                        <li><strong>Portaria TCU 122/2023</strong> - Catálogo Eletrônico de Padronização</li>
                        <li><strong>Portaria TCU 123/2023</strong> - Sistema Nacional de Preços de Referência</li>
                    </ul>

                    <h6 class="text-primary mt-3">Metodologia</h6>
                    <p>O sistema utiliza metodologia estatística robusta:</p>
                    <ul>
                        <li><strong>Mediana</strong> - Preferencial para alta dispersão (CV > 30%)</li>
                        <li><strong>Média Saneada</strong> - Para baixa dispersão, com remoção de outliers</li>
                        <li><strong>Validação</strong> - CNPJ dos fornecedores via Receita Federal</li>
                    </ul>

                    <h6 class="text-primary mt-3">Fontes de Dados</h6>
                    <div class="row">
                        <div class="col-md-6">
                            <div class="card border-success mb-2">
                                <div class="card-body py-2">
                                    <small class="d-block text-success fw-bold">PRIORIDADE 1</small>
                                    <small>Painel de Preços (ME)</small>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="card border-primary mb-2">
                                <div class="card-body py-2">
                                    <small class="d-block text-primary fw-bold">PRIORIDADE 2</small>
                                    <small>PNCP</small>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="card border-info mb-2">
                                <div class="card-body py-2">
                                    <small class="d-block text-info fw-bold">PRIORIDADE 3</small>
                                    <small>ComprasNet</small>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="card border-secondary mb-2">
                                <div class="card-body py-2">
                                    <small class="d-block text-secondary fw-bold">PRIORIDADE 4</small>
                                    <small>Portal da Transparência</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Custom JS -->
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

--- END OF FILE: ./app/templates/base.html ---

--- START OF FILE: ./app/templates/comparacao.html ---

```

```

--- END OF FILE: ./app/templates/comparacao.html ---

--- START OF FILE: ./app/templates/dashboard.html ---

```

```

--- END OF FILE: ./app/templates/dashboard.html ---

--- START OF FILE: ./app/templates/hello.html ---

```
{% extends "base.html" %}

{% block title %}Hello World{% endblock %}

{% block content %}
    <h1>Hello World</h1>
{% endblock %}
```

--- END OF FILE: ./app/templates/hello.html ---

--- START OF FILE: ./app/templates/historico.html ---

```
{% extends "base.html" %}

{% block title %}Histórico de Pesquisas - Preço Ágil{% endblock %}

{% block content %}
<div class="container">
    <!-- Header -->
    <div class="row mb-4">
        <div class="col">
            <div class="card shadow-lg border-0">
                <div class="card-header bg-primary text-white">
                    <div class="d-flex justify-content-between align-items-center">
                        <h4 class="mb-0">
                            <i class="bi bi-clock-history me-2"></i>Histórico de Pesquisas
                        </h4>
                        <a href="{{ url_for('main.index') }}" class="btn btn-light">
                            <i class="bi bi-plus-circle me-1"></i>Nova Pesquisa
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    {% if pesquisas %}
    <!-- Lista de Pesquisas -->
    <div class="row">
        <div class="col">
            <div class="card shadow">
                <div class="card-body p-0">
                    <div class="table-responsive">
                        <table class="table table-hover mb-0">
                            <thead class="table-light">
                                <tr>
                                    <th width="80">ID</th>
                                    <th width="120">Data</th>
                                    <th width="120">Código</th>
                                    <th>Descrição</th>
                                    <th width="100">Tipo</th>
                                    <th width="100">Amostras</th>
                                    <th width="120" class="text-end">Valor Est.</th>
                                    <th width="150" class="text-center">Ações</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for pesquisa in pesquisas %}
                                <tr>
                                    <td><strong>#{{ pesquisa.id }}</strong></td>
                                    <td>
                                        <small>{{ pesquisa.research_date.strftime('%d/%m/%Y') }}</small><br>
                                        <small class="text-muted">{{ pesquisa.research_date.strftime('%H:%M') }}</small>
                                    </td>
                                    <td>
                                        <code class="text-primary">{{ pesquisa.item_code }}</code>
                                    </td>
                                    <td>
                                        <small>{{ pesquisa.item_description[:60] }}{% if pesquisa.item_description|length > 60 %}...{% endif %}</small>
                                    </td>
                                    <td>
                                        <span class="badge {{ 'bg-primary' if pesquisa.catalog_type == 'material' else 'bg-info' }}">
                                            {{ pesquisa.catalog_type|upper }}
                                        </span>
                                    </td>
                                    <td class="text-center">
                                        <span class="badge bg-secondary">{{ pesquisa.sample_size }}</span>
                                    </td>
                                    <td class="text-end">
                                        <strong class="text-success">R$ {{ "%.2f"|format(pesquisa.estimated_value) }}</strong>
                                    </td>
                                    <td class="text-center">
                                        <div class="btn-group btn-group-sm" role="group">
                                            <a href="{{ url_for('main.ver_pesquisa', id=pesquisa.id) }}" 
                                               class="btn btn-outline-primary"
                                               title="Ver detalhes">
                                                <i class="bi bi-eye"></i>
                                            </a>
                                            {% if pesquisa.pdf_filename %}
                                            <a href="{{ url_for('main.download_pdf', filename=pesquisa.pdf_filename) }}" 
                                               class="btn btn-outline-danger"
                                               title="Download PDF">
                                                <i class="bi bi-file-earmark-pdf"></i>
                                            </a>
                                            {% endif %}
                                        </div>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <!-- Paginação -->
                {% if pagination and pagination.pages > 1 %}
                <div class="card-footer">
                    <nav aria-label="Navegação de páginas">
                        <ul class="pagination justify-content-center mb-0">
                            <li class="page-item {{ 'disabled' if not pagination.has_prev }}">
                                <a class="page-link" href="{{ url_for('main.historico', page=pagination.prev_num) if pagination.has_prev else '#' }}">
                                    <i class="bi bi-chevron-left"></i> Anterior
                                </a>
                            </li>
                            
                            {% for page_num in pagination.iter_pages(left_edge=1, right_edge=1, left_current=2, right_current=2) %}
                                {% if page_num %}
                                    <li class="page-item {{ 'active' if page_num == pagination.page }}">
                                        <a class="page-link" href="{{ url_for('main.historico', page=page_num) }}">
                                            {{ page_num }}
                                        </a>
                                    </li>
                                {% else %}
                                    <li class="page-item disabled">
                                        <span class="page-link">...</span>
                                    </li>
                                {% endif %}
                            {% endfor %}
                            
                            <li class="page-item {{ 'disabled' if not pagination.has_next }}">
                                <a class="page-link" href="{{ url_for('main.historico', page=pagination.next_num) if pagination.has_next else '#' }}">
                                    Próxima <i class="bi bi-chevron-right"></i>
                                </a>
                            </li>
                        </ul>
                    </nav>
                    
                    <div class="text-center mt-2">
                        <small class="text-muted">
                            Exibindo {{ pesquisas|length }} de {{ pagination.total }} pesquisas
                        </small>
                    </div>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
    {% else %}
    <!-- Mensagem quando não há pesquisas -->
    <div class="row">
        <div class="col text-center py-5">
            <i class="bi bi-inbox display-1 text-muted mb-3"></i>
            <h4 class="text-muted">Nenhuma pesquisa realizada ainda</h4>
            <p class="text-muted mb-4">Comece fazendo sua primeira pesquisa de preços!</p>
            <a href="{{ url_for('main.index') }}" class="btn btn-primary btn-lg">
                <i class="bi bi-plus-circle me-2"></i>Nova Pesquisa
            </a>
        </div>
    </div>
    {% endif %}
</div>
{% endblock %}
```

--- END OF FILE: ./app/templates/historico.html ---

--- START OF FILE: ./app/templates/index.html ---

```

{% extends "base.html" %}

{% block title %}Buscar Item - Preço Ágil{% endblock %}

{% block content %}
<div class="container">
    <!-- Header -->
    <div class="row mb-4">
        <div class="col text-center">
            <div class="hero-section py-5">
                <i class="bi bi-search display-1 text-primary mb-3"></i>
                <h1 class="display-4 fw-bold text-primary">Pesquisa de Preços</h1>
                <p class="lead text-muted">
                    Conforme Lei 14.133/2021 e Portarias TCU 121, 122 e 123/2023
                </p>
            </div>
        </div>
    </div>

    <!-- Busca de Item -->
    <div class="row justify-content-center mb-5">
        <div class="col-lg-8">
            <div class="card shadow-lg border-0">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">
                        <i class="bi bi-1-circle me-2"></i>Buscar Item nos Catálogos
                    </h5>
                </div>
                <div class="card-body p-4">
                    <form method="POST" action="{{ url_for('main.buscar_item') }}">
                        <div class="mb-3">
                            <label for="descricao" class="form-label fw-bold">
                                <i class="bi bi-file-text me-1"></i>Descrição do Item
                            </label>
                            <input 
                                type="text" 
                                class="form-control form-control-lg" 
                                id="descricao" 
                                name="descricao"
                                placeholder="Ex: cadeira escritório, computador, serviço limpeza..."
                                value="{{ descricao_buscada or '' }}"
                                required
                                autofocus
                            >
                            <div class="form-text">
                                <i class="bi bi-info-circle me-1"></i>
                                Digite palavras-chave para buscar nos catálogos CATMAT (materiais) e CATSER (serviços)
                            </div>
                        </div>
                        
                        <button type="submit" class="btn btn-primary btn-lg w-100">
                            <i class="bi bi-search me-2"></i>Buscar Item
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <!-- Resultados da Busca -->
    {% if resultados %}
    <div class="row justify-content-center">
        <div class="col-lg-10">
            <div class="card shadow border-0">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">
                        <i class="bi bi-2-circle me-2"></i>Resultados Encontrados
                        <span class="badge bg-light text-success ms-2">{{ resultados.total }} itens</span>
                    </h5>
                </div>
                <div class="card-body">
                    {% if resultados.materiais %}
                    <h6 class="text-primary mb-3">
                        <i class="bi bi-box-seam me-2"></i>Materiais (CATMAT)
                        <span class="badge bg-primary">{{ resultados.materiais|length }}</span>
                    </h6>
                    <div class="table-responsive mb-4">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th width="120">Código</th>
                                    <th>Descrição</th>
                                    <th width="150" class="text-center">Ação</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for item in resultados.materiais[:20] %}
                                <tr>
                                    <td><code class="text-primary">{{ item.codigo }}</code></td>
                                    <td>{{ item.descricao[:100] }}{% if item.descricao|length > 100 %}...{% endif %}</td>
                                    <td class="text-center">
                                        <button 
                                            type="button"
                                            class="btn btn-sm btn-primary btn-selecionar-item"
                                            data-codigo="{{ item.codigo }}"
                                            data-tipo="material"
                                            data-descricao="{{ item.descricao }}"
                                        >
                                            <i class="bi bi-arrow-right-circle me-1"></i>Selecionar
                                        </button>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    {% endif %}

                    {% if resultados.servicos %}
                    <h6 class="text-info mb-3">
                        <i class="bi bi-gear me-2"></i>Serviços (CATSER)
                        <span class="badge bg-info">{{ resultados.servicos|length }}</span>
                    </h6>
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th width="120">Código</th>
                                    <th>Descrição</th>
                                    <th width="150" class="text-center">Ação</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for item in resultados.servicos[:20] %}
                                <tr>
                                    <td><code class="text-info">{{ item.codigo }}</code></td>
                                    <td>{{ item.descricao[:100] }}{% if item.descricao|length > 100 %}...{% endif %}</td>
                                    <td class="text-center">
                                        <button 
                                            type="button"
                                            class="btn btn-sm btn-info btn-selecionar-item"
                                            data-codigo="{{ item.codigo }}"
                                            data-tipo="servico"
                                            data-descricao="{{ item.descricao }}"
                                        >
                                            <i class="bi bi-arrow-right-circle me-1"></i>Selecionar
                                        </button>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
    {% endif %}

    <!-- Informações -->
    <div class="row mt-5">
        <div class="col-md-4 mb-3">
            <div class="card h-100 border-primary">
                <div class="card-body text-center">
                    <i class="bi bi-shield-check display-4 text-primary mb-3"></i>
                    <h5 class="card-title">Conformidade Legal</h5>
                    <p class="card-text text-muted small">
                        100% conforme Lei 14.133/2021 e Portarias TCU
                    </p>
                </div>
            </div>
        </div>
        <div class="col-md-4 mb-3">
            <div class="card h-100 border-success">
                <div class="card-body text-center">
                    <i class="bi bi-graph-up display-4 text-success mb-3"></i>
                    <h5 class="card-title">Análise Estatística</h5>
                    <p class="card-text text-muted small">
                        Mediana, média saneada e outliers identificados
                    </p>
                </div>
            </div>
        </div>
        <div class="col-md-4 mb-3">
            <div class="card h-100 border-info">
                <div class="card-body text-center">
                    <i class="bi bi-file-earmark-pdf display-4 text-info mb-3"></i>
                    <h5 class="card-title">Relatório PDF</h5>
                    <p class="card-text text-muted small">
                        Documentação completa conforme Art. 29
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Modal de Pesquisa -->
<div class="modal fade" id="modalPesquisa" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <form method="POST" action="{{ url_for('main.pesquisar_precos') }}">
                <div class="modal-header bg-primary text-white">
                    <h5 class="modal-title">
                        <i class="bi bi-currency-dollar me-2"></i>Pesquisar Preços
                    </h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <input type="hidden" id="item_code" name="item_code">
                    <input type="hidden" id="catalog_type" name="catalog_type">
                    
                    <div class="mb-3">
                        <label class="form-label fw-bold">Item Selecionado</label>
                        <div class="alert alert-info mb-0">
                            <div><strong>Código:</strong> <span id="display_code">-</span></div>
                            <div><strong>Descrição:</strong> <span id="display_desc">-</span></div>
                        </div>
                    </div>

                    <div class="mb-3">
                        <label for="region" class="form-label">
                            <i class="bi bi-geo-alt me-1"></i>Região (Opcional)
                        </label>
                        <select class="form-select" id="region" name="region">
                            <option value="">Todas as regiões</option>
                            <option value="SP">São Paulo</option>
                            <option value="RJ">Rio de Janeiro</option>
                            <option value="MG">Minas Gerais</option>
                            <option value="DF">Distrito Federal</option>
                        </select>
                    </div>

                    <div class="mb-3">
                        <label for="responsible" class="form-label">
                            <i class="bi bi-person me-1"></i>Responsável
                        </label>
                        <input 
                            type="text" 
                            class="form-control" 
                            id="responsible" 
                            name="responsible"
                            value="Sistema Automatizado"
                            required
                        >
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                    <button type="submit" class="btn btn-primary">
                        <i class="bi bi-search me-1"></i>Iniciar Pesquisa
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>

{% endblock %}
```

--- END OF FILE: ./app/templates/index.html ---

--- START OF FILE: ./app/templates/resultado.html ---

```

{% extends "base.html" %}

{% block title %}Resultado da Pesquisa - Preço Ágil{% endblock %}

{% block extra_css %}
<style>
    .stat-card {
        transition: transform 0.3s;
    }
    .stat-card:hover {
        transform: translateY(-5px);
    }
</style>
{% endblock %}

{% block content %}
<div class="container">
    
    {% if error %}
    <!-- Erro -->
    <div class="row justify-content-center mt-5">
        <div class="col-lg-8">
            <div class="alert alert-warning text-center py-5">
                <i class="bi bi-exclamation-triangle display-1 mb-3"></i>
                <h3>Nenhum Preço Encontrado</h3>
                <p>Não foi possível encontrar preços para este item.</p>
                <a href="{{ url_for('main.index') }}" class="btn btn-primary mt-3">
                    <i class="bi bi-arrow-left me-2"></i>Nova Busca
                </a>
            </div>
        </div>
    </div>
    
    {% else %}
    
    <!-- Header -->
    <div class="row mt-4 mb-4">
        <div class="col">
            <div class="d-flex justify-content-between align-items-center">
                <h2 class="text-primary">
                    <i class="bi bi-check-circle-fill me-2"></i>Pesquisa Concluída
                </h2>
                <div>
                    {% if pdf_filename %}
                    <a href="{{ url_for('main.download_pdf', filename=pdf_filename) }}" 
                       class="btn btn-success btn-lg me-2">
                        <i class="bi bi-download me-2"></i>Baixar PDF
                    </a>
                    {% endif %}
                    <a href="{{ url_for('main.index') }}" class="btn btn-outline-primary">
                        <i class="bi bi-arrow-left me-2"></i>Nova Pesquisa
                    </a>
                </div>
            </div>
        </div>
    </div>

    <!-- Info do Item -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card shadow">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0"><i class="bi bi-box-seam me-2"></i>Item Pesquisado</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-3">
                            <strong>Código:</strong><br>
                            <code class="fs-5">{{ research.item_code }}</code>
                        </div>
                        <div class="col-md-6">
                            <strong>Descrição:</strong><br>
                            {{ research.catalog_info.description }}
                        </div>
                        <div class="col-md-3">
                            <strong>Catálogo:</strong><br>
                            <span class="badge bg-info">{{ research.catalog_source }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Estatísticas -->
    <div class="row mb-4">
        <div class="col-lg-6">
            <div class="card shadow h-100">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0"><i class="bi bi-graph-up me-2"></i>Estatísticas</h5>
                </div>
                <div class="card-body">
                    <table class="table">
                        <tr><td><strong>Mediana:</strong></td><td class="text-end"><strong>R$ {{ "%.2f"|format(stats.median) }}</strong></td></tr>
                        <tr><td>Média:</td><td class="text-end">R$ {{ "%.2f"|format(stats.mean) }}</td></tr>
                        <tr><td>Média Saneada:</td><td class="text-end">R$ {{ "%.2f"|format(stats.sane_mean) }}</td></tr>
                        <tr><td>Coef. Variação:</td><td class="text-end">{{ "%.1f"|format(stats.coefficient_variation * 100) }}%</td></tr>
                        <tr><td>Mínimo:</td><td class="text-end">R$ {{ "%.2f"|format(stats.min) }}</td></tr>
                        <tr><td>Máximo:</td><td class="text-end">R$ {{ "%.2f"|format(stats.max) }}</td></tr>
                    </table>
                </div>
            </div>
        </div>

        <div class="col-lg-6">
            <div class="card shadow h-100">
                <div class="card-header bg-warning text-dark">
                    <h5 class="mb-0"><i class="bi bi-award me-2"></i>Valor Estimado</h5>
                </div>
                <div class="card-body text-center">
                    <h1 class="display-3 text-success">R$ {{ "%.2f"|format(stats.estimated_value) }}</h1>
                    <p class="text-muted">Valor unitário</p>
                    <div class="alert alert-info mt-3">
                        <strong>Método:</strong> {{ stats.recommended_method }}
                    </div>
                    <div class="alert alert-light">
                        <small>{{ stats.justification }}</small>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Fontes -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card shadow">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0"><i class="bi bi-database me-2"></i>Fontes Consultadas</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        {% for source in research.sources_consulted %}
                        <div class="col-md-6 mb-3">
                            <div class="card">
                                <div class="card-body">
                                    <h6>
                                        {% if source.prioridade == 999 %}
                                        <span class="badge bg-warning">TESTE</span>
                                        {% endif %}
                                        {{ source.fonte }}
                                    </h6>
                                    <p class="mb-0"><strong>Preços:</strong> {{ source.quantidade }}</p>
                                    {% if source.nota %}
                                    <small class="text-warning">⚠️ {{ source.nota }}</small>
                                    {% endif %}
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- GRÁFICOS -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card shadow">
                <div class="card-header bg-dark text-white">
                    <h5 class="mb-0">
                        <i class="bi bi-bar-chart me-2"></i>Análise Visual
                    </h5>
                </div>
                <div class="card-body">
                    <!-- Tabs -->
                    <ul class="nav nav-tabs" role="tablist">
                        <li class="nav-item">
                            <a class="nav-link active" data-bs-toggle="tab" href="#histogram">
                                <i class="bi bi-bar-chart-fill me-1"></i>Histograma
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-bs-toggle="tab" href="#boxplot">
                                <i class="bi bi-box me-1"></i>Boxplot
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-bs-toggle="tab" href="#timeline">
                                <i class="bi bi-graph-up me-1"></i>Timeline
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-bs-toggle="tab" href="#scatter">
                                <i class="bi bi-scatter-chart me-1"></i>Por Fonte
                            </a>
                        </li>
                    </ul>
                    
                    <!-- Conteúdo das tabs -->
                    <div class="tab-content mt-3">
                        <div id="histogram" class="tab-pane fade show active">
                            {{ charts.histogram|safe }}
                        </div>
                        <div id="boxplot" class="tab-pane fade">
                            {{ charts.boxplot|safe }}
                        </div>
                        <div id="timeline" class="tab-pane fade">
                            {{ charts.timeline|safe }}
                        </div>
                        <div id="scatter" class="tab-pane fade">
                            {{ charts.scatter|safe }}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Preços -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card shadow">
                <div class="card-header bg-secondary text-white">
                    <h5 class="mb-0"><i class="bi bi-list-ul me-2"></i>Preços Coletados ({{ research.sample_size }})</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-sm table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th>#</th>
                                    <th>Fonte</th>
                                    <th>Fornecedor</th>
                                    <th>UF</th>
                                    <th>Data</th>
                                    <th class="text-end">Valor (R$)</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for price in research.prices_collected[:50] %}
                                <tr>
                                    <td>{{ loop.index }}</td>
                                    <td><small>{{ price.source }}</small></td>
                                    <td><small>{{ price.supplier[:25] }}</small></td>
                                    <td>{{ price.region }}</td>
                                    <td><small>{{ price.date[:10] if price.date is string else price.date.strftime('%d/%m/%Y') }}</small></td>
                                    <td class="text-end"><strong>{{ "%.2f"|format(price.price) }}</strong></td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                        {% if research.prices_collected|length > 50 %}
                        <p class="text-center text-muted">Mostrando 50 de {{ research.prices_collected|length }}. Veja todos no PDF.</p>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Ações -->
    <div class="row mb-5">
        <div class="col text-center">
            {% if pdf_filename %}
            <a href="{{ url_for('main.download_pdf', filename=pdf_filename) }}" 
               class="btn btn-success btn-lg me-2">
                <i class="bi bi-download me-2"></i>Baixar Relatório PDF
            </a>
            {% endif %}
            <a href="{{ url_for('main.historico') }}" class="btn btn-outline-secondary btn-lg me-2">
                <i class="bi bi-clock-history me-2"></i>Ver Histórico
            </a>
            <a href="{{ url_for('main.index') }}" class="btn btn-primary btn-lg">
                <i class="bi bi-search me-2"></i>Nova Pesquisa
            </a>
        </div>
    </div>

    {% endif %}
</div>
{% endblock %}
```

--- END OF FILE: ./app/templates/resultado.html ---

--- START OF FILE: ./app/templates/selecionar_comparacao.html ---

```

```

--- END OF FILE: ./app/templates/selecionar_comparacao.html ---

--- START OF FILE: ./app/templates/auth/audit.html ---

```

```

--- END OF FILE: ./app/templates/auth/audit.html ---

--- START OF FILE: ./app/templates/auth/change_password.html ---

```

```

--- END OF FILE: ./app/templates/auth/change_password.html ---

--- START OF FILE: ./app/templates/auth/create_user.html ---

```

```

--- END OF FILE: ./app/templates/auth/create_user.html ---

--- START OF FILE: ./app/templates/auth/login.html ---

```
{% extends "base.html" %}

{% block title %}Login - Preço Ágil{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center" style="margin-top: 10vh;">
        <div class="col-md-5">
            <div class="card shadow-lg border-0">
                <div class="card-body p-5">
                    <div class="text-center mb-4">
                        <i class="bi bi-speedometer2 display-3 text-primary"></i>
                        <h2 class="mt-3 text-primary">Preço Ágil</h2>
                        <p class="text-muted">Faça login para continuar</p>
                    </div>

                    <form method="POST" action="{{ url_for('auth.login') }}">
                        <div class="mb-3">
                            <label for="username" class="form-label">
                                <i class="bi bi-person me-1"></i>Usuário
                            </label>
                            <input 
                                type="text" 
                                class="form-control form-control-lg" 
                                id="username" 
                                name="username"
                                required
                                autofocus
                            >
                        </div>

                        <div class="mb-3">
                            <label for="password" class="form-label">
                                <i class="bi bi-lock me-1"></i>Senha
                            </label>
                            <input 
                                type="password" 
                                class="form-control form-control-lg" 
                                id="password" 
                                name="password"
                                required
                            >
                        </div>

                        <div class="mb-3 form-check">
                            <input 
                                type="checkbox" 
                                class="form-check-input" 
                                id="remember" 
                                name="remember"
                            >
                            <label class="form-check-label" for="remember">
                                Lembrar-me
                            </label>
                        </div>

                        <button type="submit" class="btn btn-primary btn-lg w-100">
                            <i class="bi bi-box-arrow-in-right me-2"></i>Entrar
                        </button>
                    </form>

                    <hr class="my-4">

                    <div class="text-center">
                        <p class="mb-2">Primeiro acesso?</p>
                        <a href="{{ url_for('auth.register') }}" class="btn btn-outline-secondary">
                            <i class="bi bi-person-plus me-2"></i>Criar Conta
                        </a>
                    </div>

                    <div class="text-center text-muted small mt-4">
                        <p class="mb-0">Sistema de Pesquisa de Preços</p>
                        <p class="mb-0">Conforme Lei 14.133/2021</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

--- END OF FILE: ./app/templates/auth/login.html ---

--- START OF FILE: ./app/templates/auth/profile.html ---

```
{% extends "base.html" %}

{% block title %}Meu Perfil - Preço Ágil{% endblock %}

{% block content %}
<div class="container">
    <div class="row mb-4">
        <div class="col">
            <h2 class="text-primary">
                <i class="bi bi-person-circle me-2"></i>Meu Perfil
            </h2>
        </div>
    </div>

    <div class="row">
        <div class="col-md-4 mb-4">
            <div class="card shadow">
                <div class="card-body text-center py-5">
                    <i class="bi bi-person-circle display-1 text-primary mb-3"></i>
                    <h4>{{ current_user.full_name }}</h4>
                    <p class="text-muted">@{{ current_user.username }}</p>
                    
                    <span class="badge bg-{{ 'danger' if current_user.role == 'admin' else 'info' if current_user.role == 'gestor' else 'secondary' }} mb-3">
                        {{ current_user.role|upper }}
                    </span>
                    
                    <hr>
                    
                    <div class="text-start">
                        <p class="mb-2">
                            <i class="bi bi-envelope me-2"></i>
                            <small>{{ current_user.email }}</small>
                        </p>
                        <p class="mb-2">
                            <i class="bi bi-calendar-check me-2"></i>
                            <small>Membro desde {{ current_user.created_at.strftime('%d/%m/%Y') }}</small>
                        </p>
                        <p class="mb-0">
                            <i class="bi bi-graph-up me-2"></i>
                            <small>{{ current_user.login_count }} acessos</small>
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-md-8">
            <div class="card shadow">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">
                        <i class="bi bi-gear me-2"></i>Configurações da Conta
                    </h5>
                </div>
                <div class="card-body">
                    <p class="text-muted">Funcionalidades em desenvolvimento...</p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

--- END OF FILE: ./app/templates/auth/profile.html ---

--- START OF FILE: ./app/templates/auth/register.html ---

```
{% extends "base.html" %}

{% block title %}Criar Conta - Preço Ágil{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center" style="margin-top: 5vh;">
        <div class="col-md-6">
            <div class="card shadow-lg border-0">
                <div class="card-body p-5">
                    <div class="text-center mb-4">
                        <i class="bi bi-person-plus display-3 text-primary"></i>
                        <h2 class="mt-3 text-primary">Criar Conta</h2>
                        <p class="text-muted">Primeiro usuário será Administrador</p>
                    </div>

                    <form method="POST" action="{{ url_for('auth.register') }}">
                        <div class="mb-3">
                            <label for="full_name" class="form-label">
                                <i class="bi bi-person me-1"></i>Nome Completo
                            </label>
                            <input 
                                type="text" 
                                class="form-control" 
                                id="full_name" 
                                name="full_name"
                                required
                                autofocus
                            >
                        </div>

                        <div class="mb-3">
                            <label for="username" class="form-label">
                                <i class="bi bi-person-badge me-1"></i>Nome de Usuário
                            </label>
                            <input 
                                type="text" 
                                class="form-control" 
                                id="username" 
                                name="username"
                                required
                            >
                            <div class="form-text">Apenas letras, números e underline</div>
                        </div>

                        <div class="mb-3">
                            <label for="email" class="form-label">
                                <i class="bi bi-envelope me-1"></i>Email
                            </label>
                            <input 
                                type="email" 
                                class="form-control" 
                                id="email" 
                                name="email"
                                required
                            >
                        </div>

                        <div class="mb-3">
                            <label for="password" class="form-label">
                                <i class="bi bi-lock me-1"></i>Senha
                            </label>
                            <input 
                                type="password" 
                                class="form-control" 
                                id="password" 
                                name="password"
                                required
                                minlength="6"
                            >
                            <div class="form-text">Mínimo de 6 caracteres</div>
                        </div>

                        <div class="mb-3">
                            <label for="password_confirm" class="form-label">
                                <i class="bi bi-lock-fill me-1"></i>Confirmar Senha
                            </label>
                            <input 
                                type="password" 
                                class="form-control" 
                                id="password_confirm" 
                                name="password_confirm"
                                required
                            >
                        </div>

                        <button type="submit" class="btn btn-primary btn-lg w-100">
                            <i class="bi bi-check-circle me-2"></i>Criar Conta
                        </button>
                    </form>

                    <hr class="my-4">

                    <div class="text-center">
                        <a href="{{ url_for('auth.login') }}" class="text-decoration-none">
                            <i class="bi bi-arrow-left me-1"></i>Já tenho conta
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

--- END OF FILE: ./app/templates/auth/register.html ---

--- START OF FILE: ./src/index.html ---

```
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Hello World</title>
  </head>

  <body>
    <h1>Hello World</h1>
  </body>
</html>
```

--- END OF FILE: ./src/index.html ---

--- START OF FILE: ./tests/test_app.py ---

```
import unittest
from unittest.mock import patch
from app import create_app

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        # Disable CSRF protection for testing forms
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()

    def test_index_page(self):
        """Test that the index page loads correctly and has the correct title."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Correctly check for the title in the response
        self.assertIn('Busca de Preços de Referência', response.data.decode('utf-8'))

    # Patch the price_collector to avoid real API calls
    @patch('app.services.price_collector.collect_prices')
    def test_search_with_query_and_results(self, mock_collect_prices):
        """Test that the search works with a valid query and returns results."""
        # Configure the mock to return some sample data
        mock_collect_prices.return_value = [
            {'fonte': 'TestAPI', 'valor_unitario': 10.5, 'descricao_item': 'caneta azul', 'data_compra': '2023-01-01'},
            {'fonte': 'TestAPI', 'valor_unitario': 11.0, 'descricao_item': 'caneta azul', 'data_compra': '2023-01-02'},
            {'fonte': 'TestAPI', 'valor_unitario': 10.0, 'descricao_item': 'caneta azul', 'data_compra': '2023-01-03'},
        ]

        response = self.client.get('/search?query=caneta')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')

        # Check that the main sections appear
        self.assertIn('Relatório de Pesquisa de Preços', response_text)
        self.assertIn('Análise Estatística', response_text)
        self.assertIn('Itens Coletados', response_text)

        # Check that the analysis shows a recommended value (the exact value depends on the data_analyzer logic)
        self.assertIn('Valor Recomendado', response_text)
        self.assertIn('10.50', response_text) # Median of [10.0, 10.5, 11.0] is 10.5

    @patch('app.services.price_collector.collect_prices')
    def test_search_with_no_results(self, mock_collect_prices):
        """Test the search page when no prices are found."""
        # Configure the mock to return an empty list
        mock_collect_prices.return_value = []

        response = self.client.get('/search?query=produto_inexistente')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')

        # Check that an appropriate message is shown
        self.assertIn('Nenhum preço foi encontrado', response_text)
        self.assertIn('Análise não realizada', response_text) # Check for the error message from the analyzer

    def test_search_without_query(self):
        """Test that the search page handles missing queries gracefully."""
        response = self.client.get('/search')
        self.assertEqual(response.status_code, 200)
        # Check for the specific error message for no query
        self.assertIn('Nenhum termo de pesquisa foi fornecido', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
```

--- END OF FILE: ./tests/test_app.py ---

--- START OF FILE: ./src/index.html ---

```
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Hello World</title>
  </head>

  <body>
    <h1>Hello World</h1>
  </body>
</html>
```

--- END OF FILE: ./src/index.html ---

--- START OF FILE: ./tests/test_app.py ---

```
import unittest
from unittest.mock import patch
from app import create_app

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        # Disable CSRF protection for testing forms
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()

    def test_index_page(self):
        """Test that the index page loads correctly and has the correct title."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Correctly check for the title in the response
        self.assertIn('Busca de Preços de Referência', response.data.decode('utf-8'))

    # Patch the price_collector to avoid real API calls
    @patch('app.services.price_collector.collect_prices')
    def test_search_with_query_and_results(self, mock_collect_prices):
        """Test that the search works with a valid query and returns results."""
        # Configure the mock to return some sample data
        mock_collect_prices.return_value = [
            {'fonte': 'TestAPI', 'valor_unitario': 10.5, 'descricao_item': 'caneta azul', 'data_compra': '2023-01-01'},
            {'fonte': 'TestAPI', 'valor_unitario': 11.0, 'descricao_item': 'caneta azul', 'data_compra': '2023-01-02'},
            {'fonte': 'TestAPI', 'valor_unitario': 10.0, 'descricao_item': 'caneta azul', 'data_compra': '2023-01-03'},
        ]

        response = self.client.get('/search?query=caneta')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')

        # Check that the main sections appear
        self.assertIn('Relatório de Pesquisa de Preços', response_text)
        self.assertIn('Análise Estatística', response_text)
        self.assertIn('Itens Coletados', response_text)

        # Check that the analysis shows a recommended value (the exact value depends on the data_analyzer logic)
        self.assertIn('Valor Recomendado', response_text)
        self.assertIn('10.50', response_text) # Median of [10.0, 10.5, 11.0] is 10.5

    @patch('app.services.price_collector.collect_prices')
    def test_search_with_no_results(self, mock_collect_prices):
        """Test the search page when no prices are found."""
        # Configure the mock to return an empty list
        mock_collect_prices.return_value = []

        response = self.client.get('/search?query=produto_inexistente')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')

        # Check that an appropriate message is shown
        self.assertIn('Nenhum preço foi encontrado', response_text)
        self.assertIn('Análise não realizada', response_text) # Check for the error message from the analyzer

    def test_search_without_query(self):
        """Test that the search page handles missing queries gracefully."""
        response = self.client.get('/search')
        self.assertEqual(response.status_code, 200)
        # Check for the specific error message for no query
        self.assertIn('Nenhum termo de pesquisa foi fornecido', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
```

--- END OF FILE: ./tests/test_app.py ---
