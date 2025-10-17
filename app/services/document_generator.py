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
