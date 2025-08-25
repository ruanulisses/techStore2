
var btn_exp = document.querySelector('#btn_exp')
var menu_side = document.querySelector('.menu_lateral')

btn_exp.addEventListener('click', function(){
    menu_side.classList.toggle('expandir')
})


function toggleExpand() {
    var box = document.getElementById('btn_expandir');
    box.classList.toggle('expanded');
}

// foksofoas

document.addEventListener('DOMContentLoaded', () => {
    // Seleciona todos os containers e setas
    const containers = document.querySelectorAll('.container');
    const leftArrows = document.querySelectorAll('.bi-chevron-left');
    const rightArrows = document.querySelectorAll('.bi-chevron-right');

    const scrollAmount = 500; // Define a quantidade de rolagem em pixels

    // Adiciona event listener para todas as setas de esquerda
    leftArrows.forEach((leftArrow, index) => {
        leftArrow.addEventListener('click', () => {
            containers[index].scrollBy({
                left: -scrollAmount,
                behavior: 'smooth'
            });
        });
    });

    // Adiciona event listener para todas as setas de direita
    rightArrows.forEach((rightArrow, index) => {
        rightArrow.addEventListener('click', () => {
            containers[index].scrollBy({
                left: scrollAmount,
                behavior: 'smooth'
            });
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const produtos = document.querySelectorAll('.produto');
    let clickTimer = null;
    const clickDelay = 300; // Tempo em milissegundos para considerar dois cliques como um duplo clique

    produtos.forEach(produto => {
        produto.addEventListener('click', () => {
            // Se o temporizador já estiver definido, significa que é um duplo clique
            if (clickTimer !== null) {
                clearTimeout(clickTimer);
                clickTimer = null;

                // Remove a classe "expanded" de todos os produtos
                produtos.forEach(p => {
                    if (p !== produto) {
                        p.classList.remove('expanded');
                    }
                });
                

                // Alterna a classe "expanded" no produto clicado
                produto.classList.toggle('expanded');
            } else {
                // Se não for um duplo clique, define o temporizador para o próximo clique
                clickTimer = setTimeout(() => {
                    clickTimer = null;
                }, clickDelay);
            }
        });
    });
});


// Selecione todos os botões e containers
var botoesVerMais = document.querySelectorAll('.btn_expandir_contaner');
var containers = document.querySelectorAll('.container');

botoesVerMais.forEach(function(botao, index) {
    botao.addEventListener('click', function() {
        var container = containers[index];
        
        // Seleciona as setas dentro do container atual
        var leftArrow = container.querySelector('.bi-chevron-left');
        var rightArrow = container.querySelector('.bi-chevron-right');

        // Toggle a classe expandir_contaner
        container.classList.toggle('expandir_contaner');

        // Alterna o texto do botão entre "Ver mais" e "Ver menos"
        if (botao.textContent.includes('Mais')) {
            botao.innerHTML = '<i class="bi bi-chevron-up"></i> Menos';
            // Esconde as setas
            if (leftArrow) leftArrow.style.display = 'none';
            if (rightArrow) rightArrow.style.display = 'none';
        } else {
            botao.innerHTML = '<i class="bi bi-chevron-down"></i> Mais';
            // Mostra as setas novamente
            if (leftArrow) leftArrow.style.display = 'block';
            if (rightArrow) rightArrow.style.display = 'block';
        }

        // Ajuste a rolagem se necessário
        if (container.classList.contains('expandir_contaner')) {
            // Espera o tempo da transição CSS
            setTimeout(function() {
                // Ajusta a rolagem para garantir que o container esteja visível sem alterar a posição atual
                container.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 300); // Tempo de transição CSS
        }
    });
});


var btn_exp = document.querySelector('#btn_exp')
var menu_side = document.querySelector('.menu_lateral')

btn_exp.addEventListener('click', function(){
    menu_side.classList.toggle('expandir')
})


function toggleExpand() {
    var box = document.getElementById('btn_expandir');
    box.classList.toggle('expanded');
}