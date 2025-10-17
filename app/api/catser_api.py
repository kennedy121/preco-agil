# -*- coding: utf-8 -*-
"""
Cliente para catálogo CATSER (CSV) - VERSÃO ESPECÍFICA
Preço Ágil - Sistema de Pesquisa de Preços
"""

import pandas as pd
import unicodedata
from typing import List, Dict, Optional
from config import Config
import os

class CATSERClient:
    """Cliente para catálogo CATSER em formato CSV"""
    
    def __init__(self):
        self.catalog = None
        self.catalog_df = None
        self.load_catalog()
    
    def load_catalog(self):
        """
        Carrega catálogo CATSER do arquivo CSV
        
        Formato específico:
        - Linha 1: "Lista CATSER"
        - Linha 2: "Extração realizada em..."
        - Linha 3: Cabeçalhos das colunas
        - Linha 4+: Dados
        - Coluna 6: Codigo Material Serviço
        - Coluna 7: Descrição
        """
        try:
            if not os.path.exists(Config.CATSER_FILE):
                print(f"⚠️ Arquivo CATSER não encontrado: {Config.CATSER_FILE}")
                self.catalog = {}
                return
            
            # Lê CSV pulando as 3 primeiras linhas
            df = pd.read_csv(
                Config.CATSER_FILE,
                sep=',',
                encoding='utf-8',
                dtype=str,
                skiprows=2,  # ⭐ MUDOU: Pula só 2 linhas (não 3)
                header=0,    # ⭐ NOVO: Usa primeira linha após skip como header
                low_memory=False
            )
            
            # Remove linhas completamente vazias
            df = df.dropna(how='all')
            
            # Identifica colunas pelo nome
            codigo_col = None
            descricao_col = None
            
            for col in df.columns:
                col_lower = str(col).lower()
                
                if 'codigo' in col_lower and 'material' in col_lower and 'servico' in col_lower:
                    codigo_col = col
                elif not descricao_col and col_lower not in ['tipo', 'grupo', 'classe', 'sit']:
                    # Pega primeira coluna que não seja metadado
                    if df[col].notna().sum() > 0 and 'Unnamed' not in col:
                        descricao_col = col
            
            # Fallback: usa colunas por índice (mais seguro)
            if not codigo_col or not descricao_col:
                if len(df.columns) >= 7:
                    codigo_col = df.columns[5]  # ⭐ Coluna 6 (índice 5)
                    descricao_col = df.columns[6]  # ⭐ Coluna 7 (índice 6)
                    print(f"   ℹ️ Usando colunas por índice")
            
            if not codigo_col or not descricao_col:
                print(f"   ❌ Não foi possível identificar colunas")
                self.catalog = {}
                return
            
            # Limpa dados
            df_clean = df[[codigo_col, descricao_col]].copy()
            df_clean = df_clean.dropna()
            
            # Remove espaços em branco
            df_clean[codigo_col] = df_clean[codigo_col].str.strip()
            df_clean[descricao_col] = df_clean[descricao_col].str.strip()
            
            # Remove vazios
            df_clean = df_clean[df_clean[codigo_col].astype(bool)]
            df_clean = df_clean[df_clean[descricao_col].astype(bool)]
            
            # Remove linhas que parecem cabeçalhos
            df_clean = df_clean[~df_clean[codigo_col].str.lower().str.contains('codigo', na=False)]
            
            # Cria dicionário código: descrição
            self.catalog = dict(zip(
                df_clean[codigo_col].astype(str),
                df_clean[descricao_col].astype(str)
            ))
            
            self.catalog_df = df_clean
            
            print(f"✅ CATSER carregado: {len(self.catalog)} itens")
            print(f"   📄 Arquivo: {Config.CATSER_FILE}")
            print(f"   📊 Colunas: [{codigo_col}] → [{descricao_col}]")
            
            # Exemplos
            if len(self.catalog) > 0:
                print(f"   📝 Exemplos:")
                for i, (cod, desc) in enumerate(list(self.catalog.items())[:3]):
                    print(f"      • {cod}: {desc[:70]}...")
            
        except Exception as e:
            print(f"❌ Erro ao carregar CATSER: {e}")
            import traceback
            traceback.print_exc()
            self.catalog = {}
    
    def search_by_description(self, description: str, limit: int = 50) -> List[Dict]:
        """Busca códigos CATSER por descrição"""
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
                    "tipo": "servico"
                })
                
                if len(resultados) >= limit:
                    break
        
        return resultados
    
    def get_description(self, code: str) -> Optional[str]:
        """Retorna descrição de um código CATSER"""
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
                "tipo": "servico"
            }
        
        return None
    
    @staticmethod
    def _normalize(text: str) -> str:
        """Remove acentos e normaliza texto"""
        if not isinstance(text, str):
            text = str(text)
        
        text = unicodedata.normalize("NFD", text.lower())
        text = text.encode("ascii", "ignore").decode("utf-8")
        text = ' '.join(text.split())
        
        return text