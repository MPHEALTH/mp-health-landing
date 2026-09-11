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
  # Acento: cada condicion toma uno de la paleta terrosa, como las de diagnosticos
  'acc': 'rose', 'acc2': 'sage', 'acc3': 'ochre', 'acc_ink': '#7d443c',
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
# El sistema visual no se inventa aqui: es el mismo de diagnosticos.html y el
# landing — fondo arena con manchas de color que derivan, helice de ADN detras
# y tarjetas de vidrio. Los tokens y la receta del vidrio estan copiados tal cual
# para que las paginas de patologia no parezcan de otra marca.
CSS = """
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
 --sand:#f5f1ea;--sand2:#ece5da;--ink:#1e2a35;--ink-soft:#4b5761;
 --line:rgba(30,42,53,.10);--accent:#0a5b4d;
 --sage:#7fa89b;--ochre:#c39a63;--slate:#8098b0;--rose:#b8837c;--deep:#38505e;
 --font-body:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;
 --font-serif:'Cormorant Garamond',Georgia,serif}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{font-family:var(--font-body);color:var(--ink);line-height:1.65;
 overflow-x:hidden;background:var(--sand);position:relative}
img{max-width:100%;display:block}
.wrap{max-width:1120px;margin:0 auto;padding:0 28px}
section{padding:92px 0}
@media(max-width:720px){section{padding:60px 0}.wrap{padding:0 20px}}

/* ── Fondo vivo: manchas que derivan + helice de ADN ── */
.bg{position:fixed;inset:0;z-index:-2;overflow:hidden;pointer-events:none}
.blob{position:absolute;border-radius:50%;filter:blur(90px);opacity:.5;will-change:transform}
.blob.b1{width:46vw;height:46vw;background:var(--c1);top:-14%;left:-8%;animation:drift1 26s ease-in-out infinite}
.blob.b2{width:40vw;height:40vw;background:var(--c2);top:-6%;right:-6%;animation:drift2 32s ease-in-out infinite}
.blob.b3{width:44vw;height:44vw;background:var(--c3);bottom:-16%;left:28%;animation:drift3 29s ease-in-out infinite}
.blob.b4{width:34vw;height:34vw;background:var(--slate);bottom:6%;right:12%;animation:drift4 35s ease-in-out infinite}
@keyframes drift1{0%,100%{transform:translate(0,0) scale(1)}50%{transform:translate(9vw,7vh) scale(1.14)}}
@keyframes drift2{0%,100%{transform:translate(0,0) scale(1.08)}50%{transform:translate(-8vw,9vh) scale(.94)}}
@keyframes drift3{0%,100%{transform:translate(0,0) scale(1)}50%{transform:translate(7vw,-8vh) scale(1.16)}}
@keyframes drift4{0%,100%{transform:translate(0,0) scale(1.05)}50%{transform:translate(-10vw,-6vh) scale(.92)}}
.helix{position:fixed;inset:0;z-index:-1;pointer-events:none;opacity:.16}
.helix .tilt{transform:rotate(-7deg) scale(1.25);transform-origin:50% 50%}
.helix svg{width:100%;height:100%}
.helix .strand{fill:none;stroke:var(--ink);stroke-width:1.4;stroke-opacity:.55}
.helix .layer{animation:slide 34s linear infinite}
.helix .layer.slow{animation-duration:52s;opacity:.6}
@keyframes slide{from{transform:translateX(0)}to{transform:translateX(-1440px)}}
@media(max-width:720px){.blob{filter:blur(70px);opacity:.42}.helix{opacity:.07}}
@media(prefers-reduced-motion:reduce){.blob,.helix .layer{animation:none!important}}

/* ── Vidrio ── */
.glass{
 background:rgba(255,255,255,.52);
 backdrop-filter:blur(26px) saturate(165%);
 -webkit-backdrop-filter:blur(26px) saturate(165%);
 border:1px solid rgba(255,255,255,.62);
 box-shadow:inset 0 1px 0 rgba(255,255,255,.85),
            inset 0 -1px 0 rgba(255,255,255,.28),
            0 20px 50px rgba(30,42,53,.08);
 border-radius:22px}
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){
 .glass,.nav-glass{background:rgba(255,255,255,.92)!important}}

h1,h2,h3{font-family:var(--font-serif);font-weight:400;line-height:1.12;
 color:var(--ink);letter-spacing:-.012em}
h1{font-size:clamp(2.3rem,5vw,3.9rem)}
h2{font-size:clamp(1.8rem,3.6vw,2.75rem)}
.label{display:inline-block;font-size:.66rem;letter-spacing:.24em;text-transform:uppercase;
 color:var(--acc-ink);font-weight:600;margin-bottom:18px}
.lede{font-size:1.03rem;color:var(--ink-soft);line-height:1.85;font-weight:300}

/* ── Nav ── */
.nav{position:sticky;top:0;z-index:90;padding:12px 0}
.nav-glass{position:absolute;inset:12px 28px auto;height:calc(100% - 24px);
 background:rgba(255,255,255,.55);
 backdrop-filter:blur(22px) saturate(170%);-webkit-backdrop-filter:blur(22px) saturate(170%);
 border:1px solid rgba(255,255,255,.6);border-radius:100px;
 box-shadow:inset 0 1px 0 rgba(255,255,255,.85),0 8px 26px rgba(30,42,53,.07);
 pointer-events:none}
.nav-row{position:relative;z-index:1;display:flex;align-items:center;justify-content:space-between;
 max-width:1120px;margin:0 auto;padding:0 46px;gap:14px}
.nav-logo{height:104px;width:auto}
.nav-r{display:flex;align-items:center;gap:18px}
.nav-tel{font-size:.79rem;color:var(--ink-soft);text-decoration:none}
.nav-tel:hover{color:var(--ink)}
.nav-cta{background:rgba(30,42,53,.92);color:#fff;text-decoration:none;padding:11px 22px;
 border-radius:100px;font-size:.79rem;font-weight:600;white-space:nowrap;
 transition:background .2s,transform .2s;backdrop-filter:blur(10px);border:none;cursor:pointer;
 font-family:var(--font-body)}
.nav-cta:hover{background:var(--ink);transform:translateY(-1px)}
@media(max-width:720px){.nav-row{padding:0 24px}.nav-logo{height:74px}
 .nav-cta{padding:10px 16px;font-size:.73rem}.nav-tel{display:none}}

/* ── Boton ── */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;
 background:var(--acc-ink);color:#fff;font-family:var(--font-body);font-weight:600;
 font-size:.92rem;padding:16px 34px;border-radius:100px;text-decoration:none;border:none;
 cursor:pointer;transition:transform .2s,box-shadow .2s,filter .2s;
 box-shadow:0 10px 28px rgba(30,42,53,.16)}
.btn:hover{transform:translateY(-2px);filter:brightness(1.12);box-shadow:0 14px 34px rgba(30,42,53,.22)}
.btn-lg{font-size:1rem;padding:19px 42px}

/* ── Hero ── */
.hero{padding:64px 0 40px}
.hero-in{display:grid;grid-template-columns:1.05fr .95fr;gap:46px;align-items:center}
.hero h1 em{font-style:italic;color:var(--acc-ink)}
.hero .lede{margin:26px 0 32px;max-width:520px}
.hero-img{border-radius:22px;overflow:hidden;box-shadow:0 26px 60px rgba(30,42,53,.14);
 aspect-ratio:4/5;background:var(--sand2)}
.hero-img img{width:100%;height:100%;object-fit:cover}
.trust{display:flex;align-items:flex-start;gap:9px;margin-top:24px;font-size:.82rem;
 color:var(--ink-soft);line-height:1.6;max-width:480px}
.trust svg{flex:0 0 15px;color:var(--acc-ink);margin-top:3px}
@media(max-width:880px){.hero-in{grid-template-columns:1fr;gap:34px}
 .hero-img{aspect-ratio:16/11;order:-1}.hero{padding:34px 0 20px}}

/* ── Banda de datos ── */
.proof{padding:0 0 20px}
.proof-in{display:flex;justify-content:space-around;gap:18px;flex-wrap:wrap;
 padding:26px 34px;text-align:center}
.proof b{display:block;font-family:var(--font-serif);font-size:1.9rem;color:var(--acc-ink);font-weight:600}
.proof span{display:block;font-size:.72rem;color:var(--ink-soft);line-height:1.5;margin-top:2px}

/* ── Dato clinico ── */
.dato-card{padding:52px 56px}
.dato-card p{font-size:1.01rem;line-height:1.9;color:var(--ink-soft);font-weight:300;margin-top:20px}
.dato-card p b{color:var(--ink);font-weight:600}
.dato-nota{margin-top:30px;padding-top:24px;border-top:1px solid var(--line);
 font-size:.87rem;color:var(--ink-soft);line-height:1.75;font-style:italic}
@media(max-width:720px){.dato-card{padding:34px 24px}}

/* ── Que medimos ── */
.med-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(248px,1fr));gap:20px;margin-top:48px}
.med-card{padding:30px 28px}
.med-card h3{font-size:1.12rem;color:var(--acc-ink);margin-bottom:12px;line-height:1.3}
.med-card p{font-size:.92rem;line-height:1.8;color:var(--ink-soft);font-weight:300}

/* ── Pasos ── */
.pasos-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(246px,1fr));gap:20px;margin-top:48px}
.paso{padding:30px 28px}
.paso-n{font-family:var(--font-serif);font-size:2.5rem;color:var(--acc-ink);line-height:1}
.paso h3{font-size:1.1rem;margin:10px 0 10px}
.paso p{font-size:.92rem;line-height:1.8;color:var(--ink-soft);font-weight:300}

/* ── FAQ ── */
.faq-list{margin-top:44px;max-width:840px;padding:8px 34px}
.faq-i{border-bottom:1px solid var(--line)}
.faq-i:last-child{border-bottom:none}
.faq-q{width:100%;display:flex;align-items:center;gap:16px;text-align:left;background:none;
 border:none;cursor:pointer;padding:24px 0;font-family:var(--font-body);font-size:1rem;
 font-weight:600;color:var(--ink);line-height:1.45}
.faq-q span{flex:1}
.faq-ico{flex:0 0 18px;color:var(--acc-ink);transition:transform .22s}
.faq-i.open .faq-ico{transform:rotate(45deg)}
.faq-a{display:none;padding:0 0 24px;font-size:.95rem;line-height:1.9;color:var(--ink-soft);
 font-weight:300;max-width:700px}
.faq-i.open .faq-a{display:block}
.faq-a b{color:var(--ink);font-weight:600}
@media(max-width:720px){.faq-list{padding:4px 22px}}

/* ── Cierre ── */
.cierre-card{padding:64px 56px;text-align:center}
.cierre-card .lede{max-width:600px;margin:22px auto 38px}
@media(max-width:720px){.cierre-card{padding:44px 24px}}

/* ── Footer ── */
.foot{padding:48px 28px 40px;text-align:center}
.foot img{height:40px;width:auto;margin:0 auto 20px;opacity:.55}
.foot a{color:var(--ink-soft);font-size:.79rem;text-decoration:none;margin:0 12px}
.foot a:hover{color:var(--acc-ink)}
.foot small{display:block;margin-top:18px;font-size:.72rem;color:var(--ink-soft);opacity:.65}

/* ── WhatsApp ── */
.wa{position:fixed;right:20px;bottom:20px;z-index:80;display:flex;align-items:center;gap:9px;
 background:rgba(255,255,255,.72);backdrop-filter:blur(20px) saturate(160%);
 -webkit-backdrop-filter:blur(20px) saturate(160%);border:1px solid rgba(255,255,255,.7);
 color:var(--ink);padding:13px 20px;border-radius:100px;text-decoration:none;
 font-size:.85rem;font-weight:600;box-shadow:0 12px 32px rgba(30,42,53,.14)}
.wa svg{width:19px;height:19px;color:#25d366}
@media(max-width:720px){.wa span{display:none}.wa{padding:15px}}
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
        '        <div class="med-card glass"><h3>%s</h3><p>%s</p></div>' % (h, p)
        for h, p in c['medimos'])

    pasos = '\n'.join(
        '        <div class="paso glass"><div class="paso-n">%d</div><h3>%s</h3><p>%s</p></div>'
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
        acc=c['acc'], acc2=c['acc2'], acc3=c['acc3'], acc_ink=c['acc_ink'],
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
:root{{--c1:var(--{acc});--c2:var(--{acc2});--c3:var(--{acc3});--acc-ink:{acc_ink}}}
{modal_css}
</style>
</head>
<body>

<div class="bg" aria-hidden="true">
  <span class="blob b1"></span><span class="blob b2"></span>
  <span class="blob b3"></span><span class="blob b4"></span>
</div>
  <div class="helix" aria-hidden="true">
    <svg viewBox="0 0 2880 1620" preserveAspectRatio="xMidYMid slice">
      <g class="tilt">
        <g class="layer"><path class="strand" d="M0,300 C240,205 480,205 720,300 C960,395 1200,395 1440,300 C1680,205 1920,205 2160,300 C2400,395 2640,395 2880,300 C3120,205 3360,205 3600,300 C3840,395 4080,395 4320,300"/><path class="strand" d="M0,300 C240,395 480,395 720,300 C960,205 1200,205 1440,300 C1680,395 1920,395 2160,300 C2400,205 2640,205 2880,300 C3120,395 3360,395 3600,300 C3840,205 4080,205 4320,300"/></g>
        <g class="layer slow"><path class="strand" d="M0,880 C240,750 480,750 720,880 C960,1010 1200,1010 1440,880 C1680,750 1920,750 2160,880 C2400,1010 2640,1010 2880,880 C3120,750 3360,750 3600,880 C3840,1010 4080,1010 4320,880"/><path class="strand" d="M0,880 C240,1010 480,1010 720,880 C960,750 1200,750 1440,880 C1680,1010 1920,1010 2160,880 C2400,750 2640,750 2880,880 C3120,1010 3360,1010 3600,880 C3840,750 4080,750 4320,880"/></g>
        <g class="layer"><path class="strand" d="M0,1420 C240,1315 480,1315 720,1420 C960,1525 1200,1525 1440,1420 C1680,1315 1920,1315 2160,1420 C2400,1525 2640,1525 2880,1420 C3120,1315 3360,1315 3600,1420 C3840,1525 4080,1525 4320,1420"/><path class="strand" d="M0,1420 C240,1525 480,1525 720,1420 C960,1315 1200,1315 1440,1420 C1680,1525 1920,1525 2160,1420 C2400,1315 2640,1315 2880,1420 C3120,1525 3360,1525 3600,1420 C3840,1315 4080,1315 4320,1420"/></g>
      </g>
    </svg>
  </div>

<nav class="nav">
  <div class="nav-glass"></div>
  <div class="nav-row">
    <a href="index.html"><img src="images/LOGO%20%286%29.png" alt="Michelle Peiret Health" class="nav-logo" style="filter:invert(1) brightness(.22)"></a>
    <div class="nav-r">
      <a href="tel:{tel_h}" class="nav-tel">{tel}</a>
      <a href="empezar.html?objetivo={objetivo}" class="nav-cta">{cta} &rarr;</a>
    </div>
  </div>
</nav>

<section class="hero">
  <div class="wrap hero-in">
    <div>
      <span class="label">{eyebrow}</span>
      <h1>{h1a}<br><em>{h1b}</em><br>{h1c}</h1>
      <p class="lede">{sub}</p>
      <a href="empezar.html?objetivo={objetivo}" class="btn btn-lg">{cta} &rarr;</a>
      <p class="trust">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
        {trust}
      </p>
    </div>
    <div class="hero-img"><img src="{hero_img}" alt="{hero_alt}"></div>
  </div>
</section>

<div class="proof">
  <div class="wrap">
    <div class="proof-in glass">
      <div><b>900+</b><span>Biomarcadores<br>en tu evaluaci&oacute;n</span></div>
      <div><b>7</b><span>Especialistas<br>leyendo tu caso</span></div>
      <div><b>+7,000</b><span>Personas ya<br>tienen sus datos</span></div>
      <div><b>+15</b><span>A&ntilde;os leyendo<br>biolog&iacute;a humana</span></div>
    </div>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="dato-card glass">
      <span class="label">{dato_label}</span>
      <h2>{dato_h}</h2>
{dato}
      <p class="dato-nota">{dato_nota}</p>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="label">{medimos_label}</span>
    <h2>{medimos_h}</h2>
    <div class="med-grid">
{medimos}
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="label">C&oacute;mo empieza</span>
    <h2>Tres pasos, y el primero<br>toma dos minutos</h2>
    <div class="pasos-grid">
{pasos}
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="label">Antes de decidir</span>
    <h2>Lo que la gente pregunta</h2>
    <div class="faq-list glass">
{faq}
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="cierre-card glass">
      <h2>{cierre_h}</h2>
      <p class="lede">{cierre_p}</p>
      <a href="empezar.html?objetivo={objetivo}" class="btn btn-lg">{cta} &rarr;</a>
    </div>
  </div>
</section>

<footer class="foot">
  <img src="images/LOGO%20%286%29.png" alt="Michelle Peiret Health" style="filter:invert(1) brightness(.3)">
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
  <span>Escr&iacute;benos</span>
</a>

<script>
  /* El modal lo lee para abrir el formulario con la condici\u00f3n ya respondida */
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
