# -*- coding: utf-8 -*-
"""
Preço Ágil - Módulo de APIs
Integrações com fontes governamentais e auxiliares
"""

from app.api.catmat_api import CATMATClient
from app.api.catser_api import CATSERClient
# from app.api.pncp_api import PNCPClient # Comentado, pois ainda não foi refatorado
# from app.api.comprasnet_api import ComprasNetClient # Comentado, pois ainda não foi refatorado
# from app.api.painel_precos_api import PainelPrecosClient # Comentado, pois ainda não foi refatorado
from app.api.portal_transparencia_api import PortalTransparenciaClient
from app.api.brasilapi_client import BrasilAPIClient
# from app.api.fallback_manager import APIFallbackManager, exponential_backoff, rate_limit

__all__ = [
    'CATMATClient',
    'CATSERClient',
    'PortalTransparenciaClient',
    'BrasilAPIClient',
    # 'PNCPClient',
    # 'ComprasNetClient',
    # 'PainelPrecosClient',
    # 'APIFallbackManager',
    # 'exponential_backoff',
    # 'rate_limit'
]
