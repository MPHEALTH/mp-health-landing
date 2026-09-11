#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera las paginas de patologia de MP Health desde una plantilla comun.

Existen porque el trafico de Meta viene segmentado por condicion y aterrizarlo
todo en el landing generico desperdicia la unica ventaja que da segmentar: que
la pagina hable de lo que la persona vino a resolver.

Cada pagina abre el MISMO formulario de empezar.html en un modal, pero con la
condicion ya respondida (?objetivo=), asi que quien llega por aqui contesta
ocho preguntas en vez de nueve.

REGLA INNEGOCIABLE en el texto: se afirma lo que medimos, nunca se promete un
resultado clinico. En fertilidad esto es literal — nunca se promete un embarazo.
"""
import io, os

OUT = os.path.dirname(os.path.abspath(__file__))
GA4, PIXEL = 'G-B7PSHFCHGY', '1219764922715386'
TEL, TEL_H = '+1 (786) 484 8729', '+17864848729'
WA = 'https://wa.me/17864848729?text='

# ─────────────────────────────────────────────────────────────────────────
#  DATOS POR CONDICION  — lo unico que cambia entre paginas
# ─────────────────────────────────────────────────────────────────────────
CONDICIONES = {
 'fertilidad': {
  'slug': 'fertilidad',
  'objetivo': 'hormonal',          # clave de la pregunta 1 de empezar.html
  'title': 'Fertilidad | Michelle Peiret Health',
  'desc': 'Leemos los marcadores que un estudio de fertilidad convencional no mira: '
          'MTHFR, tiroides completa, inflamación y micronutrientes. Miami u online.',
  'eyebrow': 'Método MP · Fertilidad',
  'h1a': 'Que no te digan',
  'h1b': '«sin causa»',
  'h1c': 'cuando nadie la ha buscado',
  'sub': 'Un estudio de fertilidad mide hormonas y anatomía. Casi nunca mira la genética '
         'de tus vitaminas, tu tiroides completa, tu inflamación ni tus micronutrientes — '
         'y ahí es donde suele quedar algo por revisar.',
  'hero_img': 'images/paso2-michelle-consulta.jpg',
  'hero_alt': 'Consulta de evaluación con Michelle Peiret',
  'trust': 'Online o presencial en Miami · Trabajamos junto a tu ginecólogo o tu especialista en fertilidad',
  'dato_label': 'Lo que casi nunca se mide',
  'dato_h': 'MTHFR: el gen que decide si tu ácido fólico te sirve',
  'dato_p': [
    'Existe una variante genética llamada <b>MTHFR</b> que reduce la capacidad de convertir '
    'el ácido fólico común en su forma activa, el folato que el cuerpo de verdad usa. Quien '
    'la tiene puede estar tomando su suplemento todos los días y aprovechar solo una parte.',
    'Es una variante frecuente y se mide con una prueba sencilla. Aun así, rara vez entra en '
    'un estudio de fertilidad de rutina — y cuando aparece, cambia algo tan concreto como '
    '<b>qué forma de folato tiene sentido que tomes</b>.',
    'No es la explicación de todos los casos, y nadie serio te diría que lo es. Es un dato que '
    'se puede tener, y al que mucha gente llega a un tratamiento sin haber tenido nunca.',
  ],
  'dato_nota': 'MTHFR es uno de los marcadores que revisamos. Ni el único, ni una garantía de nada: '
               'un dato más sobre la mesa a la hora de decidir.',
  'medimos_label': 'Qué revisamos en tu caso',
  'medimos_h': 'Los cuatro frentes que un estudio<br>de fertilidad no suele cruzar',
  'medimos': [
    ('La genética de tus vitaminas',
     'MTHFR y la conversión de folato, B12 y B6. Define qué forma de cada nutriente te sirve '
     'a ti, y cuál estás tomando sin aprovechar.'),
    ('Tiroides completa, no solo TSH',
     'El examen estándar mide TSH, que es la orden de la pituitaria. Puedes tener TSH normal '
     'y T3 libre baja a la vez, y los anticuerpos casi nunca se miran.'),
    ('Inflamación y microbiota',
     'La inflamación crónica silenciosa altera el ambiente hormonal. Y hay bacterias '
     'intestinales que regulan cuánto estrógeno recircula tu cuerpo.'),
    ('Micronutrientes y carga tóxica',
     'Hierro y ferritina reales, vitamina D, zinc, selenio, omega 3 y metales pesados. Las '
     'deficiencias silenciosas no salen en un panel de rutina.'),
  ],
  'pasos': [
    ('Cuéntanos tu caso', 'Ocho preguntas rápidas sobre qué llevas intentando, desde cuándo y '
     'qué te han dicho hasta ahora. Toma dos minutos y no cuesta nada.'),
    ('Te llama un especialista', 'Revisa tu caso contigo, te dice con franqueza si es para '
     'nosotros y te explica qué incluye la evaluación y cómo se paga.'),
    ('Tu evaluación con Michelle', 'Tu BioScan de 900+ biomarcadores y tu InBody, leídos '
     'contigo. Sales con un plan escrito, no con una lista de suplementos.'),
  ],
  'faq': [
    ('¿Esto reemplaza mi tratamiento de fertilidad?',
     'No, y no debería. Trabajamos <b>junto</b> a tu ginecólogo o tu especialista, no en su '
     'lugar. Lo que hacemos es leer la parte de tu biología que su estudio no cubre, para que '
     'lo que ya estás haciendo ocurra en un cuerpo mejor preparado.'),
    ('¿Me garantizan un embarazo?',
     'No. Nadie honesto puede garantizarte eso, y si alguien te lo garantiza, desconfía. Lo que '
     'sí te podemos comprometer es el dato: vas a saber qué tienes, qué te falta y qué depende '
     'de ti, con números y por escrito.'),
    ('¿Sirve si llevo años intentando?',
     'Es el caso más frecuente que vemos. Cuanto más tiempo llevas sin una respuesta clara, más '
     'probable es que falte medir algo — no que hayas hecho algo mal.'),
    ('¿Y si mi pareja también quiere revisarse?',
     'Tiene sentido: cerca de la mitad de los factores son masculinos y se miden distinto. Si '
     'vienen los dos, el equipo aplica un precio de pareja sobre las dos evaluaciones. '
     'Menciónalo en la llamada.'),
    ('¿Qué incluye la evaluación de $700?',
     'Tu <b>BioScan</b> de más de 900 biomarcadores desde una muestra de cabello, tu <b>InBody</b> '
     'de composición corporal, y la consulta en la que Michelle interpreta ambos contigo. Los '
     'estudios van dentro del precio.'),
    ('¿Tengo que ir a Miami?',
     'No es obligatorio. La consulta puede ser online y el kit del BioScan llega a tu casa, estés '
     'donde estés. Si estás en Miami puedes hacerlo presencial y añadir el InBody ahí mismo.'),
  ],
  'cierre_h': 'Antes de otro intento,<br>ten los datos completos',
  'cierre_p': 'No te vamos a prometer un resultado. Te vamos a dar lo que hoy no tienes: la '
              'lectura completa de tu biología, para que la próxima decisión la tomes sabiendo.',
  'cta': 'Quiero empezar',
  'wa_msg': 'Hola, vengo de la página de fertilidad y quiero información.',
 },
}

# ─────────────────────────────────────────────────────────────────────────
#  PLANTILLA
# ─────────────────────────────────────────────────────────────────────────
CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--navy:#0d1b2e;--navy2:#13223a;--teal:#00c9a7;--teal-dk:#00a88c;
 --cream:#f7f5f0;--cream2:#edeae2;--white:#fff;--text:#1a2332;--muted:#6b7a8d;
 --border:rgba(13,27,46,.10);--font-body:'Inter',-apple-system,sans-serif;
 --font-serif:'Cormorant Garamond',Georgia,serif}
html{scroll-behavior:smooth}
body{font-family:var(--font-body);color:var(--text);background:var(--cream);-webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}
.wrap{max-width:1180px;margin:0 auto;padding:0 32px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;background:var(--teal);
 color:var(--navy);font-weight:700;font-size:.88rem;letter-spacing:.05em;text-transform:uppercase;
 padding:16px 34px;border-radius:6px;text-decoration:none;border:none;cursor:pointer;
 transition:background .2s,transform .15s,box-shadow .2s;box-shadow:0 4px 22px rgba(0,201,167,.3);
 font-family:var(--font-body)}
.btn:hover{background:var(--teal-dk);transform:translateY(-2px);box-shadow:0 8px 30px rgba(0,201,167,.4)}
.btn-lg{font-size:.98rem;padding:19px 44px}
.label{display:block;font-size:.68rem;letter-spacing:.22em;text-transform:uppercase;
 color:var(--teal-dk);font-weight:700;margin-bottom:12px}
.h2{font-family:var(--font-serif);font-size:clamp(1.9rem,3.2vw,2.85rem);font-weight:600;
 line-height:1.16;color:var(--navy)}
/* NAV */
.nav{position:sticky;top:0;z-index:100;background:rgba(8,17,30,.96);backdrop-filter:blur(16px);
 -webkit-backdrop-filter:blur(16px);border-bottom:1px solid rgba(0,201,167,.2);padding:10px 32px;
 display:flex;align-items:center;justify-content:space-between;gap:16px}
.nav img{height:42px;width:auto}
.nav-r{display:flex;align-items:center;gap:20px}
.nav-tel{font-size:.8rem;color:rgba(255,255,255,.55);text-decoration:none}
.nav-tel:hover{color:var(--teal)}
.nav .btn{padding:12px 22px;font-size:.74rem;box-shadow:none}
/* HERO */
.hero{display:grid;grid-template-columns:1fr 44%;gap:0;align-items:center;background:var(--white)}
.hero-l{padding:76px 56px 76px max(32px,calc((100vw - 1180px)/2 + 32px))}
.hero h1{font-family:var(--font-serif);font-size:clamp(2.3rem,4.4vw,3.7rem);font-weight:600;
 line-height:1.1;color:var(--navy);margin-bottom:22px}
.hero h1 em{font-style:italic;color:var(--teal-dk)}
.hero-sub{font-size:1.04rem;line-height:1.75;color:var(--muted);font-weight:300;
 max-width:520px;margin-bottom:34px}
.hero-r{position:relative;align-self:stretch;min-height:520px;overflow:hidden}
.hero-r img{width:100%;height:100%;object-fit:cover;position:absolute;inset:0}
.trust{display:flex;align-items:flex-start;gap:9px;margin-top:22px;font-size:.8rem;
 color:var(--muted);line-height:1.55;max-width:470px}
.trust svg{flex:0 0 15px;color:var(--teal-dk);margin-top:2px}
/* BANDA */
.proof{background:var(--navy);padding:30px 32px;display:flex;justify-content:center;
 gap:clamp(28px,6vw,80px);flex-wrap:wrap;text-align:center}
.proof b{display:block;font-family:var(--font-serif);font-size:1.85rem;color:var(--teal);font-weight:600}
.proof span{display:block;font-size:.72rem;color:rgba(255,255,255,.45);line-height:1.5;margin-top:3px}
/* DATO */
.dato{padding:92px 0;background:var(--cream)}
.dato-card{background:var(--white);border-radius:18px;padding:52px 56px;
 box-shadow:0 10px 50px rgba(13,27,46,.07);border-left:4px solid var(--teal)}
.dato-card h2{margin-bottom:24px}
.dato-card p{font-size:1rem;line-height:1.85;color:var(--muted);font-weight:300;margin-bottom:18px}
.dato-card p b{color:var(--navy);font-weight:600}
.dato-nota{margin-top:28px;padding-top:22px;border-top:1px solid var(--border);
 font-size:.86rem;color:var(--muted);line-height:1.7;font-style:italic}
/* MEDIMOS */
.med{padding:92px 0;background:var(--navy);color:var(--white)}
.med .h2{color:var(--white)}
.med .label{color:var(--teal)}
.med-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:22px;margin-top:52px}
.med-card{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);
 border-radius:14px;padding:30px 28px}
.med-card h3{font-size:1.02rem;font-weight:600;color:var(--teal);margin-bottom:12px;line-height:1.35}
.med-card p{font-size:.9rem;line-height:1.75;color:rgba(255,255,255,.6);font-weight:300}
/* PASOS */
.pasos{padding:92px 0;background:var(--cream2)}
.pasos-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:28px;margin-top:52px}
.paso-n{font-family:var(--font-serif);font-size:2.6rem;color:var(--teal-dk);font-weight:600;line-height:1}
.paso h3{font-size:1.06rem;color:var(--navy);font-weight:600;margin:12px 0 10px}
.paso p{font-size:.92rem;line-height:1.75;color:var(--muted);font-weight:300}
/* FAQ */
.faq{padding:92px 0;background:var(--white)}
.faq-list{margin-top:46px;max-width:820px}
.faq-i{border-bottom:1px solid var(--border)}
.faq-q{width:100%;display:flex;align-items:center;gap:16px;text-align:left;background:none;
 border:none;cursor:pointer;padding:23px 0;font-family:var(--font-body);font-size:1rem;
 font-weight:600;color:var(--navy);line-height:1.45}
.faq-q span{flex:1}
.faq-ico{flex:0 0 18px;color:var(--teal-dk);transition:transform .22s}
.faq-i.open .faq-ico{transform:rotate(45deg)}
.faq-a{display:none;padding:0 0 24px;font-size:.95rem;line-height:1.85;color:var(--muted);
 font-weight:300;max-width:700px}
.faq-i.open .faq-a{display:block}
.faq-a b{color:var(--navy);font-weight:600}
/* CIERRE */
.cierre{padding:100px 0;background:var(--navy);color:var(--white);text-align:center}
.cierre h2{font-family:var(--font-serif);font-size:clamp(2rem,3.6vw,3.1rem);font-weight:600;
 line-height:1.18;margin-bottom:22px}
.cierre p{font-size:1.02rem;line-height:1.8;color:rgba(255,255,255,.6);font-weight:300;
 max-width:600px;margin:0 auto 40px}
/* FOOTER */
.foot{background:#08111e;padding:44px 32px;text-align:center}
.foot img{height:38px;width:auto;margin:0 auto 20px;opacity:.85}
.foot a{color:rgba(255,255,255,.4);font-size:.78rem;text-decoration:none;margin:0 12px}
.foot a:hover{color:var(--teal)}
.foot small{display:block;margin-top:18px;font-size:.72rem;color:rgba(255,255,255,.25)}
/* WHATSAPP */
.wa{position:fixed;right:20px;bottom:20px;z-index:90;display:flex;align-items:center;gap:9px;
 background:#25d366;color:#fff;padding:13px 20px;border-radius:99px;text-decoration:none;
 font-size:.86rem;font-weight:600;box-shadow:0 8px 26px rgba(37,211,102,.4)}
.wa svg{width:19px;height:19px}
@media(max-width:980px){
 .hero{grid-template-columns:1fr}
 .hero-l{padding:52px 26px 44px;order:1}
 .hero-r{order:0;min-height:300px}
 .dato-card{padding:36px 26px}
 .wrap{padding:0 22px}
 .dato,.med,.pasos,.faq{padding:64px 0}
 .cierre{padding:72px 0}
 .wa span{display:none}
 .wa{padding:15px}
 .nav-tel{display:none}
}
"""

