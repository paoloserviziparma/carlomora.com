#!/usr/bin/env python3
"""Genera le pagine statiche del sito in public/.

Uso:  python3 tools/build.py
Non serve a Netlify (che pubblica public/ così com'è): si lancia in locale
dopo aver modificato testi o struttura, poi si fa commit dei file generati.
"""
import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
SITE = "https://www.carlomora.com"
TODAY = "2026-10-24"

WA_NUM = "393911156147"
PHONE = "+390521285916"
EMAIL = "carlo@carlomora.com"


def ver():
    h = hashlib.sha256()
    for p in ("assets/css/style.css", "assets/js/main.js"):
        h.update((PUB / p).read_bytes())
    return h.hexdigest()[:10]


V = ver()


def wa(msg):
    from urllib.parse import quote
    return f"https://wa.me/{WA_NUM}?text={quote(msg)}"


def e(s):
    return html.escape(s, quote=True)


def srcset(name, widths):
    return ", ".join(f"/assets/img/{name}-{w}.webp {w}w" for w in widths)


WA_ICON = ('<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
           'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21l1.7-5A8.5 8.5 0 1 1 8 19.4z"/>'
           '<path d="M9 9.5c0 3 2.5 5.5 5.5 5.5l1.2-1.4-2-1-.9.8a4 4 0 0 1-2.2-2.2l.8-.9-1-2z"/></svg>')

HOURS = [  # (giorno schema.org, apre, chiude)
    ("Tuesday", "09:00", "18:00"),
    ("Wednesday", "12:00", "20:00"),
    ("Thursday", "09:00", "18:00"),
    ("Friday", "10:00", "20:00"),
    ("Saturday", "09:00", "18:00"),
]

