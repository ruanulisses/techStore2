// Adiciona um ouvinte de eventos que aguarda o carregamento completo do DOM
document.addEventListener('DOMContentLoaded', () => {

    // Seleciona todos os botões com a classe 'add_carinho' (botões para adicionar ao carrinho)
    let btnsAdicionar = document.querySelectorAll(".add_carinho");

    // Itera sobre cada botão encontrado
    btnsAdicionar.forEach(btn => {
        // Adiciona um ouvinte de evento 'click' para cada botão
        btn.addEventListener("click", function() {
            // Encontra o elemento pai mais próximo com a classe 'produto' (o contêiner do produto)
            let produtoElement = this.closest(".produto");

            // Extrai informações do produto
            let nome = produtoElement.querySelector(".nome_produto").textContent.trim(); // Nome do produto
            let preco = produtoElement.querySelector(".preco").textContent.trim(); // Preço do produto
            let disponibilidade = produtoElement.querySelector(".disponibilidade").textContent.replace('Disponibilidade:', '').trim(); // Disponibilidade do produto
            let imagem = produtoElement.querySelector(".fotos_produtos").src; // URL da imagem do produto

            // Cria um objeto para representar o produto
            let produto = { nome, preco, disponibilidade, imagem };

            // Verifica se o produto está em estoque
            if (disponibilidade === 'Em estoque') {
                
                // Obtém o ID do usuário logado do localStorage
                let userId = localStorage.getItem('userId');

                // Se não houver um usuário logado, exibe uma mensagem de alerta e encerra a função
                if (!userId) {
                    alert('Por favor, faça login para adicionar produtos ao carrinho.');
                    return;
                }

                // Define a chave para o carrinho baseada no ID do usuário
                let carrinhoKey = `carrinho_${userId}`;

                // Obtém o carrinho do localStorage ou inicializa como um array vazio
                //prese tranforma stirng em outros tipos de dados
                let carrinho = JSON.parse(localStorage.getItem(carrinhoKey)) || [];

                // Adiciona o novo produto ao carrinho
                carrinho.push(produto);

                // Atualiza o carrinho no localStorage
                localStorage.setItem(carrinhoKey, JSON.stringify(carrinho));

            
                alert("Produto adicionado ao carrinho!");
            } else {
               
                alert("Produto sem estoque");
            }
        });
    });
});