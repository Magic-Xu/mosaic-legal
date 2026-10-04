# SnapMosaic website

The official product website and legal pages for SnapMosaic, an Android photo privacy editor. Published with GitHub Pages from the repository root on `main`.

- [Website](https://magic-xu.github.io/mosaic-legal/)
- [Google Play](https://play.google.com/store/apps/details?id=com.magic.snapmosaic)
- [Privacy policy](https://magic-xu.github.io/mosaic-legal/privacy.html)
- [Terms of service](https://magic-xu.github.io/mosaic-legal/terms.html)
- Support: <snapmosaic.help@outlook.com>

## Product content

The homepage and guide cover smart detection, word selection, masking and highlighting, face stickers, text watermarks, multiple-photo editing, custom masking rules, export preferences, detection help, and experimental video face masking. Editing tools are free. Optional one-time Pro removes the SnapMosaic brand watermark and in-app ads.

Selected photos are edited on the device. No account is required. The privacy policy describes third-party services and data handling in detail.

## Languages and routes

All 15 app languages have a homepage, 11 guide pages, a searchable FAQ, privacy policy, and terms of service. English lives at the root; other languages use their language directory. Existing legal URLs remain valid.

| Language | Route |
| --- | --- |
| English | `/` |
| 简体中文 | `/zh-CN/` |
| 繁體中文 | `/zh-Hant/` |
| Español | `/es/` |
| Português (Brasil) | `/pt-BR/` |
| हिन्दी | `/hi/` |
| اردو | `/ur/` |
| Français | `/fr/` |
| 日本語 | `/ja/` |
| 한국어 | `/ko/` |
| Bahasa Indonesia | `/id/` |
| ไทย | `/th/` |
| Tiếng Việt | `/vi/` |
| Bahasa Melayu | `/ms/` |
| Filipino | `/fil/` |

The Android legacy locale `in` maps to the standard web locale `id`. Urdu pages use right-to-left layout. Language switching preserves the current page and section. The site does not redirect visitors based on their browser language.

The shared top navigation uses page destinations for **Product**, **User guide**, **Privacy**, and **FAQ**, with the current page highlighted. The homepage’s “Explore the tools” link scrolls to its feature section.

The guide keeps its chapter navigation in a sticky left sidebar on desktop and a collapsible menu on mobile. Chapters cover the overview, quick start, smart detection, manual masking, face stickers and watermarks, multiple photos, export, custom rules, detection help, Pro, and experimental video masking. Articles have in-page contents where useful, adjacent chapter links, enlarged screenshots, and a small interactive word-masking example.

Product behavior was checked against Android `main` commit `8b3f3565`, including the product requirements, core behavior contract, editor/settings code, and video capability flag. The video guide describes automatic analysis, preview, saving and sharing; manual video editing is not enabled. Text recognition is unavailable for Thai and Urdu; face and code detection are independent.

English and Simplified Chinese screenshots were refreshed from the connected phone running SnapMosaic 2.5.0 (version code 17) on 2026-10-04. Nine real-device tutorials have seekable steps and Chinese/English caption tracks. The installed QA build could not verify Google Play billing, so Pro has no purchase recording. [Guide media](docs/guide-media.md) records capture provenance, coverage and integration.

## Editing and preview

Requires Python 3; no package installation or frontend build service is needed.

```sh
python3 tools/build_site.py
python3 tools/build_site.py --check
python3 -m unittest discover -s tools/tests
python3 tools/serve_site.py
```

Open <http://127.0.0.1:8798/> or a language route to preview. Commit the generated HTML and sitemap together with their sources. The build and check commands do not commit or push. After review and publication approval, merge the website branch into `main` to publish with GitHub Pages.

- `content/home.html`: shared homepage template.
- `content/site.json` and `content/product.json`: localized homepage, feature descriptions, and common FAQ answers.
- `content/interface.json`: shared navigation, interaction labels, and FAQ questions.
- `content/guide.json`, `content/chapters.json`, and `content/guide.html`: guide copy and page template.
- `content/guide-media.json`: verified recording paths, localized captions, interface language, posters and step times.
- `tools/site_chrome.py`: shared header, language picker, footer, and screenshot dialog.
- `tools/render_guides.py` and `tools/guide_components.py`: guide pages and reusable interaction/media components.
- `tools/render_faq.py`: the localized FAQ, progressively enhanced with search.
- `assets/guide.css` and `assets/guide.js`: guide layout, video chapter seeking, chapter menu, contents indicator, and word-selection example.
- `assets/site.css` and `assets/site.js`: shared appearance, language menu, keyboard-accessible feature tabs, screenshot viewer, and FAQ search. Reading, navigation, and full screenshot links work without JavaScript.
- `tools/build_site.py`: builds/checks 225 static pages and `sitemap.xml`.
- `content/legal/<locale>.json`: privacy-policy and terms text for each app language.
- `content/legal.json`: the shared legal effective date (`effectiveDate`, `YYYY-MM-DD`).
- `tools/render_legal_pages.py` and `assets/legal.css`: legal page generation and reading styles.

Keep the site, product, and legal locales complete. Edit the appropriate JSON source or shared template, then regenerate; the HTML files are build outputs. Legal changes must reflect actual app behavior across all 15 languages. Update the effective date when the policy takes effect.

This repository owns the website and legal sources. The Android repository checks this checkout with `python3 tools/release/validate_store_listing.py --legal-root /path/to/mosaic-legal`; that check is read-only. When reviewing a website feature worktree, pass its path so the App release check validates the candidate pages. Validate published content and dates after GitHub Pages deploys.

## Assets

`assets/guide/2-5-0/` contains the current real-device captures, optimized recordings and caption tracks. Screenshot content is preserved with a system-status-bar crop and WebP compression; CSS crops focus attention on the relevant controls. `assets/product/` retains earlier captures and approved store feature graphics. English captures illustrate the other language homepages, with a localized screenshot-language note. This does not change the app's language support.

The SnapMosaic logo is the supplied Play icon. Inter and Phosphor icons are self-hosted; their licenses are included in `assets/fonts/Inter-LICENSE.txt` and `assets/icons/LICENSE`. Existing legacy asset URLs remain available.

GitHub Pages excludes the source content, generation tools, maintenance docs, README, and design QA report via `_config.yml`. The published pages do not load analytics, third-party fonts, or a client-side framework.
