import math
import os
from urllib.parse import quote

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 1280, 360
CX, CY, R = 1030, 180, 140
POINTS = 200
FRAMES = 20
DURATION = 28
TILT = 0.42
SANS = "Inter, 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SF Mono', Menlo, Consolas, monospace"
LABELS = {11: "NEXT.JS", 37: "REACT", 63: "TYPESCRIPT", 89: "NODE", 115: "SEO", 141: "API", 167: "FRAMER", 191: "DESIGN"}
THEMES = {
    "light": {"bg": "#ffffff", "fg": "#0d0e12", "muted": "#0d0e12"},
    "dark": {"bg": "#0d0e12", "fg": "#e6e6e6", "muted": "#e6e6e6"},
}


def sphere():
    golden = math.pi * (3 - math.sqrt(5))
    for i in range(POINTS):
        y = 1 - (i / (POINTS - 1)) * 2
        radius = math.sqrt(1 - y * y)
        theta = golden * i
        yield math.cos(theta) * radius, y, math.sin(theta) * radius


def project(x, y, z, angle):
    c, s = math.cos(angle), math.sin(angle)
    x1, z1 = x * c + z * s, -x * s + z * c
    ct, st = math.cos(TILT), math.sin(TILT)
    y2, z2 = y * ct - z1 * st, y * st + z1 * ct
    depth = (z2 + 1) / 2
    return CX + x1 * R, CY + y2 * R, depth


def values(seq):
    return ";".join(f"{v:.1f}" if isinstance(v, float) else str(v) for v in seq)


def banner(theme):
    t = THEMES[theme]
    key_times = ";".join(f"{k / FRAMES:.4f}" for k in range(FRAMES + 1))
    anim = f'dur="{DURATION}s" repeatCount="indefinite" calcMode="linear" keyTimes="{key_times}"'
    dots, labels = [], []
    for index, (x, y, z) in enumerate(sphere()):
        frames = [project(x, y, z, 2 * math.pi * k / FRAMES) for k in range(FRAMES + 1)]
        xs = [f[0] for f in frames]
        ys = [f[1] for f in frames]
        rs = [0.5 + f[2] * 2.3 for f in frames]
        ops = [0.25 + f[2] * 0.75 for f in frames]
        dots.append(
            f'<circle cx="{xs[0]:.1f}" cy="{ys[0]:.1f}" r="{rs[0]:.2f}">'
            f'<animate attributeName="cx" values="{values(xs)}" {anim}/>'
            f'<animate attributeName="cy" values="{values(ys)}" {anim}/>'
            f'<animate attributeName="r" values="{";".join(f"{v:.2f}" for v in rs)}" {anim}/>'
            "</circle>"
        )
        if index in LABELS:
            label_ops = [max(0.0, min(1.0, (f[2] - 0.55) / 0.2)) for f in frames]
            labels.append(
                f'<text x="{xs[0]:.1f}" y="{ys[0] - 9:.1f}" fill-opacity="{label_ops[0]:.2f}">{LABELS[index]}'
                f'<animate attributeName="x" values="{values(xs)}" {anim}/>'
                f'<animate attributeName="y" values="{values([v - 9 for v in ys])}" {anim}/>'
                f'<animate attributeName="fill-opacity" values="{";".join(f"{v:.2f}" for v in label_ops)}" {anim}/>'
                "</text>"
            )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Maksym Vasianin — Websites that bring clients. Apps that save hours.">
