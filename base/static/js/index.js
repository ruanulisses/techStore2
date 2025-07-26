  let paginaAtual = 0;
        const paginas = document.querySelectorAll('.page');
        const botao = document.getElementById('ver-outros');

        botao.addEventListener('click', () => {
            paginas[paginaAtual].style.display = 'none';
            paginaAtual = (paginaAtual + 1) % paginas.length;
            paginas[paginaAtual].style.display = 'flex';
        });
        // ----------- função para aparece o menuSuspenso -------
        var menuSuspenso = document.getElementById("menuProduto");


        function pEnter() {
            menuSuspenso.style.display = 'grid'
        }

        function pClose() {
            menuSuspenso.style.display = 'none'
        }

        // -------------- function para o menu na vertical quando a tela esta pequena--------------
        var MenuItems = document.getElementById('menuItems');

        MenuItems.style.maxHeight = "0px";

        function menutoggle() {
            if (MenuItems.style.maxHeight == "0px") {
                MenuItems.style.maxHeight = "200px"
            } else {
                MenuItems.style.maxHeight = "0px"
            }
        }

        // animar todos os itens na tela que tiverem meu atributo data-anime

        const item = document.querySelectorAll("[data-anime]");

        const animeScroll = () => {
            const windowTop = window.scrollY + window.innerHeight * 0.65 ;

            item.forEach((element) => {
                if (windowTop > element.offsetTop) {
                    element.classList.add("animate");
                } else {
                element.classList.remove("animate")
                }
            });
        };

        animeScroll();
        window.addEventListener("scroll", () => {
            animeScroll();
        })


        /* ---------- js para products gallery ----------- */
        // para mudar a foto de destaque na pagina
        var ProductImg = document.getElementById('product-img');
        var SmallImg = document.getElementsByClassName('small-img');

        SmallImg[0].onclick = function(){
        ProductImg.src = SmallImg[0].src;
        }
        SmallImg[1].onclick = function(){
        ProductImg.src = SmallImg[1].src;
        }
        SmallImg[2].onclick = function(){
        ProductImg.src = SmallImg[2].src;
        }
        SmallImg[3].onclick = function(){
        ProductImg.src = SmallImg[3].src;
        }
