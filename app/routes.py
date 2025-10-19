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
from datetime import datetime
import os
import pandas as pd
import io

bp = Blueprint('main', __name__)

# Inicializa todos os serviços
collector = EnhancedPriceCollector()
analyzer = StatisticalAnalyzer()
doc_generator = DocumentGenerator()
chart_gen = ChartGenerator()

@bp.route('/')
@login_required
def index():
    return render_template('index.html')

@bp.route('/buscar-item', methods=['POST'])
@login_required
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
@login_required
def pesquisar_precos():
    item_code = request.form.get('item_code', '').strip()
    catalog_type = request.form.get('catalog_type', '').strip()
    region = request.form.get('region', '').strip() or None
    responsible_agent = current_user.full_name # Atribui o usuário logado como responsável
    
    charts = {}
    research_data = {"item_code": item_code, "catalog_type": catalog_type}
    stats = {}

    if not item_code or not catalog_type:
        flash('Código do item e tipo são obrigatórios.', 'danger')
        return redirect(url_for('main.index'))

    try:
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

        catalog_info = collector.get_catalog_info(item_code, catalog_type)
        research_data = {
            "item_code": item_code, "catalog_type": catalog_type,
            "catalog_info": catalog_info, "catalog_source": "CATMAT" if catalog_type == "material" else "CATSER",
            "responsible_agent": responsible_agent, "research_date": datetime.now().strftime('%d/%m/%Y %H:%M'),
            "sources_consulted": price_data['sources'], "prices_collected": price_data['prices'],
            "filters_applied": price_data['filters'], "sample_size": len(prices_values)
        }

        charts = {
            'histogram': chart_gen.create_histogram(prices_values, stats),
            'boxplot': chart_gen.create_boxplot(prices_values, stats),
            'timeline': chart_gen.create_timeline(price_data['prices']),
            'scatter': chart_gen.create_scatter_by_source(price_data['prices'])
        }

        pdf_filename = None
        try:
            pdf_path = doc_generator.generate_research_report({**research_data, "statistical_analysis": stats})
            pdf_filename = os.path.basename(pdf_path)
        except Exception as e:
            current_app.logger.error(f"Erro ao gerar PDF: {e}")
            flash('Pesquisa salva, mas houve erro ao gerar o PDF.', 'warning')

        prices_serializable = [p if not isinstance(p.get('date'), datetime) else {**p, 'date': p['date'].isoformat()} for p in price_data['prices']]
        db_research = Pesquisa(
            user_id=current_user.id,
            item_code=item_code, item_description=catalog_info.get('description', 'N/A'),
            catalog_type=catalog_type, responsible_agent=responsible_agent, stats=stats,
            prices_collected=prices_serializable, sources_consulted=price_data['sources'],
            pdf_filename=pdf_filename
        )
        
        research_id = None
        try:
            db.session.add(db_research)
            db.session.commit()
            research_id = db_research.id
            flash('Pesquisa de preços concluída e salva com sucesso!', 'success')
            
            # Auditoria
            audit_log(
                'pesquisa_criada', 'pesquisa', research_id,
                {'item': f'{item_code} ({catalog_type})', 'valor': stats.get('estimated_value')}
            )
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erro ao salvar pesquisa: {e}")
            flash('Pesquisa concluída, mas com erro ao salvar no histórico.', 'danger')

        return render_template('resultado.html', research=research_data, stats=stats, pdf_filename=pdf_filename, research_id=research_id, charts=charts)

    except Exception as e:
        current_app.logger.error(f"Erro crítico na pesquisa de preços: {e}")
        flash(f'Erro crítico ao realizar pesquisa: {e}', 'danger')
        return render_template('resultado.html', error=True, research=research_data, charts=charts)

@bp.route('/download-pdf/<filename>')
@login_required
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
@login_required
def historico():
    """Histórico com filtros e controle de acesso"""
    try:
        page = request.args.get('page', 1, type=int)
        
        item_code = request.args.get('item_code', '').strip()
        responsible = request.args.get('responsible', '').strip()

        if current_user.is_gestor:
            query = Pesquisa.query
        else:
            query = Pesquisa.query.filter_by(user_id=current_user.id)

        if item_code:
            query = query.filter(Pesquisa.item_code.contains(item_code))
        if responsible:
            query = query.filter(Pesquisa.responsible_agent.contains(responsible))

        pagination = query.order_by(
            Pesquisa.research_date.desc()
        ).paginate(page=page, per_page=15, error_out=False)
        
        return render_template(
            'historico.html', 
            pesquisas=pagination.items,
            pagination=pagination,
            filters={'item_code': item_code, 'responsible': responsible}
        )
        
    except Exception as e:
        current_app.logger.error(f'Erro ao carregar histórico: {e}')
        flash('Erro ao carregar histórico.', 'danger')
        return redirect(url_for('main.index'))

