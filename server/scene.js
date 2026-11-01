// Trusted renderer only. Film data is passed as an argument, never inserted into source.
window.initFilm = (film) => {
  const output=document.getElementById('film');
  output.width=film.width; output.height=film.height;
  const canvas=document.createElement('canvas');
  const pixel=film.style==='pixel-rpg';
  canvas.width=pixel?320:film.width;canvas.height=pixel?180:film.height;
  const ctx=canvas.getContext('2d');
  const w=canvas.width,h=canvas.height;
  let gl, program, texture, loc;
  if(film.webgl){
    gl=output.getContext('webgl',{preserveDrawingBuffer:true});
    if(!gl)throw Error('WebGL unavailable on this host');
    const shader=(type,source)=>{const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw Error(gl.getShaderInfoLog(s));return s;};
    program=gl.createProgram();
    gl.attachShader(program,shader(gl.VERTEX_SHADER,'attribute vec2 p; varying vec2 uv; void main(){gl_Position=vec4(p,0.,1.);uv=vec2((p.x+1.)*.5,(1.-p.y)*.5);}'));
    gl.attachShader(program,shader(gl.FRAGMENT_SHADER,'precision mediump float; varying vec2 uv; uniform sampler2D tex; void main(){gl_FragColor=texture2D(tex,uv);}'));
    gl.linkProgram(program);if(!gl.getProgramParameter(program,gl.LINK_STATUS))throw Error('WebGL link failed');gl.useProgram(program);
    const b=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,b);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);
    loc=gl.getAttribLocation(program,'p');gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,2,gl.FLOAT,false,0,0);
    texture=gl.createTexture();gl.bindTexture(gl.TEXTURE_2D,texture);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.NEAREST);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.NEAREST);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
  }
  const palettes={'swiss-motion':['#f2f0ea','#161616','#e3472b'],'blueprint':['#183b75','#e7f0f9','#e7f0f9'],'chalkboard':['#153b32','#eee7cc','#e2c96c'],'woodcut':['#eee4cd','#171812','#b85b32'],'pixel-rpg':['#172444','#b7d8c8','#e7aa58']};
  const [bg,ink,accent]=palettes[film.style];
  const line=(x,y,a,b,color=ink,width=1)=>{ctx.strokeStyle=color;ctx.lineWidth=width;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(a,b);ctx.stroke();};
  const rect=(x,y,a,b,color)=>{ctx.fillStyle=color;ctx.fillRect(x,y,a,b);};
  const text=(value,x,y,size,color=ink)=>{ctx.font=`${size}px sans-serif`;ctx.fillStyle=color;ctx.fillText(value,x,y);};
  const wrapped=(value,x,y,width,size,maxLines)=>{
    let rows=[];
    for(;size>=8;size--){ctx.font=`${size}px sans-serif`;rows=[];let row='';for(const ch of value){if(ctx.measureText(row+ch).width>width||ch==='\n'){rows.push(row);row=ch==='\n'?'':ch;}else row+=ch;}if(row)rows.push(row);if(rows.length<=maxLines)break;}
    if(rows.length>maxLines)throw Error('Caption cannot fit; shorten text');
    rows.forEach((v,i)=>text(v,x,y+i*size*1.2,size));
  };
  window.render=(time)=>{
    let start=0,index=0;for(;index<film.scenes.length-1;index++){if(time<start+film.scenes[index].duration)break;start+=film.scenes[index].duration;}
    const scene=film.scenes[index],t=Math.max(0,time-start),style=film.style;
    ctx.setTransform(1,0,0,1,0,0);rect(0,0,w,h,bg);
    if(style==='swiss-motion'){
      for(let i=1;i<12;i++)line(w*(.06+.88*i/12),h*.23,w*(.06+.88*i/12),h*.71,'#dedcd5');
      line(w*.06,h*.22,w*.94,h*.22,ink,2);text(String(index+1).padStart(2,'0'),w*.82,h*.15,h*.09);
    }else if(style==='blueprint'){
      for(let x=15;x<w;x+=Math.max(12,w/24))line(x,h*.22,x,h*.70,'#254d83');
      for(let y=h*.22;y<h*.7;y+=Math.max(12,w/24))line(w*.04,y,w*.96,y,'#254d83');
      ctx.strokeStyle=ink;ctx.strokeRect(w*.02,h*.02,w*.96,h*.96);text(`FIG. ${index+1} / REV 01`,w*.73,h*.72,h*.028);
    }else if(style==='chalkboard'){
      ctx.strokeStyle='#795d3b';ctx.lineWidth=Math.max(3,w/80);ctx.strokeRect(3,3,w-6,h-6);line(w*.02,h*.94,w*.98,h*.94,'#997b53',4);
    }else if(style==='woodcut')rect(w*.045,h*.23,w*.91,h*.47,ink);
    else{
      for(let k=0;k<3;k++){const y=h*(.38+k*.10),offset=Math.floor(t*(3+k*2))%32;for(let x=-32;x<w+32;x+=32){ctx.fillStyle=['#283d52','#335454','#487561'][k];ctx.beginPath();ctx.moveTo(x-offset,y+25);ctx.lineTo(x+16-offset,y-8);ctx.lineTo(x+32-offset,y+25);ctx.fill();}}
      rect(0,h*.65,w,h*.07,'#416757');
    }
    // Fixed-seed world texture. No mutable PRNG state between frames.
    if(['woodcut','blueprint','chalkboard'].includes(style)){
      ctx.fillStyle=style==='woodcut'?'rgba(0,0,0,.06)':'rgba(255,255,255,.025)';
      for(let i=0;i<900;i++){const x=((i*127+film.seed*31)%1009)/1009*w,y=((i*263+film.seed*17)%1013)/1013*h;ctx.fillRect(x,y,1,1);}
    }
    scene.objects.forEach((o,j)=>{
      const clock=pixel?Math.floor(t*8)/8:t;let x=o.x*w,y=o.y*h,r=(o.size??.1)*h;
      if(o.motion==='drift')x+=Math.sin(clock*1.3)*w*.035;
      if(o.motion==='pulse')r*=1+.08*Math.sin(clock*3);
      let z=scene.camera==='push'?1+.06*Math.min(t/scene.duration,1):1;
      x=w/2+(x-w/2)*z;y=h*.46+(y-h*.46)*z;r*=z;
      if(scene.camera==='pan')x-=w*.04*t/scene.duration;
      if(pixel){x=Math.round(x);y=Math.round(y);r=Math.round(r);}
      let p=Math.min(1,Math.max(0,(t-j*.035)/.65));if(style==='swiss-motion')p=p*p*(3-2*p);
      ctx.save();ctx.beginPath();ctx.rect(x-r-2,y-r-2,Math.max(0,2*r*p+2),2*r+4);ctx.clip();
      const c=o.accent?accent:ink,outline=['blueprint','chalkboard'].includes(style);
      ctx.fillStyle=c;ctx.strokeStyle=c;ctx.lineWidth=Math.max(1,h*.006);
      const finish=()=>{if(outline){ctx.stroke();}else{if(style==='woodcut'){ctx.fillStyle=ink;ctx.fill();ctx.strokeStyle=o.accent?accent:bg;ctx.stroke();}else ctx.fill();}};
      ctx.beginPath();
      if(o.shape==='circle')ctx.arc(x,y,r,0,Math.PI*2);
      else if(o.shape==='box')ctx.rect(x-r,y-r,2*r,2*r);
      else if(o.shape==='triangle'){ctx.moveTo(x,y-r);ctx.lineTo(x+r,y+r);ctx.lineTo(x-r,y+r);ctx.closePath();}
      else{ctx.ellipse(x,y-r*.7,r*.3,r*.3,0,0,Math.PI*2);finish();ctx.beginPath();ctx.rect(x-r*.35,y-r*.35,r*.7,r*.75);finish();line(x-r*.2,y+r*.35,x-r*.4,y+r,c,Math.max(2,r*.2));line(x+r*.2,y+r*.35,x+r*.4,y+r,c,Math.max(2,r*.2));ctx.beginPath();}
      finish();
      if(style==='woodcut')for(let k=0;k<10;k++){let rr=r*(.4+k*.065);ctx.beginPath();ctx.strokeStyle=o.accent?accent:bg;ctx.lineWidth=Math.max(1,h*.005);if(o.shape==='box'){const yy=y-r+r*.12*k;ctx.moveTo(x-r*.88,yy);ctx.lineTo(x-r*.15,yy+r*.4);}else ctx.arc(x,y,rr,200*Math.PI/180,340*Math.PI/180);ctx.stroke();}
      ctx.restore();
      if(style==='blueprint'&&p===1){const yy=y+r+8;line(x-r,yy,x+r,yy);line(x-r,yy-4,x-r,yy+4);line(x+r,yy-4,x+r,yy+4);text(`${j+1} / ${Math.round(r*2)}`,x-r,yy+12,h*.026);}
    });
    wrapped(scene.title,w*.07,h*.12,w*.70,h*.07,2);
    if(scene.narration){
      if(pixel){rect(10,133,300,41,bg);ctx.strokeStyle=ink;ctx.lineWidth=2;ctx.strokeRect(10,133,300,41);}
      else if(style==='blueprint'){ctx.strokeStyle=ink;ctx.lineWidth=1;ctx.strokeRect(w*.055,h*.76,w*.89,h*.17);}
      else if(!['woodcut','swiss-motion'].includes(style))line(w*.07,h*.75,w*.93,h*.75);
      wrapped(scene.narration,w*.09,pixel?148:h*.83,w*.82,h*.048,3);
    }
    if(gl){gl.bindTexture(gl.TEXTURE_2D,texture);gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,canvas);gl.drawArrays(gl.TRIANGLE_STRIP,0,4);}
    else{const c=output.getContext('2d');c.imageSmoothingEnabled=!pixel;c.drawImage(canvas,0,0,film.width,film.height);}
  };
  window.render(0);return true;
};
