import hashlib
import math
import os
from urllib.parse import quote

# The script lives in scripts/, the README and assets in the repo root.
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1280, 360
CX, CY, R = 1030, 180, 140
POINTS = 200
FRAMES = 20
DURATION = 28
TILT = 0.42
SANS = "Inter, 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SF Mono', Menlo, Consolas, monospace"
LABELS = {11: "NEXT.JS", 37: "REACT", 63: "TYPESCRIPT", 89: "NODE", 115: "NESTJS", 141: "POSTGRES", 167: "MCP", 191: "AI"}
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
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Maksym Vasianin — full-stack developer. Web apps and AI products, end to end in TypeScript.">
<rect width="{W}" height="{H}" fill="{t['bg']}"/>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" fill="none" stroke="{t['fg']}" stroke-opacity="0.15"/>
<text x="64" y="92" fill="{t['muted']}" fill-opacity="0.6" font-family="{MONO}" font-size="16" letter-spacing="3">MAKSYM VASIANIN — FULL-STACK DEVELOPER</text>
<text x="62" y="168" fill="{t['fg']}" font-family="{SANS}" font-size="54" font-weight="700" letter-spacing="-1.5">Web apps and AI products,</text>
<text x="62" y="232" fill="{t['fg']}" font-family="{SANS}" font-size="54" font-weight="700" letter-spacing="-1.5">end to end in TypeScript.</text>
<text x="64" y="290" fill="{t['muted']}" fill-opacity="0.7" font-family="{SANS}" font-size="20">React · Next.js · Node.js · 5+ years in production · Ukraine</text>
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
    ("CV", "readdotcv", "https://cv.maksymvasianin.com", "CV"),
    ("LinkedIn", "linkedin", "https://www.linkedin.com/in/m-vasianin/", "LinkedIn"),
    ("Email", "gmail", "mailto:vasanin02@gmail.com", "Email"),
]
STACK = [
    "TypeScript", "React", "Next.js", "Node.js", "NestJS", "PostgreSQL (Supabase)", "Firebase", "React Native",
    "Tailwind CSS", "Claude and OpenAI APIs", "MCP", "Vitest", "Playwright", "Docker", "AWS",
]
STREAK = "https://streak-stats.demolab.com?user=maximwas&hide_border=true&date_format=j%20M%5B%20Y%5D"
STREAK_LIGHT = STREAK + "&background=FFFFFF&stroke=E6E6E6&ring=0D0E12&fire=0D0E12&currStreakNum=0D0E12&sideNums=0D0E12&currStreakLabel=0D0E12&sideLabels=0D0E12&dates=6B6B6B"
STREAK_DARK = STREAK + "&background=0D0E12&stroke=2A2B30&ring=E6E6E6&fire=E6E6E6&currStreakNum=E6E6E6&sideNums=E6E6E6&currStreakLabel=E6E6E6&sideLabels=E6E6E6&dates=9A9A9A"
MARKET = "maksym-vasianin.px-to-tailwind-plus"


def readme():
    contacts = "\n  ".join(badge(*c) for c in CONTACTS)
    stack = " · ".join(STACK)
    # The content hash in the query busts GitHub's 5-minute image cache after every banner change.
    version = hashlib.sha1(banner("light").encode()).hexdigest()[:8]
    banner_img = themed(f"./assets/banner-light.svg?v={version}", f"./assets/banner-dark.svg?v={version}",
                        "Maksym Vasianin — full-stack developer. Web apps and AI products, end to end in TypeScript.", ' width="100%"')
    streak = themed(STREAK_LIGHT, STREAK_DARK, "GitHub contribution streak", ' height="170"')
    return f"""{banner_img}

<p>
  {contacts}
</p>

Full-stack developer from Zhytomyr, Ukraine, writing production code since 2021. I build web apps and AI features end to end: React and Next.js on the front end, Node.js and NestJS on the back end, chatbots, AI agents and MCP servers on the Claude and OpenAI APIs.

## Stack

{stack}

## Projects

| Project | What it does | |
| --- | --- | --- |
| [**pixelwright**](https://github.com/maximwas/pixelwright) | MCP server and Figma plugin that let AI agents (Claude Code, Cursor, Codex) read and edit the Figma file you have open, through the Plugin API: no token, no rate limits. TypeScript, Node.js, WebSockets. | [Docs](https://maximwas.github.io/pixelwright/) |
| [**saldo**](https://github.com/maximwas/saldo) | Personal finance PWA: balances, spending, upcoming payments and the money actually free to spend, each number explained. Shared ledgers with roles, works offline, MCP connector for AI assistants. Next.js 16, React 19, Supabase (Postgres, RLS), TanStack Query, Cloudflare Workers. | In development |
| [**px-to-tailwind-plus**](https://github.com/maximwas/px-to-tailwind-plus) | VS Code and Cursor extension: type `p-16px`, get `p-4`; Tailwind v3 and v4. | [Marketplace](https://marketplace.visualstudio.com/items?itemName={MARKET}) |

## Activity

<p>
  {streak}
</p>

---

<p align="center">
  CV → <a href="https://cv.maksymvasianin.com"><b>cv.maksymvasianin.com</b></a> · <a href="https://maksymvasianin.com">maksymvasianin.com</a><br>
  Українською: Full-Stack розробник — React, Next.js, Node.js, TypeScript · <a href="https://maksymvasianin.com/ua">maksymvasianin.com/ua</a>
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
