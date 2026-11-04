// Keep the footer year current.
document.getElementById('year').textContent = new Date().getFullYear();

// Fade sections in as they scroll into view, and draw the blueprint house.
(function () {
  var items = document.querySelectorAll('.reveal, .draw');
  if (!('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  items.forEach(function (el) { io.observe(el); });
})();

// DEMO ONLY: the form doesn't send anywhere yet.
// At launch, connect it to a form service (e.g. Netlify Forms or Formspree)
// so requests go to the owner's email or phone.
document.getElementById('estimate-form').addEventListener('submit', function (e) {
  e.preventDefault();
  document.getElementById('form-note').textContent =
    'Demo only: on the live site, this request goes straight to your phone and email.';
});
