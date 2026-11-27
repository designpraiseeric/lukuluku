# Lukuluku: film look lab

See how lighting, lenses, atmosphere, glass, filtration, colour science and film medium land on real faces, with deep skin tones front and centre, before you shoot or prompt anything. By DesignPraise Studio.

- **Web app (installable, works offline):** https://designpraiseeric.github.io/lukuluku/
  - Android (Chrome): menu → *Install app*. iPhone/iPad (Safari): Share → *Add to Home Screen*.
- **Android APK:** see [Releases](../../releases). Download the latest `.apk` on the phone and open it. Every plate is built in, so it works fully offline.

## What it does
- **In camera** (lighting × optics × atmosphere): rendered in Blender as one plate per combination, five scenes so far.
- **Post** (lens character, diffusion, 17 colour-science LUTs, 11 film/video media, 11 aspect ratios): simulated live in WebGL 2.
- **Grade:** exposure, highlights, shadows, whites, blacks, white balance and more; primary and log colour wheels; curves and hue curves; look-strength controls; undo/redo; waveform and vectorscope; before/after; pinned comparisons.
- **Your frame:** grade a still of your own (normal photo or a LogC3 grab). It stays on the device.
- **Out:** `.cube` LUT export (LogC3 / Rec.709 in), PNG export, a share link that opens the exact look, and prompts for Midjourney, Veo, Runway or Kling with a shot composer.

Every look has a code such as `L1·O1·H0·K0·D0·C0·M0·2.39`.

## Coming next
The options shown as **soon** (dashed) are waiting on renders. See [`render/RENDER_QUEUE.md`](render/RENDER_QUEUE.md): S4 haze, four new lighting setups (Butterfly, Golden hour, Overcast, Noon sun) and the S5 daylight exterior scene.

## Layout
- `src/index.html`: the app (one file). `src/catalog.js`: every axis, recipe, reference and the roadmap.
- `src/plates/<scene>/*.webp`: LogC3-encoded plates. `src/plates/index.json` is generated and tells the app which plates exist.
- `src/luts/*.bin`: 33³ colour-science LUTs (uint16), with sizes in `luts.json`.
- `tools/build.py`: builds `www/` (manifest, icons, service worker). `tools/icons.py`: app icons. `tools/encode_plates.py`: EXR renders → plates. `tools/render_queue.py`: lists missing plates.
- `render/`: Blender render driver and queue.
- `.github/workflows/`: deploys `www/` to GitHub Pages and builds the Android APK on every push to `main`.

Local: `python3 tools/build.py && npm run serve`, then open http://localhost:8080.

Credits: cast scans (CC BY 4.0) by deep3dstudio and yaro.pro via Sketchfab; set props and textures from Poly Haven (CC0).

## License

Code is MIT licensed (see [LICENSE](LICENSE)). Third-party assets keep their own licenses: cast scans are CC BY 4.0 (credits above), Poly Haven props and textures are CC0.
