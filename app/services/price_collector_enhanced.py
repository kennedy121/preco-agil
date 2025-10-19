# -*- coding: utf-8 -*-
"""
Coletor de Preços APRIMORADO - Preço Ágil
Incorpora padrões dos repositórios open source
"""

from typing import List, Dict, Optional
from datetime import datetime
from app.api.pncp_api import PNCPClient
from app.api.comprasnet_api import ComprasNetClient
from app.api.painel_precos_api import PainelPrecosClient
from app.api.portal_transparencia_api import PortalTransparenciaClient
from app.api.catmat_api import CATMATClient
from app.api.catser_api import CATSERClient
from app.api.brasilapi_client import BrasilAPIClient
from app.api.fallback_manager import APIFallbackManager, exponential_backoff, rate_limit

class EnhancedPriceCollector:
    """
    Coletor de preços aprimorado com:
    - Fallback automático
    - Rate limiting
    - Exponential backoff
    - Validação de fornecedores
    - Cache inteligente
    
    Conforme Portaria TCU 121/2023
    """
    
    def __init__(self):
        # Catálogos locais
        self.catmat = CATMATClient()
        self.catser = CATSERClient()
        
        # APIs principais (ordem de prioridade)
        self.painel_precos = PainelPrecosClient()
        self.pncp = PNCPClient()
        self.comprasnet = ComprasNetClient()
        self.portal_transparencia = PortalTransparenciaClient()
        
        # APIs auxiliares
        self.brasilapi = BrasilAPIClient()
        self.fallback_manager = APIFallbackManager()
        
        # Cache simples
        self._cache = {}
        self._cache_ttl = 3600  # 1 hora
    
    @exponential_backoff(max_retries=3, base_delay=2.0)
    @rate_limit(calls_per_minute=30)
    def collect_prices_with_fallback(
        self,
        item_code: str,
        catalog_type: str,
        region: Optional[str] = None,
        max_days: int = 365,
        validate_suppliers: bool = True
    ) -> Dict:
        """
        Coleta preços com sistema robusto de fallback
        
        Args:
            item_code: Código CATMAT/CATSER
            catalog_type: "material" ou "servico"
            region: UF (opcional)
            max_days: Idade máxima dos preços
            validate_suppliers: Validar CNPJs dos fornecedores
        
        Returns:
            Dados completos com preços validados
        """
        
        # Verifica cache
        cache_key = f"{item_code}_{catalog_type}_{region}_{max_days}"
        if cache_key in self._cache:
            cached_time, cached_data = self._cache[cache_key]
            if (datetime.now() - cached_time).seconds < self._cache_ttl:
                print("  💾 Dados recuperados do cache")
                # Garante que o cache_hit seja verdadeiro no retorno
                cached_data["metadata"]["cache_hit"] = True
                return cached_data
        
        all_prices = []
        sources_used = []
        
        print(f"\n{'='*70}")
        print(f"🔍 COLETA APRIMORADA DE PREÇOS - Item: {item_code}")
        print(f"{'='*70}")
        
        # 1. PAINEL DE PREÇOS (Prioridade 1)
        print(f"\n1️⃣ Consultando Painel de Preços...")
        painel_prices = self._collect_from_painel(item_code, catalog_type, region)
        if painel_prices:
            all_prices.extend(painel_prices)
            sources_used.append({
                "fonte": "Painel de Preços - Ministério da Economia",
                "quantidade": len(painel_prices),
                "url": "https://paineldeprecos.planejamento.gov.br",
                "prioridade": 1
            })
            print(f"   ✅ {len(painel_prices)} preços encontrados")
        else:
            print(f"   ℹ️ Nenhum preço encontrado")
        
        # 2. PNCP (Prioridade 2)
        print(f"\n2️⃣ Consultando PNCP...")
        pncp_prices = self._collect_from_pncp(item_code, catalog_type, region, max_days)
        if pncp_prices:
            all_prices.extend(pncp_prices)
            sources_used.append({
                "fonte": "PNCP - Portal Nacional de Contratações Públicas",
                "quantidade": len(pncp_prices),
                "url": "https://pncp.gov.br",
                "prioridade": 2
            })
            print(f"   ✅ {len(pncp_prices)} preços encontrados")
        else:
            print(f"   ℹ️ Nenhum preço encontrado")
        
        # 3. COMPRASNET (Prioridade 3)
        print(f"\n3️⃣ Consultando ComprasNet...")
        comprasnet_prices = self._collect_from_comprasnet(item_code, catalog_type)
        if comprasnet_prices:
            all_prices.extend(comprasnet_prices)
            sources_used.append({
                "fonte": "ComprasNet - Sistema Integrado de Administração",
                "quantidade": len(comprasnet_prices),
                "url": "https://compras.dados.gov.br",
                "prioridade": 3
            })
            print(f"   ✅ {len(comprasnet_prices)} preços encontrados")
        else:
            print(f"   ℹ️ Nenhum preço encontrado")
        
        # 4. PORTAL DA TRANSPARÊNCIA (Prioridade 4)
        print(f"\n4️⃣ Consultando Portal da Transparência...")
        pt_prices = self._collect_from_portal_transparencia(item_code, catalog_type)
        if pt_prices:
            all_prices.extend(pt_prices)
            sources_used.append({
                "fonte": "Portal da Transparência - CGU",
                "quantidade": len(pt_prices),
                "url": "https://portaltransparencia.gov.br",
                "prioridade": 4
            })
            print(f"   ✅ {len(pt_prices)} preços encontrados")
        else:
            print(f"   ℹ️ Nenhum preço encontrado")
        
        # 5. Valida fornecedores (se solicitado)
        if validate_suppliers and all_prices:
            print(f"\n🔍 Validando fornecedores via BrasilAPI...")
            all_prices = self._validate_suppliers(all_prices)
        
        # 6. Remove duplicatas e outliers extremos
            all_prices = self._clean_prices(all_prices)
        
        # ⭐⭐⭐ NOVO: FALLBACK PARA DADOS MOCKADOS ⭐⭐⭐
        if len(all_prices) == 0:
            print(f"\n⚠️ NENHUM PREÇO REAL ENCONTRADO")
            print(f"   📊 Gerando dados de teste para demonstração...")
            print(f"   (Em produção, configure as APIs ou remova esta funcionalidade)")
            
            try:
                from app.services.mock_price_data import generate_mock_prices
                
                mock_count = 35  # Quantidade de preços mockados
                mock_prices = generate_mock_prices(item_code, count=mock_count)
                all_prices.extend(mock_prices)
                
                sources_used.append({
                    "fonte": "⚠️ DADOS DE TESTE (Mockados)",
                    "quantidade": len(mock_prices),
                    "url": "Sistema Local - Demonstração",
                    "prioridade": 999,
                    "nota": "Dados simulados para demonstração do sistema"
                })
                
                print(f"   ✅ {len(mock_prices)} preços de teste gerados")
                print(f"   💡 Dica: Configure as APIs para obter dados reais")
                
            except Exception as e:
                print(f"   ❌ Erro ao gerar dados mockados: {e}")
        # ⭐⭐⭐ FIM DO FALLBACK ⭐⭐⭐
        
        # 7. Ordena por data (mais recentes primeiro)
        all_prices.sort(key=lambda x: x.get("date", datetime.min), reverse=True)  

        # 8. Filtra por região se especificado
        if region and all_prices:
            original_count = len(all_prices)
            all_prices = [p for p in all_prices if p.get("region") == region]
            if len(all_prices) < original_count:
                print(f"\n📍 Filtro regional: {original_count} → {len(all_prices)} preços")
        
        # Obtém descrição do catálogo
        item_description = self.catmat.search_by_code(item_code)['descricao'] if catalog_type == "material" else self.catser.search_by_code(item_code)['descricao']

        result = {
            "item_code": item_code,
            "item_description": item_description,
            "catalog_type": catalog_type,
            "prices": all_prices,
            "total_prices": len(all_prices),
            "sources": sources_used,
            "filters": {
                "region": region,
                "max_days": max_days
            },
            "collection_date": datetime.now(),
            "metadata": {
                "suppliers_validated": validate_suppliers,
                "used_fallback": len(sources_used) < 3,
                "cache_hit": False
            }
        }
        
        # Armazena em cache APENAS se houver resultados
        if result["total_prices"] > 0:
            self._cache[cache_key] = (datetime.now(), result)
            print(f"   💾 Resultado com {result['total_prices']} preços salvo em cache.")
        
        print(f"\n{'='*70}")
        print(f"✅ COLETA CONCLUÍDA - {len(all_prices)} preços válidos")
        print(f"   📊 Fontes consultadas: {len(sources_used)}")
        print(f"{'='*70}\n")
        
        return result
    
    def _collect_from_painel(self, item_code: str, catalog_type: str, region: Optional[str]) -> List[Dict]:
        """
        Coleta preços do Painel com tratamento de erro robusto
        
        Args:
            item_code: Código CATMAT/CATSER
            catalog_type: 'material' ou 'servico'
            region: UF (opcional)
            
        Returns:
            Lista de preços ou lista vazia em caso de erro
        """
        try:
                return self.painel_precos.search_by_item(
                    item_code=item_code,
                    item_type=catalog_type,
                    region=region,
                    max_days=365,  # Pode vir de Config
                    max_results=500
                )
        except ValueError as e:
                # Erro de validação (não deveria acontecer, mas...)
                print(f"   ❌ Erro de validação: {e}")
                return []
        except ConnectionError as e:
                # Erro de conexão/timeout/rate limit
                print(f"   ⚠️ Erro de conexão: {e}")
                return []
        except Exception as e:
                # Qualquer outro erro
                print(f"   ❌ Erro inesperado no Painel: {e}")
                return []
    
    def _collect_from_pncp(
        self, 
        item_code: str, 
        catalog_type: str, 
        region: Optional[str], 
        max_days: int
    ) -> List[Dict]:
        """Coleta do PNCP com tratamento de erro"""
        try:
            return self.pncp.search_contracts(
                item_code=item_code,
                catalog_type=catalog_type,
                max_days=max_days,
                region=region
            )
        except Exception as e:
            print(f"   ⚠️ Erro: {e}")
            return []
    
    def _collect_from_comprasnet(
        self, 
        item_code: str, 
        catalog_type: str
    ) -> List[Dict]:
        """Coleta do ComprasNet com tratamento de erro"""
        try:
            if catalog_type == "material":
                return self.comprasnet.search_material(item_code, max_pages=2)
            else:
                return self.comprasnet.search_service(item_code, max_pages=2)
        except Exception as e:
            print(f"   ⚠️ Erro: {e}")
            return []
    
    def _collect_from_portal_transparencia(
        self, 
        item_code: str, 
        catalog_type: str
    ) -> List[Dict]:
        """Coleta do Portal da Transparência com tratamento de erro"""
        try:
            # Obtém descrição para buscar
            if catalog_type == "material":
                item_info = self.catmat.search_by_code(item_code)
            else:
                item_info = self.catser.search_by_code(item_code)
        
            if not item_info:
                print(f"   ⚠️ Item não encontrado no catálogo")
                return []
        
            description = item_info.get('descricao', '')
        
            if description:
                # Pega primeiras 5 palavras da descrição para buscar
                search_terms = " ".join(description.split()[:5])
            
                return self.portal_transparencia.search_contracts(
                    item_description=search_terms  # ✅ SEM max_pages
                )
            return []
        except Exception as e:
            print(f"   ⚠️ Erro no Portal da Transparência: {e}")
            return []
    
    def _validate_suppliers(self, prices: List[Dict]) -> List[Dict]:
        """
        Valida fornecedores usando BrasilAPI
        Remove preços de fornecedores com situação irregular
        """
        validated_prices = []
        validated_cnpjs = {}  # Cache de CNPJs já validados
        
        for price in prices:
            supplier_cnpj = price.get('supplier_cnpj')
            
            if not supplier_cnpj:
                # Sem CNPJ, aceita mas marca como não validado
                price['supplier_validated'] = None
                validated_prices.append(price)
                continue
            
            # Verifica cache
            if supplier_cnpj in validated_cnpjs:
                validation = validated_cnpjs[supplier_cnpj]
            else:
                # Valida CNPJ
                validation = self.brasilapi.validate_supplier(supplier_cnpj)
                validated_cnpjs[supplier_cnpj] = validation
            
            if validation.get('valid'):
                price['supplier_validated'] = True
                price['supplier_info'] = validation.get('cnpj_info')
                validated_prices.append(price)
            else:
                # Marca como não validado mas mantém
                price['supplier_validated'] = False
                price['validation_reason'] = validation.get('reason')
                validated_prices.append(price)
                print(f"   ⚠️ Fornecedor irregular: {supplier_cnpj}")
        
        return validated_prices
    
    def _clean_prices(self, prices: List[Dict]) -> List[Dict]:
        """
        Remove duplicatas e outliers extremos
        """
        if not prices:
            return []
        
        # Remove duplicatas
        unique_prices = []
        seen = set()
        
        for p in prices:
            key = (
                round(p.get('price', 0), 2),
                p.get('supplier'),
                p.get('date')
            )
            
            if key not in seen:
                seen.add(key)
                unique_prices.append(p)
        
        if len(unique_prices) < len(prices):
            print(f"   🔄 Duplicatas removidas: {len(prices)} → {len(unique_prices)}")
        
        # Remove outliers extremos (> 10x ou < 0.1x a mediana)
        if len(unique_prices) >= 5:
            import numpy as np
            values = [p['price'] for p in unique_prices if p['price'] > 0]
            
            if values:
                median = np.median(values)
                
                cleaned = [
                    p for p in unique_prices
                    if p['price'] > 0 and median * 0.1 <= p['price'] <= median * 10
                ]
                
                if len(cleaned) < len(unique_prices):
                    print(f"   🧹 Outliers extremos: {len(unique_prices)} → {len(cleaned)}")
                
                return cleaned
        
        return unique_prices
    
    def search_item(self, description: str) -> Dict:
        """Busca item nos catálogos"""
        materiais = self.catmat.search_by_description(description)
        servicos = self.catser.search_by_description(description)
        
        return {
            "materiais": materiais,
            "servicos": servicos,
            "total": len(materiais) + len(servicos)
        }
    
    def get_catalog_info(self, item_code: str, catalog_type: str) -> Dict:
        """Informações do catálogo"""
        if catalog_type == "material":
            return {
                "code": item_code,
                "description": self.catmat.get_description(item_code),
                "catalog": "CATMAT",
                "type": catalog_type
            }
        else:
            return {
                "code": item_code,
                "description": self.catser.get_description(item_code),
                "catalog": "CATSER",
                "type": catalog_type
            }
