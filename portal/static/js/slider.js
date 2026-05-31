let currentIndex = 0;
let slides = [];
let autoInterval = null;

function initSlider() {
    slides = document.querySelectorAll('.slide');
    if (slides.length === 0) return;

    currentIndex = 0;
    showSlide(currentIndex);

    if (autoInterval) clearInterval(autoInterval);
    autoInterval = setInterval(nextSlide, 3000);
}

function showSlide(index) {
    if (slides.length === 0) return;

    slides.forEach(function(slide) {
        slide.classList.remove('active');
    });

    if (index < 0) index = slides.length - 1;
    if (index >= slides.length) index = 0;
    currentIndex = index;

    slides[currentIndex].classList.add('active');
}

function nextSlide() {
    showSlide(currentIndex + 1);
}

function prevSlide() {
    showSlide(currentIndex - 1);
}

document.addEventListener('DOMContentLoaded', initSlider);