# Zoom Out (Cosmic Zoom)

Type your ZIP code (or use your location) and a single continuous camera flight
lifts you off your own street and pulls back — past the horizon, into the blue
marble, out to a pale blue dot, and finally into a real Milky Way starfield where
Earth is gone. A mindfulness quote fades in. Then you can zoom back in.

A tool for perspective: a simulated "overview effect" for when things feel too big,
and its reverse for when you feel too small.

Built on [CesiumJS](https://cesium.com/platform/cesiumjs/) — a real 3D globe you fly
a camera through, not a sequence of flat images. No build step for the app itself.

## Run / host it

It's 100% static files, so any static host works — and hosting fixes the one catch:
opening `index.html` directly (`file://`) blocks the local data files in some
browsers. Serve it instead:

- **Locally:** `python3 -m http.server` in this folder, then open `http://localhost:8000`.
- **Share it (recommended):** drag this folder onto [app.netlify.com/drop](https://app.netlify.com/drop) for an instant HTTPS link. Or push to a repo and enable **GitHub Pages**, or use **Cloudflare Pages**. All give free HTTPS and gzip the ZIP data (~1.1 MB → ~300 KB).

Geolocation ("use my location") requires HTTPS, which all the above provide.

## Files

| File | What it is |
|------|-----------|
| `index.html` | The whole app (markup, styles, JS). CesiumJS loads from a CDN. |
| `zipcodes.js` | Generated: `window.ZIPS = { "94103": [37.77,-122.41], ... }` — 41k US ZIP centroids for offline lookup. |
| `sky/*.jpg` | Milky Way skybox — 6 cube faces (~2.4 MB). |
| `og-image.jpg`, `favicon.png`, `apple-touch-icon.png` | Share card + icons. |
| `build_zipcodes.py` | Regenerates `zipcodes.js` from GeoNames. |
| `build_sky.py` | Downloads the ESO Milky Way panorama and regenerates the cube faces. |
| `build_meta.py` | Regenerates the favicon, touch icon, and share card. |

Regenerate assets anytime with `python3 build_sky.py` / `build_meta.py` (needs `pip install Pillow numpy`).

## Imagery: two tiers

- **Default — free & keyless:** EOX **Sentinel-2 cloudless** (a CC BY 4.0 global cloudless mosaic). Properly licensed for a public app, gorgeous for the pull-back. Softer than sub-meter imagery at street level — which is what the Google tier is for.
- **Google Earth-grade (optional):** paste a billing-enabled Google Maps API key into `GOOGLE_MAPS_KEY` at the top of `index.html` to load Google Photorealistic 3D Tiles (real 3D buildings). Bills per session; 1,000 free sessions/month — effectively free at personal usage. See Google Cloud Console → enable the **Map Tiles API** + billing → create an API key.

## Tuning

Constants near the top of the script:
- `OUT_SECONDS` / `IN_SECONDS` — flight durations (auto-shortened when the OS requests reduced motion).
- `REST_BEAT` — pause of empty space before the quote appears.
- `R_START` / `R_END` — start altitude (town scale) → end distance (deep space, Earth gone).
- `QUOTES_OUT` / `QUOTES_IN` — the quote pools (real quotes, real people).

The ambient pad is synthesized with the Web Audio API (no audio files).

## Credits & licenses

- Milky Way panorama: **ESO / S. Brunier**, CC BY 4.0.
- Satellite imagery: **Sentinel-2 cloudless (2020) © EOX IT Services** — contains modified Copernicus data.
- ZIP centroids: **GeoNames**, CC BY.
- Globe engine: **CesiumJS** (Apache-2.0).

## Notes

- Needs a browser with WebGL; shows a friendly message if unavailable.
- Rendering runs only while the tab is visible (standard `requestAnimationFrame`).
- US ZIP lookup is US-only; "use my location" works anywhere.
