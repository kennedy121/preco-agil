# -*- coding: utf-8 -*-
"""
Coletor de Preços APRIMORADO - Preço Ágil
"""

from typing import List, Dict, Optional
from datetime import datetime
import pandas as pd
from app.api.pncp_api import PNCPClient
from app.api.comprasnet_api import ComprasNetClient
from app.api.painel_precos_api import PainelPrecosClient
from app.api.portal_transparencia_api import PortalTransparenciaClient
from app.api.catmat_api import CATMATClient
from app.api.catser_api import CATSERClient
from app.api.brasilapi_client import BrasilAPIClient


class EnhancedPriceCollector:
    """
    Coletor de preços com fallback automático
    Conforme Portaria TCU 121/2023
    """
    
    def __init__(self):
        # Catálogos locais
        self.catmat = CATMATClient()
        self.catser = CATSERClient()
        
        # APIs principais
        self.painel_precos = PainelPrecosClient()
        self.pncp = PNCPClient()
        self.comprasnet = ComprasNetClient()
        self.portal_transparencia = PortalTransparenciaClient()
        
        # APIs auxiliares
        self.brasilapi = BrasilAPIClient()
        
        # Cache simples
        self._cache = {}
        self._cache_ttl = 3600  # 1 hora
    
    def _normalize_dates(self, prices: List[Dict]) -> List[Dict]:
        """
        Normaliza todas as datas para o formato YYYY-MM-DD (string)
        """
        for price in prices:
            if 'date' in price:
                try:
                    date_val = price['date']
                    
                    if isinstance(date_val, datetime):
                        price['date'] = date_val.strftime('%Y-%m-%d')
                    
                    elif isinstance(date_val, str):
                        dt = pd.to_datetime(date_val, errors='coerce')
                        if pd.notna(dt):
                            price['date'] = dt.strftime('%Y-%m-%d')
                        else:
                            price['date'] = datetime.now().strftime('%Y-%m-%d')
                    
                    else:
                        price['date'] = datetime.now().strftime('%Y-%m-%d')
                        
                except Exception as e:
                    print(f"  ⚠️ Erro ao normalizar data: {e}")
                    price['date'] = datetime.now().strftime('%Y-%m-%d')
            else:
                price['date'] = datetime.now().strftime('%Y-%m-%d')
        
        return prices

    def collect_prices_with_fallback(
        self,
        item_code: str,
        catalog_type: str,
        region: Optional[str] = None,
        max_days: int = 365,
        validate_suppliers: bool = False
    ) -> Dict:
        """
        Coleta preços com sistema robusto de fallback
        """
        print("\n" + "="*70)
        print(f"🔍 COLETA APRIMORADA DE PREÇOS - Item: {item_code}")
        print("="*70 + "\n")

        all_prices = []
        sources_used = []
        
        # 1. PAINEL DE PREÇOS
        print("1️⃣  Consultando Painel de Preços...")
        try:
            painel_prices = self._collect_from_painel(item_code, catalog_type, region)
            if painel_prices:
                all_prices.extend(painel_prices)
                sources_used.append({
                    'fonte': 'Painel de Preços',
                    'quantidade': len(painel_prices),
                })
                print(f"   ✅ {len(painel_prices)} preços encontrados")
            else:
                print("   ℹ️  Nenhum preço encontrado")
        except Exception as e:
            print(f"   ⚠️  Erro: {e}")
            print("   ℹ️  Nenhum preço encontrado")

        # 2. PNCP
        print("\n2️⃣  Consultando PNCP...")
        try:
            pncp_prices = self._collect_from_pncp(item_code, catalog_type, region, max_days)
            if pncp_prices:
                all_prices.extend(pncp_prices)
                sources_used.append({
                    'fonte': 'PNCP',
                    'quantidade': len(pncp_prices),
                })
                print(f"   ✅ {len(pncp_prices)} preços encontrados")
            else:
                print("   ℹ️  Nenhum preço encontrado")
        except Exception as e:
            print(f"   ⚠️  Erro: {e}")
            print("   ℹ️  Nenhum preço encontrado")

        # 3. COMPRASNET
        print("\n3️⃣  Consultando ComprasNet...")
        try:
            comprasnet_prices = self._collect_from_comprasnet(item_code, catalog_type)
            if comprasnet_prices:
                all_prices.extend(comprasnet_prices)
                sources_used.append({
                    'fonte': 'ComprasNet',
                    'quantidade': len(comprasnet_prices),
                })
                print(f"   ✅ {len(comprasnet_prices)} preços encontrados")
            else:
                print("   ℹ️  Nenhum preço encontrado")
        except Exception as e:
            print(f"   ⚠️  Erro: {e}")
            print("   ℹ️  Nenhum preço encontrado")

        # 4. PORTAL DA TRANSPARÊNCIA
        print("\n4️⃣  Consultando Portal da Transparência...")
        try:
            pt_prices = self._collect_from_portal_transparencia(item_code, catalog_type)
            if pt_prices:
                all_prices.extend(pt_prices)
                sources_used.append({
                    'fonte': 'Portal da Transparência',
                    'quantidade': len(pt_prices),
                })
                print(f"   ✅ {len(pt_prices)} preços encontrados")
            else:
                print("   ℹ️  Nenhum preço encontrado")
        except Exception as e:
            print(f"   ⚠️  Erro: {e}")
            print("   ℹ️  Nenhum preço encontrado")

        # Fallback para dados mockados
        fallback_used = False
        if not all_prices:
            fallback_used = True
            print("\n" + "="*30)
            print("   ⚠️ NENHUM PREÇO REAL ENCONTRADO   ")
            print("   Fallback para dados mockados...   ")
            print("="*30 + "\n")
            try:
                from app.services.mock_price_data import generate_mock_prices
                mock_prices = generate_mock_prices(item_code, count=35)
                all_prices.extend(mock_prices)
                sources_used.append({
                    'fonte': 'DADOS DE TESTE (Mockados)',
                    'quantidade': len(mock_prices),
                })
            except Exception as e:
                print(f"   ❌ Erro ao gerar dados mockados: {e}")

        # Limpeza, normalização e ordenação
        all_prices = self._clean_prices(all_prices)
        all_prices = self._normalize_dates(all_prices)
        all_prices.sort(key=lambda x: x.get('date', '1900-01-01'), reverse=True)
        
        item_description = self.catmat.get_description(item_code) if catalog_type == 'material' else self.catser.get_description(item_code)
        
        # Resumo final
        print("\n" + "="*70)
        print(f"✅ COLETA CONCLUÍDA - {len(all_prices)} preços válidos")
        print(f"   📊 Fontes consultadas: {len(sources_used)}")
        if sources_used:
            fontes_str = ', '.join([s['fonte'] for s in sources_used])
            print(f"   📍 Fontes: {fontes_str}")
        print("="*70 + "\n")
        
        return {
            'item_code': item_code,
            'item_description': item_description or 'Descrição não disponível',
            'catalog_type': catalog_type,
            'prices': all_prices,
            'total_prices': len(all_prices),
            'sources': sources_used,
            'filters': {
                'region': region,
                'max_days': max_days
            },
            'collection_date': datetime.now(),
            'metadata': {
                'suppliers_validated': validate_suppliers,
                'cache_hit': False,
                'fallback_used': fallback_used
            }
        }
    
    def _collect_from_painel(self, item_code: str, catalog_type: str, region: Optional[str]) -> List[Dict]:
        """Coleta do Painel de Preços"""
        return self.painel_precos.search_by_item(
            item_code=item_code,
            catalog_type=catalog_type,
            region=region
        )
    
    def _collect_from_pncp(self, item_code: str, catalog_type: str, region: Optional[str], max_days: int) -> List[Dict]:
        """Coleta do PNCP"""
        return self.pncp.search_contracts(
            item_code=item_code,
            catalog_type=catalog_type,
            max_days=max_days,
            region=region
        )
    
    def _collect_from_comprasnet(self, item_code: str, catalog_type: str) -> List[Dict]:
        """Coleta do ComprasNet"""
        return self.comprasnet.search_by_item(item_code, catalog_type=catalog_type)
    
    def _collect_from_portal_transparencia(self, item_code: str, catalog_type: str) -> List[Dict]:
        """Coleta do Portal da Transparência"""
        return self.portal_transparencia.search_by_item(item_code, catalog_type=catalog_type)
    
    def _clean_prices(self, prices: List[Dict]) -> List[Dict]:
        """Remove duplicatas"""
        if not prices:
            return []
        
        unique_prices = []
        seen = set()
        
        for p in prices:
            key = (
                round(p.get('price', 0), 2),
                p.get('supplier'),
                str(p.get('date'))
            )
            
            if key not in seen:
                seen.add(key)
                unique_prices.append(p)
        
        return unique_prices
    
    def search_item(self, description: str) -> Dict:
        """Busca item nos catálogos"""
        materiais = self.catmat.search_by_description(description)
        servicos = self.catser.search_by_description(description)
        
        return {
            'materiais': materiais,
            'servicos': servicos,
            'total': len(materiais) + len(servicos)
        }
    
    def get_catalog_info(self, item_code: str, catalog_type: str) -> Dict:
        """Informações do catálogo"""
        if catalog_type == 'material':
            return {
                'code': item_code,
                'description': self.catmat.get_description(item_code) or 'N/A',
                'catalog': 'CATMAT',
                'type': catalog_type
            }
        else:
            return {
                'code': item_code,
                'description': self.catser.get_description(item_code) or 'N/A',
                'catalog': 'CATSER',
                'type': catalog_type
            }
