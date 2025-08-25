
const form = document.getElementById('login-form');
const errorMessage = document.getElementById('error-message');

// Lista de usuários válidos
const defaultUsers = [
    // { id: 'user_1', nome: 'admin', email: 'admin@gmail.com', senha: 'admin', foto:'/fotos/user-png-icon-big-image-png-2240.png', Ntelefone: '77 993423212', idade: 20, cidade: 'Bom Jesus da Lapa', CPF: '412.312.412.09' },
    // { id: 'user_2', nome: 'Ruan Ulisses', email: 'ruanba2@gmail.com', senha: '123', foto:'/fotos/IMG_20230407_201357.jpg', Ntelefone: '77 993423212', idade: 20, cidade: 'Bom Jesus da Lapa', CPF: '412.312.412.09' },
    // { id: 'user_3', nome:'Luan santos', email: 'luansantos@gmail.com', senha: '123', foto:'https://media-gru1-2.cdn.whatsapp.net/v/t61.24694-24/420105544_8042185889221868_493583484032481042_n.jpg?ccb=11-4&oh=01_Q5AaIBmU6eXej9yIkq5FX_ldYqiH3-lKdMlpYn1kW8ri5s-Q&oe=66BD10F5&_nc_sid=e6ed6c&_nc_cat=111', Ntelefone: '77 993423212', idade: 19, cidade: 'Bom Jesus da Lapa', CPF: '412.312.412.09' },
    // { id: 'user_4', nome: 'Joelson', email: 'joelson@gmail.com', senha: '123', foto:'https://suap.ifbaiano.edu.br/media/alunos/23486.mdNwDRA2Wxja.jpg', Ntelefone: '77 993423212', idade: 22, cidade: 'Serra do Ramalho', CPF: '412.312.412.09' },
    // { id: 'user_5', nome: 'Daniele', email: 'daniele@gmail.com', senha: '123', foto:'https://suap.ifbaiano.edu.br/media/fotos/75x100/17327.TrEl2PCB7_qX.jpg', Ntelefone: '77 993423212', idade: 32, cidade: 'Bom Jesus da Lapa', CPF: '412.312.412.09' },
    // { id: 'user_6', nome: 'Mariana', email: 'Mariana@gmail.com', senha: '123', foto:'/fotos/image.jpg', Ntelefone: '77 993423212', idade: 80, cidade: 'Serra do Ramalho', CPF: '412.312.412.09' }
];

// Função para carregar usuários do localStorage
function loadUsers() {
    let users = JSON.parse(localStorage.getItem('validUsers')) || [];
    // Adiciona usuários padrão se localStorage estiver vazio
    if (users.length === 0) {
        users = defaultUsers;
        localStorage.setItem('validUsers', JSON.stringify(users));
    }

    return users;
}

form.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;

    // Verificar se os campos estão preenchidos
    if (email === '' || senha === '') {
        errorMessage.textContent = 'Preencha todos os campos!';
        return;
    }

    // Carregar usuários do localStorage (ou lista padrão se vazio)
    const validUsers = loadUsers();
    console.log('Usuários carregados:', validUsers); // Debug

    // Verificar se o usuário é válido
    const user = validUsers.find(user => user.email === email && user.senha === senha);
    console.log('Usuário encontrado:', user); // Debug

    if (!user) {
        errorMessage.textContent = 'Usuário ou senha inválidos!';
        return;
    }

    // Armazenar o ID do usuário no Local Storage
    localStorage.setItem('userId', user.id);

    // Armazenar outros dados do usuário no Local Storage
    localStorage.setItem('userName', user.nome);
    localStorage.setItem('userEmail', user.email);
    localStorage.setItem('userPhoto', user.foto);
    localStorage.setItem('userNtelefone', user.Ntelefone);
    localStorage.setItem('userIdade', user.idade);
    localStorage.setItem('userCidade', user.cidade);
    localStorage.setItem('userCPF', user.CPF);

    // Redirecionar baseado no tipo de usuário
    if (user.nome === 'admin') {
        window.location.href = "{% url 'blog/index' %}"; // Redireciona para a página do administrador
    } else {
        // Redirecionar para a página principal
        window.location.href = "{% url 'home/index' %}";
    }
});
/*--------------------cadastra usuario ----------------------------------------------------------------------*/