# ---------------------------------------------------------------- testi
T = {
    "it": {
        "lang": "it", "locale": "it_IT", "prefix": "/",
        "home_title": "Parrucchiere a Parma | Carlo Mora Parrucchieri – Viale Mentana",
        "home_desc": "Carlo Mora Parrucchieri, salone Art Hair Studios by Wella in Viale Mentana 12/a a Parma: taglio, colore, piega e trattamenti donna. Prenota su WhatsApp.",
        "skip": "Vai al contenuto",
        "menu": "Menu",
        "nav": [("filosofia", "Filosofia"), ("arcano", "Quale Arcano sei?"), ("prima-volta", "Prima volta"), ("orari", "Orari"), ("contatti", "Contatti")],
        "book": "Prenota su WhatsApp",
        "wa_msg": "Ciao Carlo! Vorrei prenotare un appuntamento.",
        "wa_first": "Ciao Carlo! È la prima volta che vengo da voi e vorrei prenotare un appuntamento.",
        "hero_kicker": "Parrucchieri a Parma · Viale Mentana 12/a",
        "hero_h1": "Unicità e imperfezione",
        "hero_claim": "Energia, design, arte, colori, riciclo, originalità e ironia. Siamo qua, ti ascoltiamo, risolviamo.",
        "hero_alt": "Modella con caschetto rosso scolpito e giacca oversize su fondo cipria, collezione Art Hair Studios",
        "write_wa": "Scrivici su WhatsApp",
        "call": "Chiama 0521 285916",
        "fascia": ["Taglio", "Colore", "Piega", "Trattamenti", "Salone Art Hair Studios by Wella"],
        "filo_kicker": "01 — La nostra filosofia",
        "filo_h2": "Siamo rock, sì.",
        "filo_quote": "“So cosa vorrei farti trovare quando entri nel nostro negozio. Vediamo se ci azzecco.”",
        "filo_p": [
            "Dev'essere un luogo dove si possono trovare energia, design, arte, colori, riciclo, originalità e ironia; un luogo dove ci sono le risposte alle tue esigenze, sia per chi ha poco tempo da dedicare ai capelli, sia per chi non ne ha proprio voglia.",
            "Essere stilosi è trovare l’empatia, è cambiare vestito senza rendere conto a nessuno e sentendoci sempre in ordine e, soprattutto, noi stessi (meglio: voi stesse). Siamo qua per chi ama il dettaglio e il coraggio di rompere uno schema.",
            "Preferiamo l'imperfezione#, per chi si sente a suo agio a essere imperfetta. Ecco perché l’hashtag lo mettiamo alla fine.",
        ],
        "filo_sign": "Carlo Mora &amp; la sua tribù",
        "coll_kicker": "02 — Collezione Art Hair Studios",
        "coll_text": "Facciamo parte della rete Art Hair Studios by Wella. La collezione di questa stagione si ispira agli Arcani dei Tarocchi: ogni carta è uno spunto per cambiare, da leggere insieme a noi in salone.",
        "coll_alts": ["Raccolto lucido con diadema dorato a bilancia su fondo cipria", "Caschetto rosso scolpito con ciocche bagnate e giacca oversize su fondo cipria", "Capelli biondi lunghissimi con trecce laterali su fondo cipria"],
        "credits": "Foto: collezione Alchemy F/W 2026 © Art Hair Studios by Wella.",
        "arc_kicker": "03 — Il rituale",
        "arc_h2": "Quale Arcano sei?",
        "arc_text": "Tre domande, una carta, un'idea da portare in salone. Non è una previsione: è un punto di partenza per parlarne insieme.",
        "arc_your": "La tua carta",
        "arc_book": "Prenota con questa carta",
        "arc_again": "Rifai il test",
        "quiz": {
            "labels": {"step": "Domanda {n} di {t}", "waMsg": "Ciao Carlo! Ho fatto il test sul sito: la mia carta è {card}. Vorrei prenotare un appuntamento."},
            "cards": {
                "torre": {"num": "XVI", "name": "La Torre", "title": "È il momento del cambio netto.", "idea": "Un taglio che rompe lo schema: corto, asimmetrico, deciso. Prima delle forbici ne parliamo insieme, con calma."},
                "stella": {"num": "XVII", "name": "La Stella", "title": "Cerchi luce.", "idea": "Riflessi e schiariture morbide che illuminano il viso, con una piega facile da rifare a casa in pochi minuti."},
                "giustizia": {"num": "XI", "name": "La Giustizia", "title": "Equilibrio, e zero fatica.", "idea": "Un taglio pulito e preciso, pensato per stare in ordine da solo anche quando di tempo non ne hai."},
                "luna": {"num": "XVIII", "name": "La Luna", "title": "Un colore che si fa notare.", "idea": "Toni intensi, rame e rossi profondi, per chi ama il dettaglio e un po’ di mistero."},
            },
            "questions": [
                {"q": "Cosa vuoi chiedere ai tuoi capelli oggi?", "o": [["Cambiare tutto", "torre"], ["Più luce", "stella"], ["Ordine, senza fatica", "giustizia"], ["Un colore che si noti", "luna"]]},
                {"q": "Quanto tempo dedichi ai capelli la mattina?", "o": [["Zero: lavati e via", "giustizia"], ["Qualche minuto", "stella"], ["Mi piace prendermelo", "luna"], ["Dipende dall’umore", "torre"]]},
                {"q": "Quanto vuoi osare?", "o": [["Rompiamo lo schema", "torre"], ["Un passo alla volta", "stella"], ["Me stessa, ma meglio", "giustizia"], ["Voglio stupire", "luna"]]},
            ],
        },
        "prima_kicker": "04 — Prima volta da noi?",
        "prima_h2": "Come funziona",
        "prima_alt": "Modella con capelli biondi lunghi e treccia laterale su fondo cipria",
        "prima_steps": [
            ("Scrivici su WhatsApp", "Dicci che è la prima volta, che giorno preferisci e cosa hai in mente. Ti rispondiamo con la disponibilità."),
            ("Ti ascoltiamo", "Prima di iniziare parliamo di te, dei tuoi capelli e di quanto tempo vuoi dedicarci ogni giorno."),
            ("Scegliamo insieme", "Taglio, colore o trattamento: ti proponiamo la strada più adatta, anche se è quella che rompe lo schema."),
            ("A casa, come in salone", "Ti spieghiamo come mantenere il risultato con pochi gesti."),
        ],
        "prima_btn": "Scrivici: è la mia prima volta",
        "orari_kicker": "05 — Orari d'apertura",
        "orari_h2": "Quando ci trovi",
        "orari_text": "A luglio e agosto cambiano gli orari del mercoledì e del sabato. Domenica e lunedì siamo chiusi.",
        "orari": [("Martedì", "9:00 – 18:00", ""), ("Mercoledì", "12:00 – 20:00", "Luglio e agosto: 10:00 – 20:00"), ("Giovedì", "9:00 – 18:00", ""), ("Venerdì", "10:00 – 20:00", ""), ("Sabato", "9:00 – 18:00", "Luglio e agosto: 9:00 – 15:00"), ("Domenica e lunedì", "Chiuso", "")],
        "faq_kicker": "06 — Domande frequenti",
        "faq_h2": "Da sapere",
        "faq": [
            ("Come si prenota un appuntamento?", "Il modo più veloce è scriverci su WhatsApp al 391 1156147: indicaci il giorno che preferisci e il servizio che desideri, ti rispondiamo con la disponibilità. Puoi anche chiamarci allo 0521 285916 negli orari di apertura."),
            ("Dove si trova il salone?", "Siamo in Viale Mentana 12/a, 43121 Parma (PR)."),
            ("Siete aperti la domenica e il lunedì?", "No, domenica e lunedì il salone è chiuso. Siamo aperti dal martedì al sabato: martedì e giovedì 9:00–18:00, mercoledì 12:00–20:00, venerdì 10:00–20:00, sabato 9:00–18:00."),
            ("Gli orari cambiano d'estate?", "Sì: a luglio e agosto il mercoledì siamo aperti dalle 10:00 alle 20:00 e il sabato dalle 9:00 alle 15:00."),
            ("Cos'è Art Hair Studios by Wella?", "È una rete di saloni acconciatori nata nel 1976 e legata a Wella, che ogni stagione presenta una collezione di tendenze. Carlo Mora Parrucchieri fa parte della rete."),
        ],
        "cont_kicker": "07 — Contatti",
        "cont_h2": "Prenota il tuo momento",
        "cont_wa_k": "WhatsApp · apri l'app",
        "cont_wa_t": "Scrivici giorno e servizio che desideri: ti rispondiamo noi con la disponibilità.",
        "cont_tel_k": "Telefono e email",
        "cont_where_k": "Dove siamo",
        "cont_maps": "Apri in Mappe →",
        "social_t": "Se la curiosità ti assale, seguici:",
        "privacy": "Privacy policy", "cookie": "Cookie policy",
        "privacy_url": "/privacy/", "cookie_url": "/cookie/",
        "vat": "P. IVA", "home": "Home",
        "float": "Scrivici su WhatsApp",
        "nf_title": "Pagina non trovata | Carlo Mora Parrucchieri",
        "nf_h1": "404", "nf_t": "Questa pagina non esiste (più). Torna alla home o scrivici su WhatsApp.",
        "nf_btn": "Torna alla home",
        "upd": "Ultimo aggiornamento: 24 ottobre 2026",
    },
    "en": {
        "lang": "en", "locale": "en_GB", "prefix": "/en/",
        "home_title": "Hairdresser in Parma, Italy | Carlo Mora Hair Salon",
        "home_desc": "Carlo Mora, an Art Hair Studios by Wella hair salon at Viale Mentana 12/a in Parma, Italy: women's cuts, colour, blow-dry and treatments. Book on WhatsApp.",
        "skip": "Skip to content",
        "menu": "Menu",
        "nav": [("filosofia", "Philosophy"), ("arcano", "Which Arcana are you?"), ("prima-volta", "First visit"), ("orari", "Opening hours"), ("contatti", "Contact")],
        "book": "Book on WhatsApp",
        "wa_msg": "Hi Carlo! I'd like to book an appointment.",
        "wa_first": "Hi Carlo! It's my first time at your salon and I'd like to book an appointment.",
        "hero_kicker": "Hair salon in Parma · Viale Mentana 12/a",
        "hero_h1": "Uniqueness and imperfection",
        "hero_claim": "Energy, design, art, colour, recycling, originality and irony. We're here, we listen, we sort it out.",
        "hero_alt": "Model with a sculpted red bob and oversized jacket on a powder-pink background, Art Hair Studios collection",
        "write_wa": "Message us on WhatsApp",
        "call": "Call +39 0521 285916",
        "fascia": ["Cut", "Colour", "Blow-dry", "Treatments", "Art Hair Studios by Wella salon"],
        "filo_kicker": "01 — Our philosophy",
        "filo_h2": "Yes, we're rock.",
        "filo_quote": "“I know what I'd like you to find when you walk into our salon. Let's see if I get it right.”",
        "filo_p": [
            "It has to be a place full of energy, design, art, colour, recycling, originality and irony; a place with answers to what you need, whether you have little time for your hair or simply don't feel like spending any.",
            "Being stylish means finding empathy, changing your look without answering to anyone, always feeling put together and, above all, yourself. We're here for those who love detail and have the courage to break the mould.",
            "We prefer imperfection#, for those who feel at ease being imperfect. That's why the hashtag goes at the end.",
        ],
        "filo_sign": "Carlo Mora &amp; his tribe",
        "coll_kicker": "02 — Art Hair Studios collection",
        "coll_text": "We are part of the Art Hair Studios by Wella network. This season's collection is inspired by the Tarot's Major Arcana: each card is a prompt for change, to read together with us in the salon.",
        "coll_alts": ["Sleek updo with golden scales headpiece on a powder-pink background", "Sculpted red bob with wet-look strands and oversized jacket on a powder-pink background", "Very long blonde hair with side braids on a powder-pink background"],
        "credits": "Photos: Alchemy F/W 2026 collection © Art Hair Studios by Wella.",
        "arc_kicker": "03 — The ritual",
        "arc_h2": "Which Arcana are you?",
        "arc_text": "Three questions, one card, an idea to bring to the salon. It's not a prediction: it's a starting point to talk it through together.",
        "arc_your": "Your card",
        "arc_book": "Book with this card",
        "arc_again": "Take the test again",
        "quiz": {
            "labels": {"step": "Question {n} of {t}", "waMsg": "Hi Carlo! I took the test on your website: my card is {card}. I'd like to book an appointment."},
            "cards": {
                "torre": {"num": "XVI", "name": "The Tower", "title": "Time for a clean break.", "idea": "A cut that breaks the mould: short, asymmetric, bold. Before the scissors come out, we talk it through calmly."},
                "stella": {"num": "XVII", "name": "The Star", "title": "You're looking for light.", "idea": "Soft highlights and balayage that brighten your face, with a blow-dry you can redo at home in minutes."},
                "giustizia": {"num": "XI", "name": "Justice", "title": "Balance, zero effort.", "idea": "A clean, precise cut designed to fall into place on its own, even when you have no time."},
                "luna": {"num": "XVIII", "name": "The Moon", "title": "A colour that gets noticed.", "idea": "Intense tones, coppers and deep reds, for those who love detail and a touch of mystery."},
            },
            "questions": [
                {"q": "What do you want to ask of your hair today?", "o": [["Change everything", "torre"], ["More light", "stella"], ["Order, no effort", "giustizia"], ["A colour that stands out", "luna"]]},
                {"q": "How much time do you spend on your hair in the morning?", "o": [["None: wash and go", "giustizia"], ["A few minutes", "stella"], ["I enjoy taking my time", "luna"], ["Depends on my mood", "torre"]]},
                {"q": "How daring do you want to be?", "o": [["Let's break the mould", "torre"], ["One step at a time", "stella"], ["Me, only better", "giustizia"], ["I want to amaze", "luna"]]},
            ],
        },
        "prima_kicker": "04 — First time with us?",
        "prima_h2": "How it works",
        "prima_alt": "Model with long blonde hair and a side braid on a powder-pink background",
        "prima_steps": [
            ("Message us on WhatsApp", "Tell us it's your first visit, which day suits you and what you have in mind. We'll reply with availability."),
            ("We listen", "Before we start, we talk about you, your hair and how much time you want to spend on it every day."),
            ("We choose together", "Cut, colour or treatment: we suggest the best path for you, even if it's the one that breaks the mould."),
            ("At home, like in the salon", "We show you how to keep the result with a few simple steps."),
        ],
        "prima_btn": "Message us: it's my first time",
        "orari_kicker": "05 — Opening hours",
        "orari_h2": "When to find us",
        "orari_text": "In July and August our Wednesday and Saturday hours change. We are closed on Sundays and Mondays.",
        "orari": [("Tuesday", "9:00 – 18:00", ""), ("Wednesday", "12:00 – 20:00", "July and August: 10:00 – 20:00"), ("Thursday", "9:00 – 18:00", ""), ("Friday", "10:00 – 20:00", ""), ("Saturday", "9:00 – 18:00", "July and August: 9:00 – 15:00"), ("Sunday and Monday", "Closed", "")],
        "faq_kicker": "06 — FAQ",
        "faq_h2": "Good to know",
        "faq": [
            ("How do I book an appointment?", "The quickest way is to message us on WhatsApp at +39 391 1156147: tell us which day you prefer and the service you'd like, and we'll reply with availability. You can also call us on +39 0521 285916 during opening hours."),
            ("Where is the salon?", "We are at Viale Mentana 12/a, 43121 Parma (PR), Italy."),
            ("Are you open on Sundays and Mondays?", "No, the salon is closed on Sundays and Mondays. We are open Tuesday to Saturday: Tuesday and Thursday 9:00–18:00, Wednesday 12:00–20:00, Friday 10:00–20:00, Saturday 9:00–18:00."),
            ("Do the opening hours change in summer?", "Yes: in July and August we are open on Wednesdays from 10:00 to 20:00 and on Saturdays from 9:00 to 15:00."),
            ("What is Art Hair Studios by Wella?", "It's a network of hair salons founded in 1976 and linked to Wella, presenting a trend collection every season. Carlo Mora is part of the network."),
        ],
        "cont_kicker": "07 — Contact",
        "cont_h2": "Book your moment",
        "cont_wa_k": "WhatsApp · open the app",
        "cont_wa_t": "Tell us the day and the service you'd like: we'll reply with availability.",
        "cont_tel_k": "Phone and email",
        "cont_where_k": "Where we are",
        "cont_maps": "Open in Maps →",
        "social_t": "If you're curious, follow us:",
        "privacy": "Privacy policy", "cookie": "Cookie policy",
        "privacy_url": "/en/privacy/", "cookie_url": "/en/cookie/",
        "vat": "VAT no.", "home": "Home",
        "float": "Message us on WhatsApp",
        "nf_title": "Page not found | Carlo Mora Hair Salon",
        "nf_h1": "404", "nf_t": "This page doesn't exist (any more). Go back to the home page or message us on WhatsApp.",
        "nf_btn": "Back to home",
        "upd": "Last updated: 24 October 2026",
    },
}

