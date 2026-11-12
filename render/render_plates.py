"""Lukuluku render driver: run inside Blender (Scripting tab -> Run, or blender -b file.blend -P render/render_plates.py -- --batch 1).
Renders queued plates as scene-linear EXRs into render/out/, then encode them on any machine with:
    python3 tools/encode_plates.py render/out
The four set_* hooks below are the only part tied to how your .blend files are built. Fill them in to
match the setup that produced the existing 692 plates (collection names, light rigs, camera/lens objects)."""
import bpy, json, os, sys
HERE=os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else bpy.path.abspath('//')
QUEUE=json.load(open(os.path.join(HERE,'queue.json')))
OUT=os.path.join(HERE,'out'); os.makedirs(OUT,exist_ok=True)
BATCHES={ # see RENDER_QUEUE.md
 1: lambda q: (q['scene']=='S4' and q['H']=='H1' and q['L'] not in NEW_L) or q['key']=='S1b_L9_O1_H1',
 2: lambda q: q['L'] in NEW_L and q['scene']!='S5',
 3: lambda q: q['scene']=='S5'}
NEW_L={'L12','L13','L14','L15'}

# ---------------------------------------------------------------- hooks: adapt to your scene files
def set_scene(scene_id):
    """Switch to the set + cast for S1, S1b, S2, S3, S4, S5 (e.g. a View Layer, a Scene, or collection visibility)."""
    raise NotImplementedError('set_scene: show the collections for '+scene_id)
def set_lighting(L):
    """Enable only the light rig for L1..L15. New rigs to build: L12 golden hour, L13 overcast, L14 hard noon sun, L15 butterfly."""
    raise NotImplementedError('set_lighting '+L)
def set_optics(O):
    """Camera + lens for O1..O7: focal length, f-stop/DOF distance, camera distance, anamorphic squeeze / bokeh for O4, 6-blade iris for O7."""
    raise NotImplementedError('set_optics '+O)
def set_atmosphere(H):
    """H0 clean air, H1 volumetric haze (world volume or a haze cube)."""
    raise NotImplementedError('set_atmosphere '+H)
# ----------------------------------------------------------------

def setup_output():
    r=bpy.context.scene.render
    r.resolution_x, r.resolution_y, r.resolution_percentage = 1536, 768, 100
    r.image_settings.file_format='OPEN_EXR'; r.image_settings.color_depth='16'; r.image_settings.exr_codec='DWAA'
    bpy.context.scene.view_settings.view_transform='Standard'   # EXR stays scene-linear; the encoder applies LogC3
def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    batch=int(argv[argv.index('--batch')+1]) if '--batch' in argv else 1
    jobs=[q for q in QUEUE if BATCHES[batch](q) and not os.path.exists(os.path.join(OUT,q['key']+'.exr'))]
    print(f'Lukuluku batch {batch}: {len(jobs)} plates to render'); setup_output(); last={}
    for i,q in enumerate(jobs):
        for k,fn in (('scene',set_scene),('L',set_lighting),('O',set_optics),('H',set_atmosphere)):
            if last.get(k)!=q[k]: fn(q[k]); last[k]=q[k]
        bpy.context.scene.render.filepath=os.path.join(OUT,q['key']+'.exr')
        bpy.ops.render.render(write_still=True); print(f'[{i+1}/{len(jobs)}] {q["key"]}')
main()
