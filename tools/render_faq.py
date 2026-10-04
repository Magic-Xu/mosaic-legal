"""Render the searchable FAQ from shared product and guide answers."""
import html
from site_chrome import chrome

e = html.escape


def build_faq(root, base, sites, products, guides, interface, routes, output):
    for code, site in sites.items():
        ui, product, guide = interface[code], products[code], guides[code]
        prefix = './' if code == 'en' else '../'
        entries = [*zip(site['faq'][1:4], [product['freeAnswer'], product['privacyAnswer'], site['faq'][4]]),
                   (ui['faqQuestions'][0], guide['steps'][1]['tip']),
                   (ui['faqQuestions'][1], guide['steps'][2]['body']),
                   (ui['faqQuestions'][2], guide['steps'][3]['tip'])]
        items = '\n'.join(f'''<details class="faq-item" id="question-{i}">
          <summary>{e(question)}<img class="icon" src="{prefix}assets/icons/plus.svg" alt="" width="20" height="20"></summary>
          <p>{e(answer)}</p></details>''' for i, (question, answer) in enumerate(entries, 1))
        shared = chrome(root, code, 'faq.html', 'faq')
        alternates = '\n'.join(f'<link rel="alternate" hreflang="{other}" href="{base}{route}faq.html">' for other, route in routes.items())
        output(root / routes[code] / 'faq.html', f'''<!DOCTYPE html>
<html lang="{code}" dir="{'rtl' if code == 'ur' else 'ltr'}">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark"><meta name="theme-color" content="#0b0a10">
  <title>{e(site['nav'][2])} · SnapMosaic</title><meta name="description" content="{e(ui['faqLead'])}">
  <link rel="canonical" href="{base}{routes[code]}faq.html">{alternates}
  <link rel="alternate" hreflang="x-default" href="{base}faq.html">
  <link rel="icon" href="{prefix}assets/snapmosaic-play-icon-512.png">
  <link rel="stylesheet" href="{prefix}assets/site.css?v=7"><script src="{prefix}assets/site.js?v=5" defer></script>
</head>
<body class="faq-page">
{shared['header']}
<main id="main" class="faq-layout wrap">
  <header class="reading-header"><p class="eyebrow">SnapMosaic</p><h1>{e(site['nav'][2])}</h1><p>{e(ui['faqLead'])}</p>
    <a class="text-link" href="./guide/">{e(ui['guideLink'])} →</a></header>
  <section class="faq-content" aria-label="{e(site['nav'][2])}">
    <div class="faq-search" hidden><label for="faq-search">{e(ui['search'])}</label><input id="faq-search" type="search" autocomplete="off" placeholder="{e(ui['search'])}"></div>
    <div class="faq-list">{items}</div><p class="faq-empty" role="status" hidden>{e(ui['empty'])}</p>
    <aside class="support-line"><h2>{e(guide['help'])}</h2><a class="text-link" href="mailto:snapmosaic.help@outlook.com">{e(site['ui'][2])} →</a></aside>
  </section>
</main>
{shared['footer']}
</body>
</html>
''')