# ---------------------------------------------------------------- testi legali
import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parent))
from legal import PRIVACY_IT, COOKIE_IT, PRIVACY_EN, COOKIE_EN  # noqa: E402

LEGAL = {
    ("it", "privacy"): {"title": "Privacy policy | Carlo Mora Parrucchieri – Parma",
                        "desc": "Informativa sul trattamento dei dati personali degli utenti del sito di Carlo Mora Parrucchieri, Viale Mentana, Parma.",
                        "h1": "Privacy policy", "body": PRIVACY_IT},
    ("it", "cookie"): {"title": "Cookie policy | Carlo Mora Parrucchieri – Parma",
                       "desc": "Informativa sull'uso dei cookie sul sito di Carlo Mora Parrucchieri, Viale Mentana, Parma.",
                       "h1": "Cookie policy", "body": COOKIE_IT},
    ("en", "privacy"): {"title": "Privacy policy | Carlo Mora Hair Salon – Parma",
                        "desc": "How the personal data of visitors to the Carlo Mora hair salon website in Parma, Italy, are processed.",
                        "h1": "Privacy policy", "body": PRIVACY_EN},
    ("en", "cookie"): {"title": "Cookie policy | Carlo Mora Hair Salon – Parma",
                       "desc": "Information on the use of cookies on the Carlo Mora hair salon website in Parma, Italy.",
                       "h1": "Cookie policy", "body": COOKIE_EN},
}

