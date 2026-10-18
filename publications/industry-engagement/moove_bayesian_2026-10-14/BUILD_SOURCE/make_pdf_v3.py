from PIL import Image
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
src = ROOT / ".build/moove_bayesian_2026-10-14/rendered-slides-v3-2x"
out = Path(__file__).resolve().parents[1] / "BAYESIAN_RELATIVITIES_X_MOOVE_RESEARCH_PARTNERSHIP_DECK_2026-10-14_V3.pdf"
files=sorted(src.glob('slide-*.png'))
images=[Image.open(p).convert('RGB') for p in files]
if len(images)!=19: raise SystemExit(f'Expected 19 slides; found {len(images)}')
images[0].save(out,format='PDF',resolution=192.0,save_all=True,append_images=images[1:])
print(f'Wrote {out} with {len(images)} raster pages, each 2560x1440 rendered slide at 192 dpi')
