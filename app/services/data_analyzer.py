import numpy as np
from config import MIN_SAMPLES, CV_THRESHOLD, OUTLIER_THRESHOLD

def analyze_prices(prices: list) -> dict:
    """
    Performs a statistical analysis on a list of collected prices based on TCU regulations.

    Args:
        prices (list): A list of price dictionaries from the collector.

    Returns:
        dict: A dictionary containing the full statistical analysis, including the
              recommended value and justification.
    """
    # 1. Coleta de Preços & Limpeza Inicial
    price_values = [p.get('valor_unitario') for p in prices if p.get('valor_unitario') and p.get('valor_unitario') > 0]

    analysis_result = {
        "total_samples": len(prices),
        "valid_samples": len(price_values),
        "median": None,
        "mean": None,
        "sanitized_mean": None,
        "std_dev": None,
        "cv": None,
        "min_price": None,
        "max_price": None,
        "outliers_identified": [],
        "recommended_value": None,
        "recommendation_method": None,
        "justification": None,
        "error": None
    }

    if len(price_values) < MIN_SAMPLES:
        analysis_result["error"] = f"Análise não realizada. São necessárias pelo menos {MIN_SAMPLES} amostras de preços válidas."
        analysis_result["justification"] = "Número insuficiente de dados para uma análise estatística confiável."
        print(analysis_result["error"])
        return analysis_result

    price_array = np.array(price_values)

    # 2. Cálculo de Estatísticas Básicas
    analysis_result["median"] = np.median(price_array)
    analysis_result["mean"] = np.mean(price_array)
    analysis_result["std_dev"] = np.std(price_array)
    analysis_result["min_price"] = np.min(price_array)
    analysis_result["max_price"] = np.max(price_array)
    
    # Avoid division by zero for CV
    if analysis_result["mean"] > 0:
        analysis_result["cv"] = (analysis_result["std_dev"] / analysis_result["mean"]) * 100
    else:
        analysis_result["cv"] = 0

    # Média Saneada (remove outliers by IQR)
    q1 = np.percentile(price_array, 25)
    q3 = np.percentile(price_array, 75)
    iqr = q3 - q1
    lower_bound = q1 - OUTLIER_THRESHOLD * iqr
    upper_bound = q3 + OUTLIER_THRESHOLD * iqr

    sanitized_prices = [p for p in price_array if lower_bound <= p <= upper_bound]
    outliers = [p for p in price_array if p < lower_bound or p > upper_bound]
    analysis_result["outliers_identified"] = outliers

    if len(sanitized_prices) > 0:
        analysis_result["sanitized_mean"] = np.mean(sanitized_prices)
    else:
        # In the extreme case all data is considered outlier, fall back to the simple mean
        analysis_result["sanitized_mean"] = analysis_result["mean"]
        sanitized_prices = price_array # Use original data for decision

    # 3. Decisão do Método
    if analysis_result["cv"] > (CV_THRESHOLD * 100):
        analysis_result["recommendation_method"] = "Mediana"
        analysis_result["recommended_value"] = analysis_result["median"]
        analysis_result["justification"] = f"Alta dispersão de dados (CV > {CV_THRESHOLD * 100}%). A mediana é uma medida mais robusta a outliers e distribuições assimétricas."
    else:
        analysis_result["recommendation_method"] = "Média Saneada"
        analysis_result["recommended_value"] = analysis_result["sanitized_mean"]
        analysis_result["justification"] = f"Baixa dispersão de dados (CV <= {CV_THRESHOLD * 100}%). A média saneada (após remoção de outliers) é uma representação estatística adequada e confiável do valor central."

    print(f"\n--- Statistical Analysis Complete ---")
    print(f"Recommended Method: {analysis_result['recommendation_method']}")
    print(f"Recommended Value: {analysis_result['recommended_value']:.2f}")
    print(f"Justification: {analysis_result['justification']}")

    return analysis_result
