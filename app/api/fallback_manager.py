# -*- coding: utf-8 -*-
"""Gerenciador de Fallback e Resiliência (Simulado)"""

import time
from functools import wraps

class APIFallbackManager:
    """Classe placeholder para o gerenciador de fallback."""
    def __init__(self):
        print("   -> [SIMULADO] APIFallbackManager instanciado.")

def exponential_backoff(max_retries=3, base_delay=1):
    """Decorator simulado para exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Simplesmente chama a função original sem lógica de retry
            return func(*args, **kwargs)
        return wrapper
    return decorator

def rate_limit(calls_per_minute=60):
    """Decorator simulado para rate limiting."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Simplesmente chama a função original sem lógica de rate limiting
            return func(*args, **kwargs)
        return wrapper
    return decorator
