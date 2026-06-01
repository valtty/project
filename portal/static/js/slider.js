var currentSlide = 0;
var slides = [];
var timer = null;

function showSlide(n) {
    if (!slides.length) return;
    if (n >= slides.length) currentSlide = 0;
    else if (n < 0) currentSlide = slides.length - 1;
    else currentSlide = n;

    for (var i = 0; i < slides.length; i++) {
        slides[i].classList.remove('active');
    }
    slides[currentSlide].classList.add('active');
}

function nextSlide() {
    showSlide(currentSlide + 1);
}

function prevSlide() {
    showSlide(currentSlide - 1);
}

function startTimer() {
    if (timer) clearInterval(timer);
    timer = setInterval(nextSlide, 3000);
}

document.addEventListener('DOMContentLoaded', function () {
    slides = document.querySelectorAll('.slide');
    if (slides.length === 0) return;
    showSlide(0);
    startTimer();
});
