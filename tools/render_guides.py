"""Render the guide library, using current product content and shared navigation."""
import html
import json
from string import Template
from site_chrome import chrome
from guide_components import media_slot, word_demo

e = html.escape
STEP_IDS = ('choose', 'smart', 'refine', 'export')
CHAPTERS = (
    ('index', 'overview', 'gettingStarted'), ('quickstart', 'quickstart', 'gettingStarted'),
    ('smart-detection', 0, 'editing'), ('manual-masking', 1, 'editing'),
    ('decorations', 'decorations', 'editing'), ('batch', 'batch', 'editing'),
    ('export', 2, 'editing'), ('custom-rules', 'rules', 'settingsGroup'),
    ('recognition-help', 'help', 'settingsGroup'), ('pro', 'pro', 'settingsGroup'),
    ('video', 'video', 'labGroup'),
)
GUIDE_PAGES = tuple(slug + '.html' for slug, _, _ in CHAPTERS)


def validate_guides(guides, locales):
    if set(guides) != set(locales):
        raise ValueError('Guide, site, and legal locales must match')
    def filled(value):
        if isinstance(value, str):
            return bool(value.strip())
        if isinstance(value, dict):
            return bool(value) and all(filled(v) for v in value.values())
        return isinstance(value, list) and bool(value) and all(filled(v) for v in value)
    for code, guide in guides.items():
        if set(guide) != set(guides['en']) or len(guide['steps']) != 4 or len(guide['checks']) != 3 or len(guide['articles']) != 3 or not filled(guide):
            raise ValueError(f'Incomplete guide: {code}')


