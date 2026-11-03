#!/usr/bin/env python3
"""Regenerate approved HAL face textures from repository's original concept image.
Requires Pillow==11.3.0. Generated files are deterministic with the pinned version.
This script never runs on Jibo; only its PNG outputs are packaged.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'assets/hal_eye_concept.png'
assert SOURCE.exists(), f'Missing source art: {SOURCE}'
img=Image.open(SOURCE).convert('RGB')
assert img.size==(1448,1086),'Unexpected source dimensions'
S=1024
SIZE=898
R=207
centers={'idle':(400,305),'listening':(1005,305),'speaking':(401,750),'closed':(1006,751)}
mask=Image.new('L',(S,S),0)
d=ImageDraw.Draw(mask)
rad=SIZE//2
c=S//2
d.ellipse((c-rad+10,c-rad+10,c+rad-10,c+rad-10),fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(9))
for state,(x,y) in centers.items():
    crop=img.crop((x-R,y-R,x+R,y+R)).resize((SIZE,SIZE),Image.Resampling.LANCZOS)
    out=Image.new('RGBA',(S,S),(0,0,0,0))
    out.paste(crop,((S-SIZE)//2,(S-SIZE)//2))
    out.putalpha(mask)
    path={'idle':'face/eye.png','listening':'face/eyeListening.png','closed':'face/eyeClosed.png','speaking':'preview/states/speaking.png'}[state]
    dst=ROOT/path;dst.parent.mkdir(parents=True,exist_ok=True)
    out.save(dst,optimize=True)
    if state!='speaking':
        preview=ROOT/'preview/states'/f'{state}.png'
        out.save(preview,optimize=True)

fonts=['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf']
font_file=next((p for p in fonts if Path(p).exists()),None)
font=lambda size: ImageFont.truetype(font_file,size) if font_file else ImageFont.load_default()
banner=Image.new('RGB',(1280,720),(0,0,0))
eye=Image.open(ROOT/'face/eye.png').resize((630,630),Image.Resampling.LANCZOS)
banner.paste(eye,(30,44),eye)
db=ImageDraw.Draw(banner)
db.text((697,206),'HAL',font=font(74),fill=(245,245,245))
db.text((697,307),'RED EYE',font=font(44),fill=(234,61,52))
db.text((701,391),'JIBO THEME',font=font(24),fill=(174,174,174))
db.text((701,440),'by Matt87c',font=font(24),fill=(135,135,135))
banner.save(ROOT/'banner.png',optimize=True)
print('Regenerated supported HAL assets and concept-only speaking art.')
