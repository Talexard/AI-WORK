document.getElementById('year').textContent = new Date().getFullYear();

(function () {
  var items = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) { items.forEach(function (el) { el.classList.add('in'); }); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  items.forEach(function (el) { io.observe(el); });
})();

// Highlight today's row on the lineup board (Arizona time).
(function () {
  var wd = new Intl.DateTimeFormat('en-US', { timeZone: 'America/Phoenix', weekday: 'short' }).format(new Date());
  var day = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(wd);
  var row = document.querySelector('.board li[data-day="' + day + '"]');
  if (row) row.classList.add('today');
})();
