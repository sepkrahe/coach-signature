# coach-signature — memory

## 2026-10-30
- Created from rocket-signature's layout, styled with the "Executive Coachings" design system (built the same day from executive-coachings.com).
- Open: Thomas's phone number is not on the website, so `daten.json` has no `telefon` and the phone row is omitted. Add it to the local `daten.json` and rebuild.
- Open: custom domain (e.g. `signatur.executive-coachings.com`) needs a DNS CNAME at the domain's registrar, then a `CNAME` file here and a rebuild with the new image URL.
