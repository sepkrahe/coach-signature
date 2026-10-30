---
name: email-signature
description: Build, change, test and install Thomas Stiegler's HTML email signature (executive-coachings.com) so it works in Apple Mail, Gmail, Outlook and phone mail apps. Use when creating or editing the signature in this repository, adding a variant, changing its images, or when a signature shows broken images, lost layout or "?" boxes.
---

# Email signature: build, test, install

This repository holds Thomas Stiegler's email signature for Apple Mail and
other mail programs. It follows the current best practices for email-client
compatibility. Read this whole file before changing anything. Its sibling
`sepkrahe/rocket-signature` follows the same rules; keep the two in step.

## What lives where

| Path | Public? | What |
|---|---|---|
| `bilder/` | yes (GitHub Pages) | Logo and icons as PNG at 2x display size |
| `build.py` | yes | Builds the signature from a template |
| `lint.py` | yes | Compatibility checks (13 rules) |
| `test_render.py` | yes | Renders 7 simulated client scenarios |
| `daten.example.json` | yes | Placeholder contact data |
| `daten.json` | **no** (gitignored) | The real contact data |
| `dist/` | **no** (gitignored) | Generated signatures |

Images are served at `https://signatur.executive-coachings.com/bilder/`
(GitHub Pages with a custom domain; DNS CNAME `signatur` →
`sepkrahe.github.io` at Squarespace; HTTPS enforced).

