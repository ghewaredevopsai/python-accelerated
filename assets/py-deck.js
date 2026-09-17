/* ===========================================================================
   Python Accelerated - slide runner
   Plain ES5-ish DOM, no dependencies, no CDN. Works from file:// and offline.

   A deck only authors <section class="slide">...</section> blocks.
   Branding, footers, counter, index and notes are injected from here, so the
   whole module is re-branded by editing this file and py-theme.css.

   Keys:  arrows / space / PgUp / PgDn / Home / End  navigate
          T index      N notes      F fullscreen      Esc close
   =========================================================================== */
(function () {
  'use strict';

  var BRAND = {
    org:   'Gheware DevOps &amp; Agentic AI',
    site:  'devops.gheware.com',
    siteU: 'https://devops.gheware.com',
    mail:  'training@gheware.com',
    phone: '+91-9606795215',
    trainer: 'Rajesh Gheware'
  };

  var stage  = document.getElementById('stage');
  var slides = [].slice.call(document.querySelectorAll('.slide'));
  var d      = document.body.dataset;
  var deck   = d.deck || 'Python Accelerated';
  var home   = d.home || '../index.html';
  var cur    = 0;

  /* ---- chrome -------------------------------------------------------- */
  function el(html) { var t = document.createElement('div'); t.innerHTML = html; return t.firstChild; }

  document.body.appendChild(el('<div id="bar"><i></i></div>'));
  document.body.appendChild(el(
    '<div id="hud">' +
      '<a href="' + home + '" title="Module home">MODULE</a><span class="sep">|</span>' +
      (d.prev ? '<a href="' + d.prev + '" title="' + (d.prevLabel || '') + '">&#8592; prev</a><span class="sep">|</span>' : '') +
      (d.next ? '<a href="' + d.next + '" title="' + (d.nextLabel || '') + '">next &#8594;</a><span class="sep">|</span>' : '') +
      '<a href="#" data-act="index">index</a><span class="sep">|</span>' +
      '<a href="#" data-act="notes">notes</a><span class="sep">|</span>' +
      '<span id="count">1 / ' + slides.length + '</span>' +
    '</div>'));
  document.body.appendChild(el(
    '<div class="overlay" id="indexOv"><h3>' + deck + '</h3>' +
    '<p class="hint">click a slide, or press T to close</p><div id="indexList"></div></div>'));
  document.body.appendChild(el(
    '<div class="overlay" id="notesOv"><h3>Notes</h3>' +
    '<p class="hint">press N to close</p><div id="notesBody"></div></div>'));

  var bar = document.querySelector('#bar > i');
  var count = document.getElementById('count');
  var indexOv = document.getElementById('indexOv');
  var notesOv = document.getElementById('notesOv');
  var notesBody = document.getElementById('notesBody');

  /* ---- footer on every slide ----------------------------------------- */
  slides.forEach(function (s, i) {
    if (s.querySelector(':scope > footer')) return;
    var f = document.createElement('footer');
    f.innerHTML =
      '<span class="brand"><b>' + BRAND.org + '</b> &middot; ' +
        '<a href="' + BRAND.siteU + '">' + BRAND.site + '</a> &middot; ' +
        BRAND.mail + ' &middot; ' + BRAND.phone + '</span>' +
      '<span>' + deck + ' &middot; Trainer: ' + BRAND.trainer + '</span>';
    s.appendChild(f);
  });

  /* ---- index --------------------------------------------------------- */
  function titleOf(h) {
    var c = h.cloneNode(true);                 // a <br> in a title is a line break,
    [].forEach.call(c.querySelectorAll('br'),  // not a word join
      function (b) { b.parentNode.replaceChild(document.createTextNode(' '), b); });
    return c.textContent.replace(/\s+/g, ' ').trim();
  }

  var list = document.getElementById('indexList');
  slides.forEach(function (s, i) {
    var h = s.querySelector('h1, h2');
    var a = el('<a href="#/' + (i + 1) + '"><span class="n">' +
      (i + 1 < 10 ? '0' : '') + (i + 1) + '</span>' +
      (h ? titleOf(h) : 'Slide ' + (i + 1)) + '</a>');
    a.addEventListener('click', function () { closeOverlays(); });
    list.appendChild(a);
  });
  var links = [].slice.call(list.children);

  /* ---- scaling ------------------------------------------------------- */
  function fit() {
    var s = Math.min(window.innerWidth / 1280, window.innerHeight / 720);
    stage.style.transform = 'scale(' + s + ')';
  }

  /* ---- navigation ---------------------------------------------------- */
  function show(n) {
    cur = Math.max(0, Math.min(slides.length - 1, n));
    slides.forEach(function (s, i) { s.classList.toggle('active', i === cur); });
    links.forEach(function (a, i) { a.classList.toggle('cur', i === cur); });
    bar.style.width = ((cur + 1) / slides.length * 100) + '%';
    count.textContent = (cur + 1) + ' / ' + slides.length;
    var nt = slides[cur].querySelector('.notes');
    notesBody.innerHTML = nt ? nt.innerHTML : '<p style="color:var(--fg-faint)">No notes for this slide.</p>';
    if (history.replaceState) history.replaceState(null, '', '#/' + (cur + 1));
  }
  function closeOverlays() { indexOv.classList.remove('open'); notesOv.classList.remove('open'); }
  function toggle(ov) { var was = ov.classList.contains('open'); closeOverlays(); if (!was) ov.classList.add('open'); }

  document.addEventListener('keydown', function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var k = e.key;
    if (k === 'ArrowRight' || k === 'PageDown' || k === ' ') { show(cur + 1); e.preventDefault(); }
    else if (k === 'ArrowLeft' || k === 'PageUp') { show(cur - 1); e.preventDefault(); }
    else if (k === 'Home') { show(0); }
    else if (k === 'End') { show(slides.length - 1); }
    else if (k === 't' || k === 'T') { toggle(indexOv); }
    else if (k === 'n' || k === 'N') { toggle(notesOv); }
    else if (k === 'f' || k === 'F') {
      if (document.fullscreenElement) document.exitFullscreen();
      else document.documentElement.requestFullscreen();
    }
    else if (k === 'Escape') { closeOverlays(); }
  });

  document.getElementById('hud').addEventListener('click', function (e) {
    var act = e.target.getAttribute('data-act');
    if (!act) return;
    e.preventDefault();
    toggle(act === 'index' ? indexOv : notesOv);
  });

  [indexOv, notesOv].forEach(function (ov) {
    ov.addEventListener('click', function (e) { if (e.target === ov) closeOverlays(); });
  });

  /* click / swipe on the stage */
  var x0 = null;
  stage.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  stage.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 45) show(cur + (dx < 0 ? 1 : -1));
    x0 = null;
  }, { passive: true });

  window.addEventListener('resize', fit);
  window.addEventListener('hashchange', function () {
    var m = /^#\/(\d+)/.exec(location.hash);
    if (m) show(parseInt(m[1], 10) - 1);
  });

  fit();
  var m = /^#\/(\d+)/.exec(location.hash);
  show(m ? parseInt(m[1], 10) - 1 : 0);
})();
