
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
