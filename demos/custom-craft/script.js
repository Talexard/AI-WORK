// Keep the footer year current.
document.getElementById('year').textContent = new Date().getFullYear();

// DEMO ONLY: the form doesn't send anywhere yet.
// At launch, connect it to a form service (e.g. Netlify Forms or Formspree)
// so requests go to the owner's email or phone.
document.getElementById('estimate-form').addEventListener('submit', function (e) {
  e.preventDefault();
  document.getElementById('form-note').textContent =
    'Demo only: on the live site, this request goes straight to your phone and email.';
});
