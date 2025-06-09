function applyResponsiveClass() {
    const body = document.body;
    const width = window.visualViewport ? window.visualViewport.width : window.innerWidth;
    const isTouchLandscape = window.matchMedia("(orientation: landscape) and (pointer: coarse)").matches;

    body.classList.remove('mobile-layout', 'medium-layout', 'default-layout');

    if (width <= 768) {
        body.classList.add('mobile-layout');
    } else if (width > 768 && isTouchLandscape) {
        body.classList.add('mobile-layout');
    } else if (width > 768 && width < 1200) {
        body.classList.add('medium-layout');
    } else {
        body.classList.add('default-layout');
    }
}

window.addEventListener('load', () => {
    // Delay to let viewport settle
    setTimeout(applyResponsiveClass, 100);
});

window.addEventListener('resize', applyResponsiveClass);

// Run on initial load
window.addEventListener('DOMContentLoaded', applyResponsiveClass);

// Run on orientation change
window.addEventListener('orientationchange', () => {
    setTimeout(applyResponsiveClass, 50);
});

// Run on resize
window.addEventListener('resize', () => {
    setTimeout(applyResponsiveClass, 50);
});


const navToggle = document.getElementById('nav-toggle');
const navMenu = document.getElementById('nav-menu');

navToggle.addEventListener('click', () => {
    const isExpanded = navToggle.getAttribute('aria-expanded') === 'true';
    navToggle.setAttribute('aria-expanded', !isExpanded);
    navMenu.classList.toggle('show');
});