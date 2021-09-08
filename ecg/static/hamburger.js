let burger = document.querySelector('#hamburger');
let list = document.querySelector('.nav-list');

burger.onclick = () => {
    if (window.getComputedStyle(list).getPropertyValue('display') == 'none') {
        list.style.display = 'flex';
    } else {
        list.style.display = 'none';
    }
}

window.addEventListener('resize', e => {
    if (window.innerWidth > 700) {
        list.style.display = 'flex';
    } else {
        list.style.display = 'none';
    }
})