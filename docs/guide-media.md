# Guide media

## Current capture set

Captured on 2026-10-04 from the connected OPPO PEEM00 (Android 14), running SnapMosaic 2.5.0, version code 17. The installed package was `com.magic.snapmosaic.smartqa`, a QA build. Editing flows were exercised on that installation; Google Play billing was unavailable and was not exercised. The Pro chapter therefore contains instructions without a purchase recording.

The site uses current English and Simplified Chinese screenshots. The nine silent recordings use the Simplified Chinese app interface and have Simplified Chinese and English WebVTT instructions. Other website languages use the English instructions and retain the visible Chinese-interface label. They are not presented as recordings of a translated interface.

| Media key | Recorded content |
| --- | --- |
| `quickstart` | Edited sequence of Smart, word selection, undo/redo and export preferences. |
| `smart-detection` | Smart suggestions, review, removal of an unwanted mask and manual corrections. |
| `manual-masking` | Long-press a recognized line, keep the middle number segments masked, undo/redo. |
| `decorations` | Enable face stickers, apply Smart, enter and enable a text watermark. |
| `batch` | Edit two photos independently, return to retained edits, inspect current/all export choices. |
| `custom-rules` | Add and save the fictional literal-text rule `Alex`. |
| `export` | PNG selection, output preferences and return to the canvas for review. |
| `recognition-help` | Open recognition help, inspect local resource status, expand a troubleshooting answer. |
| `video` | Preview an already analyzed clip, scrub, save, inspect the share entry. Analysis itself is not accelerated or simulated in the recording. |

The image export and video export were also opened locally after saving. The video export retained the 1280 × 720 dimensions, 10.04-second duration and audio track; a decoded frame confirmed the face mask. Recognition is imperfect; examples and instructions require the user to review and supplement masks.

## Sources and processing

Raw screenshots, UI hierarchies and recordings are retained outside the published repository at `../../website-media-capture/2026-10-04/` relative to this checkout. The recordings were made with scrcpy. The only screenshot processing is removal of the system status bar and WebP compression. Videos use the same status-bar crop, H.264 encoding and a corrected BT.709 color tag; the quick start joins actual recorded segments. No app interface or interaction was generated or redrawn. The export recording ends before the QA advertising result screen; it demonstrates preferences, not completion of a purchase or an ad reward.

All imported content is fictional project material:

- Android `design/product/assets/onboarding-travel-share.jpg` and `onboarding-travel-share-en.jpg`: travel chat examples.
- Android `design/marketing/play-screenshots-v2/assets/travel-group.png` and `project-estimate.png`: generated group photo and fictional estimate.
- Media archive `library/shared-scene-library/2026-09-12/people-and-props/01.mp4`: generated portrait video. Source SHA-256: `9cdef9e955925c2718fca8a63002089062e57a0b19da318516f037903d82e478`. Its provenance is in Android `design/marketing/shared-scene-library/manifest.json`.

No personal gallery media or notifications appear in the published assets. The temporary rule, imported phone samples and exported phone copies were removed after capture. The app was returned to its English empty editor, with touch indicators disabled.

## Website integration

`content/guide-media.json` maps chapter keys to localized instructions, posters, MP4s, caption tracks and time points. English caption variants can share the Chinese recording; `interfaceLanguage` must describe the interface actually shown. Only registered recordings render a player. Keep original captures outside the website and optimized files under `assets/guide/2-5-0/`.

Video uses native controls, `playsinline` and `preload="none"`. Chapter buttons load and seek on demand; play pauses any other recording on the page. A poster and native controls remain usable without JavaScript. Screenshots can be opened at full size. The interactive number example is a separate website illustration.

For local verification run `python3 tools/serve_site.py`; its byte-range support allows video seeking, unlike Python's basic static file server. Then check video controls, every time point, captions, screenshot enlargement and mobile layouts. Changes to referenced assets must be accompanied by a site rebuild and a missing-asset check.
