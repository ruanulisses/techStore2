document.addEventListener('DOMContentLoaded', (event) => {
    const checkbox = document.getElementById('color_mode');

    // Verificar o estado salvo no localStorage e aplicar o modo escuro se necessário
    if (localStorage.getItem('dark-mode') === 'enabled') {
        document.body.classList.add('dark-mode');
        document.querySelector('nav.menu_lateral').classList.add('dark-mode');
        document.querySelector('body').classList.add('dark-mode');
        checkbox.checked = true;
    }

    checkbox.addEventListener('click', function() {
        if (checkbox.checked) {
            document.body.classList.add('dark-mode');
            document.querySelector('nav.menu_lateral').classList.add('dark-mode');
            localStorage.setItem('dark-mode', 'enabled');
        } else {
            document.body.classList.remove('dark-mode');
            document.querySelector('nav.menu_lateral').classList.remove('dark-mode');
            localStorage.setItem('dark-mode', 'disabled');
        }
    });
});