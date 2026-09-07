# SnapMosaic website

The official product website and legal pages for SnapMosaic, an Android photo privacy editor. Published with GitHub Pages from the repository root on `main`.

- [Website](https://magic-xu.github.io/mosaic-legal/)
- [Google Play](https://play.google.com/store/apps/details?id=com.magic.snapmosaic)
- [Privacy policy](https://magic-xu.github.io/mosaic-legal/privacy.html)
- [Terms of service](https://magic-xu.github.io/mosaic-legal/terms.html)
- Support: <snapmosaic.help@outlook.com>

## Product content

The homepage presents SnapMosaic 2.0 photo and screenshot editing: smart detection, precise word selection, face emoji stickers, masking styles, user text watermarks, and export controls. Editing tools are free. Optional one-time Pro removes the SnapMosaic brand watermark and in-app ads.

Selected photos are edited on the device. No account is required. The privacy policy describes third-party services and data handling in detail.

## Languages and routes

All 15 app languages have a homepage, privacy policy, and terms of service. English lives at the root; other languages use their language directory. Existing legal URLs remain valid.

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

The Android legacy locale `in` maps to the standard web locale `id`. Urdu pages use right-to-left layout. Language switching preserves the current homepage section. The site does not redirect visitors based on their browser language.

## Editing and preview

Requires Python 3; no package installation or frontend build service is needed.

```sh
python3 tools/build_site.py
python3 tools/build_site.py --check
python3 -m http.server 8797 --bind 127.0.0.1
```

Open <http://127.0.0.1:8797/> or a language route to preview. Commit the generated HTML and sitemap together with their sources.

- `content/home.html`: shared homepage template.
- `content/site.json`: localized navigation, hero, feature copy, and FAQ labels.
- `content/product.json`: product descriptions and explanations adapted from the approved 2.0.0 store material.
- `assets/site.css` and `assets/site.js`: responsive styling and progressive enhancement for the language menu and keyboard-accessible feature tabs.
- `tools/build_site.py`: generates 15 static homepages and `sitemap.xml`; maintains the existing legal-page home links and theme metadata.
- `assets/legal.css`: shared legal-page appearance. Legal text remains in each language's HTML file and is not generated from homepage copy.

Keep locale keys complete in both JSON files. Update the shared template and regenerate instead of editing generated homepages by hand. Review legal translations and effective dates separately when legal content changes.

## Assets

`assets/product/` contains authentic English and Simplified Chinese app captures and approved store feature graphics. Screenshot pixels are preserved; CSS crops focus attention on the relevant controls. English captures illustrate the other language homepages, with a localized screenshot-language note. This does not change the app's language support.

The SnapMosaic logo is the supplied Play icon. Inter and Phosphor icons are self-hosted; their licenses are included in `assets/fonts/Inter-LICENSE.txt` and `assets/icons/LICENSE`. Existing legacy asset URLs remain available.

GitHub Pages excludes the source content, generation tools, README, and design QA report via `_config.yml`. The published pages do not load analytics, third-party fonts, or a client-side framework.
