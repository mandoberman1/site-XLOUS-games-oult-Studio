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
