"""Original, model-free educational scene compiler shared by Pillow/Canvas/SVG.

Coordinates are design units. Scenes compile once; only animation progress changes
per frame. Layout is inspected before encoding, never silently clipped or shrunk.
"""
from __future__ import annotations
import ast
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation, localcontext
from functools import lru_cache
import html
import math
from pathlib import Path

FONTS = Path(__file__).parent/'assets/fonts'
THEMES = {
    'studio': {'bg':'#f5f3ed','panel':'#ffffff','ink':'#182b3a','muted':'#536675','accent':'#c94726','secondary':'#126d7c','grid':'#dce2e4'},
    'midnight': {'bg':'#101a2b','panel':'#19283f','ink':'#f1f6fc','muted':'#b0c1d6','accent':'#67dfd1','secondary':'#f5b572','grid':'#2b3d55'},
    'paper': {'bg':'#f5eee0','panel':'#fffbf3','ink':'#302a27','muted':'#685e53','accent':'#b44334','secondary':'#336c68','grid':'#dbd1bf'},
    'ocean': {'bg':'#eef7fa','panel':'#ffffff','ink':'#163e53','muted':'#486c7c','accent':'#006d9a','secondary':'#a65020','grid':'#c8e0e8'},
    'coral': {'bg':'#fff1ed','panel':'#ffffff','ink':'#452d38','muted':'#755768','accent':'#b63d50','secondary':'#216c70','grid':'#ecd6d1'},
    'violet': {'bg':'#f3f0fd','panel':'#ffffff','ink':'#302449','muted':'#685b7b','accent':'#7041b5','secondary':'#177476','grid':'#dfd7ec'},
    'swiss-motion': {'bg':'#f2f0ea','panel':'#ffffff','ink':'#161616','muted':'#5a5a55','accent':'#c73b22','secondary':'#4d5964','grid':'#dedcd5'},
    'blueprint': {'bg':'#173a72','panel':'#204981','ink':'#f0f6fd','muted':'#c4d8ef','accent':'#ffffff','secondary':'#a2d5fa','grid':'#34598c'},
    'chalkboard': {'bg':'#153b32','panel':'#1d493d','ink':'#f6efd8','muted':'#cbd6c0','accent':'#f0d173','secondary':'#a4d5c9','grid':'#356052'},
    'woodcut': {'bg':'#eee4cd','panel':'#f7eedb','ink':'#171812','muted':'#625b49','accent':'#a34425','secondary':'#3e6157','grid':'#d0c4ab'},
    'pixel-rpg': {'bg':'#172444','panel':'#233657','ink':'#e0eee3','muted':'#bdcdcf','accent':'#f3bc68','secondary':'#8bdbbf','grid':'#394f6d'},
}
TEMPLATES = {
 'title':'Lesson opener with a visual concept and subtitle',
 'concept':'A central idea connected to explanatory cards',
 'process':'Ordered steps with directional connections',
 'cycle':'A closed sequence with curved directional connections',
 'comparison':'Two sides with aligned points of comparison',
 'timeline':'Dated milestones placed in supplied order',
 'bar-chart':'Zero-baseline bars whose lengths encode supplied values',
 'line-chart':'A labelled numeric series with a shared linear scale',
 'donut-chart':'Nonnegative values normalized to a complete whole',
 'equation':'Restricted arithmetic expression, verified substitutions and result',
 'number-line':'Numeric values positioned on an explicit number line',
 'fraction':'Exact numerator out of denominator as equal-area cells',
 'labeled-diagram':'Central illustration with explicit callouts and leaders',
 'solar-energy':'Simplified sunlight → PV DC → inverter AC → home flow',
 'water-cycle':'Evaporation, condensation, precipitation and collection',
 'recap':'A readable summary with numbered takeaways',
 'quiz':'Question, delayed reveal and an explicit correct option',
 'code-walkthrough':'Literal code with line numbers and explanatory notes',
}
ICONS = ['sun','panel','inverter','home','battery','cloud','water','plant','book','lightbulb','atom','globe','gear','check']