# ─────────────────────────────────────────────────────────────────────────
#  EL MODAL SE LEE DE index.html
#  Asi no existen dos versiones: si el modal cambia en el landing, estas
#  paginas lo heredan en la siguiente corrida del generador.
# ─────────────────────────────────────────────────────────────────────────
def bloques_del_modal():
    s = io.open(os.path.join(OUT, 'index.html'), encoding='utf-8').read()
    css = s[s.index('/* ━━━ MODAL DEL FORMULARIO ━━━'): s.index('\n</style>')]
    m0  = s.index('  <!-- ━━━ MODAL DEL FORMULARIO ━━━ -->')
    m1  = s.index('</iframe>', m0)
    html = s[m0: s.index('\n\n', m1)]
    js  = s[s.index('    /* ── MODAL DEL FORMULARIO ── */'): s.index('    /* ── FAQ accordion ── */')]
    assert html.count('<div') == html.count('</div>'), 'modal HTML desbalanceado'
    return css, html, js


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def build(c):
    css, modal_html, modal_js = bloques_del_modal()

    medimos = '\n'.join(
        '        <div class="med-card"><h3>%s</h3><p>%s</p></div>' % (h, p)
        for h, p in c['medimos'])

    pasos = '\n'.join(
        '        <div class="paso"><div class="paso-n">%d</div><h3>%s</h3><p>%s</p></div>'
        % (i + 1, h, p) for i, (h, p) in enumerate(c['pasos']))

    faq = '\n'.join(
        '        <div class="faq-i"><button class="faq-q" type="button">'
        '<span>%s</span>'
        '<svg class="faq-ico" viewBox="0 0 24 24" width="18" height="18" fill="none" '
        'stroke="currentColor" stroke-width="2.2" stroke-linecap="round">'
        '<path d="M12 5v14M5 12h14"/></svg></button>'
        '<div class="faq-a">%s</div></div>' % (q, a) for q, a in c['faq'])

    dato = '\n'.join('        <p>%s</p>' % p for p in c['dato_p'])

    return TEMPLATE.format(
        ga4=GA4, pixel=PIXEL, tel=TEL, tel_h=TEL_H,
        wa=WA + c['wa_msg'].replace(' ', '%20'),
        title=esc(c['title']), desc=esc(c['desc']),
        eyebrow=c['eyebrow'], h1a=c['h1a'], h1b=c['h1b'], h1c=c['h1c'],
        sub=c['sub'], hero_img=c['hero_img'], hero_alt=c['hero_alt'],
        trust=c['trust'], objetivo=c['objetivo'], cta=c['cta'],
        dato_label=c['dato_label'], dato_h=c['dato_h'], dato=dato, dato_nota=c['dato_nota'],
        medimos_label=c['medimos_label'], medimos_h=c['medimos_h'], medimos=medimos,
        pasos=pasos, faq=faq,
        cierre_h=c['cierre_h'], cierre_p=c['cierre_p'],
        modal_css=css, modal_html=modal_html, modal_js=modal_js,
        css=CSS,
    )

TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="icon" type="image/png" href="images/LOGO%20%286%29.png">

<script>
  window.TRACKING = {{ GA4_ID: '{ga4}', META_PIXEL_ID: '{pixel}', GADS_ID: '' }};
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id={ga4}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{ga4}');
</script>
<script>
  !function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;
  n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,
  document,'script','https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', '{pixel}');
  fbq('track', 'PageView');
</script>

<style>{css}
{modal_css}
</style>
</head>
<body>

<nav class="nav">
  <a href="index.html"><img src="images/LOGO%20%2810%29.png" alt="Michelle Peiret Health"></a>
  <div class="nav-r">
    <a href="tel:{tel_h}" class="nav-tel">{tel}</a>
    <a href="empezar.html?objetivo={objetivo}" class="btn">{cta} &rarr;</a>
  </div>
</nav>

<section class="hero">
  <div class="hero-l">
    <span class="label">{eyebrow}</span>
    <h1>{h1a}<br><em>{h1b}</em><br>{h1c}</h1>
    <p class="hero-sub">{sub}</p>
    <a href="empezar.html?objetivo={objetivo}" class="btn btn-lg">{cta} &rarr;</a>
    <p class="trust">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
      {trust}
    </p>
  </div>
  <div class="hero-r"><img src="{hero_img}" alt="{hero_alt}"></div>