LLMS = '''# Carlo Mora Parrucchieri

> Salone di parrucchieri per donna a Parma, in Viale Mentana 12/a (43121 Parma, PR, Italia). Fa parte della rete Art Hair Studios by Wella. Taglio, colore, piega e trattamenti. Prenotazioni su WhatsApp.

## Contatti
- WhatsApp (prenotazioni): +39 391 1156147 – https://wa.me/393911156147
- Telefono: +39 0521 285916
- Email: carlo@carlomora.com
- Indirizzo: Viale Mentana 12/a, 43121 Parma (PR), Italia

## Orari
- Martedì 9:00–18:00
- Mercoledì 12:00–20:00 (luglio e agosto 10:00–20:00)
- Giovedì 9:00–18:00
- Venerdì 10:00–20:00
- Sabato 9:00–18:00 (luglio e agosto 9:00–15:00)
- Domenica e lunedì: chiuso

## Pagine
- [Home (italiano)](https://www.carlomora.com/)
- [Home (English)](https://www.carlomora.com/en/)
- [Privacy policy](https://www.carlomora.com/privacy/)
- [Cookie policy](https://www.carlomora.com/cookie/)
'''

# ---------------------------------------------------------------- JSON-LD
def ld_business(L):
    t = T[L]
    return {
        "@context": "https://schema.org",
        "@type": "HairSalon",
        "@id": SITE + "/#salone",
        "name": "Carlo Mora Parrucchieri",
        "description": t["home_desc"],
        "url": SITE + t["prefix"],
        "image": SITE + "/assets/img/og-carlo-mora.jpg",
        "logo": SITE + "/assets/img/logo-cm-512.png",
        "telephone": PHONE,
        "email": EMAIL,
        "vatID": "IT01904010343",
        "address": {"@type": "PostalAddress", "streetAddress": "Viale Mentana 12/a", "postalCode": "43121",
                    "addressLocality": "Parma", "addressRegion": "PR", "addressCountry": "IT"},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": d, "opens": o, "closes": c} for d, o, c in HOURS
        ] + [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Wednesday", "opens": "10:00", "closes": "20:00",
             "validFrom": "2026-07-01", "validThrough": "2026-08-31"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "15:00",
             "validFrom": "2026-07-01", "validThrough": "2026-08-31"},
        ],
        "contactPoint": {"@type": "ContactPoint", "contactType": "reservations", "telephone": "+393911156147",
                         "availableLanguage": ["Italian", "English"]},
        "sameAs": ["https://www.facebook.com/cmparrucchieriparma/", "https://www.instagram.com/carlomoraparrucchieri/"],
        "inLanguage": t["lang"],
    }


