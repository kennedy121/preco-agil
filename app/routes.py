from flask import Blueprint, render_template, request, jsonify
from app.api.catmat_api import CATMATClient
from app.api.catser_api import CATSERClient

bp = Blueprint('main', __name__)

# Instancia os clientes para que os catálogos CSV sejam carregados na memória
catmat_client = CATMATClient()
catser_client = CATSERClient()

@bp.route('/')
def index():
    """Renderiza a página inicial"""
    return render_template('index.html')

@bp.route('/search')
def search():
    """Página de resultados da pesquisa (a ser implementada)"""
    # A lógica principal de busca de preços será implementada aqui no futuro
    return render_template('results.html')

@bp.route('/api/search_catalog')
def search_catalog():
    """
    Endpoint de API para buscar itens nos catálogos CATMAT e CATSER.
    Usa o parâmetro de consulta 'term'.
    Exemplo: /api/search_catalog?term=parafuso
    """
    search_term = request.args.get('term', '').strip()
    
    # Validação básica do termo de busca
    if not search_term or len(search_term) < 3:
        return jsonify({
            "error": "O termo de busca deve ter pelo menos 3 caracteres."
        }), 400

    # Define um limite de resultados por catálogo
    limit = 25

    # Realiza a busca nos dois catálogos simultaneamente
    catmat_results = catmat_client.search_by_description(search_term, limit=limit)
    catser_results = catser_client.search_by_description(search_term, limit=limit)
    
    # Combina os resultados, dando prioridade para materiais (CATMAT)
    combined_results = catmat_results + catser_results
    
    # Retorna a lista de resultados em formato JSON
    return jsonify(combined_results)
