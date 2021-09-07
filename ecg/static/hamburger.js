let burger = document.querySelector('#hamburger');
let list = document.querySelector('.nav-list');
let bar = document.querySelector('.navbar-container');

burger.addEventListener('click',e=>{
  if (window.getComputedStyle(list).getPropertyValue('display')=='none') {
    list.style.display='flex';
    list.style.justifyContent = 'left';
    bar.style.flexDirection = 'column'
  }
  else list.style.display='none';
})

window.addEventListener('resize', e=>{
  if (window.innerWidth > 700) {
    list.style.display='flex';
    list.style.justifyContent = 'right';
    bar.style.flexDirection = 'row';
    bar.style.justifyContent =  'space-between';
  }
  else {
    list.style.display = 'none';
    bar.style.flexDirection = 'column'
  }
})