def build_guides(root, base, play, sites, products, guides, routes, output):
    template = Template((root / 'content/guide.html').read_text())
    interface = json.loads((root / 'content/interface.json').read_text())
    chapters = json.loads((root / 'content/chapters.json').read_text())
    media = json.loads((root / 'content/guide-media.json').read_text())
    if set(chapters) != set(guides) or any(set(v) != set(chapters['en']) for v in chapters.values()):
        raise ValueError('Chapter translations must match guide locales and keys')
    for code, guide in guides.items():
        site, product, ui, extra = sites[code], products[code], interface[code], chapters[code]
        prefix = '../' if code == 'en' else '../../'
        image_lang = 'zh' if code == 'zh-CN' else 'en'
        arrow = f'<img class="icon arrow" src="{prefix}assets/icons/arrow-right.svg" alt="" width="20" height="20">'
        titles = {slug: guide['articles'][key]['title'] if isinstance(key, int) else guide[key] if slug in ('index', 'quickstart') else extra[key]['title'] for slug, key, _ in CHAPTERS}

        def shot(name, title):
            src = f'{prefix}assets/guide/2-5-0/{name}-{image_lang}.webp'
            return f'''<figure class="guide-figure"><a class="guide-shot {name}" href="{src}" data-lightbox aria-label="{e(ui['zoom'])}: {e(title)}">
              <img src="{src}" alt="{e(title)}" width="1080" height="2316" loading="lazy"><span class="zoom-indicator" aria-hidden="true">↗</span></a>
              <figcaption>{e(site['ui'][1])} <a href="{src}" data-lightbox>{e(ui['zoom'])} ↗</a></figcaption></figure>'''

        def section(id, title, paragraphs, note='', image='', number=None):
            number_html = f'<span class="step-number" aria-hidden="true">{number:02}</span>' if number else ''
            note_html = f'<aside class="guide-note">{e(note)}</aside>' if note else ''
            return f'''<section class="guide-step" id="{id}" aria-labelledby="{id}-title"><h2 id="{id}-title">{number_html}{e(title)}</h2>
              <div class="step-content {'has-figure' if image else ''}"><div>{''.join(f'<p>{e(text)}</p>' for text in paragraphs)}{note_html}</div>{image}</div></section>'''

        for page_index, (slug, key, group) in enumerate(CHAPTERS):
            page = slug + '.html'
            overview, quickstart = slug == 'index', slug == 'quickstart'
            page_path = '' if overview else page
            title = guide['nav'] if overview else titles[slug]
            lead = guide['lead'] if overview else guide['articleLead'] if quickstart else '' if isinstance(key, int) else extra[key]['lead']
            description = lead or guide['steps'][key + 1]['body']
            page_links, previous_group = [], None
            for target, _, target_group in CHAPTERS:
                if target_group != previous_group:
                    group_title = guide.get(target_group, ui.get(target_group))
                    page_links.append(f'<p class="sidebar-label">{e(group_title)}</p>')
                    previous_group = target_group
                active = ' aria-current="page"' if target == slug else ''
                href = './' if target == 'index' else f'./{target}.html'
                page_links.append(f'<a class="sidebar-page" href="{href}"{active}>{e(titles[target])}</a>')
            toc_entries = []
            if overview:
                path = ''.join(f'<li>{e(step["title"])}</li>' for step in guide['steps'])
                body = f'''<section class="guide-intro"><p class="eyebrow">SnapMosaic · Android</p><h1>{e(title)}</h1><p class="guide-lead">{e(lead)}</p>
                  <a class="button" href="./quickstart.html">{e(guide['start'])} {arrow}</a></section>
                  <ol class="guide-path">{path}</ol>{media_slot(ui, media, 'quickstart', prefix, code)}{word_demo(ui)}'''
            else:
                body = f'''<article><header class="article-header"><p class="eyebrow">{e(guide.get(group, ui.get(group)))}</p><h1>{e(title)}</h1>{f'<p class="guide-lead">{e(lead)}</p>' if lead else ''}</header>'''
                body += media_slot(ui, media, slug, prefix, code)
                if quickstart:
                    body += f'<aside class="guide-before"><h2>{e(guide["before"])}</h2><p>{e(guide["beforeBody"])}</p></aside>'
                    for i, (id, step) in enumerate(zip(STEP_IDS, guide['steps']), 1):
                        picture = shot('words', titles['manual-masking']) if id == 'refine' else shot('export', titles['export']) if id == 'export' else ''
                        body += section(id, step['title'], [step['body']], step['tip'], picture, i)
                        toc_entries.append((id, step['title']))
                    body += f'<section class="guide-check" id="review"><h2>{e(guide["checkTitle"])}</h2><ul>{"".join(f"<li>{e(item)}</li>" for item in guide["checks"])}</ul></section>'
                    toc_entries.append(('review', guide['checkTitle']))
                elif isinstance(key, int):
                    step, topic = guide['steps'][key + 1], guide['articles'][key]
                    if key == 1:
                        body += word_demo(ui)
                    picture = shot('hero', title) if key == 0 else shot('words', title) if key == 1 else shot('export', title)
                    body += section('use', guide['howTo'], [step['body']], step['tip'], picture)
                    body += section('options', topic['detailsTitle'], topic['details'], image=shot('metadata', title + ' · EXIF') if key == 2 else '')
                    if key == 1:
                        body += section('controls', topic['controlsTitle'], topic['controls'])
                    if key == 0:
                        body += f'<aside class="guide-note">{e(extra["help"]["paragraphs"][1])}</aside>'
                        body += f'<a class="text-link" href="./custom-rules.html">{e(extra["rules"]["title"])} {arrow}</a><br><a class="text-link" href="./recognition-help.html">{e(extra["help"]["title"])} {arrow}</a>'
                    toc_entries = [('use', guide['howTo']), ('options', topic['detailsTitle'])]
                    if key == 1:
                        toc_entries.append(('controls', topic['controlsTitle']))
                elif key == 'decorations':
                    body += section('faces', ui['faceTitle'], [extra[key]['paragraphs'][0], site['faces'][1]], image=shot('faces', ui['faceTitle']))
                    body += section('watermark', ui['watermarkTitle'], [extra[key]['paragraphs'][1], product['watermark']['body']], image=shot('watermark', ui['watermarkTitle']))
                    toc_entries = [('faces', ui['faceTitle']), ('watermark', ui['watermarkTitle'])]
                else:
                    picture = shot({'batch':'batch', 'rules':'rules', 'help':'help', 'video':'video'}.get(key), title) if key in ('batch', 'rules', 'help', 'video') else ''
                    body += section('use', guide['howTo'], extra[key]['paragraphs'], image=picture)
                    toc_entries = [('use', guide['howTo'])]
                body += '</article>'
            adjacent = []
            for index, label in ((page_index - 1, ui['previous']), (page_index + 1, ui['next'])):
                if 0 <= index < len(CHAPTERS):
                    target = CHAPTERS[index][0]
                    target_url = './' if target == 'index' else f'./{target}.html'
                    position = 'previous' if index < page_index else 'next'
                    adjacent.append(f'<a class="chapter-{position}" href="{target_url}"><span>{e(label)}</span><strong>{e(titles[target])}</strong>{arrow}</a>')
            body += f'<nav class="chapter-pagination" aria-label="{e(guide["nav"])}">{"".join(adjacent)}</nav>'
            body += f'<aside class="guide-help"><h2>{e(guide["help"])}</h2><a class="text-link" href="../faq.html">{e(site["nav"][2])} {arrow}</a><a class="text-link" href="mailto:snapmosaic.help@outlook.com">{e(site["ui"][2])} {arrow}</a></aside>'
            toc_links = ''.join(f'<a href="#{id}">{e(label)}</a>' for id, label in toc_entries)
            toc = f'<aside class="guide-toc"><nav aria-label="{e(guide["toc"])}"><p>{e(guide["toc"])}</p>{toc_links}</nav></aside>' if toc_entries else ''
            alternates = '\n'.join(f'<link rel="alternate" hreflang="{other}" href="{base}{route}guide/{page_path}">' for other, route in routes.items())
            alternates += f'\n<link rel="alternate" hreflang="x-default" href="{base}guide/{page_path}">'
            fields = {'locale': code, 'direction': 'rtl' if code == 'ur' else 'ltr', 'prefix': prefix,
                      'page_class': 'guide-overview' if overview else 'guide-article', 'page_title': title + ' · SnapMosaic',
                      'description': description, 'canonical': base + routes[code] + 'guide/' + page_path,
                      'social_image': base + f'assets/product/feature-{image_lang}.png', 'nav_guide': guide['nav'],
                      'nav_faq': site['nav'][2], 'support': site['ui'][2], 'current_label': titles[slug]}
            fields = {k: e(v) for k, v in fields.items()}
            fields.update(**chrome(root, code, 'guide/' + page, 'guide'), body=body, toc=toc, arrow=arrow,
                          alternates=alternates, page_links='\n'.join(page_links))
            rendered = '\n'.join(line.rstrip() for line in template.substitute(fields).splitlines()) + '\n'
            output(root / routes[code] / 'guide' / page, rendered)
