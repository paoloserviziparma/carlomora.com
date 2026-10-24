# carlomora.com

Sito di **Carlo Mora Parrucchieri**, Viale Mentana 12/a, 43121 Parma.
Sito statico in HTML, CSS e JavaScript, senza framework. Netlify pubblica la cartella `public/` così com'è, senza build.

## Struttura

```
public/
  index.html            home italiano
  en/index.html         home inglese
  privacy/, cookie/     privacy e cookie policy (IT)
  en/privacy/, en/cookie/  versioni inglesi
  404.html
  sitemap.xml, robots.txt, site.webmanifest, favicon.ico, apple-touch-icon.png
  assets/css/style.css
  assets/js/main.js
  assets/fonts/         Archivo (variabile) e Instrument Serif, ospitati in locale
  assets/img/           foto in WebP a più larghezze, logo, immagine Open Graph
tools/build.py          generatore delle pagine HTML (si lancia in locale)
netlify.toml            redirect, intestazioni di sicurezza, cache
```

## Modificare testi e pagine

Tutti i testi (IT ed EN), i testi legali e i dati strutturati sono in `tools/build.py`. Dopo una modifica:

```
python3 tools/build.py
```

Lo script rigenera le pagine in `public/` e aggiorna il numero di versione di CSS e JS (`?v=…`, un hash del contenuto). Va lanciato anche dopo ogni modifica a `style.css` o `main.js`, poi si fa commit dei file generati.

## Prenotazioni

Il sito non ha moduli. Tutti i pulsanti di prenotazione sono link `https://wa.me/393911156147?text=…`: da telefono aprono l'app WhatsApp con un messaggio già scritto, da computer aprono WhatsApp Web. Il risultato del test "Quale Arcano sei?" aggiunge al messaggio il nome della carta.

## Animazioni

- Testi dell'hero in entrata e titoli delle sezioni che compaiono parola per parola.
- Blocchi che compaiono allo scroll con IntersectionObserver.
- Parallax leggero su hero, galleria e foto "Prima volta", dimezzato su mobile.
- Intestazione fissa che sparisce in dissolvenza scorrendo in giù e ricompare scorrendo in su.
- Menu a tendina sotto i 1080 px.
- Tutto si disattiva con `prefers-reduced-motion`.

## Statistiche, privacy e cookie

Nessun cookie e nessuno script di tracciamento, quindi nessun banner. Le statistiche si leggono da **Netlify Analytics**, che lavora sui log del server: va attivato nel pannello Netlify del sito (Site configuration → Analytics). Font e immagini sono locali: il sito non contatta servizi esterni.

I testi di privacy e cookie policy sono quelli del sito originale, riportati come pagine interne (`tools/legal.py`); le versioni inglesi sono traduzioni di cortesia. Parlano ancora di Wix, banner cookie, cookie statistici ed e-commerce, che il nuovo sito non ha: **vanno aggiornati e fatti verificare da un consulente**.

## Immagini

- Le foto vengono virate leggermente sui toni del sito: 30% di duotono nero → bianco osso.
- Le immagini hanno cache di un anno. Se ne sostituisci una, salvala con un nome nuovo.
- Crediti: foto della collezione **Alchemy F/W 2026 © Art Hair Studios by Wella**, usate in quanto salone della rete. Prima della messa online va confermato con Wella che l'uso sul sito è consentito.
- `giustizia` e `torre` arrivano dal sito Art Hair Studios a 800 px: andrebbero sostituite con gli originali ad alta risoluzione.

## Video

Nell'hero c'è un video in loop, muto e senza audio: `assets/video/hero-720.mp4` per computer e `hero-480.mp4` per telefono, più l'immagine di anteprima `hero-poster.webp`.
- Il loop è reso continuo con una dissolvenza di 1,5 secondi tra la fine e l'inizio.
- Il video si ferma quando l'hero esce dallo schermo e non parte con `prefers-reduced-motion`.
- Fonte: Mixkit, "Portrait of a young model with wind in her hair" (41662), licenza Mixkit Stock Video Free License: uso commerciale consentito, attribuzione non richiesta.
- Per sostituirlo basta mettere nuovi file con nomi diversi e aggiornare `tools/build.py`. Se `hero-720.mp4` non c'è, l'hero torna alla foto.

## Font

Archivo e Instrument Serif, licenza SIL Open Font License 1.1.
