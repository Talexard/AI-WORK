// Fade sections in as they scroll into view.
(function () {
  var items = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) { items.forEach(function (el) { el.classList.add('in'); }); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  items.forEach(function (el) { io.observe(el); });
})();

// Menu tabs.
(function () {
  var tabs = Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));
  function select(tab) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { select(t); });
    t.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        var next = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length];
        select(next); next.focus();
      }
    });
  });
})();

// "Open now" badge, using Arizona time (no daylight saving).
(function () {
  // Parlor hours: opens 11:00. Closes 22:00 Sun–Thu, 23:00 Fri–Sat.
  var closeHour = { 0: 22, 1: 22, 2: 22, 3: 22, 4: 22, 5: 23, 6: 23 };
  var parts = new Intl.DateTimeFormat('en-US', { timeZone: 'America/Phoenix', weekday: 'short', hour: 'numeric', minute: 'numeric', hour12: false }).formatToParts(new Date());
  var get = function (type) { var p = parts.find(function (x) { return x.type === type; }); return p ? p.value : ''; };
  var day = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(get('weekday'));
  var hour = parseInt(get('hour'), 10) % 24 + parseInt(get('minute'), 10) / 60;
  if (day < 0 || isNaN(hour)) return;
  var close = closeHour[day];
  var open = hour >= 11 && hour < close;
  var fmt = function (h) { return (h > 12 ? h - 12 : h) + (h >= 12 ? 'pm' : 'am'); };
  var label = open ? 'Open now · until ' + fmt(close) : (hour < 11 ? 'Opens today at 11am' : 'Closed · opens 11am');
  ['open-pill', 'open-pill-2'].forEach(function (id) {
    var el = document.getElementById(id); if (!el) return;
    el.classList.toggle('closed', !open);
    el.querySelector('.open-text').textContent = label;
  });
  var today = document.getElementById('today-hours');
  if (today) today.textContent = 'Today: 11am – ' + fmt(close);
  var row = document.querySelector('.hours tr[data-day="' + day + '"]');
  if (row) row.classList.add('today');
})();
