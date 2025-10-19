# -*- coding: utf-8 -*-
"""
Cliente para catálogo CATSER (CSV) - VERSÃO ROBUSTA
Preço Ágil - Sistema de Pesquisa de Preços
"""

import pandas as pd
import unicodedata
from typing import List, Dict, Optional
from config import Config
import os
import logging

logger = logging.getLogger(__name__)


class CATSERClient:
    """Cliente para catálogo CATSER em formato CSV"""

    def __init__(self):
        self.catalog = None
        self.catalog_df = None
        self.load_catalog()

    def load_catalog(self):
        """Carrega catálogo CATSER do arquivo CSV"""
        try:
            if not os.path.exists(Config.CATSER_FILE):
                logger.warning(f"Arquivo CATSER não encontrado: {Config.CATSER_FILE}")
                self.catalog = {}
                return

            logger.info(f"Carregando CATSER: {Config.CATSER_FILE}")

            # PARSER ROBUSTO
            df = self._read_csv_robust(Config.CATSER_FILE)

            if df is None or df.empty:
                logger.warning("Arquivo CATSER vazio ou inválido")
                self.catalog = {}
                return

            # Identifica colunas
            codigo_col, descricao_col = self._identify_columns(df)

            if not codigo_col or not descricao_col:
                logger.error("Não foi possível identificar colunas no CATSER")
                self.catalog = {}
                return

            # Limpa dados
            df_clean = self._clean_dataframe(df, codigo_col, descricao_col)

            # Cria dicionário
            self.catalog = dict(zip(
                df_clean[codigo_col].astype(str),
                df_clean[descricao_col].astype(str)
            ))

            self.catalog_df = df_clean

            logger.info(f"CATSER carregado: {len(self.catalog)} itens")

            # Exemplos
            if len(self.catalog) > 0:
                logger.info("Exemplos:")
                for i, (cod, desc) in enumerate(list(self.catalog.items())[:3]):
                    logger.info(f" • {cod}: {desc[:70]}...")

        except Exception as e:
            logger.error(f"Erro ao carregar CATSER: {e}")
            import traceback
            traceback.print_exc()
            self.catalog = {}

    def _read_csv_robust(self, filepath: str) -> Optional[pd.DataFrame]:
        """
        Lê CSV com múltiplas tentativas
        """

        strategies = [
            # Estratégia 1: Pula PRIMEIRA linha (cabeçalho extra)
            {
                'sep': ';',
                'on_bad_lines': 'skip',
                'encoding': 'utf-8',
                'skiprows': 1  # Pula linha "Consulta realizada em..."
            },
            # Estratégia 2: Pula DUAS linhas
            {
                'sep': ';',
                'on_bad_lines': 'skip',
                'encoding': 'utf-8',
                'skiprows': 2
            },
            # Estratégia 3: Latin-1, pula 1
            {
                'sep': ';',
                'on_bad_lines': 'skip',
                'encoding': 'latin-1',
                'skiprows': 1
            },
            # Estratégia 4: Vírgula
            {
                'sep': ',',
                'on_bad_lines': 'skip',
                'encoding': 'utf-8',
                'skiprows': 1
            },
            # Estratégia 5: Detector automático
            {
                'sep': None,
                'engine': 'python',
                'on_bad_lines': 'skip',
                'encoding': 'utf-8',
                'skiprows': 0
            }
        ]

        for i, strategy in enumerate(strategies):
            try:
                logger.debug(f"Tentativa {i+1}: {strategy}")
                df = pd.read_csv(filepath, **strategy, dtype=str, low_memory=False)

                # Remove linhas completamente vazias
                df = df.dropna(how='all')

                if not df.empty and len(df.columns) > 1:
                    logger.info(f"CSV lido com estratégia {i+1}: {len(df)} linhas, {len(df.columns)} colunas")
                    logger.debug(f"Colunas: {list(df.columns)[:5]}")
                    return df

            except Exception as e:
                logger.debug(f"Estratégia {i+1} falhou: {e}")
                continue

        logger.error("Todas as estratégias falharam")
        return None


    def _identify_columns(self, df: pd.DataFrame) -> tuple:
        """Identifica colunas de código e descrição"""
        codigo_col = None
        descricao_col = None

        for col in df.columns:
            col_lower = str(col).lower()

            if not codigo_col and any(x in col_lower for x in ['codigo', 'code', 'servico', 'catser']):
                codigo_col = col

            if not descricao_col and any(x in col_lower for x in ['descricao', 'description', 'desc', 'nome']):
                descricao_col = col

        # Fallback: posição
        if not codigo_col or not descricao_col:
            logger.warning("Usando colunas por posição (fallback)")

            if len(df.columns) >= 7:
                codigo_col = df.columns[5]  # Coluna 6
                descricao_col = df.columns[6]  # Coluna 7
            elif len(df.columns) >= 2:
                codigo_col = df.columns[0]
                descricao_col = df.columns[1]

            logger.info(f"Colunas: [{codigo_col}] → [{descricao_col}]")

        return codigo_col, descricao_col


    def _clean_dataframe(self, df: pd.DataFrame, codigo_col: str, descricao_col: str) -> pd.DataFrame:
        """Limpa e valida dataframe"""

        try:
            # Verifica se colunas existem
            if codigo_col not in df.columns or descricao_col not in df.columns:
                logger.error(f"Colunas não encontradas: {codigo_col}, {descricao_col}")
                return pd.DataFrame()

            # Seleciona apenas colunas necessárias
            df_clean = df[[codigo_col, descricao_col]].copy()

            # Remove NaN
            df_clean = df_clean.dropna()

            # CORREÇÃO: Acessa a Series corretamente
            df_clean.loc[:, codigo_col] = df_clean[codigo_col].astype(str).str.strip()
            df_clean.loc[:, descricao_col] = df_clean[descricao_col].astype(str).str.strip()

            # Remove vazios
            df_clean = df_clean[df_clean[codigo_col].astype(bool)]
            df_clean = df_clean[df_clean[descricao_col].astype(bool)]

            # Remove linhas que parecem cabeçalhos
            df_clean = df_clean[~df_clean[codigo_col].str.lower().str.contains('codigo|catmat', na=False)]

            # Remove duplicatas
            df_clean = df_clean.drop_duplicates(subset=[codigo_col])

            logger.debug(f"DataFrame limpo: {len(df_clean)} linhas válidas")

            return df_clean

        except Exception as e:
            logger.error(f"Erro ao limpar dataframe: {e}")
            return pd.DataFrame()


    def search_by_description(self, description: str, limit: int = 50) -> List[Dict]:
        """Busca códigos CATSER por descrição"""
        if not self.catalog:
            return []

        palavras = [self._normalize(p) for p in description.split() if len(p) >= 3]
        if not palavras:
            return []

        resultados = []
        for codigo, desc in self.catalog.items():
            desc_norm = self._normalize(desc)
            if all(palavra in desc_norm for palavra in palavras):
                resultados.append({"codigo": codigo, "descricao": desc, "tipo": "servico"})
                if len(resultados) >= limit:
                    break

        return resultados

    def get_description(self, code: str) -> Optional[str]:
        """Retorna descrição"""
        if not self.catalog:
            return None
        return self.catalog.get(str(code).strip())

    def search_by_code(self, code: str) -> Optional[Dict]:
        """Busca por código"""
        desc = self.get_description(code)
        if desc:
            return {"codigo": code, "descricao": desc, "tipo": "servico"}
        return None

    @staticmethod
    def _normalize(text: str) -> str:
        """Normaliza texto"""
        if not isinstance(text, str):
            text = str(text)
        text = unicodedata.normalize('NFD', text.lower())
        text = text.encode('ascii', 'ignore').decode('utf-8')
        text = ' '.join(text.split())
        return text