@lru_cache(maxsize=256)
def font(size, bold=False, mono=False):
    from PIL import ImageFont
    return ImageFont.truetype(str(FONTS/('DejaVuSansMono.ttf' if mono else 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')),int(size))


@lru_cache(maxsize=4096)
def glyph_available(character):
    if character.isspace():return True
    return bytes(font(32).getmask(character))!=bytes(font(32).getmask('\U0010ffff'))


def fmt(number):
    d=Decimal(str(number))
    if abs(d)>=Decimal('1000000000') or (d and abs(d)<Decimal('0.0001')):return f'{float(d):.4g}'
    return f'{d:,.4f}'.rstrip('0').rstrip('.') if d%1 else f'{d:,.0f}'


def calculate(expression, variables):
    """Evaluate arithmetic only. No calls, attributes, indexing, code or builtins."""
    if len(expression)>100:raise ValueError('Expression exceeds 100 characters')
    try:tree=ast.parse(expression,mode='eval')
    except SyntaxError as e:raise ValueError('Expression is not valid arithmetic') from e
    if sum(1 for _ in ast.walk(tree))>40:raise ValueError('Expression too complex')
    def visit(n):
        if isinstance(n,ast.Expression):return visit(n.body)
        if isinstance(n,ast.Constant) and type(n.value) in (int,float):return Decimal(str(n.value))
        if isinstance(n,ast.Name) and n.id in variables:return Decimal(str(variables[n.id]))
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.UAdd,ast.USub)):
            return visit(n.operand)*(1 if isinstance(n.op,ast.UAdd) else -1)
        if isinstance(n,ast.BinOp) and isinstance(n.op,(ast.Add,ast.Sub,ast.Mult,ast.Div,ast.Pow)):
            a,b=visit(n.left),visit(n.right)
            if isinstance(n.op,ast.Add):v=a+b
            elif isinstance(n.op,ast.Sub):v=a-b
            elif isinstance(n.op,ast.Mult):v=a*b
            elif isinstance(n.op,ast.Div):v=a/b
            else:
                if b!=int(b) or abs(b)>6:raise ValueError('Exponent must be an integer between -6 and 6')
                v=a**int(b)
            if not v.is_finite() or abs(v)>Decimal('1e15'):raise ValueError('Arithmetic result exceeds supported range')
            return v
        raise ValueError('Only arithmetic and declared variable names are supported')
    try:
        with localcontext() as ctx:
            ctx.prec=28
            result=visit(tree)
            if not result.is_finite() or abs(result)>Decimal('1e15'):raise ValueError('Arithmetic result exceeds supported range')
            return result
    except (InvalidOperation,ArithmeticError,OverflowError) as e:raise ValueError('Invalid arithmetic (including division by zero)') from e


def ease(t):
    t=max(0.,min(1.,t));return t*t*(3-2*t)


@dataclass
class Plan:
    width:int
    height:int
    ops:list=field(default_factory=list)
    boxes:list=field(default_factory=list)
    metrics:dict=field(default_factory=dict)
    def add(self, kind, *, enter=0., span=.45, effect='rise', **kw):
        self.ops.append(dict(op=kind,enter=enter,span=span,effect=effect,**kw))
    def rect(self,x,y,w,h,fill,*,radius=0,stroke=None,stroke_width=1,**kw):
        self.add('rect',x=x,y=y,w=w,h=h,fill=fill,radius=radius,stroke=stroke,stroke_width=stroke_width,**kw)
    def line(self,points,fill,width=3,**kw):self.add('line',points=points,fill=fill,width=width,**kw)
    def ellipse(self,x,y,w,h,fill,*,stroke=None,stroke_width=2,**kw):
        self.add('ellipse',x=x,y=y,w=w,h=h,fill=fill,stroke=stroke,stroke_width=stroke_width,**kw)
    def polygon(self,points,fill,**kw):self.add('polygon',points=points,fill=fill,**kw)
    def text(self,value,x,y,w,h,size=30,*,fill='#182b3a',bold=False,align='left',min_size=23,**kw):
        text=str(value)
        if not text:return
        if any(ord(ch)<32 and ch not in '\n\t' for ch in text):raise ValueError('Text contains control characters')
        unsupported=next((ch for ch in text if not glyph_available(ch)),None)
        if unsupported is not None:raise ValueError(f'Bundled font lacks glyph {unsupported!r}; use supported text or add a licensed font')
        # Measure with the actual bundled font. Never wrap in the middle of words.
        final=None
        for fs in range(int(size),int(min_size)-1,-1):
            ft=font(fs,bold);rows=[]
            for paragraph in text.split('\n'):
                row=''
                for word in paragraph.expandtabs(4).split(' '):
                    if ft.getlength(word)>w:break
                    trial=(row+' '+word).strip()
                    if ft.getlength(trial)>w:rows.append(row);row=word
                    else:row=trial
                else:rows.append(row);continue
                break
            else:
                ascent,descent=ft.getmetrics();step=fs*1.28
                if len(rows)*step<=h:final=(fs,ft,rows,ascent,step);break
        if final is None:raise ValueError(f'Text does not fit readable bounds: {text[:65]!r}; shorten it or use fewer items')
        fs,ft,rows,ascent,step=final
        for i,row in enumerate(rows):
            length=ft.getlength(row);xx=x if align=='left' else x+(w-length)/2 if align=='center' else x+w-length
            self.add('text',text=row,x=xx,y=y+i*step+ascent,size=fs,bold=bold,fill=fill,**kw)
            self.boxes.append({'text':row,'x':xx,'y':y+i*step,'w':length,'h':step,'size':fs})
    def arrow(self,a,b,color,width=3,**kw):
        self.line([a,b],color,width,**kw)
        angle=math.atan2(b[1]-a[1],b[0]-a[0]);size=11
        self.polygon([b,(b[0]-size*math.cos(angle-.5),b[1]-size*math.sin(angle-.5)),(b[0]-size*math.cos(angle+.5),b[1]-size*math.sin(angle+.5))],color,**kw)


def icon(p,name,cx,cy,r,color,enter=0):
    """Original vector pictograms; they are diagrams, not downloaded assets."""
    opts=dict(enter=enter,effect='draw');lw=max(3,r*.07)
    if name=='sun':
        p.ellipse(cx-r*.4,cy-r*.4,r*.8,r*.8,color,**opts)
        for i in range(8):
            a=i*math.tau/8;p.line([(cx+math.cos(a)*r*.62,cy+math.sin(a)*r*.62),(cx+math.cos(a)*r*.94,cy+math.sin(a)*r*.94)],color,lw,**opts)
    elif name=='panel':
        p.rect(cx-r*.85,cy-r*.58,r*1.7,r*1.15,None,stroke=color,stroke_width=lw,radius=r*.06,**opts)
        for i in range(1,4):p.line([(cx-r*.85+r*1.7*i/4,cy-r*.58),(cx-r*.85+r*1.7*i/4,cy+r*.57)],color,lw*.5,**opts)
        p.line([(cx-r*.85,cy),(cx+r*.85,cy)],color,lw*.5,**opts)
        p.line([(cx,cy+r*.58),(cx,cy+r*.88),(cx+r*.5,cy+r*.88),(cx-r*.5,cy+r*.88)],color,lw,**opts)
    elif name=='home':
        p.line([(cx-r*.9,cy-r*.05),(cx,cy-r*.85),(cx+r*.9,cy-r*.05)],color,lw,**opts)
        p.rect(cx-r*.65,cy-r*.1,r*1.3,r*.95,None,stroke=color,stroke_width=lw,**opts)
        p.rect(cx-r*.18,cy+r*.25,r*.36,r*.6,None,stroke=color,stroke_width=lw*.7,**opts)
    elif name=='cloud':
        for dx,dy,rr in [(-.45,0,.4),(0,-.25,.55),(.48,0,.38)]:p.ellipse(cx+(dx-rr)*r,cy+(dy-rr)*r,rr*2*r,rr*2*r,color,**opts)
        p.rect(cx-r*.7,cy,r*1.4,r*.3,color,**opts)
    elif name=='water':
        p.polygon([(cx,cy-r),(cx-r*.65,cy+r*.3),(cx-r*.45,cy+r*.75),(cx,cy+r*.9),(cx+r*.45,cy+r*.75),(cx+r*.65,cy+r*.3)],color,**opts)
    elif name=='plant':
        p.line([(cx,cy+r*.9),(cx,cy-r*.8)],color,lw,**opts)
        p.ellipse(cx-r*.8,cy-r*.5,r*.8,r*.4,color,**opts);p.ellipse(cx,cy-r*.05,r*.8,r*.4,color,**opts)
        p.line([(cx-r*.7,cy+r*.9),(cx+r*.7,cy+r*.9)],color,lw,**opts)
    elif name=='battery':
        p.rect(cx-r*.8,cy-r*.5,r*1.5,r,None,stroke=color,stroke_width=lw,radius=r*.1,**opts)
        p.rect(cx+r*.7,cy-r*.18,r*.2,r*.36,color,**opts)
        p.line([(cx-r*.4,cy),(cx+r*.25,cy)],color,lw,**opts);p.line([(cx-r*.05,cy-r*.23),(cx-r*.05,cy+r*.23)],color,lw,**opts)
    elif name=='book':
        p.line([(cx-r*.9,cy-r*.7),(cx,cy-r*.45),(cx+r*.9,cy-r*.7),(cx+r*.9,cy+r*.65),(cx,cy+r*.9),(cx-r*.9,cy+r*.65),(cx-r*.9,cy-r*.7)],color,lw,**opts)
        p.line([(cx,cy-r*.45),(cx,cy+r*.9)],color,lw,**opts)
    elif name=='lightbulb':
        p.ellipse(cx-r*.6,cy-r*.85,r*1.2,r*1.2,None,stroke=color,stroke_width=lw,**opts)
        for i in range(3):p.line([(cx-r*.3,cy+r*(.35+i*.2)),(cx+r*.3,cy+r*(.35+i*.2))],color,lw,**opts)
    elif name=='globe':
        p.ellipse(cx-r*.9,cy-r*.9,r*1.8,r*1.8,None,stroke=color,stroke_width=lw,**opts)
        p.ellipse(cx-r*.4,cy-r*.9,r*.8,r*1.8,None,stroke=color,stroke_width=lw*.65,**opts)
        p.line([(cx-r*.9,cy),(cx+r*.9,cy)],color,lw*.65,**opts)
    elif name=='atom':
        for angle in [0,math.pi/3,-math.pi/3]:
            points=[]
            for i in range(49):
                a=i*math.tau/48;x=r*.9*math.cos(a);y=r*.35*math.sin(a)
                points.append((cx+x*math.cos(angle)-y*math.sin(angle),cy+x*math.sin(angle)+y*math.cos(angle)))
            p.line(points,color,lw*.65,**opts)
        p.ellipse(cx-r*.13,cy-r*.13,r*.26,r*.26,color,**opts)
    elif name=='check':p.line([(cx-r*.7,cy),(cx-r*.15,cy+r*.6),(cx+r*.8,cy-r*.65)],color,lw*1.8,**opts)
    elif name=='inverter':
        p.rect(cx-r*.78,cy-r*.85,r*1.56,r*1.7,None,stroke=color,stroke_width=lw,radius=r*.1,**opts)
        p.line([(cx-r*.5,cy-r*.35),(cx-r*.05,cy-r*.35)],color,lw*.7,**opts)
        p.line([(cx-r*.5,cy-r*.15),(cx-r*.05,cy-r*.15)],color,lw*.7,**opts)
        p.line([(cx-r*.5+i*r/24,cy+r*.35+math.sin(i*math.tau/24)*r*.17) for i in range(25)],color,lw*.7,**opts)
    else:
        for i in range(10):
            a=i*math.tau/10;p.line([(cx+math.cos(a)*r*.7,cy+math.sin(a)*r*.7),(cx+math.cos(a)*r,cy+math.sin(a)*r)],color,lw*1.7,**opts)
        p.ellipse(cx-r*.6,cy-r*.6,r*1.2,r*1.2,None,stroke=color,stroke_width=lw,**opts)
        p.ellipse(cx-r*.2,cy-r*.2,r*.4,r*.4,None,stroke=color,stroke_width=lw,**opts)


def validate_content(scene):
    name=scene['template'];c=scene.get('content',{});items=c.get('items',[])
    if not scene['title'].strip():raise ValueError('Educational scenes need a readable title')
    if scene['duration']<4:raise ValueError('Educational templates need at least 4 seconds for reveal and reading')
    minimum={'concept':2,'process':2,'cycle':3,'comparison':2,'timeline':2,'bar-chart':2,'line-chart':2,'donut-chart':2,'number-line':1,'labeled-diagram':2,'recap':1,'quiz':2}
    if name in minimum and len(items)<minimum[name]:raise ValueError(f'{name}: supply at least {minimum[name]} content.items')
    maximum={'comparison':2,'process':5,'cycle':5,'concept':4,'timeline':5,'recap':5,'quiz':4,'labeled-diagram':4,'donut-chart':6,'number-line':6,'bar-chart':6,'line-chart':8}
    if len(items)>maximum.get(name,8):raise ValueError(f'{name}: too many items; split this lesson into scenes')
    numeric=['bar-chart','line-chart','donut-chart','number-line']
    if name in numeric:
        if any('value' not in i for i in items):raise ValueError(f'{name}: every item needs a numeric value')
        if name in ('bar-chart','donut-chart') and any(i['value']<0 for i in items):raise ValueError(f'{name}: values must be nonnegative')
        if name=='donut-chart' and sum(i['value'] for i in items)<=0:raise ValueError('Donut total must be positive')
        if c.get('data_kind','illustrative')=='sourced' and not c.get('source'):raise ValueError('Sourced data needs a source label and URL')
    if name=='number-line':
        if c.get('maximum',10)<=c.get('minimum',0):raise ValueError('Number line maximum must exceed minimum')
        if any(not c.get('minimum',0)<=i['value']<=c.get('maximum',10) for i in items):raise ValueError('Number-line marker lies outside its declared range')
        vals=sorted(i['value'] for i in items)
        if any(b-a<(c.get('maximum',10)-c.get('minimum',0))*.08 for a,b in zip(vals,vals[1:])):raise ValueError('Number-line labels are too close; split markers into scenes')
    if name=='fraction':
        n,d=c.get('numerator'),c.get('denominator')
        if n is None or d is None or d<1 or d>24 or n<0 or n>d:raise ValueError('Fraction requires 0 <= numerator <= denominator <= 24')
    if name=='equation':
        if not c.get('expression'):raise ValueError('Equation needs content.expression')
        result=calculate(c['expression'],c.get('variables',{}))
        if 'result' in c and abs(result-Decimal(str(c['result'])))>Decimal('0.000001'):raise ValueError('Supplied equation result does not match the expression')
    if name=='quiz' and not 0<=c.get('correct',-1)<len(items):raise ValueError('Quiz needs a valid zero-based correct option')
    if name=='code-walkthrough' and not c.get('code'):raise ValueError('Code walkthrough needs content.code')
    if c.get('source') and not c['source']['url'].startswith('https://'):raise ValueError('Source URL must use HTTPS (it is recorded, never fetched)')


def compile_scene(film,scene,index=0):
    """Build a resolution-independent scene with checked typography and geometry."""
    validate_content(scene)
    vertical=film['height']>film['width'];W=720 if vertical else 1280;H=round(W*film['height']/film['width'])
    p=Plan(W,H);theme=THEMES[film['style']];c=scene.get('content',{});name=scene['template'];items=c.get('items',[])
    bg,panel,ink,muted,acc,second,grid=[theme[k] for k in ('bg','panel','ink','muted','accent','secondary','grid')]
    margin=52 if not vertical else 40
    p.rect(0,0,W,H,bg,effect='none')
    p.rect(0,0,12,H,acc,effect='none')
    p.text(c.get('eyebrow','CHATREEL / LEARN IN MOTION').upper(),margin,28,W-margin*2-80,28,19,min_size=17,fill=muted,bold=True,effect='none')
    p.text(f'{index+1:02}',W-margin-60,28,60,28,20,min_size=18,fill=acc,bold=True,align='right',effect='none')
    p.text(scene['title'],margin,78,W-margin*2,110 if vertical else 90,48 if vertical else 49,min_size=36,fill=ink,bold=True,enter=.05)
    if c.get('subtitle'):p.text(c['subtitle'],margin,192 if vertical else 156,W-margin*2,70 if vertical else 45,27,min_size=24,fill=muted,enter=.15)
    top=300 if vertical else 235;bottom=H-(210 if vertical else 145);area=bottom-top
    x0,x1=margin,W-margin;AW=x1-x0
    p.line([(margin,H-116),(W-margin,H-116)],grid,1,effect='none')
    caption=scene.get('narration','')
    if caption:p.text(caption,margin,H-100,AW,69,26,min_size=24,fill=ink,enter=.05,effect='none')
    source=c.get('source')
    foot=(source['label'] if source else 'ILLUSTRATIVE DATA' if name in ('bar-chart','line-chart','donut-chart') else 'CODE-RENDERED / NO GENERATIVE MODELS')
    p.text(foot,margin,H-28,AW,23,16,min_size=14,fill=muted,effect='none')
    delay=lambda i:.25+i*.18
    def card(x,y,w,h,label,detail='',number=None,icon_name=None,i=0):
        p.rect(x,y,w,h,panel,radius=18,stroke=grid,enter=delay(i))
        if number is not None:
            p.text(str(number).zfill(2),x+22,y+18,w-44,45,30,min_size=25,fill=acc,bold=True,enter=delay(i)+.1)
        if icon_name:icon(p,icon_name,x+w/2,y+65,36,acc,delay(i)+.1)
        ly=y+(120 if icon_name else 76 if number is not None else 25)
        p.text(label,x+22,ly,w-44,min(85,h-(ly-y)-18),30,min_size=24,fill=ink,bold=True,enter=delay(i)+.12)
        if detail:p.text(detail,x+22,ly+85,w-44,h-(ly-y)-100,25,min_size=23,fill=muted,enter=delay(i)+.2)
    if name=='title':
        icon(p,c.get('icon','lightbulb'),W/2,top+area*.35,min(AW*.19,area*.26),acc,.2)
        p.text(c.get('body','A clear idea. One step at a time.'),margin+AW*.08,top+area*.70,AW*.84,area*.28,38,min_size=28,fill=ink,bold=True,align='center',enter=.5)
    elif name=='concept':
        if vertical:
            for i,item in enumerate(items):card(x0,top+i*(area/len(items)),AW,area/len(items)-14,item['label'],item.get('detail',''),number=i+1,i=i)
        else:
            count=len(items);gap=18;cw=(AW-gap*(count-1))/count
            for i,item in enumerate(items):card(x0+i*(cw+gap),top,cw,area,item['label'],item.get('detail',''),icon_name=item.get('icon','book'),i=i)
    elif name in ('process','solar-energy'):
        steps=items if name=='process' else [{'label':'Sunlight','detail':'Photons reach the panel','icon':'sun'},{'label':'PV panel','detail':'Produces DC electricity','icon':'panel'},{'label':'Inverter','detail':'Converts DC into AC','icon':'inverter'},{'label':'Home','detail':'Uses AC electricity','icon':'home'}]
        n=len(steps)
        if vertical:
            sh=area/n
            for i,item in enumerate(steps):
                cy=top+(i+.5)*sh;icon(p,item.get('icon','gear'),x0+50,cy,32,acc,delay(i))
                p.text(item['label'],x0+115,cy-35,AW-140,40,30,min_size=25,fill=ink,bold=True,enter=delay(i))
                p.text(item.get('detail',''),x0+115,cy+8,AW-140,55,24,min_size=23,fill=muted,enter=delay(i)+.1)
                if i<n-1:p.arrow((x0+50,cy+42),(x0+50,cy+sh-42),second,3,enter=delay(i)+.25,effect='draw')
        else:
            cw=AW/n
            for i,item in enumerate(steps):
                cx=x0+(i+.5)*cw;cy=top+area*.28;icon(p,item.get('icon','gear'),cx,cy,48,acc,delay(i))
                if i<n-1:
                    a,b=(cx+68,cy),(cx+cw-68,cy)
                    p.arrow(a,b,second,3,enter=delay(i)+.2,effect='draw')
                    p.ellipse(a[0]-4,a[1]-4,8,8,acc,enter=1.2,travel=[a,b],period=2.4,phase=i*.25)
                p.text(item['label'],cx-cw*.46,top+area*.56,cw*.92,55,29,min_size=24,fill=ink,bold=True,align='center',enter=delay(i)+.1)
                p.text(item.get('detail',''),cx-cw*.45,top+area*.78,cw*.9,area*.22,24,min_size=23,fill=muted,align='center',enter=delay(i)+.2)
        if name=='solar-energy':p.metrics['simplification']='Energy-flow diagram, not installation wiring; battery/storage omitted.'
    elif name in ('cycle','water-cycle'):
        steps=items if name=='cycle' else [{'label':'Evaporation','icon':'water'},{'label':'Condensation','icon':'cloud'},{'label':'Precipitation','icon':'water'},{'label':'Collection','icon':'globe'}]
        cx,cy=W/2,top+area/2;rx=AW*.32;ry=area*.32
        coords=[]
        for i,item in enumerate(steps):
            a=-math.pi/2+i*math.tau/len(steps);x=cx+rx*math.cos(a);y=cy+ry*math.sin(a);coords.append((x,y))
            icon(p,item.get('icon','gear'),x,y,33,acc,delay(i))
            p.text(item['label'],x-125,y+48,250,70,26,min_size=23,fill=ink,bold=True,align='center',enter=delay(i)+.1)
        for i in range(len(steps)):
            a=-math.pi/2+(i+.18)*math.tau/len(steps);b=-math.pi/2+(i+.78)*math.tau/len(steps)
            points=[(cx+rx*math.cos(a+(b-a)*j/24),cy+ry*math.sin(a+(b-a)*j/24)) for j in range(25)]
            p.line(points,second,3,enter=delay(i)+.25,effect='draw');p.arrow(points[-2],points[-1],second,3,enter=delay(i)+.25,effect='draw')
            p.ellipse(points[0][0]-4,points[0][1]-4,8,8,acc,enter=1.2,travel=points,period=2.4,phase=i*.25)
        p.metrics['sequence']=[i['label'] for i in steps]
    elif name=='comparison':
        gap=24;cw=(AW-gap)/2
        for i,item in enumerate(items):card(x0+i*(cw+gap),top,cw,area,item['label'],item.get('detail',''),icon_name=item.get('icon','book'),i=i)
    elif name=='timeline':
        if vertical:
            xx=x0+32;p.line([(xx,top+12),(xx,bottom-20)],grid,4,effect='draw',enter=.2)
            for i,item in enumerate(items):
                yy=top+(i+.2)*area/len(items);p.ellipse(xx-9,yy,18,18,acc,enter=delay(i))
                p.text(item['label'],xx+35,yy-6,AW-100,48,28,min_size=24,fill=ink,bold=True,enter=delay(i))
                p.text(item.get('detail',''),xx+35,yy+45,AW-100,area/len(items)-55,24,min_size=23,fill=muted,enter=delay(i)+.1)
        else:
            yy=top+60;p.line([(x0+20,yy),(x1-20,yy)],grid,4,effect='draw',enter=.2);cw=AW/len(items)
            for i,item in enumerate(items):
                xx=x0+(i+.5)*cw;p.ellipse(xx-9,yy-9,18,18,acc,enter=delay(i))
                p.text(item['label'],x0+i*cw+10,yy+35,cw-20,85,29,min_size=24,fill=ink,bold=True,align='center',enter=delay(i))
                p.text(item.get('detail',''),x0+i*cw+10,yy+130,cw-20,area-200,24,min_size=23,fill=muted,align='center',enter=delay(i)+.1)
    elif name=='bar-chart':
        values=[i['value'] for i in items];maximum=max(values) or 1
        labelw=AW*.23;chartx=x0+labelw;chartw=AW*.62;rowh=area/len(items)
        for tick in range(5):
            x=chartx+chartw*tick/4;p.line([(x,top),(x,bottom-18)],grid,1,effect='none')
            p.text(fmt(maximum*tick/4),x-34,top-32,68,28,19,min_size=18,fill=muted,align='center',effect='none')
        for i,item in enumerate(items):
            y=top+i*rowh;p.text(item['label'],x0,y+rowh*.22,labelw-18,rowh*.66,26,min_size=23,fill=ink,enter=delay(i))
            width=chartw*item['value']/maximum
            p.rect(chartx,y+rowh*.2,width,rowh*.48,acc if i==values.index(max(values)) else second,radius=5,enter=delay(i),effect='grow-x')
            p.text(fmt(item['value'])+(' '+c['unit'] if c.get('unit') else ''),chartx+width+12,y+rowh*.22,AW*.14,rowh*.65,24,min_size=23,fill=ink,bold=True,enter=delay(i)+.3)
        p.metrics.update(values=values,bar_widths=[chartw*v/maximum for v in values],zero_baseline=chartx,maximum=maximum)
    elif name=='line-chart':
        values=[i['value'] for i in items];lo=min(0,min(values));hi=max(0,max(values))
        if c.get('unit'):p.text('Units: '+c['unit'],x0,top-32,AW,28,19,min_size=18,fill=muted,effect='none')
        if hi<=lo:hi=lo+1
        left=x0+85;right=x1-35;yt=top+12;yb=bottom-60
        for i in range(5):
            val=lo+(hi-lo)*i/4;y=yb-(yb-yt)*i/4;p.line([(left,y),(right,y)],grid,1,effect='none');p.text(fmt(val),x0,y-12,70,30,20,min_size=18,fill=muted,align='right',effect='none')
        points=[(left+(right-left)*i/(len(items)-1),yb-(v-lo)/(hi-lo)*(yb-yt)) for i,v in enumerate(values)]
        p.line(points,acc,5,enter=.3,span=1.1,effect='draw')
        for i,(x,y) in enumerate(points):
            p.ellipse(x-6,y-6,12,12,acc,enter=delay(i)+.35)
            p.text(fmt(values[i]),max(left-30,min(right-70,x-35)),max(top-5,y-42),90,32,22,min_size=20,fill=ink,bold=True,enter=delay(i)+.4)
            # Stagger labels if needed, without changing point positions.
            p.text(items[i]['label'],x-55,yb+20,110,40,22,min_size=19,fill=muted,align='center',enter=delay(i))
        p.metrics.update(values=values,points=points,minimum=lo,maximum=hi)
    elif name=='donut-chart':
        total=sum(i['value'] for i in items);cx=x0+AW*(.5 if vertical else .25);cy=top+area*(.25 if vertical else .5);radius=min(AW*.2,area*(.23 if vertical else .43));angle=-math.pi/2
        colors=[acc,second,ink,muted,'#8f9d69','#a17d9b']
        for i,item in enumerate(items):
            sweep=math.tau*item['value']/total;points=[(cx,cy)]+[(cx+radius*math.cos(angle+sweep*j/64),cy+radius*math.sin(angle+sweep*j/64)) for j in range(65)]
            p.polygon(points,colors[i],enter=delay(i));angle+=sweep
            ly=top+area*.55+i*45 if vertical else top+i*area/len(items)
            lx=x0 if vertical else x0+AW*.52
            p.rect(lx,ly+8,14,14,colors[i],enter=delay(i))
            p.text(f"{item['label']}  ·  {fmt(item['value'])} ({item['value']/total*100:.1f}%)",lx+28,ly,AW*(.94 if vertical else .45),43,25,min_size=23,fill=ink,enter=delay(i))
        p.ellipse(cx-radius*.60,cy-radius*.60,radius*1.2,radius*1.2,bg,enter=.15)
        p.text(fmt(total),cx-radius*.5,cy-24,radius,60,32,min_size=26,fill=ink,bold=True,align='center',enter=.5)
        p.metrics.update(values=[i['value'] for i in items],total=total,sector_radians=[math.tau*i['value']/total for i in items])
    elif name=='equation':
        expression=c['expression'];variables=c.get('variables',{});result=calculate(expression,variables)
        p.rect(x0,top,AW,area,panel,radius=20,stroke=grid,enter=.15)
        p.text(expression.replace('**','^').replace('*',' × ').replace('/',' ÷ '),x0+36,top+30,AW-72,100,47,min_size=32,fill=ink,bold=True,align='center',enter=.2)
        substitution='   '.join(f'{k} = {fmt(v)}'+(' '+c['variable_units'][k] if k in c.get('variable_units',{}) else '') for k,v in variables.items())
        p.text(substitution or 'Evaluate the expression',x0+36,top+145,AW-72,90,29,min_size=24,fill=muted,align='center',enter=.45)
        display_result=fmt(result)
        relation='=' if Decimal(display_result.replace(',',''))==result else '≈'
        p.text(relation+' '+display_result+(' '+c['unit'] if c.get('unit') else ''),x0+36,top+area*.68,AW-72,area*.3,55,min_size=35,fill=acc,bold=True,align='center',enter=.9)
        p.metrics.update(expression=expression,result=str(result),variables=variables)
    elif name=='number-line':
        minimum=c.get('minimum',0);maximum=c.get('maximum',10);left=x0+40;right=x1-40;yy=top+area*.48
        p.arrow((left,yy),(right,yy),ink,3,enter=.2,effect='draw')
        for i in range(6):
            x=left+(right-left)*i/5;v=minimum+(maximum-minimum)*i/5;p.line([(x,yy-9),(x,yy+9)],muted,2,enter=.2)
            p.text(fmt(v),x-38,yy+24,76,40,23,min_size=20,fill=muted,align='center',enter=.25)
        positions=[]
        for i,item in enumerate(items):
            x=left+(item['value']-minimum)/(maximum-minimum)*(right-left);positions.append(x)
            p.ellipse(x-9,yy-9,18,18,acc,enter=delay(i)+.3)
            p.text(item['label']+' = '+fmt(item['value']),max(x0,min(x1-170,x-85)),yy-95-(i%2)*55,170,80,25,min_size=23,fill=ink,bold=True,align='center',enter=delay(i)+.3)
        p.metrics.update(values=[i['value'] for i in items],positions=positions,minimum=minimum,maximum=maximum)
    elif name=='fraction':
        n,d=c['numerator'],c['denominator'];cols=min(8,d);rows=math.ceil(d/cols);gap=10;size=min((AW-gap*(cols-1))/cols,(area*.6-gap*(rows-1))/rows);sx=W/2-(cols*size+(cols-1)*gap)/2
        for i in range(d):p.rect(sx+(i%cols)*(size+gap),top+(i//cols)*(size+gap),size,size,acc if i<n else panel,radius=6,stroke=grid,enter=.25+i*.035)
        percentage=Decimal(n)*100/Decimal(d);rounded=percentage.quantize(Decimal('.01'))
        relation='=' if percentage==rounded else '≈'
        p.text(f'{n} / {d}  {relation}  {rounded:.2f}%',x0,top+area*.73,AW,area*.25,46,min_size=32,fill=ink,bold=True,align='center',enter=1.1)
        p.metrics.update(numerator=n,denominator=d,filled_cells=n,total_cells=d)
    elif name=='labeled-diagram':
        cx=W/2;cy=top+area*.4;icon(p,c.get('icon','atom'),cx,cy,min(AW*.12,area*.23),acc,.25)
        for i,item in enumerate(items):
            leftside=i%2==0;y=top+(i//2)*area*.56;xx=x0 if leftside else x0+AW*.72;cw=AW*.28
            p.text(item['label'],xx,y,cw,75,27,min_size=23,fill=ink,bold=True,enter=delay(i)+.2)
            if item.get('detail'):p.text(item['detail'],xx,y+82,cw,area*.38-82,23,min_size=23,fill=muted,enter=delay(i)+.3)
            p.line([((xx+cw) if leftside else xx,y+42),(cx+(-AW*.15 if leftside else AW*.15),cy)],second,2,enter=delay(i)+.2,effect='draw')
    elif name=='recap':
        rh=area/len(items)
        for i,item in enumerate(items):
            icon(p,'check',x0+24,top+(i+.35)*rh,17,acc,delay(i))
            p.text(item['label'],x0+65,top+i*rh,AW-80,rh-10,32,min_size=25,fill=ink,bold=True,enter=delay(i))
    elif name=='quiz':
        p.text(c.get('body','Choose the correct answer.'),x0,top,AW,85,32,min_size=27,fill=ink,bold=True,enter=.2)
        rh=(area-105)/len(items);reveal=max(1.5,scene['duration']*.55)
        for i,item in enumerate(items):
            y=top+100+i*rh;p.rect(x0,y,AW,rh-12,panel,radius=10,stroke=grid,enter=delay(i))
            p.text(f'{chr(65+i)}.  {item["label"]}',x0+25,y+12,AW-95,rh-24,27,min_size=23,fill=ink,enter=delay(i)+.1)
            if i==c['correct']:icon(p,'check',x1-35,y+(rh-12)/2,17,acc,reveal)
        p.metrics['correct']=c['correct']
    elif name=='code-walkthrough':
        code=c['code'].expandtabs(4).splitlines()
        if len(code)>9:raise ValueError('Code walkthrough supports at most 9 lines per scene')
        p.rect(x0,top,AW,area,panel,radius=16,stroke=grid,enter=.15)
        step=min(45,(area-40)/len(code))
        for i,line in enumerate(code):
            literal=f'{i+1:02}  {line}'
            fs=26
            while fs>23 and font(fs,mono=True).getlength(literal)>AW-50:fs-=1
            length=font(fs,mono=True).getlength(literal)
            if length>AW-50:raise ValueError('Code line too long; split it into shorter lines')
            ascent=font(fs,mono=True).getmetrics()[0]
            yy=top+20+i*step
            p.add('text',text=literal,x=x0+25,y=yy+ascent,size=fs,bold=False,mono=True,fill=acc if i==c.get('highlight',0) else ink,enter=delay(i))
            p.boxes.append({'text':literal,'x':x0+25,'y':yy,'w':length,'h':step,'size':fs})
        p.metrics['code_lines']=len(code)
    for box in p.boxes:
        if box['x']<0 or box['y']<0 or box['x']+box['w']>W+.1 or box['y']+box['h']>H+.1:raise ValueError('Text outside frame: '+box['text'])
    body_chars=sum(len(b['text']) for b in p.boxes if 60<=b['y']<H-116)
    reading_seconds=round(max(4,1.5+(body_chars+len(caption)*.5)/22),1)
    for i,a in enumerate(p.boxes):
        for b in p.boxes[i+1:]:
            dx=min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x'])
            dy=min(a['y']+a['h'],b['y']+b['h'])-max(a['y'],b['y'])
            if dx>2 and dy>3:raise ValueError(f'Text labels overlap: {a["text"][:35]!r} and {b["text"][:35]!r}; shorten labels or split the scene')
    p.metrics.update(template=name,text_boxes=p.boxes,design_size=[W,H],recommended_duration=reading_seconds,
        reading_review='increase duration' if scene['duration']<reading_seconds else 'sufficient by heuristic')
    return p


def evaluated_ops(plan,t):
    result=[]
    for raw in plan.ops:
        op=dict(raw);effect=op.pop('effect');enter=op.pop('enter');span=op.pop('span')
        progress=1 if effect=='none' else ease((t-enter)/span)
        if progress<=0:continue
        travel=op.pop('travel',None);period=op.pop('period',2.4);phase=op.pop('phase',0)
        if travel:
            q=((t-enter)/period+phase)%1;lengths=[math.dist(a,b) for a,b in zip(travel,travel[1:])];distance=sum(lengths)*q
            for a,b,length in zip(travel,travel[1:],lengths):
                if distance>length:distance-=length;continue
                k=distance/length if length else 0;op['x']=a[0]+(b[0]-a[0])*k-op['w']/2;op['y']=a[1]+(b[1]-a[1])*k-op['h']/2;break
        op['opacity']=1 if effect in ('none','draw','grow-x') else progress
        if effect=='rise':
            offset=(1-progress)*12
            if 'y' in op:op['y']+=offset
        if effect=='grow-x':op['w']*=progress
        if effect=='draw' and op['op']=='line':
            points=op['points'];lengths=[math.dist(a,b) for a,b in zip(points,points[1:])];target=sum(lengths)*progress
            sliced=[points[0]]
            for a,b,length in zip(points,points[1:],lengths):
                if target>=length:sliced.append(b);target-=length
                else:
                    q=target/length if length else 0;sliced.append((a[0]+(b[0]-a[0])*q,a[1]+(b[1]-a[1])*q));break
            op['points']=sliced
        result.append(op)
    return result


def pillow_frame(plan,t,width,height,supersample=2):
    from PIL import Image,ImageDraw
    scale=min(width/plan.width,height/plan.height)*supersample
    # Design ratio follows the output so no hidden cropping or stretching.
    ow,oh=width*supersample,height*supersample
    im=Image.new('RGB',(ow,oh),'#ffffff');d=ImageDraw.Draw(im)
    sx=ow/plan.width;sy=oh/plan.height
    for op in evaluated_ops(plan,t):
        opacity=op['opacity']
        layer=Image.new('RGBA',im.size) if opacity<1 else None
        draw=ImageDraw.Draw(layer if layer is not None else im)
        color=op.get('fill');stroke=op.get('stroke');kind=op['op']
        if kind in ('rect','ellipse'):
            x,y,w,h=op['x']*sx,op['y']*sy,op['w']*sx,op['h']*sy
            box=(x,y,x+max(0,w),y+max(0,h));lw=max(1,round(op.get('stroke_width',1)*min(sx,sy)))
            if kind=='ellipse':draw.ellipse(box,fill=color,outline=stroke,width=lw)
            elif op.get('radius',0):draw.rounded_rectangle(box,radius=min(op['radius']*min(sx,sy),w/2,h/2),fill=color,outline=stroke,width=lw)
            else:draw.rectangle(box,fill=color,outline=stroke,width=lw)
        elif kind in ('line','polygon'):
            points=[(x*sx,y*sy) for x,y in op['points']]
            if kind=='polygon':draw.polygon(points,fill=color)
            elif len(points)>1:draw.line(points,fill=color,width=max(1,round(op['width']*min(sx,sy))),joint='curve')
        elif kind=='text':
            draw.text((op['x']*sx,op['y']*sy),op['text'],font=font(max(1,round(op['size']*min(sx,sy))),op['bold'],op.get('mono',False)),fill=color,anchor='ls')
        if layer is not None:
            layer.putalpha(layer.getchannel('A').point(lambda a:round(a*opacity)));im.paste(layer,(0,0),layer)
    return im.resize((width,height),Image.Resampling.LANCZOS) if supersample>1 else im


def svg_frame(plan,t):
    """Inspectable standalone vectors; text fonts can be embedded by the exporter."""
    rows=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {plan.width} {plan.height}">']
    for o in evaluated_ops(plan,t):
        typ=o['op'];fill=o.get('fill') or 'none';attrs=f'fill="{fill}" opacity="{o["opacity"]:.5f}"'
        if typ in ('rect','ellipse'):
            attrs+=f' stroke="{o.get("stroke") or "none"}" stroke-width="{o.get("stroke_width",1)}"'
            if typ=='rect':rows.append(f'<rect x="{o["x"]}" y="{o["y"]}" width="{o["w"]}" height="{o["h"]}" rx="{o.get("radius",0)}" {attrs}/>')
            else:rows.append(f'<ellipse cx="{o["x"]+o["w"]/2}" cy="{o["y"]+o["h"]/2}" rx="{o["w"]/2}" ry="{o["h"]/2}" {attrs}/>')
        elif typ in ('line','polygon'):
            points=' '.join(f'{x},{y}' for x,y in o['points'])
            if typ=='line':rows.append(f'<polyline points="{points}" fill="none" stroke="{fill}" stroke-width="{o["width"]}" opacity="{o["opacity"]}"/>')
            else:rows.append(f'<polygon points="{points}" {attrs}/>')
        elif typ=='text':
            family='DejaVu Sans Mono' if o.get('mono') else 'DejaVu Sans'
            rows.append(f'<text x="{o["x"]}" y="{o["y"]}" font-family="{family}" font-size="{o["size"]}" font-weight="{700 if o["bold"] else 400}" {attrs}>{html.escape(o["text"])}</text>')
    rows.append('</svg>');return '\n'.join(rows)

class PreparedScene:
    """Cache finished static layers; recompute only genuine motion during holds."""
    def __init__(self,plan,width,height):
        self.plan,self.width,self.height=plan,width,height
        self.moving=[op for op in plan.ops if op.get('travel')]
        self.static=[op for op in plan.ops if not op.get('travel')]
        self.settle=max((op['enter']+op['span'] for op in plan.ops if op['effect']!='none'),default=0)
        self.background=None
    def render(self,t):
        if t<self.settle:return pillow_frame(self.plan,t,self.width,self.height)
        if self.background is None:
            base=Plan(self.plan.width,self.plan.height,ops=self.static)
            self.background=pillow_frame(base,self.settle,self.width,self.height)
        im=self.background.copy()
        if not self.moving:return im
        from PIL import Image,ImageDraw
        dynamic=Plan(self.plan.width,self.plan.height,ops=self.moving)
        sx,sy=self.width/self.plan.width,self.height/self.plan.height
        for op in evaluated_ops(dynamic,t):
            x,y,w,h=op['x']*sx,op['y']*sy,op['w']*sx,op['h']*sy
            ix,iy=math.floor(x)-2,math.floor(y)-2;pw,ph=math.ceil(w)+5,math.ceil(h)+5
            patch=Image.new('RGBA',(pw*2,ph*2));d=ImageDraw.Draw(patch)
            d.ellipse(((x-ix)*2,(y-iy)*2,(x-ix+w)*2,(y-iy+h)*2),fill=op['fill'])
            patch=patch.resize((pw,ph),Image.Resampling.LANCZOS);im.paste(patch,(ix,iy),patch)
        return im
