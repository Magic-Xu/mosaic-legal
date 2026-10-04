"""Shared public navigation, language switching, and footer."""
import html
import json
from urllib.parse import quote

e = html.escape
PLAY = "https://play.google.com/store/apps/details?id=com.magic.snapmosaic"


def chrome(root, code, page, current):
    sites = json.loads((root / 'content/site.json').read_text())
    guides = json.loads((root / 'content/guide.json').read_text())
    products = json.loads((root / 'content/product.json').read_text())
    labels = json.loads((root / 'content/interface.json').read_text())
    if set(labels) != set(sites) or any(set(v) != set(labels['en']) for v in labels.values()):
        raise ValueError('Interface translations must match site locales and keys')
    site, guide, product, ui = sites[code], guides[code], products[code], labels[code]
    up = '../' * page.count('/') or './'
    prefix = ('../' if code != 'en' else '') + ('../' * page.count('/')) or './'
    links = []
    for key, target, label in [('product', 'index.html', ui['product']), ('guide', 'guide/index.html', guide['nav']),
                              ('privacy', 'privacy.html', site['nav'][1]), ('faq', 'faq.html', site['nav'][2])]:
        active = ' aria-current="page"' if current == key else ''
        links.append(f'<a href="{up}{target}"{active}>{e(label)}</a>')
    languages = []
    for other, other_site in sites.items():
        route = '' if other == 'en' else other + '/'
        active = ' aria-current="page"' if other == code else ''
        languages.append(f'<a href="{prefix}{route}{page}" lang="{other}" dir="{"rtl" if other == "ur" else "ltr"}"{active}>{e(other_site["native"])}</a>')
    header = f'''<a class="skip-link" href="#main">{e(site['ui'][0])}</a>
  <header class="site-header">
    <a class="brand" href="{up}index.html" aria-label="SnapMosaic · {e(site['ui'][3])}">
      <img src="{prefix}assets/snapmosaic-play-icon-512.png" alt="" width="40" height="40"><span>SnapMosaic</span>
    </a>
    <nav class="primary-nav" aria-label="{e(ui['navLabel'])}">{''.join(links)}</nav>
    <div class="header-actions">
      <details class="language-picker">
        <summary aria-label="{e(site['nav'][4])}: {e(site['native'])}"><span class="language-native">{e(site['native'])}</span><span class="language-short">{e(site['nav'][4])}</span><img class="icon" src="{prefix}assets/icons/caret-down.svg" alt="" width="16" height="16"></summary>
        <nav class="language-options" aria-label="{e(site['nav'][4])}">{''.join(languages)}</nav>
      </details>
      <a class="button button-small header-download" href="{PLAY}&amp;hl={quote(code)}">{e(site['nav'][3])}</a>
    </div>
  </header>'''
    footer = f'''<footer class="site-footer wrap">
    <span class="footer-brand">© 2026 SnapMosaic</span>
    <nav aria-label="{e(ui['footerLabel'])}">
      <a href="{up}index.html">{e(ui['product'])}</a><a href="{up}guide/index.html">{e(guide['nav'])}</a>
      <a href="{up}faq.html">{e(site['nav'][2])}</a><a href="{up}privacy.html">{e(product['privacyLabel'])}</a>
      <a href="{up}terms.html">{e(product['termsLabel'])}</a><a href="mailto:snapmosaic.help@outlook.com">{e(site['ui'][2])}</a>
      <a href="https://x.com/snapmosaic_app" rel="noopener noreferrer">X / Twitter</a>
    </nav>
  </footer>
  <dialog class="image-dialog" aria-label="{e(ui['zoom'])}">
    <form method="dialog"><button class="dialog-close" aria-label="{e(ui['close'])}">×</button></form>
    <img alt=""><p class="image-dialog-caption"></p>
  </dialog>'''
    return {'header': header, 'footer': footer}
