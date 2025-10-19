# -*- coding: utf-8 -*-
"""
Preço Ágil - Rotas da Aplicação Flask
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file, jsonify, current_app
from flask_login import login_required, current_user
from app.models import db
from app.models.models import Pesquisa, User
from app.services.price_collector_enhanced import EnhancedPriceCollector
from app.services.statistical_analyzer import StatisticalAnalyzer
from app.services.document_generator import DocumentGenerator
from app.services.chart_generator import ChartGenerator
from app.auth import audit_log, admin_required
from config import Config
from datetime import datetime, timedelta
import os
import pandas as pd
import io
from sqlalchemy import func

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
            flash(f"Encontrados {resultados['total']} itens.", 'success')
        
        return render_template('index.html', descricao_buscada=descricao, resultados=resultados)
    
    except Exception as e:
        current_app.logger.error(f'Erro na busca de item: {e}')
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
        research_data = {
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
        }

        # Gera gráficos
        charts = {
            'histogram': chart_gen.create_histogram(prices_values, stats),
            'boxplot': chart_gen.create_boxplot(prices_values, stats),
            'timeline': chart_gen.create_timeline(price_data['prices']),
            'scatter': chart_gen.create_scatter_by_source(price_data['prices'])
        }

        # Gera PDF
        pdf_filename = None
        try:
            pdf_data = {**research_data, 'statistical_analysis': stats}
            pdf_path = doc_generator.generate_research_report(pdf_data)
            pdf_filename = os.path.basename(pdf_path)
        except Exception as e:
            current_app.logger.error(f'Erro ao gerar PDF: {e}')

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
                {'item': f"{item_code} ({catalog_type})", 'valor': stats.get('estimated_value')}
            )
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Erro ao salvar: {e}')
            research_id = None

        return render_template('resultado.html', 
                             research=research_data, 
                             stats=stats, 
                             pdf_filename=pdf_filename, 
                             research_id=research_id, 
                             charts=charts)

    except Exception as e:
        current_app.logger.error(f'Erro na pesquisa: {e}')
        import traceback
        traceback.print_exc()
        flash(f'Erro ao realizar pesquisa: {e}', 'danger')
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
        current_app.logger.error(f'Erro no download: {e}')
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
        current_app.logger.error(f'Erro no histórico: {e}')
        flash('Erro ao carregar histórico.', 'danger')
        return redirect(url_for('main.index'))

@bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard com estatísticas"""
    try:
        # Estatísticas gerais
        total_pesquisas = Pesquisa.query.count()
        
        hoje = datetime.utcnow().date()
        pesquisas_hoje = Pesquisa.query.filter(
            func.date(Pesquisa.research_date) == hoje
        ).count()
        
        inicio_mes = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
        pesquisas_mes = Pesquisa.query.filter(
            Pesquisa.research_date >= inicio_mes
        ).count()
        
        usuarios_ativos = User.query.filter_by(active=True).count()
        
        stats = {
            'total_pesquisas': total_pesquisas,
            'pesquisas_hoje': pesquisas_hoje,
            'pesquisas_mes': pesquisas_mes,
            'usuarios_ativos': usuarios_ativos
        }
        
        # Pesquisas recentes
        recent_searches = Pesquisa.query.order_by(
            Pesquisa.research_date.desc()
        ).limit(10).all()
        
        # Itens mais pesquisados
        top_items_query = db.session.query(
            Pesquisa.item_code,
            Pesquisa.item_description,
            func.count(Pesquisa.id).label('count')
        ).group_by(
            Pesquisa.item_code,
            Pesquisa.item_description
        ).order_by(
            func.count(Pesquisa.id).desc()
        ).limit(5).all()
        
        top_items = [item._asdict() for item in top_items_query]
        
        # Dados para gráfico - últimos 30 dias
        inicio_periodo = datetime.utcnow() - timedelta(days=30)
        
        pesquisas_periodo = db.session.query(
            func.date(Pesquisa.research_date).label('date'),
            func.count(Pesquisa.id).label('count')
        ).filter(
            Pesquisa.research_date >= inicio_periodo
        ).group_by(
            func.date(Pesquisa.research_date)
        ).order_by(
            func.date(Pesquisa.research_date)
        ).all()

        chart_dict = {}
        for i in range(30):
            data = (datetime.utcnow() - timedelta(days=29-i)).date()
            chart_dict[data.strftime('%d/%m')] = 0
        
        for pesquisa in pesquisas_periodo:
            data_key = datetime.strptime(pesquisa.date, '%Y-%m-%d').strftime('%d/%m')
            if data_key in chart_dict:
                chart_dict[data_key] = pesquisa.count
        
        chart_labels = list(chart_dict.keys())
        chart_values = list(chart_dict.values())
        
        chart_data = {
            'labels': chart_labels,
            'values': chart_values
        }
        
        # Dados de fontes
        fonte_data = {
            'labels': ['PNCP', 'ComprasNet', 'Painel Preços', 'Portal Transparência'],
            'values': [45, 30, 15, 10]
        }
        
        return render_template(
            'dashboard.html',
            stats=stats,
            recent_searches=recent_searches,
            top_items=top_items,
            chart_data=chart_data,
            fonte_data=fonte_data
        )
        
    except Exception as e:
        current_app.logger.error(f"Erro no dashboard: {e}")
        import traceback
        traceback.print_exc()
        flash(f'Erro ao carregar dashboard: {str(e)}', 'danger')
        return redirect(url_for('main.index'))