**Privacy rule:** the repository is public. Never commit phone numbers,
email addresses, postal addresses or generated signatures, in any file or
commit message. Before every commit, run:
`git grep -nE "@[a-z0-9-]+\.[a-z]|\+49|[0-9]{5} [A-Z]" -- . ':!daten.example.json' ':!.claude/skills'`
and stop if it finds real data. Commit as
`sepkrahe <sepkrahe@users.noreply.github.com>` (set in this repo's git config).

## The rules (from research; each one fixes a real failure)

1. **Host images; never embed them.** Gmail does not display base64 /
   `data:` images, and some spam filters flag such mail. Images are PNG at
   an `https://` URL. No SVG: most clients don't show it.
2. **Images at display size, 2x pixels, with `width` and `height`
   attributes** on every `<img>`: logo 56 × 50 (file 112 × 100), icons
   22 × 22 (file 44 × 44). Without the attributes, Outlook and Apple Mail's
   paste show images at full pixel size.
3. **Tables for layout, inline styles only.** No `<style>`, no classes,
   no flexbox, grid, `position`, `float`, media queries or
   `background-image`. The one allowed `div` use is the hybrid columns
   in rule 5.
4. **Background colours twice:** `bgcolor` attribute and inline
   `background-color` (Outlook Desktop reads the attribute).
5. **Width:** 540px with `width="540"` and
   `style="width:100%;max-width:540px"`: fixed in Outlook, fluid on phones.
   The contacts sit in two columns side by side (as in rocket-signature)
   as **hybrid columns**: two `display:inline-block` divs with
   `width:100%;max-width:<n>px` (206px: phone, website; 226px: email,
   LinkedIn, the longest line) that wrap under each other on narrow
   screens, inside a cell with `font-size:0`, plus an `<!--[if mso]>`
   two-column table for Outlook Desktop, which ignores `max-width`. A
   plain two-column table would be cut off on phones. Gaps between an
   icon and its text are padding, not cell width, so a phone cannot
   squeeze them away.
6. **Fonts:** text in `Helvetica, Arial, sans-serif` (the brand's Almarai
   is a web font; mail clients don't load it). Name and tagline in
   `'Libre Baskerville', Baskerville, Georgia, serif`: Apple Mail shows
   Baskerville, other clients Georgia, both installed system fonts.
7. **Corners are square**, as in the design system, so Outlook Desktop
   looks the same as everything else.
8. **Alt text:** the logo gets `alt="Executive Coachings"`; icons next to
   text are decorative, `alt=""`.
9. **Dark mode:** explicit background colours on the card and the band.
   Check both a full colour inversion (Outlook.com, Gmail app) and a dark
   page behind the light card (Apple Mail).
10. **Size:** under 10,000 characters (Gmail's signature limit), ASCII
    only (non-ASCII as HTML entities like `&auml;` and `&middot;`), so Apple
    Mail's 7-bit `.mailsignature` file stays valid.
11. **Links:** absolute only (`https://`, `mailto:`, `tel:`).
12. **Contrast:** text at least 4.5:1 against its background, icons 3:1.
    Current values: name and contacts navy on mist 13.1:1, roles and
    address `#5E6E7D` on mist 4.9:1, icon glyphs and tagline white on navy
    14:1. Never use the brand's slate `#6B7C8C` for small text (4.0:1 on
    mist).
13. **Line breaks on phones:** lines made of parts ("A · B · C": roles,
    address) get one break point, after their first half; `build.py`
    (`keep_parts`) joins everything else with `&nbsp;`. At 360px the name
    must stay on one line and no line may hold a single word. An empty
    `telefon` leaves the phone row out of the left column; the email
    address then moves up into it.

Design source: the **Executive Coachings** design system
(https://claude.ai/artifact/BacdKe8KtJ3AkkjxEA9qEu), component
`EmailSignature`, which documents every colour and size. Colours: navy
`#1F2D3D` (text, icons, band), muted `#5E6E7D` (roles: 11px bold
capitals, 1.2px tracking; address), mist `#F7F7F7` (card),
white. One accent only: the navy band with the tagline "Klarheit. Kraft.
Konsequenz.". No gradients, no shadows, no call-to-action button. Change a
colour in the design system first, then in `build.py`.

## Build

```bash
cp daten.example.json daten.json   # first time only, then fill in real data
python3 build.py https://signatur.executive-coachings.com/bilder dist
```

An empty `telefon` leaves the phone row out. This writes, per variant
(`mit-adresse`, `ohne-adresse`):
- `dist/signatur-*.html`: preview page
- `dist/apple-mail-*.txt`: complete `.mailsignature` content (headers included)
- `dist/snippet-*.html`: bare signature HTML for other programs

Change the design in `build.py` (the template), contact data in
`daten.json`. Never hand-edit files in `dist/`.

## Test (all three steps, every change)

1. **Lint:** `python3 lint.py dist/snippet-mit-adresse.html` and the same
   for `ohne-adresse`. Every line must say PASS.
2. **Render:** serve the images over http (WebKit refuses some `file://`
   images, which shows up as false "images did not load" failures), build
   a test copy against that server, and render both variants:
   ```bash
   python3 -m http.server 8765 --bind 127.0.0.1 &
   python3 build.py http://127.0.0.1:8765/bilder /tmp/sig-test
   for v in mit ohne; do
     uv run --no-project --with playwright==1.64.1 --with pillow \
       python test_render.py /tmp/sig-test/signatur-$v-adresse.html /tmp/sig-test/tests-$v
   done
   kill %1
   ```
   On kalahari, Playwright 1.64.1 matches the browsers already cached in
   `~/.cache/ms-playwright` (Chromium 1248, WebKit 2370); elsewhere run
   `python3 -m playwright install chromium webkit` once.
   Open each `overview.png` and look at every scenario: Apple Mail
   (WebKit), Gmail web (Chromium), Outlook Desktop (fixed width), images
   blocked, dark mode inverted, dark page behind the card, phone at 360px.
   Check: nothing cut off, no single-word lines, the name on one line,
   images the right size, text readable in dark mode. The script also
   reports images that fail to load.
3. **Real clients:** after installing, send a test email to a Gmail
   address and, if available, Outlook.com and an iPhone. Gmail may ask to
   show images first; that is normal. Simulations don't replace this.

## Publish image changes

Images go live by pushing to `main`; GitHub Pages redeploys within a
minute or two. Keep file names stable: installed signatures load images
by name, so replacing `bilder/sig-logo.png` updates every signature
already sent or installed. A new image name means reinstalling. If a
logo's display size changes, change `width`/`height` in `build.py` in the
same commit and reinstall.

## Install in Apple Mail (the only reliable way)

Copying the preview from Safari into Mail's signature editor breaks the
table layout and attaches the images to every mail. Instead:

1. Mail → Einstellungen → Signaturen: select the account that actually
   sends, click **+**, name the signature, type `XXX`. Quit Mail with ⌘Q.
2. Open `~/Library/Mail/V10/MailData/Signatures/` (the `V` number can
   differ; use the highest). Sort by date modified; the newest
   `.mailsignature` file is the new one.
3. If the file is locked: Get Info (Informationen) → uncheck Locked
   (Geschützt).
4. Replace the file's ENTIRE content with
   `dist/apple-mail-<variant>.txt` (it includes the right headers):
   `cp dist/apple-mail-mit-adresse.txt "<that file>"`.
5. Lock the file again (`chflags uchg "<file>"`, or Get Info → Locked),
   otherwise Mail overwrites it.
6. Open Mail, ⌘N, choose the signature in the Signature menu.

If the signature doesn't appear in a new mail's menu, it is assigned to
the wrong account: drag it from "Alle Signaturen" onto the account that
sends the mail, then set "Signatur auswählen" for that account.

For Outlook (outlook.com and Outlook accounts): Settings → Mail → Compose and reply
→ Email signature; open `dist/signatur-<variant>.html` in a browser,
select the signature, copy, paste. Send a test mail afterwards.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Grey boxes instead of images in Gmail | base64 images | host images (rule 1) |
| "?" boxes in Apple Mail | image URL unreachable or changed | check the URL in a browser; keep file names stable |
| Huge logo and icons, layout broken | signature pasted through Mail's editor | install via the `.mailsignature` file |
| Signature missing from the menu | wrong account | assign it to the sending account |
| Images attached to every mail | images pasted into Mail's editor | install via the file, with hosted images |
| Name or roles break oddly on a phone | text too long for 360px | shorten it in `daten.json`; keep "A &middot; B" parts |
