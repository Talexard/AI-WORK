document.getElementById('year').textContent = new Date().getFullYear();

(function () {
  var items = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) { items.forEach(function (el) { el.classList.add('in'); }); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  items.forEach(function (el) { io.observe(el); });
})();

// Live open/closed status for each café (Arizona time). All open at 6am.
(function () {
  var parts = new Intl.DateTimeFormat('en-US', { timeZone: 'America/Phoenix', weekday: 'short', hour: 'numeric', minute: 'numeric', hour12: false }).formatToParts(new Date());
  var get = function (t) { var p = parts.find(function (x) { return x.type === t; }); return p ? p.value : ''; };
  var day = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(get('weekday'));
  var h = parseInt(get('hour'), 10) % 24 + parseInt(get('minute'), 10) / 60;
  if (day < 0 || isNaN(h)) return;
  var openCount = 0;
  document.querySelectorAll('.cafe').forEach(function (cafe) {
    var close = parseInt(cafe.getAttribute('data-close').split(',')[day], 10);
    var open = h >= 6 && h < close;
    if (open) openCount++;
    var s = cafe.querySelector('.status');
    s.textContent = open ? 'Open now · until ' + (close - 12) + 'pm' : 'Closed · opens 6am';
    s.classList.toggle('closed', !open);
  });
  document.getElementById('open-count').textContent = openCount ? openCount + ' cafés open now' : '3 cafés';
})();
