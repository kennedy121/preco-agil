# -*- coding: utf-8 -*-
"""
Gerador de Gráficos - Preço Ágil
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
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
        try:
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
        except Exception as e:
            print(f"❌ Erro ao criar gráfico de dispersão: {e}")
            return ""

    
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