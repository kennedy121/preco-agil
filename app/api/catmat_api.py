# -*- coding: utf-8 -*-
"""
Cliente para catálogo CATMAT (CSV)
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
        
        Formatos aceitos:
        - codigo,descricao
        - codigo;descricao
        - Com ou sem cabeçalho
        """
        try:
            if not os.path.exists(Config.CATMAT_FILE):
                print(f"⚠️ Arquivo CATMAT não encontrado: {Config.CATMAT_FILE}")
                self.catalog = {}
                return
            
            # Tenta com vírgula
            try:
                df = pd.read_csv(Config.CATMAT_FILE, encoding='utf-8')
            except:
                # Tenta com ponto-e-vírgula
                try:
                    df = pd.read_csv(Config.CATMAT_FILE, sep=';', encoding='utf-8')
                except:
                    # Tenta com latin1
                    try:
                        df = pd.read_csv(Config.CATMAT_FILE, encoding='latin1')
                    except:
                        df = pd.read_csv(Config.CATMAT_FILE, sep=';', encoding='latin1')
            
            # Normaliza nomes das colunas
            df.columns = [self._normalize(col) for col in df.columns]
            
            # Identifica colunas de código e descrição
            codigo_col = None
            descricao_col = None
            
            for col in df.columns:
                if 'codigo' in col or 'cod' in col:
                    codigo_col = col
                if 'descricao' in col or 'desc' in col or 'nome' in col:
                    descricao_col = col
            
            if not codigo_col or not descricao_col:
                print(f"⚠️ Colunas não identificadas. Usando as duas primeiras colunas")
                codigo_col = df.columns[0]
                descricao_col = df.columns[1]
            
            # Remove linhas vazias
            df = df.dropna(subset=[codigo_col, descricao_col])
            
            # Cria dicionário código: descrição
            self.catalog = dict(zip(
                df[codigo_col].astype(str).str.strip(),
                df[descricao_col].astype(str).str.strip()
            ))
            
            self.catalog_df = df
            
            print(f"✅ CATMAT carregado: {len(self.catalog)} itens")
            print(f"   📄 Arquivo: {Config.CATMAT_FILE}")
            print(f"   📊 Colunas: {codigo_col} | {descricao_col}")
            
        except Exception as e:
            print(f"❌ Erro ao carregar CATMAT: {e}")
            import traceback
            traceback.print_exc()
            self.catalog = {}
    
    def search_by_description(self, description: str, limit: int = 50) -> List[Dict]:
        """
        Busca códigos CATMAT por descrição
        
        Args:
            description: Descrição ou palavras-chave
            limit: Máximo de resultados
        
        Returns:
            Lista de dicionários com código e descrição
        """
        if not self.catalog:
            return []
        
        # Normaliza e separa palavras
        palavras = [self._normalize(p) for p in description.split() if len(p) > 2]
        
        if not palavras:
            return []
        
        resultados = []
        
        for codigo, desc in self.catalog.items():
            desc_norm = self._normalize(desc)
            
            # Verifica se TODAS as palavras estão na descrição
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
        """
        Retorna descrição de um código CATMAT
        
        Args:
            code: Código do item
        
        Returns:
            Descrição do item ou None
        """
        if not self.catalog:
            return None
        
        return self.catalog.get(str(code).strip())
    
    def search_by_code(self, code: str) -> Optional[Dict]:
        """
        Busca item por código exato
        
        Args:
            code: Código do item
        
        Returns:
            Dicionário com informações do item
        """
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
        """
        Remove acentos e converte para minúsculas
        
        Args:
            text: Texto a normalizar
        
        Returns:
            Texto normalizado
        """
        return unicodedata.normalize("NFD", str(text).lower())\
            .encode("ascii", "ignore")\
            .decode("utf-8")