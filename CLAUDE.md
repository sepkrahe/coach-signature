# coach-signature — Claude Instructions

Email signature for Thomas Stiegler (executive-coachings.com). Sibling of `sepkrahe/rocket-signature`; keep the two in the same shape.

- Public repo: GitHub Pages serves `bilder/` at `https://signatur.executive-coachings.com/bilder/`. Everything committed is public.
- `daten.json` holds the real contact data and stays local (gitignored). Never commit it. Sep: phone number and email address never go to GitHub, in any file (README, memory.md, examples, commit messages). The built `dist/` stays local too.
- Colors and type come from the claude.ai design system "Executive Coachings" (https://claude.ai/artifact/BacdKe8KtJ3AkkjxEA9qEu). Change them there first, then in `build.py`.
- After any change: `python3 build.py https://signatur.executive-coachings.com/bilder dist` and `python3 lint.py dist/snippet-mit-adresse.html` (and `ohne-adresse`) must print ALL PASS.
