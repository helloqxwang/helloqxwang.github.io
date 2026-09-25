# Qianxu Wang Academic Website

Astro academic website with local face-aware portrait processing and an EXIF photography wall.

## Preview and build

One-time setup (Node.js 24+, Python 3.9–3.12):

```sh
npm ci
npm run media:setup
```

Run `./preview-site.command` to preview at http://localhost:8080.
`npm run publish:static` builds and refreshes the static files in the repository root.
`npm run build` generates `dist/`, which the GitHub Pages workflow deploys.
No push or deployment is needed for local preview.

## Add or change photos

- Put portrait originals in `headshots/` and photography originals in `Photos/`.
- JPEG, PNG, WebP, AVIF, HEIC, and HEIF are supported; EXIF orientation is respected.
- Preview startup and production builds run media preparation automatically. While the preview is running, adding files or editing YAML also triggers processing and updates the page.
- New files are discovered automatically. Add a YAML entry to set order, descriptions, or overrides.
- `npm run media:prepare` runs processing manually. Unchanged images use a content-hash cache.
- Originals are never modified. Generated WebP files omit source metadata except their sRGB color profile; only the selected camera fields are included in the website manifest.
- ICC images are converted to sRGB. Rec.2020 AVIFs are decoded as complete images through libheif, transformed in linear light with FFmpeg/zscale, and PQ HDR images receive a Mobius tone map before sRGB encoding. This avoids treating HDR or wide-gamut channel values as ordinary sRGB.

### Portraits: config/portraits.yml

The six selected originals replace the previous profile photo. The neural YuNet detector runs locally through OpenCV; it detects faces rather than recognizing identity. A configurable composition rule creates a 4:5 crop including headroom, shoulders, and some setting. This is neural face detection plus geometric framing, not a learned aesthetic-ranking model.

`context` adjusts crop height in face-height units; `face_position` adjusts vertical framing. For multiple faces, the largest is selected by default; `face_index` selects another detection in left-to-right order. A normalized `crop: [x, y, width, height]` overrides detection and must have a 4:5 aspect ratio in pixels. If no face is detected, processing stops with a clear message asking for this override.

Click/tap the portrait to cycle; horizontal swipes and left/right arrow keys also work. The front card is upright with equal borders. The small corner icon reveals the surroundings in place, keeping the headshot scale and position over a frosted backdrop. Large originals can be dragged (or panned with arrow keys); the lower-right image icon fits the whole composition. The upper-right collapse icon, the backdrop, or Escape returns to the headshot. Reduced-motion preferences are respected.

Live Photos need both the still image and its paired video: put `IMG_1741.MOV` alongside `IMG_1741.HEIC` in `headshots/`, or specify another video filename with `live: your-video.MOV` in the portrait's YAML entry. The processor generates muted browser-compatible H.264 MP4s for both the headshot crop and the full composition. Tap the lower-left LIVE badge to play once (tap again to stop), or hold the photograph to play and release to stop. A short tap on the headshot still switches photos. The expanded viewer and its fit-to-frame view also support LIVE playback; dragging pans instead of triggering a hold. Expanding or collapsing during playback resumes at the same point after the transition. Playback returns to the still image when finished. No LIVE badge is shown without an actual video; a HEIC alone does not contain the paired motion resource.

Model source and license: `scripts/models/README.md`, `scripts/models/YUNET-LICENSE`.

### Photography: config/photos.yml

The YAML list controls order, captions, and prominence:

```yaml
- file: DSC06320.JPG
  priority: 1
  caption: exif
  alt: A quiet park with benches beneath green trees
```

- All landscape photographs span two columns, regardless of priority.
- `priority: 0`: portrait photographs span one normal column.
- `priority: 1`: portrait photographs span one and a half columns.
- Currently only `DSC06320.JPG` has priority 1. All other photographs have priority 0.
- All images keep their original aspect ratios. The wall uses responsive packing with aligned top edges, three conventional columns on desktop and two on phones.
- `caption: exif` displays camera, lens, focal length, aperture, shutter, and ISO. Missing fields are not guessed. `DSC06819.JPG` and `DSC06871.JPG` have no recorded lens, focal length, or aperture.
- `caption: none` hides the caption; any other string displays a custom caption.
- Optional `metadata` overrides can set `camera`, `lens`, `focal_length`, `aperture`, `shutter`, and `iso`. Values are presentation strings, for example `shutter: 1/2500 s`.

The generated `src/data/media.json` and `public/portraits/`, `public/photography/` are build outputs. Edit originals and YAML instead of these generated files.

Opening a wall photo grows its four edges directly from the tile into the largest composition that fits the screen and caption. The photo stays centered on its original position where there is room; viewport boundaries redistribute expansion toward the available side. Closing reverses back into that photo's tile. The frosted background and camera details fade in during expansion.

## Other website content

- `src/data/site.ts`: identity, navigation, and social links.
- `src/data/publications.ts`: five publications; `selected: true` marks KITE and SparseDFF.
- `src/pages/index.astro`: biography, research focus, and Misc.
- CV and Resources pages are not included in the published site.
- `src/components/`: portrait stack, publication tabs, photo wall and viewers.

CV and LinkedIn remain hidden; Teaching and Resources are removed from the published site. Publication links without verified destinations are omitted.

## Checks

```sh
node --test tests/photo-layout.test.mjs
.media-venv/bin/python -m unittest discover -s tests -p 'test_*.py'
npm run build
```
