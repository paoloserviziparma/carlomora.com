/* Carlo Mora Parrucchieri — interazioni del sito (nessun cookie, nessun tracciamento) */
(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* menu mobile */
  var menuBtn = document.querySelector('.menu-btn');
  var nav = document.getElementById('nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        nav.classList.remove('is-open');
        menuBtn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* intestazione: sparisce scorrendo in giù, ricompare scorrendo in su */
  var header = document.querySelector('.header');
  var lastY = window.scrollY;
  var ticking = false;
  var heroImg = document.querySelector('.hero-img img, .hero-img video');
  var heroVideo = document.querySelector('[data-hero-video]');
  if (heroVideo) {
    heroVideo.closest('.hero').classList.add('has-video');
    if (reduce) { heroVideo.removeAttribute('autoplay'); heroVideo.pause(); }
    else {
      var p = heroVideo.play();
      if (p && p.catch) p.catch(function () {});
      /* fermo il video quando l'hero non si vede, per risparmiare batteria */
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (en) {
          en.forEach(function (x) { if (x.isIntersecting) { var q = heroVideo.play(); if (q && q.catch) q.catch(function () {}); } else heroVideo.pause(); });
        }).observe(heroVideo);
      }
    }
  }
  var mobile = window.matchMedia('(max-width: 760px)');
  var parallax = Array.prototype.slice.call(document.querySelectorAll('[data-parallax] img'));

  /* titoli delle sezioni: entrata parola per parola */
  if (!reduce) {
    document.querySelectorAll('.h2').forEach(function (h) {
      var words = [];
      function walk(node, out) {
        Array.prototype.slice.call(node.childNodes).forEach(function (n) {
          if (n.nodeType === 3) {
            n.textContent.split(/(\s+)/).forEach(function (w) {
              if (!w) return;
              if (/^\s+$/.test(w)) { out.appendChild(document.createTextNode(w)); return; }
              var s = document.createElement('span');
              s.className = 'w';
              var i = document.createElement('span');
              i.textContent = w;
              i.style.transitionDelay = (words.length * 0.07) + 's';
              words.push(i);
              s.appendChild(i);
              out.appendChild(s);
            });
          } else if (n.nodeType === 1) {
            var c = n.cloneNode(false);
            walk(n, c);
            out.appendChild(c);
          }
        });
      }
      var frag = document.createDocumentFragment();
      walk(h, frag);
      h.textContent = '';
      h.appendChild(frag);
      h.classList.add('split');
    });
  }

  function onScroll() {
    var y = window.scrollY;
    if (header) {
      var menuOpen = nav && nav.classList.contains('is-open');
      if (y > 120 && y > lastY + 4 && !menuOpen) header.classList.add('is-hidden');
      else if (y < lastY - 4 || y <= 120) header.classList.remove('is-hidden');
    }
    if (!reduce) {
      var half = mobile.matches ? 0.5 : 1; /* parallax dimezzato su mobile */
      if (heroImg && y < window.innerHeight * 1.2) {
        heroImg.style.transform = 'translate3d(0,' + (-y * 0.14 * half).toFixed(1) + 'px,0)';
      }
      var vh = window.innerHeight;
      parallax.forEach(function (img) {
        var r = img.parentNode.getBoundingClientRect();
        if (r.bottom < -100 || r.top > vh + 100) return;
        var p = (r.top + r.height / 2 - vh / 2) / vh; /* -1 … 1 */
        img.style.transform = 'translate3d(0,' + (p * -40 * half).toFixed(1) + 'px,0) scale(1.1)';
      });
    }
    lastY = y;
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { window.requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });

  /* blocchi che compaiono allo scroll */
  var items = document.querySelectorAll('.reveal');
  if (reduce || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  }
  onScroll();

  /* Quale Arcano sei? */
  var quiz = document.getElementById('quiz');
  var dataEl = document.getElementById('quiz-data');
  if (quiz && dataEl) {
    var D = JSON.parse(dataEl.textContent);
    var answers = [];
    var stepEl = quiz.querySelector('[data-q-step]');
    var qEl = quiz.querySelector('[data-q-text]');
    var optsEl = quiz.querySelector('[data-q-opts]');
    var barEl = quiz.querySelector('[data-q-bar]');
    var askEl = quiz.querySelector('[data-q-ask]');
    var resEl = quiz.querySelector('[data-q-res]');

    function waLink(msg) {
      return 'https://wa.me/' + D.phone + '?text=' + encodeURIComponent(msg);
    }
    function render() {
      var step = answers.length;
      barEl.style.width = (Math.min(step, D.questions.length) / D.questions.length * 100) + '%';
      if (step < D.questions.length) {
        var q = D.questions[step];
        askEl.hidden = false; resEl.hidden = true;
        stepEl.textContent = D.labels.step.replace('{n}', step + 1).replace('{t}', D.questions.length);
        qEl.textContent = q.q;
        optsEl.innerHTML = '';
        q.o.forEach(function (o) {
          var b = document.createElement('button');
          b.type = 'button';
          b.className = 'opzione';
          b.textContent = o[0];
          b.addEventListener('click', function () { answers.push(o[1]); render(); focusQuiz(); });
          optsEl.appendChild(b);
        });
        return;
      }
      var tally = {};
      answers.forEach(function (a) { tally[a] = (tally[a] || 0) + 1; });
      var best = answers[0];
      Object.keys(tally).forEach(function (k) { if (tally[k] > tally[best]) best = k; });
      var c = D.cards[best];
      askEl.hidden = true; resEl.hidden = false;
      resEl.querySelector('[data-c-num]').textContent = c.num;
      resEl.querySelector('[data-c-name]').textContent = c.name;
      resEl.querySelector('[data-c-title]').textContent = c.title;
      resEl.querySelector('[data-c-idea]').textContent = c.idea;
      resEl.querySelector('[data-c-wa]').href = waLink(D.labels.waMsg.replace('{card}', c.name));
      var card = resEl.querySelector('.carta');
      card.style.animation = 'none'; void card.offsetWidth; card.style.animation = '';
    }
    function focusQuiz() {
      var target = answers.length < D.questions.length ? qEl : resEl.querySelector('[data-c-title]');
      if (target) { target.setAttribute('tabindex', '-1'); target.focus({ preventScroll: true }); }
    }
    quiz.querySelector('[data-q-restart]').addEventListener('click', function () { answers = []; render(); focusQuiz(); });
    render();
  }
})();