def ld_faq(L):
    return {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": T[L]["lang"],
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in T[L]["faq"]]}


def ld_crumbs(L, name, url):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": T[L]["home"], "item": SITE + T[L]["prefix"]},
        {"@type": "ListItem", "position": 2, "name": name, "item": SITE + url}]}


def ld_tag(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"


# ---------------------------------------------------------------- parti comuni
def head(L, title, desc, path, alt_path, extra_ld=(), noindex=False, og_type="website"):
    t = T[L]
    other = "en" if L == "it" else "it"
    it_path, en_path = (path, alt_path) if L == "it" else (alt_path, path)
    alt = ""
    if not noindex:
        alt = (f'<link rel="canonical" href="{SITE}{path}">\n'
               f'<link rel="alternate" hreflang="it" href="{SITE}{it_path}">\n'
               f'<link rel="alternate" hreflang="en" href="{SITE}{en_path}">\n'
               f'<link rel="alternate" hreflang="x-default" href="{SITE}{it_path}">\n')
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    lds = "\n".join(ld_tag(o) for o in extra_ld)
    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}{alt}<meta name="theme-color" content="#0c0c0c">
<meta name="format-detection" content="telephone=no">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Carlo Mora Parrucchieri">
<meta property="og:locale" content="{t['locale']}">
<meta property="og:locale:alternate" content="{T[other]['locale']}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/assets/img/og-carlo-mora.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/img/logo-cm-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/archivo-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css?v={V}">
{lds}
<script src="/assets/js/main.js?v={V}" defer></script>
</head>
<body>
"""


def header(L, home_anchor_base, lang_href_other):
    t = T[L]
    other = "en" if L == "it" else "it"
    nav = "\n".join(f'      <a href="{home_anchor_base}#{a}">{e(label)}</a>' for a, label in t["nav"])
    lang = (f'<span class="lang"><strong>{L.upper()}</strong> / <a href="{lang_href_other}" hreflang="{other}" lang="{other}">{other.upper()}</a></span>'
            if L == "it" else
            f'<span class="lang"><a href="{lang_href_other}" hreflang="{other}" lang="{other}">{other.upper()}</a> / <strong>{L.upper()}</strong></span>')
    return f"""<a class="skip" href="#main">{t['skip']}</a>
