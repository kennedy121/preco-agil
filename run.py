#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Preço Ágil - Sistema de Pesquisa de Preços para Licitações

Conforme:
- Lei 14.133/2021 (Nova Lei de Licitações)
- Portaria TCU 121/2023 (Pesquisa de Preços)
- Portaria TCU 122/2023 (Catálogo Eletrônico)
- Portaria TCU 123/2023 (Sistema Nacional de Preços)
"""

from app.models import create_app
from config import Config
import os

# Cria a aplicação
app = create_app()

if __name__ == '__main__':
    # Cria diretórios necessários
    os.makedirs(Config.DATA_DIR, exist_ok=True)
    os.makedirs(Config.REPORTS_DIR, exist_ok=True)
    
    # Banner
    print("\n" + "="*70)
    print("🚀 PREÇO ÁGIL - SISTEMA DE PESQUISA DE PREÇOS")
    print("="*70)
    print(f"📋 Versão: {Config.APP_VERSION}")
    print(f"📋 Lei 14.133/2021 | Portarias TCU 121, 122 e 123/2023")
    print("="*70)
    print(f"🌐 Servidor: http://{Config.HOST}:{Config.PORT}")
    print(f"📊 Ambiente: {'Desenvolvimento' if Config.DEBUG else 'Produção'}")
    print(f"💾 Banco: {Config.SQLALCHEMY_DATABASE_URI}")
    print(f"📁 CATMAT: {'✅' if os.path.exists(Config.CATMAT_FILE) else '❌'} {Config.CATMAT_FILE}")
    print(f"📁 CATSER: {'✅' if os.path.exists(Config.CATSER_FILE) else '❌'} {Config.CATSER_FILE}")
    print("="*70 + "\n")
    
    # Verifica arquivos CSV
    if not os.path.exists(Config.CATMAT_FILE):
        print("⚠️ AVISO: Arquivo catmat.csv não encontrado em data/")
        print("   Coloque o arquivo CSV com as colunas: codigo,descricao\n")
    
    if not os.path.exists(Config.CATSER_FILE):
        print("⚠️ AVISO: Arquivo catser.csv não encontrado em data/")
        print("   Coloque o arquivo CSV com as colunas: codigo,descricao\n")
    
    # Inicia o servidor
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
