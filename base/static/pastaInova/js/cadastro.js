const formCadastro = document.getElementById('cadastro-form');
const errorMessage = document.getElementById('error-message');

formCadastro.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const novoNome = document.getElementById('novo_nome').value;
    const novoFoto = document.getElementById('novo_foto').value;
    const novoNumero = document.getElementById('novo_numero').value;
    const novoEmail = document.getElementById('novo_email').value;
    const novaCidade = document.getElementById('novo_cidade').value;
    const novoCPF = document.getElementById('novo_CPF').value;
    const novoIdade = document.getElementById('novo_idade').value;
    const novaSenha = document.getElementById('nova_senha').value;

    if (novoNome === '' || novoFoto === '' || novoNumero === '' || novoEmail === '' || novaCidade === '' || novoCPF === '' || novoIdade === '' || novaSenha === '') {
        errorMessage.textContent = 'Preencha todos os campos!';
        errorMessage.style.color = 'red';
        return;
    }

    // Adicionar novo usuário ao array validUsers
    const novoId = `user_${validUsers.length + 1}`;
    const novoUsuario = {
        id: novoId,
        nome: novoNome,
        foto: novoFoto,
        Ntelefone: novoNumero,
        email: novoEmail,
        cidade: novaCidade,
        CPF: novoCPF,
        idade: parseInt(novoIdade),
        senha: novaSenha
    };
    validUsers.push(novoUsuario);

    // Salvar o novo usuário no localStorage
    localStorage.setItem('validUsers', JSON.stringify(validUsers));

    errorMessage.textContent = 'Usuário adicionado com sucesso!';
    errorMessage.style.color = 'green';

    formCadastro.reset();
});