<header class="header">
  <div class="wrap header-in">
    <a class="brand" href="{t['prefix']}" aria-label="Carlo Mora Parrucchieri – {t['home']}">
      <img src="/assets/img/logo-cm-96.png" alt="" width="48" height="48">
      <span>Carlo Mora</span>
    </a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="{t['menu']}">
      <svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
    </button>
    <nav class="nav" id="nav" aria-label="{t['menu']}">
{nav}
      {lang}
      <a class="btn btn-oro" href="{wa(t['wa_msg'])}" target="_blank" rel="noopener">{t['book']}</a>
    </nav>
  </div>
</header>
"""


def footer(L):
    t = T[L]
    return f"""<footer class="footer">
  <div class="wrap">
    <div>
      <strong>Carlo Mora Parrucchieri</strong><br>
      Viale Mentana 12/a · 43121 Parma (PR)<br>
      {t['vat']} 01904010343 · REA PR-186865
    </div>
    <nav aria-label="Note legali">
      <a href="{t['privacy_url']}">{t['privacy']}</a>
      <a href="{t['cookie_url']}">{t['cookie']}</a>
    </nav>
  </div>
</footer>
<a class="wa-float" href="{wa(t['wa_msg'])}" target="_blank" rel="noopener" aria-label="{t['float']}">
  <svg aria-hidden="true" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21l1.7-5A8.5 8.5 0 1 1 8 19.4z"/><path d="M9 9.5c0 3 2.5 5.5 5.5 5.5l1.2-1.4-2-1-.9.8a4 4 0 0 1-2.2-2.2l.8-.9-1-2z"/></svg>
</a>
</body>
</html>
"""


# ---------------------------------------------------------------- home
def home(L):
    t = T[L]
    other_home = "/en/" if L == "it" else "/"
    q = dict(t["quiz"])
    q["phone"] = WA_NUM
    quiz_json = json.dumps(q, ensure_ascii=False).replace("</", "<\\/")
    fascia = "<span aria-hidden=\"true\">·</span>".join(f"<span>{e(x)}</span>" for x in t["fascia"])
    filo = "\n".join(f"        <p>{p}</p>" for p in t["filo_p"])
    coll_imgs = [("giustizia", (480, 800)), ("diavolo", (480, 960, 1600)), ("torre", (480, 800))]
    gal = "\n".join(
        f'        <figure class="reveal" data-parallax><img src="/assets/img/{n}-{w[0]}.webp" srcset="{srcset(n, w)}" '
        f'sizes="(max-width:560px) 92vw, (max-width:900px) 46vw, 30vw" alt="{e(alt)}" width="{w[-1]}" '
        f'height="{round(w[-1]*1.25)}" loading="lazy" decoding="async"></figure>'
        for (n, w), alt in zip(coll_imgs, t["coll_alts"]))
    steps = "\n".join(
        f'          <li><span class="n" aria-hidden="true">{i}</span><div><h3>{e(a)}</h3><p>{e(b)}</p></div></li>'
        for i, (a, b) in enumerate(t["prima_steps"], 1))
    orari = "\n".join(
        f'          <div><dt>{e(d)}</dt><dd>{e(h)}</dd>' + (f'<dd class="nota">{e(n)}</dd>' if n else "") + "</div>"
        for d, h, n in t["orari"])
    faq = "\n".join(f'        <details class="reveal"><summary>{e(qq)}</summary><p>{e(aa)}</p></details>' for qq, aa in t["faq"])
    if (PUB / "assets/video/hero-720.mp4").exists():
        hero_media = f"""  <div class="hero-img hero-video">
    <video autoplay muted loop playsinline preload="auto" poster="/assets/video/hero-poster.webp" aria-hidden="true" tabindex="-1" data-hero-video>
      <source src="/assets/video/hero-480.mp4" type="video/mp4" media="(max-width: 760px)">
      <source src="/assets/video/hero-720.mp4" type="video/mp4">
    </video>
  </div>"""
    else:
        hero_media = f"""  <div class="hero-img">
    <img src="/assets/img/diavolo-960.webp" srcset="{srcset('diavolo', (480, 960, 1600))}" sizes="(max-width:760px) 100vw, 58vw" alt="{e(t['hero_alt'])}" width="1600" height="2263" fetchpriority="high">
  </div>"""
    out = head(L, t["home_title"], t["home_desc"], t["prefix"], other_home, (ld_business(L), ld_faq(L)))
    out += header(L, "", other_home)
    out += f"""<main id="main">
