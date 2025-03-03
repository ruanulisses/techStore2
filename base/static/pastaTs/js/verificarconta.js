const user_nome = localStorage.getItem('userName');
const user_email = localStorage.getItem('userEmail');
const user_foto = localStorage.getItem('userPhoto');
const user_Ntelefone = localStorage.getItem('userNtelefone');
const user_idade = localStorage.getItem('userIdade');
const user_cidade = localStorage.getItem('userCidade');
const user_CPF = localStorage.getItem('userCPF');

if (user_nome && user_email && user_foto && user_Ntelefone && user_idade && user_cidade) {
    // Criação do elemento div e configuração de seus atributos
    let div = document.createElement("div");
    div.setAttribute("class", "div-dinamica");

    // Criação e adição do elemento img com a foto do usuário
    let img = document.createElement("img");
    img.src = user_foto;
    img.alt = "Foto do usuário"; // Texto alternativo para a imagem
    img.style.width = "100px"; // Definindo largura da imagem
    img.style.height = "100px"; // Definindo altura da imagem
    img.style.borderRadius = "50%"; // Tornar a imagem redonda, se desejar
    div.appendChild(img);

    // Criação e adição do título e nome do usuário
    let nameContainer = document.createElement("div");
    let nameLabel = document.createElement("span");
    nameLabel.textContent = "Nome: ";
    let nameValue = document.createElement("span");
    nameValue.textContent = user_nome;
    nameContainer.appendChild(nameLabel);
    nameContainer.appendChild(nameValue);
    div.appendChild(nameContainer);

    // Criação e adição do título e e-mail do usuário
    let emailContainer = document.createElement("div");
    let emailLabel = document.createElement("span");
    emailLabel.textContent = "Email: ";
    let emailValue = document.createElement("span");
    emailValue.textContent = user_email;
    emailContainer.appendChild(emailLabel);
    emailContainer.appendChild(emailValue);
    div.appendChild(emailContainer);

    // Criação e adição do título e estado civil do usuário
    let NtelefoneContainer = document.createElement("div");
    let NtelefoneLabel = document.createElement("span");
    NtelefoneLabel.textContent = "Telefone: ";
    let NtelefoneValue = document.createElement("span");
    NtelefoneValue.textContent = user_Ntelefone;
    NtelefoneContainer.appendChild(NtelefoneLabel);
    NtelefoneContainer.appendChild(NtelefoneValue);
    div.appendChild(NtelefoneContainer);

    // Criação e adição do título e idade do usuário
    let idadeContainer = document.createElement("div");
    let idadeLabel = document.createElement("span");
    idadeLabel.textContent = "Idade: ";
    let idadeValue = document.createElement("span");
    idadeValue.textContent = user_idade;
    idadeContainer.appendChild(idadeLabel);
    idadeContainer.appendChild(idadeValue);
    div.appendChild(idadeContainer);

    // Criação e adição do título e cidade do usuário
    let cidadeContainer = document.createElement("div");
    let cidadeLabel = document.createElement("span");
    cidadeLabel.textContent = "Cidade: ";
    let cidadeValue = document.createElement("span");
    cidadeValue.textContent = user_cidade;
    cidadeContainer.appendChild(cidadeLabel);
    cidadeContainer.appendChild(cidadeValue);
    div.appendChild(cidadeContainer);


    let CPFContainer = document.createElement("div");
    let CPFLabel = document.createElement("span");
    CPFLabel.textContent = "CPF: ";
    let CPFValue = document.createElement("span");
    CPFValue.textContent = user_CPF;
    CPFContainer.appendChild(CPFLabel);
    CPFContainer.appendChild(CPFValue);
    div.appendChild(CPFContainer);

    // Adiciona o novo div ao contêiner na página
    document.querySelector(".container").appendChild(div);

    console.log('Nome:', user_nome);
    console.log('Email:', user_email);
    console.log('Foto:', user_foto);
    console.log('Nº Telefone:', user_Ntelefone);
    console.log('Idade:', user_idade);
    console.log('Cidade:', user_cidade);
    console.log('CPF:', user_CPF);

    // alert("Usuário logado");
} else {
    alert("Nenhum usuário logado");
    console.log('Nenhum usuário logado.');
}
