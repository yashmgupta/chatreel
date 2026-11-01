import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'renderer-py'))
import render

class SchemaTests(unittest.TestCase):
    def setUp(self):self.f=json.loads((ROOT/'examples/film.json').read_text())
    def test_schema_and_openapi_share_contract(self):
        import jsonschema,yaml
        schema=json.loads((ROOT/'film-schema.json').read_text());jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.validate(self.f,schema)
        api=yaml.safe_load((ROOT/'openapi.yaml').read_text())
        self.assertEqual(api['components']['schemas']['Film']['properties'],schema['properties'])
    def test_rejects_bad_inputs(self):
        cases=[]
        for k,v in [('width',641),('fps',True),('style','remote-js'),('seed',float('nan')),('url','https://example.com')]:
            f=copy.deepcopy(self.f);f[k]=v;cases.append(f)
        f=copy.deepcopy(self.f);f['scenes']*=21;cases.append(f)
        f=copy.deepcopy(self.f);f['music']['cues'][0]['time']=6;cases.append(f)
        f=copy.deepcopy(self.f);f['scenes'][0]['duration']=30;f['width']=1280;f['height']=720;f['fps']=30;f['scenes']*=4;cases.append(f)
        for f in cases:
            with self.subTest(f=f):
                with self.assertRaises(ValueError):render.validate(f)
    def test_every_style_deterministic_nonblank_and_moves(self):
        import numpy as np
        for style in render.STYLES:
            f=render.validate({**self.f,'style':style});scene=render.Scene(f,f['scenes'][0])
            a=np.asarray(scene.render(1));scene.render(3);b=np.asarray(scene.render(1))
            self.assertTrue(np.array_equal(a,b),style)
            self.assertGreater(float(a.std()),10,style)
            self.assertFalse(np.array_equal(a,np.asarray(scene.render(2))),style)
    def test_five_second_mp4(self):
        with tempfile.TemporaryDirectory() as td:
            result=render.render_film(self.f,td)
            self.assertIsNotNone(result['mp4'])
            probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',result['mp4']]))
            self.assertAlmostEqual(float(probe['format']['duration']),5,delta=.1)
            self.assertEqual({s['codec_type'] for s in probe['streams']},{'video','audio'})
            v=next(s for s in probe['streams'] if s['codec_type']=='video')
            self.assertEqual((v['width'],v['height'],int(v['nb_frames'])),(640,360,120))
            self.assertTrue((Path(td)/'film.srt').read_text().startswith('1\n00:00:00,000 --> 00:00:05,000'))
    def test_missing_encoder_exports_actual_frames(self):
        f={**self.f,'fps':8,'width':320,'height':180,'voice':'tts','webgl':True}
        caps=render.capabilities();caps.update(ffmpeg=None,moviepy=False)
        with tempfile.TemporaryDirectory() as td,patch.object(render,'capabilities',return_value=caps):
            result=render.render_film(f,td)
            self.assertIsNone(result['mp4']);self.assertEqual(len(list((Path(td)/'frames').glob('*.png'))),40)
            self.assertEqual(len(result['warnings']),3)
    def test_broken_encoder_degrades_to_frames(self):
        f={**self.f,'fps':8,'width':320,'height':180}
        with tempfile.TemporaryDirectory() as td,patch.object(render,'encode_frames',side_effect=RuntimeError('codec unavailable')):
            result=render.render_film(f,td)
            self.assertIsNone(result['mp4'])
            self.assertEqual(len(list((Path(td)/'frames').glob('*.png'))),40)
            self.assertIn('Encoder failed',result['warnings'][0])

    def test_voice_mix_and_missing_dependencies(self):
        import numpy as np
        f=render.validate(self.f)
        with tempfile.TemporaryDirectory() as td:
            voice=Path(td)/'user.wav';render.write_wav(voice,np.sin(np.arange(24000)*.1)*.1)
            result=render.render_film(f,Path(td)/'out',voice)
            self.assertIsNotNone(result['mp4'])
        caps=render.capabilities();caps['numpy']=False
        with patch.object(render,'capabilities',return_value=caps):
            with self.assertRaisesRegex(RuntimeError,'required'):render.render_film(f,'unused')

if __name__=='__main__':unittest.main()