<section class="hero" aria-label="Carlo Mora Parrucchieri">
{hero_media}
  <div class="hero-fade" aria-hidden="true"></div>
  <div class="wrap hero-text">
    <div class="hero-anim">
      <h1><span class="kick">{e(t['hero_kicker'])}</span>{e(t['hero_h1'])}<span class="hash">#</span></h1>
      <p class="claim">{e(t['hero_claim'])}</p>
      <div class="cta">
        <a class="btn btn-oro" href="{wa(t['wa_msg'])}" target="_blank" rel="noopener">{WA_ICON}{t['write_wa']}</a>
        <a class="btn btn-linea" href="tel:{PHONE}">{t['call']}</a>
      </div>
    </div>
  </div>
</section>

<div class="fascia chiara"><div class="wrap">{fascia}</div></div>

<section id="filosofia" class="section filosofia">
  <div class="wrap cols">
    <div class="col-1 reveal">
      <p class="eyebrow">{t['filo_kicker']}</p>
      <h2 class="h2">{e(t['filo_h2'])}</h2>
      <img class="logo-big" src="/assets/img/logo-cm-480.webp" alt="" width="220" height="220" loading="lazy">
    </div>
    <div class="col-2 testo reveal">
      <p class="quote">{e(t['filo_quote'])}</p>
{filo}
      <p class="firma">{t['filo_sign']}</p>
    </div>
  </div>
</section>

<section id="collezione" class="section chiara">
  <div class="wrap">
    <div class="coll-head reveal">
      <div>
        <p class="eyebrow">{t['coll_kicker']}</p>
        <h2 class="h2">Alchemy <span class="fw">F/W 2026</span></h2>
      </div>
      <p>{e(t['coll_text'])}</p>
    </div>
    <div class="galleria">
{gal}
    </div>
    <p class="crediti">{e(t['credits'])}</p>
  </div>
</section>

<section id="arcano" class="section">
  <div class="wrap cols">
    <div class="col-1 reveal">
      <p class="eyebrow">{t['arc_kicker']}</p>
      <h2 class="h2">{e(t['arc_h2'])}</h2>
      <p class="lead">{e(t['arc_text'])}</p>
    </div>
    <div class="col-2 reveal">
      <div class="quiz" id="quiz" aria-live="polite">
        <div class="barra" aria-hidden="true"><span data-q-bar style="width:0"></span></div>
        <div data-q-ask>
          <p class="step" data-q-step></p>
          <h3 class="domanda" data-q-text></h3>
          <div class="opzioni" data-q-opts></div>
          <noscript><p>{e(t['wa_msg'])}</p></noscript>
        </div>
        <div class="risultato" data-q-res hidden>
          <div class="carta">
            <span class="num" data-c-num></span>
            <img src="/assets/img/logo-cm-192.webp" alt="" width="96" height="96" loading="lazy">
            <span class="nome" data-c-name></span>
          </div>
          <div class="info">
            <p class="eyebrow">{t['arc_your']}</p>
            <h3 class="titolo" data-c-title></h3>
            <p class="idea" data-c-idea></p>
            <div class="azioni">
              <a class="btn btn-oro" data-c-wa href="{wa(t['wa_msg'])}" target="_blank" rel="noopener">{WA_ICON}{t['arc_book']}</a>
              <button class="btn btn-linea" type="button" data-q-restart>{t['arc_again']}</button>
            </div>
          </div>
        </div>
      </div>
      <script type="application/json" id="quiz-data">{quiz_json}</script>
    </div>
  </div>
</section>

<section id="prima-volta" class="section chiara prima">
  <div class="wrap cols">
    <div class="foto reveal" data-parallax>
      <img src="/assets/img/treccia-lunga-960.webp" srcset="{srcset('treccia-lunga', (480, 960, 1600))}" sizes="(max-width:860px) 92vw, 42vw" alt="{e(t['prima_alt'])}" width="1600" height="2400" loading="lazy" decoding="async">
    </div>
    <div class="passi reveal">
      <p class="eyebrow">{t['prima_kicker']}</p>
      <h2 class="h2">{e(t['prima_h2'])}</h2>
      <ol>
{steps}
      </ol>
      <a class="btn btn-nero" href="{wa(t['wa_first'])}" target="_blank" rel="noopener">{WA_ICON}{t['prima_btn']}</a>
    </div>
  </div>
</section>

<section id="orari" class="section">
  <div class="wrap cols">
    <div class="col-1 reveal">
      <p class="eyebrow">{t['orari_kicker']}</p>
      <h2 class="h2">{e(t['orari_h2'])}</h2>
      <p class="lead">{e(t['orari_text'])}</p>
    </div>
    <div class="col-2 reveal">
      <dl class="orari-lista">
{orari}
      </dl>
    </div>
  </div>
</section>

<section id="faq" class="section chiara faq">
  <div class="wrap cols">
    <div class="col-1 reveal">
      <p class="eyebrow">{t['faq_kicker']}</p>
      <h2 class="h2">{e(t['faq_h2'])}</h2>
    </div>
    <div class="col-2">
{faq}
    </div>
  </div>
