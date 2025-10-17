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