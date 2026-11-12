# Render queue

`queue.json` lists every plate the catalog expects that isn't in `src/plates` yet (568 at the time of writing).
Regenerate it any time with `python3 tools/render_queue.py`.

| Batch | What | Plates | Unlocks in the app |
|---|---|---|---|
| 1 | Haze (H1) for every S4 Doorway combination, plus the one missing Portrait B plate (S1b · Fluorescent · 40mm · Haze) | 78 | S4 Haze; S1b Fluorescent + 40mm + Haze |
| 2 | New lighting setups L12 Golden hour, L13 Overcast, L14 Hard noon sun and L15 Butterfly/Paramount for S1, S1b, S2, S3 and S4 (all optics, clean air and haze) | 280 | The four "soon" lighting buttons |
| 3 | New scene S5 Daylight exterior: all 15 lighting setups × 7 optics × 2 atmospheres | 210 | The "S5 Daylight soon" scene |

## Plate format (match the existing 692)
- 1536 × 768 px (2:1), WebP. Every aspect ratio in the app is a crop of this frame.
- Encoded with the **ARRI LogC3 (EI 800)** curve on **Rec.709 primaries**. The app decodes LogC3 to linear before all post effects and LUTs.
- Named `<scene>_<L>_<O>_<H>.webp` in `src/plates/<scene>/`.

## Steps
1. In Blender, fill in the four `set_*` hooks at the top of `render/render_plates.py` to match how the existing plates were set up. Then run batch 1:
   `blender -b <scene>.blend -P render/render_plates.py -- --batch 1`
   The script skips plates that are already rendered, so you can stop and resume it.
2. `python3 tools/encode_plates.py render/out` converts the EXRs to LogC3 WebP plates and updates `src/plates/index.json`.
3. For batches 2 and 3, also remove `soon:true` (lighting) or set `ready:true` and remove `soon` (S5) in `src/catalog.js`, and update the `roadmap` list.
4. Commit and push. The web app and the APK rebuild automatically, and the new buttons switch on by themselves once their plates exist.

Lighting recipes for the new setups are in `src/catalog.js` (`L12`–`L15`). S5's subject and prompt text are there too.