</section>

<section id="contatti" class="section scura-2">
  <div class="wrap">
    <div class="reveal">
      <p class="eyebrow">{t['cont_kicker']}</p>
      <h2 class="h2">{e(t['cont_h2'])}</h2>
    </div>
    <div class="card-grid">
      <a class="card card-wa reveal" href="{wa(t['wa_msg'])}" target="_blank" rel="noopener">
        <span class="eyebrow">{t['cont_wa_k']}</span>
        <span class="big">391 1156147</span>
        <span class="sotto">{e(t['cont_wa_t'])}</span>
      </a>
      <div class="card reveal">
        <span class="eyebrow">{t['cont_tel_k']}</span>
        <a class="big" href="tel:{PHONE}">0521 285916</a>
        <a href="mailto:{EMAIL}">{EMAIL}</a>
      </div>
      <address class="card reveal" style="font-style:normal">
        <span class="eyebrow">{t['cont_where_k']}</span>
        <span class="big">Viale Mentana 12/a</span>
        <span style="color:var(--osso-testo)">43121 Parma (PR)</span>
        <a class="link" href="https://www.google.com/maps/search/?api=1&amp;query=Carlo+Mora+Parrucchieri+Viale+Mentana+12%2Fa+43121+Parma" target="_blank" rel="noopener">{t['cont_maps']}</a>
      </address>
    </div>
    <div class="social">
      <span class="serif">{e(t['social_t'])}</span>
      <a href="https://www.instagram.com/carlomoraparrucchieri/" target="_blank" rel="noopener">Instagram</a>
      <a href="https://www.facebook.com/cmparrucchieriparma/" target="_blank" rel="noopener">Facebook</a>
    </div>
  </div>
</section>
</main>
"""
    out += footer(L)
    return out


def legal(L, kind):
    t = T[L]
    d = LEGAL[(L, kind)]
    path = t["privacy_url"] if kind == "privacy" else t["cookie_url"]
    other_L = "en" if L == "it" else "it"
    other = T[other_L]["privacy_url"] if kind == "privacy" else T[other_L]["cookie_url"]
    out = head(L, d["title"], d["desc"], path, other, (ld_crumbs(L, d["h1"], path),))
    out += header(L, t["prefix"], other)
    out += f"""<main id="main" class="legal">
  <div class="wrap">
    <nav aria-label="Breadcrumb" class="eyebrow"><a href="{t['prefix']}">{t['home']}</a> / {d['h1']}</nav>
    <h1>{d['h1']}</h1>
    {d['body']}
  </div>
</main>
"""
    return out + footer(L)


def notfound():
    t = T["it"]
    out = head("it", t["nf_title"], t["nf_t"], "/404", "/404", noindex=True)
    out += header("it", "/", "/en/")
    out += f"""<main id="main" class="notfound">
  <div class="wrap">
    <p class="eyebrow">Carlo Mora Parrucchieri</p>
    <h1>{t['nf_h1']}<span style="color:var(--oro)">#</span></h1>
    <p class="lead">{t['nf_t']}<br><span lang="en">{T['en']['nf_t']}</span></p>
    <div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:36px">
      <a class="btn btn-oro" href="/">{t['nf_btn']}</a>
      <a class="btn btn-linea" href="/en/" lang="en">{T['en']['nf_btn']}</a>
    </div>
  </div>
</main>
"""
    return out + footer("it")


def sitemap():
    pairs = [("/", "/en/", "1.0"), ("/privacy/", "/en/privacy/", "0.3"), ("/cookie/", "/en/cookie/", "0.3")]
    rows = []
    for it, en, pr in pairs:
        for loc in (it, en):
            rows.append(f"""  <url>
    <loc>{SITE}{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <priority>{pr}</priority>
    <xhtml:link rel="alternate" hreflang="it" href="{SITE}{it}"/>
    <xhtml:link rel="alternate" hreflang="en" href="{SITE}{en}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{it}"/>
  </url>""")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(rows) + "\n</urlset>\n")


def write(rel, text):
    p = PUB / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print("scritto", rel)


if __name__ == "__main__":
    write("index.html", home("it"))
    write("en/index.html", home("en"))
    for L in ("it", "en"):
        base = "" if L == "it" else "en/"
        write(f"{base}privacy/index.html", legal(L, "privacy"))
        write(f"{base}cookie/index.html", legal(L, "cookie"))
    write("404.html", notfound())
    write("sitemap.xml", sitemap())
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    write("llms.txt", LLMS)
    write("site.webmanifest", json.dumps({
        "name": "Carlo Mora Parrucchieri", "short_name": "Carlo Mora", "start_url": "/", "display": "browser",
        "background_color": "#0c0c0c", "theme_color": "#0c0c0c",
        "icons": [{"src": "/assets/img/logo-cm-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/img/logo-cm-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2) + "\n")
    print("versione asset:", V)
