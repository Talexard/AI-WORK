document.getElementById('year').textContent = new Date().getFullYear();

// Reveal on scroll (also starts the gauge animation).
(function () {
  var items = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) { items.forEach(function (el) { el.classList.add('in'); }); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
  items.forEach(function (el) { io.observe(el); });
})();

// Open/closed status using Arizona time. Mon–Fri 7:30–18:00, Sat 8:00–15:00, Sun closed.
(function () {
  var parts = new Intl.DateTimeFormat('en-US', { timeZone: 'America/Phoenix', weekday: 'short', hour: 'numeric', minute: 'numeric', hour12: false }).formatToParts(new Date());
  var get = function (t) { var p = parts.find(function (x) { return x.type === t; }); return p ? p.value : ''; };
  var day = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(get('weekday'));
  var h = parseInt(get('hour'), 10) % 24 + parseInt(get('minute'), 10) / 60;
  if (day < 0 || isNaN(h)) return;
  var hours = day === 0 ? null : day === 6 ? [8, 15] : [7.5, 18];
  var open = hours && h >= hours[0] && h < hours[1];
  var fmt = function (x) { var hr = Math.floor(x), m = x % 1 ? ':30' : ''; return (hr > 12 ? hr - 12 : hr) + m + (hr >= 12 ? 'pm' : 'am'); };
  var line = open ? 'Both shops open now · until ' + fmt(hours[1]) : 'Closed now · towing available 24/7';
  document.getElementById('status-line').textContent = line;
  document.querySelector('.live').classList.toggle('closed', !open);
  document.querySelectorAll('.hours dl div').forEach(function (row) {
    if (row.getAttribute('data-days').split(',').indexOf(String(day)) > -1) row.classList.add('today');
  });
})();

// DEMO ONLY: form isn't connected yet. At launch, connect to Netlify Forms / Formspree.
document.getElementById('book-form').addEventListener('submit', function (e) {
  e.preventDefault();
  document.getElementById('form-note').textContent = 'Demo only: on the live site, this request goes straight to the shop you picked.';
});
