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
});
let a = document.querySelector('.function_comment')

let b = [214, 216, 216, 217, 218, 218, 218, 219, 220, 220, 220, 221, 222, 223, 224, 225, 225, 225, 225, 227, 227, 228, 228, 228, 231];

// Используем метод reduce для суммирования всех элементов массива
let sum = b.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

console.log(sum); // Выводим сумму
