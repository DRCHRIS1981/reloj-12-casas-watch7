import re, urllib.request

SRC='https://raw.githubusercontent.com/DRCHRIS1981/reloj-12-casas-watch7/b2132f1d7adc1f0cf9e17c54f188d39e6f368cf0/app/src/main/res/raw/watchface.xml'
OUT='app/src/main/res/raw/watchface.xml'
xml=urllib.request.urlopen(SRC, timeout=30).read().decode('utf-8')

# Base visual: V7.2 aprobada. Solo reemplazamos los 12 bloques cyan por llamas.
cut=xml.index('<PartText')
head, tail = xml[:cut], xml[cut:]
pat=re.compile(r'<Group x="0" y="0" width="450" height="450"><Transform target="alpha" value="\[HOUR_0_11\] &lt; \d+ \? 255 : 0"/><Variant mode="AMBIENT" target="alpha" value="0"/><PartDraw x="0" y="0" width="450" height="450">.*?</PartDraw></Group>', re.S)
old=pat.findall(head)
if len(old) != 12:
    raise RuntimeError(f'Se esperaban 12 casas en V7.2 y se encontraron {len(old)}')

# Aries arriba y después sentido horario. 12:00=12 encendidas, 1:00=11, ..., 11:00=1.
pos=[(197,8),(289,33),(357,101),(382,188),(357,279),(289,347),(197,372),(105,347),(37,279),(12,188),(37,101),(105,33)]
flames=[]
for i,(x,y) in enumerate(pos):
    threshold=12-i
    base=i*30
    # Tres fotogramas alternan cada segundo. Esto produce un movimiento visible y fiable en Wear OS.
    frames=[]
    frame_specs=[
        (0, 2, 4, 52, 68, base-3),
        (1, 1, 1, 54, 72, base),
        (2, 3, 5, 50, 66, base+3),
    ]
    for secmod,fx,fy,fw,fh,ang in frame_specs:
        frames.append(
            f'<Group x="0" y="0" width="58" height="76">'
            f'<Transform target="alpha" value="[SECOND] % 3 == {secmod} ? 255 : 0"/>'
            f'<PartImage x="{fx}" y="{fy}" width="{fw}" height="{fh}" angle="{ang}"><Image resource="flame_v3"/></PartImage>'
            '</Group>'
        )
    flames.append(
        f'<Group name="flame{i+1}" x="{x}" y="{y}" width="58" height="76" pivotX="0.5" pivotY="0.70">'
        f'<Transform target="alpha" value="[HOUR_0_11] &lt; {threshold} ? 255 : 0"/>'
        '<Variant mode="AMBIENT" target="alpha" value="0"/>'
        + ''.join(frames) +
        '</Group>'
    )

for a,b in zip(old,flames):
    head=head.replace(a,b,1)
xml=head+tail
open(OUT,'w',encoding='utf-8').write(xml)
print('V7.7 preparada desde V7.2: 12 llamas cyan con animacion visible de 3 fotogramas')
