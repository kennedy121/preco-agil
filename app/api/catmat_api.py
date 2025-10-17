# -*- coding: utf-8 -*-
"""
Cliente para catálogo CATMAT (CSV) - VERSÃO ESPECÍFICA
Preço Ágil - Sistema de Pesquisa de Preços
"""

import pandas as pd
import unicodedata
from typing import List, Dict, Optional
from config import Config
import os

class CATMATClient:
    """Cliente para catálogo CATMAT em formato CSV"""
    
    def __init__(self):
        self.catalog = None
        self.catalog_df = None
        self.load_catalog()
    
    def load_catalog(self):
        """
        Carrega catálogo CATMAT do arquivo CSV
        
        Formato específico:
        - Linha 1: ",,,Consulta realizada em..."
        - Linha 2: Cabeçalhos das colunas
        - Linha 3+: Dados
        - Coluna 7: Código do Item
        - Coluna 8: Descrição do Item
        """
        try:
            if not os.path.exists(Config.CATMAT_FILE):
                print(f"⚠️ Arquivo CATMAT não encontrado: {Config.CATMAT_FILE}")
                self.catalog = {}
                return
            
            # Lê CSV pulando a primeira linha, usando linha 2 como header
            df = pd.read_csv(
                Config.CATMAT_FILE,
                sep=',',
                encoding='utf-8',
                dtype=str,
                skiprows=1,  # ⭐ Pula primeira linha
                low_memory=False
            )
            
            # Remove linhas completamente vazias
            df = df.dropna(how='all')
            
            # Identifica colunas pelo nome
            codigo_col = None
            descricao_col = None
            
            for col in df.columns:
                col_lower = str(col).lower()
                
                if 'codigo' in col_lower and 'item' in col_lower:
                    codigo_col = col
                elif 'descricao' in col_lower and 'item' in col_lower:
                    descricao_col = col
            
            # Fallback: usa colunas por índice
            if not codigo_col or not descricao_col:
                if len(df.columns) >= 8:
                    codigo_col = df.columns[6]  # ⭐ Coluna 7 (índice 6)
                    descricao_col = df.columns[7]  # ⭐ Coluna 8 (índice 7)
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
            
            print(f"✅ CATMAT carregado: {len(self.catalog)} itens")
            print(f"   📄 Arquivo: {Config.CATMAT_FILE}")
            print(f"   📊 Colunas: [{codigo_col}] → [{descricao_col}]")
            
            # Exemplos
            if len(self.catalog) > 0:
                print(f"   📝 Exemplos:")
                for i, (cod, desc) in enumerate(list(self.catalog.items())[:3]):
                    print(f"      • {cod}: {desc[:70]}...")
            
        except Exception as e:
            print(f"❌ Erro ao carregar CATMAT: {e}")
            import traceback
            traceback.print_exc()
            self.catalog = {}
    
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
        
        text = unicodedata.normalize("NFD", text.lower())
        text = text.encode("ascii", "ignore").decode("utf-8")
        text = ' '.join(text.split())
        
        return text