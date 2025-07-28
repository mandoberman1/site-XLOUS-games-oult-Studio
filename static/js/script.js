// Эфффект в index.ejs
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

// Список обновлений
let data
const page = document.querySelector('title').textContent
const result = page.replace(/\s+/g, '');
console.log(result);
document.addEventListener('DOMContentLoaded', ()=> {
    fetch('../../update-list.json')                       // 1
    .then(response => response.json())    // 2
    .then(data => {                        // 3
        console.log(data);
        let found = []
        data.forEach((item) => {
            if(item.name == result){
                item.text.forEach((textItem) => {
                    found.push(textItem)
                })
                
            }
            
        })
        console.log(found);
        
        let listUp = document.querySelector('.list-updates');
        
        found.forEach(function(item){
            listUp.innerHTML += `<p>${item}</p>`
        });
        
    })                                    // 5
    .catch(error => console.error(error)); // 6



})




