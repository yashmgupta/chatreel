"""Educational fidelity checks, not just a nonblank-frame smoke test."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'renderer-py'))
import render
from education import TEMPLATES,THEMES,calculate,compile_scene,pillow_frame,evaluated_ops,svg_frame

class EducationalTests(unittest.TestCase):
    def sample(self,name):return json.loads((ROOT/'templates'/f'{name}.json').read_text())
    def plan(self,name):
        f=render.validate(self.sample(name));return compile_scene(f,f['scenes'][0])
    def test_all_eighteen_templates_preflight_and_random_access_frames(self):
        self.assertEqual(len(TEMPLATES),18)
        for name in TEMPLATES:
            with self.subTest(template=name):
                f=render.validate(self.sample(name));renderer=render.FilmRenderer(f)
                a=np.asarray(renderer.frame(2));renderer.frame(.1);b=np.asarray(renderer.frame(2))
                self.assertTrue(np.array_equal(a,b));self.assertGreater(float(a.std()),10)
                p=renderer.scenes[0].plan;self.assertIn('<svg',svg_frame(p,3))
                for box in p.boxes:self.assertGreaterEqual(box['size'],14) # 14 only for source footer; content uses >=23.
    def test_every_template_has_safe_portrait_layout(self):
        for name in TEMPLATES:
            with self.subTest(template=name):
                f=self.sample(name);f.update(width=720,height=1280)
                p=compile_scene(f,f['scenes'][0])
                self.assertEqual(p.metrics['design_size'],[720,1280])

    def test_themes_preserve_numeric_geometry(self):
        f=self.sample('bar-chart');reference=None
        for theme in THEMES:
            f['style']=theme;p=compile_scene(f,f['scenes'][0]);geometry=p.metrics['bar_widths']
            if reference is None:reference=geometry
            self.assertEqual(geometry,reference)
    def test_bar_values_and_zero_baseline_are_proportional(self):
        p=self.plan('bar-chart');v=p.metrics['values'];w=p.metrics['bar_widths']
        for a,b in zip(v,w):self.assertAlmostEqual(b/w[-1],a/v[-1])
        self.assertGreater(p.metrics['zero_baseline'],0)
    def test_actual_raster_bar_lengths_match_supplied_values(self):
        from PIL import ImageColor
        f=self.sample('bar-chart');f['style']='studio';p=compile_scene(f,f['scenes'][0])
        im=np.asarray(pillow_frame(p,4,1280,720))
        baseline=p.metrics['zero_baseline'];values=p.metrics['values']
        for i,width in enumerate(p.metrics['bar_widths']):
            y=round(235+(i+.44)*(340/len(values)))
            color=ImageColor.getrgb(THEMES['studio']['accent' if i==1 else 'secondary'])
            row=im[y];distance=np.max(np.abs(row.astype(int)-np.array(color)),axis=1)
            pixels=np.where((distance<=32)&(np.arange(len(row))>=baseline-3)&(np.arange(len(row))<=baseline+max(p.metrics['bar_widths'])+3))[0]
            self.assertGreater(len(pixels),0)
            self.assertAlmostEqual(len(pixels),width,delta=2)
            self.assertAlmostEqual(pixels[0],baseline,delta=3)
    def test_code_indentation_and_monospaced_layout_are_preserved(self):
        f=self.sample('code-walkthrough');f['scenes'][0]['content']['code']='for i in range(3):\n    print(i)'
        p=compile_scene(f,f['scenes'][0]);ops=[o for o in p.ops if o.get('mono')]
        self.assertEqual(len(ops),2)
        self.assertEqual(ops[1]['text'],'02      print(i)')

    def test_line_chart_has_linear_scale_and_explicit_zero(self):
        p=self.plan('line-chart');lo,hi=p.metrics['minimum'],p.metrics['maximum']
        self.assertEqual(lo,0)
        points=p.metrics['points'];values=p.metrics['values']
        scales=[(points[i][1]-points[0][1])/(values[i]-values[0]) for i in range(1,len(values))]
        self.assertTrue(all(abs(s-scales[0])<1e-6 for s in scales))
    def test_parts_sum_to_whole_and_equal_area_fraction(self):
        donut=self.plan('donut-chart').metrics
        self.assertAlmostEqual(sum(donut['sector_radians']),2*np.pi)
        fraction=self.plan('fraction').metrics
        self.assertEqual((fraction['filled_cells'],fraction['total_cells']),(3,8))
    def test_arithmetic_is_exact_and_does_not_execute_code(self):
        self.assertEqual(str(calculate('distance / time',{'distance':120,'time':2})),'60')
        self.assertEqual(str(calculate('0.1 + 0.2',{})),'0.3')
        for text in ['not valid(', '__import__("os").getcwd()','1/0','2**100','(1).__class__','[1][0]']:
            with self.subTest(text=text):
                with self.assertRaises((ValueError,SyntaxError)):calculate(text,{})
        f=self.sample('equation');f['scenes'][0]['content']['result']=61
        with self.assertRaisesRegex(ValueError,'does not match'):render.validate(f)
    def test_rounded_numbers_are_not_presented_as_exact_equalities(self):
        f=self.sample('equation');f['scenes'][0]['content']={'expression':'1 / 3'}
        p=compile_scene(f,f['scenes'][0]);text=' '.join(o['text'] for o in p.ops if o['op']=='text')
        self.assertIn('≈ 0.3333',text)
        f=self.sample('fraction');f['scenes'][0]['content'].update(numerator=1,denominator=3)
        p=compile_scene(f,f['scenes'][0]);text=' '.join(o['text'] for o in p.ops if o['op']=='text')
        self.assertIn('≈ 33.33%',text)
        from education import fmt
        self.assertNotEqual(fmt(0.000001),'0')
        f=self.sample('equation');f['scenes'][0]['content']={'expression':'2**3'}
        p=compile_scene(f,f['scenes'][0]);self.assertTrue(any(o.get('text')=='2^3' for o in p.ops))

    def test_unknown_or_inconsistent_content_fails(self):
        cases=[]
        f=self.sample('donut-chart');f['scenes'][0]['content']['items'][0]['value']=-1;cases.append(f)
        f=self.sample('number-line');f['scenes'][0]['content']['maximum']=-10;cases.append(f)
        f=self.sample('fraction');f['scenes'][0]['content']['numerator']=9;cases.append(f)
        f=self.sample('bar-chart');f['scenes'][0]['content']['data_kind']='sourced';cases.append(f)
        f=self.sample('quiz');f['scenes'][0]['content']['correct']=3;cases.append(f)
        f=self.sample('title');f['scenes'][0]['duration']=1;cases.append(f)
        f=self.sample('title');f['scenes'][0]['content']['body']='Unbreakable'*20;cases.append(f)
        f=self.sample('title');f['scenes'][0]['content']['body']='漢字';cases.append(f)
        for f in cases:
            with self.subTest(f=f['scenes'][0]['template']):
                with self.assertRaises(ValueError):render.validate(f)
    def test_portrait_and_production_defaults(self):
        f=self.sample('process');f.update(width=720,height=1280)
        p=compile_scene(f,f['scenes'][0]);im=pillow_frame(p,3,720,1280)
        self.assertEqual(im.size,(720,1280))
        f=self.sample('equation');f.pop('width');f.pop('height');f.pop('fps');f['profile']='production'
        f=render.validate(f);self.assertEqual((f['width'],f['height'],f['fps']),(1920,1080,30))
    def test_template_math_metadata_and_svg_are_exported_with_real_mp4(self):
        f=self.sample('equation');f.update(width=640,height=360,fps=12);f['scenes'][0]['duration']=5
        with tempfile.TemporaryDirectory() as td:
            result=render.render_film(f,td);self.assertIsNotNone(result['mp4'])
            quality=json.loads((Path(td)/'quality.json').read_text());self.assertEqual(quality['encoding']['status'],'passed')
            self.assertEqual(quality['encoding']['frames'],60)
            metrics=json.loads((Path(td)/'scene-metrics.json').read_text());self.assertEqual(metrics[0]['result'],'60')
            self.assertTrue((Path(td)/'scene-01.svg').exists())

if __name__=='__main__':unittest.main()
