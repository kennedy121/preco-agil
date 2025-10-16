🚀 Preço Ágil
Sistema de Pesquisa de Preços para Licitações Públicas

📋 Descrição
O Preço Ágil é uma ferramenta completa para realizar pesquisas de preços conforme a Lei 14.133/2021 (Nova Lei de Licitações) e as Portarias TCU 121, 122 e 123/2023.

✅ Funcionalidades
🔍 Busca em múltiplas fontes oficiais (PNCP, ComprasNet, Painel de Preços)
📊 Análise estatística robusta (mediana, média saneada)
📄 Geração automática de relatórios em PDF
✅ Validação de fornecedores (CNPJ via Receita Federal)
💾 Histórico completo de pesquisas
🔄 Sistema de fallback (alta disponibilidade)

🎯 Conformidade Legal
✅ Lei 14.133/2021 - Nova Lei de Licitações
✅ Portaria TCU 121/2023 - Pesquisa de Preços
✅ Portaria TCU 122/2023 - Catálogo Eletrônico
✅ Portaria TCU 123/2023 - Sistema Nacional de Preços

🛠️ Tecnologias
Python 3.8+
Flask 3.0
SQLAlchemy
Pandas
ReportLab
APIs governamentais

📦 Instalação
1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/preco-agil.git
cd preco-agil
```
2. Crie ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```
3. Instale dependências
```bash
pip install -r requirements.txt
```
4. Configure os catálogos
Baixe os catálogos CATMAT e CATSER em formato CSV e coloque na pasta data/:

data/

├── catmat.csv (formato: codigo,descricao)

└── catser.csv (formato: codigo,descricao)

Fontes oficiais:

CATMAT: https://www.gov.br/compras/pt-br/acesso-a-informacao/catalogo-de-materiais
CATSER: https://www.gov.br/compras/pt-br/acesso-a-informacao/catalogo-de-servicos

5. Configure o .env
```bash
cp .env.example .env
# Edite o .env com suas configurações
```
6. Execute
```bash
python run.py
```
Acesse: http://localhost:8000

📊 APIs Integradas
Painel de Preços - Ministério da Economia (Prioridade 1)
PNCP - Portal Nacional de Contratações Públicas
ComprasNet - Sistema Integrado de Administração
Portal da Transparência - CGU
BrasilAPI - Validação de CNPJ

📖 Como Usar
1.  **Buscar Item**: Digite a descrição do produto/serviço
2.  **Selecionar**: Escolha o código CATMAT ou CATSER
3.  **Pesquisar**: O sistema coleta preços de todas as fontes
4.  **Analisar**: Análise estatística automática
5.  **Download**: Baixe o relatório PDF completo

🤝 Contribuindo
Contribuições são bem-vindas! Por favor:

1.  Fork o projeto
2.  Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3.  Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4.  Push para a branch (`git push origin feature/nova-funcionalidade`)
5.  Abra um Pull Request

📄 Licença
Este projeto está sob a licença MIT.

👥 Autores
*   **Seu Nome** - _Trabalho Inicial_ - [@seu-usuario](https://github.com/seu-usuario)

🙏 Agradecimentos
*   TCU - Pela documentação e orientações
*   Comunidade Open Source brasileira
*   Mantenedores das APIs governamentais

📁 ESTRUTURA DE ARQUIVOS CSV
Formato esperado para `catmat.csv`:
```csv
codigo,descricao
123456,CADEIRA GIRATÓRIA PARA ESCRITÓRIO
234567,MESA DE ESCRITÓRIO EM MADEIRA
345678,COMPUTADOR DESKTOP CORE I5
```
OU com ponto-e-vírgula:
```csv
codigo;descricao
123456;CADEIRA GIRATÓRIA PARA ESCRITÓRIO
234567;MESA DE ESCRITÓRIO EM MADEIRA
345678;COMPUTADOR DESKTOP CORE I5
```

Formato esperado para `catser.csv`:
```csv
codigo,descricao
11001,SERVIÇO DE LIMPEZA E CONSERVAÇÃO
22002,SERVIÇO DE VIGILÂNCIA ARMADA
33003,SERVIÇO DE MANUTENÇÃO PREDIAL
```