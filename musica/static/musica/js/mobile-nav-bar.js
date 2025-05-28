const mobileMenus = document.querySelectorAll('.mobile-menu');
const navLists = document.querySelectorAll('.nav-list');
const closeButtons = document.querySelectorAll('.close-menu');

const header = document.querySelector('header');
const main = document.querySelector('main');
const footer = document.querySelector('footer');

mobileMenus.forEach((mobileMenu, index) => {
    mobileMenu.addEventListener('click', () => {
        navLists[index].classList.toggle('active');
        header.classList.toggle('active');
        main.classList.toggle('none');
        footer.classList.toggle('none');
    });
});

closeButtons.forEach((closeButton, index) => {
    closeButton.addEventListener('click', () => {
        navLists[index].classList.remove('active');
        header.classList.remove('active');
        main.classList.remove('none');
        footer.classList.remove('none');
    });
});