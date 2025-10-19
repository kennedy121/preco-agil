
# app/services/statistical_analyzer.py
# -*- coding: utf-8 -*-
"""
Análise Estatística de Preços - Preço Ágil
Conforme Portaria TCU 121/2023, Art. 26

Implementa:
- ✅ Mediana (robusta a outliers)
- ✅ Média Saneada (remove outliers IQR)
- ✅ Detecção de outliers
- ✅ Coeficiente de Variação
- ✅ Validação de dados
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from scipy import stats
from config import Config
import logging

logger = logging.getLogger(__name__)


class StatisticalAnalyzerError(Exception):
    """Exceção customizada para erros de análise estatística"""
    pass


class StatisticalAnalyzer:
    """
    Análise estatística de preços conforme Portaria TCU 121/2023
    
    Art. 26 - Preferência pela MEDIANA ou MÉDIA SANEADA
    - CV > 30% → MEDIANA (mais robusta)
    - CV ≤ 30% → MÉDIA SANEADA (após remover outliers)
    """
    
    def __init__(self):
        """Inicializa analisador com configurações do sistema"""
        self.min_samples = Config.MIN_SAMPLES
        self.cv_threshold = Config.CV_THRESHOLD
        self.outlier_threshold = Config.OUTLIER_THRESHOLD
        
        logger.info(
            f"📊 StatisticalAnalyzer inicializado: "
            f"MIN_SAMPLES={{self.min_samples}}, CV_THRESHOLD={{self.cv_threshold}}"
        )
    
    def analyze_prices(self, prices: List[float]) -> Dict:
        """
        Analisa série de preços e retorna estatísticas completas
        
        Args:
            prices: Lista de preços a analisar (deve conter apenas valores > 0)
        
        Returns:
            Dicionário com estatísticas completas:
            {{
                'sample_size': int,
                'median': float,
                'mean': float,
                'sane_mean': float,
                'min': float,
                'max': float,
                'std_deviation': float,
                'coefficient_variation': float,
                'outliers_count': int,
                'outliers_values': List[float],
                'recommended_method': str,
                'estimated_value': float,
                'justification': str,
                'confidence_level': str,  # 'high', 'medium', 'low'
                'warnings': List[str]
            }}
            
            OU em caso de erro:
            {{
                'error': str,
                'sample_size': int,
                'warnings': List[str]
            }}
        
        Raises:
            StatisticalAnalyzerError: Se dados inválidos
        """
        
        # ✅ Validação e limpeza de entrada
        try:
            prices_clean = self._validate_and_clean_prices(prices)
        except StatisticalAnalyzerError as e:
            logger.warning(f"⚠️ Validação falhou: {{e}}")
            return {{
                "error": str(e),
                "sample_size": len(prices) if prices else 0,
                "warnings": []
            }}
        
        # ✅ Verifica tamanho da amostra
        if len(prices_clean) < self.min_samples:
            error_msg = (
                f"Análise não realizada. São necessárias pelo menos "
                f"{{self.min_samples}} amostras válidas. "
                f"Obtido: {{len(prices_clean)}}"
            )
            logger.warning(f"⚠️ {{error_msg}}")
            return {{
                "error": error_msg,
                "sample_size": len(prices_clean),
                "warnings": ["Amostra insuficiente para análise confiável"]
            }}
        
        # Converte para numpy array
        prices_array = np.array(prices_clean)
        
        # Lista de avisos
        warnings = []
        
        # ✅ Calcula estatísticas básicas
        try:
            median = float(np.median(prices_array))
            mean = float(np.mean(prices_array))
            std_dev = float(np.std(prices_array, ddof=1))  # Amostra, não população
            min_price = float(np.min(prices_array))
            max_price = float(np.max(prices_array))
        except Exception as e:
            logger.error(f"❌ Erro ao calcular estatísticas básicas: {{e}}")
            raise StatisticalAnalyzerError(f"Erro no cálculo estatístico: {{e}}")
        
        # ✅ Coeficiente de Variação (CV)
        if mean > 0:
            cv = std_dev / mean
        else:
            cv = 0
            warnings.append("Média zero - CV não calculável")
        
        # ✅ Calcula Média Saneada (remove outliers)
        sane_mean, outliers = self._calculate_sane_mean(prices_array)
        
        # ✅ Decide método baseado no CV (Art. 26 Portaria TCU 121/2023)
        if cv > self.cv_threshold:
            recommended_method = "MEDIANA"
            estimated_value = median
            justification = (
                f"Coeficiente de Variação = {{cv:.2%}} > {{self.cv_threshold:.0%}}. "
                f"Alta dispersão nos dados - a mediana é mais robusta a outliers. "
                f"Conforme Art. 26 da Portaria TCU 121/2023, que recomenda o uso da mediana "
                f"quando há grande variabilidade nos preços coletados."
            )
        else:
            recommended_method = "MÉDIA SANEADA"
            estimated_value = sane_mean
            justification = (
                f"Coeficiente de Variação = {{cv:.2%}} ≤ {{self.cv_threshold:.0%}}. "
                f"Baixa dispersão nos dados - média saneada é adequada. "
                f"{{len(outliers)}} outliers removidos pelo método IQR (Interquartile Range). "
                f"Conforme Enunciado CJF 33/2023, que recomenda o uso de critérios estatísticos "
                f"para exclusão de valores discrepantes."
            )
        
        # ✅ Calcula nível de confiança
        confidence_level = self._calculate_confidence_level(
            len(prices_clean), cv, len(outliers)
        )
        
        # ✅ Avisos adicionais
        if len(outliers) > len(prices_clean) * 0.25:
            warnings.append(
                f"Alto percentual de outliers ({{len(outliers) / len(prices_clean):.1%}})"
            )
        
        if max_price > median * 3:
            warnings.append(
                f"Valor máximo muito acima da mediana ({{max_price / median:.1f}}x)"
            )
        
        if len(prices_clean) < 10:
            warnings.append("Amostra pequena - resultado pode não ser representativo")
        
        # ✅ Monta resultado
        result = {{
            "sample_size": len(prices_clean),
            "median": median,
            "mean": mean,
            "sane_mean": sane_mean,
            "min": min_price,
            "max": max_price,
            "std_deviation": std_dev,
            "coefficient_variation": cv,
            "outliers_count": len(outliers),
            "outliers_values": [float(x) for x in outliers],
            "recommended_method": recommended_method,
            "estimated_value": estimated_value,
            "justification": justification,
            "confidence_level": confidence_level,
            "warnings": warnings
        }}
        
        logger.info(
            f"✅ Análise concluída: {{len(prices_clean)}} amostras, "
            f"método={{recommended_method}}, valor=R${{estimated_value:.2f}}"
        )
        
        return result
    
    def _validate_and_clean_prices(self, prices: List[float]) -> List[float]:
        """
        Valida e limpa lista de preços
        
        Args:
            prices: Lista de preços
            
        Returns:
            Lista limpa (apenas valores válidos > 0)
            
        Raises:
            StatisticalAnalyzerError: Se entrada inválida
        """
        
        if prices is None:
            raise StatisticalAnalyzerError("Lista de preços é None")
        
        if not isinstance(prices, (list, tuple, np.ndarray)):
            raise StatisticalAnalyzerError(
                f"Tipo inválido: {{type(prices)}}. Esperado: list, tuple ou ndarray"
            )
        
        if len(prices) == 0:
            raise StatisticalAnalyzerError("Lista de preços está vazia")
        
        # Remove valores inválidos
        clean = []
        invalid_count = 0
        
        for p in prices:
            try:
                # Converte para float
                value = float(p)
                
                # Valida
                if np.isnan(value) or np.isinf(value):
                    invalid_count += 1
                    continue
                
                if value <= 0:
                    invalid_count += 1
                    continue
                
                clean.append(value)
                
            except (ValueError, TypeError):
                invalid_count += 1
                continue
        
        if invalid_count > 0:
            logger.debug(f"🧹 Removidos {{invalid_count}} valores inválidos")
        
        if len(clean) == 0:
            raise StatisticalAnalyzerError(
                "Nenhum preço válido após limpeza (todos ≤ 0 ou inválidos)"
            )
        
        return clean
    
    def _calculate_sane_mean(
        self, 
        prices: np.ndarray
    ) -> Tuple[float, np.ndarray]:
        """
        Calcula média saneada removendo outliers usando método IQR
        (Interquartile Range)
        
        Args:
            prices: Array numpy com preços
            
        Returns:
            Tupla (média_saneada, lista_de_outliers)
        """
        
        if len(prices) < 4:
            # Muito pequeno para IQR - retorna média simples
            logger.debug("⚠️ Amostra muito pequena para IQR, usando média simples")
            return float(np.mean(prices)), np.array([])
        
        # Calcula quartis
        Q1 = np.percentile(prices, 25)
        Q3 = np.percentile(prices, 75)
        IQR = Q3 - Q1
        
        # Define limites para outliers
        # Usando threshold configurável (padrão 1.5)
        lower_bound = Q1 - (self.outlier_threshold * IQR)
        upper_bound = Q3 + (self.outlier_threshold * IQR)
        
        # Identifica outliers
        outlier_mask = (prices < lower_bound) | (prices > upper_bound)
        outliers = prices[outlier_mask]
        
        # Preços sem outliers
        clean_prices = prices[~outlier_mask]
        
        # Calcula média saneada
        if len(clean_prices) > 0:
            sane_mean = float(np.mean(clean_prices))
        else:
            # Se todos são outliers, usa média original
            logger.warning("⚠️ Todos os valores são outliers, usando média original")
            sane_mean = float(np.mean(prices))
            outliers = np.array([])
        
        logger.debug(
            f"📊 IQR: Q1={{Q1:.2f}}, Q3={{Q3:.2f}}, "
            f"limites=[{{lower_bound:.2f}}, {{upper_bound:.2f}}], "
            f"outliers={{len(outliers)}}"
        )
        
        return sane_mean, outliers
    
    def _calculate_confidence_level(
        self, 
        sample_size: int, 
        cv: float, 
        outliers_count: int
    ) -> str:
        """
        Calcula nível de confiança baseado em múltiplos fatores
        
        Args:
            sample_size: Tamanho da amostra
            cv: Coeficiente de variação
            outliers_count: Número de outliers
            
        Returns:
            'high', 'medium' ou 'low'
        """
        
        score = 0
        
        # Fator 1: Tamanho da amostra
        if sample_size >= 30:
            score += 3
        elif sample_size >= 15:
            score += 2
        elif sample_size >= 10:
            score += 1
        
        # Fator 2: Coeficiente de Variação
        if cv <= 0.15:  # Baixíssima variação
            score += 3
        elif cv <= 0.30:  # Baixa variação
            score += 2
        elif cv <= 0.50:  # Média variação
            score += 1
        
        # Fator 3: Outliers
        outlier_ratio = outliers_count / sample_size if sample_size > 0 else 0
        if outlier_ratio <= 0.05:  # Até 5% outliers
            score += 2
        elif outlier_ratio <= 0.15:  # Até 15% outliers
            score += 1
        
        # Classificação
        if score >= 7:
            return "high"
        elif score >= 4:
            return "medium"
        else:
            return "low"
    
    def compare_methods(self, prices: List[float]) -> Dict:
        """
        Compara todos os métodos estatísticos disponíveis
        
        Útil para análise e debugging
        
        Args:
            prices: Lista de preços
            
        Returns:
            Dicionário com resultados de todos os métodos
        """
        
        try:
            prices_clean = self._validate_and_clean_prices(prices)
            prices_array = np.array(prices_clean)
            
            median = float(np.median(prices_array))
            mean = float(np.mean(prices_array))
            sane_mean, outliers = self._calculate_sane_mean(prices_array)
            mode_result = stats.mode(prices_array, keepdims=True)
            mode = float(mode_result.mode[0]) if len(mode_result.mode) > 0 else None
            
            return {{
                "sample_size": len(prices_clean),
                "median": median,
                "mean": mean,
                "sane_mean": sane_mean,
                "mode": mode,
                "outliers_removed": len(outliers),
                "difference_median_vs_mean": abs(median - mean),
                "difference_median_vs_sane": abs(median - sane_mean),
                "recommendation": "Mediana mais confiável" if abs(median - mean) > mean * 0.1 else "Métodos similares"
            }}
            
        except Exception as e:
            logger.error(f"❌ Erro na comparação de métodos: {{e}}")
            return {{"error": str(e)}}


# ✅ Função auxiliar para uso rápido
def analyze_prices_quick(prices: List[float]) -> Optional[float]:
    """
    Função auxiliar para análise rápida
    
    Args:
        prices: Lista de preços
        
    Returns:
        Valor estimado ou None se erro
    """
    try:
        analyzer = StatisticalAnalyzer()
        result = analyzer.analyze_prices(prices)
        return result.get("estimated_value")
    except Exception:
        return None
