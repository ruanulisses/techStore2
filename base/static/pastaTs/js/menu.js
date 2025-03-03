

//expandir manu


var btn_exp = document.querySelector('#btn_exp')
var menu_side = document.querySelector('.menu_lateral')

btn_exp.addEventListener('click', function(){
    menu_side.classList.toggle('expandir')
})


function toggleExpand() {
    var box = document.getElementById('btn_expandir');
    box.classList.toggle('expanded');
}