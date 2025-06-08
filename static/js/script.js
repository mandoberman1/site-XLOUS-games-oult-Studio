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



const accImg = document.querySelector('.img-acc')
const autor = document.querySelector('.with_autor')
const lines = document.querySelector('.lines')

let hide = () => {
    autor.classList.toggle('hidden')
    
}

accImg.addEventListener('click', hide)
lines.addEventListener('click', hide)

let hideIp = document.querySelector('.hide-ip')
normIp = hideIp.textContent
hideIp.textContent = 'Your ip: ***:***:***'


function showIp(){
    hideIp.textContent = normIp
}

let allIp = document.querySelector('.allIp').value.split(',')
let currentIp = normIp.replace('Your ip: ', '')
let form = document.querySelector('.comment-form')

allIp.forEach((el) => {
    if(el == currentIp){
        form.remove()
    }
})
