"""Small interactive and media components used in the guides."""
import html

e = html.escape


def word_demo(ui):
    tokens = ''.join(f'<button type="button" class="demo-token" aria-pressed="{str(i == 1).lower()}" aria-label="{token}"><span>{token}</span></button>' for i, token in enumerate(('138', '0000', '2731')))
    return f'''<section class="word-demo" aria-label="{e(ui['demoLabel'])}">
      <div class="demo-copy"><p class="eyebrow">{e(ui['demoLabel'])}</p><h2>{e(ui['demoTitle'])}</h2><p>{e(ui['demoLead'])}</p></div>
      <div class="demo-workspace"><div class="demo-number" dir="ltr">{tokens}</div>
        <div class="demo-controls"><p role="status">{e(ui['demoStatus'])} <output dir="ltr">1 / 3</output></p><button class="demo-reset" type="button">{e(ui['demoReset'])} ↺</button></div>
      </div>
    </section>'''


def media_slot(ui, media, key, prefix, locale):
    variants = media.get(key, {}).get('locales', {})
    source = variants.get(locale) or variants.get('en') or variants.get('zh-CN')
    if not source:
        return ''
    media_locale = locale if locale in variants else 'en' if 'en' in variants else 'zh-CN'
    language = '简体中文' if source.get('interfaceLanguage', media_locale) == 'zh-CN' else 'English'
    subtitle_language = '简体中文' if media_locale == 'zh-CN' else 'English'
    caption = f'{ui["mediaTitle"]} · {language} · SnapMosaic {media["version"]}'
    if not source.get('video'):
        return f'''<figure class="guide-media-still"><a href="{prefix}{e(source['poster'])}" data-lightbox aria-label="{e(ui['zoom'])}"><img src="{prefix}{e(source['poster'])}" alt="{e(caption)}" width="1080" height="2316" loading="lazy"></a><figcaption>{e(caption)}</figcaption></figure>'''
    steps = ''.join(f'''<li><button type="button" disabled data-video-time="{item['time']}"><time>{int(item['time']) // 60}:{int(item['time']) % 60:02}</time><span lang="{media_locale}">{e(item['label'])}</span><span aria-hidden="true">↗</span></button></li>''' for item in source['steps'])
    return f'''<figure class="guide-recording" data-media-slot="{key}">
      <div class="recording-player"><video controls preload="none" playsinline poster="{prefix}{e(source['poster'])}" aria-label="{e(caption)}" width="1080" height="2316"><source src="{prefix}{e(source['video'])}" type="video/mp4"><track kind="captions" src="{prefix}{e(source['captions'])}" srclang="{media_locale}" label="{subtitle_language}" default></video><button class="recording-play" type="button" aria-label="{e(ui['mediaPlay'])}" hidden><svg viewBox="0 0 24 24" width="23" height="23" aria-hidden="true"><path d="M8 5v14l11-7z" fill="currentColor"/></svg></button></div>
      <figcaption><p class="eyebrow">{e(ui['mediaTitle'])}</p><p class="recording-meta">{language} · SnapMosaic {media['version']}</p><ol class="recording-steps">{steps}</ol><p class="recording-hint">{e(ui['mediaHint'])}</p></figcaption>
    </figure>'''
