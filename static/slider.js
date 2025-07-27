const slider = document.querySelector('.slider');
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');
let currentIndex = 0;

const firstSlide = slides[0].cloneNode(true);
const lastSlide = slides[slides.length - 1].cloneNode(true);

slider.appendChild(firstSlide);
slider.insertBefore(lastSlide, slides[0]);

let totalSlides = slides.length + 2;
slider.style.transform = `translateX(-100%)`;

function updateSlider() {
    slider.style.transition = 'transform 0.9s ease-out';
    slider.style.transform = `translateX(-${(currentIndex + 1) * 100}%)`;

    updateDots();
}

function updateDots() {
    dots.forEach((dot, index) => {
        dot.classList.toggle('active', index === currentIndex);
    });
}

function moveToSlide(index) {
    currentIndex = index;
    updateSlider();
}

slider.addEventListener('transitionend', () => {
    if (currentIndex === -1) {
        slider.style.transition = 'none';
        currentIndex = slides.length - 1;
        slider.style.transform = `translateX(-${(currentIndex + 1) * 100}%)`;
    } else if (currentIndex === slides.length) {
        slider.style.transition = 'none';
        currentIndex = 0;
        slider.style.transform = `translateX(-100%)`;
    }
    setTimeout(() => slider.style.transition = 'transform 0.9s ease-out', 10);
    updateDots();
});

dots.forEach((dot, index) => {
    dot.addEventListener('click', () => moveToSlide(index));
});

setInterval(() => {
    moveToSlide(currentIndex + 1);
}, 5000);

updateDots();
