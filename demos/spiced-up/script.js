document.getElementById('year').textContent = new Date().getFullYear();
(function () {
  var items = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) { items.forEach(function (el) { el.classList.add('in'); }); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  items.forEach(function (el) { io.observe(el); });
})();
// Spice chips toggle.
document.querySelectorAll('.chips button').forEach(function (b) {
  b.addEventListener('click', function () { b.classList.toggle('on'); });
});
// Open status (Arizona time). Mon closed; Tue–Fri 8–18; Sat 9–18; Sun 9–17.
(function () {
  var hrs = { 0: [9, 17], 1: null, 2: [8, 18], 3: [8, 18], 4: [8, 18], 5: [8, 18], 6: [9, 18] };
  var parts = new Intl.DateTimeFormat('en-US', { timeZone: 'America/Phoenix', weekday: 'short', hour: 'numeric', minute: 'numeric', hour12: false }).formatToParts(new Date());
  var get = function (t) { var p = parts.find(function (x) { return x.type === t; }); return p ? p.value : ''; };
  var day = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(get('weekday'));
  var h = parseInt(get('hour'), 10) % 24 + parseInt(get('minute'), 10) / 60;
  if (day < 0 || isNaN(h)) return;
  var t = hrs[day], open = t && h >= t[0] && h < t[1];
  document.getElementById('open-text').textContent = open ? 'Open · until ' + (t[1] - 12) + 'pm' : (day === 1 ? 'Closed Mondays' : 'Closed now');
  document.getElementById('open-pill').classList.toggle('closed', !open);
  document.querySelectorAll('.hours dl div').forEach(function (row) {
    if (row.getAttribute('data-d').split(',').indexOf(String(day)) > -1) row.classList.add('today');
  });
})();
