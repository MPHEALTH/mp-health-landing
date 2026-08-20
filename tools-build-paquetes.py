#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera las tres páginas de paquetes MP a partir de una plantilla común."""
import io, os

OUT = "/Users/eliasabdou/Downloads/CLAUDE BRAIN/MP HEALTH/web mockups/mp-health-landing"

WA = "https://wa.me/17869302544?text="
TEL = "+1 (786) 930-2544"

HEAD = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="icon" type="image/png" href="images/LOGO%20%286%29.png">
  <link rel="stylesheet" href="css/paquete.css">
  <link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet">
  <script src="https://assets.calendly.com/assets/external/widget.js" defer></script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-B7PSHFCHGY"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-B7PSHFCHGY');
  </script>
</head>
<body>

  <div class="bg" aria-hidden="true">
    <span class="blob b1"></span><span class="blob b2"></span>
    <span class="blob b3"></span><span class="blob b4"></span>
  </div>

  <div class="helix" aria-hidden="true">
    <svg viewBox="0 0 2880 1620" preserveAspectRatio="xMidYMid slice">
      <g class="tilt">
        <g class="layer"><path class="strand" d="M0,300 C240,205 480,205 720,300 C960,395 1200,395 1440,300 C1680,205 1920,205 2160,300 C2400,395 2640,395 2880,300 C3120,205 3360,205 3600,300 C3840,395 4080,395 4320,300"/>
          <path class="strand" d="M0,300 C240,395 480,395 720,300 C960,205 1200,205 1440,300 C1680,395 1920,395 2160,300 C2400,205 2640,205 2880,300 C3120,395 3360,395 3600,300 C3840,205 4080,205 4320,300"/></g>
        <g class="layer slow"><path class="strand" d="M0,880 C240,1010 480,1010 720,880 C960,750 1200,750 1440,880 C1680,1010 1920,1010 2160,880 C2400,750 2640,750 2880,880 C3120,1010 3360,1010 3600,880 C3840,750 4080,750 4320,880"/>
          <path class="strand" d="M0,880 C240,750 480,750 720,880 C960,1010 1200,1010 1440,880 C1680,750 1920,750 2160,880 C2400,1010 2640,1010 2880,880 C3120,750 3360,750 3600,880 C3840,1010 4080,1010 4320,880"/></g>
        <g class="layer"><path class="strand" d="M0,1420 C240,1315 480,1315 720,1420 C960,1525 1200,1525 1440,1420 C1680,1315 1920,1315 2160,1420 C2400,1525 2640,1525 2880,1420 C3120,1315 3360,1315 3600,1420 C3840,1525 4080,1525 4320,1420"/>
          <path class="strand" d="M0,1420 C240,1525 480,1525 720,1420 C960,1315 1200,1315 1440,1420 C1680,1525 1920,1525 2160,1420 C2400,1315 2640,1315 2880,1420 C3120,1525 3360,1525 3600,1420 C3840,1315 4080,1315 4320,1420"/></g>
      </g>
    </svg>
  </div>

  <nav class="nav">
    <div class="nav-glass"></div>
    <div class="nav-row">
      <a href="diagnosticos.html"><img src="images/LOGO%20%286%29.png" alt="Michelle Peiret Health" class="nav-logo"></a>
      <div class="nav-right">
        <a href="diagnosticos.html" class="nav-back">← Todos los diagnósticos</a>
        <a href="#agendar" class="nav-cta">Agendar mi llamada</a>
      </div>
    </div>
  </nav>
"""

HERO = """
  <header class="pk-hero">
    <div class="wrap">
      <div class="pk-eyebrow"><span>Paquete · {tipo}</span></div>
      <h1>{h1}</h1>
      <p class="pk-name">{nombre}</p>
      <p class="lede">{sub}</p>

      <div class="pk-priceline">
        <span class="pk-price">${precio}</span>
        <span class="pk-price-note">{price_note}</span>
        {save}
      </div>

      <div class="pk-chips">{chips}</div>

      <div class="pk-actions">
        <a href="#agendar" class="btn-primary">Agendar mi llamada de 15 min →</a>
        <a href="#incluye" class="btn-ghost">Ver qué incluye</a>
      </div>
    </div>
  </header>
"""

INCLUYE = """
  <section id="incluye">
    <div class="wrap">
      <div style="max-width:660px" class="fade">
        <span class="label">Qué incluye</span>
        <h2>{inc_h2}</h2>
        <p class="lede" style="margin-top:15px;">{inc_p}</p>
      </div>

      <div class="inc-grid">
{cards}
      </div>

      <div class="sum glass fade">
        <span class="sum-l">{sum_l}</span>
        <span class="sum-r">{sum_r}</span>
      </div>
    </div>
  </section>
