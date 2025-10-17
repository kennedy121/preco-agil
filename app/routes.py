# -*- coding: utf-8 -*-
"""
Preço Ágil - Rotas da Aplicação Flask
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file, jsonify, current_app
from app.models import db
from app.models.models import Pesquisa
from app.services.price_collector_enhanced import EnhancedPriceCollector
from app.services.statistical_analyzer import StatisticalAnalyzer
from app.services.document_generator import DocumentGenerator
from app.services.chart_generator import ChartGenerator # Importa o novo serviço
from config import Config
from datetime import datetime
import os

bp = Blueprint('main', __name__)

# Inicializa todos os serviços
collector = EnhancedPriceCollector()
analyzer = StatisticalAnalyzer()
doc_generator = DocumentGenerator()
chart_gen = ChartGenerator() # Instancia o gerador de gráficos

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/buscar-item', methods=['POST'])
def buscar_item():
    descricao = request.form.get('descricao', '').strip()
    if not descricao or len(descricao) < 3:
        flash('Por favor, informe uma descrição com pelo menos 3 caracteres.', 'warning')
        return redirect(url_for('main.index'))
    try:
        resultados = collector.search_item(descricao)
        if resultados['total'] == 0:
            flash('Nenhum item encontrado. Tente usar outras palavras-chave.', 'info')
        else:
            flash(f"Encontrados {resultados['total']} itens.", 'success')
        return render_template('index.html', descricao_buscada=descricao, resultados=resultados)
    except Exception as e:
        current_app.logger.error(f"Erro na busca de item: {e}")
        flash('Erro ao buscar item. Tente novamente.', 'danger')
        return redirect(url_for('main.index'))

@bp.route('/pesquisar-precos', methods=['POST'])
def pesquisar_precos():
    item_code = request.form.get('item_code', '').strip()
    catalog_type = request.form.get('catalog_type', '').strip()
    responsible = request.form.get('responsible', 'Sistema Automatizado').strip()
    region = request.form.get('region', '').strip() or None
    
    # Inicializa variáveis para garantir que existam em todos os caminhos
    charts = {}
    research_data = {"item_code": item_code, "catalog_type": catalog_type}
    stats = {}

    if not item_code or not catalog_type:
        flash('Código do item e tipo são obrigatórios.', 'danger')
        return redirect(url_for('main.index'))

    try:
        # ETAPAS 1 e 2: Coleta e Análise
        price_data = collector.collect_prices_with_fallback(item_code, catalog_type, region=region)
        if price_data['total_prices'] == 0:
            flash('Nenhum preço encontrado para este item.', 'warning')
            return render_template('resultado.html', error=True, **locals())

        prices_values = [p['price'] for p in price_data['prices'] if p.get('price') and p['price'] > 0]
        if not prices_values:
            flash('Nenhum preço válido encontrado para análise.', 'danger')
            return render_template('resultado.html', error=True, **locals())
            
        stats = analyzer.analyze_prices(prices_values)
        if 'error' in stats:
            flash(stats['error'], 'danger')
            return render_template('resultado.html', error=True, **locals())

        # ETAPA 3: Preparação dos Dados para Relatório
        catalog_info = collector.get_catalog_info(item_code, catalog_type)
        research_data = {
            "item_code": item_code, "catalog_type": catalog_type,
            "catalog_info": catalog_info, "catalog_source": "CATMAT" if catalog_type == "material" else "CATSER",
            "responsible_agent": responsible, "research_date": datetime.now().strftime('%d/%m/%Y %H:%M'),
            "sources_consulted": price_data['sources'], "prices_collected": price_data['prices'],
            "filters_applied": price_data['filters'], "sample_size": len(prices_values)
        }

        # ETAPA 4 (NOVO): Geração de Gráficos
        charts = {
            'histogram': chart_gen.create_histogram(prices_values, stats),
            'boxplot': chart_gen.create_boxplot(prices_values, stats)
        }

        # ETAPA 5: Geração de PDF
        pdf_filename = None
        try:
            pdf_path = doc_generator.generate_research_report({**research_data, "statistical_analysis": stats})
            pdf_filename = os.path.basename(pdf_path)
        except Exception as e:
            current_app.logger.error(f"Erro ao gerar PDF: {e}")
            flash('Pesquisa salva, mas houve erro ao gerar o PDF.', 'warning')

        # ETAPA 6: Salvamento no Banco
        prices_serializable = [p if not isinstance(p.get('date'), datetime) else {**p, 'date': p['date'].isoformat()} for p in price_data['prices']]
        db_research = Pesquisa(
            item_code=item_code, item_description=catalog_info.get('description', 'N/A'),
            catalog_type=catalog_type, responsible_agent=responsible, stats=stats,
            prices_collected=prices_serializable, sources_consulted=price_data['sources'],
            pdf_filename=pdf_filename
        )
        
        research_id = None
        try:
            db.session.add(db_research)
            db.session.commit()
            research_id = db_research.id
            flash('Pesquisa de preços concluída e salva com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erro ao salvar pesquisa: {e}")
            flash('Pesquisa concluída, mas com erro ao salvar no histórico.', 'danger')

        return render_template('resultado.html', research=research_data, stats=stats, pdf_filename=pdf_filename, research_id=research_id, charts=charts)

    except Exception as e:
        current_app.logger.error(f"Erro crítico na pesquisa de preços: {e}")
        flash(f'Erro crítico ao realizar pesquisa: {e}', 'danger')
        return render_template('resultado.html', error=True, research=research_data, charts=charts)

# Demais rotas (download, historico, etc.) permanecem as mesmas...

@bp.route('/download-pdf/<filename>')
def download_pdf(filename):
    try:
        reports_dir = current_app.config['REPORTS_DIR']
        filepath = os.path.join(reports_dir, filename)
        if not os.path.exists(filepath):
            flash('Arquivo PDF não encontrado.', 'danger')
            return redirect(url_for('main.index'))
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        current_app.logger.error(f"Erro no download do PDF: {e}")
        flash('Erro ao baixar o arquivo PDF.', 'danger')
        return redirect(url_for('main.index'))

@bp.route('/historico')
def historico():
    try:
        page = request.args.get('page', 1, type=int)
        pesquisas = Pesquisa.query.order_by(Pesquisa.research_date.desc()).paginate(page=page, per_page=15, error_out=False)
        return render_template('historico.html', pesquisas=pesquisas)
    except Exception as e:
        current_app.logger.error(f"Erro ao carregar histórico: {e}")
        flash('Erro ao carregar histórico.', 'danger')
        return redirect(url_for('main.index'))

@bp.route('/pesquisa/<int:id>')
def ver_pesquisa(id):
    pesquisa = Pesquisa.query.get_or_404(id)
    research_data = {
        "item_code": pesquisa.item_code, "catalog_type": pesquisa.catalog_type,
        "catalog_info": {"description": pesquisa.item_description, "catalog": "CATMAT" if pesquisa.catalog_type == "material" else "CATSER"},
        "catalog_source": "CATMAT" if pesquisa.catalog_type == "material" else "CATSER",
        "responsible_agent": pesquisa.responsible_agent, "research_date": pesquisa.research_date.strftime('%d/%m/%Y %H:%M'),
        "sources_consulted": pesquisa.sources_consulted or [], "prices_collected": pesquisa.prices_collected or [],
        "sample_size": pesquisa.stats.get('sample_size', 0), "filters_applied": pesquisa.stats.get('filters_applied', {})
    }
    
    # Gera gráficos também para pesquisas históricas
    charts = {}
    if pesquisa.prices_collected and pesquisa.stats:
        prices_values = [p['price'] for p in pesquisa.prices_collected if p.get('price') and p['price'] > 0]
        if prices_values:
            charts = {
                'histogram': chart_gen.create_histogram(prices_values, pesquisa.stats),
                'boxplot': chart_gen.create_boxplot(prices_values, pesquisa.stats)
            }

    return render_template('resultado.html',
                         research=research_data,
                         stats=pesquisa.stats,
                         pdf_filename=pesquisa.pdf_filename,
                         research_id=pesquisa.id,
                         charts=charts, # Passa os gráficos para o template
                         is_from_history=True)

@bp.route('/deletar-pesquisa/<int:id>', methods=['POST'])
def deletar_pesquisa(id):
    try:
        pesquisa = Pesquisa.query.get_or_404(id)
        if pesquisa.pdf_filename:
            pdf_path = os.path.join(current_app.config['REPORTS_DIR'], pesquisa.pdf_filename)
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        db.session.delete(pesquisa)
        db.session.commit()
        flash('Pesquisa deletada com sucesso.', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao deletar pesquisa: {e}")
        flash('Erro ao deletar a pesquisa.', 'danger')
    return redirect(url_for('main.historico'))

# API Endpoints e Filtros
@bp.route('/api/health')
def api_health():
    return jsonify(status="ok")

@bp.app_template_filter('currency')
def currency_filter(value):
    try: return f"R$ {float(value):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError): return "R$ 0,00"
