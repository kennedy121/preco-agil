// static/js/main.js
// Preço Ágil - JavaScript Principal

/**
 * Função para selecionar item e abrir modal de pesquisa
 */
function selecionarItem(codigo, tipo, descricao) {
    console.log('Item selecionado:', codigo, tipo, descricao);
    
    // Preenche campos hidden do formulário
    document.getElementById('item_code').value = codigo;
    document.getElementById('catalog_type').value = tipo;
    
    // Preenche informações visuais
    document.getElementById('display_code').textContent = codigo;
    document.getElementById('display_desc').textContent = descricao;
    
    // Abre o modal
    const modalElement = document.getElementById('modalPesquisa');
    if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    } else {
        console.error('Modal não encontrado!');
    }
}

/**
 * Inicialização quando página carrega
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('Preço Ágil - JavaScript carregado');
    
    // ⭐ Event listeners para botões de selecionar
    const botoes = document.querySelectorAll('.btn-selecionar-item');
    console.log(`Encontrados ${botoes.length} botões`);
    
    botoes.forEach(function(botao) {
        botao.addEventListener('click', function() {
            const codigo = this.getAttribute('data-codigo');
            const tipo = this.getAttribute('data-tipo');
            const descricao = this.getAttribute('data-descricao');
            
            console.log('Clicou em:', codigo, tipo);
            selecionarItem(codigo, tipo, descricao);
        });
    });
    
    // Configurações de mensagens flash (auto-fechar após 5 segundos)
    const alerts = document.querySelectorAll('.alert:not(.alert-info)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

/**
 * Funcionalidade dos cards informativos
 */
document.addEventListener('DOMContentLoaded', function() {
    
    // Botão Conformidade Legal
    const conformidadeCards = document.querySelectorAll('.card.border-primary');
    conformidadeCards.forEach(card => {
        card.style.cursor = 'pointer';
        card.addEventListener('click', function() {
            // Abrir modal ou mostrar informações
            showConformidadeModal();
        });
    });
    
    // Botão Análise Estatística
    const analiseCards = document.querySelectorAll('.card.border-success');
    analiseCards.forEach(card => {
        card.style.cursor = 'pointer';
        card.addEventListener('click', function() {
            showAnaliseModal();
        });
    });
    
    // Botão Relatório PDF
    const pdfCards = document.querySelectorAll('.card.border-info');
    pdfCards.forEach(card => {
        card.style.cursor = 'pointer';
        card.addEventListener('click', function() {
            showPDFInfo();
        });
    });
});

function showConformidadeModal() {
    const modalHTML = `
        <div class="modal fade" id="conformidadeModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title">
                            <i class="bi bi-shield-check me-2"></i>Conformidade Legal
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <h6 class="text-primary">Legislação Aplicável</h6>
                        <ul>
                            <li><strong>Lei 14.133/2021</strong> - Nova Lei de Licitações (Art. 23)</li>
                            <li><strong>Portaria TCU 121/2023</strong> - Metodologia de Pesquisa (Art. 26, 28, 29)</li>
                            <li><strong>Portaria TCU 122/2023</strong> - Catálogo Eletrônico</li>
                            <li><strong>Portaria TCU 123/2023</strong> - Sistema Nacional de Preços</li>
                        </ul>
                        
                        <h6 class="text-primary mt-3">Requisitos Atendidos</h6>
                        <ul>
                            <li>✅ Pesquisa em múltiplas fontes oficiais</li>
                            <li>✅ Análise estatística robusta</li>
                            <li>✅ Documentação completa</li>
                            <li>✅ Rastreabilidade total</li>
                        </ul>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Adiciona modal ao DOM
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    const modal = new bootstrap.Modal(document.getElementById('conformidadeModal'));
    modal.show();
    
    // Remove modal após fechar
    document.getElementById('conformidadeModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

function showAnaliseModal() {
    const modalHTML = `
        <div class="modal fade" id="analiseModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header bg-success text-white">
                        <h5 class="modal-title">
                            <i class="bi bi-graph-up me-2"></i>Análise Estatística
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <h6 class="text-success">Metodologia Estatística</h6>
                        <p>O sistema utiliza metodologia robusta conforme TCU:</p>
                        
                        <ul>
                            <li><strong>Mediana:</strong> Valor central que divide a distribuição ao meio</li>
                            <li><strong>Média Saneada:</strong> Média após remoção de outliers</li>
                            <li><strong>IQR (Interquartile Range):</strong> Método de detecção de valores discrepantes</li>
                        </ul>
                        
                        <h6 class="text-success mt-3">Indicadores Calculados</h6>
                        <ul>
                            <li>📊 Mediana (Q2)</li>
                            <li>📊 Primeiro Quartil (Q1)</li>
                            <li>📊 Terceiro Quartil (Q3)</li>
                            <li>📊 Média Saneada</li>
                            <li>📊 Desvio Padrão</li>
                            <li>📊 Coeficiente de Variação</li>
                        </ul>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    const modal = new bootstrap.Modal(document.getElementById('analiseModal'));
    modal.show();
    
    document.getElementById('analiseModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

function showPDFInfo() {
    const modalHTML = `
        <div class="modal fade" id="pdfModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header bg-info text-white">
                        <h5 class="modal-title">
                            <i class="bi bi-file-earmark-pdf me-2"></i>Relatório PDF
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <h6 class="text-info">Conteúdo do Relatório</h6>
                        <p>O relatório PDF contém todas as informações necessárias:</p>
                        
                        <ul>
                            <li>📄 Identificação do item pesquisado</li>
                            <li>📄 Fontes consultadas (com URLs)</li>
                            <li>📄 Série completa de preços coletados</li>
                            <li>📄 Análise estatística detalhada</li>
                            <li>📄 Gráficos e visualizações</li>
                            <li>📄 Justificativa da metodologia</li>
                            <li>📄 Valor estimado recomendado</li>
                        </ul>
                        
                        <div class="alert alert-info mt-3">
                            <i class="bi bi-info-circle me-2"></i>
                            <strong>Conformidade:</strong> O relatório atende todos os requisitos do 
                            Art. 29 da Portaria TCU 121/2023
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    const modal = new bootstrap.Modal(document.getElementById('pdfModal'));
    modal.show();
    
    document.getElementById('pdfModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

console.log('✅ Funcionalidades dos cards carregadas');
