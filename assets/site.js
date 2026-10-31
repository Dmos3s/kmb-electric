/* KMB Electric shared script. Used by every page. Blocks guard for elements that only exist on some pages. */
document.addEventListener('DOMContentLoaded', function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var isTouch = window.matchMedia('(hover: none)').matches;

  /* 1. Lenis smooth scroll (first) */
  var lenis = null;
  if (!reduce && window.Lenis) {
    lenis = new Lenis({ lerp: 0.08 });
    function raf(time) { lenis.raf(time); requestAnimationFrame(raf); }
    requestAnimationFrame(raf);
  }
  function scrollToEl(el) {
    var offset = -64;
    if (lenis) { lenis.scrollTo(el, { offset: offset }); }
    else { var y = el.getBoundingClientRect().top + window.pageYOffset + offset; window.scrollTo({ top: y, behavior: reduce ? 'auto' : 'smooth' }); }
  }

  /* 2. AOS (after Lenis) */
  if (window.AOS) AOS.init({ duration: 700, once: true, offset: 80, disable: reduce });

  /* 3. Hero: Splitting first, then GSAP word stagger */
  var sub = document.getElementById('hero-sub');
  var ctas = document.getElementById('hero-ctas');
  if (!sub || !ctas) { /* not the homepage */ }
  else if (!reduce && window.Splitting && window.gsap) {
    Splitting();
    gsap.from('.hero-headline .word', { y: 40, opacity: 0, duration: 0.8, stagger: 0.08, ease: 'power3.out', delay: 0.15,
      onComplete: function () { sub.classList.add('is-in'); setTimeout(function () { ctas.classList.add('is-in'); }, 200); } });
    /* Safety net: if the tab was hidden and rAF was throttled, force the final state */
    setTimeout(function () {
      gsap.killTweensOf('.hero-headline .word');
      gsap.set('.hero-headline .word', { clearProps: 'all' });
      sub.classList.add('is-in'); ctas.classList.add('is-in');
    }, 3200);
  } else {
    sub.classList.add('is-in'); ctas.classList.add('is-in');
  }

  /* 4. Particles */
  if (!reduce && window.tsParticles && document.getElementById('particles')) {
    tsParticles.load('particles', {
      fullScreen: { enable: false },
      particles: {
        number: { value: 28 },
        color: { value: '#F1D27A' },
        opacity: { value: 0.18, random: true, animation: { enable: true, speed: 0.6, minimumValue: 0.05, sync: false } },
        size: { value: 2, random: true },
        move: { enable: true, speed: 0.5, direction: 'top', random: true, straight: false, outModes: 'out' },
        shape: { type: 'circle' }
      },
      detectRetina: true
    });
  }

  /* 5. Tilt on service cards (desktop only) */
  if (!reduce && !isTouch && window.VanillaTilt) {
    VanillaTilt.init(document.querySelectorAll('.service-card'), { max: 6, speed: 400, glare: true, 'max-glare': 0.15, perspective: 800 });
  }

  /* 6. Testimonials */
  if (window.Swiper && document.querySelector('.testimonials-swiper')) {
    new Swiper('.testimonials-swiper', {
      loop: true, spaceBetween: 24, grabCursor: true, centeredSlides: true,
      autoplay: reduce ? false : { delay: 3500, disableOnInteraction: false, pauseOnMouseEnter: true },
      breakpoints: { 0: { slidesPerView: 1.15, centeredSlides: true }, 768: { slidesPerView: 2.2, centeredSlides: false }, 1024: { slidesPerView: 3, centeredSlides: false } }
    });
  }

  /* 7. Trust bar counters: IntersectionObserver + GSAP expo.out */
  var trust = document.getElementById('trust');
  var counted = false;
  function runCounters() {
    if (counted) return; counted = true;
    document.querySelectorAll('.counter').forEach(function (el) {
      var target = parseFloat(el.getAttribute('data-target'));
      var dec = parseInt(el.getAttribute('data-decimals') || '0', 10);
      if (reduce || !window.gsap) { el.textContent = target.toFixed(dec); return; }
      var obj = { v: 0 };
      gsap.to(obj, { v: target, duration: 2, ease: 'expo.out', onUpdate: function () { el.textContent = obj.v.toFixed(dec); } });
    });
  }
  if (!trust) { /* no trust bar on this page */ }
  else if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) { entries.forEach(function (e) { if (e.isIntersecting) { runCounters(); io.disconnect(); } }); }, { threshold: 0.3 });
    io.observe(trust);
  } else { runCounters(); }

  /* 8. Header state + scroll progress */
  var header = document.getElementById('site-header');
  var bar = document.getElementById('scroll-progress');
  function onScroll() {
    var y = window.pageYOffset || document.documentElement.scrollTop;
    header.classList.toggle('is-scrolled', y > 80);
    var max = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.width = (max > 0 ? (y / max) * 100 : 0) + '%';
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* 9. Mobile menu */
  var header = document.getElementById('site-header');
  var toggle = document.getElementById('menu-toggle');
  var menu = document.getElementById('mobile-menu');
  function closeMenu() { menu.classList.remove('is-open'); header.classList.remove('menu-open'); toggle.setAttribute('aria-expanded', 'false'); toggle.setAttribute('aria-label', 'Open menu'); document.body.style.overflow = ''; if (lenis) lenis.start(); }
  function openMenu() { menu.classList.add('is-open'); header.classList.add('menu-open'); toggle.setAttribute('aria-expanded', 'true'); toggle.setAttribute('aria-label', 'Close menu'); document.body.style.overflow = 'hidden'; if (lenis) lenis.stop(); }
  menu.addEventListener('click', function (e) { if (e.target === menu) closeMenu(); });
  toggle.addEventListener('click', function () { menu.classList.contains('is-open') ? closeMenu() : openMenu(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMenu(); });

  /* 10. Anchor links (smooth via Lenis) + service preselect */
  var select = document.getElementById('f-service');
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href');
      if (id.length < 2) return;
      var el = document.querySelector(id);
      if (!el) return;
      e.preventDefault();
      closeMenu();
      var svc = a.getAttribute('data-service');
      if (svc && select) { select.value = svc; }
      scrollToEl(el);
    });
  });

  /* 11. Estimate form */
  var form = document.getElementById('estimate-form');
  var ENDPOINT = 'https://formsubmit.co/ajax/c103a0fb4189d09b76abc02c6d298964';
  var LEAD_TEXT = 'https://sms.fusehq.cloud/kmb-lead';
  var TEST = /[?&#]test=1\b/.test(location.href);   /* ?test=1 routes texts to Dan and drops the cc */
  var LEAD_TOKEN = '4FC0a52AXd73n5iACmKz6kjpcCkoYMX7';
  function showSuccess() {
    form.innerHTML = '<div class="success-msg"><p class="big">Got it. We will be in touch during business hours.</p><p>Check your phone, we usually call or text first. Need it faster? Call <a href="tel:+17199635191" style="color:#A8791F;font-weight:600">719-963-5191</a>.</p></div>';
  }
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var name = form.name.value.trim(), phone = form.phone.value.trim(), service = form.service.value;
    var bad = null;
    if (!name) bad = form.name; else if (phone.replace(/\D/g, '').length < 10) bad = form.phone; else if (!service) bad = form.service;
    if (bad) { bad.focus(); bad.style.borderColor = '#C0392B'; bad.style.boxShadow = '0 0 0 3px rgba(192,57,43,.18)'; bad.addEventListener('input', function () { bad.style.borderColor = ''; bad.style.boxShadow = ''; }, { once: true }); return; }
    if (form._honey.value) { showSuccess(); return; }
    var btn = document.getElementById('f-submit');
    btn.disabled = true; btn.textContent = 'Sending...';
    var msg = form.message.value.trim();
    var payload = { name: name, phone: phone, service: service, message: msg,
      _subject: 'KMB Electric estimate request: ' + service, _template: 'table', _captcha: 'false' };
    if (!TEST) payload._cc = 'kylebashford@kmbelectric.com';
    /* Instant text to Kyle via Hermes (fire-and-forget; email goes out via FormSubmit). */
    try {
      fetch(LEAD_TEXT, { method: 'POST', headers: { 'Content-Type': 'application/json' }, keepalive: true,
        body: JSON.stringify({ token: LEAD_TOKEN, name: name, phone: phone, service: service, message: msg, test: TEST }) }).catch(function () {});
    } catch (err) {}
    fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(payload) })
      .then(function () { showSuccess(); })
      .catch(function () { showSuccess(); });
  });


  /* Text-us bubble: visitor leaves a cell number, Kyle gets a text with it and replies from his phone. */
  (function () {
    var fab = document.getElementById('tw-open'), panel = document.getElementById('tw-panel'), closeBtn = document.getElementById('tw-close'), tf = document.getElementById('tw-form');
    if (!fab || !panel || !tf) return;
    function twOpen() { panel.hidden = false; fab.setAttribute('aria-expanded', 'true'); setTimeout(function () { var f = tf.querySelector('[name=name]'); if (f) f.focus(); }, 60); }
    function twShut() { panel.hidden = true; fab.setAttribute('aria-expanded', 'false'); }
    fab.addEventListener('click', function () { panel.hidden ? twOpen() : twShut(); });
    closeBtn.addEventListener('click', twShut);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) twShut(); });
    var mb = document.getElementById('mbar-text'); if (mb) mb.addEventListener('click', function (e) { e.preventDefault(); twOpen(); });
    document.querySelectorAll('[data-textus]').forEach(function (a) { a.addEventListener('click', function (e) { e.preventDefault(); twOpen(); }); });
    function mark(el) { el.classList.add('tw-err'); el.focus(); el.addEventListener('input', function () { el.classList.remove('tw-err'); }, { once: true }); }
    tf.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = tf.name.value.trim(), phone = tf.phone.value.trim(), msg = tf.message.value.trim();
      if (!name) return mark(tf.name);
      if (phone.replace(/\D/g, '').length < 10) return mark(tf.phone);
      if (!msg) return mark(tf.message);
      var btn = document.getElementById('tw-send'); btn.disabled = true; btn.textContent = 'Sending...';
      var emailPayload = { name: name, phone: phone, message: msg, request: 'Text back requested from the website bubble', _subject: 'KMB Electric text request: ' + name, _template: 'table', _captcha: 'false' };
      if (!TEST) emailPayload._cc = 'kylebashford@kmbelectric.com';
      fetch(LEAD_TEXT, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ token: LEAD_TOKEN, kind: 'text', name: name, phone: phone, message: msg, test: TEST }) })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          if (!j || !j.ok) throw new Error('bridge');
          try { fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, keepalive: true, body: JSON.stringify(emailPayload) }).catch(function () {}); } catch (err) {}
          tf.innerHTML = '<div class="tw-done"><strong>Sent to Kyle.</strong><p>He will text you at ' + phone.replace(/[<>&]/g, '') + ' during business hours. Need it now? Call <a href="tel:+17199635191">719-963-5191</a>.</p></div>';
        })
        .catch(function () {
          btn.disabled = false; btn.textContent = 'Send text';
          var p = tf.querySelector('.tw-fine'); if (p) p.innerHTML = '<strong style="color:#C0392B">That did not go through.</strong> Text Kyle directly at <a href="sms:+17199635191">719-963-5191</a>.';
        });
    });
  })();
  var yr = document.getElementById('year'); if (yr) yr.textContent = new Date().getFullYear();

  /* 12. Projects gallery lightbox (projects page only) */
  var lb = document.getElementById('lightbox');
  if (lb) {
    var lbImg = lb.querySelector('img'), lbCap = lb.querySelector('figcaption');
    document.querySelectorAll('.gallery a').forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        lbImg.src = a.getAttribute('href'); lbImg.alt = a.getAttribute('data-alt') || '';
        lbCap.textContent = a.getAttribute('data-caption') || '';
        if (typeof lb.showModal === 'function') lb.showModal(); else lb.setAttribute('open', '');
      });
    });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.classList.contains('lb-close')) lb.close(); });
  }
});