</section>

<div class="proof">
  <div><b>900+</b><span>Biomarcadores<br>en tu evaluación</span></div>
  <div><b>7</b><span>Especialistas<br>leyendo tu caso</span></div>
  <div><b>+7,000</b><span>Personas ya<br>tienen sus datos</span></div>
  <div><b>+15</b><span>Años leyendo<br>biología humana</span></div>
</div>

<section class="dato">
  <div class="wrap">
    <div class="dato-card">
      <span class="label">{dato_label}</span>
      <h2 class="h2">{dato_h}</h2>
{dato}
      <p class="dato-nota">{dato_nota}</p>
    </div>
  </div>
</section>

<section class="med">
  <div class="wrap">
    <span class="label">{medimos_label}</span>
    <h2 class="h2">{medimos_h}</h2>
    <div class="med-grid">
{medimos}
    </div>
  </div>
</section>

<section class="pasos">
  <div class="wrap">
    <span class="label">Cómo empieza</span>
    <h2 class="h2">Tres pasos, y el primero<br>toma dos minutos</h2>
    <div class="pasos-grid">
{pasos}
    </div>
  </div>
</section>

<section class="faq">
  <div class="wrap">
    <span class="label">Antes de decidir</span>
    <h2 class="h2">Lo que la gente pregunta</h2>
    <div class="faq-list">
{faq}
    </div>
  </div>
