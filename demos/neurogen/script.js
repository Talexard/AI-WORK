document.getElementById('year').textContent = new Date().getFullYear();
(function () {
  var items = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) { items.forEach(function (el) { el.classList.add('in'); }); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  items.forEach(function (el) { io.observe(el); });
})();
// Open status (Arizona time): Mon–Fri 9:30–4:30.
(function () {
  var parts = new Intl.DateTimeFormat('en-US', { timeZone: 'America/Phoenix', weekday: 'short', hour: 'numeric', minute: 'numeric', hour12: false }).formatToParts(new Date());
  var get = function (t) { var p = parts.find(function (x) { return x.type === t; }); return p ? p.value : ''; };
  var day = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(get('weekday'));
  var h = parseInt(get('hour'), 10) % 24 + parseInt(get('minute'), 10) / 60;
  var open = day >= 1 && day <= 5 && h >= 9.5 && h < 16.5;
  var el = document.getElementById('open-line');
  el.textContent = open ? 'Open now · until 4:30pm' : 'Closed now · call to book';
  el.classList.toggle('closed', !open);
})();
// DEMO ONLY: connect the form at launch.
document.getElementById('book-form').addEventListener('submit', function (e) {
  e.preventDefault();
  document.getElementById('form-note').textContent = 'Demo only: on the live site, this request goes straight to Neurogen.';
});
