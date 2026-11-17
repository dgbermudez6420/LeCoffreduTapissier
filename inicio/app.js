'use strict';
const marquee = document.querySelector('.marquee');
if (marquee) {
  marquee.addEventListener('pointerdown', () => marquee.classList.add('touch-paused'));
  ['pointerup', 'pointercancel'].forEach(type => window.addEventListener(type, () => marquee.classList.remove('touch-paused')));
}
// Fallback lisible si le catalogue ne répond pas; aucun prix inventé.
setTimeout(function () {
  document.querySelectorAll('[data-main-price] .price-loading').forEach(function (el) {
    el.textContent = 'Tarif indisponible momentanément';
  });
}, 12000);
