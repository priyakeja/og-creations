document.addEventListener('DOMContentLoaded', function () {

  // Email link: on desktop open Gmail compose in the browser, on phones use the Mail app
    document.querySelectorAll('a[data-gmail]').forEach(function (mailLink) {
    mailLink.addEventListener('click', function (e) {
      if (/Android|iPhone|iPad|iPod/i.test(navigator.userAgent)) return;
      e.preventDefault();
      window.open(mailLink.getAttribute('data-gmail'), '_blank', 'noopener');
    });
  });

  var form = document.getElementById('contactForm');
  if (!form) return;

  var card = form.closest('.contact__card');
  var success = document.getElementById('cfSuccess');
  var again = document.getElementById('cfAgain');
  var waLink = document.getElementById('cfWhatsapp');
  var alertBox = document.getElementById('cfAlert');
  var btn = form.querySelector('.cf-submit');
  var names = ['name', 'phone', 'email', 'service', 'details'];
  var touched = {};

  function field(n) { return form.querySelector('[data-field="' + n + '"]'); }
  function input(n) { return form.elements[n]; }

  function setError(n, msg) {
    field(n).classList.toggle('has-error', !!msg);
    field(n).querySelector('.cf-error').textContent = msg || '';
    input(n).setAttribute('aria-invalid', msg ? 'true' : 'false');
  }

  // ---------- Validation rules ----------
  var rules = {
    name: function (v) {
      v = v.trim().replace(/\s+/g, ' ');
      if (!v) return 'Please enter your full name.';
      if (/\d/.test(v)) return 'Name should not contain numbers.';
      if (!/^[\p{L}\p{M} .'\-]+$/u.test(v)) return 'Name can contain letters only.';
      if ((v.match(/\p{L}/gu) || []).length < 3) return 'Name must be at least 3 characters.';
      return '';
    },
    phone: function (v) {
      if (!v) return 'Please enter your phone number.';
      if (!/^\d{10}$/.test(v)) return 'Enter a valid 10-digit phone number (without +91).';
      return '';
    },
    email: function (v) {
      v = v.trim();
      if (!v) return 'Please enter your email address.';
      if (!/^[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}$/.test(v)) {
        return 'Enter a valid email address.';
      }
      return '';
    },
    service: function (v) {
      return v ? '' : 'Please select a service.';
    },
    details: function (v) {
      v = v.trim();
      if (!v) return 'Please share your project details.';
      if (v.length < 10) return 'Please add a little more detail (at least 10 characters).';
      return '';
    }
  };

  // validate on blur, then live while typing
  names.forEach(function (n) {
    var el = input(n);
    el.addEventListener('blur', function () {
      touched[n] = true;
      setError(n, rules[n](el.value));
    });
    el.addEventListener(n === 'service' ? 'change' : 'input', function () {
      if (touched[n]) setError(n, rules[n](el.value));
    });
  });

  // name: numbers and symbols cannot be typed
  var nameEl = input('name');
  nameEl.addEventListener('input', function () {
    var cleaned = nameEl.value.replace(/[^\p{L}\p{M} .'\-]/gu, '');
    if (cleaned !== nameEl.value) {
      nameEl.value = cleaned;
      setError('name', 'Only letters are allowed in the name.');
    }
  });

  // phone: digits only, max 10 (a pasted +91 / 0 prefix is removed)
  var phoneEl = input('phone');
  phoneEl.addEventListener('input', function () {
    var d = phoneEl.value.replace(/\D/g, '');
    if (d.length === 12 && d.indexOf('91') === 0) d = d.slice(2);
    else if (d.length === 11 && d.charAt(0) === '0') d = d.slice(1);
    phoneEl.value = d.slice(0, 10);
  });

  // ---------- Helpers ----------
  function showAlert(msg) {
    alertBox.textContent = msg;
    alertBox.hidden = false;
  }
  function hideAlert() { alertBox.hidden = true; }

  function setLoading(on) {
    btn.classList.toggle('is-loading', on);
    btn.disabled = on;
  }

  function shake(n) {
    var f = field(n);
    f.classList.remove('is-shake');
    void f.offsetWidth;
    f.classList.add('is-shake');
    setTimeout(function () { f.classList.remove('is-shake'); }, 600);
  }

  function showSuccess(data, waWin) {
    var url = data.whatsapp_url;
    if (url && waWin) {
      waWin.location.href = url;          // WhatsApp opens with the message ready
      waLink.hidden = true;
    } else {
      if (waWin) waWin.close();
      if (url) { waLink.href = url; waLink.hidden = false; }  // fallback button
      else { waLink.hidden = true; }
    }
    form.hidden = true;
    success.hidden = false;
    success.classList.remove('is-show');
    void success.offsetWidth;
    success.classList.add('is-show');
    card.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  // ---------- Submit ----------
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    hideAlert();

    var firstBad = null;
    names.forEach(function (n) {
      touched[n] = true;
      var msg = rules[n](input(n).value);
      setError(n, msg);
      if (msg) { shake(n); if (!firstBad) firstBad = n; }
    });
    if (firstBad) { input(firstBad).focus(); return; }

    // open the tab now (inside the click) so the browser does not block it
    var waWin = null;
    try {
      waWin = window.open('', '_blank');
      if (waWin) {
        waWin.document.write('<p style="font-family:sans-serif;padding:2rem;color:#8D2236">Opening WhatsApp&hellip;</p>');
      }
    } catch (err) { waWin = null; }

    setLoading(true);

// always send the CURRENT csrf cookie value, so a stale page token cannot fail
    var fd = new FormData(form);
    var csrfMatch = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
    if (csrfMatch) fd.delete('csrfmiddlewaretoken');

    fetch(form.action, {
      method: 'POST',
      body: fd,
      credentials: 'same-origin',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrfMatch ? decodeURIComponent(csrfMatch[1]) : ''
      }
    })
      .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
      .then(function (res) {
        setLoading(false);
        if (res.ok && res.d.ok) {
          showSuccess(res.d, waWin);
        } else {
          if (waWin) waWin.close();
          var errs = (res.d && res.d.errors) || {};
          var bad = null;
          Object.keys(errs).forEach(function (k) {
            if (field(k)) { setError(k, errs[k]); shake(k); if (!bad) bad = k; }
          });
          if (bad) input(bad).focus();
          else showAlert('Something went wrong. Please try again or call us.');
        }
      })
      .catch(function () {
        setLoading(false);
        if (waWin) waWin.close();
        showAlert('Could not send your enquiry. Please check your connection and try again.');
      });
  });

  // ---------- Send another enquiry ----------
  again.addEventListener('click', function () {
    form.reset();
    touched = {};
    names.forEach(function (n) { setError(n, ''); });
    hideAlert();
    success.hidden = true;
    success.classList.remove('is-show');
    form.hidden = false;
  });
});