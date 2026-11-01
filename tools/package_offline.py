"""Create a self-contained source upload without external runtime downloads."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import shutil
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'dist';out.mkdir(exist_ok=True)
with ZipFile(out/'chatreel-offline.zip','w',ZIP_DEFLATED) as z:
    files=[ROOT/'film-schema.json',ROOT/'ATTRIBUTION.md',ROOT/'LICENSE',ROOT/'README.md',ROOT/'examples/film.json']
    files+=list((ROOT/'renderer-py').glob('*.py'))+list((ROOT/'renderer-py').glob('*.txt'))+list((ROOT/'licenses').glob('*'))
    files+=list((ROOT/'renderer-py/assets').rglob('*.ttf'))
    files+=list((ROOT/'templates').glob('*.json'))+[ROOT/'templates/README.md',ROOT/'gpt/knowledge/EDUCATION.md']
    for p in files:z.write(p,'chatreel/'+str(p.relative_to(ROOT)))
shutil.copy2(out/'chatreel-offline.zip',ROOT/'gpt/chatreel-offline.zip')
print(out/'chatreel-offline.zip')
