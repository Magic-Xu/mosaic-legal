#!/usr/bin/env python3
"""Render static SnapMosaic legal pages from localized JSON sources."""

from __future__ import annotations

import argparse
from datetime import date
import html
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LEGAL_ROOT = REPO_ROOT
CONTENT_ROOT = REPO_ROOT / "content" / "legal"
LOCALES = (
    "en",
    "zh-CN",
    "zh-Hant",
    "es",
    "pt-BR",
    "hi",
    "ur",
    "fr",
    "ja",
    "ko",
    "id",
    "th",
    "vi",
    "ms",
    "fil",
)
DOCUMENTS = ("privacy", "terms")
EXPECTED_SECTION_COUNTS = {"privacy": 9, "terms": 10}
EXTERNAL_LINKS = {
    "google_privacy": "https://policies.google.com/privacy",
    "admob_disclosure": "https://developers.google.com/admob/android/privacy/play-data-disclosure",
    "firebase_analytics": "https://firebase.google.com/docs/analytics",
    "firebase_crashlytics": "https://firebase.google.com/docs/crashlytics",
    "firebase_disclosure": "https://firebase.google.com/docs/android/play-data-disclosure",
    "mlkit_disclosure": "https://developers.google.com/ml-kit/android-data-disclosure",
    "github_privacy": "https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement",
}


def load_locales() -> dict[str, dict]:
    loaded: dict[str, dict] = {}
    for locale in LOCALES:
        path = CONTENT_ROOT / f"{locale}.json"
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError(f"cannot read {path.relative_to(REPO_ROOT)}: {error}") from error
        if data.get("locale") != locale:
            raise ValueError(f"{path.relative_to(REPO_ROOT)} must declare locale {locale!r}")
        for key in ("name", "direction", "languageLabel", "effectiveDateLabel", *DOCUMENTS):
            if not data.get(key):
                raise ValueError(f"{path.relative_to(REPO_ROOT)} is missing {key!r}")
        if data["direction"] not in {"ltr", "rtl"}:
            raise ValueError(f"{path.relative_to(REPO_ROOT)} has invalid direction")
        for document in DOCUMENTS:
            page = data[document]
            if not page.get("title") or not page.get("intro") or not page.get("sections"):
                raise ValueError(f"{path.relative_to(REPO_ROOT)} has incomplete {document} content")
            if len(page["sections"]) != EXPECTED_SECTION_COUNTS[document]:
                raise ValueError(
                    f"{path.relative_to(REPO_ROOT)} must contain "
                    f"{EXPECTED_SECTION_COUNTS[document]} {document} sections"
                )
            for section in page["sections"]:
                if not section.get("title"):
                    raise ValueError(f"{path.relative_to(REPO_ROOT)} has an untitled section")
                if not any(section.get(key) for key in ("paragraphs", "items", "contact")):
                    raise ValueError(f"{path.relative_to(REPO_ROOT)} has an empty section")
                for link in section.get("links", []):
                    if link["key"] not in EXTERNAL_LINKS:
                        raise ValueError(f"{path.relative_to(REPO_ROOT)} uses unknown link {link['key']!r}")
        loaded[locale] = data
    return loaded


def page_path(locale: str, document: str) -> Path:
    filename = f"{document}.html"
    return LEGAL_ROOT / filename if locale == "en" else LEGAL_ROOT / locale / filename


def relative_href(from_locale: str, to_locale: str, document: str) -> str:
    filename = f"{document}.html"
    if from_locale == "en":
        return f"./{filename}" if to_locale == "en" else f"./{to_locale}/{filename}"
    return f"../{filename}" if to_locale == "en" else f"../{to_locale}/{filename}"


def render_language_menu(
    current_locale: str,
    document: str,
    data: dict,
    all_locales: dict[str, dict],
) -> str:
    links = []
    for locale in LOCALES:
        target = all_locales[locale]
        current = ' aria-current="page"' if locale == current_locale else ""
        links.append(
            f'          <a href="{relative_href(current_locale, locale, document)}" '
            f'lang="{html.escape(locale)}" dir="{target["direction"]}"{current}>'
            f'{html.escape(target["name"])}</a>'
        )
    return (
        '      <details class="language-menu">\n'
        f'        <summary><span>{html.escape(data["languageLabel"])}</span>'
        f'<strong>{html.escape(data["name"])}</strong></summary>\n'
        f'        <nav aria-label="{html.escape(data["languageLabel"])}">\n'
        + "\n".join(links)
        + "\n        </nav>\n      </details>"
    )


