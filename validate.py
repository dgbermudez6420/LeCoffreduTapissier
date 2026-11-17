from pathlib import Path
from html.parser import HTMLParser
import re, json
root=Path(__file__).parent/'inicio'
class Audit(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.buttons=[];self.sections=[];self.details=0
 def handle_starttag(self,t,attrs):
  d=dict(attrs)
  if t in ['img','script','link']:
   u=d.get('src',d.get('href',''));self.refs.append(u)
  if t=='a':self.buttons.append(d)
  if t=='section':self.sections.append(d.get('id',''))
  if t=='details':self.details+=1
p=Audit();s=(root/'index.html').read_text();p.feed(s)
missing=[u for u in p.refs if u and not u.startswith(('http','#')) and not (root/u).is_file()]
assert not missing,missing
assert '<html lang="fr">' in s
assert p.details==6,p.details
assert len(p.buttons)==2
assert all(a.get('href','').startswith('https://') and a.get('href','').endswith('/checkout') for a in p.buttons)
assert len(set(a['href'] for a in p.buttons))==1
assert not re.search(r'data-upsell(?:-|=)',s)
assert 'the-upholstery-vault.impultienda.ar' not in s
assert '/embed/upsells.js' in s
assert s.count('<script src="tracking.js"></script>') == 1
assert (root/'tracking.js').read_bytes() == (root/'tracking-original.js').read_bytes()
assert len(p.sections)==8,len(p.sections)
for u in p.refs:
 if u.endswith(('.webp','.png','.ttf')):assert (root/u).stat().st_size>100
print(json.dumps({'assets_present':len(set(p.refs)),'faq':p.details,'cta':len(p.buttons),'sections':len(p.sections),'checkout':'French store connected','marketing_tracking':'UTMify reference integrations enabled','lang':'fr'},indent=2))