<rect width="{W}" height="{H}" fill="{t['bg']}"/>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" fill="none" stroke="{t['fg']}" stroke-opacity="0.15"/>
<text x="64" y="92" fill="{t['muted']}" fill-opacity="0.6" font-family="{MONO}" font-size="16" letter-spacing="3">MAKSYM VASIANIN — FULL-STACK DEVELOPER</text>
<text x="62" y="168" fill="{t['fg']}" font-family="{SANS}" font-size="54" font-weight="700" letter-spacing="-1.5">Websites that bring clients.</text>
<text x="62" y="232" fill="{t['fg']}" font-family="{SANS}" font-size="54" font-weight="700" letter-spacing="-1.5">Apps that save hours.</text>
<text x="64" y="290" fill="{t['muted']}" fill-opacity="0.7" font-family="{SANS}" font-size="20">Websites and web apps for businesses · maksymvasianin.com</text>
<g fill="{t['fg']}">{''.join(dots)}</g>
<g fill="{t['fg']}" font-family="{MONO}" font-size="11" font-weight="600" text-anchor="middle">{''.join(labels)}</g>
</svg>
"""


def badge(label, logo, href, alt):
    text = quote(label.replace("-", "--").replace(" ", "_"))
    light = f"https://img.shields.io/badge/{text}-0d0e12?style=for-the-badge&logo={logo}&logoColor=white"
    dark = f"https://img.shields.io/badge/{text}-e6e6e6?style=for-the-badge&logo={logo}&logoColor=0d0e12"
    image = (
        f'<picture><source media="(prefers-color-scheme: dark)" srcset="{dark}">'
        f'<img alt="{alt}" src="{light}"></picture>'
    )
    return f'<a href="{href}">{image}</a>' if href else image


def themed(light, dark, alt, extra=""):
    return (
        f'<picture><source media="(prefers-color-scheme: dark)" srcset="{dark}">'
        f'<img alt="{alt}" src="{light}"{extra}></picture>'
    )


CONTACTS = [
    ("maksymvasianin.com", "googlechrome", "https://maksymvasianin.com", "Website"),
    ("Telegram", "telegram", "https://t.me/wmm_02", "Telegram"),
    ("LinkedIn", "linkedin", "https://www.linkedin.com/in/m-vasianin/", "LinkedIn"),
    ("Email", "gmail", "mailto:vasanin02@gmail.com", "Email"),
    ("Support on Patreon", "patreon", "https://www.patreon.com/cw/VasianinMaksim", "Patreon"),
]
STACK = [
    ("TypeScript", "typescript"), ("React", "react"), ("Next.js", "nextdotjs"), ("Node.js", "nodedotjs"),
    ("NestJS", "nestjs"), ("Tailwind CSS", "tailwindcss"), ("Framer", "framer"), ("Figma", "figma"),
    ("Firebase", "firebase"), ("Vercel", "vercel"),
]
STREAK = "https://streak-stats.demolab.com?user=maximwas&hide_border=true&date_format=j%20M%5B%20Y%5D"
STREAK_LIGHT = STREAK + "&background=FFFFFF&stroke=E6E6E6&ring=0D0E12&fire=0D0E12&currStreakNum=0D0E12&sideNums=0D0E12&currStreakLabel=0D0E12&sideLabels=0D0E12&dates=6B6B6B"
STREAK_DARK = STREAK + "&background=0D0E12&stroke=2A2B30&ring=E6E6E6&fire=E6E6E6&currStreakNum=E6E6E6&sideNums=E6E6E6&currStreakLabel=E6E6E6&sideLabels=E6E6E6&dates=9A9A9A"
LANGS = "https://github-readme-stats.vercel.app/api/top-langs/?username=maximwas&layout=compact&hide_border=true&langs_count=6"
LANGS_LIGHT = LANGS + "&bg_color=ffffff&title_color=0d0e12&text_color=0d0e12"
LANGS_DARK = LANGS + "&bg_color=0d0e12&title_color=e6e6e6&text_color=e6e6e6"
MARKET = "maksym-vasianin.px-to-tailwind-plus"


def readme():
    contacts = "\n  ".join(badge(*c) for c in CONTACTS)
    stack = " · ".join(name for name, _ in STACK)
    banner_img = themed("./assets/banner-light.svg", "./assets/banner-dark.svg",
                        "Maksym Vasianin — Websites that bring clients. Apps that save hours.", ' width="100%"')
    streak = themed(STREAK_LIGHT, STREAK_DARK, "GitHub contribution streak", ' height="170"')
    langs = themed(LANGS_LIGHT, LANGS_DARK, "Most used languages", ' height="170"')
    return f"""{banner_img}

<p>
  {contacts}
</p>

Independent full-stack developer from Ukraine. I build websites and web applications for businesses — from the first conversation to a launched product, and support after launch. You work with me directly.

## What I do

| | |
| --- | --- |
| **Websites** — modern sites on Next.js, React and TypeScript, from a finished design or an agreed structure, with SEO and accessibility in place. | **Business web applications** — user accounts, booking systems, internal tools, integrations and process automation. |
| **Fast launches on Framer** — landing pages and small sites on a tight timeline, without losing quality. | **Support and development** — bug fixes, new features, updates and performance work on existing projects. |

## How I work

| 01 · Discovery | 02 · Planning | 03 · Development | 04 · Launch |
| --- | --- | --- | --- |
| I get to know the project, define the goals and the result you expect. | I estimate the scope and timeline, and choose the right approach to build it. | I build the functionality, implement the design and integrate the services you need. | Testing, publishing the project and support after release. |

## Stack

{stack}

## Open source

| Project | What it does | |
| --- | --- | --- |
| [**framer-sitewright**](https://github.com/maximwas/framer-sitewright) | MCP server and CLI that let AI agents build and edit Framer sites, with a local journal you can undo. | [Docs](https://maximwas.github.io/framer-sitewright/) |
| [**px-to-tailwind-plus**](https://github.com/maximwas/px-to-tailwind-plus) | VS Code and Cursor extension: type `p-16px`, get `p-4`; Tailwind v3 and v4. | <a href="https://marketplace.visualstudio.com/items?itemName={MARKET}"><img alt="Installs" src="https://img.shields.io/visual-studio-marketplace/i/{MARKET}?label=installs&color=0d0e12&style=flat-square"></a> |

## Activity

<p>
  {streak}
  {langs}
</p>

---

<p align="center">
  Open for new projects → <a href="https://maksymvasianin.com"><b>maksymvasianin.com</b></a><br>
  Українською: незалежний Full-Stack розробник — сайти та вебзастосунки для бізнесу · <a href="https://maksymvasianin.com/ua">maksymvasianin.com/ua</a>
</p>
"""


os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
for name in THEMES:
    with open(os.path.join(OUT, "assets", f"banner-{name}.svg"), "w") as f:
        f.write(banner(name))
with open(os.path.join(OUT, "README.md"), "w") as f:
    f.write(readme())
for name in THEMES:
    print(name, os.path.getsize(os.path.join(OUT, "assets", f"banner-{name}.svg")), "bytes")
print("README", os.path.getsize(os.path.join(OUT, "README.md")), "bytes")
