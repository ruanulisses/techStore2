function updateCartCounter() {
    let userId = localStorage.getItem('userId');
    if (!userId) return;

    let carrinhoKey = `carrinho_${userId}`;
    let carrinho = JSON.parse(localStorage.getItem(carrinhoKey)) || [];
    let carrinhoCont = carrinho.length;
    localStorage.setItem('carrinho_cont', carrinhoCont);

    const cartCounter = document.getElementById('cart-counter');
    if (cartCounter) {
        cartCounter.textContent = carrinhoCont;
        if (carrinhoCont > 0) {
            cartCounter.style.display = 'inline';
        } else {
            cartCounter.className = `bi bi-0-circle-fill`;
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Atualiza o contador na carga da página
    updateCartCounter();
});

function addItemToCart() {
    let userId = localStorage.getItem('userId');
    if (!userId) return;

    let carrinhoKey = `carrinho_${userId}`;
    let carrinho = JSON.parse(localStorage.getItem(carrinhoKey)) || [];

    carrinho.push({/* Dados do item */});
    localStorage.setItem(carrinhoKey, JSON.stringify(carrinho));

    // Atualiza o contador do carrinho
    updateCartCounter();
}

function removeItemFromCart(index) {
    let userId = localStorage.getItem('userId');
    if (!userId) return;

    let carrinhoKey = `carrinho_${userId}`;
    let carrinho = JSON.parse(localStorage.getItem(carrinhoKey)) || [];

    if (index >= 0 && index < carrinho.length) {
        carrinho.splice(index, 1);
        localStorage.setItem(carrinhoKey, JSON.stringify(carrinho));

        // Atualiza o contador do carrinho
        updateCartCounter();
    }
}

// No carregamento da página do carrinho
document.addEventListener('DOMContentLoaded', () => {
    let userId = localStorage.getItem('userId');
    if (!userId) return;

    let carrinhoKey = `carrinho_${userId}`;
    let carrinho = JSON.parse(localStorage.getItem(carrinhoKey)) || [];
    let carrinhoContainer = document.querySelector(".carrinho");

    if (!carrinhoContainer) {
        console.error("Elemento .carrinho não encontrado na página.");
        return;
    }

    if (carrinho.length === 0) {
        carrinhoContainer.innerHTML = "<p>Seu carrinho está vazio.</p>";
    } else {
        carrinhoContainer.innerHTML = "";

        carrinho.forEach((produto, index) => {
            let div = document.createElement("div");
            div.setAttribute("class", "item-carrinho");

            let img = document.createElement("img");
            img.src = produto.imagem;
            img.alt = produto.nome;
            div.appendChild(img);

            let h2 = document.createElement("h2");
            h2.textContent = produto.nome;
            div.appendChild(h2);

            let pPreco = document.createElement("p");
            pPreco.textContent = `Preço: R$ ${parseFloat(produto.preco).toFixed(2)}`;
            div.appendChild(pPreco);

            let pDisponibilidade = document.createElement("p");
            pDisponibilidade.textContent = produto.disponibilidade;
            div.appendChild(pDisponibilidade);

            let removeBtn = document.createElement("button");
            removeBtn.textContent = "Deletar";
            removeBtn.className = "remove-btn";
            removeBtn.addEventListener("click", () => {
                removeItemFromCart(index);
                // Atualiza a visualização do carrinho e o contador
                window.location.reload();
            });
            div.appendChild(removeBtn);

            carrinhoContainer.appendChild(div);
        });

        let total = calcularTotalCarrinho(carrinho);

        let totalElement = document.createElement("p");
        totalElement.className = "total-carrinho";
        totalElement.textContent = `Total: R$ ${total.toFixed(2)}`;
        carrinhoContainer.appendChild(totalElement);
    }

    // Atualiza o contador do carrinho
    updateCartCounter();
});