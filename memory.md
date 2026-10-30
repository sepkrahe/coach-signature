# coach-signature — memory

## Session log

- **2026-10-30** — Built the "Executive Coachings" design system (claude.ai artifact BacdKe8KtJ3AkkjxEA9qEu) from executive-coachings.com, then this repo as a sibling of `rocket-signature`: hosted images on GitHub Pages at `signatur.executive-coachings.com`, render tests and the `email-signature` skill. Mirrored rocket-signature's later change (contacts in two hybrid columns, 540px). Both repos, the Lift Off and Executive Coachings design systems verified in sync (lint, 28 renders, previews byte-identical to fresh builds). Instructions and both signature files emailed to Thomas from the kalahari agent Gmail.

## Decisions

- Keep this repo and `sepkrahe/rocket-signature` in step: `lint.py`, `test_render.py` and `daten.example.json` stay byte-identical; `build.py` differs only in brand values (colors, fonts, logo, column widths 206/226).
- Contact data (phone, email, address) never goes to GitHub, in any file or commit message (Sep). `daten.json` and `dist/` stay local; run the skill's privacy grep before every commit.
- Commits in this repo use `sepkrahe <sepkrahe@users.noreply.github.com>` (repo-local git config): GitHub rejects pushes carrying the private iCloud address.
- Render tests run with images served over a local http server and `uv run --with playwright==1.64.1` (matches the cached Chromium 1248 / WebKit 2370); `file://` images give false WebKit failures.

## Open items

- `docs/defects/MA-install-1.md`: Thomas still has to install and confirm the signature.
