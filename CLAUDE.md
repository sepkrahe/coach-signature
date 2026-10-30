# coach-signature — Claude Instructions

Email signature for Thomas Stiegler (executive-coachings.com). Sibling of `sepkrahe/rocket-signature`; keep the two in the same shape.

Before any change, read `.claude/skills/email-signature/SKILL.md`: it has the compatibility rules, build, test and install steps.

- Public repo: GitHub Pages serves `bilder/` at `https://signatur.executive-coachings.com/bilder/`. Everything committed is public.
- `daten.json` holds the real contact data and stays local (gitignored). Never commit it. Sep: phone number and email address never go to GitHub, in any file (README, memory.md, examples, commit messages). Postal addresses and the built `dist/` stay local too. Run the privacy grep from the skill before every commit.
- Colors and type come from the claude.ai design system "Executive Coachings" (https://claude.ai/artifact/BacdKe8KtJ3AkkjxEA9qEu). Change them there first, then in `build.py`.
