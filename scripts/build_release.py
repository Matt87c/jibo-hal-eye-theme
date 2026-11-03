#!/usr/bin/env python3
"""Build reproducible visual-only BEacon ZIP."""
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT=Path(__file__).resolve().parents[1]
FILES=('manifest.json','README.md','banner.png','face/face.json','face/eye.png','face/eyeListening.png','face/eyeClosed.png','atex/happy-glow-01.png','atex/eye_shape_03.png','atex/eye_shape_04.png','atex/eye_shape_05.png','atex/eye_shape_06.png','atex/eye_shape_08.png')
OUT=ROOT/'dist'/'jibo-hal-eye-theme.zip'

def package_bytes():
    return {f:(ROOT/f).read_bytes() for f in FILES}

def main():
    OUT.parent.mkdir(exist_ok=True)
    with ZipFile(OUT,'w') as z:
        for filename,content in sorted(package_bytes().items()):
            item=ZipInfo(filename,date_time=(2026,1,1,0,0,0))
            item.compress_type=ZIP_DEFLATED
            item.create_system=3
            item.external_attr=0o100644<<16
            z.writestr(item,content,compress_type=ZIP_DEFLATED,compresslevel=9)
    print(OUT,OUT.stat().st_size,'bytes')

if __name__=='__main__': main()