"""

DIA = """
  <section style="padding-top:0;">
    <div class="wrap">
      <div class="guide-card glass fade" style="padding:46px 44px;">
        <div style="max-width:640px">
          <span class="label">{dia_label}</span>
          <h2>{dia_h2}</h2>
        </div>
        <div class="day">
{rows}
        </div>
      </div>
    </div>
  </section>
"""

QUIEN = """
  <section style="padding-top:0;">
    <div class="wrap">
      <div style="max-width:640px" class="fade">
        <span class="label">Para quién es</span>
        <h2>{q_h2}</h2>
      </div>
      <div class="who-grid">
        <div class="who si glass fade">
          <h3>Este paquete es para ti si</h3>
          <ul>{si}</ul>
        </div>
        <div class="who no glass fade">
          <h3>Quizá te conviene otra cosa si</h3>
          <ul>{no}</ul>
        </div>
      </div>
    </div>
  </section>
"""

FAQ = """
  <section style="padding-top:0;">
    <div class="wrap">
      <div style="text-align:center" class="fade">
        <span class="label">Preguntas frecuentes</span>
        <h2>Antes de reservar</h2>
      </div>
      <div class="faq glass fade" style="padding:14px 36px;">
{items}
      </div>
    </div>
  </section>
"""

BOOK = """
  <section id="agendar">
    <div class="wrap">
      <div class="book glass fade">
        <h2>Reserva tu {nombre}</h2>
        <p class="lede">Empezamos con una llamada de 15 minutos para confirmar que este paquete
        es el correcto para tu caso y coordinar tu fecha. Sin costo y sin compromiso.</p>

        <div class="pk-step on" id="pkStep1">
          <form id="pkForm" novalidate>
            <div class="fld-row">
              <div class="fld">
                <label for="pkName">Nombre y apellido</label>
                <input type="text" id="pkName" autocomplete="name" placeholder="Tu nombre completo">
                <div class="err" id="errName">Escribe tu nombre y apellido</div>
              </div>
              <div class="fld">
                <label for="pkEmail">Email</label>
                <input type="email" id="pkEmail" autocomplete="email" inputmode="email"
                       autocapitalize="none" autocorrect="off" spellcheck="false" placeholder="tu@email.com">
                <div class="err" id="errEmail">Revisa tu email — parece incompleto</div>
              </div>
            </div>

            <div class="fld-row">
              <div class="fld">
                <label for="pkPhone">Teléfono / WhatsApp</label>
                <input type="tel" id="pkPhone" autocomplete="tel" inputmode="tel" placeholder="+1 786 000 0000">
                <div class="err" id="errPhone">Necesitamos un teléfono válido</div>
              </div>
              <div class="fld">
                <label for="pkWhen">¿Cuándo te gustaría hacerlo?</label>
                <select id="pkWhen">
                  <option value="">Selecciona…</option>
                  <option value="Esta semana">Esta semana</option>
                  <option value="En las próximas 2 semanas">En las próximas 2 semanas</option>
                  <option value="Este mes">Este mes</option>
                  <option value="Todavía estoy evaluando">Todavía estoy evaluando</option>
                </select>
                <div class="err" id="errWhen">Elige una opción</div>
              </div>
            </div>

            <div class="fld">
              <label for="pkLoc">¿Desde dónde nos escribes?</label>
              <input type="text" id="pkLoc" placeholder="Ciudad y país">
            </div>

            <div class="fld">
              <label for="pkCase">¿Qué quieres resolver? <span style="font-weight:400;color:var(--ink-soft);">(opcional)</span></label>
              <textarea id="pkCase" placeholder="Síntomas, diagnósticos previos, qué has intentado — lo que nos ayude a llegar preparados."></textarea>
            </div>

            <div class="err" id="errForm"></div>

            <div class="pk-nav">
              <span style="font-size:0.8rem;color:var(--ink-soft);">Llamada de 15 min · sin costo</span>
              <button type="submit" class="btn-primary" id="pkSubmit">Agendar mi llamada →</button>
            </div>
          </form>
        </div>

        <div class="pk-done" id="pkDone">
          <div class="pk-done-mark">✓</div>
          <h2 style="font-size:1.6rem;">Recibimos tus datos</h2>
          <p class="lede" style="margin-top:10px;">Elige abajo el horario que mejor te funcione.</p>
          <div id="pkCalWrap"></div>
        </div>

        <div class="trust">
          <span>Tus datos son confidenciales</span>
          <span>Sin compromiso</span>
          <span>Se acredita a tu tratamiento</span>
        </div>
      </div>
    </div>
  </section>