@bp.app_template_filter('currency')
def currency_filter(value):
    """Filtro para formatar valores monetários"""
    try:
        return f"R$ {float(value):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError):
        return 'R$ 0,00'


@bp.route('/pesquisa/<int:id>')
@login_required
def ver_pesquisa(id):
    """Visualiza uma pesquisa específica do histórico"""
    pesquisa = Pesquisa.query.get_or_404(id)
    
    if not current_user.is_gestor and pesquisa.user_id != current_user.id:
        flash('Você não tem permissão para ver esta pesquisa.', 'danger')
        return redirect(url_for('main.historico'))
        
    research_data = {
        "item_code": pesquisa.item_code, "catalog_type": pesquisa.catalog_type,
        "catalog_info": {"description": pesquisa.item_description, "catalog": "CATMAT" if pesquisa.catalog_type == "material" else "CATSER"},
        "catalog_source": "CATMAT" if pesquisa.catalog_type == "material" else "CATSER",
        "responsible_agent": pesquisa.responsible_agent, "research_date": pesquisa.research_date.strftime('%d/%m/%Y %H:%M'),
        "sources_consulted": pesquisa.sources_consulted or [], "prices_collected": pesquisa.prices_collected or [],
        "sample_size": pesquisa.stats.get('sample_size', 0), "filters_applied": pesquisa.stats.get('filters_applied', {})
    }
    
    charts = {}
    if pesquisa.prices_collected and pesquisa.stats:
        prices_values = [p['price'] for p in pesquisa.prices_collected if p.get('price') and p['price'] > 0]
        if prices_values:
            charts = {
                'histogram': chart_gen.create_histogram(prices_values, pesquisa.stats),
                'boxplot': chart_gen.create_boxplot(prices_values, pesquisa.stats),
                'timeline': chart_gen.create_timeline(pesquisa.prices_collected),
                'scatter': chart_gen.create_scatter_by_source(pesquisa.prices_collected)
            }

    return render_template('resultado.html',
                         research=research_data,
                         stats=pesquisa.stats,
                         pdf_filename=pesquisa.pdf_filename,
                         research_id=pesquisa.id,
                         charts=charts,
                         is_from_history=True)


@bp.route('/comparar', methods=['GET', 'POST'])
@login_required
def comparar_pesquisas():
    if request.method == 'POST':
        pesquisa_ids = request.form.getlist('pesquisa_ids')
        if len(pesquisa_ids) < 2 or len(pesquisa_ids) > 5:
            flash('Selecione de 2 a 5 pesquisas para comparar.', 'warning')
            return redirect(url_for('main.historico'))
        
        pesquisas = Pesquisa.query.filter(Pesquisa.id.in_(pesquisa_ids)).all()
        
        if not current_user.is_gestor:
            for p in pesquisas:
                if p.user_id != current_user.id:
                    flash('Você tentou comparar uma pesquisa que não tem permissão para ver.', 'danger')
                    return redirect(url_for('main.historico'))

        charts = chart_gen.create_comparison_charts(pesquisas)
        
        return render_template('comparacao.html', pesquisas=pesquisas, charts=charts)

    query = Pesquisa.query.order_by(Pesquisa.research_date.desc())
    if not current_user.is_gestor:
        query = query.filter_by(user_id=current_user.id)
        
    pesquisas = query.limit(100).all()
    return render_template('selecionar_comparacao.html', pesquisas=pesquisas)

@bp.route('/export/<int:id>/<format>')
@login_required
def export_pesquisa(id, format):
    pesquisa = Pesquisa.query.get_or_404(id)
    if not current_user.is_gestor and pesquisa.user_id != current_user.id:
        flash('Você não tem permissão para exportar esta pesquisa.', 'danger')
        return redirect(url_for('main.historico'))

    df = pd.DataFrame(pesquisa.prices_collected)
    filename = f"pesquisa_{pesquisa.id}_{pesquisa.item_code}.{format}"

    if format == 'excel':
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Preços')
        output.seek(0)
        return send_file(output, download_name=filename, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    
    elif format == 'csv':
        csv_data = df.to_csv(index=False)
        return send_file(io.BytesIO(csv_data.encode('utf-8')), download_name=filename, as_attachment=True, mimetype='text/csv')

    elif format == 'json':
        json_data = df.to_json(orient='records', indent=4)
        return send_file(io.BytesIO(json_data.encode('utf-8')), download_name=filename, as_attachment=True, mimetype='application/json')

    else:
        flash('Formato de exportação inválido.', 'danger')
        return redirect(url_for('main.ver_pesquisa', id=id))