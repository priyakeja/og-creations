document.addEventListener('DOMContentLoaded', function () {

  // ---------- Scroll reveal (used by upcoming sections) ----------
  var items = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-zoom');

  items.forEach(function (el) {
    var delay = el.getAttribute('data-delay');
             if (delay) el.style.transitionDelay = (parseInt(delay, 10) * 1.3) + 'ms';
  });

  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    items.forEach(function (el) { observer.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('is-visible'); });
  }

  // ---------- Elements used on scroll ----------
  var bar = document.getElementById('scroll-progress');
  var navbar = document.getElementById('og-navbar');
  var navLinks = document.querySelectorAll('.og-nav .nav-link');
  var heroBg = document.querySelector('[data-parallax]');
  var heroContent = document.querySelector('[data-hero-content]');
  var hero = document.getElementById('home');
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function updateActiveLink() {
    if (window.scrollY < 60) {
      navLinks.forEach(function (l) { l.classList.remove('active'); });
      return;
    }
    var pos = window.scrollY + 140;
    var current = null;
    navLinks.forEach(function (link) {
      var href = link.getAttribute('href') || '';
      if (href.length > 1 && href.charAt(0) === '#') {
        try {
          var sec = document.querySelector(href);
          if (sec && sec.offsetTop <= pos) current = link;
        } catch (e) {}
      }
    });
    navLinks.forEach(function (l) { l.classList.remove('active'); });
    if (current) current.classList.add('active');
  }

  function onScroll() {
    var y = window.scrollY;
    var h = document.documentElement;

    // progress bar
    if (bar) bar.style.width = (y / (h.scrollHeight - h.clientHeight)) * 100 + '%';

    // navbar shrink
    if (navbar) navbar.classList.toggle('is-scrolled', y > 40);

    

    updateActiveLink();
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // ---------- Close mobile menu after clicking a link ----------
  var collapseEl = document.getElementById('ogNav');
  navLinks.forEach(function (link) {
    link.addEventListener('click', function () {
      if (collapseEl && collapseEl.classList.contains('show')) {
        bootstrap.Collapse.getOrCreateInstance(collapseEl).hide();
      }
    });
  });

});