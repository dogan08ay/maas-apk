# Maaş Modülü ikon üreticisi: turkuaz zemin, hesap makinesi; ekranda baştan sona kalp ritmi ve köşede ₺
import os,sys
from PIL import Image,ImageDraw
BG=(0,168,181,255);SCREEN=(0,66,82,255);GOLD=(255,193,7,255);WHITE=(255,255,255,255);KEY=(226,232,238,255);KEYSH=(170,180,192,255);OPK=(178,235,242,255);OPSH=(110,185,196,255);PULSE=(110,242,190,255)
def content(S):
    k=4;N=S*k;im=Image.new('RGBA',(N,N),(0,0,0,0));d=ImageDraw.Draw(im)
    P=lambda x,y:(x*N,y*N);w=lambda v:max(1,int(v*N))
    d.rounded_rectangle([P(.22,.112),P(.78,.912)],radius=w(.055),fill=(0,60,70,70))
    d.rounded_rectangle([P(.22,.10),P(.78,.90)],radius=w(.055),fill=WHITE)
    d.rounded_rectangle([P(.27,.15),P(.73,.45)],radius=w(.03),fill=SCREEN)
    # ₺ ekranın sol üst köşesinde
    cx,cy,sc=.352,.238,.58;sx=cx-.035*sc;lw=w(.034*sc)
    d.line([P(sx,cy-.11*sc),P(sx,cy+.035*sc),P(sx+.015*sc,cy+.08*sc),P(sx+.055*sc,cy+.1*sc),P(sx+.105*sc,cy+.1*sc)],fill=GOLD,width=lw,joint='curve')
    d.line([P(cx-.1*sc,cy-.005*sc),P(cx+.085*sc,cy-.05*sc)],fill=GOLD,width=lw);d.line([P(cx-.1*sc,cy+.04*sc),P(cx+.085*sc,cy-.005*sc)],fill=GOLD,width=lw)
    # kalp ritmi: ekranın solundan sağına
    ecg=[(.295,.375),(.40,.375),(.44,.32),(.49,.42),(.545,.265),(.60,.395),(.635,.375),(.705,.375)]
    d.line([P(*p) for p in ecg],fill=PULSE,width=w(.03),joint='curve')
    for p in (ecg[0],ecg[-1]):d.ellipse([P(p[0]-.015,p[1]-.015),P(p[0]+.015,p[1]+.015)],fill=PULSE)
    # tuşlar: 4 sütun, gölgeli
    bw,bh,gx,gy=.095,.1,.028,.03;x0=.268;y0=.505
    def key(c,r,hh=1,fill=KEY,sh=KEYSH):
        x=x0+c*(bw+gx);y=y0+r*(bh+gy);h=bh*hh+gy*(hh-1)
        d.rounded_rectangle([P(x,y+.012),P(x+bw,y+h+.012)],radius=w(.022),fill=sh);d.rounded_rectangle([P(x,y),P(x+bw,y+h)],radius=w(.022),fill=fill);return x,y,h
    for r in range(3):
        for c in range(3):key(c,r)
    x,y,h=key(3,0,fill=OPK,sh=OPSH);mx,my=x+bw/2,y+bh/2;d.line([P(mx-.022,my),P(mx+.022,my)],fill=SCREEN,width=w(.014));d.line([P(mx,my-.022),P(mx,my+.022)],fill=SCREEN,width=w(.014))
    x,y,h=key(3,1,hh=2,fill=GOLD,sh=(205,150,0,255));mx,my=x+bw/2,y+h/2
    d.line([P(mx-.024,my-.016),P(mx+.024,my-.016)],fill=SCREEN,width=w(.016));d.line([P(mx-.024,my+.016),P(mx+.024,my+.016)],fill=SCREEN,width=w(.016))
    return im.resize((S,S),Image.LANCZOS)
def square(S,scale=1.0,mask=None):
    bg=Image.new('RGBA',(S,S),BG);c=content(int(S*scale));bg.alpha_composite(c,((S-c.width)//2,(S-c.height)//2))
    if mask:
        m=Image.new('L',(S*4,S*4),0);dm=ImageDraw.Draw(m)
        (dm.ellipse([0,0,S*4-1,S*4-1],fill=255) if mask=='round' else dm.rounded_rectangle([0,0,S*4-1,S*4-1],radius=S*4*.22,fill=255))
        out=Image.new('RGBA',(S,S),(0,0,0,0));out.paste(bg,mask=m.resize((S,S),Image.LANCZOS));return out
    return bg
def foreground(S):
    s2=int(S*.70);c=content(s2);o=Image.new('RGBA',(S,S),(0,0,0,0));o.alpha_composite(c,((S-s2)//2,(S-s2)//2));return o
def android(res):
    for dn,(lg,ad) in {'mdpi':(48,108),'hdpi':(72,162),'xhdpi':(96,216),'xxhdpi':(144,324),'xxxhdpi':(192,432)}.items():
        p=os.path.join(res,'mipmap-'+dn);os.makedirs(p,exist_ok=True)
        square(lg,.9,'rect').save(p+'/ic_launcher.png');square(lg,.9,'round').save(p+'/ic_launcher_round.png');foreground(ad).save(p+'/ic_launcher_foreground.png')
    os.makedirs(res+'/values',exist_ok=True);open(res+'/values/ic_launcher_background.xml','w').write('<?xml version="1.0" encoding="utf-8"?><resources><color name="ic_launcher_background">#00A8B5</color></resources>')
    os.makedirs(res+'/mipmap-anydpi-v26',exist_ok=True)
    x='<?xml version="1.0" encoding="utf-8"?><adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android"><background android:drawable="@color/ic_launcher_background"/><foreground android:drawable="@mipmap/ic_launcher_foreground"/></adaptive-icon>'
    for n in('ic_launcher','ic_launcher_round'):open(res+'/mipmap-anydpi-v26/%s.xml'%n,'w').write(x)
    for f in('drawable-v24/ic_launcher_foreground.xml','drawable/ic_launcher_background.xml'):
        q=os.path.join(res,f)
        if os.path.exists(q):os.remove(q)
if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='web':
        square(512,.9).save('icon-512.png');square(192,.9).save('icon-192.png')
    else:android('android/app/src/main/res')
