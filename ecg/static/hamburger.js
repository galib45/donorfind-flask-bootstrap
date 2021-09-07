let burger = document.querySelector('#hamburger');
let list = document.querySelector('.nav-list');
let bar = document.querySelector('.navbar-container');

burger.onclick = () => {
  if (window.getComputedStyle(list).getPropertyValue('display')=='none') {
    list.style.display='flex';
  } else {
    list.style.display='none';
  }
}