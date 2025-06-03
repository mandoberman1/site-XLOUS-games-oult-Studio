let card = document.querySelectorAll('.card-game');
let img = document.querySelectorAll('.card-game-img');
let text = document.querySelectorAll('.hide-text');
card.forEach((element, id) => {
    element.addEventListener('mouseover', () => {
        img[id].classList.add('card-game-img-hover')
        text[id].classList.add('hide-text-hover')
    })
    element.addEventListener('mouseout', () => {
        img[id].classList.remove('card-game-img-hover')
        text[id].classList.remove('hide-text-hover')
    })
})
let a = [
    'Версия 1.0 Создание игры',
    'Обновление 1.2 Исправление ошибок'
];

let listUp = document.querySelector('.list-updates');

a.forEach(function(item){
    listUp.innerHTML += `<p>${item}</p>`;
});

const btnEdit = document.querySelector('.edit_reg');
const btnSub = document.querySelector('.reg_in');
const form = document.querySelector('.form_reg_in');
const conPassword = document.querySelectorAll('.Con-Password')
const createpass = document.querySelector('.createpass')

btnEdit.addEventListener('click', () => {
  if (btnEdit.classList.contains('edit_reg')) {
    btnEdit.textContent = 'Перейти на регистрацию';
    btnSub.textContent = 'Вход';
    form.setAttribute('action', '/login');
    btnEdit.classList.remove('edit_reg');
    conPassword.forEach((i) => {
        i.style.visibility = 'hidden'
    })
    createpass.textContent = 'Password'
  } else {
    btnEdit.textContent = 'Перейти на вход';
    btnSub.textContent = 'Зарегистрироваться';
    form.setAttribute('action', '/register');
    btnEdit.classList.add('edit_reg');
    conPassword.forEach((i) => {
        i.style.visibility = 'visible'
    })
    createpass.textContent = 'Create password'
  }
});

const accImg = document.querySelector('.img-acc')
const autor = document.querySelector('.with_autor')
const lines = document.querySelector('.lines')

let hide = () => {
    autor.classList.toggle('hidden')
    
}

accImg.addEventListener('click', hide)
lines.addEventListener('click', hide)