</section>

<section class="cierre">
  <div class="wrap">
    <h2>{cierre_h}</h2>
    <p>{cierre_p}</p>
    <a href="empezar.html?objetivo={objetivo}" class="btn btn-lg">{cta} &rarr;</a>
  </div>
</section>

<footer class="foot">
  <img src="images/LOGO%20%286%29.png" alt="Michelle Peiret Health">
  <div>
    <a href="index.html">Inicio</a>
    <a href="https://michellepeiret.com" target="_blank" rel="noopener">michellepeiret.com</a>
    <a href="https://www.instagram.com/michellepeiret" target="_blank" rel="noopener">Instagram</a>
    <a href="tel:{tel_h}">{tel}</a>
  </div>
  <small>760 NW 107th Ave, Suite #340, Miami FL 33172 &middot; &copy; 2026 Michelle Peiret Health</small>
</footer>

{modal_html}

<a class="wa" href="{wa}" target="_blank" rel="noopener">
  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.2-1.8-.9-2-1-.3-.1-.5-.2-.7.1-.2.3-.7 1-.9 1.2-.2.2-.3.2-.6.1-.3-.2-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.5-.5c.1-.2.2-.3.3-.5 0-.2 0-.4 0-.5 0-.2-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.3.2-1.4-.1-.1-.3-.2-.6-.4M12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2m0 18.2c-1.6 0-3.2-.4-4.5-1.3l-.3-.2-3.1.8.8-3-.2-.3a8.2 8.2 0 1 1 7.3 4"/></svg>
  <span>Escríbenos</span>
