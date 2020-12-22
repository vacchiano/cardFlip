// tablet/mobile menu dropdown
//console.log(('hello'));

let burgerIcon = document.querySelector('#burger');
let navbarMenu = document.querySelector('#nav-links');

burgerIcon.addEventListener('click', () => {
    navbarMenu.classList.toggle('is-active');
});