# coach-signature

Bilder und Vorlage für die E-Mail-Signatur von Thomas Stiegler, executive-coachings.com.
Die Bilder werden über GitHub Pages unter `https://signatur.executive-coachings.com/bilder/` ausgeliefert.

Farben und Schriften stammen aus dem Design System "Executive Coachings"
(https://claude.ai/artifact/BacdKe8KtJ3AkkjxEA9qEu): Navy `#1F2D3D`, Slate `#6B7C8C`,
gedämpfter Text `#5E6E7D`, Fläche `#F7F7F7`; Name und Tagline in Libre Baskerville
(Fallback Baskerville/Georgia), Text in Helvetica/Arial (Almarai läuft in E-Mail-Programmen nicht).

## Inhalt
- `bilder/` – Logo und Icons (PNG, doppelte Auflösung)
- `build.py` – erzeugt die Signatur: `python3 build.py https://signatur.executive-coachings.com/bilder dist`
- `lint.py` – prüft die Signatur auf E-Mail-Kompatibilität: `python3 lint.py dist/snippet-mit-adresse.html`
- `test_render.py` – rendert 7 simulierte E-Mail-Programme (Apple Mail, Gmail, Outlook, Bilder blockiert, Dark Mode, Smartphone)
- `.claude/skills/email-signature/SKILL.md` – Anleitung für Claude Code: Regeln, Bauen, Testen, Installieren
- `daten.example.json` – Vorlage für die Kontaktdaten. Die echten Daten liegen nur lokal in `daten.json` (nicht im Repository). Ist `telefon` leer, entfällt die Telefonzeile.

## Ausgabe (`dist/`)
- `signatur-*.html` – Vorschau im Browser; in Safari öffnen, alles markieren, in Apple Mail / Outlook einfügen
- `apple-mail-*.txt` – Inhalt für eine `.mailsignature`-Datei
- `snippet-*.html` – reines HTML für Gmail, Outlook oder andere Werkzeuge

Je eine Variante mit und ohne Adresse.

## Umgesetzte Best Practices
- Bilder über https gehostet statt eingebettet (Gmail blockiert Base64-Bilder)
- Bilder in doppelter Auflösung mit festen `width`/`height`-Attributen
- Tabellen-Layout, nur Inline-CSS, 460 px breit, auf Mobilgeräten fließend
- Hintergrundfarben zusätzlich als `bgcolor` (Outlook)
- Icons dekorativ (`alt=""`), Logo mit Alt-Text
- Unter 10.000 Zeichen (Gmail-Limit), nur ASCII
- Kontrast mindestens 4,5:1 für Text
- Auf dem Smartphone (360 px) keine einzelnen Wörter in einer Zeile; Rollen und Adresse brechen nur am Mittelpunkt

Kontaktdaten werden bewusst nicht veröffentlicht.
