#!/usr/bin/env python3
"""Generate static, independently addressable homepages for GitHub Pages."""
import argparse
import html
import json
import re
from pathlib import Path
from string import Template
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://magic-xu.github.io/mosaic-legal/"
PLAY = "https://play.google.com/store/apps/details?id=com.magic.snapmosaic"
e = html.escape


def build(check=False):
    sites = json.loads((ROOT / "content/site.json").read_text())
    products = json.loads((ROOT / "content/product.json").read_text())
    if sites.keys() != products.keys():
        raise ValueError("Site and product locales must match")
    template = Template((ROOT / "content/home.html").read_text())
    expected_lengths = {"nav": 5, "hero": 8, "privacy": 5, "tabs": 5,
                        "words": 2, "faces": 2, "faq": 5, "closing": 2, "ui": 5}
    stale = []
    routes = {code: "" if code == "en" else code + "/" for code in sites}
    alternates = "\n".join(
        f'  <link rel="alternate" hreflang="{code}" href="{BASE}{route}">'
        for code, route in routes.items()
    ) + f'\n  <link rel="alternate" hreflang="x-default" href="{BASE}">'

    def output(path, content):
        if check:
            if not path.exists() or path.read_text() != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)

    for code, s in sites.items():
        for key, length in expected_lengths.items():
            if len(s[key]) != length or any(not value.strip() for value in s[key]):
                raise ValueError(f"Incomplete {code}.{key}")
        p = products[code]
        prefix = "./" if code == "en" else "../"
        direction = "rtl" if code == "ur" else "ltr"
        image_lang = "zh" if code == "zh-CN" else "en"
        arrow = f'<img class="icon arrow" src="{prefix}assets/icons/arrow-right.svg" alt="" width="20" height="20">'
        language_links = []
        for other, route in routes.items():
            current = ' aria-current="page"' if other == code else ""
            language_links.append(
                f'          <a href="{prefix}{route}index.html" lang="{other}" '
                f'dir="{"rtl" if other == "ur" else "ltr"}"{current}>{e(sites[other]["native"])}</a>')
        features = [dict(zip(("title", "body"), s["words"])),
                    dict(zip(("title", "body"), s["faces"])), p["styles"], p["watermark"], p["export"]]
        images = ["words", "faces", "effects", "watermark", "export"]
        buttons, panels = [], []
        for i, (feature, name) in enumerate(zip(features, images)):
            buttons.append(f'        <button type="button" id="tab-{name}" data-panel="panel-{name}">{e(s["tabs"][i])}</button>')
            panels.append(f'''        <section class="tool-panel" id="panel-{name}" aria-labelledby="tool-{name}-heading">
          <div class="tool-copy">
            <p class="tool-index" aria-hidden="true">0{i + 1} / 05</p>
            <h3 id="tool-{name}-heading">{e(feature["title"].capitalize() if code == "en" and feature["title"].isupper() else feature["title"])}</h3>
            <p>{e(feature["body"])}</p>
          </div>
          <figure class="tool-figure">
            <div class="capture tool-capture {name}-capture" dir="ltr">
              {'<div class="capture detail-crop">' if name == 'words' else ''}
              <img src="{prefix}assets/product/{name}-{image_lang}.png" alt="{e(feature["title"])}" width="1220" height="2656" loading="lazy">
              {'</div>' if name == 'words' else ''}
            </div>
            <figcaption>{e(s["ui"][1])}</figcaption>
          </figure>
        </section>''')
        answers = [p["freeAnswer"], p["privacyAnswer"], s["faq"][4]]
        faq_items = "\n".join(f'''        <details class="faq-item">
          <summary>{e(question)}<img class="icon" src="{prefix}assets/icons/plus.svg" alt="" width="22" height="22"></summary>
          <p>{e(answer)}</p>
        </details>''' for question, answer in zip(s["faq"][1:4], answers))
        fields = {
            "locale": code, "direction": direction, "prefix": prefix,
            "native": s["native"], "home_url": "./index.html", "home_label": s["ui"][3],
            "page_title": "SnapMosaic — " + s["hero"][1] + " " + s["hero"][2],
            "description": p["description"], "canonical": BASE + routes[code],
            "social_image": BASE + f"assets/product/feature-{image_lang}.png",
            "play_url": PLAY + "&hl=" + quote(code),
            "nav_features": s["nav"][0], "nav_privacy": s["nav"][1],
            "nav_faq": s["nav"][2], "nav_download": s["nav"][3], "language_label": s["nav"][4],
            "hero_eyebrow": s["hero"][0], "hero_title": s["hero"][1], "hero_accent": s["hero"][2],
            "hero_description": s["hero"][3], "cta": s["hero"][4], "explore": s["hero"][5],
            "proof": s["hero"][6], "hero_caption": s["hero"][7],
            "privacy_eyebrow": s["privacy"][0], "privacy_title": s["privacy"][1],
            "privacy_accent": s["privacy"][2], "privacy_description": s["privacy"][3],
            "privacy_link": s["privacy"][4], "tools_title": s["toolsTitle"],
            "faq_title": s["faq"][0], "closing_title": s["closing"][0],
            "closing_description": s["closing"][1], "skip": s["ui"][0],
            "screenshot_note": s["ui"][1], "support": s["ui"][2], "free_note": s["ui"][4],
            "privacy_label": p["privacyLabel"], "terms_label": p["termsLabel"],
            "image_lang": image_lang, "hero_image_alt": p["smart"]["title"],
            "words_image_alt": s["words"][0]
        }
        fields = {key: e(value) for key, value in fields.items()}
        fields.update(alternates=alternates, language_links="\n".join(language_links),
                      tool_buttons="\n".join(buttons), tool_panels="\n".join(panels),
                      faq_items=faq_items, arrow=arrow)
        rendered = "\n".join(line.rstrip() for line in template.substitute(fields).splitlines()) + "\n"
        output(ROOT / routes[code] / "index.html", rendered)
        # Keep the existing policy text; connect its brand link to its own homepage.
        for name in ("privacy", "terms"):
            path = ROOT / routes[code] / f"{name}.html"
            text = path.read_text()
            text = text.replace('name="color-scheme" content="light"', 'name="color-scheme" content="dark"')
            text = re.sub(r'<p class="brand">.*?</p>',
                          '<p class="brand"><a href="./index.html">SnapMosaic</a></p>', text, count=1)
            output(path, text)

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for route in routes.values():
        for page in ("", "privacy.html", "terms.html"):
            sitemap += f"  <url><loc>{BASE}{route}{page}</loc></url>\n"
    sitemap += "</urlset>\n"
    output(ROOT / "sitemap.xml", sitemap)
    if stale:
        raise SystemExit("Generated files are stale: " + ", ".join(stale))
    print(f'{"Verified" if check else "Generated"} {len(sites)} localized homepages and legal navigation.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if committed output differs from its sources")
    build(parser.parse_args().check)