</a>

<script>
  /* El modal lo lee para abrir el formulario con la condición ya respondida */
  window.MP_OBJETIVO = '{objetivo}';

  function track(name, params) {{
    params = params || {{}};
    try {{ if (window.gtag) gtag('event', name, params); }} catch (e) {{}}
    try {{ if (window.fbq) fbq('trackCustom', name, params); }} catch (e) {{}}
  }}

{modal_js}
  /* FAQ */
  document.querySelectorAll('.faq-i').forEach(function (item) {{
    item.querySelector('.faq-q').addEventListener('click', function () {{
      var open = item.classList.contains('open');
      document.querySelectorAll('.faq-i').forEach(function (x) {{ x.classList.remove('open'); }});
      if (!open) {{ item.classList.add('open'); track('faq_abierta', {{}}); }}
    }});
  }});

  document.querySelector('.wa').addEventListener('click', function () {{
    track('whatsapp_click', {{ origen: 'condicion' }});
  }});
</script>
</body>
</html>
"""


if __name__ == '__main__':
    for nombre, c in CONDICIONES.items():
        destino = os.path.join(OUT, c['slug'] + '.html')
        html = build(c)
        io.open(destino, 'w', encoding='utf-8').write(html)
        print('  %-22s %6.1f KB' % (c['slug'] + '.html', len(html) / 1024))
