# -*- coding: utf-8 -*-
"""
Análise Estatística de Preços - Preço Ágil
Conforme Portaria TCU 121/2023, Art. 26
"""

import numpy as np
from typing import List, Dict, Tuple
from scipy import stats
from config import Config

class StatisticalAnalyzer:
    """
    Análise estatística de preços conforme Portaria TCU 121/2023
    
    Art. 26 - Preferência pela MEDIANA ou MÉDIA SANEADA
    Enunciado CJF 33/2023 - Critérios estatísticos robustos
    """
    
    def __init__(self):
        self.config = Config()
    
    def analyze_prices(self, prices: List[float]) -> Dict:
        """
        Analisa série de preços e retorna estatísticas completas
        
        Args:
            prices: Lista de preços a analisar
        
        Returns:
            Dicionário com estatísticas e recomendação
        """
        
        if not prices or len(prices) < Config.MIN_SAMPLES:
            return {
                "error": f"Necessário mínimo de {Config.MIN_SAMPLES} amostras. Obtido: {len(prices) if prices else 0}",
                "sample_size": len(prices) if prices else 0
            }
        
        # Remove preços zero ou negativos
        prices_array = np.array([p for p in prices if p > 0])
        
        if len(prices_array) < Config.MIN_SAMPLES:
            return {
                "error": f"Após filtrar preços inválidos, restaram apenas {len(prices_array)} amostras",
                "sample_size": len(prices_array)
            }
        
        # Estatísticas básicas
        median = np.median(prices_array)
        mean = np.mean(prices_array)
        std_dev = np.std(prices_array, ddof=1)  # ddof=1 para amostra
        min_price = np.min(prices_array)
        max_price = np.max(prices_array)
        
        # Coeficiente de variação (CV)
        cv = (std_dev / mean) if mean > 0 else 0
        
        # Média saneada (remove outliers pelo método IQR)
        sane_mean, outliers = self._calculate_sane_mean(prices_array)
        
        # Decide método baseado no CV (Art. 26)
        # CV > 0.30 indica alta dispersão → preferir MEDIANA
        if cv > Config.CV_THRESHOLD:
            recommended_method = "MEDIANA"
            estimated_value = median
            justification = (
                f"Coeficiente de Variação = {cv:.2%} > {Config.CV_THRESHOLD:.0%}. "
                f"Alta dispersão nos dados, mediana é mais robusta contra outliers. "
                f"Conforme Art. 26 da Portaria TCU 121/2023, que recomenda o uso da mediana "
                f"quando há grande variabilidade nos preços coletados."
            )
        else:
            recommended_method = "MÉDIA SANEADA"
            estimated_value = sane_mean
            justification = (
                f"Coeficiente de Variação = {cv:.2%} ≤ {Config.CV_THRESHOLD:.0%}. "
                f"Baixa dispersão nos dados, média saneada é adequada. "
                f"{len(outliers)} outliers removidos pelo método IQR (Interquartile Range). "
                f"Conforme Enunciado CJF 33/2023, que recomenda o uso de critérios estatísticos "
                f"para exclusão de valores discrepantes."
            )
        
        return {
            "sample_size": len(prices_array),
            "median": float(median),
            "mean": float(mean),
            "sane_mean": float(sane_mean),
            "min": float(min_price),
            "max": float(max_price),
            "std_deviation": float(std_dev),
            "coefficient_variation": float(cv),
            "outliers_count": len(outliers),
            "outliers_values": [float(x) for x in outliers],
            "recommended_method": recommended_method,
            "estimated_value": float(estimated_value),
            "justification": justification,
        }
    
    def _calculate_sane_mean(self, prices: np.ndarray) -> Tuple[float, np.ndarray]:
        """
        Calcula média saneada removendo outliers usando método IQR
        (Interquartile Range)
        """
        Q1 = np.percentile(prices, 25)
        Q3 = np.percentile(prices, 75)
        IQR = Q3 - Q1
        
        # Limites para identificar outliers
        lower_bound = Q1 - (Config.OUTLIER_THRESHOLD * IQR)
        upper_bound = Q3 + (Config.OUTLIER_THRESHOLD * IQR)
        
        # Identifica outliers
        outliers = prices[(prices < lower_bound) | (prices > upper_bound)]
        
        # Preços sem outliers
        clean_prices = prices[(prices >= lower_bound) & (prices <= upper_bound)]
        
        # Média dos preços limpos
        sane_mean = np.mean(clean_prices) if len(clean_prices) > 0 else np.mean(prices)
        
        return sane_mean, list(outliers)
