#!/usr/bin/env python3
"""Generate original HAL-red animation textures (not stock Jibo artwork).

Only selected known jibo-anim-db-animations filenames are overridden. This
script runs on a development computer, not on Jibo. Original 1.0.0 eye images
stay byte-for-byte unchanged. See docs/ANIMATION_COVERAGE.md for limitations.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import math

ROOT = Path(__file__).resolve().parents[1]
DST = ROOT / 'atex'
DST.mkdir(parents=True, exist_ok=True)
S = 720
base = Image.open(ROOT/'face/eye.png').convert('RGBA').resize((S,S), Image.Resampling.LANCZOS)


def bright_curve(start, end, y_fn, thick, red, halo):
    """Transparent red light band; deliberately no white/glow stock pixels."""
    thick = int(thick)
    shape = Image.new('RGBA',(S,S),(0,0,0,0))
    pen=ImageDraw.Draw(shape)
    coords=[(x,int(y_fn(x))) for x in range(start,end+1,3)]
    gl=Image.new('RGBA',(S,S),(0,0,0,0))
    ImageDraw.Draw(gl).line(coords, fill=red[:3]+(halo,), width=thick+22, joint='curve')
    gl=gl.filter(ImageFilter.GaussianBlur(18))
    shape.alpha_composite(gl)
    pen=ImageDraw.Draw(shape)
    pen.line(coords, fill=red, width=thick, joint='curve')
    return shape


def expression(name, style):
    # Keep some recognizable glass detail underneath the native expression.
    dark=ImageEnhance.Brightness(base).enhance(0.58 if style!='intense' else 0.9)
    mask=Image.new('L',(S,S),0)
    m=ImageDraw.Draw(mask)
    if style=='smile':
        # Crimson smiling lens, echoing Jibo's excited half-moon without white.
        def shape(x):
            u=(x-360)/266
            return 300 + 155*(1-u*u)
        m.line([(x,int(shape(x))) for x in range(100,621,3)],fill=255,width=137,joint='curve')
        band=bright_curve(132,589,lambda x: shape(x)-36,8,(255,28,23,210),130)
    elif style=='squint':
        m.ellipse((68,248,652,468), fill=255)
        band=bright_curve(155,565,lambda x: 282+17*math.cos((x-360)/205*math.pi/2),7,(247,18,20,195),105)
    elif style=='arched':
        def shape(x):
            u=(x-360)/280
            return 432 - 145*(1-u*u)
        m.line([(x,int(shape(x))) for x in range(92,629,3)],fill=255,width=122,joint='curve')
        band=bright_curve(131,589,lambda x: shape(x)-22,7,(255,32,28,190),100)
    elif style=='slit':
        m.ellipse((78,324,642,412),fill=255)
        band=bright_curve(140,580,lambda x: 369+4*math.sin((x-140)/440*math.pi),8,(255,30,20,220),135)
    elif style=='intense':
        m.ellipse((48,48,672,672),fill=255)
        band=Image.new('RGBA',(S,S),(0,0,0,0))
        drawer=ImageDraw.Draw(band)
        drawer.arc((109,109,611,611),204,333,fill=(255,20,20,220),width=11)
        drawer.arc((109,109,611,611),24,156,fill=(255,18,14,150),width=8)
    else: raise ValueError(style)
    mask=mask.filter(ImageFilter.GaussianBlur(5))
    dark.putalpha(ImageChopsMultiply(dark.getchannel('A'),mask))
    dark.alpha_composite(band)
    dark.save(DST/name,optimize=True)
    return dark


def ImageChopsMultiply(a,b):
    from PIL import ImageChops
    return ImageChops.multiply(a,b)

# The happy expression's secondary eye overlay was WHITE in the stock animation.
# Recoloring a matching overlay path is the minimal fix for the reported symptom.
overlay=Image.new('RGBA',(S,S),(0,0,0,0))
glow=Image.new('RGBA',(S,S),(0,0,0,0))
dg=ImageDraw.Draw(glow)
dg.arc((74,92,646,638),194,347,fill=(222,0,12,185),width=45)
dg.arc((122,119,598,594),196,337,fill=(244,0,15,120),width=19)
glow=glow.filter(ImageFilter.GaussianBlur(21))
overlay.alpha_composite(glow)
d=ImageDraw.Draw(overlay)
d.arc((113,115,606,615),201,338,fill=(245,22,18,148),width=8)
d.arc((127,135,592,580),202,337,fill=(255,41,25,86),width=4)
overlay.save(DST/'happy-glow-01.png',optimize=True)

styles={
    'eye_shape_03.png':'smile',
    'eye_shape_04.png':'squint',
    'eye_shape_05.png':'arched',
    'eye_shape_06.png':'slit',
    'eye_shape_08.png':'intense',
}
images={'Happy overlay':overlay}
for filename,style in styles.items():
    images[filename.replace('eye_shape_','Shape ')]=expression(filename,style)

# Optional visual reference for on-device comparison. Not installed into Jibo.
thumbs=Image.new('RGB',(3*420,2*490),'#070707')
from PIL import ImageFont
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20)
for idx,(label,picture) in enumerate(images.items()):
    x=(idx%3)*420;y=(idx//3)*490
    pr=picture.resize((400,400),Image.Resampling.LANCZOS)
    thumbs.paste(pr,(x+10,y+5),pr)
    ImageDraw.Draw(thumbs).text((x+20,y+422),label,fill='#f2dcdc',font=f)
(ROOT/'preview/hal_expression_coverage.png').parent.mkdir(exist_ok=True)
thumbs.save(ROOT/'preview/hal_expression_coverage.png',optimize=True)
print('Generated HAL-red native animation overrides: '+', '.join(sorted(x.name for x in DST.glob('*.png'))))
