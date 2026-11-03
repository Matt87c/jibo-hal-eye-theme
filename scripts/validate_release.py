#!/usr/bin/env python3
"""Strict static package audit; physical acceptance is separate."""
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
import json,hashlib,re,sys
from PIL import Image,ImageChops
from build_release import ROOT,OUT,FILES,package_bytes

def test_payload(files):
    assert set(files)==set(FILES), 'the 7 base assets and 6 animation overrides are required'
    mani=json.loads(files['manifest.json'])
    face=json.loads(files['face/face.json'])
    assert mani=={'name':'HAL Red Eye','version':'1.0.1','supported':'3.1.8','type':'theme'}
    assert face=={'backgroundColor':'#000000','eyeSize':125}
    assert sum(map(len,files.values()))<64*1024*1024
    assert 'Matt87c' in files['README.md'].decode('utf-8')
    imgs={}
    for path in ['banner.png','face/eye.png','face/eyeListening.png','face/eyeClosed.png'] + sorted(f for f in FILES if f.startswith('atex/')):
        b=files[path]
        with Image.open(BytesIO(b)) as im:
            im.verify()
        with Image.open(BytesIO(b)) as im:
            im.load()
            assert im.format=='PNG'
            assert im.mode in ('RGB','RGBA')
            assert 0<im.width<=4096 and 0<im.height<=4096
            assert not im.info, 'no metadata allowed in art'
            if path.startswith('face/'):
                assert im.size==(1024,1024) and im.mode=='RGBA'
            if path.startswith('atex/'):
                assert im.size==(720,720) and im.mode=='RGBA', path
                assert im.getpixel((0,0))[3]==0, 'animation effects must not be square backgrounds'
                assert im.getchannel('A').getbbox(), 'empty animation override is not acceptable'
            imgs[path]=im.copy().convert('RGBA')
    assert len(files['banner.png'])<=2*1024*1024
    a=imgs['face/eye.png']; b=imgs['face/eyeListening.png']; c=imgs['face/eyeClosed.png']
    assert a.getchannel('A').tobytes()==b.getchannel('A').tobytes()==c.getchannel('A').tobytes(), 'native textures need consistent geometry'
    for other in (b,c):
        assert ImageChops.difference(a.convert('RGB'),other.convert('RGB')).getbbox(),'state images not distinct'
    mid=a.width//2
    assert a.convert('RGB').getpixel((mid,mid))!=b.convert('RGB').getpixel((mid,mid)),'listening center not different'
    assert a.getpixel((0,0))[3]==0,'outside theme must be transparent'
    effect=imgs['atex/happy-glow-01.png']
    # Reject white/yellow/cyan excited-eye overlays. Visible glow must be red.
    red=0; not_red=0
    for r,g,b,alpha in effect.getdata():  # pinned Pillow 11.3.0
        if alpha>=30:
            if r>1.75*g and r>1.5*b: red+=1
            else: not_red+=1
    assert red>=500 and not_red<=red//100, ('happy eye overlay is not consistently red', red, not_red)
    for name in FILES:
        if name.startswith('atex/'):
            assert '/' not in name[5:], 'only confirmed top-level stock filenames permitted'
            assert name.lower()==name, 'exact stock filename casing'
    return mani

def main():
    expected=package_bytes()
    test_payload(expected)
    assert OUT.is_file() and OUT.stat().st_size<=32*1024*1024
    with ZipFile(OUT) as z:
        assert z.testzip() is None, 'corrupt ZIP'
        names=z.namelist()
        assert len(names)==len(set(names)) and set(names)==set(FILES), 'unexpected files'
        for item in z.infolist():
            assert item.filename in FILES and '..' not in item.filename.split('/')
            assert item.compress_type in (0,8)
            assert (item.external_attr>>16)&0o170000!=0o120000
            assert not (item.flag_bits&1),'no encrypted entries'
        packaged={f:z.read(f) for f in names}
    assert packaged==expected, 'released ZIP content does not match sources'
    test_payload(packaged)
    print('PASS: 6 animation overrides, manifest, red overlay, alpha, image states, ZIP safety and reproducibility')
    print('SHA256',hashlib.sha256(OUT.read_bytes()).hexdigest())

if __name__=='__main__': main()
