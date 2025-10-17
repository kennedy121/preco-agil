
// static/js/main.js
// Preço Ágil - JavaScript Principal

console.log('🚀 Preço Ágil - JavaScript carregando...');

/**
 * Função para selecionar item e abrir modal
 */
function selecionarItem(codigo, tipo, descricao) {
    console.log('📦 Item selecionado:', codigo, tipo);
    
    try {
        // Preenche campos hidden
        const inputCode = document.getElementById('item_code');
        const inputType = document.getElementById('catalog_type');
        
        if (inputCode) inputCode.value = codigo;
        if (inputType) inputType.value = tipo;
        
        // Preenche campos de exibição
        const spanCode = document.getElementById('display_code');
        const spanDesc = document.getElementById('display_desc');
        
        if (spanCode) spanCode.textContent = codigo;
        if (spanDesc) spanDesc.textContent = descricao.substring(0, 200);
        
        // Abre modal
        const modalElement = document.getElementById('modalPesquisa');
        if (modalElement) {
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
            console.log('✅ Modal aberto!');
        } else {
            console.error('❌ Modal não encontrado!');
        }
    } catch (error) {
        console.error('❌ Erro ao selecionar item:', error);
    }
}

/**
 * Inicialização quando DOM carrega
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ DOM carregado');
    
    // Aguarda um pouco para garantir que tudo carregou
    setTimeout(function() {
        inicializarEventListeners();
    }, 100);
    
    // Auto-fechar alerts
    configurarAlerts();
});

/**
 * Inicializa event listeners nos botões
 */
function inicializarEventListeners() {
    const botoes = document.querySelectorAll('.btn-selecionar-item');
    
    console.log(`🔍 Encontrados ${botoes.length} botões`);
    
    if (botoes.length === 0) {
        console.warn('⚠️ Nenhum botão encontrado. Os resultados foram carregados?');
        return;
    }
    
    botoes.forEach(function(botao, index) {
        // Remove listeners antigos (se houver)
        const novoBtn = botao.cloneNode(true);
        botao.parentNode.replaceChild(novoBtn, botao);
        
        // Adiciona novo listener
        novoBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const codigo = this.getAttribute('data-codigo');
            const tipo = this.getAttribute('data-tipo');
            const descricao = this.getAttribute('data-descricao');
            
            console.log(`🖱️ Clique no botão ${index + 1}:`, codigo, tipo);
            
            if (codigo && tipo && descricao) {
                selecionarItem(codigo, tipo, descricao);
            } else {
                console.error('❌ Dados incompletos:', {codigo, tipo, descricao});
            }
        });
    });
    
    console.log('✅ Event listeners adicionados a todos os botões');
}

/**
 * Configura auto-fechar para alerts
 */
function configurarAlerts() {
    const alerts = document.querySelectorAll('.alert-dismissible');
    
    alerts.forEach(function(alert) {
        // Não fecha o alert do modal
        if (!alert.closest('#modalPesquisa')) {
            setTimeout(function() {
                try {
                    const bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                } catch(e) {
                    // Ignora erro se já foi fechado
                }
            }, 5000);
        }
    });
}

// Expõe função globalmente para debug
window.selecionarItem = selecionarItem;
window.inicializarEventListeners = inicializarEventListeners;

console.log('✅ JavaScript carregado completamente');
