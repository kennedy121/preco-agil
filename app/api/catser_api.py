# -*- coding: utf-8 -*-
"""
Cliente para catálogo CATSER (CSV)
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
        """
        try:
            if not os.path.exists(Config.CATSER_FILE):
                print(f"⚠️ Arquivo CATSER não encontrado: {Config.CATSER_FILE}")
                self.catalog = {}
                return
            
            # Tenta diferentes separadores e encondings
            try:
                df = pd.read_csv(Config.CATSER_FILE, encoding='utf-8')
            except:
                try:
                    df = pd.read_csv(Config.CATSER_FILE, sep=';', encoding='utf-8')
                except:
                    try:
                        df = pd.read_csv(Config.CATSER_FILE, encoding='latin1')
                    except:
                        df = pd.read_csv(Config.CATSER_FILE, sep=';', encoding='latin1')
            
            df.columns = [self._normalize(col) for col in df.columns]
            
            codigo_col = None
            descricao_col = None
            
            for col in df.columns:
                if 'codigo' in col or 'cod' in col:
                    codigo_col = col
                if 'descricao' in col or 'desc' in col or 'nome' in col:
                    descricao_col = col
            
            if not codigo_col or not descricao_col:
                print(f"⚠️ Colunas não identificadas no CATSER. Usando as duas primeiras.")
                codigo_col = df.columns[0]
                descricao_col = df.columns[1]
            
            df = df.dropna(subset=[codigo_col, descricao_col])
            
            self.catalog = dict(zip(
                df[codigo_col].astype(str).str.strip(),
                df[descricao_col].astype(str).str.strip()
            ))
            
            self.catalog_df = df
            
            print(f"✅ CATSER carregado: {len(self.catalog)} itens")
            print(f"   📄 Arquivo: {Config.CATSER_FILE}")
            print(f"   📊 Colunas: {codigo_col} | {descricao_col}")
            
        except Exception as e:
            print(f"❌ Erro ao carregar CATSER: {e}")
            self.catalog = {}

    def search_by_description(self, description: str, limit: int = 50) -> List[Dict]:
        """
        Busca códigos CATSER por descrição
        """
        if not self.catalog:
            return []
        
        palavras = [self._normalize(p) for p in description.split() if len(p) > 2]
        
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
        """
        Retorna descrição de um código CATSER
        """
        if not self.catalog:
            return None
        return self.catalog.get(str(code).strip())

    def search_by_code(self, code: str) -> Optional[Dict]:
        """
        Busca item por código exato
        """
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
        """
        Remove acentos e converte para minúsculas
        """
        return unicodedata.normalize("NFD", str(text).lower())\
            .encode("ascii", "ignore")\
            .decode("utf-8")