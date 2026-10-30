"""Build the email signature HTML following email-client best practices.

Colors and type come from the "Executive Coachings" design system
(https://claude.ai/artifact/BacdKe8KtJ3AkkjxEA9qEu).

Usage: python3 build.py <image_base_url> <out_dir>
"""
import sys, os

BASE = sys.argv[1].rstrip("/")
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)

FONT = "Helvetica, Arial, sans-serif"          # Almarai is not available in mail clients
SERIF = "'Libre Baskerville', Baskerville, Georgia, serif"
NAVY = "#1F2D3D"   # navy / ink
MUTED = "#5E6E7D"  # muted (slate darkened to 5.3:1 for small text)
CARD = "#F7F7F7"   # mist
WHITE = "#FFFFFF"

import json
_d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "daten.json")))
NAME = _d["name"]
LINKS = {
    "phone": (_d.get("telefon_link", ""), _d.get("telefon", ""), "Telefon"),
    "mail": ("mailto:" + _d["email"], _d["email"], "E-Mail"),
    "web": (_d["website_link"], _d["website"], "Website"),
    "linkedin": (_d["linkedin_link"], "LinkedIn", "LinkedIn"),
}
ADDRESS = _d["adresse"]
TAGLINE = _d["tagline"]
ROLES = _d["rollen"]


def icon(name, alt):
    return (f'<img src="{BASE}/sig-{name}.png" width="22" height="22" alt="" '
            f'style="display:block;width:22px;height:22px;border:0;outline:none;">')


def contact(name, pad_bottom, pad_right):
    href, label, alt = LINKS[name]
    return (
        f'<td width="30" valign="middle" style="padding:0 0 {pad_bottom}px 0;width:30px;">{icon(name, alt)}</td>'
        f'<td valign="middle" style="padding:0 {pad_right}px {pad_bottom}px 0;font-family:{FONT};font-size:13px;line-height:18px;color:{NAVY};">'
        f'<a href="{href}" style="color:{NAVY};text-decoration:none;">{label}</a></td>'
    )


def build(with_address):
    # The phone row is optional: it is left out when daten.json has no number.
    rows = [n for n in ("phone", "mail", "web", "linkedin") if LINKS[n][1]]
    contacts = "\n".join(f"<tr>{contact(n, 0 if n == rows[-1] else 7, 0)}</tr>" for n in rows)
    address = (
        f'<tr><td colspan="2" style="padding:12px 0 0 0;font-family:{FONT};font-size:12px;line-height:16px;color:{MUTED};">{ADDRESS}</td></tr>'
        if with_address else ""
    )
    return f'''<table cellpadding="0" cellspacing="0" border="0" role="presentation" width="460" style="border-collapse:collapse;width:100%;max-width:460px;font-family:{FONT};">
<tr><td bgcolor="{CARD}" style="background-color:{CARD};padding:20px 20px;">
<table cellpadding="0" cellspacing="0" border="0" role="presentation" width="100%" style="border-collapse:collapse;width:100%;">
<tr>
<td width="82" valign="top" style="padding:2px 18px 0 0;width:64px;"><a href="{LINKS["web"][0]}" style="text-decoration:none;"><img src="{BASE}/sig-logo.png" width="64" height="58" alt="Executive Coachings" style="display:block;width:64px;height:58px;border:0;outline:none;"></a></td>
<td valign="top" width="100%">
<table cellpadding="0" cellspacing="0" border="0" role="presentation" width="100%" style="border-collapse:collapse;width:100%;">
<tr><td colspan="2" style="font-family:{SERIF};font-size:18px;line-height:24px;font-weight:normal;letter-spacing:1px;text-transform:uppercase;color:{NAVY};">{NAME}</td></tr>
<tr><td colspan="2" style="padding:4px 0 14px 0;font-family:{FONT};font-size:12px;line-height:16px;color:{MUTED};">{ROLES}</td></tr>
{contacts}
{address}
</table>
</td>
</tr>
</table>
</td></tr>
<tr><td bgcolor="{NAVY}" style="background-color:{NAVY};padding:11px 20px;font-family:{SERIF};font-size:11px;line-height:15px;letter-spacing:1px;text-transform:uppercase;color:{WHITE};">{TAGLINE}</td></tr>
</table>'''


HEADER = ("Content-Transfer-Encoding: 7bit\n"
          "Content-Type: text/html;\n\tcharset=us-ascii\n"
          "Mime-Version: 1.0 (Mac OS X Mail 16.0)\n\n")

for with_address, slug in [(True, "mit-adresse"), (False, "ohne-adresse")]:
    sig = build(with_address)
    assert all(ord(c) < 128 for c in sig), "non-ASCII character in signature"
    # 1) Standalone HTML page (preview / Safari)
    with open(f"{OUT}/signatur-{slug}.html", "w") as f:
        f.write('<!DOCTYPE html><html lang="de"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width, initial-scale=1">'
                f'<title>Signatur {NAME}</title></head><body style="margin:0;padding:24px;background:#ffffff;">{sig}</body></html>\n')
    # 2) Apple Mail .mailsignature content
    with open(f"{OUT}/apple-mail-{slug}.txt", "w") as f:
        f.write(HEADER + '<body style="word-wrap: break-word; -webkit-nbsp-mode: space; line-break: after-white-space;">'
                f'<div><br></div>{sig}</body>\n')
    # 3) Bare snippet (Gmail / Outlook / other tools)
    with open(f"{OUT}/snippet-{slug}.html", "w") as f:
        f.write(sig + "\n")
print("built", OUT)