"""

ALT = """
  <section style="padding-top:0;">
    <div class="wrap">
      <div style="max-width:640px" class="fade">
        <span class="label">Otros paquetes</span>
        <h2>¿No es este el tuyo?</h2>
      </div>
      <div class="alt-grid">
{alts}
      </div>
    </div>
  </section>
"""

FOOT = """
  <footer>
    <div class="wrap">
      <img src="images/LOGO%20%286%29.png" alt="Michelle Peiret Health">
      <p>760 NW 107th Ave, Suite #340, Miami FL 33172</p>
      <p>WhatsApp <a href="https://wa.me/17869302544">+1 (786) 930-2544</a> · <a href="https://www.michellepeiret.com">michellepeiret.com</a></p>
      <p class="small">Los diagnósticos MP no sustituyen una consulta médica ni constituyen un diagnóstico clínico.
      Sus resultados se interpretan siempre con un especialista del equipo.</p>
    </div>
  </footer>

  <a class="wa-fab" href="{wa}" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp">
    <svg viewBox="0 0 24 24"><path d="M17.5 14.4c-.3-.2-1.8-.9-2-1-.3-.1-.5-.2-.7.1-.2.3-.7 1-.9 1.2-.2.2-.3.2-.6.1-.3-.2-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.5-.5c.1-.2.2-.3.3-.5 0-.2 0-.4 0-.5 0-.2-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.3.2-1.4-.1-.1-.3-.2-.6-.4M12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2m0 18.2c-1.6 0-3.2-.4-4.5-1.3l-.3-.2-3.1.8.8-3-.2-.3a8.2 8.2 0 1 1 7.3 4"/></svg>
    <span>Escríbenos por WhatsApp</span>
  </a>

  <script>window.PAQUETE = {cfg};</script>
  <script src="js/paquete.js" defer></script>
