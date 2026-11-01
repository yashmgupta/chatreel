// Original trusted display-list interpreter. No source code is accepted from callers.
window.initDisplayList = ({width,height,designWidth,designHeight}) => {
  const canvas=document.getElementById('film');canvas.width=width;canvas.height=height;
  const c=canvas.getContext('2d');
  window.drawDisplayList=ops=>{
    c.setTransform(width/designWidth,0,0,height/designHeight,0,0);
    c.clearRect(0,0,designWidth,designHeight);
    for(const o of ops){
      c.save();c.globalAlpha=o.opacity;c.fillStyle=o.fill||'transparent';c.strokeStyle=o.stroke||o.fill||'transparent';
      c.lineWidth=o.stroke_width||o.width||1;c.lineCap='round';c.lineJoin='round';
      if(o.op==='rect'){
        c.beginPath();c.roundRect(o.x,o.y,Math.max(0,o.w),Math.max(0,o.h),Math.max(0,Math.min(o.radius||0,o.w/2,o.h/2)));
        if(o.fill)c.fill();if(o.stroke)c.stroke();
      }else if(o.op==='ellipse'){
        c.beginPath();c.ellipse(o.x+o.w/2,o.y+o.h/2,o.w/2,o.h/2,0,0,Math.PI*2);if(o.fill)c.fill();if(o.stroke)c.stroke();
      }else if(o.op==='line'||o.op==='polygon'){
        c.beginPath();o.points.forEach(([x,y],i)=>i?c.lineTo(x,y):c.moveTo(x,y));
        if(o.op==='polygon'){c.closePath();c.fill();}else c.stroke();
      }else if(o.op==='text'){
        c.font=`${o.bold?700:400} ${o.size}px ${o.mono?"ChatreelMono":"Chatreel"}`;c.textBaseline='alphabetic';c.fillText(o.text,o.x,o.y);
      }else throw new Error('Unknown trusted display primitive');
      c.restore();
    }
  };
};