def render_section(section: dict, section_number: int) -> str:
    parts = [f'      <section><h2>{section_number}. {html.escape(section["title"])}</h2>']
    for paragraph in section.get("paragraphs", []):
        parts.append(f"        <p>{html.escape(paragraph)}</p>")
    items = section.get("items", [])
    if items:
        parts.append("        <ul>")
        parts.extend(f"          <li>{html.escape(item)}</li>" for item in items)
        parts.append("        </ul>")
    note = section.get("note")
    if note:
        parts.append(f'        <p class="note">{html.escape(note)}</p>')
    for link in section.get("links", []):
        url = EXTERNAL_LINKS[link["key"]]
        parts.append(
            f'        <p class="reference">{html.escape(link["label"])}: '
            f'<a href="{url}" rel="noopener noreferrer">{url}</a></p>'
        )
    if section.get("contact"):
        contact = section["contact"]
        parts.append(
            f'        <p>{html.escape(contact["publisherLabel"])}: '
            'zhangxu.magic<br>\n'
            f'          {html.escape(contact["contactLabel"])}:<br>\n'
            f'          {html.escape(contact["emailLabel"])}: '
            '<a href="mailto:snapmosaic.help@outlook.com">snapmosaic.help@outlook.com</a><br>\n'
            '          <a href="https://github.com/Magic-Xu/mosaic-legal/issues" '
            'rel="noopener noreferrer">https://github.com/Magic-Xu/mosaic-legal/issues</a>\n'
            '        </p>'
        )
    parts.append("      </section>")
    return "\n".join(parts)


def render_page(
    locale: str,
    document: str,
    data: dict,
    all_locales: dict[str, dict],
    effective_date: str,
) -> str:
    page = data[document]
    nested_prefix = "../" if locale != "en" else "./"
    alternates = "\n".join(
        f'  <link rel="alternate" hreflang="{target_locale}" '
        f'href="{relative_href(locale, target_locale, document)}">'
        for target_locale in LOCALES
    )
    sections = "\n\n".join(
        render_section(section, index)
        for index, section in enumerate(page["sections"], start=1)
    )
    return f'''<!DOCTYPE html>
<html lang="{html.escape(locale)}" dir="{data["direction"]}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="color-scheme" content="dark">
  <title>{html.escape(page["title"])}</title>
  <link rel="stylesheet" href="{nested_prefix}assets/legal.css">
{alternates}
</head>
<body>
  <main class="container">
    <header class="page-header">
      <p class="brand"><a href="./index.html">SnapMosaic</a></p>
{render_language_menu(locale, document, data, all_locales)}
      <h1>{html.escape(page["title"])}</h1>
      <p class="meta">{html.escape(data["effectiveDateLabel"])}: <time datetime="{effective_date}">{effective_date}</time></p>
      <p>{html.escape(page["intro"])}</p>
    </header>

{sections}
  </main>
</body>
</html>
'''


def write_or_check(path: Path, content: str, check: bool) -> bool:
    if check:
        try:
            current = path.read_text(encoding="utf-8")
        except OSError:
            print(f"OUTDATED {path.relative_to(REPO_ROOT)}")
            return False
        if current != content:
            print(f"OUTDATED {path.relative_to(REPO_ROOT)}")
            return False
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"WROTE {path.relative_to(REPO_ROOT)}")
    return True


def build(check: bool = False) -> bool:
    try:
        metadata = json.loads((REPO_ROOT / "content/legal.json").read_text(encoding="utf-8"))
        effective_date = metadata["effectiveDate"]
        if date.fromisoformat(effective_date).isoformat() != effective_date:
            raise ValueError("effectiveDate must use YYYY-MM-DD")
        localized = load_locales()
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return False

    valid = True
    for locale in LOCALES:
        for document in DOCUMENTS:
            valid = write_or_check(
                page_path(locale, document),
                render_page(locale, document, localized[locale], localized, effective_date),
                check,
            ) and valid
    return valid


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated pages are stale")
    return 0 if build(parser.parse_args().check) else 1


if __name__ == "__main__":
    raise SystemExit(main())