@bp.route('/pesquisa/<int:id>')
@login_required
def ver_pesquisa(id):
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

@bp.route('/deletar-pesquisa/<int:id>', methods=['POST'])
@admin_required
def deletar_pesquisa(id):
    try:
        pesquisa = Pesquisa.query.get_or_404(id)
        
        audit_log(
            'pesquisa_deletada', 'pesquisa', id,
            {'item': pesquisa.item_code, 'deletado_por': current_user.username}
        )

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

@bp.route('/comparar', methods=['GET', 'POST'])
@login_required
def comparar_pesquisas():
    if request.method == 'POST':
        pesquisa_ids = request.form.getlist('pesquisa_ids')
        if len(pesquisa_ids) < 2 or len(pesquisa_ids) > 5:
            flash('Selecione de 2 a 5 pesquisas para comparar.', 'warning')
            return redirect(url_for('main.historico'))
        
        pesquisas = Pesquisa.query.filter(Pesquisa.id.in_(pesquisa_ids)).all()
        
        # Garante que o usuário tem permissão para ver todas as pesquisas selecionadas
        if not current_user.is_gestor:
            for p in pesquisas:
                if p.user_id != current_user.id:
                    flash('Você tentou comparar uma pesquisa que não tem permissão para ver.', 'danger')
                    return redirect(url_for('main.historico'))

        charts = chart_gen.create_comparison_charts(pesquisas)
        
        return render_template('comparacao.html', pesquisas=pesquisas, charts=charts)

    # Método GET
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

@bp.route('/api/health')
def api_health():
    return jsonify(status="ok")

@bp.app_template_filter('currency')
def currency_filter(value):
    try: return f"R$ {float(value):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError): return "R$ 0,00"

@bp.route('/dashboard')
@login_required
def dashboard():
    try:
        if current_user.is_gestor:
            query = Pesquisa.query
        else:
            query = Pesquisa.query.filter_by(user_id=current_user.id)

        total_pesquisas = query.count()
        if total_pesquisas == 0:
            flash('Ainda não há dados suficientes para o dashboard.', 'info')
            return redirect(url_for('main.index'))
        
        all_pesquisas = query.all()
        
        pesquisas_recentes = len([p for p in all_pesquisas if p.research_date >= datetime.now() - pd.Timedelta(days=30)])
        valores = [p.estimated_value for p in all_pesquisas if p.estimated_value]
        valor_medio = sum(valores) / len(valores) if valores else 0
        
        metodos = {}
        for p in all_pesquisas:
            metodo = p.stats.get('recommended_method', 'N/A')
            metodos[metodo] = metodos.get(metodo, 0) + 1
        
        materiais = len([p for p in all_pesquisas if p.catalog_type == 'material'])
        servicos = len([p for p in all_pesquisas if p.catalog_type == 'servico'])

        top_itens = db.session.query(
            Pesquisa.item_code, Pesquisa.item_description, db.func.count(Pesquisa.item_code).label('total')
        ).group_by(Pesquisa.item_code, Pesquisa.item_description).order_by(db.desc('total')).limit(10).all()

        pesquisas_por_mes_query = db.session.query(
            db.func.strftime('%Y-%m', Pesquisa.research_date).label('mes'),
            db.func.count().label('quantidade')
        ).group_by('mes').order_by('mes').all()

        pesquisas_por_mes = [{'mes': r.mes, 'quantidade': r.quantidade} for r in pesquisas_por_mes_query]
        
        dashboard_charts = chart_gen.create_dashboard_charts(all_pesquisas=all_pesquisas, pesquisas_por_mes=pesquisas_por_mes, metodos=metodos)
        
        stats_gerais = {
            'total_pesquisas': total_pesquisas,
            'pesquisas_recentes': pesquisas_recentes,
            'valor_medio': valor_medio, 'materiais': materiais, 'servicos': servicos, 'metodos': metodos
        }
        
        return render_template('dashboard.html', stats=stats_gerais, charts=dashboard_charts, top_itens=top_itens)
        
    except Exception as e:
        current_app.logger.error(f'Erro no dashboard: {e}')
        flash('Erro ao carregar dashboard.', 'danger')
        return redirect(url_for('main.index'))