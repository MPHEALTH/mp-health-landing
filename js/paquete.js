/* ═══════════════════════════════════════════════════════════
   PAQUETES MP · lógica compartida
   Mismo camino que paneles-sangre.html: los datos se envían a
   /api/lead (correo al equipo + Zoho + Sheet) y solo si el envío
   sale bien se muestra el Calendly. Cada página define antes:
     window.PAQUETE = { nombre, precio, slug, calendly }
═══════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var PK        = window.PAQUETE || {};
  var ENDPOINT  = 'https://bioscan.michellepeiret.com/api/lead';
  var CALENDLY  = PK.calendly || '';

  function $(id)  { return document.getElementById(id); }
  function val(id) { var e = $(id); return e ? (e.value || '').trim() : ''; }
  function err(id, on) { var e = $(id); if (e) e.classList.toggle('on', !!on); }
  function ev(name, params) { try { if (window.gtag) gtag('event', name, params || {}); } catch (e) {} }

  /* ── Revelado al hacer scroll ── */
  var faders = document.querySelectorAll('.fade');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    faders.forEach(function (el) { io.observe(el); });
  } else {
    faders.forEach(function (el) { el.classList.add('in'); });
  }

  /* ── FAQ ── */
  document.querySelectorAll('.faq-q').forEach(function (b) {
    b.addEventListener('click', function () {
      var item = b.parentElement;
      var open = item.classList.contains('on');
      document.querySelectorAll('.faq-item').forEach(function (i) { i.classList.remove('on'); });
      if (!open) { item.classList.add('on'); ev('faq_open', { item_name: b.textContent.trim() }); }
    });
  });

  /* ── Pasos ── */
  function show(which) {
    ['pkStep1', 'pkDone'].forEach(function (id) {
      var e = $(id); if (e) e.classList.toggle('on', id === which);
    });
  }

  /* ── Envío ── */
  var form = $('pkForm');
  if (!form) return;

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    var name = val('pkName'), email = val('pkEmail'), phone = val('pkPhone'),
        loc  = val('pkLoc'),  when  = val('pkWhen'),  caso  = val('pkCase');

    var ok = true;
    if (name.length < 3 || name.indexOf(' ') === -1) { err('errName', true);  ok = false; } else err('errName', false);
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))   { err('errEmail', true); ok = false; } else err('errEmail', false);
    if (phone.replace(/\D/g, '').length < 8)         { err('errPhone', true); ok = false; } else err('errPhone', false);
    if (!when)                                       { err('errWhen', true);  ok = false; } else err('errWhen', false);
    if (!ok) return;

    var btn = $('pkSubmit');
    btn.disabled = true; btn.textContent = 'Enviando…';
    err('errForm', false);

    fetch(ENDPOINT, {
      method: 'POST',
      keepalive: true,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name:      name,
        email:     email,
        phone:     phone,
        country:   loc,
        challenge: caso,
        goal:      'Paquete de diagnósticos',
        program:   'Paquete — ' + PK.nombre,
        timeline:  when,
        origen:    'paquete_' + PK.slug,
        paquete:   PK.nombre,
        precio:    PK.precio,
        source:    'landing paquete ' + PK.slug,
        calendar:  'paquetes_15min'
      })
    })
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        ev('generate_lead', { item_name: PK.nombre, currency: 'USD', value: PK.valor || 0 });
        show('pkDone');
        var a = $('agendar'); if (a) a.scrollIntoView({ behavior: 'smooth', block: 'start' });
        loadCalendly(name, email);
      })
      .catch(function (e2) {
        var box = $('errForm');
        if (box) box.textContent = 'No se pudo enviar. Inténtalo de nuevo o llámanos al +1 (786) 930-2544.';
        err('errForm', true);
        btn.disabled = false; btn.textContent = 'Agendar mi llamada →';
        console.error('Paquete lead error:', e2);
      });
  });

  /* ── Calendly: sin enlace configurado se muestra un aviso, no un iframe roto ── */
  function loadCalendly(name, email) {
    var wrap = $('pkCalWrap');
    if (!wrap) return;
    if (!CALENDLY) {
      wrap.innerHTML = '<div class="pk-cal-fallback"><p><b>Recibimos tus datos.</b> ' +
        'Nuestro equipo te contactará para coordinar tu llamada de 15 minutos y reservar tu fecha. ' +
        'Si prefieres adelantarlo, llámanos al +1 (786) 930-2544.</p></div>';
      return;
    }
    wrap.innerHTML = '<div id="pkCal" style="min-width:320px;height:660px;"></div>';
    var url = CALENDLY + '?hide_gdpr_banner=1&name=' + encodeURIComponent(name) +
              '&email=' + encodeURIComponent(email);
    (function init() {
      if (window.Calendly && window.Calendly.initInlineWidget) {
        window.Calendly.initInlineWidget({ url: url, parentElement: $('pkCal') });
      } else { setTimeout(init, 300); }
    })();
  }
})();
