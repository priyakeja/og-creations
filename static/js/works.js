document.addEventListener('DOMContentLoaded', function () {

  var grid = document.getElementById('worksGrid');
  if (!grid) return;

  var cards = Array.prototype.slice.call(grid.querySelectorAll('.work-card'));
  var buttons = document.querySelectorAll('.works__filter');
  var current = 'all';
  var busy = false;

  // ---------- Filter tabs ----------
  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var key = btn.getAttribute('data-filter');
      if (busy || key === current) return;
      current = key;
      busy = true;

      buttons.forEach(function (b) { b.classList.toggle('is-active', b === btn); });

      // fade the grid out, rearrange, fade it back in with a stagger
      grid.classList.add('is-switching');
      setTimeout(function () {
        var n = 0;
        cards.forEach(function (card) {
          var show = key === 'all' || card.getAttribute('data-cat') === key;
          card.hidden = !show;
          card.classList.remove('is-large', 'is-pop');
          if (show) {
            card.classList.add('is-visible');
            if (n === 0) card.classList.add('is-large');
            card.style.setProperty('--pop-d', (n * 0.12) + 's');
            n++;
          }
        });
        void grid.offsetWidth; // restart animation
        cards.forEach(function (card) {
          if (!card.hidden) card.classList.add('is-pop');
        });
        grid.classList.remove('is-switching');
        busy = false;
      }, 450);
    });
  });

  // ---------- Video popup ----------
  var modal = document.getElementById('videoModal');
  var frame = document.getElementById('videoFrame');

  function toEmbed(url) {
    var m = url.match(/(?:youtube\.com\/(?:watch\?v=|embed\/|shorts\/)|youtu\.be\/)([\w-]{11})/);
    if (m) return { type: 'iframe', src: 'https://www.youtube.com/embed/' + m[1] + '?autoplay=1&rel=0' };
    m = url.match(/vimeo\.com\/(?:video\/)?(\d+)/);
    if (m) return { type: 'iframe', src: 'https://player.vimeo.com/video/' + m[1] + '?autoplay=1' };
    if (/\.(mp4|webm|ogg)(\?.*)?$/i.test(url)) return { type: 'video', src: url };
    return { type: 'link', src: url };
  }

  function openModal(url) {
    var v = toEmbed(url);
    if (v.type === 'link') { window.open(url, '_blank', 'noopener'); return; }
    frame.innerHTML = '';
    var el;
    if (v.type === 'video') {
      el = document.createElement('video');
      el.src = v.src;
      el.controls = true;
      el.autoplay = true;
      el.setAttribute('playsinline', '');
    } else {
      el = document.createElement('iframe');
      el.src = v.src;
      el.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      el.allowFullscreen = true;
      el.title = 'Project video';
    }
    frame.appendChild(el);
    modal.classList.add('is-open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    modal.classList.remove('is-open');
    modal.setAttribute('aria-hidden', 'true');
    frame.innerHTML = ''; // stops the video
    document.body.style.overflow = '';
  }

  cards.forEach(function (card) {
    var url = card.getAttribute('data-video');
    if (!url) return;
    card.addEventListener('click', function () { openModal(url); });
    card.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openModal(url); }
    });
  });

  if (modal) {
    modal.querySelectorAll('[data-close]').forEach(function (el) {
      el.addEventListener('click', closeModal);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && modal.classList.contains('is-open')) closeModal();
    });
  }

});