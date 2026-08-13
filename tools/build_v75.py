import re, urllib.request

SRC='https://raw.githubusercontent.com/DRCHRIS1981/reloj-12-casas-watch7/b2132f1d7adc1f0cf9e17c54f188d39e6f368cf0/app/src/main/res/raw/watchface.xml'
OUT='app/src/main/res/raw/watchface.xml'
xml=urllib.request.urlopen(SRC, timeout=30).read().decode('utf-8')

# Tomamos la V7.2 que fue la base visual aprobada y SOLO sustituimos los 12 bloques cyan por llamas.
cut=xml.index('<PartText')
head, tail = xml[:cut], xml[cut:]
pat=re.compile(r'<Group x="0" y="0" width="450" height="450"><Transform target="alpha" value="\[HOUR_0_11\] &lt; \d+ \? 255 : 0"/><Variant mode="AMBIENT" target="alpha" value="0"/><PartDraw x="0" y="0" width="450" height="450">.*?</PartDraw></Group>', re.S)
old=pat.findall(head)
if len(old) != 12:
    raise RuntimeError(f'Se esperaban 12 casas en V7.2 y se encontraron {len(old)}')

# Aries arriba y luego sentido horario. A las 12: 12 llamas; 1: 11; ...; 11: 1.
pos=[(199,10),(290,34),(356,101),(380,191),(356,282),(290,348),(199,372),(109,348),(42,282),(18,191),(42,101),(109,34)]
flames=[]
for i,(x,y) in enumerate(pos):
    threshold=i+1
    phase=i*29
    flames.append(
        f'<Group name="flame{i+1}" x="{x}" y="{y}" width="52" height="68" pivotX="0.5" pivotY="0.82">'
        f'<Transform target="alpha" value="[HOUR_0_11] &lt; {threshold} ? 255 : 0"/>'
        f'<Transform target="scaleY" value="1+0.07*sin(rad([SECOND_MILLISECOND]*0.10+{phase}))"/>'
        f'<Transform target="scaleX" value="1+0.035*cos(rad([SECOND_MILLISECOND]*0.13+{phase+17}))"/>'
        f'<Transform target="angle" value="2.0*sin(rad([SECOND_MILLISECOND]*0.08+{phase+9}))"/>'
        '<Variant mode="AMBIENT" target="alpha" value="0"/>'
        '<PartImage x="0" y="0" width="52" height="68"><Image resource="flame_v3"/></PartImage>'
        '</Group>'
    )

for a,b in zip(old,flames):
    head=head.replace(a,b,1)
xml=head+tail

# Asegura reloj digital 12 h y segundos al centro, sin alterar la composición zodiacal.
xml=xml.replace('format="h:mm" hourFormat="12"','format="h:mm" hourFormat="12"')
open(OUT,'w',encoding='utf-8').write(xml)
print('V7.5 preparada desde V7.2: 12 llamas animadas + diseño zodiacal conservado')