</body>
</html>
"""


def card(cls, tag, val, tl, body, link=None, img=None):
    l = ('\n          <a class="inc-link" href="%s">%s →</a>' % link) if link else ''
    if img:
        top = ('          <div class="inc-img"><img src="%s" alt="%s" loading="lazy">'
               '<span class="inc-dot"></span></div>\n' % img)
    else:
        top = '          <div class="inc-dot"></div>\n'
    return ('        <div class="inc %s glass fade">\n'
            '%s'
            '          <div class="inc-top"><h3>%s</h3><span class="inc-val">%s</span></div>\n'
            '          <p class="inc-tl">%s</p>\n'
            '          <p>%s</p>%s\n'
            '        </div>' % (cls, top, tag, val, tl, body, l))


def rows(items):
    return '\n'.join(
        '          <div class="day-row"><span class="day-num">%02d</span>'
        '<div><b>%s</b><span>%s</span></div></div>' % (i + 1, a, b)
        for i, (a, b) in enumerate(items))


def lis(items):
    return ''.join('<li>%s</li>' % i for i in items)


def faqs(items):
    return '\n'.join(
        '        <div class="faq-item">\n'
        '          <button class="faq-q" type="button">%s</button>\n'
        '          <div class="faq-a"><p>%s</p></div>\n'
        '        </div>' % (q, a) for q, a in items)


def alts(items):
    return '\n'.join(
        '        <a class="alt glass fade" href="%s">\n'
        '          <div class="alt-top"><h3>%s</h3><span class="alt-price">%s</span></div>\n'
        '          <p class="alt-tl">%s</p>\n'
        '          <p>%s</p>\n'
        '          <span class="alt-go">Ver el paquete →</span>\n'
        '        </a>' % it for it in items)


def build(p):
    html = HEAD.format(title=p['title'], desc=p['desc'])
    html += HERO.format(h1=p['h1'], sub=p['sub'], precio=p['precio'],
                        tipo=p['tipo'], nombre=p['nombre'],
                        price_note=p['price_note'], save=p.get('save', ''),
                        chips=''.join('<span class="pk-chip">%s</span>' % c for c in p['chips']))
    html += INCLUYE.format(inc_h2=p['inc_h2'], inc_p=p['inc_p'],
                           cards='\n'.join(card(*c) for c in p['cards']),
                           sum_l=p['sum_l'], sum_r=p['sum_r'])
    html += DIA.format(dia_label=p['dia_label'], dia_h2=p['dia_h2'], rows=rows(p['dia']))
    html += QUIEN.format(q_h2=p['q_h2'], si=lis(p['si']), no=lis(p['no']))
    html += FAQ.format(items=faqs(p['faq']))
    html += BOOK.format(nombre=p['nombre'])
    html += ALT.format(alts=alts(p['alts']))
    html += FOOT.format(wa=p['wa'], cfg=p['cfg'])
    path = os.path.join(OUT, p['file'])
    io.open(path, 'w', encoding='utf-8').write(html)
    print('escrito: %s  (%d KB)' % (p['file'], len(html) // 1024))


# ══════════════════════════════════════════════════════════════
#  1 · PUNTO DE PARTIDA MP — $540
# ══════════════════════════════════════════════════════════════
PUNTO = dict(
    file='paquete-punto-de-partida.html',
    nombre='Punto de Partida MP',
    tipo='Diagnóstico inicial',
    title='Punto de Partida MP — $540 | Michelle Peiret Health',
    desc='BioScan e InBody con tu consulta de interpretación. El paquete para empezar a cuidarte con datos, no con suposiciones. Se acredita íntegro a tu tratamiento.',
    h1='Empieza por<br>saber <em>dónde estás</em>',
    sub='La mayoría de la gente que quiere cuidarse no sabe por dónde empezar, así que empieza por lo que vio en redes. Este paquete invierte el orden: primero mides, después decides. <strong>900+ biomarcadores desde tu casa y la composición real de tu cuerpo</strong>, leídos contigo por un especialista.',
    precio='540',
    price_note='· BioScan + InBody + consulta de interpretación',
    save='',
    chips=['Miami u online', 'Kit a domicilio', 'Sin agujas', 'Se acredita íntegro'],
    inc_h2='Dos estudios que se complementan',
    inc_p='Uno mira hacia adentro, a nivel celular. El otro mide de qué está hecho tu cuerpo por fuera. Juntos te dan el punto de partida completo, y ninguno requiere una aguja.',
    cards=[
        ('bioscan', 'BioScan', '$447 por separado',
         '900+ biomarcadores desde cuatro hebras de cabello',
         'Deficiencias de vitaminas y minerales, hormonas, microbiota, carga de toxinas y sensibilidad a 115+ alimentos. El kit llega a tu casa, envías la muestra y en 7 a 10 días tienes el informe.',
         ('https://bioscan.michellepeiret.com/', 'Ver el BioScan'),
         ('images/bioscan-muestra.jpg', 'Toma de la muestra de cabello para el BioScan')),
        ('inbody', 'InBody 970S', '$95 por separado',
         'De qué está hecho tu peso, por segmento',
         'Músculo, grasa, grasa visceral, agua celular y proteína, medidos brazo por brazo y pierna por pierna en 30 segundos. Resultados al instante, sin radiación.',
         ('inbody.html', 'Ver el InBody'),
         ('images/inbody-centro.jpg', 'Medición de composición corporal en el InBody 970S')),
        ('consulta', 'Interpretación', 'Incluida',
         'Tus resultados, explicados por un especialista',
         'Media hora para entender qué dicen tus dos informes, qué está fuera de rango y qué hacer al respecto. Un dato sin lectura no cambia nada.',
         None,
         ('images/paso2-michelle-consulta.jpg', 'Consulta de interpretación con Michelle Peiret')),
        ('iv', 'Crédito', 'El 100 %',
         'Los $540 se descuentan de tu tratamiento',
         'Si decides iniciar un tratamiento nutricional personalizado dentro de los 60 días siguientes, el monto completo del paquete se acredita. En la práctica, los estudios te salen gratis.',
         None,
         ('images/centro-equipo.jpg', 'Equipo clínico del centro MP Health')),
    ],
    sum_l='<b>BioScan $447</b> + <b>InBody $95</b> por separado, con sus consultas',
    sum_r='<s>$542</s>$540',
    dia_label='Cómo funciona',
    dia_h2='De la llamada al informe',
    dia=[
        ('Llamada de 15 minutos',
         'Confirmamos que este es el paquete correcto para ti y resolvemos tus dudas. Sin costo y sin compromiso.'),
        ('Te llega el kit del BioScan',
         'A tu casa, con instrucciones. Cortas cuatro hebras de cabello, las envías en el sobre prepagado y listo.'),
        ('Tu InBody en el centro',
         'Quince minutos en Miami, descalzo y sin joyas. Los resultados salen impresos en el momento. Si estás fuera de Miami, coordinamos esta parte cuando puedas venir.'),
        ('Tu consulta de interpretación',
         'Cuando el informe del BioScan está listo, un especialista se sienta contigo — presencial u online — a leer ambos estudios y darte el plan de acción.'),
    ],
    q_h2='Un punto de partida, no un tratamiento',
    si=[
        'Quieres empezar a cuidarte en serio pero no sabes por dónde',
        'Tomas suplementos sin saber si de verdad los necesitas',
        'Te sientes mal y tus análisis de rutina «salen bien»',
        'Quieres saber si lo que pierdes es grasa o músculo',
        'Prefieres empezar sin agujas y buena parte desde casa',
    ],
    no=[
        'Necesitas medir hormonas específicas en sangre — ahí va el <em>Panel de Sangre Hormonal MP</em>',
        'Entrenas en serio y buscas rendimiento — mira el <em>Atleta MP</em>',
        'Quieres la fotografía completa de una vez — ese es el <em>Mapa Biológico MP</em>',
        'Buscas ya un tratamiento con seguimiento, no un diagnóstico',
    ],
    faq=[
        ('¿Necesito ir a Miami?',
         'Para el BioScan no: el kit llega a tu casa y la consulta puede ser online. El InBody sí es presencial, porque requiere el equipo del centro. Si vives fuera, puedes hacer el BioScan de inmediato y dejar el InBody para cuando vengas — o hablar con nosotros sobre hacer solo el BioScan.'),
        ('¿Qué significa que se acredita íntegro?',
         'Que si dentro de los 60 días siguientes decides iniciar un tratamiento nutricional personalizado con nosotros, los $540 se descuentan del precio del tratamiento. No es un descuento parcial: es el monto completo.'),
        ('¿Cuánto tardan los resultados?',
         'El InBody es inmediato, sales del centro con las hojas en la mano. El BioScan tarda entre 7 y 10 días desde que el laboratorio recibe tu muestra. La consulta de interpretación se agenda cuando ambos están listos.'),
        ('¿El BioScan reemplaza un análisis de sangre?',
         'No, mide cosas distintas. El cabello muestra qué ha pasado a nivel celular durante meses; la sangre muestra el momento actual y marcadores clínicos que el cabello no ve. Si necesitas valores clínicos, lo tuyo es un Panel de Sangre MP.'),
        ('¿Puedo pagar en cuotas?',
         'Escríbenos por WhatsApp y lo vemos según el caso. En la llamada de 15 minutos también podemos revisar las opciones disponibles.'),
    ],
    alts=[
        ('paquete-atleta.html', 'Atleta MP', '$895', 'Tu rendimiento, medido y optimizado.',
         'Metabólico con VO2 Max, panel de sangre completo, InBody y una sesión de IV Therapy de recuperación.'),
        ('paquete-mapa-biologico.html', 'Mapa Biológico MP', '$1,200', 'La fotografía completa de tu biología.',
         'Los cuatro estudios en una sola visita: BioScan, sangre, metabólico e InBody.'),
    ],
    wa=WA + 'Hola%2C%20quiero%20informaci%C3%B3n%20del%20Punto%20de%20Partida%20MP',
    cfg="{ nombre: 'Punto de Partida MP', precio: '$540', valor: 540, slug: 'punto_de_partida', calendly: '' }",
)

# ══════════════════════════════════════════════════════════════
#  2 · ATLETA MP — $895
# ══════════════════════════════════════════════════════════════
ATLETA = dict(
    file='paquete-atleta.html',
    nombre='Atleta MP',
    tipo='Diagnóstico para atletas',
    title='Atleta MP — $895 | Michelle Peiret Health',
    desc='Análisis Metabólico con VO2 Max, panel de sangre completo, InBody y una sesión de IV Therapy de recuperación. Con interpretación de un especialista.',
    h1='Deja de entrenar<br><em>a ciegas</em>',
    sub='Puedes entrenar duro durante años y estancarte por algo que nunca mediste: una zona de esfuerzo mal calculada, un hierro bajo, un déficit calórico que te está costando músculo. <strong>Este paquete mide tu motor, tu sangre y tu composición</strong>, y cierra con una sesión de recuperación.',
    precio='895',
    price_note='· cuatro servicios con tu consulta de interpretación',
    save='<span class="pk-save">Ahorras desde $150</span>',
    chips=['Presencial en Miami', 'VO2 Max real', 'IV Therapy incluida', 'Se acredita íntegro'],
    inc_h2='Tu motor, tu química y tu chasis',
    inc_p='El metabólico mide cómo produces energía. La sangre, con qué materia prima cuentas. El InBody, qué estás construyendo o perdiendo. La IV Therapy cierra el día ayudándote a recuperar.',
    cards=[
        ('metab', 'Análisis Metabólico MP', '$350 por separado',
         'Tu VO2 max y tus zonas reales de entrenamiento',
         'Dos pruebas con tecnología PNOĒ, en reposo y en esfuerzo: tus calorías y macros reales, tu VO2 max, tus zonas de frecuencia cardíaca y tu edad biológica. Respirando por una mascarilla.',
         ('metabolico.html', 'Ver el Análisis Metabólico'),
         ('images/centro-vo2max.jpg', 'Prueba de VO2 max con mascarilla PNOĒ en el centro')),
        ('sangre', 'Panel de Sangre MP · Completo', '$500 – $600 por separado',
         'Tu analítica de sangre completa',
         'Una extracción de sangre que mide hierro y ferritina, testosterona, cortisol, tiroides, marcadores de inflamación y perfil metabólico. Lo que explica por qué te falta chispa aunque entrenes bien.',
         ('paneles-sangre.html', 'Ver los Paneles'),
         ('images/239michelle%20peiret%20oficina%202026%20-Edit.jpg', 'Especialista preparando una muestra de sangre')),
        ('inbody', 'InBody 970S', '$95 por separado',
         'Músculo y grasa, segmento por segmento',
         'Si estás ganando músculo o perdiéndolo, dónde tienes asimetrías entre lados y cómo va tu agua celular. La báscula de casa no distingue nada de esto.',
         ('inbody.html', 'Ver el InBody'),
         ('images/inbody-centro.jpg', 'Medición de composición corporal en el InBody 970S')),
        ('iv', 'IV Therapy de recuperación', 'Incluida',
         'Una sesión de recuperación deportiva',
         'Protocolo intravenoso de recuperación para cerrar el día de mediciones: hidratación, minerales y vitaminas según lo que tu analítica muestre.',
         None,
         ('images/127michelle%20peiret%20oficina%202026%20.jpg', 'Sala de IV Therapy del centro')),
    ],
    sum_l='<b>$945 a $1,045</b> si contratas los cuatro por separado',
    sum_r='<s>desde $945</s>$895',
    dia_label='Cómo es el día',
    dia_h2='Todo en una visita',
    dia=[
        ('Llamada de 15 minutos',
         'Revisamos cómo entrenas, qué buscas mejorar y confirmamos que este es el paquete correcto. Sin costo.'),
        ('Llegas en ayuno de 4 horas',
         'Con ropa de entrenamiento. Empezamos por la extracción de sangre y el InBody, que requieren ayuno.'),
        ('Análisis Metabólico',
         'Primero en reposo, después en esfuerzo sobre bicicleta o caminadora con la mascarilla PNOĒ. Unos 60 minutos entre ambas pruebas.'),
        ('IV Therapy de recuperación',
         'Mientras terminas la visita, tu sesión intravenosa de recuperación. Sales con los resultados del metabólico y del InBody el mismo día.'),
        ('Tu consulta de interpretación',
         'Cuando llega el panel de sangre, un especialista cruza los tres estudios y te entrega tus zonas, tus macros y las correcciones que tu química pide.'),
    ],
    q_h2='Para quien ya entrena y quiere subir el techo',
    si=[
        'Entrenas con constancia y llevas tiempo estancado',
        'Quieres tus zonas de entrenamiento medidas, no estimadas por fórmula',
        'Compites o preparas una carrera y quieres afinar la estrategia',
        'Sospechas que la fatiga viene de algo que no has medido',
        'Quieres saber tus calorías reales en lugar de seguir una calculadora',
    ],
    no=[
        'No entrenas todavía y quieres empezar a cuidarte — mejor el <em>Punto de Partida MP</em>',
        'Te interesa más microbiota, toxinas y sensibilidad alimentaria — ahí entra el <em>BioScan</em>',
        'Quieres los cuatro estudios incluido el BioScan — ese es el <em>Mapa Biológico MP</em>',
        'Vives fuera de Miami y no puedes viajar: este paquete es presencial completo',
    ],
    faq=[
        ('¿Tengo que ser atleta de competencia?',
         'No. El paquete se llama así porque mide rendimiento, pero sirve igual para alguien que entrena cuatro veces por semana y quiere dejar de adivinar. Si nunca entrenas, el Punto de Partida MP te da más por menos.'),
        ('¿Qué panel de sangre entra en el paquete?',
         'El Panel de Sangre MP Completo, el más amplio de los cinco paneles de sangre. Si tu caso pide otro énfasis — por ejemplo el hormonal — lo ajustamos en la llamada de 15 minutos sin cambiar el precio del paquete.'),
        ('¿Cuánto dura la visita?',
         'Entre 2 y 2.5 horas, contando la extracción, el InBody, las dos pruebas metabólicas y la sesión de IV Therapy. Ven sin prisa.'),
        ('¿Puedo entrenar el día anterior?',
         'Sí, pero evita sesiones muy intensas las 24 horas previas y nada de ejercicio el mismo día antes de la prueba. La cafeína también altera la medición: déjala para después.'),
        ('¿El VO2 max es el mismo que da mi reloj?',
         'No. Tu reloj lo estima a partir de tu frecuencia cardíaca y tu ritmo. Aquí se mide directamente el oxígeno que consumes y el CO₂ que exhalas. Es la diferencia entre un cálculo y un dato.'),
    ],
    alts=[
        ('paquete-punto-de-partida.html', 'Punto de Partida MP', '$540', 'Entiende qué está pasando en tu cuerpo.',
         'BioScan e InBody con tu consulta de interpretación. Buena parte desde casa y sin agujas.'),
        ('paquete-mapa-biologico.html', 'Mapa Biológico MP', '$1,200', 'La fotografía completa de tu biología.',
         'Los cuatro estudios en una sola visita: BioScan, sangre, metabólico e InBody.'),
    ],
    wa=WA + 'Hola%2C%20quiero%20informaci%C3%B3n%20del%20paquete%20Atleta%20MP',
    cfg="{ nombre: 'Atleta MP', precio: '$895', valor: 895, slug: 'atleta', calendly: '' }",
)

# ══════════════════════════════════════════════════════════════
#  3 · MAPA BIOLÓGICO MP — $1,200
# ══════════════════════════════════════════════════════════════
MAPA = dict(
    file='paquete-mapa-biologico.html',
    nombre='Mapa Biológico MP',
    tipo='Diagnóstico completo',
    title='Mapa Biológico MP — $1,200 · el más completo | Michelle Peiret Health',
    desc='BioScan, panel de sangre completo, Análisis Metabólico e InBody en una sola visita, con interpretación de un especialista. El diagnóstico más completo de MP Health.',
    h1='Toda tu biología,<br>en <em>un solo día</em>',
    sub='Cuatro estudios que normalmente se hacen por separado, a lo largo de meses y en sitios distintos. Aquí se hacen en una visita y se leen juntos: <strong>lo celular, lo clínico, lo metabólico y lo estructural</strong>, cruzados por un especialista en una sola conversación.',
    precio='1,200',
    price_note='· los cuatro estudios con tu consulta de interpretación',
    save='<span class="pk-save">Ahorras desde $192</span>',
    chips=['Presencial en Miami', 'Visita de 3 a 3.5 h', '4 estudios', 'Se acredita íntegro'],
    inc_h2='Las cuatro capas de tu biología',
    inc_p='Cada estudio ve algo que los otros no. Medidos por separado son cuatro informes sueltos; medidos juntos y leídos a la vez, son un mapa.',
    cards=[
        ('bioscan', 'BioScan', '$447 por separado',
         'Lo celular: 900+ biomarcadores',
         'Deficiencias, hormonas, microbiota, carga de toxinas y sensibilidad a 115+ alimentos, desde cuatro hebras de cabello. Muestra lo acumulado durante meses.',
         ('https://bioscan.michellepeiret.com/', 'Ver el BioScan'),
         ('images/bioscan-muestra.jpg', 'Toma de la muestra de cabello para el BioScan')),
        ('sangre', 'Panel de Sangre MP · Completo', '$500 – $600 por separado',
         'Lo clínico: tu sangre hoy',
         'El panel de sangre más amplio de los cinco: metabólico, hormonal, inflamatorio y nutricional. Los valores que un médico necesita ver, con la interpretación que casi nunca viene incluida.',
         ('paneles-sangre.html', 'Ver los Paneles'),
         ('images/239michelle%20peiret%20oficina%202026%20-Edit.jpg', 'Especialista preparando una muestra de sangre')),
        ('metab', 'Análisis Metabólico MP', '$350 por separado',
         'Lo metabólico: cómo produces energía',
         'Tus calorías y macros reales, tu VO2 max, tus zonas de entrenamiento y tu edad biológica, con tecnología PNOĒ. Medido, no estimado por fórmula.',
         ('metabolico.html', 'Ver el Análisis Metabólico'),
         ('images/centro-vo2max.jpg', 'Prueba de VO2 max con mascarilla PNOĒ en el centro')),
        ('inbody', 'InBody 970S', '$95 por separado',
         'Lo estructural: de qué está hecho tu peso',
         'Músculo, grasa, grasa visceral, agua celular y proteína por segmento. El punto de referencia contra el que medirás todo lo que hagas después.',
         ('inbody.html', 'Ver el InBody'),
         ('images/inbody-centro.jpg', 'Medición de composición corporal en el InBody 970S')),
    ],
    sum_l='<b>$1,392 a $1,492</b> si contratas los cuatro por separado',
    sum_r='<s>desde $1,392</s>$1,200',
    dia_label='Cómo es el día',
    dia_h2='Tres horas y media, una sola vez',
    dia=[
        ('Llamada de 15 minutos',
         'Revisamos tu historia y confirmamos que el Mapa completo es lo que tu caso necesita. A veces no lo es, y te lo decimos.'),
        ('Llegas en ayuno de 4 horas',
         'Te enviamos las instrucciones completas por adelantado. Ropa cómoda para hacer ejercicio ligero.'),
        ('Sangre, cabello e InBody',
         'Empezamos por lo que requiere ayuno: la extracción de sangre, la toma de la muestra de cabello para el BioScan y el escaneo de composición corporal.'),
        ('Análisis Metabólico',
         'En reposo y en esfuerzo con la mascarilla PNOĒ. Sales del centro con los resultados del metabólico y del InBody el mismo día.'),
        ('Tu consulta de interpretación',
         'Cuando llegan el panel de sangre y el BioScan — entre 7 y 10 días — te sientas con un especialista que cruza los cuatro estudios y te entrega el plan.'),
    ],
    q_h2='El más completo, y no siempre el necesario',
    si=[
        'Llevas años con síntomas y ningún estudio te ha explicado por qué',
        'Quieres una línea base completa contra la que medir todo lo que hagas',
        'Vas a iniciar un tratamiento y quieres que se diseñe sobre datos, no sobre supuestos',
        'Prefieres resolverlo en una visita en vez de estirarlo por meses',
        'Te interesa tu edad biológica y qué la está empujando hacia arriba',
    ],
    no=[
        'Solo quieres empezar a cuidarte sin tanta profundidad — el <em>Punto de Partida MP</em> basta',
        'Tu foco es rendimiento deportivo y recuperación — mira el <em>Atleta MP</em>',
        'Ya sabes exactamente qué medir: contrata ese estudio suelto y ahorra',
        'No puedes viajar a Miami: la visita completa es presencial',
    ],
    faq=[
        ('¿Por qué hacerlo todo el mismo día?',
         'Porque los cuatro estudios se leen mejor juntos. Un hierro bajo en sangre explica un VO2 max pobre; una microbiota alterada explica una inflamación que el panel detecta. Medidos con meses de diferencia, esas conexiones se pierden.'),
        ('¿Cuánto dura exactamente la visita?',
         'Entre 3 y 3.5 horas. Es la parte más exigente del paquete, así que conviene reservar la mañana completa y no encadenarla con compromisos.'),
        ('¿Cuándo tengo todos los resultados?',
         'El InBody y el metabólico salen el mismo día. El panel de sangre y el BioScan tardan entre 7 y 10 días. La consulta de interpretación se agenda cuando está todo, para verlo completo de una vez.'),
        ('¿Se acreditan los $1,200 completos?',
         'Sí. Si inicias un tratamiento nutricional personalizado dentro de los 60 días siguientes, el monto íntegro se descuenta del precio del tratamiento.'),
        ('¿Esto reemplaza a mi médico?',
         'No. Los diagnósticos MP no sustituyen una consulta médica ni constituyen un diagnóstico clínico. Son estudios que te dan datos y su interpretación; muchos pacientes se los llevan a su médico tratante, y nos parece bien que lo hagan.'),
        ('¿Puedo pagar en cuotas?',
         'Hay opciones de financiamiento para este paquete. Se revisan en la llamada de 15 minutos según el caso.'),
    ],
    alts=[
        ('paquete-punto-de-partida.html', 'Punto de Partida MP', '$540', 'Entiende qué está pasando en tu cuerpo.',
         'BioScan e InBody con tu consulta de interpretación. Buena parte desde casa y sin agujas.'),
        ('paquete-atleta.html', 'Atleta MP', '$895', 'Tu rendimiento, medido y optimizado.',
         'Metabólico con VO2 Max, panel de sangre completo, InBody y una sesión de IV Therapy de recuperación.'),
    ],
    wa=WA + 'Hola%2C%20quiero%20informaci%C3%B3n%20del%20Mapa%20Biol%C3%B3gico%20MP',
    cfg="{ nombre: 'Mapa Biológico MP', precio: '$1,200', valor: 1200, slug: 'mapa_biologico', calendly: '' }",
)

for p in (PUNTO, ATLETA, MAPA):
    build(p)
