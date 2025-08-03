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
    $.getJSON("../update-list.json")
    .done(function( data ) {
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

// slider
document.addEventListener('DOMContentLoaded', function() {
            const slider = document.querySelector('.slider');
            const slides = document.querySelectorAll('.slide');
            const prevBtn = document.querySelector('.prev');
            const nextBtn = document.querySelector('.next');
            const indicators = document.querySelectorAll('.indicator');
            
            let currentIndex = 0;
            const slideCount = slides.length;
            
            // Функция для обновления слайдера
            function updateSlider() {
                slider.style.transform = `translateX(-${currentIndex * 100}%)`;
                
                // Обновление активного класса для слайдов
                slides.forEach((slide, index) => {
                    slide.classList.toggle('active', index === currentIndex);
                });
                
                // Обновление индикаторов
                indicators.forEach((indicator, index) => {
                    indicator.classList.toggle('active', index === currentIndex);
                });
            }
            
            // Переход к следующему слайду
            function nextSlide() {
                currentIndex = (currentIndex + 1) % slideCount;
                updateSlider();
            }
            
            // Переход к предыдущему слайду
            function prevSlide() {
                currentIndex = (currentIndex - 1 + slideCount) % slideCount;
                updateSlider();
            }
            
            // Автоматическое перелистывание
            let slideInterval = setInterval(nextSlide, 3000);
            
            // Остановка авто-перелистывания при наведении
            slider.addEventListener('mouseenter', () => {
                clearInterval(slideInterval);
            });
            
            // Возобновление авто-перелистывания при уходе курсора
            slider.addEventListener('mouseleave', () => {
                slideInterval = setInterval(nextSlide, 3000);
            });
            
            // Обработчики кнопок
            nextBtn.addEventListener('click', nextSlide);
            prevBtn.addEventListener('click', prevSlide);
            
            // Обработчики индикаторов
            indicators.forEach((indicator, index) => {
                indicator.addEventListener('click', () => {
                    currentIndex = index;
                    updateSlider();
                });
            });
            
            // Обработчики клавиатуры
            document.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowRight') {
                    nextSlide();
                } else if (e.key === 'ArrowLeft') {
                    prevSlide();
                }
            });
            
            // Инициализация слайдера
            updateSlider();
        });




