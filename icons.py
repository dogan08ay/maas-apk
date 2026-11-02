# Maaş Modülü uygulama ikonu üretici (Sağlık çalışanları teması: kırmızı zemin, beyaz sağlık artısı, nabız çizgisi, ₺ parası)
import os,sys
from PIL import Image,ImageDraw
RED=(198,40,40,255);DARK=(142,15,26,255);GOLD=(255,193,7,255);WHITE=(255,255,255,255)
def content(S):
    k=4;N=S*k;im=Image.new('RGBA',(N,N),(0,0,0,0));d=ImageDraw.Draw(im)
    P=lambda x,y:(x*N,y*N);w=lambda v:max(1,int(v*N))
    cx,cy,t,L=.45,.45,.12,.31
    d.rounded_rectangle([P(cx-L,cy-t),P(cx+L,cy+t)],radius=w(.06),fill=WHITE)
    d.rounded_rectangle([P(cx-t,cy-L),P(cx+t,cy+L)],radius=w(.06),fill=WHITE)
    ecg=[(.17,.45),(.27,.45),(.32,.37),(.38,.55),(.44,.34),(.49,.45),(.56,.45)]
    d.line([P(*p) for p in ecg],fill=RED,width=w(.032),joint='curve')
    for p in (ecg[0],ecg[-1]):d.ellipse([P(p[0]-.016,p[1]-.016),P(p[0]+.016,p[1]+.016)],fill=RED)
    mx,my,r=.73,.73,.2
    d.ellipse([P(mx-r-.02,my-r-.02),P(mx+r+.02,my+r+.02)],fill=WHITE)
    d.ellipse([P(mx-r,my-r),P(mx+r,my+r)],fill=GOLD)
    d.ellipse([P(mx-r+.025,my-r+.025),P(mx+r-.025,my+r-.025)],outline=(255,236,160,255),width=w(.012))
    sx=mx-.035;lw=w(.034)
    d.line([P(sx,my-.11),P(sx,my+.035),P(sx+.015,my+.08),P(sx+.055,my+.1),P(sx+.105,my+.1)],fill=DARK,width=lw,joint='curve')
    d.line([P(mx-.1,my-.005),P(mx+.085,my-.05)],fill=DARK,width=lw);d.line([P(mx-.1,my+.04),P(mx+.085,my-.005)],fill=DARK,width=lw)
    return im.resize((S,S),Image.LANCZOS)
def square(S,scale=1.0,mask=None):
    bg=Image.new('RGBA',(S,S),RED);c=content(int(S*scale));bg.alpha_composite(c,((S-c.width)//2,(S-c.height)//2))
    if mask:
        m=Image.new('L',(S*4,S*4),0);dm=ImageDraw.Draw(m)
        (dm.ellipse([0,0,S*4-1,S*4-1],fill=255) if mask=='round' else dm.rounded_rectangle([0,0,S*4-1,S*4-1],radius=S*4*.22,fill=255))
        out=Image.new('RGBA',(S,S),(0,0,0,0));out.paste(bg,mask=m.resize((S,S),Image.LANCZOS));return out
    return bg
def foreground(S):
    s2=int(S*.62);c=content(s2);o=Image.new('RGBA',(S,S),(0,0,0,0));o.alpha_composite(c,((S-s2)//2-int(S*.02),(S-s2)//2-int(S*.02)));return o
def android(res):
    for dn,(lg,ad) in {'mdpi':(48,108),'hdpi':(72,162),'xhdpi':(96,216),'xxhdpi':(144,324),'xxxhdpi':(192,432)}.items():
        p=os.path.join(res,'mipmap-'+dn);os.makedirs(p,exist_ok=True)
        square(lg,.86,'rect').save(p+'/ic_launcher.png');square(lg,.86,'round').save(p+'/ic_launcher_round.png');foreground(ad).save(p+'/ic_launcher_foreground.png')
    os.makedirs(res+'/values',exist_ok=True);open(res+'/values/ic_launcher_background.xml','w').write('<?xml version="1.0" encoding="utf-8"?><resources><color name="ic_launcher_background">#C62828</color></resources>')
    os.makedirs(res+'/mipmap-anydpi-v26',exist_ok=True)
    x='<?xml version="1.0" encoding="utf-8"?><adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android"><background android:drawable="@color/ic_launcher_background"/><foreground android:drawable="@mipmap/ic_launcher_foreground"/></adaptive-icon>'
    for n in('ic_launcher','ic_launcher_round'):open(res+'/mipmap-anydpi-v26/%s.xml'%n,'w').write(x)
    for f in('drawable-v24/ic_launcher_foreground.xml','drawable/ic_launcher_background.xml'):
        q=os.path.join(res,f)
        if os.path.exists(q):os.remove(q)
if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='web':
        square(512,.8).save('icon-512.png');square(192,.8).save('icon-192.png')
    else:android('android/app/src/main/res')
